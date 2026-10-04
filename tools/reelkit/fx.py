#!/usr/bin/env python3
"""fx.py: efeitos de edição "viral" aplicados no vídeo pronto (legenda e cartões incluídos).
Uso: python3 fx.py entrada.mp4 eventos.json saida.mp4
eventos.json (tempos em segundos no vídeo final):
  {"punch":  [{"t": 1.2, "amt": 0.12, "attack": 0.05, "decay": 0.16}],   zoom que soca e volta
   "shake":  [{"t": 2.0, "dur": 0.3, "amp": 18}],                        tremida com leve giro
   "glitch": [{"t": 0.0, "dur": 0.18, "rgb": 22, "invert": false}]}       RGB separado + faixas deslocadas
O áudio é copiado sem mexer. Precisa de numpy e opencv-python-headless."""
import json, math, subprocess, sys

import cv2
import numpy as np


def probe(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate", "-of", "json", p], capture_output=True, text=True).stdout
    s = json.loads(out)["streams"][0]
    n, d = s["r_frame_rate"].split("/")
    return s["width"], s["height"], float(n) / float(d)


def zoom_at(t, ev):
    z = 1.0
    for p in ev.get("punch", []):
        dt = t - p["t"]
        if dt < 0:
            continue
        a, att = p.get("amt", 0.1), p.get("attack", 0.05)
        z += a * dt / att if dt < att else a * math.exp(-(dt - att) / p.get("decay", 0.16))
    return z


def shake_at(t, i, ev):
    dx = dy = rot = 0.0
    for s in ev.get("shake", []):
        dt, d = t - s["t"], s.get("dur", 0.3)
        if 0 <= dt < d:
            k = (1 - dt / d) ** 1.5 * s.get("amp", 16)
            r = np.random.default_rng(int(s["t"] * 1000) * 31 + i)
            dx += k * r.uniform(-1, 1); dy += k * r.uniform(-1, 1); rot += k * 0.05 * r.uniform(-1, 1)
    return dx, dy, rot


def glitch(fr, t, i, ev, H):
    for g in ev.get("glitch", []):
        dt, d = t - g["t"], g.get("dur", 0.18)
        if not 0 <= dt < d:
            continue
        k = 1 - dt / d
        r = np.random.default_rng(int(g["t"] * 1000) * 7 + i)
        s = int(g.get("rgb", 22) * k) + 2
        fr = np.dstack([np.roll(fr[:, :, 0], -s, axis=1), fr[:, :, 1], np.roll(fr[:, :, 2], s, axis=1)])
        for _ in range(int(r.integers(3, 8))):
            y0, h = int(r.integers(0, H - 40)), int(r.integers(10, 130))
            fr[y0:y0 + h] = np.roll(fr[y0:y0 + h], int(r.integers(-90, 90) * k), axis=1)
        if g.get("invert") and dt < 0.04:
            fr = 255 - fr
    return fr


def main():
    src, evp, out = sys.argv[1:4]
    ev = json.load(open(evp, encoding="utf-8"))
    W, H, fps = probe(src)
    cy = H * ev.get("center_y", 0.42)  # zoom e giro em volta do rosto, não do meio da tela
    rd = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    wr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", f"{fps:.3f}",
                           "-i", "-", "-i", src, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                           "-profile:v", "high", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", "-shortest", out],
                          stdin=subprocess.PIPE)
    size, i = W * H * 3, 0
    while True:
        buf = rd.stdout.read(size)
        if len(buf) < size:
            break
        fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy()
        t = i / fps
        z = zoom_at(t, ev)
        dx, dy, rot = shake_at(t, i, ev)
        if abs(z - 1) > 1e-3 or dx or dy or rot:
            M = cv2.getRotationMatrix2D((W / 2, cy), rot, z)
            M[0, 2] += dx; M[1, 2] += dy
            fr = cv2.warpAffine(fr, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        fr = glitch(fr, t, i, ev, H)
        wr.stdin.write(np.ascontiguousarray(fr).tobytes())
        i += 1
    wr.stdin.close(); wr.wait(); rd.wait()
    print("fx ok", out, i, "quadros,", len(ev.get("punch", [])), "punches,", len(ev.get("shake", [])), "tremidas,",
          len(ev.get("glitch", [])), "glitches")


if __name__ == "__main__":
    main()
