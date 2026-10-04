#!/usr/bin/env python3
"""dub_align.py: troca o áudio de uma cena pelo áudio limpo (TTS) no ritmo da boca.
Uso: python3 dub_align.py cena.mp4 fala_limpa.mp3 saida.mp4
Quebra as duas falas em frases (pausas > 0,22 s pelas palavras do Whisper), estica cada frase
limpa até a duração da frase no vídeo e coloca no mesmo instante. Assim a palavra fica exata
(sem as trocas do gerador de vídeo) e a boca continua batendo."""
import subprocess, sys

GAP = 0.22


def sh(*a):
    r = subprocess.run(list(a), capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-1500:]); sys.exit(1)
    return r.stdout


def dur(p):
    return float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p).strip())


def phrases(path, model):
    segs, _ = model.transcribe(path, language="pt", word_timestamps=True, beam_size=5, vad_filter=False,
                               condition_on_previous_text=False)
    out = []
    for s in segs:
        for w in s.words:
            if out and w.start - out[-1][1] < GAP:
                out[-1][1] = w.end; out[-1][2].append(w.word.strip())
            else:
                out.append([w.start, w.end, [w.word.strip()]])
    return out


def words(path, model):
    segs, _ = model.transcribe(path, language="pt", word_timestamps=True, beam_size=5, vad_filter=False,
                               condition_on_previous_text=False)
    import re
    return [(w.start, w.end, re.sub(r"[^a-z0-9à-ú]", "", w.word.lower())) for s in segs for w in s.words]


def anchors(wv, wc, min_gap=0.28):
    """palavras iguais nas duas falas viram âncoras (início no limpo -> início no vídeo)"""
    import difflib
    sm = difflib.SequenceMatcher(a=[w[2] for w in wc], b=[w[2] for w in wv], autojunk=False)
    pts = [(wc[0][0], wv[0][0])]
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            c, v = wc[a + k][0], wv[b + k][0]
            if c - pts[-1][0] >= min_gap and v - pts[-1][1] >= min_gap:
                pts.append((c, v))
    end = (wc[-1][1], wv[-1][1])
    if end[0] - pts[-1][0] < min_gap or end[1] - pts[-1][1] < min_gap:
        pts[-1] = end
    else:
        pts.append(end)
    return pts


def main():
    video, clean, outp = sys.argv[1:4]
    from faster_whisper import WhisperModel
    m = WhisperModel("small", compute_type="int8")
    D = dur(video)
    if "--frases" not in sys.argv:  # padrão: âncoras palavra a palavra
        wv, wc = words(video, m), words(clean, m)
        pts = anchors(wv, wc)
        print("âncoras (limpo -> vídeo):", [(round(c, 2), round(v, 2)) for c, v in pts])
        pv = [[pts[i][1], pts[i + 1][1], []] for i in range(len(pts) - 1)]
        pc = [[pts[i][0], pts[i + 1][0], []] for i in range(len(pts) - 1)]
        pad = 0.0
    else:
        pv, pc = phrases(video, m), phrases(clean, m)
        print("vídeo:", [(round(a, 2), round(b, 2), " ".join(t)) for a, b, t in pv])
        print("limpo:", [(round(a, 2), round(b, 2), " ".join(t)) for a, b, t in pc])
        if len(pv) != len(pc):  # sem par frase a frase: estica a fala inteira entre o 1º e o último som
            pv = [[pv[0][0], pv[-1][1], []]]; pc = [[pc[0][0], pc[-1][1], []]]
        pad = 0.06
    if pad == 0.0 and pv:  # respiro antes da 1ª e depois da última palavra
        pc[0][0] = max(0.0, pc[0][0] - 0.05); pv[0][0] = max(0.0, pv[0][0] - 0.05)
        pc[-1][1] = min(dur(clean), pc[-1][1] + 0.12); pv[-1][1] = min(D, pv[-1][1] + 0.12)
    fl, ins = [], ["-i", clean]
    for i, ((va, vb, _), (ca, cb, _)) in enumerate(zip(pv, pc)):
        ca, cb = max(0.0, ca - pad), min(dur(clean), cb + pad)
        tgt = (vb - va) + 2 * pad
        r = (cb - ca) / tgt  # >1 acelera
        r = min(1.35, max(0.75, r))
        ms = int(max(0.0, va - pad) * 1000)
        seg = (cb - ca) / r
        fl.append(f"[0:a]atrim={ca:.3f}:{cb:.3f},asetpts=PTS-STARTPTS,atempo={r:.4f},afade=t=in:d=0.006,"
                  f"afade=t=out:st={max(0, seg - 0.006):.3f}:d=0.006,adelay={ms}|{ms}[p{i}]")
        print(f"frase {i}: limpa {cb-ca:.2f}s -> vídeo {tgt:.2f}s (x{r:.3f}) em {va-pad:.2f}s")
    n = len(fl)
    fl.append("".join(f"[p{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0,apad,atrim=0:{D:.3f}[a]")
    sh("ffmpeg", "-v", "error", "-y", *ins, "-i", video, "-filter_complex", ";".join(fl), "-map", "1:v", "-map", "[a]",
       "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", outp)
    print("ok", outp)


if __name__ == "__main__":
    main()
