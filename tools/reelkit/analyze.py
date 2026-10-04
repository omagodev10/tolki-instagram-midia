#!/usr/bin/env python3
"""analyze.py: VAD + Whisper (sherpa-onnx) + alinhamento com o roteiro.
Uso: python3 analyze.py raw.mp4 script.txt out_dir
Gera out_dir/edit.json com os trechos mantidos (retakes e silencios fora),
palavras com tempo na timeline final e inicio/fim de cada linha do roteiro."""
import json, os, re, subprocess, sys, unicodedata, difflib

HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(HERE, "models")
PAD_PRE, PAD_POST, MERGE_GAP = 0.07, 0.14, 0.12


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9%]", "", w)


NUMS = {"um": "1", "uma": "1", "dois": "2", "duas": "2", "tres": "3", "quatro": "4", "cinco": "5",
        "seis": "6", "sete": "7", "oito": "8", "nove": "9", "dez": "10", "quinze": "15",
        "cinquenta": "50", "quarenta": "40", "porcento": "%", "pra": "para", "pro": "para"}


def toks(text):
    out = []
    for w in re.findall(r"\S+", text):
        n = norm(w)
        if not n:
            continue
        n = NUMS.get(n, n)
        if n.endswith("%") and len(n) > 1:
            out += [n[:-1], "%"]
        else:
            out.append(n)
    return out


def load_audio(path, sr=16000):
    import numpy as np
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(pcm, dtype=np.float32).copy()


def vad_segments(a, sr=16000):
    import sherpa_onnx
    cfg = sherpa_onnx.VadModelConfig()
    cfg.silero_vad.model = os.path.join(M, "silero_vad.onnx")
    cfg.silero_vad.threshold = 0.45
    cfg.silero_vad.min_silence_duration = 0.22
    cfg.silero_vad.min_speech_duration = 0.18
    cfg.silero_vad.max_speech_duration = 25
    cfg.sample_rate = sr
    vad = sherpa_onnx.VoiceActivityDetector(cfg, buffer_size_in_seconds=600)
    win = cfg.silero_vad.window_size
    segs = []
    for i in range(0, len(a), win):
        vad.accept_waveform(a[i:i + win])
        while not vad.empty():
            s = vad.front
            segs.append([s.start / sr, (s.start + len(s.samples)) / sr])
            vad.pop()
    vad.flush()
    while not vad.empty():
        s = vad.front
        segs.append([s.start / sr, (s.start + len(s.samples)) / sr])
        vad.pop()
    return segs


def recognizer():
    import sherpa_onnx
    d = os.path.join(M, "sherpa-onnx-whisper-small")
    return sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=os.path.join(d, "small-encoder.int8.onnx"), decoder=os.path.join(d, "small-decoder.int8.onnx"),
        tokens=os.path.join(d, "small-tokens.txt"), language="pt", task="transcribe", num_threads=2)


