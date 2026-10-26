"""Voz contínua no PADRÃO DE VOZ DA TOLKI de 26/10/2026 (tools/reel-motion/VOZ_PADRAO_TOLKI.md).
python3 voz_continua.py roteiro.json WORK [--takes 3]
roteiro.json: {"hook": 0, "falas": [{"texto": "..."}, ...]}  (voz e estilo são fixos do padrão; "voz"/"estilo" do roteiro são ignorados)
1. Uma tomada só para o texto inteiro (as falas juntas), voz pt-br-commercial-7, estilo fixo em inglês. Gera N tomadas.
2. Transcreve cada tomada (Parakeet), descarta as que ficaram mais de 4 pontos abaixo da melhor e, entre as que sobram,
   fica com a de menor deriva de tom (altura média da voz por trechos de 5 s).
3. Apara só o silêncio do começo e do fim, acelera o áudio inteiro em 1,20x e aplica um ganho só (-16 LUFS).
4. Mede o início real de cada palavra na tomada final (só para sincronizar texto e animação, nunca para recortar)
   e grava WORK/a/voz.wav, WORK/tl.json e WORK/tl.js. O render.py usa a/voz.wav inteiro quando ele existe.
Precisa de GEMINI_API_KEY no ambiente."""
import base64, difflib, json, os, re, subprocess, sys, unicodedata, urllib.request
import numpy as np
from concurrent.futures import ThreadPoolExecutor
MODEL = os.path.expanduser('~/.cache/gancho-tensao/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8/')
VOZ = 'pt-br-commercial-7'
ESTILO = 'warm, confident and engaging female narrator, like a friendly expert talking to one person, natural pacing, smiling voice, clear diction'
TEMPO = 1.20; LUFS = -16.0
NUM = {'15': 'quinze', '45': 'quarenta e cinco', '54': 'cinquenta e quatro', '2': 'dois', '3': 'tres', '6': 'seis', '7': 'sete', '10': 'dez', '38': 'trinta e oito', '200': 'duzentos', '60': 'sessenta', '470': 'quatrocentos e setenta'}
def clean(t): return re.sub(r'\s*<[^>]+>\s*', ' ', t).strip()
def nz(w):
    w = unicodedata.normalize('NFD', w.lower()).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]', '', w)
def toks(t):
    out = []
    for w in re.findall(r"[\wÀ-ÿ%]+", t):
        w = nz(w.replace('%', ' por cento'))
        out += (NUM.get(w, w)).split() if w else []
    return [x.replace('para', 'pra') if x == 'para' else x for x in out]
def tts(text, out):
    body = {"model": "gemini-3.8-flash-tts", "input": [{"type": "user_input", "content": [{"type": "text", "text": text,
            "annotations": [{"type": "speech_metadata", "style": ESTILO}]}]}], "response_format": {"type": "audio"},
            "generation_config": {"speech_config": [{"voice": VOZ}]}}
    req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/interactions", data=json.dumps(body).encode(),
                                 headers={"x-goog-api-key": os.environ["GEMINI_API_KEY"], "Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    def find(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ('data', 'audio') and isinstance(v, str) and len(v) > 1000: return v
                x = find(v)
                if x: return x
        if isinstance(o, list):
            for v in o:
                x = find(v)
                if x: return x
    raw = base64.b64decode(find(r))
    if raw[:4] == b'RIFF': open(out, 'wb').write(raw)
    else:
        open(out + '.pcm', 'wb').write(raw); subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', '24000', '-ac', '1', '-i', out + '.pcm', out], check=True)
def pcm16k(p):
    return np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', p, '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
_R = None
def asr(p):
    global _R
    import sherpa_onnx
    if _R is None:
        _R = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=MODEL + 'encoder.int8.onnx', decoder=MODEL + 'decoder.int8.onnx', joiner=MODEL + 'joiner.int8.onnx', tokens=MODEL + 'tokens.txt', model_type='nemo_transducer', num_threads=4)
    x = np.concatenate([np.zeros(4000, np.float32), pcm16k(p), np.zeros(8000, np.float32)])
    s = _R.create_stream(); s.accept_waveform(16000, x); _R.decode_stream(s); r = s.result; ws = []
    for tok, ts in zip(r.tokens, r.timestamps):
        if tok.startswith((' ', '▁')) or not ws: ws.append([tok.strip().replace('▁', ''), ts - .25])
        else: ws[-1][0] += tok
    return ws
