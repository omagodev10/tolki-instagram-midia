"""Estáticos do lote 9 (30/10): N26 e N27 (4:5).
N26 (70%): a N1 vencedora (manchete igual) com o antes e depois da mesma resposta ao "quanto custa?" (exemplo ilustrativo). Testa prova por conversa.
N27 (30%): conceito novo da biblioteca 7.4, "segunda-feira 8h": as conversas do fim de semana esperando resposta (número ilustrativo). Biblioteca de 30/10: concorrentes com "sua recepção está aproveitando todas as oportunidades?" e "anti-vazamento de receita".
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
.rule{height:3px;margin:18px 0;flex-shrink:0}
.foot{margin-top:auto;display:flex;align-items:center;justify-content:space-between}
.btn{padding:22px 38px;border-radius:60px;font-family:'Inter Tight';font-weight:800;font-size:38px}'''

def page(body):
    return ('<!doctype html><html><head><meta charset="utf-8"><base href="file://%s/">'
            '<link rel="stylesheet" href="fonts.css"><style>%s</style></head><body>%s</body></html>') % (ENGINE, CSS, body)

CAB = '''<div style="display:flex;justify-content:space-between;align-items:flex-end"><div class="sern" style="font-size:64px;letter-spacing:-1px">Gestão de Clínicas</div><div class="mono" style="font-size:18px;color:#7A6E5E">Conteúdo de marca</div></div>
<div class="rule" style="background:#15120E"></div><div class="mono" style="font-size:20px;color:#7A6E5E;display:flex;justify-content:space-between"><span>Atendimento</span><span>WhatsApp</span></div>'''

P = {}
SIZES = {'N26': 1350, 'N27': 1350}
BUB = lambda txt, cor, lado: ('<div style="display:flex;justify-content:%s"><div class="inter" style="background:%s;border-radius:22px;padding:18px 26px;font-size:38px;line-height:1.28;color:#15120E;max-width:820px">%s</div></div>') % (lado, cor, txt)
P['N26'] = '''<div class="p" style="background:#F4EFE6;color:#15120E">''' + CAB + '''
<div class="mono" style="font-size:22px;color:#B3261E;margin-top:44px">Caso real · atendimento com a Tolki</div>
<div class="sans" style="font-size:80px;line-height:1.02;margin-top:20px">Clínica triplica a taxa de agendamento mudando só a resposta do "quanto custa?"</div>
<div style="display:flex;gap:28px;margin-top:44px">
<div style="flex:1;display:flex;flex-direction:column;gap:14px"><div class="mono" style="font-size:20px;color:#7A6E5E">Antes · 15%</div>''' + BUB('Quanto custa a avaliação?', '#FFFFFF', 'flex-start') + BUB('R$ 150.', '#E6DED1', 'flex-end') + '''</div>
<div style="flex:1.25;display:flex;flex-direction:column;gap:14px"><div class="mono" style="font-size:20px;color:#B3261E">Depois · 45%</div>''' + BUB('Quanto custa a avaliação?', '#FFFFFF', 'flex-start') + BUB('Te explico! Antes, me conta o que está te incomodando? Tenho quinta 10h ou sexta 16h.', '#DCF8C6', 'flex-end') + '''</div></div>
<div class="mono" style="font-size:18px;color:#7A6E5E;margin-top:24px;line-height:1.6">Conversas: exemplo ilustrativo · Agendamento: Odonto Excellence, de 15% para 45%</div>
<div class="foot"><div class="mono" style="font-size:22px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#15120E;color:#F4EFE6">Ler o método</div></div></div>'''
ROW = lambda h, n, t: ('<div style="display:flex;align-items:center;gap:22px;padding:24px 0;border-bottom:2px solid #22303D"><div style="width:22px;height:22px;border-radius:11px;background:#25D366"></div>'
    '<div class="inter" style="flex:1;font-size:38px;color:#E6EDF3">%s</div><div class="mono" style="font-size:20px;color:#8A97A3">%s</div>'
    '<div class="sans" style="min-width:58px;height:58px;border-radius:29px;background:#25D366;color:#06210F;font-size:30px;display:flex;align-items:center;justify-content:center">%s</div></div>') % (t, h, n)
P['N27'] = '''<div class="p" style="background:#0B141A;color:#fff">
<div class="mono" style="font-size:22px;color:#25D366;display:flex;justify-content:space-between"><span>Segunda-feira · 8h</span><span style="color:#8A97A3">Exemplo ilustrativo</span></div><div class="rule" style="background:#22303D"></div>
<div class="sans" style="font-size:100px;line-height:1.0;margin-top:44px">40 conversas do fim de semana esperando resposta.</div>
<div style="margin-top:34px">''' + ROW('sáb 10:14', '3', 'Quanto custa o clareamento?') + ROW('sáb 19:02', '1', 'Vocês atendem convênio?') + ROW('dom 21:40', '2', 'Tem horário essa semana?') + '''</div>
<div class="ser" style="font-size:48px;line-height:1.22;margin-top:46px;color:#C9D6E3">Cada uma é um paciente que perguntou e ainda não recebeu um horário. A ordem certa para responder cabe em 10 minutos de método.</div>
<div class="foot"><div class="mono" style="font-size:22px;color:#8A97A3">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#25D366;color:#06210F">Ver o método</div></div></div>'''


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
