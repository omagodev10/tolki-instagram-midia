#!/usr/bin/env python3
"""render.py: monta o Reel a partir do edit.json (analyze.py) e do plan.json.
Uso: python3 render.py raw.mp4 work_dir/edit.json plan.json out.mp4
plan.json: {"cards":[{"line":0,"until":1,"kind":"top|full","html":"..."}], "zoom":[1,1.12]}
"""
import json, os, re, subprocess, sys, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
NODE_DIR = os.environ.get("REELKIT_NODE", HERE)
ASSETS = os.path.join(HERE, "assets")
W, HH, FPS = 1080, 1920, 30

BLUE, PURPLE, INK = "#1597D4", "#8A3FD1", "#0E1A2B"


def ass_color(hex6, alpha="00"):
    h = hex6.lstrip("#")
    return f"&H{alpha}{h[4:6]}{h[2:4]}{h[0:2]}".upper()


def ts(t):
    t = max(0, t)
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def clean_word(w):
    w = w.strip()
    w = re.sub(r"^[\"'“”(]+|[\"'“”),.;:!]+$", "", w)
    return w.upper()


def chunks(words, maxw=3, maxc=16):
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        txt = " ".join(clean_word(x["w"]) for x in cur)
        nxt = words[i + 1] if i + 1 < len(words) else None
        end_line = nxt is None or nxt["line"] != w["line"]
        punct = bool(re.search(r"[.?!,:]$", w["w"]))
        gap = nxt is not None and nxt["start"] - w["end"] > 0.25
        if len(cur) >= maxw or len(txt) >= maxc or end_line or punct or gap:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


def write_ass(words, hide, path, size=76, maxw=3, y=1268, maxc=16):
    hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {HH}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,TK Montserrat Black,{size},{ass_color('#FFFFFF')},{ass_color('#FFFFFF')},{ass_color(INK)},{ass_color('#000000','80')},0,0,0,0,100,100,0,0,1,7,2,5,90,90,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    cs = chunks(words, maxw=maxw, maxc=maxc)
    for ci, c in enumerate(cs):
        c_end = c[-1]["end"]
        if ci + 1 < len(cs) and cs[ci + 1][0]["start"] - c_end < 0.35:
            c_end = cs[ci + 1][0]["start"]
        for wi, w in enumerate(c):
            s = w["start"]
            e = c[wi + 1]["start"] if wi + 1 < len(c) else c_end
            if any(a <= (s + e) / 2 <= b for a, b in hide):
                continue
            parts = []
            for wj, x in enumerate(c):
                t = H.unescape(clean_word(x["w"]))
                if wj == wi:
                    parts.append("{\\c" + ass_color("#1AA6E3") + "}" + t + "{\\c" + ass_color("#FFFFFF") + "}")
                else:
                    parts.append(t)
            pop = "{\\fscx88\\fscy88\\t(0,90,\\fscx100\\fscy100)}" if wi == 0 else ""
            ev.append(f"Dialogue: 0,{ts(s)},{ts(e)},Cap,,0,0,0,,{{\\pos(540,{y})}}{pop}{' '.join(parts)}")
    open(path, "w", encoding="utf-8").write(hdr + "\n".join(ev) + "\n")


ICON = os.path.join(ASSETS, "tolki-icon.png")
LOGO_W = os.path.join(ASSETS, "tolki-logo-white.png")
LOGO_D = os.path.join(ASSETS, "tolki-logo-dark.png")


def fonts_css():
    return "".join(f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('file://{FONTS}/{fn}')}}" for fam, w, fn in [
        ("Montserrat", 800, "montserrat-latin-800.ttf"), ("Montserrat", 900, "montserrat-latin-900.ttf"),
        ("Inter", 400, "inter-latin-600.ttf"), ("Inter", 600, "inter-latin-600.ttf"), ("Inter", 700, "inter-latin-700.ttf"), ("Inter", 800, "inter-latin-800.ttf")])


