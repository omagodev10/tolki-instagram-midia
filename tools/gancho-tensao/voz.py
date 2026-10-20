"""Voz + linha do tempo do modelo gancho de tensão.
python3 voz.py roteiro.json WORK
roteiro.json: {"voz": "pt-br-techagent-4", "estilo": "tom geral", "hook": 6.0,
               "falas": [{"texto": "Você ficou seis segundos esperando ...", "estilo": "intrigante"}, ...],
               "pausas": {"2": 0.15, "3": 0.45}}   (pausa extra ANTES da fala n, além de 0,28 s)
Gera WORK/a/l1.wav... (uma fala por pedido ao Gemini, silêncio aparado), mede o início real de cada palavra
com o Parakeet TDT v3 (ASR com timestamps) e grava WORK/tl.json e WORK/tl.js. Precisa de GEMINI_API_KEY no ambiente.
Opções: --so-tl (não gera voz de novo, só refaz a linha do tempo), --falas 3,7 (regera só essas falas)."""
import json, os, re, subprocess, sys, difflib, unicodedata
import numpy as np
ENGINE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(ENGINE))
TTS = os.path.join(REPO, 'tools', 'reel-motion', 'gemini_tts.py')
MODEL = os.path.expanduser('~/.cache/gancho-tensao/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8/')
AL = {'15%': 'quinze', '45%': 'quarenta', '54': 'cinquenta', 'para': 'pra', 'ta': 'esta', 'toc': 'tolki', 'talk': 'tolki', 'tolque': 'tolki', 'donto': 'odonto', 'ortodonic': 'orthodontic'}
def clean(t): return re.sub(r'\s*<[^>]+>\s*', ' ', t).strip()
def nz(w):
    w = unicodedata.normalize('NFD', w.lower()).encode('ascii', 'ignore').decode().strip('.,!?:;')
    return AL.get(w, re.sub(r'[^a-z0-9]', '', w))
def nsyl(w): return max(1, len(re.findall(r'[aeiouáéíóúâêôãõày]+', w.lower())))
def dur(p): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)
def gerar(R, work, idx):
    os.makedirs(os.path.join(work, 'v'), exist_ok=True); os.makedirs(os.path.join(work, 'a'), exist_ok=True)
    for i in idx:
        f = R['falas'][i - 1]; rot = os.path.join(work, 'v', f'f{i}.json'); mp3 = os.path.join(work, 'v', f'f{i}.mp3')
        json.dump({'estilo': R.get('estilo', ''), 'falas': [f]}, open(rot, 'w'), ensure_ascii=False)
        subprocess.run([sys.executable, TTS, rot, mp3, R.get('voz', 'pt-br-techagent-4')], check=True, stdout=subprocess.DEVNULL)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp3, '-af', 'silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse',
                        '-ar', '48000', '-ac', '1', os.path.join(work, 'a', f'l{i}.wav')], check=True)
        print('voz', i, clean(f['texto']))
def palavras(work, n):
    import sherpa_onnx
    R = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=MODEL + 'encoder.int8.onnx', decoder=MODEL + 'decoder.int8.onnx', joiner=MODEL + 'joiner.int8.onnx', tokens=MODEL + 'tokens.txt', model_type='nemo_transducer', num_threads=8)
    out = []
    for i in range(1, n + 1):
        x = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', os.path.join(work, 'a', f'l{i}.wav'), '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
        x = np.concatenate([np.zeros(4000, np.float32), x, np.zeros(8000, np.float32)])
        s = R.create_stream(); s.accept_waveform(16000, x); R.decode_stream(s); r = s.result; ws = []
        for tok, ts in zip(r.tokens, r.timestamps):
            if tok.startswith((' ', '▁')) or not ws: ws.append([tok.strip().replace('▁', ''), ts - .25])
            else: ws[-1][0] += tok
        out.append(ws); print('ouvido', i, ' '.join(w for w, _ in ws))
    return out
def linha_do_tempo(R, work, W):
    hook = R.get('hook', 6.0); t = hook + .55 if hook else .4; P = {int(k): v for k, v in R.get('pausas', {}).items()}; lines = []
    for i, f in enumerate(R['falas'], 1):
        if i > 1: t += .28 + P.get(i, 0)
        txt = clean(f['texto']); p = os.path.join(work, 'a', f'l{i}.wav'); d = dur(p); rec = W[i - 1]; words = txt.split()
        A = [nz(w) for w in words]; B = [nz(w) for w, _ in rec]; off = [None] * len(words)
        for blk in difflib.SequenceMatcher(None, A, B, autojunk=False).get_matching_blocks():
            for k in range(blk.size): off[blk.a + k] = max(0, rec[blk.b + k][1])
        if off[0] is None: off[0] = 0
        known = [(k, v) for k, v in enumerate(off) if v is not None] + [(len(words), d)]
        for (a, va), (b, vb) in zip(known, known[1:]):
            if b - a > 1:
                sy = np.cumsum([0] + [nsyl(w) for w in words[a:b]]); span = (vb - va) * (.85 if b == len(words) else 1)
                for k in range(a + 1, b): off[k] = va + span * sy[k - a] / sy[-1]
        lines.append(dict(n=i, t=round(t, 3), d=round(d, 3), text=txt, words=words, wt=[round(t + o, 3) for o in off])); t += d
    TL = dict(dur=round(t + 2.4, 3), hook=hook, lines=lines)
    json.dump(TL, open(os.path.join(work, 'tl.json'), 'w'), ensure_ascii=False, indent=1)
    open(os.path.join(work, 'tl.js'), 'w').write('window.TL=' + json.dumps(TL, ensure_ascii=False) + ';')
    for l in lines: print(l['n'], l['t'], ' '.join(f"{w}@{x - l['t']:.2f}" for w, x in zip(l['words'], l['wt'])))
    print('TOTAL', TL['dur'])
if __name__ == '__main__':
    R = json.load(open(sys.argv[1])); work = os.path.abspath(sys.argv[2]); os.makedirs(work, exist_ok=True); n = len(R['falas'])
    if '--so-tl' not in sys.argv:
        idx = [int(x) for x in sys.argv[sys.argv.index('--falas') + 1].split(',')] if '--falas' in sys.argv else range(1, n + 1)
        gerar(R, work, idx)
    linha_do_tempo(R, work, palavras(work, n))
