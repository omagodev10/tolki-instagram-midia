#!/usr/bin/env python3
"""split_take.py: corta a narração inteira (um take só) em uma fala por cena, tira pausas longas e acerta o ritmo.

Uso (dentro da pasta do Reel ou do anúncio):
  python3 <repo>/tools/reel-motion/split_take.py narracao.mp3 roteiro.json [pasta_saida=a]
  python3 <repo>/tools/reel-motion/split_take.py "v/f1.mp3,v/f2.mp3,..." roteiro.json a   (uma fala por arquivo)

roteiro.json: {"lines": ["frase 1", "frase 2", ...], "bounds": [opcional, em segundos]}
  "bounds" (opcional) = início da 1a fala, cada divisa entre falas e o fim (len(lines)+1 números).
  Use só se a divisão automática errar (o script avisa).

Regra de ritmo (aprovada pelo Carlos em 07/10/2026):
  - pausas internas acima de 0,38 s viram 0,30 s (pausa cômica curta continua);
  - andamento = 3,3 palavras/s ÷ ritmo atual, entre 1,0x e 1,3x, sem mudar o tom (rubberband).
Saídas: <pasta>/l1.wav, l2.wav... e split.json (tempo, divisas, duração e palavras/s de cada fala)."""
import json, os, re, subprocess, sys
import numpy as np
from scipy.io import wavfile
from scipy.ndimage import median_filter

SR = 48000; TARGET = 3.3; CAP = 1.3; HOP = int(.01 * SR)


def load(p):
    a = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(a, np.float32).astype(np.float64)


def nwords(t): return len(re.sub(r'[^\wà-úÀ-Ú ]', ' ', t).split())
def nsyl(t): return max(1, len(re.findall(r'[aeiouáéíóúâêôãõà]+', t.lower())))


