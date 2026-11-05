"""Estáticos do lote 16 (05/11): N40 (o mesmo "vou pensar", duas recepções, variação da N37) e N41 (clínica com uma recepcionista só, prova 21 para 62). Uso: python3 noticias16.py OUTDIR"""

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
SIZES = {'N40': 1350, 'N41': 1350}
TOPO = """<div style="display:flex;justify-content:space-between;align-items:flex-end;border-bottom:3px solid #15120E;padding-bottom:22px"><div class="sern" style="font-size:66px;line-height:1">Gestão de Clínicas</div><div class="mono" style="font-size:18px;color:#7A6E5E">Conteúdo de marca</div></div>
<div class="mono" style="font-size:20px;color:#7A6E5E;display:flex;justify-content:space-between;margin-top:16px"><span>Odontologia</span><span>WhatsApp</span></div>"""

PAC = lambda t: '<div class="inter" style="align-self:flex-start;background:#fff;color:#111;font-size:33px;line-height:1.2;padding:14px 22px;border-radius:20px 20px 20px 4px;max-width:88%%;margin-top:12px">%s</div>' % t
REC = lambda t: '<div class="inter" style="align-self:flex-end;background:#D9FDD3;color:#111;font-size:33px;line-height:1.2;padding:14px 22px;border-radius:20px 20px 4px 20px;max-width:88%%;margin-top:12px">%s</div>' % t
BOX = lambda tit, cor, msgs, fim: ('<div style="background:#EFE7DD;border-radius:24px;padding:20px 26px 22px;margin-top:22px;display:flex;flex-direction:column">'
  '<div class="mono" style="font-size:21px;color:%s">%s</div>%s<div class="sans" style="font-size:38px;margin-top:14px;color:%s">%s</div></div>') % (cor, tit, msgs, cor, fim)
P['N40'] = """<div class="p" style="background:#0B1A28;color:#fff;padding:56px 66px 54px">
<div class="sans" style="font-size:80px;line-height:1">O mesmo "vou pensar".<br>Duas recepções.</div>
""" + BOX('Recepção que aceita', '#B3261E', PAC('Vou pensar e te falo.') + REC('Tá bom! Qualquer coisa estamos à disposição.'), 'Fim da conversa.') + BOX('Recepção que conduz', '#0E7A3E', PAC('Vou pensar e te falo.') + REC('Claro! O que pesou mais: o valor ou a data?') + PAC('O valor, sendo sincera.') + REC('Entendi. Na avaliação a doutora te mostra as opções. Terça 10h ou quinta 15h?') + PAC('Quinta!'), 'Horário marcado.') + """
<div class="foot" style="margin-top:auto"><div><div class="mono" style="font-size:20px;color:#FFD400">Método A.G.E.N.D.A. · R$ 47</div><div class="inter" style="font-size:22px;color:#9FB3C2;margin-top:8px">Conversas: exemplo ilustrativo</div></div><div class="btn" style="background:#FFD400;color:#15120E">Ver o método</div></div></div>"""
P['N41'] = """<div class="p" style="background:#FFD400;color:#15120E;padding:72px 72px 60px">
<div class="mono" style="font-size:24px">Clínica com uma recepcionista só</div>
<div class="sans" style="font-size:118px;line-height:.98;margin-top:28px">Você não precisa de mais gente na recepção.</div>
<div style="background:#15120E;color:#fff;border-radius:28px;padding:36px 42px;margin-top:44px">
<div class="sans" style="font-size:170px;line-height:1">21 <span style="color:#FFD400">→</span> 62</div>
<div class="inter" style="font-size:36px;line-height:1.25;margin-top:14px">contratos em um mês. Uma atendente, numa clínica que mudou o atendimento com a gente.</div></div>
<div class="ser" style="font-size:70px;line-height:1.1;margin-top:48px">Antes de contratar, treine quem você já tem.</div>
<div class="foot"><div><div class="mono" style="font-size:20px">Método A.G.E.N.D.A. · R$ 47</div><div class="inter" style="font-size:22px;margin-top:8px">Atendimento com a Tolki</div></div><div class="btn" style="background:#15120E;color:#FFD400">Ver o método</div></div></div>"""


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
