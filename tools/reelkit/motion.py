"""motion.py: cartões animados (HTML + CSS) no visual Tolki.
Cada template devolve o miolo HTML; o cards.js captura quadro a quadro
controlando o tempo das animações (document.getAnimations)."""

INK, BLUE, PURPLE, LBLUE = "#0E1A2B", "#1597D4", "#8A3FD1", "#1AA6E3"

BASE_CSS = """
*{box-sizing:border-box}
.pop{animation:pop .42s cubic-bezier(.2,.9,.3,1.25) both}
@keyframes pop{from{opacity:0;transform:translateY(34px) scale(.94)}to{opacity:1;transform:none}}
.fade{animation:fade .35s ease-out both}
@keyframes fade{from{opacity:0}to{opacity:1}}
.slide{animation:slide .45s cubic-bezier(.2,.8,.2,1) both}
@keyframes slide{from{opacity:0;transform:translateX(-60px)}to{opacity:1;transform:none}}
"""


def _d(x):
    return f"animation-delay:{x:.3f}s"


def chat(c, D, a):
    """Conversa em que a IA responde mas não agenda e o paciente some."""
    msgs = c.get("msgs") or [
        ["p", "Oi! Queria agendar uma avaliação."],
        ["ia", "Olá! Claro, posso te passar informações sobre nossos tratamentos."],
        ["p", "Tem horário amanhã?"],
        ["typing", ""],
        ["ia", "Vou encaminhar pra recepção, tá bom?"],
        ["sys", c.get("end", "Paciente saiu da conversa")],
    ]
    n = len(msgs)
    rows = []
    for i, (who, txt) in enumerate(msgs):
        t = 0.08 * D + i * (0.78 * D / max(n - 1, 1))
        if who == "p":
            rows.append(f'<div class="pop" style="{_d(t)};align-self:flex-start;max-width:800px;background:#fff;border-radius:6px 30px 30px 30px;padding:30px 36px;font:600 48px/1.3 Inter;color:{INK};box-shadow:0 6px 18px rgba(14,26,43,.08)">{txt}</div>')
        elif who == "ia":
            rows.append(f'<div class="pop" style="{_d(t)};align-self:flex-end;max-width:820px"><div style="font:700 22px Inter;letter-spacing:2px;color:{BLUE};text-align:right;margin:0 8px 8px 0">ASSISTENTE DE IA</div><div style="background:{LBLUE};color:#fff;border-radius:30px 6px 30px 30px;padding:30px 36px;font:600 48px/1.3 Inter">{txt}</div></div>')
        elif who == "typing":
            rows.append(f'<div class="pop" style="{_d(t)};align-self:flex-end;background:#dfe7ef;border-radius:30px;padding:22px 30px;display:flex;gap:12px;animation:pop .4s both, gone .2s {t + 0.5 * D / n:.3f}s forwards">' + "".join(f'<span style="width:16px;height:16px;border-radius:50%;background:#8a96a3;display:block;animation:blink 0.9s {k*0.15:.2f}s infinite"></span>' for k in range(3)) + '</div>')
        else:
            rows.append(f'<div class="pop" style="{_d(t)};align-self:center;margin-top:18px;background:#FDECEC;color:#D93A3F;border-radius:16px;padding:18px 30px;font:800 42px Inter;letter-spacing:.5px">{txt}</div>')
    return f"""<style>@keyframes blink{{0%,100%{{opacity:.3}}50%{{opacity:1}}}}@keyframes gone{{to{{opacity:0;height:0;padding:0;margin:0}}}}</style>
<div style="position:absolute;inset:0;background:#EEF2F6">
<div class="fade" style="position:absolute;left:70px;right:70px;top:230px;background:#fff;border-radius:28px;padding:26px 30px;display:flex;align-items:center;gap:22px;box-shadow:0 8px 24px rgba(14,26,43,.08)">
<div style="width:84px;height:84px;border-radius:50%;background:{PURPLE};display:flex;align-items:center;justify-content:center"><img src="file://{a['icon']}" style="width:58px"></div>
<div><div style="font:800 38px Inter;color:{INK}">{c.get('title','Sua clínica')}</div><div style="font:600 26px Inter;color:#2BB673">online agora</div></div></div>
<div style="position:absolute;left:70px;right:70px;top:440px;display:flex;flex-direction:column;gap:34px">{''.join(rows)}</div></div>"""


