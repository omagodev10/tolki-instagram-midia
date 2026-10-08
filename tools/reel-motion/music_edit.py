#!/usr/bin/env python3
"""music_edit.py: remixa uma música para o vídeo, encaixando os momentos fortes nos pontos certos.

  analyze  python3 music_edit.py analyze inst.wav song.json
           -> batidas, compassos, energia por compasso, drops (entradas fortes), breaks (quedas) e hits.
  arrange  python3 music_edit.py arrange inst.wav song.json cues.json DURACAO out.wav
           cues.json = [{"t": 15.69, "kind": "drop"}, {"t": 24.55, "kind": "break"}, {"t": 25.8, "kind": "hit"}]
           kind: drop (entrada forte da música), break (a música some/abaixa), hit (volta com força num compasso).
           Entre dois pontos a música toca contínua; quando o trecho natural não cabe, faz um corte no tempo
           da batida (mesma posição no compasso) e ajusta o andamento em até 5% para cair exato.
Saída: wav estéreo 48 kHz, sem normalizar (o mix_motion.py cuida do nível)."""
import json, subprocess, sys, os, tempfile
import numpy as np

SR = 48000


def load(p, sr=SR):
    a = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', p, '-ac', '2', '-ar', str(sr), '-f', 'f32le', '-'],
                                     capture_output=True, check=True).stdout, np.float32)
    return a.reshape(-1, 2).astype(np.float64)


def analyze(src, out):
    import librosa
    x = load(src, 22050).mean(1)
    sr = 22050
    tempo, beats = librosa.beat.beat_track(y=x, sr=sr, units='time', tightness=100)
    beats = np.asarray(beats, float)
    # kick-weighted onset to find the downbeat phase
    lo = librosa.onset.onset_strength(y=librosa.effects.preemphasis(x, coef=-0.97), sr=sr, hop_length=256)
    times = librosa.frames_to_time(np.arange(len(lo)), sr=sr, hop_length=256)
    on_at = np.interp(beats, times, lo)
    phase = int(np.argmax([on_at[p::4].mean() for p in range(4)]))
    down = beats[phase::4]
    # bar energy (dB) over the instrumental
    def rms_db(t0, t1):
        s = x[int(t0 * sr):int(t1 * sr)]
        return float(20 * np.log10(np.sqrt((s ** 2).mean()) + 1e-9)) if len(s) else -90.0
    bars = [{'t': float(down[k]), 'db': rms_db(down[k], down[k + 1])} for k in range(len(down) - 1)]
    full = librosa.onset.onset_strength(y=x, sr=sr, hop_length=256)
    def refine(t):  # snap to the strongest onset within 90 ms
        m = (times > t - .09) & (times < t + .09)
        return float(times[m][np.argmax(full[m])]) if m.any() else t
    # timbre/intensity per bar from a log-mel spectrum: catches riff entries that barely change RMS
    S = librosa.power_to_db(librosa.feature.melspectrogram(y=x, sr=sr, n_mels=64, hop_length=512, fmax=11000))
    mt = librosa.frames_to_time(np.arange(S.shape[1]), sr=sr, hop_length=512)
    M = np.array([S[:, (mt >= down[k]) & (mt < down[k + 1])].mean(1) for k in range(len(down) - 1)])
    I = M.mean(1)
    nov = np.zeros(len(M))
    for k in range(2, len(M) - 1):
        nov[k] = np.linalg.norm(M[k:k + 2].mean(0) - M[k - 2:k].mean(0)) / np.sqrt(M.shape[1])
    thr = np.percentile(nov[2:], 80) if len(nov) > 4 else 1e9
    env_t = np.arange(0, len(x) / sr, .02); env = np.array([20 * np.log10(np.sqrt((x[int(t * sr):int((t + .05) * sr)] ** 2).mean()) + 1e-9) for t in env_t])
    def fall(t0, t1):  # moment of the steepest drop in loudness between t0 and t1
        m = np.where((env_t >= t0) & (env_t <= t1 - .3))[0]
        if not len(m): return float(t0)
        d = np.array([env[max(0, i - 15):i].mean() - env[i + 3:i + 50].mean() if i + 50 < len(env) else 0 for i in m])
        return float(env_t[m[int(np.argmax(d))]])
    drops, breaks, hits = [], [], []
    for k in range(2, len(M) - 1):
        if nov[k] < thr or nov[k] < nov[k - 1] or nov[k] < nov[k + 1]: continue
        dI = I[k:k + 2].mean() - I[k - 2:k].mean()
        if dI >= 1.5: drops.append({'t': refine(bars[k]['t']), 'bar': k, 'jump_db': round(float(dI), 1), 'novelty': round(float(nov[k]), 2)})
        elif dI <= -2.5: breaks.append({'t': fall(bars[k - 1]['t'], down[k + 1]), 'bar': k, 'fall_db': round(float(-dI), 1), 'novelty': round(float(nov[k]), 2)})
    for b, ik in zip(bars, I): b['mel_db'] = round(float(ik), 1)
    E = I; hi, lo_ = np.percentile(E, 65), np.percentile(E, 35)
    for k in range(len(E)):
        if E[k] >= hi:
            hits.append({'t': refine(bars[k]['t']), 'bar': k})
    for b, e in zip(bars, E):
        b['level'] = 'high' if e >= hi else 'low' if e <= lo_ else 'mid'
    J = {'tempo': float(np.atleast_1d(tempo)[0]), 'beat': float(np.median(np.diff(beats))), 'beats': beats.round(4).tolist(),
         'downbeat_phase': phase, 'bars': bars, 'drops': drops, 'breaks': breaks, 'hits': hits, 'duration': len(x) / sr}
    json.dump(J, open(out, 'w'), indent=1)
    print(f"tempo {J['tempo']:.1f} bpm, {len(bars)} compassos, drops {[round(d['t'],2) for d in drops]}, breaks {[round(b['t'],2) for b in breaks]}")


