#!/usr/bin/env python3
"""align_fw.py: para vídeo SEM cortes (avatar ou vídeo já editado).
Transcreve com faster-whisper (tempo por palavra) e casa com o roteiro,
gerando edit.json no mesmo formato do analyze.py (um clipe só).
Uso: python3 align_fw.py video.mp4 script.txt out_dir [modelo=small]"""
import json, os, re, sys, difflib, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze import toks, norm

video, script, out = sys.argv[1:4]
model = sys.argv[4] if len(sys.argv) > 4 else "small"
os.makedirs(out, exist_ok=True)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                           capture_output=True, text=True).stdout.strip())
from faster_whisper import WhisperModel
m = WhisperModel(model, device="cpu", compute_type="int8")
segs, _ = m.transcribe(video, language="pt", word_timestamps=True, vad_filter=False,
                       condition_on_previous_text=False, beam_size=5)
hw = []  # (token, start, end)
for s in segs:
    for w in s.words:
        for t in toks(w.word):
            hw.append((t, w.start, w.end))
lines = [l.strip() for l in open(script, encoding="utf-8") if l.strip()]
st, sdisp = [], []  # tokens do roteiro e palavra exibida de cada token
for li, l in enumerate(lines):
    for w in re.findall(r"\S+", l):
        tk = toks(w)
        for t in tk:
            st.append((t, len(sdisp)))
        sdisp.append({"w": w, "line": li, "n": len(tk)})
times = [None] * len(st)
sm = difflib.SequenceMatcher(None, [t for t, _ in st], [t for t, _, _ in hw], autojunk=False)
for tag, a0, a1, b0, b1 in sm.get_opcodes():
    if tag == "equal" or (tag == "replace" and a1 - a0 == b1 - b0):
        for k in range(a1 - a0):
            times[a0 + k] = (hw[b0 + k][1], hw[b0 + k][2])
    elif tag == "replace":
        span = (hw[b0][1], hw[b1 - 1][2])
        n = a1 - a0
        for k in range(n):
            times[a0 + k] = (span[0] + (span[1] - span[0]) * k / n, span[0] + (span[1] - span[0]) * (k + 1) / n)
# interpola o que ficou sem tempo
known = [i for i, t in enumerate(times) if t]
for i in range(len(times)):
    if times[i] is None:
        prev = max([k for k in known if k < i], default=None)
        nxt = min([k for k in known if k > i], default=None)
        a = times[prev][1] if prev is not None else 0.0
        b = times[nxt][0] if nxt is not None else dur
        times[i] = (a, max(a + 0.08, b))
words, ti = [], 0
for d in sdisp:
    if d["n"] == 0:
        continue
    t0, t1 = times[ti][0], times[ti + d["n"] - 1][1]
    words.append({"w": d["w"], "line": d["line"], "start": round(t0, 3), "end": round(max(t1, t0 + 0.06), 3)})
    ti += d["n"]
lt = {}
for w in words:
    v = lt.setdefault(w["line"], [w["start"], w["end"]])
    v[0], v[1] = min(v[0], w["start"]), max(v[1], w["end"])
# corta em cada troca de linha (ponto médio da pausa) para o zoom alternar por frase
clips, cuts = [], [0.0]
keys = sorted(lt)
for a, b in zip(keys, keys[1:]):
    cuts.append(round((lt[a][1] + lt[b][0]) / 2, 3))
cuts.append(dur)
for i in range(len(cuts) - 1):
    if cuts[i + 1] - cuts[i] > 0.2:
        clips.append({"src_start": cuts[i], "src_end": cuts[i + 1], "out_start": cuts[i], "seg": i})
if os.environ.get("NO_SPLIT"):
    clips = [{"src_start": 0.0, "src_end": dur, "out_start": 0.0, "seg": 0}]
res = {"source": video, "source_duration": dur, "out_duration": dur,
       "clips": clips, "words": words, "lines": lines,
       "line_times": {str(k): v for k, v in sorted(lt.items())}, "missing_lines": [], "segments": [],
       "whisper": " ".join(t for t, _, _ in hw)}
json.dump(res, open(os.path.join(out, "edit.json"), "w"), ensure_ascii=False, indent=1)
print(f"ok {dur:.1f}s, {len(hw)} palavras ouvidas, {len(words)} palavras do roteiro, casamento {sm.ratio():.2f}")
