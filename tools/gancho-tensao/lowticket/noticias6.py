"""Estáticos do lote 6 (27/10): N19 a N21 (4:5).
70%: N19 e N20 variam a N1 vencedora (R$ 121 nas 3 cópias, 4 vendas, R$ 279, CPC R$ 2,27 a 2,67): mesmo corpo, gancho novo (N19) e mesma manchete em jornal escuro (N20).
30%: N21 conceito novo na conta, "cliente oculto na sua própria clínica" (teste que o dono faz hoje).
Só provas permitidas; selo "conteúdo de marca". Uso: python3 noticias6.py OUTDIR"""
import asyncio, os, sys
from playwright.async_api import async_playwright
ENGINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = '''*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1350px;overflow:hidden}
.p{position:relative;width:1080px;height:1350px;padding:70px 72px;display:flex;flex-direction:column}
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
CORPO = 'Na Odonto Excellence, o agendamento foi de 15% para 45% depois que a clínica mudou o atendimento no WhatsApp.'
# N19: N1 com gancho de número na frente (mesmo jornal creme e mesmo corpo)
P['N19'] = '''<div class="p" style="background:#F4EFE6;color:#15120E">''' + CAB + '''
<div class="mono" style="font-size:22px;color:#B3261E;margin-top:70px">Caso real · atendimento com a Tolki</div>
<div class="sans" style="font-size:92px;line-height:1.02;margin-top:22px">A resposta do "quanto custa?" que triplicou o agendamento de uma clínica</div>
<div class="ser" style="font-size:50px;line-height:1.2;margin-top:34px;color:#4A4036">''' + CORPO + '''</div>
<div class="foot"><div class="mono" style="font-size:22px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#15120E;color:#F4EFE6">Ler o método</div></div></div>'''
# N20: a manchete exata da N1 em jornal escuro (testa só a cor)
CABD = CAB.replace('#15120E', '#F4EFE6').replace('#7A6E5E', '#9AA6B2')
P['N20'] = '''<div class="p" style="background:#0E1B2A;color:#F4EFE6">''' + CABD + '''
<div class="mono" style="font-size:22px;color:#F5A524;margin-top:70px">Caso real · atendimento com a Tolki</div>
<div class="sans" style="font-size:96px;line-height:1.02;margin-top:22px">Clínica triplica a taxa de agendamento mudando só a resposta do "quanto custa?"</div>
<div class="ser" style="font-size:50px;line-height:1.2;margin-top:34px;color:#C9D3DD">''' + CORPO + '''</div>
<div class="foot"><div class="mono" style="font-size:22px;color:#C9D3DD">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#F5A524;color:#0E1B2A">Ler o método</div></div></div>'''
# N21: cliente oculto (conceito novo), checklist do teste
P['N21'] = '''<div class="p" style="background:#FFFFFF;color:#0B1A28">
<div class="mono" style="font-size:22px;color:#0F8FD0">Teste de 2 minutos · faça hoje</div><div class="rule" style="background:#D5DEE8"></div>
<div class="sans" style="font-size:92px;line-height:1.02;margin-top:44px">Mande "quanto custa?" para o WhatsApp da sua clínica. De outro número.</div>
<div class="inter" style="margin-top:44px;display:flex;flex-direction:column;gap:24px;font-size:42px">
<div style="display:flex;gap:22px"><span style="color:#0F8FD0">☐</span><span>Responderam em até 5 minutos?</span></div>
<div style="display:flex;gap:22px"><span style="color:#0F8FD0">☐</span><span>Perguntaram algo antes do preço?</span></div>
<div style="display:flex;gap:22px"><span style="color:#0F8FD0">☐</span><span>Ofereceram dois horários?</span></div></div>
<div class="ser" style="font-size:44px;line-height:1.25;margin-top:40px;color:#3B4554">Se faltou um, é ali que o paciente vai embora.</div>
<div class="foot"><div class="mono" style="font-size:22px;color:#5B6B7A">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#0B1A28;color:#fff">Saiba mais</div></div></div>'''


async def main(out):
    os.makedirs(out, exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(args=['--allow-file-access-from-files'])
        for k, html in P.items():
            pg = await (await b.new_context(viewport={'width': 1080, 'height': 1350})).new_page()
            f = os.path.join(ENGINE, '_tmp_' + k + '.html'); open(f, 'w').write(page(html))
            await pg.goto('file://' + f); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            await pg.screenshot(path=os.path.join(out, k + '.jpg'), type='jpeg', quality=92); print(k)
            os.remove(f)
        await b.close()

asyncio.run(main(sys.argv[1]))
