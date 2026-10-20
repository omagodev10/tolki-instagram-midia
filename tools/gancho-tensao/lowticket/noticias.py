"""Estáticos 4:5 no 'modelo notícia' com a tipografia do gancho de tensão (serif itálico, Inter Tight 800, mono).
Manchetes só com fatos permitidos (provas liberadas) ou com a dor como reportagem; selo 'CONTEÚDO DE MARCA' para não
parecer veículo real. Uso: python3 noticias.py OUTDIR  -> N1.jpg ... N6.jpg"""
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
# N1: jornal clássico (papel creme, serif), prova Odonto Excellence
N['N1'] = '''<div class="p" style="background:#F4EFE6;color:#15120E">
<div style="display:flex;justify-content:space-between;align-items:flex-end"><div class="sern" style="font-size:64px;letter-spacing:-1px">Gestão de Clínicas</div><div class="mono" style="font-size:18px;color:#7A6E5E">Conteúdo de marca</div></div>
<div class="rule" style="background:#15120E"></div><div class="mono" style="font-size:20px;color:#7A6E5E;display:flex;justify-content:space-between"><span>Atendimento</span><span>WhatsApp</span></div>
<div class="mono" style="font-size:22px;color:#B3261E;margin-top:70px">Caso real · atendimento com a Tolki</div>
<div class="sans" style="font-size:96px;line-height:1.02;margin-top:22px">Clínica triplica a taxa de agendamento mudando só a resposta do "quanto custa?"</div>
<div class="ser" style="font-size:50px;line-height:1.2;margin-top:34px;color:#4A4036">Na Odonto Excellence, o agendamento foi de 15% para 45% depois que a clínica mudou o atendimento no WhatsApp.</div>
<div class="foot"><div class="mono" style="font-size:22px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#15120E;color:#F4EFE6">Ler o método</div></div></div>'''
# N2: editorial escuro (paleta do gancho), 21 para 62
N['N2'] = '''<div class="p" style="background:#050B12;color:#fff">
<div class="mono" style="font-size:22px;color:#1AA6E3">Resultado real · cliente Tolki</div><div class="rule" style="background:#1C3347"></div>
<div class="ser" style="font-size:66px;margin-top:60px;color:#C9D6E3">uma atendente,</div>
<div class="sans" style="font-size:300px;line-height:.95;margin-top:10px">21<span style="color:#1AA6E3">→</span>62</div>
<div class="sans" style="font-size:78px;text-transform:uppercase;margin-top:10px">contratos em um mês.</div>
<div class="inter" style="font-size:38px;line-height:1.35;margin-top:40px;color:#8A97A3">Numa clínica que mudou o atendimento no WhatsApp com a Tolki. O método reúne o que funcionou nessas conversas.</div>
<div class="foot"><div class="mono" style="font-size:22px;color:#8A97A3">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#1AA6E3;color:#050B12">Saiba mais</div></div></div>'''
# N3: urgente / plantão (faixa vermelha), dor
N['N3'] = '''<div class="p" style="background:#FFFFFF;color:#0B1A28;padding-top:0">
<div style="margin:0 -72px;background:#D7261E;color:#fff;padding:26px 72px" class="mono"><span style="font-size:30px">● Agora</span><span style="font-size:22px;opacity:.85;margin-left:24px">na sua clínica</span></div>
<div class="sans" style="font-size:104px;line-height:1.02;margin-top:70px">Paciente pergunta o preço, recebe só o número e some.</div>
<div class="ser" style="font-size:54px;line-height:1.2;margin-top:34px;color:#3B4554">Acontece todo dia, no "quanto custa?". E a culpa vai para o lead.</div>
<div style="margin-top:46px;border-left:8px solid #D7261E;padding-left:28px" class="inter"><div style="font-size:36px;color:#5B6B7A;line-height:1.4">O que muda: perguntar antes, dar o valor com o motivo e oferecer dois horários.</div></div>
<div class="foot"><div class="mono" style="font-size:22px;color:#5B6B7A">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#0B1A28;color:#fff">Saiba mais</div></div></div>'''
# N4: ciano chapado, manchete grande + 470
N['N4'] = '''<div class="p" style="background:#1AA6E3;color:#06233A">
<div class="mono" style="font-size:22px;color:#fff">Clínicas que atendem com a Tolki</div><div class="rule" style="background:#06233A;opacity:.3"></div>
<div class="sans" style="font-size:330px;line-height:.9;margin-top:50px;color:#fff">+470</div>
<div class="sans" style="font-size:86px;line-height:1.02;margin-top:20px;text-transform:uppercase">clínicas já atendem com a Tolki.</div>
<div class="ser" style="font-size:54px;line-height:1.2;margin-top:30px">O que funciona nessas conversas virou um método de 10 minutos para a sua recepção.</div>
<div class="foot"><div class="mono" style="font-size:22px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#06233A;color:#fff">Saiba mais</div></div></div>'''
# N5: revista âmbar, entrevista/pergunta
N['N5'] = '''<div class="p" style="background:#0C0906;color:#FFF7EC">
<div style="display:flex;justify-content:space-between"><div class="mono" style="font-size:22px;color:#F5A524">Pergunta da semana</div><div class="mono" style="font-size:18px;color:#A8977F">Conteúdo de marca</div></div><div class="rule" style="background:#3A2C1B"></div>
<div class="ser" style="font-size:150px;line-height:1;margin-top:80px;color:#F5A524">"Vou pensar."</div>
<div class="sans" style="font-size:84px;line-height:1.04;margin-top:40px;text-transform:uppercase">Por que o paciente diz isso e nunca mais volta?</div>
<div class="inter" style="font-size:38px;line-height:1.4;margin-top:36px;color:#A8977F">Porque recebeu o preço antes do motivo. A resposta certa está na letra G do método: gerar valor antes do preço.</div>
<div class="foot"><div class="mono" style="font-size:22px;color:#A8977F">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#F5A524;color:#0C0906">Saiba mais</div></div></div>'''
# N6: portal com "lista" (análise) e data Dia do Dentista
N['N6'] = '''<div class="p" style="background:#F6F8FA;color:#0B1A28">
<div class="mono" style="font-size:22px;color:#0F8FD0">Análise · atendimento no WhatsApp</div><div class="rule" style="background:#D5DEE8"></div>
<div class="sans" style="font-size:88px;line-height:1.03;margin-top:50px">As 3 respostas que mais fazem a clínica perder paciente</div>
<div class="inter" style="margin-top:46px;display:flex;flex-direction:column;gap:26px">
<div style="display:flex;gap:26px;align-items:baseline"><span class="sans" style="font-size:64px;color:#0F8FD0">1</span><span style="font-size:44px">"R$ 900." <span style="color:#5B6B7A">(e mais nada)</span></span></div>
<div style="display:flex;gap:26px;align-items:baseline"><span class="sans" style="font-size:64px;color:#0F8FD0">2</span><span style="font-size:44px">"Qual horário fica melhor?"</span></div>
<div style="display:flex;gap:26px;align-items:baseline"><span class="sans" style="font-size:64px;color:#0F8FD0">3</span><span style="font-size:44px">"Boa tarde!" <span style="color:#5B6B7A">3 horas depois</span></span></div></div>
<div class="foot"><div class="mono" style="font-size:22px;color:#5B6B7A">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#0F8FD0;color:#fff">Saiba mais</div></div></div>'''


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
