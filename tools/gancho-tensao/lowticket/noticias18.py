"""Estáticos do lote 18 (07/11): N44 (variação da N8, que vendeu para clínica de R$ 50 a 100 mil em 07/11: novo gancho, mesmo corpo) e N45 (equipe sem padrão: mesma pergunta, três respostas; conceito novo da 7.4, clínica com equipe). Uso: python3 noticias18.py OUTDIR"""

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
SIZES = {'N44': 1350, 'N45': 1350}

P['N44'] = """<div class="p" style="background:#EEF3F8;color:#0B1A28">
<div style="display:flex;justify-content:space-between;align-items:flex-end"><div class="sern" style="font-size:64px;letter-spacing:-1px">Gestão de Clínicas</div><div class="mono" style="font-size:18px;color:#5B6B7A">Conteúdo de marca</div></div>
<div class="rule" style="background:#0B1A28"></div><div class="mono" style="font-size:20px;color:#5B6B7A;display:flex;justify-content:space-between"><span>Equipe</span><span>Recepção</span></div>
<div class="mono" style="font-size:22px;color:#0F8FD0;margin-top:66px">Caso real · atendimento com a Tolki</div>
<div class="sans" style="font-size:90px;line-height:1.02;margin-top:22px">Sua recepção não precisa de mais gente. Precisa de outra resposta.</div>
<div class="ser" style="font-size:48px;line-height:1.22;margin-top:34px;color:#33414F">Numa clínica que mudou o atendimento com a gente, a mesma atendente foi de 21 para 62 contratos em um mês. A equipe, de 59 para 121.</div>
<div class="foot"><div class="mono" style="font-size:22px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#0B1A28;color:#EEF3F8">Ler o método</div></div></div>"""

PAC = lambda t: '<div class="inter" style="align-self:flex-start;background:#fff;color:#111;font-size:34px;line-height:1.2;padding:15px 23px;border-radius:20px 20px 20px 4px;max-width:88%%">%s</div>' % t
REC = lambda quem, t, cor, nota, ncor: ('<div style="display:flex;flex-direction:column;align-items:flex-end;margin-top:20px">'
  '<div class="mono" style="font-size:18px;color:#9FB3C2;margin-bottom:6px">%s</div>'
  '<div class="inter" style="background:%s;color:#111;font-size:34px;line-height:1.2;padding:15px 23px;border-radius:20px 20px 4px 20px;max-width:88%%">%s</div>'
  '<div class="sans" style="font-size:30px;margin-top:8px;color:%s">%s</div></div>') % (quem, cor, t, ncor, nota)
P['N45'] = """<div class="p" style="background:#0B1A28;color:#fff;padding:60px 66px 56px">
<div class="mono" style="font-size:21px;color:#FFD400">Clínica com 3 recepcionistas</div>
<div class="sans" style="font-size:84px;line-height:1.02;margin-top:18px">Mesma pergunta.<br>Três respostas.</div>
<div style="background:#EFE7DD;border-radius:24px;padding:24px 28px 26px;margin-top:30px;display:flex;flex-direction:column">
""" + PAC('Quanto custa a avaliação?') + REC('Recepcionista 1', 'R$ 200.', '#E9EDEF', 'Sumiu.', '#B3261E') + REC('Recepcionista 2', 'Depende, passa aqui pra ver.', '#E9EDEF', 'Sumiu.', '#B3261E') + REC('Recepcionista 3', 'Te explico! O que te incomoda hoje? Tenho quarta 9h ou quinta 17h.', '#D9FDD3', 'Marcou.', '#0E7A3E') + """</div>
<div class="inter" style="font-size:31px;line-height:1.3;margin-top:28px;color:#D6E0E8">Numa clínica que mudou o atendimento com a gente, a equipe foi de 59 para 121 contratos em um mês.</div>
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