def card_html(c):
    k = c["kind"]
    body = c.get("html", "")
    if k == "top":
        bg = c.get("bg", "#FFFFFF"); fg = c.get("fg", INK)
        inner = f"""<div style="position:absolute;left:90px;right:90px;top:{c.get('y',250)}px;display:flex;justify-content:center">
<div style="background:{bg};border-radius:20px;padding:30px 44px 32px;box-shadow:0 18px 50px rgba(0,0,0,.28);max-width:900px">
<div style="font-family:Montserrat;font-weight:900;text-transform:uppercase;font-size:{c.get('size',66)}px;line-height:1.04;color:{fg};text-align:{c.get('align','center')};letter-spacing:-0.5px">{body}</div></div></div>"""
    elif k == "list":
        items = "".join(
            f"""<div style="display:{'flex' if i < c['n'] else 'none'};align-items:center;gap:22px;margin-top:22px">
<div style="flex:0 0 58px;height:58px;border-radius:50%;background:{BLUE};color:#fff;font-family:Montserrat;font-weight:900;font-size:32px;display:flex;align-items:center;justify-content:center">{i+1}</div>
<div style="font-family:Montserrat;font-weight:900;text-transform:uppercase;font-size:46px;line-height:1.05;color:{INK}">{t}</div></div>"""
            for i, t in enumerate(c["items"]))
        inner = f"""<div style="position:absolute;left:90px;right:90px;top:240px">
<div style="background:#fff;border-radius:20px;padding:30px 40px 36px;box-shadow:0 18px 50px rgba(0,0,0,.28)">
<div style="font-family:Inter;font-weight:700;font-size:28px;letter-spacing:3px;color:{PURPLE};text-transform:uppercase">{c.get('title','')}</div>{items}</div></div>"""
    elif k == "number":
        inner = f"""<div style="position:absolute;inset:0;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 90px">
<img src="file://{LOGO_D}" style="position:absolute;top:250px;height:56px">
<div style="font-family:Inter;font-weight:700;font-size:34px;letter-spacing:4px;color:{PURPLE};text-transform:uppercase;margin-bottom:10px">{c.get('kicker','')}</div>
<div style="font-family:Montserrat;font-weight:900;font-size:{c.get('size',230)}px;line-height:1;color:{BLUE};white-space:nowrap;letter-spacing:-6px">{body}</div>
<div style="font-family:Inter;font-weight:600;font-size:42px;line-height:1.3;color:#5B6673;text-align:center;margin-top:34px;max-width:860px">{c.get('sub','')}</div></div>"""
    elif k == "virada":
        inner = f"""<div style="position:absolute;inset:0;background:{PURPLE};display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 90px;text-align:center">
<img src="file://{ICON}" style="width:200px;height:auto;margin-bottom:46px">
<div style="font-family:Montserrat;font-weight:900;font-size:{c.get('size',112)}px;line-height:1.0;color:#fff;text-transform:uppercase">{body}</div>
<div style="font-family:Inter;font-weight:600;font-size:38px;line-height:1.4;color:#F1E6FB;margin-top:40px;max-width:880px">{c.get('sub','')}</div></div>"""
    else:
        raise ValueError(k)
    ff = fonts_css()
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{ff}html,body{{margin:0;background:transparent}}</style></head><body><div style='position:relative;width:{W}px;height:{HH}px;overflow:hidden'>{inner}</div></body></html>"


def music_drop(path, win=0.05):
    """instante do drop: maior salto de energia (média de 1 s depois contra 1 s antes) nos primeiros 20 s"""
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-t", "20", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    k = int(16000 * win); n = len(x) // k
    if n < 60:
        return 0.0
    r = np.sqrt(np.mean(x[:n * k].reshape(n, k) ** 2, axis=1) + 1e-12)
    m = int(1.0 / win)
    best, bi = 0.0, 0
    for i in range(m, n - m):
        g = r[i:i + m].mean() / (r[i - m:i].mean() + 1e-6)
        if g > best:
            best, bi = g, i
    return bi * win


def render_cards(src, out):
    os.makedirs(out, exist_ok=True)
    return run(["node", os.path.join(NODE_DIR, "cards.js"), src, out])


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-3000:]); sys.exit(r.returncode)
    return r


