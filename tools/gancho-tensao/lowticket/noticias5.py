"""Estáticos do lote 5 (26/10): N16 a N18 (4:5).
70%: N16 e N17 variam a N1 (jornal creme, a notícia com o clique mais barato da conta: R$ 2,69 a 4,22 e 1 venda).
30%: N18 conceito novo, feriadão de Finados (02/11): o anúncio roda, a recepção não. Pausar em 03/11.
Só provas permitidas; selo "conteúdo de marca". Uso: python3 noticias5.py OUTDIR"""
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
# N16: N1 com a prova 21 para 62 (mesmo jornal creme, manchete de pessoa)
P['N16'] = '''<div class="p" style="background:#F4EFE6;color:#15120E">''' + CAB + '''
<div class="mono" style="font-size:22px;color:#B3261E;margin-top:70px">Caso real · atendimento com a Tolki</div>
<div class="sans" style="font-size:94px;line-height:1.02;margin-top:22px">Mesma atendente, mesmo WhatsApp: de 21 para 62 contratos em um mês</div>
<div class="ser" style="font-size:48px;line-height:1.22;margin-top:34px;color:#4A4036">A clínica mudou o jeito de responder o "quanto custa?" no WhatsApp. A equipe inteira foi de 59 para 121 no mesmo período.</div>
<div class="foot"><div class="mono" style="font-size:22px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#15120E;color:#F4EFE6">Ler o método</div></div></div>'''
# N17: N1 com manchete em pergunta (mesma prova Odonto Excellence)
P['N17'] = '''<div class="p" style="background:#F4EFE6;color:#15120E">''' + CAB + '''
<div class="mono" style="font-size:22px;color:#B3261E;margin-top:70px">Caso real · atendimento com a Tolki</div>
<div class="sans" style="font-size:90px;line-height:1.03;margin-top:22px">O que uma clínica mudou no WhatsApp para triplicar a taxa de agendamento?</div>
<div class="ser" style="font-size:48px;line-height:1.22;margin-top:34px;color:#4A4036">Na Odonto Excellence, o agendamento foi de 15% para 45% depois que a clínica mudou o atendimento no WhatsApp.</div>
<div class="foot"><div class="mono" style="font-size:22px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#15120E;color:#F4EFE6">Ler o método</div></div></div>'''
# N18: feriadão (data do momento com gancho de dor), plantão
P['N18'] = '''<div class="p" style="background:#FFFFFF;color:#0B1A28;padding-top:0">
<div style="margin:0 -72px;background:#D7261E;color:#fff;padding:26px 72px" class="mono"><span style="font-size:30px">● Feriadão</span><span style="font-size:22px;opacity:.85;margin-left:24px">na sua clínica</span></div>
<div class="sans" style="font-size:100px;line-height:1.02;margin-top:70px">O anúncio da sua clínica não tira folga. A recepção tira.</div>
<div class="ser" style="font-size:52px;line-height:1.2;margin-top:34px;color:#3B4554">Quem pergunta "quanto custa?" no sábado e só ouve resposta na terça já marcou com outra clínica.</div>
<div style="margin-top:46px;border-left:8px solid #D7261E;padding-left:28px" class="inter"><div style="font-size:36px;color:#5B6B7A;line-height:1.4">Acolher em até 5 minutos é a primeira letra do Método A.G.E.N.D.A. Ele vem com as mensagens prontas.</div></div>
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
