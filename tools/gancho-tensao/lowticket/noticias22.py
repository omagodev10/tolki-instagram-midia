"""Estáticos do lote 22 (14/11), narrativa nova do Carlos: mensagens secretas + garantia (LP /lp4).
M1 a M4: variações da N1 (jornal creme, mesmo esqueleto). X1 a X3: conceitos novos (dossiê confidencial,
selo de garantia, print com a resposta escondida; exemplo ilustrativo). Uso: python3 noticias22.py OUTDIR"""

import asyncio, os, sys
from playwright.async_api import async_playwright
ENGINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = '''*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;overflow:hidden}
.p{position:relative;width:1080px;height:1350px;padding:70px 72px;display:flex;flex-direction:column}
.mono{font-family:'JetBrains Mono';font-weight:700;letter-spacing:5px;text-transform:uppercase}
.ser{font-family:'Instrument Serif';font-style:italic}.sern{font-family:'Instrument Serif';font-style:normal}
.sans{font-family:'Inter Tight';font-weight:800;letter-spacing:-.03em}
.inter{font-family:Inter}
.rule{height:3px;margin:18px 0;flex-shrink:0}
.foot{margin-top:auto;display:flex;align-items:center;justify-content:space-between}
.btn{white-space:nowrap;padding:22px 38px;border-radius:60px;font-family:'Inter Tight';font-weight:800;font-size:38px}
.bar{display:inline-block;height:30px;border-radius:6px;background:#15120E;vertical-align:middle}
.bb{max-width:780px;padding:22px 28px;border-radius:26px;font-family:Inter;font-size:36px;line-height:1.3;box-shadow:0 2px 0 rgba(0,0,0,.08)}'''

def page(body):
    return ('<!doctype html><html><head><meta charset="utf-8"><base href="file://%s/">'
            '<link rel="stylesheet" href="fonts.css"><style>%s</style></head><body>%s</body></html>') % (ENGINE, CSS, body)

def jornal(fundo, tinta, cinza, acento, chapeu, titulo, corpo, rodape, botao, tam=96):
    return f"""<div class="p" style="background:{fundo};color:{tinta}">
<div style="display:flex;justify-content:space-between;align-items:flex-end"><div class="sern" style="font-size:64px;letter-spacing:-1px">Gestão de Clínicas</div><div class="mono" style="font-size:18px;color:{cinza}">Conteúdo de marca</div></div>
<div class="rule" style="background:{tinta}"></div><div class="mono" style="font-size:20px;color:{cinza};display:flex;justify-content:space-between"><span>Atendimento</span><span>WhatsApp</span></div>
<div class="mono" style="font-size:22px;color:{acento};margin-top:66px">{chapeu}</div>
<div class="sans" style="font-size:{tam}px;line-height:1.02;margin-top:22px">{titulo}</div>
<div class="ser" style="font-size:48px;line-height:1.22;margin-top:34px;color:{cinza}">{corpo}</div>
<div class="foot"><div class="mono" style="font-size:22px">{rodape}</div><div class="btn" style="background:{tinta};color:{fundo}">{botao}</div></div></div>"""

CREME = ('#F4EFE6', '#15120E', '#4A4036', '#B3261E')
P = {}
P['M1'] = jornal(*CREME, 'Caso real · atendimento com a Tolki',
    'As mensagens secretas que fazem a clínica vender todo dia no WhatsApp',
    'Na Odonto Excellence, o agendamento foi de 15% para 45% depois que a clínica mudou o atendimento com a gente. Agora as mensagens cabem num kit.',
    'R$ 47 · garantia de 7 dias', 'Ver as mensagens', 90)
P['M2'] = jornal(*CREME, 'Caso real · atendimento com a Tolki',
    'Clínica triplica o agendamento com mensagens que o concorrente não conhece',
    'Na Odonto Excellence, a taxa foi de 15% para 45% depois que a clínica mudou o atendimento com a gente. As mensagens: R$ 47. Não vendeu em 7 dias, o dinheiro volta.',
    'Mensagens secretas · R$ 47', 'Quero as mensagens', 92)
P['M3'] = jornal(*CREME, 'Garantia · 7 dias',
    'R$ 47 pelas mensagens que fazem o paciente marcar. Não vendeu? Devolvemos.',
    'Copie e cole no WhatsApp da clínica hoje. Se em 7 dias a sua clínica não vender, você recebe tudo de volta. Sem pergunta difícil.',
    'Mensagens secretas · R$ 47', 'Testar sem risco', 92)
P['M4'] = jornal('#111111', '#F4EFE6', '#B9AFA2', '#E5484D', 'Revelado · atendimento no WhatsApp',
    'As 6 mensagens secretas que fazem o paciente parar de sumir',
    'Elas não parecem venda e não começam pelo preço. Terminam com o paciente escolhendo o horário. R$ 47, e se não vender em 7 dias, devolvemos.',
    'Mensagens secretas · R$ 47', 'Ver as 6', 92)