def counter(c, D, a):
    """Número grande contando (R$ 0 → R$ 59, 15% → 45%) com barra opcional."""
    v0, v1 = c.get("from", 0), c.get("to", 59)
    pre, suf = c.get("prefix", ""), c.get("suffix", "")
    dur = min(1.1, 0.45 * D)
    bar = ""
    if c.get("bar"):
        bar = f"""<div class="fade" style="{_d(0.1)};width:860px;margin-top:50px">
<div style="position:relative;height:40px;border-radius:20px;background:#E8EEF4;overflow:hidden">
<div style="position:absolute;left:0;top:0;bottom:0;background:{BLUE};border-radius:20px;animation:grow {dur:.2f}s cubic-bezier(.3,.8,.3,1) {0.2:.2f}s both"></div></div>
<div style="display:flex;justify-content:space-between;font:700 28px Inter;color:#5B6673;margin-top:16px"><span>antes: {v0}{suf}</span><span style="color:{BLUE}">depois: {v1}{suf}</span></div></div>
<style>@keyframes grow{{from{{width:{v0}%}}to{{width:{v1}%}}}}</style>"""
    return f"""<style>@property --n{{syntax:'<integer>';initial-value:{v0};inherits:false}}
.num{{--n:{v0};counter-reset:n var(--n);animation:count {dur:.2f}s cubic-bezier(.2,.7,.2,1) 0.2s both}}
.num::after{{content:'{pre}' counter(n) '{suf}'}}
@keyframes count{{from{{--n:{v0}}}to{{--n:{v1}}}}}</style>
<div style="position:absolute;inset:0;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 90px">
<img class="fade" src="file://{a['logo_dark']}" style="position:absolute;top:250px;height:56px">
<div class="pop" style="font:700 34px Inter;letter-spacing:4px;color:{PURPLE};text-transform:uppercase;margin-bottom:6px">{c.get('kicker','')}</div>
<div class="num pop" style="font:900 {c.get('size',250)}px/1 Montserrat;color:{BLUE};white-space:nowrap;letter-spacing:-6px"></div>
{bar}
<div class="fade" style="{_d(0.25 * D)};font:600 42px/1.3 Inter;color:#5B6673;text-align:center;margin-top:34px;max-width:860px">{c.get('sub','')}</div></div>"""


def cycle(c, D, a):
    """Virada roxa com as etapas do ciclo surgindo em sequência."""
    steps = c.get("steps") or ["Captura", "Resposta", "Qualificação", "Agendamento", "Recuperação"]
    n = len(steps)
    t0, span = 0.18 * D, 0.62 * D
    rows = "".join(
        f'<div class="slide" style="{_d(t0 + i * span / n)};display:flex;align-items:center;gap:28px;height:96px">'
        f'<div style="flex:0 0 72px;height:72px;border-radius:50%;background:#fff;color:{PURPLE};font:900 36px Montserrat;display:flex;align-items:center;justify-content:center">{i+1}</div>'
        f'<div style="font:900 56px Montserrat;color:#fff;text-transform:uppercase;letter-spacing:-.5px">{s}</div></div>'
        for i, s in enumerate(steps))
    return f"""<style>@keyframes line{{from{{height:0}}to{{height:{(n-1)*96}px}}}}</style>
<div style="position:absolute;inset:0;background:{PURPLE};display:flex;flex-direction:column;align-items:center;justify-content:center">
<img class="pop" src="file://{a['icon']}" style="width:150px;margin-bottom:30px">
<div class="pop" style="{_d(0.06 * D)};font:900 {c.get('size',104)}px/1 Montserrat;color:#fff;text-transform:uppercase;margin-bottom:56px">{c.get('html','Ciclo inteiro')}</div>
<div style="position:relative;width:820px">
<div style="position:absolute;left:35px;top:48px;width:4px;background:rgba(255,255,255,.45);animation:line {span:.2f}s linear {t0:.2f}s both"></div>
{rows}</div></div>"""


def comment(c, D, a):
    """Comentário sendo digitado (CTA 'Comenta PALAVRA') sobre o vídeo, no topo."""
    word = c.get("word", "AGENDA")
    n = len(word)
    tw = min(0.9, 0.45 * D)
    return f"""<style>@keyframes type{{from{{width:0}}to{{width:{n}ch}}}}@keyframes caret{{50%{{border-color:transparent}}}}
@keyframes heart{{0%{{opacity:0;transform:scale(.3)}}60%{{opacity:1;transform:scale(1.25)}}100%{{opacity:1;transform:scale(1)}}}}</style>
<div style="position:absolute;left:80px;right:80px;top:250px">
<div class="pop" style="background:#fff;border-radius:28px;padding:30px 34px;box-shadow:0 18px 50px rgba(0,0,0,.28);display:flex;align-items:center;gap:26px">
<div style="flex:0 0 86px;height:86px;border-radius:50%;background:#E8EEF4;display:flex;align-items:center;justify-content:center;font:800 34px Inter;color:#8A94A0">{c.get('initial','V')}</div>
<div style="flex:1">
<div style="font:700 26px Inter;color:#8A94A0;margin-bottom:6px">{c.get('label','Comenta aqui embaixo')}</div>
<div style="font:900 78px/1 Montserrat;color:{PURPLE};white-space:nowrap;overflow:hidden;width:0;font-family:Montserrat;border-right:6px solid {PURPLE};padding-right:6px;animation:type {tw:.2f}s steps({n}) 0.3s both, caret .6s step-end infinite">{word}</div></div>
<svg style="flex:0 0 64px;animation:heart .5s cubic-bezier(.2,.9,.3,1.4) {0.35 + tw:.2f}s both" width="64" height="64" viewBox="0 0 24 24"><path fill="#E5484D" d="M12 21s-7.5-4.6-9.6-9.2C.9 8.4 3 4.5 6.9 4.5c2.2 0 3.6 1.2 5.1 3 1.5-1.8 2.9-3 5.1-3 3.9 0 6 3.9 4.5 7.3C19.5 16.4 12 21 12 21z"/></svg>
</div></div>"""


TEMPLATES = {"chat": (chat, True), "counter": (counter, True), "cycle": (cycle, True), "comment": (comment, False)}


def anim_html(c, D, assets, fonts_css, W, H):
    fn, full = TEMPLATES[c["tpl"]]
    inner = fn(c, D, assets)
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{fonts_css}{BASE_CSS}html,body{{margin:0;background:transparent}}</style></head>"
            f"<body><div style='position:relative;width:{W}px;height:{H}px;overflow:hidden'>{inner}</div></body></html>"), full
