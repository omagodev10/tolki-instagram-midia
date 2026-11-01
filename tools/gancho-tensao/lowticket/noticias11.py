"""Estáticos do lote 11 (01/11): N30 e N31 (4:5).
N30 (70%): a N1 com a chamada "2 ou 3 atendentes" da N28 e texto só com a prova permitida (substitui a N28, que dizia "sem contratar ninguém", frase fora das provas da seção 4). Testa a manchete de resultado sem a promessa do "só a resposta".
N31 (30%): conceito novo da biblioteca 7.4 (data do momento): Black Friday, gancho de dor: a promoção enche o WhatsApp e o preço seco vira pesquisa de preço. Exemplo ilustrativo. Biblioteca de 01/11: concorrentes falam de falta, de agenda às 21h14 e de resposta automática; ninguém fala da campanha que a própria clínica vai fazer.
Uso: python3 noticias11.py OUTDIR"""

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

CAB = '''<div style="display:flex;justify-content:space-between;align-items:flex-end"><div class="sern" style="font-size:64px;letter-spacing:-1px">Gestão de Clínicas</div><div class="mono" style="font-size:18px;color:#7A6E5E">Conteúdo de marca</div></div>
<div class="rule" style="background:#15120E"></div><div class="mono" style="font-size:20px;color:#7A6E5E;display:flex;justify-content:space-between"><span>Atendimento</span><span>WhatsApp</span></div>'''

P = {}
SIZES = {'N30': 1350, 'N31': 1350}
P['N30'] = """<div class="p" style="background:#F4EFE6;color:#15120E">""" + CAB + """
<div style="margin-top:44px;align-self:flex-start;background:#15120E;color:#F4EFE6;padding:14px 24px" class="mono"><span style="font-size:24px">Clínica com 2 ou 3 atendentes? Leia isto</span></div>
<div class="mono" style="font-size:22px;color:#B3261E;margin-top:34px">Caso real · atendimento com a Tolki</div>
<div class="sans" style="font-size:92px;line-height:1.02;margin-top:22px">Clínica triplica a taxa de agendamento depois de mudar o atendimento no WhatsApp</div>
<div class="ser" style="font-size:48px;line-height:1.2;margin-top:30px;color:#4A4036">Na Odonto Excellence, o agendamento foi de 15% para 45%. Veja onde o paciente some na sua: na resposta do "quanto custa?".</div>
<div class="foot"><div class="mono" style="font-size:22px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#15120E;color:#F4EFE6">Ler o método</div></div></div>"""
BAL = lambda t, eu: ('<div style="display:flex;justify-content:%s;margin-top:16px"><div class="inter" style="background:%s;color:%s;border-radius:22px;padding:18px 28px;font-size:40px;font-weight:700">%s</div></div>') % ('flex-end' if eu else 'flex-start', '#FFD400' if eu else '#262626', '#15120E' if eu else '#FFFFFF', t)
P['N31'] = """<div class="p" style="background:#0E0E0E;color:#FFFFFF">
<div class="mono" style="font-size:22px;color:#FFD400;display:flex;justify-content:space-between"><span>Black Friday · 27/11</span><span style="color:#9A9A9A">Exemplo ilustrativo</span></div><div class="rule" style="background:#FFD400"></div>
<div class="sans" style="font-size:88px;line-height:1.03;margin-top:30px">Sua clínica vai fazer Black Friday?</div>
<div class="ser" style="font-size:52px;line-height:1.18;margin-top:20px;color:#E6E6E6">O desconto enche o WhatsApp. Quem agenda é a recepção.</div>
<div style="margin-top:30px">""" + BAL('Vi a promoção. Quanto fica?', False) + BAL('R$ 299.', True) + BAL('Vou pensar.', False) + """</div>
<div class="inter" style="font-size:40px;line-height:1.3;margin-top:34px;color:#CFCFCF">Sem conduzir a conversa, a promoção vira pesquisa de preço. Em 10 minutos, o método mostra o que responder antes do valor.</div>
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