def linha(w1, w2=None):
    s = f'<span class="bar" style="width:{w1}px"></span>'
    if w2: s += f' <span class="bar" style="width:{w2}px"></span>'
    return f'<div style="margin:14px 0">{s}</div>'

P['X1'] = """<div class="p" style="background:#EDE6D6;color:#15120E;padding:64px 72px 60px">
<div style="display:flex;justify-content:space-between;align-items:center"><div class="mono" style="font-size:22px">Arquivo · Recepção</div><div class="mono" style="font-size:22px;color:#B3261E;border:4px solid #B3261E;padding:10px 18px;transform:rotate(-6deg)">Confidencial</div></div>
<div class="sans" style="font-size:84px;line-height:1.03;margin-top:46px">As mensagens que a sua recepção deveria mandar. E ninguém te contou.</div>
<div style="background:#FFFDF8;border-radius:16px;padding:30px 40px;margin-top:40px;box-shadow:0 2px 0 #D6CDBD">
<div class="mono" style="font-size:20px;color:#7A6E5E">Mensagem 1 · "quanto custa?"</div>""" + linha(420, 260) + linha(560) + """
<div class="mono" style="font-size:20px;color:#7A6E5E;margin-top:22px">Mensagem 5 · os dois horários</div>""" + linha(300, 380) + linha(480) + """</div>
<div class="ser" style="font-size:44px;line-height:1.22;margin-top:34px;color:#4A4036">O kit completo, pronto para copiar e colar, por R$ 47. Se em 7 dias não vender, devolvemos tudo.</div>
<div class="foot"><div class="mono" style="font-size:20px;color:#B3261E">Mensagens secretas · R$ 47</div><div class="btn" style="background:#15120E;color:#EDE6D6">Abrir o arquivo</div></div></div>"""

P['X2'] = """<div class="p" style="background:#0E1A14;color:#F2F5EE;align-items:center;text-align:center;padding:80px 72px 64px">
<div class="mono" style="font-size:22px;color:#7FD3A3">Mensagens secretas para clínicas</div>
<div style="width:330px;height:330px;border-radius:50%;border:8px solid #7FD3A3;margin-top:56px;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 0 0 14px #0E1A14,0 0 0 18px #2E5A44">
<div class="sans" style="font-size:100px;line-height:.9;color:#7FD3A3">100%</div><div class="mono" style="font-size:22px;margin-top:10px">do dinheiro de volta</div></div>
<div class="sans" style="font-size:86px;line-height:1.03;margin-top:60px">Vendeu? Ótimo.<br>Não vendeu? Devolvemos.</div>
<div class="ser" style="font-size:44px;line-height:1.25;margin-top:34px;color:#B8C7BC">As mensagens que fazem o paciente marcar no WhatsApp, prontas para copiar. R$ 47. Teste por 7 dias. O risco é todo nosso.</div>
<div class="foot" style="width:100%"><div class="mono" style="font-size:22px">R$ 47 · garantia de 7 dias</div><div class="btn" style="background:#7FD3A3;color:#0E1A14">Testar sem risco</div></div></div>"""

P['X3'] = """<div class="p" style="background:#E9E3DA;color:#111;padding:60px 72px 56px">
<div class="sans" style="font-size:78px;line-height:1.03">O que a clínica respondeu aqui?</div>
<div style="background:#EFE7DD;border-radius:28px;padding:30px 30px 36px;margin-top:38px;display:flex;flex-direction:column;gap:20px;background-image:radial-gradient(#E0D6C9 2px,transparent 2px);background-size:26px 26px">
<div class="bb" style="background:#fff;align-self:flex-start">Oi, quanto custa o clareamento?</div>
<div class="bb" style="background:#D9FDD3;align-self:flex-end;filter:blur(9px)">Oi, Mariana! Que bom que chamou. É para alguma data especial? Tenho uma condição que</div>
<div class="bb" style="background:#D9FDD3;align-self:flex-end;filter:blur(9px)">Consigo terça às 10h ou quinta às 15h</div>
<div class="bb" style="background:#fff;align-self:flex-start">Terça às 10h! Pode marcar 🙌</div></div>
<div class="ser" style="font-size:44px;line-height:1.22;margin-top:30px;color:#4A4036">A resposta escondida é uma das mensagens secretas do kit. R$ 47, e se em 7 dias não vender, devolvemos.</div>
<div class="foot"><div><div class="mono" style="font-size:20px;color:#B3261E">Mensagens secretas · R$ 47</div><div class="inter" style="font-size:22px;color:#7A6E5E;margin-top:8px">Conversa: exemplo ilustrativo</div></div><div class="btn" style="background:#111;color:#E9E3DA">Ver a resposta</div></div></div>"""


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
