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


def main():
    man = json.load(open(sys.argv[1], encoding="utf-8"))
    out = os.path.abspath(sys.argv[2])
    parts = []
    for k, sc in enumerate(man["scenes"]):
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
    lst = os.path.join(W, "list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    joined = os.path.join(W, "joined.mkv")
    sh("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined)
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
