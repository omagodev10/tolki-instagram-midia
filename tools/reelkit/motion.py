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


def checklist(c, D, a):
    """Perguntas surgindo uma a uma, tela cheia branca. Cada item entra no tempo da sua linha."""
    items = c.get("items", [])
    starts = c.get("starts") or [i * D / max(len(items), 1) for i in range(len(items))]
    rows = "".join(
        f'<div class="pop" style="{_d(s)};display:flex;align-items:center;gap:30px;background:#F4F7FA;border-radius:26px;padding:34px 36px;margin-top:30px">'
        f'<div style="flex:0 0 92px;height:92px;border-radius:50%;background:{BLUE};color:#fff;font:900 48px Montserrat;display:flex;align-items:center;justify-content:center">{i+1}</div>'
        f'<div style="font:900 58px/1.08 Montserrat;color:{INK};text-transform:uppercase">{t}</div></div>'
        for i, (t, s) in enumerate(zip(items, starts)))
    return f"""<div style="position:absolute;inset:0;background:#fff;padding:0 70px">
<img class="fade" src="file://{a['logo_dark']}" style="position:absolute;top:250px;left:50%;transform:translateX(-50%);height:56px">
<div style="position:absolute;left:70px;right:70px;top:400px">
<div class="pop" style="font:700 34px Inter;letter-spacing:4px;color:{PURPLE};text-transform:uppercase;margin-bottom:10px">{c.get('title','')}</div>
{rows}</div></div>"""


def compare(c, D, a):
    """Faz a conta: duas barras (ex.: marketing x utilidade) com valores contando e um selo de economia.
    starts = [título, linha 1, linha 2, ...] em segundos a partir do início do cartão."""
    rows = c.get("rows") or [["Como marketing", 340, 100, "#E5484D"], ["Como utilidade", 40, 12, BLUE]]
    starts = c.get("starts") or [0.05 * D] + [0.2 * D + i * 0.3 * D for i in range(len(rows))]
    pre = c.get("prefix", "R$ ")
    css, body = [], []
    for i, (label, v, pct, col) in enumerate(rows):
        s = starts[i + 1] if i + 1 < len(starts) else starts[-1] + 0.8
        g = s + 0.15
        css.append(f"@property --n{i}{{syntax:'<integer>';initial-value:0;inherits:false}}"
                   f".n{i}{{counter-reset:n{i} var(--n{i});animation:c{i} .9s cubic-bezier(.2,.7,.2,1) {g:.2f}s both}}"
                   f".n{i}::after{{content:'{pre}' counter(n{i})}}"
                   f"@keyframes c{i}{{from{{--n{i}:0}}to{{--n{i}:{v}}}}}@keyframes g{i}{{from{{width:0}}to{{width:{pct}%}}}}")
        body.append(f'<div class="pop" style="{_d(s)};margin-top:64px">'
                    f'<div style="display:flex;justify-content:space-between;align-items:flex-end">'
                    f'<div style="font:900 52px/1 Montserrat;color:{INK};text-transform:uppercase">{label}</div>'
                    f'<div class="n{i}" style="font:900 100px/1 Montserrat;color:{col};letter-spacing:-3px"></div></div>'
                    f'<div style="height:58px;border-radius:29px;background:#EEF2F6;overflow:hidden;margin-top:20px">'
                    f'<div style="height:100%;border-radius:29px;background:{col};animation:g{i} .9s cubic-bezier(.3,.8,.3,1) {g:.2f}s both"></div></div></div>')
    grid = ""
    if c.get("grid"):  # enxame de mensagens surgindo enquanto ele fala "mil lembretes"
        nb = int(c.get("grid", 40))
        g0, g1 = starts[0] + 0.35, max(starts[0] + 0.8, (starts[1] if len(starts) > 1 else D) - 0.25)
        grid = ('<div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:44px">' + "".join(
            f'<div class="pop" style="{_d(g0 + (g1 - g0) * i / nb)};width:76px;height:54px;border-radius:18px 18px 18px 6px;'
            f'background:{LBLUE if i % 3 else BLUE};opacity:.9"></div>' for i in range(nb)) + '</div>')
    pill = ""
    if c.get("pill"):
        pt = max(starts[-1] + 0.3, min(starts[-1] + 0.8, D - 0.8))
        pill = (f'<div class="pop" style="{_d(pt)};margin:80px auto 0;width:fit-content;background:#E6F6EE;color:#14935A;border-radius:999px;'
                f'padding:24px 44px;font:900 54px Montserrat;text-transform:uppercase">{c["pill"]}</div>')
    return f"""<style>{''.join(css)}</style>
<div style="position:absolute;inset:0;background:#fff;padding:0 90px">
<img class="fade" src="file://{a['logo_dark']}" style="position:absolute;top:250px;left:50%;transform:translateX(-50%);height:56px">
<div style="position:absolute;left:90px;right:90px;top:400px">
<div class="pop" style="{_d(starts[0])};font:700 34px Inter;letter-spacing:4px;color:{PURPLE};text-transform:uppercase">{c.get('kicker','Faz a conta')}</div>
<div class="pop" style="{_d(starts[0] + 0.06)};font:900 84px/1.05 Montserrat;color:{INK};text-transform:uppercase;margin-top:10px">{c.get('title','')}</div>
{grid}{''.join(body)}{pill}</div>
<div class="fade" style="{_d(starts[0])};position:absolute;left:90px;right:90px;top:1560px;font:600 28px Inter;color:#8A94A0;text-align:center">{c.get('note','')}</div></div>"""


