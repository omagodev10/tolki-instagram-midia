"""Estáticos 4:5 no 'modelo notícia' com a tipografia do gancho de tensão (serif itálico, Inter Tight 800, mono).
Manchetes só com fatos permitidos (provas liberadas) ou com a dor como reportagem; selo 'CONTEÚDO DE MARCA' para não
parecer veículo real. Lote 2 (23/10): N7 a N9. Uso: python3 noticias2.py OUTDIR"""
import asyncio, os, sys
from playwright.async_api import async_playwright
ENGINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE = '''<!doctype html><html><head><meta charset="utf-8"><base href="file://%s/"><link rel="stylesheet" href="fonts.css"><style>
*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1350px;overflow:hidden}
.p{position:relative;width:1080px;height:1350px;padding:70px 72px;display:flex;flex-direction:column}
.mono{font-family:'JetBrains Mono';font-weight:700;letter-spacing:5px;text-transform:uppercase}
.ser{font-family:'Instrument Serif';font-style:italic}.sern{font-family:'Instrument Serif';font-style:normal}
.sans{font-family:'Inter Tight';font-weight:800;letter-spacing:-.03em}
.inter{font-family:Inter}
.rule{height:3px;margin:18px 0}
.chip{display:inline-block;padding:10px 20px;border-radius:8px}
.foot{margin-top:auto;display:flex;align-items:center;justify-content:space-between}
.btn{padding:22px 38px;border-radius:60px;font-family:'Inter Tight';font-weight:800;font-size:38px}
</style></head><body>%s</body></html>'''

N = {}
# Lote 23/10. N7: variação do N1 (mesmo jornal creme), número na frente
N['N7'] = """<div class="p" style="background:#F4EFE6;color:#15120E">
<div style="display:flex;justify-content:space-between;align-items:flex-end"><div class="sern" style="font-size:64px;letter-spacing:-1px">Gestão de Clínicas</div><div class="mono" style="font-size:18px;color:#7A6E5E">Conteúdo de marca</div></div>
<div class="rule" style="background:#15120E"></div><div class="mono" style="font-size:20px;color:#7A6E5E;display:flex;justify-content:space-between"><span>Atendimento</span><span>WhatsApp</span></div>
<div class="mono" style="font-size:22px;color:#B3261E;margin-top:60px">Caso real · atendimento com a Tolki</div>
<div class="sans" style="font-size:190px;line-height:.92;margin-top:16px;white-space:nowrap">15%<span style="color:#B3261E">→</span>45%</div>
<div class="sans" style="font-size:78px;line-height:1.03;margin-top:18px">O que mudou foi a resposta do "quanto custa?".</div>
<div class="ser" style="font-size:44px;line-height:1.2;margin-top:28px;color:#4A4036">Taxa de agendamento da Odonto Excellence depois que a clínica mudou o atendimento no WhatsApp.</div>
<div class="foot"><div class="mono" style="font-size:22px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#15120E;color:#F4EFE6">Ler o método</div></div></div>"""
# N8: N1 + ângulo vencedor "Antes de contratar" (T31), prova 21 para 62, jornal azul claro
N['N8'] = """<div class="p" style="background:#EEF3F8;color:#0B1A28">
<div style="display:flex;justify-content:space-between;align-items:flex-end"><div class="sern" style="font-size:64px;letter-spacing:-1px">Gestão de Clínicas</div><div class="mono" style="font-size:18px;color:#5B6B7A">Conteúdo de marca</div></div>
<div class="rule" style="background:#0B1A28"></div><div class="mono" style="font-size:20px;color:#5B6B7A;display:flex;justify-content:space-between"><span>Equipe</span><span>Recepção</span></div>
<div class="mono" style="font-size:22px;color:#0F8FD0;margin-top:66px">Caso real · atendimento com a Tolki</div>
<div class="sans" style="font-size:92px;line-height:1.02;margin-top:22px">Antes de contratar outra secretária, leia isto.</div>
<div class="ser" style="font-size:50px;line-height:1.22;margin-top:34px;color:#33414F">Numa clínica que mudou o atendimento com a gente, a mesma atendente foi de 21 para 62 contratos em um mês. A equipe, de 59 para 121.</div>
<div class="foot"><div class="mono" style="font-size:22px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#0B1A28;color:#EEF3F8">Ler o método</div></div></div>"""
# N9: conceito novo, data do momento (Dia do Dentista, 25/10), plantão com dor
N['N9'] = """<div class="p" style="background:#FFFFFF;color:#0B1A28;padding-top:0">
<div style="margin:0 -72px;background:#0F8FD0;color:#fff;padding:26px 72px" class="mono"><span style="font-size:30px">25 de outubro</span><span style="font-size:22px;opacity:.9;margin-left:24px">Dia do Dentista</span></div>
<div class="sans" style="font-size:96px;line-height:1.02;margin-top:70px">A cadeira vazia de segunda começa no WhatsApp de domingo.</div>
<div class="ser" style="font-size:52px;line-height:1.2;margin-top:34px;color:#3B4554">O paciente pergunta o preço, recebe só o número e some. Não é falta de lead.</div>
<div style="margin-top:46px;border-left:8px solid #0F8FD0;padding-left:28px" class="inter"><div style="font-size:36px;color:#5B6B7A;line-height:1.4">O presente que a recepção pode dar ao consultório: conduzir a conversa até o horário marcado.</div></div>
<div class="foot"><div class="mono" style="font-size:22px;color:#5B6B7A">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#0B1A28;color:#fff">Saiba mais</div></div></div>"""


async def main(out):
    os.makedirs(out, exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--allow-file-access-from-files'])
        pg = await (await b.new_context(viewport={'width': 1080, 'height': 1350})).new_page()
        for k, html in N.items():
            f = os.path.join(out, k + '.html'); open(f, 'w').write(BASE % (ENGINE, html))
            await pg.goto('file://' + f); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            await pg.screenshot(path=os.path.join(out, k + '.jpg'), type='jpeg', quality=92); print(k)
        await b.close()

asyncio.run(main(sys.argv[1]))
