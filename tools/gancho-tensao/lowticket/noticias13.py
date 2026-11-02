"""Estático do lote 13 (02/11): N35 (4:5), a N1 no modelo caixinha para o feed. Uso: python3 noticias13.py OUTDIR"""

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
SIZES = {'N35': 1350}
P['N35'] = """<div class="p" style="background:#0B1A28;color:#fff;justify-content:flex-start">
<div style="border-radius:28px;overflow:hidden;box-shadow:0 12px 34px rgba(0,0,0,.4)"><div class="inter" style="background:#262626;color:#fff;font-size:30px;text-align:center;padding:18px">Faça uma pergunta</div>
<div class="inter" style="background:#fff;color:#111;font-size:54px;line-height:1.22;text-align:center;padding:36px 44px;font-weight:600">Passo o preço no WhatsApp e o paciente some. É normal?</div></div>
<div class="sans" style="font-size:92px;line-height:1.02;margin-top:50px">É comum, mas não é normal.</div>
<div class="ser" style="font-size:54px;line-height:1.15;margin-top:18px;color:#8FD3F4">Quem recebe só o preço vai embora.</div>
<div style="display:flex;align-items:center;justify-content:center;gap:30px;margin-top:44px;background:#fff;color:#111;border-radius:26px;padding:28px 36px"><div class="sans" style="font-size:112px;color:#0B7FC4;white-space:nowrap">15% → 45%</div></div>
<div class="inter" style="font-size:34px;line-height:1.25;margin-top:20px;color:#DCE6EE">Agendamento na Odonto Excellence, clínica que mudou o atendimento com a Tolki.</div>
<div class="foot"><div class="mono" style="font-size:22px;color:#FFD400">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#FFD400;color:#15120E">Ver o método</div></div></div>"""


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
