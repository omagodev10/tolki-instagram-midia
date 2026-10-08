"""mix_motion.py: monta o áudio do motion (Reel ou anúncio): voz + música remixada + efeitos.
Uso: python3 <repo>/tools/reel-motion/mix_motion.py job.json   (dentro da pasta do motion; substitui o build_audio.py)
Precisa: pip install --break-system-packages pyloudnorm  (numpy e scipy já vêm)

job.json:
{
 "lines": [{"text": "frase 1", "audio": "a/l1.wav"}, ...],      # uma fala por cena (saída do split_take.py)
 "gap_first": 0.2, "gap": 0.25, "tail": 1.6,                      # respiros (s)
 "music": {"song": "songs/sna", "rel_db": -15,                    # pasta com inst.mp4 (ou inst.wav) e song.json
           "cues": [{"scene": 3, "kind": "drop"},                  # a parte forte da música entra na cena 3
                    {"scene": 5, "at": -0.15, "kind": "break"},    # some (filtro de DJ) logo antes do CTA
                    {"scene": 5, "at": 1.2, "kind": "hit"}]},      # volta com tudo no "Comenta"
   ou "music": {"file": "trilha.mp3", "offset": 0, "rel_db": -15}  # trilha simples, sem remix
   ou sem "music"                                                  # vídeo só com voz e efeitos
 "sfx_dir": "lib", "sfx": [{"name": "SFX_WHOOSH", "scene": 2, "at": -0.05, "gain": 0.5}, ...]
}
"scene": i usa o início da cena i (o B[i] do reel.html: start - 0.15; cena 0 = 0); "at" soma segundos.
A música fica ~15 dB abaixo da voz na faixa do celular, com o meio cavado para a voz passar,
sobe 4 dB nos respiros e 8 dB no final. Saídas: timing.json (gen_reel.py / gen_ad.py) e mix.wav (-14 LUFS, -1 dBTP)."""
import json, subprocess, sys, os, numpy as np, pyloudnorm as pyln
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, lfilter
SR = 48000
J = json.load(open(sys.argv[1], encoding='utf-8'))
def load(p, ch=1):
    a = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', p, '-ac', str(ch), '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32).astype(np.float64)
    return a.reshape(-1, ch) if ch > 1 else a
meter = pyln.Meter(SR)

# ---- voice lines, each normalized to the same loudness ----
L = J['lines']; t = 0.0; sc = []; vs = []
for i, l in enumerate(L):
    t += J.get('gap_first', 0.2) if i == 0 else J.get('gap', 0.25)
    v = load(l['audio']); v *= 10 ** ((-18 - meter.integrated_loudness(v)) / 20)
    sc.append({'text': l['text'], 'start': round(t, 3), 'dur': round(len(v) / SR, 3)}); vs.append((t, v)); t += len(v) / SR
total = round(t + J.get('tail', 1.6), 3); N = int(total * SR)
json.dump({'scenes': sc, 'total': total}, open('timing.json', 'w'), ensure_ascii=False, indent=1)
voice = np.zeros(N)
for t0, v in vs: s = int(t0 * SR); voice[s:s + len(v)] += v[:N - s]
B = [0.0] + [s['start'] - 0.15 for s in sc[1:]]

# ---- music: instrumental, carve the voice lane, level vs voice in the phone band ----
def peq(x, f0, g, q):
    a_ = 10 ** (g / 40); w = 2 * np.pi * f0 / SR; al = np.sin(w) / (2 * q)
    b = np.array([1 + al * a_, -2 * np.cos(w), 1 - al * a_]); a = np.array([1 + al / a_, -2 * np.cos(w), 1 - al / a_])
    return lfilter(b / a[0], a / a[0], x, axis=0)
def shelf(x, f0, g):
    a_ = 10 ** (g / 40); w = 2 * np.pi * f0 / SR; al = np.sin(w) / 2 * np.sqrt(2); c = np.cos(w); r = 2 * np.sqrt(a_) * al
    b = np.array([a_ * ((a_ + 1) - (a_ - 1) * c + r), 2 * a_ * ((a_ - 1) - (a_ + 1) * c), a_ * ((a_ + 1) - (a_ - 1) * c - r)])
    a = np.array([(a_ + 1) + (a_ - 1) * c + r, -2 * ((a_ - 1) + (a_ + 1) * c), (a_ + 1) + (a_ - 1) * c - r])
    return lfilter(b / a[0], a / a[0], x, axis=0)