def drift(p):
    import librosa
    y = pcm16k(p); f0 = librosa.yin(y, fmin=110, fmax=420, sr=16000, frame_length=1024, hop_length=160)
    rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=160)[0][:len(f0)]; v = rms > np.percentile(rms, 40)
    t = np.arange(len(f0)) * .01; m = []
    for a in np.arange(0, t[-1], 5):
        k = (t >= a) & (t < a + 5) & v
        if k.sum() > 50: m.append(np.median(12 * np.log2(f0[k] / 100)))
    return float(np.std(m)) if len(m) > 1 else 0.0
def main():
    R = json.load(open(sys.argv[1])); work = os.path.abspath(sys.argv[2]); N = int(sys.argv[sys.argv.index('--takes') + 1]) if '--takes' in sys.argv else 3
    os.makedirs(os.path.join(work, 'v'), exist_ok=True); os.makedirs(os.path.join(work, 'a'), exist_ok=True)
    falas = [clean(f['texto']) for f in R['falas']]; texto = ' '.join(falas); ref = toks(texto)
    takes = [os.path.join(work, 'v', f'take{i}.wav') for i in range(1, N + 1)]
    if '--reusar' not in sys.argv:
        with ThreadPoolExecutor(N) as ex: list(ex.map(lambda p: tts(texto, p), takes))
    sc = []
    for p in takes:
        hyp = [x for w, _ in asr(p) for x in toks(w)]; s = difflib.SequenceMatcher(None, ref, hyp, autojunk=False).ratio() * 100
        sc.append((p, s, drift(p))); print(f'{os.path.basename(p)}  texto {s:.1f}  deriva {sc[-1][2]:.2f} st')
    best = max(s for _, s, _ in sc); ok = [x for x in sc if x[1] >= best - 4]; pick = min(ok, key=lambda x: x[2])[0]
    print('escolhida:', os.path.basename(pick))
    tmp = os.path.join(work, 'v', 'final_raw.wav'); fin = os.path.join(work, 'a', 'voz.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', pick, '-af', 'silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse,atempo=%.2f' % TEMPO, '-ar', '48000', '-ac', '1', tmp], check=True)
    import pyloudnorm as pyln
    from scipy.io import wavfile
    sr, x = wavfile.read(tmp); x = x.astype(np.float64) / (32768 if x.dtype == np.int16 else 1)
    x *= 10 ** ((LUFS - pyln.Meter(sr).integrated_loudness(x)) / 20); wavfile.write(fin, sr, x.astype(np.float32))
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', fin], capture_output=True, text=True).stdout)
    rec = asr(fin); print('ouvido:', ' '.join(w for w, _ in rec))
    # tempo por palavra do roteiro (alinha a transcrição; o que não casar é interpolado por sílaba)
    words = [w for f in falas for w in f.split()]; li = [i for i, f in enumerate(falas) for _ in f.split()]
    A = [' '.join(toks(w)) for w in words]; B = [' '.join(toks(w)) for w, _ in rec]; off = [None] * len(words)
    for blk in difflib.SequenceMatcher(None, A, B, autojunk=False).get_matching_blocks():
        for k in range(blk.size): off[blk.a + k] = max(0, rec[blk.b + k][1])
    if off[0] is None: off[0] = 0
    nsyl = lambda w: max(1, len(re.findall(r'[aeiouáéíóúâêôãõày]+', w.lower())))
    known = [(k, v) for k, v in enumerate(off) if v is not None] + [(len(words), d)]
    for (a, va), (b, vb) in zip(known, known[1:]):
        if b - a > 1:
            sy = np.cumsum([0] + [nsyl(w) for w in words[a:b]]); span = (vb - va) * (.85 if b == len(words) else 1)
            for k in range(a + 1, b): off[k] = va + span * sy[k - a] / sy[-1]
    hook = R.get('hook', 0.0); t0 = hook + .55 if hook else .4; lines = []
    for i, f in enumerate(falas):
        idx = [k for k in range(len(words)) if li[k] == i]; st = off[idx[0]]
        en = off[idx[-1] + 1] if idx[-1] + 1 < len(words) else d
        lines.append(dict(n=i + 1, t=round(t0 + st, 3), d=round(en - st, 3), text=f, words=f.split(), wt=[round(t0 + off[k], 3) for k in idx]))
    TL = dict(dur=round(t0 + d + 2.4, 3), hook=hook, voz_continua=True, voz_t0=t0, lines=lines)
    json.dump(TL, open(os.path.join(work, 'tl.json'), 'w'), ensure_ascii=False, indent=1)
    open(os.path.join(work, 'tl.js'), 'w').write('window.TL=' + json.dumps(TL, ensure_ascii=False) + ';')
    for l in lines: print(l['n'], l['t'], ' '.join(f"{w}@{x - l['t']:.2f}" for w, x in zip(l['words'], l['wt'])))
    print('TOTAL', TL['dur'])
if __name__ == '__main__': main()
