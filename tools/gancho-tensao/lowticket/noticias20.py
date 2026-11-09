"""Estáticos do lote 20 (09/11): N48 (variação da N1, mesmo jornal creme com o número na frente: 15% para 45%, Odonto Excellence) e N49 (o "boa tarde" de 3 horas depois, POV de conversa; conceito novo da 7.4, letra A). Uso: python3 noticias20.py OUTDIR"""

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
SIZES = {'N48': 1350, 'N49': 1350}

P['N48'] = """<div class="p" style="background:#F4EFE6;color:#15120E">
<div style="display:flex;justify-content:space-between;align-items:flex-end"><div class="sern" style="font-size:64px;letter-spacing:-1px">Gestão de Clínicas</div><div class="mono" style="font-size:18px;color:#7A6E5E">Conteúdo de marca</div></div>
<div class="rule" style="background:#15120E"></div><div class="mono" style="font-size:20px;color:#7A6E5E;display:flex;justify-content:space-between"><span>Atendimento</span><span>WhatsApp</span></div>
<div class="mono" style="font-size:22px;color:#B3261E;margin-top:56px">Caso real · atendimento com a Tolki</div>
<div class="sans" style="font-size:178px;line-height:.95;margin-top:30px">15%<span style="color:#B3261E">→</span>45%</div>
<div class="sans" style="font-size:70px;line-height:1.05;margin-top:30px">A taxa de agendamento triplicou. O que mudou foi a conversa no WhatsApp.</div>
<div class="ser" style="font-size:48px;line-height:1.22;margin-top:40px;color:#4A4036">Na Odonto Excellence, o agendamento foi de 15% para 45% depois que a clínica mudou o atendimento com a gente.</div>
<div class="foot"><div class="mono" style="font-size:22px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#15120E;color:#F4EFE6">Ler o método</div></div></div>"""

def B(lado, t, hora, cor, txt='#15120E'):
    al = 'flex-end' if lado == 'd' else 'flex-start'
    return ('<div style="display:flex;justify-content:%s;margin-top:18px"><div style="max-width:78%%;background:%s;color:%s;border-radius:26px;padding:20px 28px">'
            '<div class="inter" style="font-size:38px;line-height:1.25">%s</div><div class="mono" style="font-size:18px;letter-spacing:2px;opacity:.6;text-align:right;margin-top:6px">%s</div></div></div>') % (al, cor, txt, t, hora)

P['N49'] = """<div class="p" style="background:#ECE5DD;color:#15120E;padding:60px 66px 56px">
<div class="mono" style="font-size:21px;color:#B3261E">Terça, 14h02</div>
<div class="sans" style="font-size:88px;line-height:1.02;margin-top:16px">Ela respondeu. Três horas depois.</div>
<div style="background:#E2D9CE;border-radius:30px;padding:16px 26px 26px;margin-top:30px">
""" + B('e', 'Oi! Quanto custa a avaliação? Queria marcar essa semana.', '14:02', '#FFFFFF') + B('d', 'Boa tarde! A avaliação é R$ 150.', '17:11', '#D9FDD3') + B('e', 'Obrigada, já marquei em outra clínica.', '17:40', '#FFFFFF') + """
</div>
<div class="inter" style="font-size:34px;line-height:1.3;margin-top:30px;color:#3A332C">A primeira letra do método é Acolher em até 5 minutos. Numa clínica que mudou o atendimento com a gente, a equipe foi de 59 para 121 contratos em um mês.</div>
<div class="foot" style="margin-top:auto"><div><div class="mono" style="font-size:20px;color:#B3261E">Método A.G.E.N.D.A. · R$ 47</div><div class="inter" style="font-size:22px;color:#7A6E5E;margin-top:8px">Conversa e valor: exemplo ilustrativo</div></div><div class="btn" style="background:#15120E;color:#ECE5DD">Ver o método</div></div></div>"""


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
