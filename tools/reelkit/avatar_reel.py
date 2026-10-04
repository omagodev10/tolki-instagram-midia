#!/usr/bin/env python3
"""avatar_reel.py: monta o Reel do avatar a partir de um manifesto JSON.
Uso: python3 avatar_reel.py manifesto.json saida.mp4
manifesto = {
  "script": "roteiro.txt",
  "plan": "plano.json",
  "scenes": [{"video": url_ou_arquivo, "audio": url_ou_arquivo}, ...],   # na ordem
  "broll": {"BROLL_NOITE": url, ...}                                      # placeholders do plano
}
Para cada cena: alinha o áudio limpo ao áudio do vídeo gerado (correlação),
corta o vídeo no fim da fala, emenda tudo, cronometra as palavras e renderiza."""
import json, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.abspath("work_avatar")
os.makedirs(W, exist_ok=True)


def sh(*a):
    r = subprocess.run(list(a), capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-2000:]); sys.exit(1)
    return r.stdout


def fetch(src, name):
    dst = os.path.join(W, name)
    if src.startswith("http"):
        sh("curl", "-sfL", "-o", dst, src)
    else:
        sh("cp", src, dst)
    return dst


def pcm(path, sr=16000, secs=None):
    cmd = ["ffmpeg", "-v", "error", "-i", path] + (["-t", str(secs)] if secs else []) + ["-ac", "1", "-ar", str(sr), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, dtype=np.float32)


def dur(path):
    return float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path).strip())


def onset(x, sr=16000, db=-35.0):
    """instante (s) em que a fala começa: primeira janela de 10 ms acima de -35 dBFS"""
    k = int(sr * 0.01)
    n = len(x) // k
    rms = np.sqrt(np.mean(x[:n * k].reshape(n, k) ** 2, axis=1) + 1e-12)
    idx = np.nonzero(20 * np.log10(rms) > db)[0]
    return float(idx[0]) * 0.01 if len(idx) else 0.0


def lag(ref, sig, sr=16000, maxlag=1.0):
    """atraso (s) de ref dentro de sig pela correlação cruzada do envelope"""
    def env(x):
        x = np.abs(x)
        k = int(sr * 0.01)
        return np.convolve(x, np.ones(k) / k, mode="same")[::k]
    a, b = env(ref), env(sig)
    n = len(a) + len(b)
    c = np.fft.irfft(np.fft.rfft(b, n) * np.conj(np.fft.rfft(a, n)), n)
    m = int(maxlag / 0.01)
    cand = np.concatenate([c[:m], c[-m:]])
    i = int(np.argmax(cand))
    shift = i if i < m else i - 2 * m
    return shift * 0.01


def noise_thr(path):
    """limiar de silêncio adaptado ao ruído de fundo (o áudio do Seedance às vezes tem ambiente alto)"""
    x = pcm(path)
    k = 160
    n = len(x) // k
    if n < 10:
        return "-35dB"
    db = 20 * np.log10(np.sqrt(np.mean(x[:n * k].reshape(n, k) ** 2, axis=1)) + 1e-9)
    lo, hi = np.percentile(db, 10), np.percentile(db, 95)
    return f"{max(-45.0, min(-22.0, lo + 0.3 * (hi - lo))):.1f}dB"


