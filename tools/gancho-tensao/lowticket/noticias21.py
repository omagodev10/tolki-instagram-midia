"""Estáticos do lote 21 (10/11): N50 (variação da N8 vencedora, mesmo jornal azul e mesmo corpo, gancho novo "Antes de abrir vaga na recepção") e N51 (conceito novo da 7.4: a conta ao vivo do paciente que perguntou o preço e sumiu, recibo; exemplo ilustrativo). Uso: python3 noticias21.py OUTDIR"""

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
SIZES = {'N50': 1350, 'N51': 1350}

P['N50'] = """<div class="p" style="background:#EEF3F8;color:#0B1A28">
<div style="display:flex;justify-content:space-between;align-items:flex-end"><div class="sern" style="font-size:64px;letter-spacing:-1px">Gestão de Clínicas</div><div class="mono" style="font-size:18px;color:#5B6B7A">Conteúdo de marca</div></div>
<div class="rule" style="background:#0B1A28"></div><div class="mono" style="font-size:20px;color:#5B6B7A;display:flex;justify-content:space-between"><span>Equipe</span><span>Recepção</span></div>
<div class="mono" style="font-size:22px;color:#0F8FD0;margin-top:66px">Caso real · atendimento com a Tolki</div>
<div class="sans" style="font-size:96px;line-height:1.02;margin-top:22px">Antes de abrir vaga na recepção, leia isto.</div>
<div class="ser" style="font-size:50px;line-height:1.22;margin-top:34px;color:#33414F">Numa clínica que mudou o atendimento com a gente, a mesma atendente foi de 21 para 62 contratos em um mês. A equipe, de 59 para 121.</div>
<div class="foot"><div class="mono" style="font-size:22px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#0B1A28;color:#EEF3F8">Ler o método</div></div></div>"""

def L(a, b, forte=False):
    peso = 'font-weight:800;' if forte else ''
    return ('<div style="display:flex;justify-content:space-between;align-items:baseline;padding:16px 0;border-bottom:2px dashed #CFC6B8">'
            '<span class="inter" style="font-size:36px;%s">%s</span><span class="mono" style="font-size:34px;letter-spacing:1px;%s">%s</span></div>') % (peso, a, peso, b)

P['N51'] = """<div class="p" style="background:#F4EFE6;color:#15120E;padding:64px 72px 60px">
<div class="mono" style="font-size:21px;color:#B3261E">A conta que quase nenhum dono faz</div>
<div class="sans" style="font-size:82px;line-height:1.03;margin-top:18px">Quanto custa o paciente que perguntou o preço e sumiu?</div>
<div style="background:#FFFDF8;border-radius:18px;padding:18px 40px 26px;margin-top:36px;box-shadow:0 2px 0 #E2D9CE">
""" + L('Perguntaram o preço e sumiram', '10/semana') + L('Em um mês', '40 pacientes') + L('Ticket médio', 'R$ 300') + L('Saiu da sua agenda', 'R$ 12.000/mês', True) + """
</div>
<div class="ser" style="font-size:44px;line-height:1.22;margin-top:32px;color:#4A4036">Não é falta de lead. É o que a recepção responde depois do "quanto custa?". Na Odonto Excellence, o agendamento foi de 15% para 45% depois que a clínica mudou o atendimento com a gente.</div>
<div class="foot"><div><div class="mono" style="font-size:20px;color:#B3261E">Método A.G.E.N.D.A. · R$ 47</div><div class="inter" style="font-size:22px;color:#7A6E5E;margin-top:8px">Números da conta: exemplo ilustrativo</div></div><div class="btn" style="background:#15120E;color:#F4EFE6">Fazer a conta</div></div></div>"""


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