def main():
    raw, script_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(out, exist_ok=True)
    sr = 16000
    a = load_audio(raw, sr)
    dur = len(a) / sr
    segs = vad_segments(a, sr)
    rec = recognizer()
    hyps = []
    for s, e in segs:
        st = rec.create_stream()
        st.accept_waveform(sr, a[int(max(0, s - 0.05) * sr):int(min(dur, e + 0.05) * sr)])
        rec.decode_stream(st)
        hyps.append(st.result.text.strip())

    lines = [l.strip() for l in open(script_path, encoding="utf-8") if l.strip()] if script_path != "-" else []
    # palavras do roteiro, com a linha de origem
    swords, sline, sdisp = [], [], []
    for li, l in enumerate(lines):
        for w in re.findall(r"\S+", l):
            for t in toks(w):
                swords.append(t); sline.append(li)
            sdisp.append((li, w))
    # tokens por linha e offsets globais
    ltoks = [toks(l) for l in lines]
    loff = [0]
    for lt in ltoks:
        loff.append(loff[-1] + len(lt))
    report, kept = [], []
    for i, ((s, e), h) in enumerate(zip(segs, hyps)):
        ht = toks(h)
        info = {"i": i, "start": round(s, 3), "end": round(e, 3), "text": h}
        if lines and ht:
            best = (0, 0, 0)
            for li in range(len(lines)):
                for lj in range(li, min(len(lines), li + 4)):
                    cand = sum(ltoks[li:lj + 1], [])
                    r = difflib.SequenceMatcher(None, cand, ht, autojunk=False).ratio()
                    if r > best[0] + 0.02:
                        best = (r, li, lj)
            r, li, lj = best
            info.update(cov=round(r, 2), lines=[li, lj], span=[loff[li], loff[lj + 1] - 1])
        report.append(info)
        if not lines:
            kept.append(info)
        elif info.get("cov", 0) >= 0.4:
            li, lj = info["lines"]
            survivors = []
            for k in kept:
                k0, k1 = k["lines"]
                ov = max(0, min(k1, lj) - max(k0, li) + 1)
                if ov == 0:
                    survivors.append(k)
                elif ov / (k1 - k0 + 1) >= 0.5:
                    if k["cov"] > info["cov"] + 0.25 and (k1 - k0) >= (lj - li):
                        info["dropped_by"] = k["i"]  # take anterior bem melhor: fica o anterior
                        survivors.append(k)
                    else:
                        k["dropped_by"] = i
                elif k0 < li:
                    a0, a1 = k["span"]
                    frac = (loff[li] - a0) / (a1 - a0 + 1)
                    k["end"] = round(k["start"] + (k["end"] - k["start"]) * frac, 3)
                    k["lines"] = [k0, li - 1]
                    k["span"] = [a0, loff[li] - 1]
                    survivors.append(k)
                else:
                    survivors.append(k)
            if "dropped_by" not in info:
                survivors.append(info)
            kept = survivors
    if lines:
        kept.sort(key=lambda k: k["span"][0])
    # timeline final
    clips, t = [], 0.0
    words = []
    for k in kept:
        cs, ce = max(0, k["start"] - PAD_PRE), min(dur, k["end"] + PAD_POST)
        if clips and lines and abs(cs - clips[-1]["src_end"]) < MERGE_GAP and cs >= clips[-1]["src_start"]:
            pass
        clip = {"src_start": round(cs, 3), "src_end": round(ce, 3), "out_start": round(t, 3), "seg": k["i"]}
        clips.append(clip)
        # palavras exibidas: do roteiro (grafia certa) ou do whisper
        if lines:
            a0, a1 = k["span"]
            disp = []
            # mapeia tokens do span de volta para palavras exibidas
            ti = 0
            for li, w in sdisp:
                n = len(toks(w))
                if n and ti + n - 1 >= a0 and ti <= a1:
                    disp.append((li, w))
                ti += n
        else:
            disp = [(None, w) for w in k["text"].split()]
        sp0, sp1 = k["start"] - cs + t, k["end"] - cs + t
        weights = [len(norm(w)) + 2 for _, w in disp] or [1]
        tot = sum(weights)
        acc = sp0
        for (li, w), wt in zip(disp, weights):
            d = (sp1 - sp0) * wt / tot
            words.append({"w": w, "line": li, "start": round(acc, 3), "end": round(acc + d, 3)})
            acc += d
        t += ce - cs
    line_times = {}
    for w in words:
        if w["line"] is None:
            continue
        lt = line_times.setdefault(w["line"], [w["start"], w["end"]])
        lt[0], lt[1] = min(lt[0], w["start"]), max(lt[1], w["end"])
    missing = [i for i in range(len(lines)) if i not in line_times]
    res = {"source": raw, "source_duration": round(dur, 3), "out_duration": round(t, 3), "clips": clips,
           "words": words, "lines": lines, "line_times": {str(k): v for k, v in sorted(line_times.items())},
           "missing_lines": missing, "segments": report}
    json.dump(res, open(os.path.join(out, "edit.json"), "w"), ensure_ascii=False, indent=1)
    print(f"bruto {dur:.1f}s -> editado {t:.1f}s | {len(segs)} trechos de fala, {len(kept)} mantidos")
    for r in report:
        flag = "ok " if any(k["i"] == r["i"] for k in kept) else "-- "
        print(flag, f"{r['start']:6.2f}-{r['end']:6.2f}", r.get("cov", ""), r["text"][:90])
    if missing:
        print("LINHAS NAO ENCONTRADAS:", [lines[i] for i in missing])


if __name__ == "__main__":
    main()
