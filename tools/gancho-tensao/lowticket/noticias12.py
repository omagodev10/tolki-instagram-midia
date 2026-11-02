"""Estático do lote 12 (02/11): N33 (4:5). 30%: conceito novo da 7.4, mito e verdade do lead ruim. Uso: python3 noticias12.py OUTDIR"""

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
SIZES = {'N33': 1350}
ROW = lambda m, v: ('<div style="display:grid;grid-template-columns:1fr 1.25fr;gap:26px;margin-top:24px;padding-top:24px;border-top:3px solid #15120E">'
  '<div class="inter" style="font-size:37px;line-height:1.22;color:#7A6E5E;font-weight:600"><div class="mono" style="font-size:18px;color:#B3261E;margin-bottom:10px">Mito</div>%s</div>'
  '<div class="inter" style="font-size:37px;line-height:1.22;color:#15120E;font-weight:800"><div class="mono" style="font-size:18px;color:#0E7A3E;margin-bottom:10px">Verdade</div>%s</div></div>') % (m, v)
P['N33'] = """<div class="p" style="background:#F4EFE6;color:#15120E">
<div class="mono" style="font-size:22px;color:#7A6E5E;display:flex;justify-content:space-between"><span>Mito e verdade</span><span>Atendimento</span></div>
<div class="sans" style="font-size:112px;line-height:1.0;margin-top:30px">"O lead está ruim."</div>
<div class="ser" style="font-size:54px;line-height:1.15;margin-top:14px;color:#4A4036">Ou a conversa parou no preço?</div>
<div style="margin-top:10px">""" + ROW('Quem pergunta o preço só quer preço.', 'Ele ainda não sabe por que pagar. Mostrar isso é da recepção.') + ROW('Preciso de mais leads.', 'Antes, veja quantos já chamaram e nunca receberam uma pergunta de volta.') + ROW('A culpa é da secretária.', 'Ninguém ensinou a recepção a conduzir a conversa.') + """</div>
<div class="foot"><div class="mono" style="font-size:22px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#15120E;color:#F4EFE6">Ver o método</div></div></div>"""


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
