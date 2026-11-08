"""Estáticos do lote 19 (08/11): N46 (variação da N8, "contratou mais uma secretária e a agenda continuou vazia?", jornal azul) e N47 (segunda 8h, conversas do fim de semana acumuladas; conceito novo da 7.4). Uso: python3 noticias19.py OUTDIR"""

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
SIZES = {'N46': 1350, 'N47': 1350}

P['N46'] = """<div class="p" style="background:#EEF3F8;color:#0B1A28">
<div style="display:flex;justify-content:space-between;align-items:flex-end"><div class="sern" style="font-size:64px;letter-spacing:-1px">Gestão de Clínicas</div><div class="mono" style="font-size:18px;color:#5B6B7A">Conteúdo de marca</div></div>
<div class="rule" style="background:#0B1A28"></div><div class="mono" style="font-size:20px;color:#5B6B7A;display:flex;justify-content:space-between"><span>Equipe</span><span>Recepção</span></div>
<div class="mono" style="font-size:22px;color:#0F8FD0;margin-top:66px">Caso real · atendimento com a Tolki</div>
<div class="sans" style="font-size:92px;line-height:1.02;margin-top:22px">Contratou mais uma secretária e a agenda continuou vazia?</div>
<div class="ser" style="font-size:48px;line-height:1.22;margin-top:34px;color:#33414F">O problema não era gente. Era a resposta. Numa clínica que mudou o atendimento com a gente, a mesma atendente foi de 21 para 62 contratos em um mês.</div>
<div class="foot"><div class="mono" style="font-size:22px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#0B1A28;color:#EEF3F8">Ler o método</div></div></div>"""

NOT = lambda hora, nome, t: ('<div style="background:rgba(255,255,255,.10);border-radius:22px;padding:18px 24px;margin-top:14px;display:flex;gap:18px;align-items:center">'
  '<div style="width:58px;height:58px;border-radius:50%%;background:#25D366;flex-shrink:0"></div>'
  '<div style="flex:1;min-width:0"><div style="display:flex;justify-content:space-between"><span class="inter" style="font-weight:700;font-size:30px">%s</span><span class="mono" style="font-size:18px;letter-spacing:2px;color:#9FB3C2">%s</span></div>'
  '<div class="inter" style="font-size:30px;color:#D6E0E8;margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">%s</div></div></div>') % (nome, hora, t)
P['N47'] = """<div class="p" style="background:#0B1A28;color:#fff;padding:60px 66px 56px">
<div class="mono" style="font-size:21px;color:#FFD400">Segunda-feira, 8h</div>
<div class="sans" style="font-size:86px;line-height:1.02;margin-top:18px">40 conversas do fim de semana esperando resposta.</div>
""" + NOT('sáb 15:02', 'Paciente', 'Oi! Quanto custa a avaliação?') + NOT('sáb 19:40', 'Paciente', 'Vocês atendem sábado?') + NOT('dom 10:15', 'Paciente', 'Queria marcar essa semana, tem horário?') + NOT('dom 21:33', 'Paciente', 'Ainda estão atendendo?') + """
<div class="inter" style="font-size:33px;line-height:1.3;margin-top:30px;color:#D6E0E8">Quem responde primeiro e conduz até o horário, marca. Numa clínica que mudou o atendimento com a gente, o agendamento foi de 15% para 45%.</div>
<div class="foot" style="margin-top:auto"><div><div class="mono" style="font-size:20px;color:#FFD400">Método A.G.E.N.D.A. · R$ 47</div><div class="inter" style="font-size:22px;color:#9FB3C2;margin-top:8px">Conversas: exemplo ilustrativo</div></div><div class="btn" style="background:#FFD400;color:#15120E">Ver o método</div></div></div>"""


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
