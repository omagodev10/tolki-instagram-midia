"""Estáticos do lote 10 (31/10): N28 e N29 (4:5).
N28 (70%): a N1 vencedora idêntica com chamada de público no topo ("clínica com 2 ou 3 atendentes"): os compradores que responderam a Luana em 7 dias são 3 de 4 com 2 a 3 atendentes. Testa só a chamada.
N29 (30%): formato novo (quiz) com conceito novo da biblioteca 7.4, "me passa o valor por aqui?": 3 respostas, qual agenda. Biblioteca de 31/10: concorrentes vendem "IA que responde 24h" e "secretária comercial"; aqui a resposta é da recepção que já existe.
Só provas permitidas; selo "conteúdo de marca". Uso: python3 noticias10.py OUTDIR"""

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
SIZES = {'N28': 1350, 'N29': 1350}
P['N28'] = """<div class="p" style="background:#F4EFE6;color:#15120E">""" + CAB + """
<div style="margin-top:44px;align-self:flex-start;background:#15120E;color:#F4EFE6;padding:14px 24px" class="mono"><span style="font-size:24px">Clínica com 2 ou 3 atendentes? Leia isto</span></div>
<div class="mono" style="font-size:22px;color:#B3261E;margin-top:34px">Caso real · atendimento com a Tolki</div>
<div class="sans" style="font-size:92px;line-height:1.02;margin-top:22px">Clínica triplica a taxa de agendamento mudando só a resposta do "quanto custa?"</div>
<div class="ser" style="font-size:48px;line-height:1.2;margin-top:30px;color:#4A4036">Na Odonto Excellence, o agendamento foi de 15% para 45% depois que a clínica mudou o atendimento no WhatsApp. Sem contratar ninguém.</div>
<div class="foot"><div class="mono" style="font-size:22px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#15120E;color:#F4EFE6">Ler o método</div></div></div>"""
OPT = lambda l, t, cor: ('<div style="display:flex;gap:22px;align-items:flex-start;background:%s;border-radius:22px;padding:22px 26px;margin-top:18px">'
    '<div class="sans" style="min-width:64px;height:64px;border-radius:32px;background:#122C48;color:#fff;font-size:34px;display:flex;align-items:center;justify-content:center">%s</div>'
    '<div class="inter" style="font-size:36px;line-height:1.3;color:#15120E">%s</div></div>') % (cor, l, t)
P['N29'] = """<div class="p" style="background:#EAF6FD;color:#122C48">
<div class="mono" style="font-size:22px;color:#00AEEF;display:flex;justify-content:space-between"><span>Teste de 10 segundos</span><span style="color:#5B7287">Exemplo ilustrativo</span></div><div class="rule" style="background:#122C48"></div>
<div class="sans" style="font-size:66px;line-height:1.05;margin-top:26px">O paciente escreveu:</div>
<div style="display:flex;margin-top:18px"><div class="inter" style="background:#FFFFFF;border-radius:24px;padding:22px 30px;font-size:46px;font-weight:600;color:#15120E;box-shadow:0 4px 0 #CFE3EF">"Me passa o valor por aqui?"</div></div>
<div class="sans" style="font-size:52px;line-height:1.1;margin-top:34px">Qual resposta marca a avaliação?</div>
""" + OPT('A', 'A avaliação é R$ 150.', '#FFFFFF') + OPT('B', 'Passo sim! Só me diz: o que te fez procurar a clínica?', '#FFFFFF') + OPT('C', 'Valores só presencialmente.', '#FFFFFF') + """
<div class="ser" style="font-size:40px;line-height:1.25;margin-top:30px;color:#2E4A66">Se a sua recepção responde A ou C, o paciente pergunta na próxima clínica. A resposta B e as que vêm depois estão no método.</div>
<div class="foot"><div class="mono" style="font-size:22px;color:#5B7287">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#00AEEF;color:#05202F">Ver as respostas</div></div></div>"""


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
