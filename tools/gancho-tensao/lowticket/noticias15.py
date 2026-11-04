"""Estáticos do lote 15 (04/11): N38 (N1 falando com a dona de clínica) e N39 (áudio que ninguém ouviu). Uso: python3 noticias15.py OUTDIR"""

import asyncio, os, sys
from playwright.async_api import async_playwright
ENGINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = '''*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;overflow:hidden}
.p{position:relative;width:1080px;height:1350px;padding:70px 72px;display:flex;flex-direction:column}
.v{height:1920px;padding:270px 72px 380px}
.mono{font-family:'JetBrains Mono';font-weight:700;letter-spacing:5px;text-transform:uppercase}
.ser{font-family:'Instrument Serif';font-style:italic}.sern{font-family:'Instrument Serif';font-style:normal}
.sans{font-family:'Inter Tight';font-weight:800;letter-spacing:-.03em}
.inter{font-family:Inter}
.rule{height:3px;margin:18px 0;flex-shrink:0}
.foot{margin-top:auto;display:flex;align-items:center;justify-content:space-between}
.btn{padding:22px 38px;border-radius:60px;font-family:'Inter Tight';font-weight:800;font-size:38px}'''

def page(body):
    return ('<!doctype html><html><head><meta charset="utf-8"><base href="file://%s/">'
            '<link rel="stylesheet" href="fonts.css"><style>%s</style></head><body>%s</body></html>') % (ENGINE, CSS, body)

P = {}
SIZES = {'N38': 1350, 'N39': 1350}
TOPO = """<div style="display:flex;justify-content:space-between;align-items:flex-end;border-bottom:3px solid #15120E;padding-bottom:22px"><div class="sern" style="font-size:66px;line-height:1">Gestão de Clínicas</div><div class="mono" style="font-size:18px;color:#7A6E5E">Conteúdo de marca</div></div>
<div class="mono" style="font-size:20px;color:#7A6E5E;display:flex;justify-content:space-between;margin-top:16px"><span>Recepção</span><span>WhatsApp</span></div>"""
P['N38'] = """<div class="p" style="background:#F1EDE5;color:#15120E">""" + TOPO + """
<div class="mono" style="font-size:23px;color:#B3261E;margin-top:62px">Caso real · Atendimento com a Tolki</div>
<div class="sans" style="font-size:112px;line-height:1;margin-top:24px">Dona de clínica, sua recepção responde ou agenda?</div>
<div class="ser" style="font-size:49px;line-height:1.2;margin-top:34px;color:#4A4036">Na Odonto Excellence, o agendamento foi de 15% para 45% depois que a clínica mudou o atendimento no WhatsApp.</div>
<div class="foot"><div class="mono" style="font-size:22px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#15120E;color:#F1EDE5">Ler o método</div></div></div>"""
ONDA = ''.join('<span style="display:inline-block;width:6px;height:%dpx;background:#54656F;border-radius:3px;margin-right:5px"></span>' % h for h in [14,30,44,22,52,34,18,46,60,28,40,16,50,32,20,42,26,12,36,24,48,18,30,14])
P['N39'] = """<div class="p" style="background:#0B1A28;color:#fff;padding:64px 70px 58px">
<div class="sans" style="font-size:104px;line-height:1">Ela mandou um áudio às 9h12.<br><span style="color:#FFD400">Ninguém ouviu.</span></div>
<div style="background:#EFE7DD;border-radius:26px;padding:26px 28px;margin-top:40px;display:flex;flex-direction:column">
<div class="inter" style="align-self:flex-start;background:#fff;color:#111;font-size:32px;padding:18px 24px;border-radius:20px 20px 20px 4px;display:flex;align-items:center;gap:20px"><span style="width:0;height:0;border-left:26px solid #54656F;border-top:16px solid transparent;border-bottom:16px solid transparent"></span><span style="display:flex;align-items:center">""" + ONDA + """</span><span style="font-size:27px;color:#667781">0:48</span></div>
<div class="inter" style="align-self:flex-start;font-size:25px;color:#667781;margin:10px 0 0 8px">9h12 · sem resposta</div>
<div class="inter" style="align-self:center;background:#fff;color:#54656F;font-size:25px;padding:8px 20px;border-radius:12px;margin-top:22px">14h37</div>
<div class="inter" style="align-self:flex-end;background:#D9FDD3;color:#111;font-size:34px;line-height:1.2;padding:16px 24px;border-radius:20px 20px 4px 20px;margin-top:18px;max-width:88%">Oi! Desculpa a demora, em que posso ajudar?</div>
<div class="inter" style="align-self:flex-start;background:#fff;color:#111;font-size:34px;line-height:1.2;padding:16px 24px;border-radius:20px 20px 20px 4px;margin-top:14px;max-width:88%">Obrigada, já marquei em outra clínica.</div>
</div>
<div class="ser" style="font-size:47px;line-height:1.15;margin-top:32px;color:#8FD3F4">Quem responde primeiro nem sempre é o melhor. Mas é quem agenda.</div>
<div class="foot"><div><div class="mono" style="font-size:20px;color:#FFD400">Método A.G.E.N.D.A. · R$ 47</div><div class="inter" style="font-size:22px;color:#9FB3C2;margin-top:8px">Conversa: exemplo ilustrativo</div></div><div class="btn" style="background:#FFD400;color:#15120E">Ver o método</div></div></div>"""


async def main(out):
    os.makedirs(out, exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(args=['--allow-file-access-from-files'])
        for k, html in P.items():
            pg = await (await b.new_context(viewport={'width': 1080, 'height': SIZES[k]})).new_page()
            f = os.path.join(ENGINE, '_tmp_' + k + '.html'); open(f, 'w').write(page(html))
            await pg.goto('file://' + f); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            await pg.screenshot(path=os.path.join(out, k + '.jpg'), type='jpeg', quality=92); print(k)
            os.remove(f)
        await b.close()

asyncio.run(main(sys.argv[1]))
