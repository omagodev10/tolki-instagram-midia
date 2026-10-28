"""Estáticos do lote 7 (28/10): N22 e N23.
N22 (70%): a N1 vencedora (5 vendas, R$ 353, R$ 311 gastos) idêntica em 9:16 para Stories e Reels (testa só o formato).
N23 (30%): conceito novo, a demora (perguntou às 9h, responderam ao meio-dia), no jornal creme da N1, exemplo ilustrativo.
Cabeçalho do lote 6 (27/10): N19 a N21 (4:5).
70%: N19 e N20 variam a N1 vencedora (R$ 121 nas 3 cópias, 4 vendas, R$ 279, CPC R$ 2,27 a 2,67): mesmo corpo, gancho novo (N19) e mesma manchete em jornal escuro (N20).
30%: N21 conceito novo na conta, "cliente oculto na sua própria clínica" (teste que o dono faz hoje).
Só provas permitidas; selo "conteúdo de marca". Uso: python3 noticias6.py OUTDIR"""
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
SIZES = {'N22': 1920, 'N23': 1350}
CORPO = 'Na Odonto Excellence, o agendamento foi de 15% para 45% depois que a clínica mudou o atendimento no WhatsApp.'
# N22: N1 idêntica em 9:16, conteúdo dentro da área segura (y 270 a 1540)
P['N22'] = '''<div class="p v" style="background:#F4EFE6;color:#15120E">''' + CAB + '''
<div class="mono" style="font-size:24px;color:#B3261E;margin-top:90px">Caso real · atendimento com a Tolki</div>
<div class="sans" style="font-size:100px;line-height:1.02;margin-top:26px">Clínica triplica a taxa de agendamento mudando só a resposta do "quanto custa?"</div>
<div class="ser" style="font-size:54px;line-height:1.2;margin-top:40px;color:#4A4036">''' + CORPO + '''</div>
<div class="foot"><div class="mono" style="font-size:24px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#15120E;color:#F4EFE6">Ler o método</div></div></div>'''
# N23: a demora (letra A, acolher em até 5 minutos), jornal creme, exemplo ilustrativo
P['N23'] = '''<div class="p" style="background:#F4EFE6;color:#15120E">''' + CAB + '''
<div class="mono" style="font-size:22px;color:#B3261E;margin-top:60px">Exemplo ilustrativo · acontece todo dia</div>
<div class="sans" style="font-size:86px;line-height:1.02;margin-top:22px">Perguntou o preço às 9h. A clínica respondeu ao meio-dia. Ele já tinha marcado em outra.</div>
<div class="ser" style="font-size:44px;line-height:1.22;margin-top:30px;color:#4A4036">Quem responde primeiro, agenda. Na Odonto Excellence, o agendamento foi de 15% para 45% depois que a clínica mudou o atendimento no WhatsApp.</div>
<div class="foot"><div class="mono" style="font-size:22px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#15120E;color:#F4EFE6">Ler o método</div></div></div>'''


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
