"""Estáticos do lote 8 (29/10): N24 e N25 (4:5).
N24 (70%): a N1 vencedora (6 vendas) com a mesma manchete e o mesmo corpo, mais um gráfico de barras 15% contra 45% (testa prova visual).
N25 (30%): conceito novo, o produto na frente: as mensagens prontas para copiar e colar (Biblioteca de 29/10: concorrentes vendendo "70 scripts por R$ 10"). Exemplo ilustrativo.
Só provas permitidas; selo "conteúdo de marca". Uso: python3 noticias8.py OUTDIR"""

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
.rule{height:3px;margin:18px 0}
.foot{margin-top:auto;display:flex;align-items:center;justify-content:space-between}
.btn{padding:22px 38px;border-radius:60px;font-family:'Inter Tight';font-weight:800;font-size:38px}'''

def page(body):
    return ('<!doctype html><html><head><meta charset="utf-8"><base href="file://%s/">'
            '<link rel="stylesheet" href="fonts.css"><style>%s</style></head><body>%s</body></html>') % (ENGINE, CSS, body)

CAB = '''<div style="display:flex;justify-content:space-between;align-items:flex-end"><div class="sern" style="font-size:64px;letter-spacing:-1px">Gestão de Clínicas</div><div class="mono" style="font-size:18px;color:#7A6E5E">Conteúdo de marca</div></div>
<div class="rule" style="background:#15120E"></div><div class="mono" style="font-size:20px;color:#7A6E5E;display:flex;justify-content:space-between"><span>Atendimento</span><span>WhatsApp</span></div>'''

P = {}
SIZES = {'N24': 1350, 'N25': 1350}
CORPO = 'Na Odonto Excellence, o agendamento foi de 15% para 45% depois que a clínica mudou o atendimento no WhatsApp.'
BAR = lambda lab, pct, cor: ('<div style="display:flex;flex-direction:column;align-items:center;justify-content:flex-end;width:250px">'
    '<div class="sans" style="font-size:64px;color:%s">%s</div>'
    '<div style="width:170px;height:%dpx;background:%s;margin-top:12px"></div>'
    '<div class="mono" style="font-size:20px;color:#7A6E5E;margin-top:14px">%s</div></div>') % (cor, pct, int(pct[:-1])*5, cor, lab)
P['N24'] = '''<div class="p" style="background:#F4EFE6;color:#15120E">''' + CAB + '''
<div class="mono" style="font-size:22px;color:#B3261E;margin-top:50px">Caso real · atendimento com a Tolki</div>
<div class="sans" style="font-size:88px;line-height:1.02;margin-top:24px">Clínica triplica a taxa de agendamento mudando só a resposta do "quanto custa?"</div>
<div style="display:flex;gap:40px;align-items:flex-end;margin-top:40px;height:400px">''' + BAR('Antes', '15%', '#9A8F80') + BAR('Depois', '45%', '#B3261E') + '''
<div class="ser" style="font-size:42px;line-height:1.2;color:#4A4036;flex:1">''' + CORPO + '''</div></div>
<div class="foot"><div class="mono" style="font-size:22px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#15120E;color:#F4EFE6">Ler o método</div></div></div>'''
MSG = lambda letra, txt: ('<div style="display:flex;gap:22px;align-items:flex-start"><div class="sans" style="min-width:76px;height:76px;border-radius:38px;background:#0F8FD0;color:#fff;font-size:44px;display:flex;align-items:center;justify-content:center">%s</div>'
    '<div class="inter" style="background:#DCF8C6;border-radius:24px;padding:22px 28px;font-size:38px;line-height:1.28;color:#0B1A28">%s</div></div>') % (letra, txt)
P['N25'] = '''<div class="p" style="background:#FFFFFF;color:#0B1A28">
<div class="mono" style="font-size:22px;color:#0F8FD0;display:flex;justify-content:space-between"><span>Copie e cole hoje</span><span style="color:#5B6B7A">Exemplo ilustrativo</span></div><div class="rule" style="background:#D5DEE8"></div>
<div class="sans" style="font-size:84px;line-height:1.02;margin-top:36px">As 3 mensagens que fazem o paciente do "quanto custa?" marcar horário</div>
<div style="display:flex;flex-direction:column;gap:30px;margin-top:56px">''' + MSG('A', 'Oi, Ana! Que bom que chamou. Me conta: é para você mesma?') + MSG('G', 'Antes do valor, deixa eu te explicar o que está incluso na avaliação.') + MSG('D', 'Tenho quinta às 10h ou sexta às 16h. Qual fica melhor?') + '''</div>
<div class="foot"><div class="mono" style="font-size:22px;color:#5B6B7A">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#0B1A28;color:#fff">Ver as mensagens</div></div></div>'''


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
