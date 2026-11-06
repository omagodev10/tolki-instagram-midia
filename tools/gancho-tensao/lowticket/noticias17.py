"""Estáticos do lote 17 (06/11): N42 (a mesma pergunta de horário, duas recepções, variação da N37 na letra D) e N43 (ponto de vista do paciente perdido, conceito novo da 7.4). Uso: python3 noticias17.py OUTDIR"""

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
SIZES = {'N42': 1350, 'N43': 1350}

PAC = lambda t: '<div class="inter" style="align-self:flex-start;background:#fff;color:#111;font-size:34px;line-height:1.2;padding:15px 23px;border-radius:20px 20px 20px 4px;max-width:88%%;margin-top:13px">%s</div>' % t
REC = lambda t: '<div class="inter" style="align-self:flex-end;background:#D9FDD3;color:#111;font-size:34px;line-height:1.2;padding:15px 23px;border-radius:20px 20px 4px 20px;max-width:88%%;margin-top:13px">%s</div>' % t
BOX = lambda tit, cor, msgs, fim: ('<div style="background:#EFE7DD;border-radius:24px;padding:22px 28px 24px;margin-top:26px;display:flex;flex-direction:column">'
  '<div class="mono" style="font-size:21px;color:%s">%s</div>%s<div class="sans" style="font-size:40px;margin-top:16px;color:%s">%s</div></div>') % (cor, tit, msgs, cor, fim)
P['N42'] = """<div class="p" style="background:#0B1A28;color:#fff;padding:60px 66px 56px">
<div class="sans" style="font-size:78px;line-height:1.02">"Tem horário essa semana?"<br><span style="color:#FFD400">Duas recepções.</span></div>
""" + BOX('Recepção que pergunta', '#B3261E', PAC('Tem horário essa semana?') + REC('Tem sim! Qual horário fica melhor pra você?') + PAC('Vou ver minha agenda e te aviso.'), 'Nunca avisou.') + BOX('Recepção que define', '#0E7A3E', PAC('Tem horário essa semana?') + REC('Tem! Quarta 9h ou quinta 17h?') + PAC('Quinta 17h.'), 'Horário marcado.') + """
<div class="foot" style="margin-top:auto"><div><div class="mono" style="font-size:20px;color:#FFD400">Método A.G.E.N.D.A. · R$ 47</div><div class="inter" style="font-size:22px;color:#9FB3C2;margin-top:8px">Conversas: exemplo ilustrativo</div></div><div class="btn" style="background:#FFD400;color:#15120E">Ver o método</div></div></div>"""
P['N43'] = """<div class="p" style="background:#F3EBDD;color:#15120E;padding:72px 76px 60px">
<div class="mono" style="font-size:22px;color:#7A6E5E">Carta de um paciente · exemplo ilustrativo</div>
<div class="sans" style="font-size:104px;line-height:1;margin-top:30px">Eu sou o paciente que sua clínica perdeu ontem.</div>
<div class="ser" style="font-size:48px;line-height:1.22;margin-top:40px">Perguntei o valor às 19h. Recebi só o preço, às 9h do dia seguinte. Ninguém perguntou do que eu precisava.<br>Marquei na clínica que respondeu primeiro e me deu dois horários.</div>
<div class="sans" style="font-size:60px;line-height:1.05;margin-top:40px;color:#B3261E">Não foi o preço.<br>Foi a conversa.</div>
<div class="inter" style="font-size:32px;line-height:1.3;margin-top:36px;border-top:3px solid #15120E;padding-top:24px">O Método A.G.E.N.D.A. ensina sua recepção a conduzir a conversa até o horário marcado. Aula de 10 minutos e mensagens prontas.</div>
<div class="foot"><div class="mono" style="font-size:20px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#15120E;color:#FFD400">Ver o método</div></div></div>"""


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