def main():
    src, rot = sys.argv[1], sys.argv[2]; out = sys.argv[3] if len(sys.argv) > 3 else 'a'
    C = json.load(open(rot, encoding='utf-8')); L = C['lines']
    if ',' in src:   # uma fala por arquivo: junta com 1 s de silêncio entre elas e segue igual
        parts = [load(f.strip()) for f in src.split(',') if f.strip()]
        x = np.concatenate([np.concatenate([p, np.zeros(SR)]) for p in parts])
    else:
        x = load(src)
    db = np.array([20 * np.log10(np.sqrt((x[i:i + HOP] ** 2).mean()) + 1e-9) for i in range(0, len(x) - HOP, HOP)])
    db = median_filter(db, 7)                           # 70 ms median: breaths and mp3 noise do not break a pause
    thr = max(np.percentile(db[db > -90], 92) - 30, np.percentile(db, 5) + 7); on = db > thr
    idx = np.where(on)[0]; s0, e0 = idx[0], idx[-1] + 1
    runs = []; i = s0                                   # silences of 120 ms or more inside the take
    while i < e0:
        if not on[i]:
            j = i
            while j < e0 and not on[j]: j += 1
            if j - i >= 12:
                if runs and i - runs[-1][1] < 8: runs[-1] = (runs[-1][0], j)   # merge a pause split by a blip
                else: runs.append((i, j))
            i = j
        else: i += 1
    sy = np.array([nsyl(l) for l in L], float); cum = np.cumsum(sy) / sy.sum(); span = e0 - s0
    exp = [s0 + cum[k] * span for k in range(len(L) - 1)]
    K = len(L) - 1; R = len(runs); INF = 1e18
    if K and R < K: sys.exit(f'só achei {R} pausas para {K} divisas: gere uma fala por pedido ou passe "bounds"')
    if 'bounds' in C:
        bnds = [int(round(b * 100)) for b in C['bounds']]
    elif K:
        cost = lambda r, k: ((runs[r][0] + runs[r][1]) / 2 - exp[k]) ** 2 / (0.06 * span) ** 2 - 2.0 * np.log(runs[r][1] - runs[r][0])
        D = np.full((K, R), INF); P = np.zeros((K, R), int)
        for r in range(R): D[0, r] = cost(r, 0)
        for k in range(1, K):
            best = INF; bi = -1
            for r in range(R):
                if r and D[k - 1, r - 1] < best: best, bi = D[k - 1, r - 1], r - 1
                if bi >= 0: D[k, r] = best + cost(r, k); P[k, r] = bi
        r = int(np.argmin(D[K - 1])); ch = [r]
        for k in range(K - 1, 0, -1): r = P[k, r]; ch.append(r)
        ch = ch[::-1]; bnds = [s0] + [(runs[c][0] + runs[c][1]) // 2 for c in ch] + [e0]
    else:
        bnds = [s0, e0]
    os.makedirs(out, exist_ok=True); segs = []
    for k in range(len(L)):
        a, b = bnds[k], bnds[k + 1]; w = np.where(on[a:b])[0]
        if not len(w): sys.exit(f'fala {k + 1} ficou vazia: confira "bounds"')
        a2, b2 = a + max(0, w[0] - 5), a + min(b - a, w[-1] + 15)   # keep soft word endings (-ção, -te)
        keep = np.ones(b2 - a2, bool); oo = on[a2:b2]; i = 0
        while i < len(oo):                              # pauses over 0.38 s shrink to 0.30 s
            if not oo[i]:
                j = i
                while j < len(oo) and not oo[j]: j += 1
                if j - i > 38: keep[i + 15:j - 15] = False
                i = j
            else: i += 1
        y = x[a2 * HOP:b2 * HOP]; m = np.repeat(keep, HOP)[:len(y)]; pieces = []; i = 0
        while i < len(m):
            if m[i]:
                j = i
                while j < len(m) and m[j]: j += 1
                pieces.append(y[i:j].copy()); i = j
            else: i += 1
        z = pieces[0]; xf = 240
        for p in pieces[1:]:
            r_ = np.linspace(0, 1, xf); z[-xf:] = z[-xf:] * (1 - r_) + p[:xf] * r_; z = np.concatenate([z, p[xf:]])
        segs.append(z)
    tot = sum(len(s) for s in segs) / SR + 0.25 * (len(L) - 1); words = sum(nwords(l) for l in L)
    f = float(np.clip(TARGET / (words / tot), 1.0, CAP))
    print(f'fala {tot:.1f}s, {words} palavras, ritmo {words / tot:.2f} palavras/s -> andamento x{f:.2f}')
    info = []
    for k, z in enumerate(segs):
        wavfile.write('_tmp.wav', SR, z.astype(np.float32)); dst = os.path.join(out, f'l{k + 1}.wav')
        try:
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '_tmp.wav', '-af', f'rubberband=tempo={f:.3f}:pitchq=quality:formant=preserved,afade=t=in:d=0.01', '-ar', str(SR), '-ac', '1', dst], check=True)
        except subprocess.CalledProcessError:   # ffmpeg sem rubberband: atempo (qualidade um pouco menor)
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '_tmp.wav', '-af', f'atempo={f:.3f},afade=t=in:d=0.01', '-ar', str(SR), '-ac', '1', dst], check=True)
        d = len(z) / SR / f; info.append({'fala': k + 1, 'dur': round(d, 2), 'palavras_s': round(nwords(L[k]) / d, 2)})
    os.remove('_tmp.wav')
    # sanity check: the pauses used as cuts must be clearly longer than every pause left inside a line
    cut = [b_ for b_ in bnds[1:-1]]
    used = [r for r in runs if any(r[0] <= c_ <= r[1] for c_ in cut)]; rest = [r for r in runs if r not in used and s0 < r[0] and r[1] < e0]
    gmin = min([r[1] - r[0] for r in used], default=0) / 100; gin = max([r[1] - r[0] for r in rest], default=0) / 100
    dev = (np.diff(bnds) / (bnds[-1] - bnds[0])) / (sy / sy.sum()) - 1    # time share vs syllable share, per line
    clear = gmin >= 1.25 * gin                                             # cuts sit on clearly longer pauses
    bad = [] if 'bounds' in C or not K or clear else [k + 1 for k in range(len(L)) if abs(dev[k]) > .35]
    for s in info: print(f"  fala {s['fala']}: {s['dur']:.2f}s, {s['palavras_s']} palavras/s")
    print(f'menor pausa usada como corte {gmin:.2f}s, maior pausa dentro das falas {gin:.2f}s')
    if bad: print('ATENÇÃO: divisão incerta nas falas', bad, '. Gere de novo uma fala por pedido e passe os arquivos separados por vírgula.')
    json.dump({'tempo': f, 'bounds': [b / 100 for b in bnds], 'falas': info, 'desvio_silabas': [round(float(v), 2) for v in dev], 'pausa_corte_min': gmin, 'pausa_interna_max': gin, 'suspeitas': bad}, open('split.json', 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