def stamp(c, D, a):
    """Carimbo: palavra grande cai girada e trava a tela (ex.: UTILIDADE)."""
    bg = c.get("bg", PURPLE)
    t = c.get("at", 0.35 * D)
    return f"""<style>@keyframes slam{{0%{{opacity:0;transform:rotate(-7deg) scale(2.6)}}55%{{opacity:1;transform:rotate(-7deg) scale(.92)}}78%{{transform:rotate(-7deg) scale(1.05)}}100%{{opacity:1;transform:rotate(-7deg) scale(1)}}}}
@keyframes shake{{0%,100%{{transform:none}}20%{{transform:translate(-14px,8px)}}40%{{transform:translate(10px,-8px)}}60%{{transform:translate(-8px,5px)}}80%{{transform:translate(5px,-3px)}}}}</style>
<div style="position:absolute;inset:0;background:{bg}"></div>
<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 80px;animation:shake .32s ease-out {t + 0.26:.2f}s both">
<img class="pop" src="file://{a['icon']}" style="width:130px;margin-bottom:46px">
<div class="pop" style="{_d(0.05)};font:800 62px/1.15 Montserrat;color:#fff;text-align:center">{c.get('kicker','')}</div>
<div style="margin-top:56px;border:14px solid #fff;border-radius:26px;padding:22px 50px 16px;font:900 {c.get('size',120)}px/1 Montserrat;color:#fff;letter-spacing:1px;text-transform:uppercase;animation:slam .5s cubic-bezier(.2,.9,.3,1) {t:.2f}s both">{c.get('word','UTILIDADE')}</div>
<div class="fade" style="{_d(t + 0.55)};font:800 50px/1.3 Montserrat;color:#fff;text-align:center;margin-top:70px">{c.get('sub','')}</div></div>"""


TEMPLATES = {"checklist": (checklist, True), "chat": (chat, True), "counter": (counter, True), "cycle": (cycle, True),
             "comment": (comment, False), "compare": (compare, True), "stamp": (stamp, True)}


def anim_html(c, D, assets, fonts_css, W, H):
    fn, full = TEMPLATES[c["tpl"]]
    inner = fn(c, D, assets)
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{fonts_css}{BASE_CSS}html,body{{margin:0;background:transparent}}</style></head>"
            f"<body><div style='position:relative;width:{W}px;height:{H}px;overflow:hidden'>{inner}</div></body></html>"), full
