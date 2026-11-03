"""Estáticos do lote 14 (03/11): N36 (a N1 com chamada de especialidade) e N37 (a mesma conversa, duas recepções). Uso: python3 noticias14.py OUTDIR"""

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
SIZES = {'N36': 1350, 'N37': 1350}
TOPO = """<div style="display:flex;justify-content:space-between;align-items:flex-end;border-bottom:3px solid #15120E;padding-bottom:22px"><div class="sern" style="font-size:66px;line-height:1">Gestão de Clínicas</div><div class="mono" style="font-size:18px;color:#7A6E5E">Conteúdo de marca</div></div>
<div class="mono" style="font-size:20px;color:#7A6E5E;display:flex;justify-content:space-between;margin-top:16px"><span>Odontologia</span><span>WhatsApp</span></div>"""
P['N36'] = """<div class="p" style="background:#F1EDE5;color:#15120E">""" + TOPO + """
<div class="mono" style="font-size:23px;color:#B3261E;margin-top:62px">Caso real · Atendimento com a Tolki</div>
<div class="sans" style="font-size:106px;line-height:1;margin-top:24px">Dentista, por que o paciente some depois que pergunta o valor?</div>
<div class="ser" style="font-size:49px;line-height:1.2;margin-top:34px;color:#4A4036">Na Odonto Excellence, o agendamento foi de 15% para 45% depois que a clínica mudou o atendimento no WhatsApp.</div>
<div class="foot"><div class="mono" style="font-size:22px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#15120E;color:#F1EDE5">Ler o método</div></div></div>"""
PAC = lambda t: '<div class="inter" style="align-self:flex-start;background:#fff;color:#111;font-size:33px;line-height:1.2;padding:14px 22px;border-radius:20px 20px 20px 4px;max-width:88%%;margin-top:12px">%s</div>' % t
REC = lambda t: '<div class="inter" style="align-self:flex-end;background:#D9FDD3;color:#111;font-size:33px;line-height:1.2;padding:14px 22px;border-radius:20px 20px 4px 20px;max-width:88%%;margin-top:12px">%s</div>' % t
BOX = lambda tit, cor, msgs, fim: ('<div style="background:#EFE7DD;border-radius:24px;padding:20px 26px 22px;margin-top:22px;display:flex;flex-direction:column">'
  '<div class="mono" style="font-size:21px;color:%s">%s</div>%s<div class="sans" style="font-size:38px;margin-top:14px;color:%s">%s</div></div>') % (cor, tit, msgs, cor, fim)
P['N37'] = """<div class="p" style="background:#0B1A28;color:#fff;padding:56px 66px 54px">
<div class="sans" style="font-size:80px;line-height:1">A mesma pergunta.<br>Duas recepções.</div>
""" + BOX('Recepção que informa', '#B3261E', PAC('Oi, quanto custa o clareamento?') + REC('R$ 900.') + PAC('Ok, vou pensar.'), 'E nunca mais respondeu.') + BOX('Recepção que agenda', '#0E7A3E', PAC('Oi, quanto custa o clareamento?') + REC('Oi, Ana! É para alguma data especial?') + PAC('Meu casamento, em março.') + REC('Parabéns! Te mostro como funciona. Terça 10h ou quinta 15h?') + PAC('Terça!'), 'Horário marcado.') + """
<div class="foot" style="margin-top:auto"><div><div class="mono" style="font-size:20px;color:#FFD400">Método A.G.E.N.D.A. · R$ 47</div><div class="inter" style="font-size:22px;color:#9FB3C2;margin-top:8px">Conversas e valor: exemplo ilustrativo</div></div><div class="btn" style="background:#FFD400;color:#15120E">Ver o método</div></div></div>"""


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