def main():
    raw, edit_p, plan_p, out = sys.argv[1:5]
    E = json.load(open(edit_p, encoding="utf-8"))
    P = json.load(open(plan_p, encoding="utf-8"))
    work = os.path.join(os.path.dirname(os.path.abspath(edit_p)), "render")
    os.makedirs(os.path.join(work, "html"), exist_ok=True)
    import shutil
    for d in ("html", "png"):
        shutil.rmtree(os.path.join(work, d), ignore_errors=True)
    os.makedirs(os.path.join(work, "html"), exist_ok=True)
    LT = {int(k): v for k, v in E["line_times"].items()}
    total = E["out_duration"]

    # efeitos sonoros (biblioteca em plan["sfx_lib"]: nome -> arquivo)
    LIB = {k: v for k, v in P.get("sfx_lib", {}).items() if v and os.path.exists(v)}
    events = []  # (instante, nome, ganho)

    def word_t(l, k):
        ws = sorted([w for w in E["words"] if w["line"] == l], key=lambda w: w["start"])
        return ws[min(k, len(ws) - 1)]["start"] if ws else LT[l][0]

    def card_events(c, t0):
        nm = c.get("sfx", P.get("card_sfx", "whoosh"))
        if nm and nm in LIB:
            events.append((t0, nm, c.get("sfx_gain", 0.45)))
        for e in c.get("sfx_at", []):
            st = c.get("starts") or [0.0]
            base = t0 + (st[min(e["i"], len(st) - 1)] if "i" in e else e.get("t", 0.0))
            events.append((base + e.get("offset", 0.0), e["name"], e.get("gain", 0.5)))

    # cartões: tempo de cada um pela linha do roteiro
    cards = []
    for i, c in enumerate(P.get("cards", [])):
        a = c["line"]; b = c.get("until", a)
        if a not in LT or b not in LT:
            print("aviso: linha sem tempo, cartão ignorado:", c.get("html", "")[:40]); continue
        t0 = max(0, LT[a][0] - 0.12)
        if c.get("instant") and a == 0:
            t0 = 0.0  # gancho já visível no primeiro quadro (capa do Reel)
        nxt = min([v[0] for k, v in LT.items() if k > b] or [total])
        t1 = min(total, max(LT[b][1] + 0.15, min(nxt, LT[b][1] + 0.6)))
        if "t1_pad" in c:
            t1 = min(total, LT[b][1] + c["t1_pad"])
        name = f"c{i:02d}"
        if c["kind"] == "broll":
            cards.append({"name": name, "t0": round(t0, 3), "t1": round(t1, 3), "full": True, "broll": c["src"], "captions": True,
                          "ss": c.get("ss", 0.0)})
            card_events(c, t0)
            continue
        if c["kind"] == "anim":
            import math, motion
            N = int(math.ceil((t1 - t0) * FPS)) + 1
            if c.get("starts_lines"):
                c = dict(c, starts=[max(0.0, LT[l][0] - 0.1 - t0) for l in c["starts_lines"] if l in LT])
            if c.get("starts_at"):  # [[linha, índice da palavra], ...] → início exato daquela palavra
                st = []
                for l, k in c["starts_at"]:
                    ws = sorted([w for w in E["words"] if w["line"] == l], key=lambda w: w["start"])
                    st.append(max(0.0, (ws[min(k, len(ws) - 1)]["start"] if ws else LT[l][0]) - 0.1 - t0))
                c = dict(c, starts=st)
            if c.get("at_word"):
                l, k = c["at_word"]
                ws = sorted([w for w in E["words"] if w["line"] == l], key=lambda w: w["start"])
                c = dict(c, at=max(0.0, (ws[min(k, len(ws) - 1)]["start"] if ws else LT[l][0]) - 0.05 - t0))
            html, full = motion.anim_html(c, t1 - t0, {"icon": ICON, "logo_dark": LOGO_D, "logo_white": LOGO_W}, fonts_css(), W, HH)
            open(os.path.join(work, "html", f"{name}__{N}.seq.html"), "w", encoding="utf-8").write(html)
            cards.append({"name": name, "t0": round(t0, 3), "t1": round(t1, 3), "full": full, "seq": True})
            card_events(c, t0)
            continue
        open(os.path.join(work, "html", name + ".html"), "w", encoding="utf-8").write(card_html(c))
        cards.append({"name": name, "t0": round(t0, 3), "t1": round(t1, 3), "full": c["kind"] in ("number", "virada"),
                      "instant": bool(c.get("instant"))})
        card_events(c, t0)
    for e in P.get("sfx_events", []):  # eventos soltos: {"name","line","word"?,"offset"?,"gain"?} ou {"abs": s}
        if "abs" in e:
            t = e["abs"]
        elif e.get("line") in LT:
            t = (word_t(e["line"], e["word"]) if "word" in e else LT[e["line"]][0]) + e.get("offset", 0.0)
        else:
            continue
        events.append((max(0.0, t), e["name"], e.get("gain", 0.5)))
    # cartões em sequência na mesma área: o anterior termina quando o próximo começa
    tops = sorted([c for c in cards if not c["full"]], key=lambda c: c["t0"])
    for x, y in zip(tops, tops[1:]):
        if x["t1"] > y["t0"]:
            x["t1"] = y["t0"]; x["cut"] = True
    if cards:
        render_cards(os.path.join(work, "html"), os.path.join(work, "png"))
    hide = [(c["t0"], c["t1"]) for c in cards if c["full"] and not c.get("captions")]
    ass = os.path.join(work, "captions.ass")
    write_ass(E["words"], hide, ass, size=P.get("cap_size", 76), maxw=P.get("cap_words", 3), y=P.get("cap_y", 1268),
              maxc=P.get("cap_chars", 16))

    # grafo do ffmpeg
    clips = E["clips"]; n = len(clips)
    zoom = P.get("zoom", [1.0, 1.12])
    fy = P.get("face_y", 0.32)
    eq = P.get("eq", "eq=contrast=1.05:saturation=1.08:brightness=0.01")
    f = [f"[0:v]split={n}" + "".join(f"[s{i}]" for i in range(n)), f"[0:a]asplit={n}" + "".join(f"[r{i}]" for i in range(n))]
    for i, c in enumerate(clips):
        z = zoom[i % len(zoom)] if i else 1.0
        zw, zh = int(round(W * z / 2) * 2), int(round(HH * z / 2) * 2)
        f.append(f"[s{i}]trim=start={c['src_start']}:end={c['src_end']},setpts=PTS-STARTPTS,"
                 f"scale={zw}:{zh}:force_original_aspect_ratio=increase,crop={W}:{HH}:(iw-{W})/2:(ih-{HH})*{fy},setsar=1,fps={FPS}[v{i}]")
        d = c['src_end'] - c['src_start']
        f.append(f"[r{i}]atrim=start={c['src_start']}:end={c['src_end']},asetpts=PTS-STARTPTS,"
                 f"afade=t=in:d=0.008,afade=t=out:st={max(0, d - 0.012):.3f}:d=0.012[a{i}]")
    f.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[cv][ca]")
    f.append(f"[cv]{eq}[base0]")
    inputs = ["-i", raw]
    last = "base0"
    for j, c in enumerate(cards):
        d = c["t1"] - c["t0"]
        idx = j + 1
        if c.get("broll"):
            inputs += ["-ss", f"{c.get('ss', 0):.3f}", "-t", f"{d:.3f}", "-i", c["broll"]]
            f.append(f"[{idx}:v]scale={int(W*1.06)}:{int(HH*1.06)}:force_original_aspect_ratio=increase,crop={W}:{HH},setsar=1,fps={FPS},"
                     f"eq=contrast=1.04:saturation=1.05,format=rgba,setpts=PTS-STARTPTS+{c['t0']}/TB[o{j}]")
        elif c.get("seq"):
            # a sequência vira um vídeo RGBA à parte: se um PNG sair sem alfa (tela toda opaca), o ffmpeg
            # reconfiguraria o grafo principal no meio e o Reel terminaria ali
            mov = os.path.join(work, "png", c["name"] + ".mkv")
            run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-start_number", "1", "-i",
                 os.path.join(work, "png", c["name"], "%04d.png"), "-vf", "format=rgba", "-c:v", "png", mov])
            inputs += ["-i", mov]
            fo = "" if (c.get("cut") or c["full"]) else f",fade=t=out:st={max(0, d - 0.14):.3f}:d=0.14:alpha=1"
            f.append(f"[{idx}:v]format=rgba{fo},setpts=PTS-STARTPTS+{c['t0']}/TB[o{j}]")
        else:
            png = os.path.join(work, "png", c["name"] + ".png")
            inputs += ["-loop", "1", "-t", f"{d:.3f}", "-framerate", str(FPS), "-i", png]
            fo = "" if c.get("cut") else f",fade=t=out:st={max(0, d - 0.14):.3f}:d=0.14:alpha=1"
            fi = "" if c.get("instant") else ",fade=t=in:st=0:d=0.16:alpha=1"
            f.append(f"[{idx}:v]format=rgba{fi}{fo},setpts=PTS-STARTPTS+{c['t0']}/TB[o{j}]")
        ydist = 0 if (c["full"] or c.get("seq") or c.get("instant")) else 36
        f.append(f"[{last}][o{j}]overlay=x=0:y='if(lt(t-{c['t0']},0.18),{ydist}*(1-(t-{c['t0']})/0.18),0)':eof_action=pass:eval=frame:enable='between(t,{c['t0']},{c['t1']})'[b{j}]")
        last = f"b{j}"
    for k, l in enumerate(P.get("flash_lines", [])):  # flash branco curto na entrada da linha (corte de impacto)
        if l in LT:
            tf = max(0.0, LT[l][0] - 0.1)
            f.append(f"color=c=white:s={W}x{HH}:r={FPS}:d={total:.3f},format=rgba,colorchannelmixer=aa=0.55[fl{k}]")
            f.append(f"[{last}][fl{k}]overlay=0:0:enable='between(t,{tf:.3f},{tf + 0.07:.3f})'[fx{k}]")
            last = f"fx{k}"
    f.append(f"[{last}]ass={ass}:fontsdir={FONTS},format=yuv420p[vout]")
    # áudio: voz + efeitos + trilha (abaixa sozinha quando a voz entra)
    n_in = 1 + len(cards)
    f.append("[ca]aformat=sample_rates=48000:channel_layouts=stereo[cas]")
    voice, extra = "[cas]", []
    mus = P.get("music") or {}
    if mus.get("src") and os.path.exists(mus["src"]) and mus.get("drop_at_line") in LT:
        mus = dict(mus, ss=round(max(0.0, music_drop(mus["src"]) - (LT[mus["drop_at_line"]][0] - 0.05)), 3))
        print("trilha: começa em", mus["ss"], "s para o drop cair na linha", mus["drop_at_line"])
    if mus.get("src") and os.path.exists(mus["src"]):
        inputs += ["-stream_loop", "-1", "-i", mus["src"]]
        mi = n_in; n_in += 1
        fo = mus.get("fade_out", 1.2)
        f.append(f"[{mi}:a]atrim=start={mus.get('ss', 0)}:duration={total:.3f},asetpts=PTS-STARTPTS,"
                 f"aformat=sample_rates=48000:channel_layouts=stereo,volume={mus.get('gain', 0.22)},"
                 f"afade=t=in:d=0.2,afade=t=out:st={max(0, total - fo):.3f}:d={fo}[mus]")
        f.append("[cas]asplit=2[vo][key]")
        f.append(f"[mus][key]sidechaincompress=threshold={mus.get('duck_thr', 0.03)}:ratio={mus.get('duck_ratio', 6)}:"
                 f"attack=15:release=350[mduck]")
        voice, extra = "[vo]", ["[mduck]"]
    if P.get("sfx", True):
        if LIB:
            for k, (t, nm, g) in enumerate(sorted(events)):
                if nm not in LIB or t >= total:
                    continue
                inputs += ["-i", LIB[nm]]
                ms = int(t * 1000)
                f.append(f"[{n_in}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={g},adelay={ms}|{ms}[w{k}]")
                extra.append(f"[w{k}]"); n_in += 1
        else:  # sem biblioteca: whoosh sintetizado na entrada de cada cartão
            for k, c in enumerate(cards):
                t = c["t0"]
                f.append(f"anoisesrc=d=0.32:c=pink:a=0.5:r=48000,highpass=f=900,lowpass=f=6000,"
                         f"afade=t=in:d=0.12,afade=t=out:st=0.12:d=0.2,volume=0.10,adelay={int(t*1000)}|{int(t*1000)},aformat=channel_layouts=stereo[w{k}]")
                extra.append(f"[w{k}]")
    amix_in = voice
    if extra:
        f.append(voice + "".join(extra) + f"amix=inputs={len(extra)+1}:duration=first:normalize=0[mix]")
        amix_in = "[mix]"
    f.append(f"{amix_in}highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=90:makeup=2,"
             f"loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[aout]")
    fg = os.path.join(work, "graph.txt")
    open(fg, "w").write(";\n".join(f))
    cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex_script", fg, "-map", "[vout]", "-map", "[aout]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(FPS),
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-t", f"{total:.3f}", out]
    run(cmd)
    json.dump(cards, open(os.path.join(work, "cards.json"), "w"), indent=1)
    print("ok", out, f"{total:.1f}s", len(cards), "cartões")


if __name__ == "__main__":
    main()