def stretch(seg, f):
    """time-stretch seg (N,2) by factor f (>1 = faster/shorter) keeping pitch."""
    if abs(f - 1) < 0.003:
        return seg
    with tempfile.TemporaryDirectory() as d:
        a, b = os.path.join(d, 'a.wav'), os.path.join(d, 'b.wav')
        from scipy.io import wavfile
        wavfile.write(a, SR, seg.astype(np.float32))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', a, '-af', f'rubberband=tempo={f:.5f}:pitchq=quality:transients=crisp', b], check=True)
        return load(b)


def arrange(src, ana, cues_p, dur, out):
    from scipy.io import wavfile
    x = load(src); J = json.load(open(ana)); beats = np.array(J['beats']); bp = J['beat']
    cues = sorted(json.load(open(cues_p)), key=lambda c: c['t']) if isinstance(cues_p, str) else sorted(cues_p, key=lambda c: c['t'])
    bi = lambda t: int(np.argmin(np.abs(beats - t)))
    def cands(kind):
        if kind == 'drop':
            c = [d['t'] for d in sorted(J['drops'], key=lambda d: -d['jump_db'])]
        elif kind == 'break':
            c = [b['t'] for b in sorted(J['breaks'], key=lambda b: -b['fall_db'])]
        else:
            c = [d['t'] for d in J['drops']] + [h['t'] for h in J['hits']]
        return c or [h['t'] for h in J['hits']] or [beats[0]]
    # choose one song anchor per cue: first cue needs pre-roll; later ones prefer anchors after the previous one
    anchors = []
    bars = J['bars']
    def lvl(t0, t1):  # mean bar loudness (dB) in [t0, t1)
        v = [b['db'] for b in bars if t0 <= b['t'] < t1]
        return float(np.mean(v)) if v else -60.0
    for i, c in enumerate(cues):
        cs = [c['song_t']] if c.get('song_t') is not None else cands(c['kind'])   # a cue may pin the exact song moment
        if i == 0:
            ok = [s for s in cs if s - c['t'] >= 0] or cs
            if c['kind'] == 'drop':    # the intro before the first drop should be quieter, so the drop lands
                ok = sorted(ok, key=lambda s: -(lvl(s, s + 4 * bp * 2) - lvl(s - c['t'], s)))
            elif c['kind'] == 'break':  # before the first break the music should be up, so the fall is felt
                ok = sorted(ok, key=lambda s: -(lvl(s - c['t'], s) - lvl(s, s + 4 * bp)))
            anchors.append(ok[0]); continue
        L = c['t'] - cues[i - 1]['t']; prev = anchors[-1]; n = max(1, round(L / bp))
        I = bi(prev)
        def score(s):
            Jx = bi(s); pen = 0 if (Jx - I - n) % 4 == 0 else (1 if (Jx - I - n) % 2 == 0 else 3)
            nat = abs((s - prev) - L) / bp  # 0 = plays straight through, no cut
            return (0 if nat < .6 else 1) * 10 + pen * 2 + (0 if s > prev else 1) + min(nat, 40) * .01
        anchors.append(min(cs, key=score))
    pieces = []  # (song_t0, song_t1, stretch, video_len)
    t0 = cues[0]['t'] if cues else 0.0
    if cues:
        s0 = anchors[0] - t0
        pieces.append((max(0.0, s0), anchors[0], 1.0, t0, -s0 if s0 < 0 else 0.0))
    for i in range(len(cues) - 1):
        L = cues[i + 1]['t'] - cues[i]['t']; A, B = anchors[i], anchors[i + 1]; I, Jb = bi(A), bi(B)
        n = max(1, round(L / bp))
        if abs((B - A) - L) < .6 * bp and B > A:                      # straight through
            pieces.append((A, B, (B - A) / L, L, 0.0)); continue
        for dn in (0, 1, -1, 2, -2):                                   # keep the bar phase across the cut
            if (Jb - I - (n + dn)) % 4 == 0 and n + dn >= 2: n = n + dn; break
        a = max(1, min(n - 1, (n // 2) // 4 * 4 or n // 2))            # cut at a bar line near the middle
        p1 = (A, beats[min(I + a, len(beats) - 1)]); p2 = (beats[max(Jb - (n - a), 0)], B)
        nat = (p1[1] - p1[0]) + (p2[1] - p2[0]); f = nat / L
        if abs(f - 1) > .06 or L < 8 * bp:                             # short gap: play straight, cut into the next anchor
            pieces.append((A, A + L, 1.0, L, 0.0)); continue
        pieces.append((p1[0], p1[1], f, (p1[1] - p1[0]) / f, 0.0)); pieces.append((p2[0], p2[1], f, (p2[1] - p2[0]) / f, 0.0))
    last = anchors[-1] if cues else 0.0
    tail = dur - (cues[-1]['t'] if cues else 0.0)
    pieces.append((last, min(last + tail + .5, len(x) / SR), 1.0, tail, 0.0))
    # render: each piece placed at its video start, 30 ms equal-power crossfades centred on every join
    xf = int(.03 * SR); h = xf // 2; outb = np.zeros((int(dur * SR) + 2 * SR, 2)); cum = 0.0
    for k, (a_, b_, f, vlen, pad) in enumerate(pieces):
        lo_s = max(0, int(a_ * SR) - h); seg = x[lo_s:int(b_ * SR) + h].copy()
        if f != 1.0: seg = stretch(seg, f)
        start = int(round(cum * SR)) - (h if lo_s > 0 or k else 0) + int(pad * SR)
        r = np.sin(np.linspace(0, np.pi / 2, xf)) ** 2
        if k: seg[:xf] *= r[:, None]
        if k < len(pieces) - 1: seg[-xf:] *= r[::-1][:, None]
        start = max(0, start); e = min(len(outb), start + len(seg)); outb[start:e] += seg[:e - start]
        cum += vlen
    outb = outb[:int(dur * SR)]
    # break = DJ filter drop: muffle (low-pass 700 Hz) and lower the music until the next hit (or 1.5 s)
    from scipy.signal import butter, sosfiltfilt
    lp = sosfiltfilt(butter(4, 700, 'lowpass', fs=SR, output='sos'), outb, axis=0) * 0.4
    for i, c in enumerate(cues):
        if c['kind'] != 'break': continue
        nxt = [d['t'] for d in cues[i + 1:] if d['kind'] in ('hit', 'drop')]
        t1 = nxt[0] if nxt else min(dur, c['t'] + 1.5)
        a, b = int(c['t'] * SR), int(t1 * SR); rr = int(.06 * SR)
        w = np.zeros(len(outb)); w[a:b] = 1
        w[a:a + rr] = np.linspace(0, 1, min(rr, len(w[a:a + rr])))
        w[max(a, b - int(.02 * SR)):b] = np.linspace(1, 0, len(w[max(a, b - int(.02 * SR)):b]))
        outb = outb * (1 - w)[:, None] + lp * w[:, None]
    wavfile.write(out, SR, outb.astype(np.float32))
    print('anchors', [round(a, 2) for a in anchors], 'pieces', [(round(p[0], 2), round(p[1], 2), round(p[2], 3)) for p in pieces])


if __name__ == '__main__':
    if sys.argv[1] == 'analyze':
        analyze(sys.argv[2], sys.argv[3])
    else:
        arrange(sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5]), sys.argv[6])