def speech_segments(path, thr=None, gap=0.28, pad=0.1):
    """trechos com fala pelo silencedetect; pausas maiores que gap saem"""
    thr = thr or noise_thr(path)
    log = subprocess.run(["ffmpeg", "-v", "info", "-i", path, "-af", f"silencedetect=n={thr}:d={gap}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    import re
    ss = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", log)]
    se = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", log)]
    D = dur(path)
    sil = list(zip(ss, se + [D] * (len(ss) - len(se))))
    keep, cur = [], 0.0
    for a, b in sil:
        if a > cur:
            keep.append((max(0.0, cur - pad), min(D, a + pad)))
        cur = b
    if cur < D - 0.05:
        keep.append((max(0.0, cur - pad), D))
    # junta trechos que se encostam
    out = []
    for a, b in keep:
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        elif b - a > 0.15:
            out.append((a, b))
    return out


def speech_segments_fw(path, gap=0.3, pad0=0.08, pad1=0.2, tail=0.6):
    """trechos com fala pelas palavras do Whisper (robusto a ruído de fundo); pausas maiores que gap saem"""
    from faster_whisper import WhisperModel
    m = WhisperModel("small", compute_type="int8")
    segs, _ = m.transcribe(path, language="pt", word_timestamps=True, vad_filter=False,
                           condition_on_previous_text=False, beam_size=5)
    out = []
    for s in segs:
        for w in s.words:
            if out and w.start - out[-1][1] < gap:
                out[-1][1] = max(out[-1][1], w.end)
            else:
                out.append([w.start, w.end])
    D = dur(path)
    res = []
    for a, b in out:
        a, b = max(0.0, a - pad0), min(D, b + pad1)
        if res and a <= res[-1][1]:
            res[-1] = (res[-1][0], b)
        else:
            res.append((a, b))
    if res:  # o Whisper costuma marcar o fim da última palavra cedo demais: deixa a frase final respirar
        res[-1] = (res[-1][0], min(D, res[-1][1] - pad1 + tail))
    return res


def build_scene(k, sc, mode, speed, prev):
    p = os.path.join(W, f"p{k}.mkv")
    vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1"
    if mode == "own":
        v = fetch(sc["video"], f"v{k}.mp4")
        segs = speech_segments_fw(v)
        got = sum(b - a for a, b in segs)
        if sc.get("match") and sc.get("audio"):
            # o Seedance costuma esticar a fala: acelera a cena até o ritmo do áudio limpo
            ref = sum(b - a for a, b in speech_segments(fetch(sc["audio"], f"ref{k}.mp3")))
            speed = min(1.25, max(1.0, got / ref * speed)) if ref > 0 else speed
        print(f"cena {k} (áudio do próprio vídeo): {len(segs)} trechos, {got:.2f}s de {dur(v):.2f}s, velocidade {speed:.3f}")
        fl = []
        for i, (a, b) in enumerate(segs):
            fl.append(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS,{vf}[v{i}];[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,"
                      f"afade=t=in:d=0.01,afade=t=out:st={max(0,b-a-0.02):.3f}:d=0.02[a{i}]")
        fl.append("".join(f"[v{i}][a{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=1[cv][ca]")
        fl.append(f"[cv]setpts=PTS/{speed}[vo];[ca]atempo={speed},aresample=48000[ao]")
        sh("ffmpeg", "-v", "error", "-y", "-i", v, "-filter_complex", ";".join(fl), "-map", "[vo]", "-map", "[ao]",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "15", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "pcm_s16le", "-ac", "2", p)
    else:  # cover: áudio limpo sobre o último quadro da cena anterior (fica coberto por cartões e B-roll)
        a = fetch(sc["audio"], f"a{k}.mp3")
        last = os.path.join(W, f"last{k}.png")
        sh("ffmpeg", "-v", "error", "-y", "-sseof", "-0.1", "-i", prev, "-frames:v", "1", "-update", "1", last)
        da = dur(a) / speed
        sh("ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "30", "-i", last, "-i", a, "-t", f"{da:.3f}",
           "-filter:a", f"atempo={speed},aresample=48000", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
           "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-ac", "2", p)
        print(f"cena {k} (coberta por gráficos): {da:.2f}s")
    return p


def main():
    man = json.load(open(sys.argv[1], encoding="utf-8"))
    out = os.path.abspath(sys.argv[2])
    parts = []
    speed = float(man.get("speed", 1.0))
    for k, sc in enumerate(man["scenes"]):
        mode = sc.get("mode", "clean")
        if mode in ("own", "cover"):
            parts.append(build_scene(k, sc, mode, speed, parts[-1] if parts else None))
            continue
        v = fetch(sc["video"], f"v{k}.mp4")
        a = fetch(sc["audio"], f"a{k}.mp3")
        la = onset(pcm(v)) - onset(pcm(a))  # >0: a fala no vídeo começa depois
        da = dur(a)
        start = max(0.0, la)
        print(f"cena {k}: atraso {la:+.2f}s, fala {da:.2f}s, vídeo {dur(v):.2f}s")
        p = os.path.join(W, f"p{k}.mkv")
        sh("ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", "-i", v, "-i", a, "-map", "0:v", "-map", "1:a",
           "-t", f"{da:.3f}", "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,tpad=stop_mode=clone:stop_duration=1",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "15", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", p)
        parts.append(p)
    # emenda reencodando (o concat com -c copy deixava o áudio com tempos voltando e o render parava no meio)
    joined = os.path.join(W, "joined.mkv")
    ins = sum([["-i", p] for p in parts], [])
    n = len(parts)
    fl = "".join(f"[{i}:v]setpts=PTS-STARTPTS[v{i}];[{i}:a]aresample=48000,asetpts=PTS-STARTPTS[a{i}];" for i in range(n))
    fl += "".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]"
    sh("ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fl, "-map", "[v]", "-map", "[a]",
       "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-pix_fmt", "yuv420p", "-r", "30",
       "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", joined)
    print("emendado:", f"{dur(joined):.2f}s", "partes:", [round(dur(p), 2) for p in parts])
    # plano com os B-rolls baixados
    plan = json.load(open(man["plan"], encoding="utf-8"))
    for i, (key, url) in enumerate(man.get("broll", {}).items()):
        local = fetch(url, f"broll{i}.mp4")
        for c in plan["cards"]:
            if c.get("src") == key:
                c["src"] = local
    plan_p = os.path.join(W, "plan.json")
    json.dump(plan, open(plan_p, "w"), ensure_ascii=False)
    sh("python3", os.path.join(HERE, "align_fw.py"), joined, man["script"], os.path.join(W, "out"), man.get("whisper", "small"))
    print(sh("python3", os.path.join(HERE, "render.py"), joined, os.path.join(W, "out", "edit.json"), plan_p, out))


if __name__ == "__main__":
    main()