mus = np.zeros((N, 2))
if J.get('music'):
    M = J['music']
    if M.get('song'):   # remix: arrange the song so drops/breaks/hits land on the video cues
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import music_edit
        cues = [{'t': sc[c['scene']]['start'] + c.get('at', 0.0), 'kind': c['kind'], 'song_t': c.get('song_t')} for c in M.get('cues', [])]
        src = next((os.path.join(M['song'], f) for f in ('inst.wav', 'inst.mp4', 'inst.m4a', 'inst.mp3') if os.path.exists(os.path.join(M['song'], f))), None)
        if not src: sys.exit('sem instrumental em ' + M['song'] + ' (inst.wav, inst.mp4, inst.m4a ou inst.mp3)')
        music_edit.arrange(src, os.path.join(M['song'], 'song.json'), cues, total, '_music.wav')
        M = dict(M, file='_music.wav', offset=0)
        mm = load('_music.wav', 1)                       # check: each cue should change the music level
        lv = lambda a, b: 20 * np.log10(np.sqrt((mm[int(max(0, a) * SR):int(b * SR)] ** 2).mean()) + 1e-9)
        for c in cues:
            d = lv(c['t'] + .1, c['t'] + 1.1) - lv(c['t'] - 1.0, c['t'] - .1)
            ok = (d >= 3) if c['kind'] in ('drop', 'hit') else (d <= -6)
            print(f"cue {c['kind']:5s} {c['t']:6.2f}s: música {d:+.1f} dB {'ok' if ok else 'FRACO (troque o cue ou a música)'}")
    m = load(M['file'], 2); s0 = int(M.get('offset', 0) * SR); m = m[s0:s0 + N]; mus[:len(m)] = m
    mus = shelf(mus, 140, -3); mus = peq(mus, 2600, -5, .7); mus = peq(mus, 1100, -2.5, 1.0); mus = peq(mus, 350, -2, 1.0)
    pb = butter(4, [300, 8000], 'bandpass', fs=SR, output='sos')
    act = np.convolve((np.abs(voice) > 10 ** (-40 / 20)).astype(float), np.ones(int(.25 * SR)), 'same') > 0
    vb = sosfilt(pb, voice); mb = sosfilt(pb, mus.mean(1))
    loud = np.convolve(np.abs(mb), np.ones(4800) / 4800, 'same') > 10 ** (-40 / 20)
    g_talk = 10 * np.log10((vb[act] ** 2).mean()) + M.get('rel_db', -15) - 10 * np.log10((mb[loud] ** 2).mean() + 1e-12)
    tt = np.arange(N) / SR
    gdb = np.where(act, g_talk, g_talk + 4.0); gdb = np.where(tt > sc[-1]['start'] + sc[-1]['dur'] + .05, g_talk + 8.0, gdb)
    def sm(x, ta, tr, cr=1000):  # one-pole smoothing (fast attack, slow release) at a 1 kHz control rate
        h = SR // cr; xc = x[::h]; y = np.empty_like(xc); y[0] = xc[0]
        ka, kr = np.exp(-1 / (ta * cr)), np.exp(-1 / (tr * cr))
        for i in range(1, len(xc)):
            k = ka if xc[i] < y[i - 1] else kr; y[i] = k * y[i - 1] + (1 - k) * xc[i]
        return np.interp(np.arange(len(x)), np.arange(len(xc)) * h, y)
    gdb = sm(gdb, .04, .3)
    env = 10 ** (gdb / 20) * np.clip(tt / .3, 0, 1) * np.clip((total - tt) / 1.2, 0, 1) ** 1.5
    mus *= env[:, None]
    print(f'music gain talk {g_talk:.1f} dB')

# ---- sfx ----
fx = np.zeros((N, 2))
for e in J.get('sfx', []):
    s = load(os.path.join(J.get('sfx_dir', 'lib'), e['name'] + '.mp3'), 2) * e.get('gain', .5)
    a = int(max(0, B[e.get('scene', 0)] + e.get('at', 0)) * SR); fx[a:a + len(s)] += s[:N - a]
vact = np.convolve(np.abs(voice), np.ones(2400) / 2400, 'same'); vact = np.clip(vact / (np.percentile(vact[vact > 1e-4], 90) + 1e-9), 0, 1)
fx *= (1 - .4 * vact)[:, None]

mix = np.stack([voice, voice], 1) + mus + fx * .8
mix *= 10 ** ((-14 - meter.integrated_loudness(mix)) / 20)
wavfile.write('_pre.wav', SR, mix.astype(np.float32))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '_pre.wav', '-af', 'alimiter=limit=0.89:attack=3:release=60:level=false', '-c:a', 'pcm_s16le', 'mix.wav'], check=True)
os.remove('_pre.wav')
fin = wavfile.read('mix.wav')[1].astype(np.float64) / 32768
print('total', total, 'LUFS', round(meter.integrated_loudness(fin), 1), 'peak', round(20 * np.log10(np.abs(fin).max()), 1), 'scenes', [(s['start'], s['dur']) for s in sc])
