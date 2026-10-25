"""Estáticos do lote 4 (25/10): N13 a N15 (4:5) e o carrossel C1 das 6 letras (1:1, 7 cartões).
Mesma tipografia do gancho de tensão. Só provas permitidas; "exemplo ilustrativo" onde há fala inventada.
Uso: python3 noticias4.py OUTDIR"""
import asyncio, os, sys
from playwright.async_api import async_playwright
ENGINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = '''*{margin:0;padding:0;box-sizing:border-box}body{width:%dpx;height:%dpx;overflow:hidden}
.p{position:relative;width:%dpx;height:%dpx;padding:70px 72px;display:flex;flex-direction:column}
.mono{font-family:'JetBrains Mono';font-weight:700;letter-spacing:5px;text-transform:uppercase}
.ser{font-family:'Instrument Serif';font-style:italic}.sern{font-family:'Instrument Serif';font-style:normal}
.sans{font-family:'Inter Tight';font-weight:800;letter-spacing:-.03em}
.inter{font-family:Inter}
.rule{height:3px;margin:18px 0}
.foot{margin-top:auto;display:flex;align-items:center;justify-content:space-between}
.btn{padding:22px 38px;border-radius:60px;font-family:'Inter Tight';font-weight:800;font-size:36px}
.x{color:#D93A3A;font-weight:800;font-size:46px;flex:none;width:56px}
.risc{text-decoration:line-through;text-decoration-color:#D93A3A;text-decoration-thickness:4px}'''

def page(w, h, body):
    return ('<!doctype html><html><head><meta charset="utf-8"><base href="file://%s/">'
            '<link rel="stylesheet" href="fonts.css"><style>%s</style></head><body>%s</body></html>') % (
        ENGINE, CSS % (w, h, w, h), body)

def lista(itens, cor='#1C2230', tam=44):
    return "\n".join(
        f'<div style="display:flex;align-items:flex-start;gap:14px;font-size:{tam}px;color:{cor}" class="sans">'
        f'<div class="x">✕</div><div class="risc" style="font-weight:700;letter-spacing:-.02em">{t}</div></div>' for t in itens)

P = {}  # nome -> (w, h, html)

# N13 (70%): ângulo vencedor "Antes de contratar" (T31, a venda de R$ 111 do maior cliente) no formato lista da S3
P['N13'] = (1080, 1350, """<div class="p" style="background:#FFFDF6;color:#1C2230">
<div class="mono" style="font-size:22px;color:#B3261E">Dono de clínica, leia antes de abrir a vaga</div>
<div class="sans" style="font-size:80px;line-height:1.03;margin-top:22px">Antes de contratar outra recepcionista, risque estas 4 respostas</div>
<div style="margin-top:46px;display:flex;flex-direction:column;gap:30px">%s</div>
<div class="sans" style="font-size:44px;line-height:1.2;margin-top:48px;color:#3A4352;font-weight:700">A que você já tem não precisa de reforço. Precisa de 6 letras.</div>
<div class="inter" style="font-size:28px;line-height:1.4;margin-top:22px;color:#5B6573">Numa clínica que mudou o atendimento com a gente, a mesma atendente foi de 21 para 62 contratos em um mês.</div>
<div class="foot" style="margin-top:36px"><div class="mono" style="font-size:20px;color:#8A93A0">Exemplo ilustrativo nas falas</div><div class="btn" style="background:#00AEEF;color:#fff">Método A.G.E.N.D.A. · R$ 47</div></div></div>"""
    % lista(['"R$ 900."', '"Qual horário fica melhor?"', '"Vou verificar e te retorno."', '"Ok, fico no aguardo."']))

# N14 (70%): variação direta da S3 (vendeu 24/10), gancho em pergunta e fundo escuro
P['N14'] = (1080, 1350, """<div class="p" style="background:#0E1621;color:#F4F7FA">
<div class="mono" style="font-size:22px;color:#FFD84D">Teste de 10 segundos</div>
<div class="sans" style="font-size:88px;line-height:1.02;margin-top:22px">Sua recepção respondeu assim hoje?</div>
<div style="margin-top:50px;display:flex;flex-direction:column;gap:32px">%s</div>
<div class="sans" style="font-size:48px;line-height:1.18;margin-top:52px;color:#FFD84D;font-weight:700">Uma delas já basta para o paciente sumir depois do "quanto custa?".</div>
<div class="foot"><div class="mono" style="font-size:20px;color:#8FA3B8">Exemplo ilustrativo</div><div class="btn" style="background:#00AEEF;color:#0E1621">Método A.G.E.N.D.A. · R$ 47</div></div></div>"""
    % lista(['"R$ 900, à vista."', '"Pode vir quando quiser."', '"Boa tarde!" (3 horas depois)', '"Qualquer coisa me chama."'], cor='#F4F7FA', tam=46))

# N15 (30%, conceito novo: falta / no-show, a letra A de Assegurar; Biblioteca 25/10 mostra concorrência falando de faltas)
P['N15'] = (1080, 1350, """<div class="p" style="background:#EEF3F8;color:#0B1A28">
<div style="display:flex;justify-content:space-between;align-items:flex-end"><div class="sern" style="font-size:60px;letter-spacing:-1px">Gestão de Clínicas</div><div class="mono" style="font-size:18px;color:#5B6B7A">Conteúdo de marca</div></div>
<div class="rule" style="background:#0B1A28"></div>
<div class="sans" style="font-size:96px;line-height:1.0;margin-top:44px">Marcou e não veio.</div>
<div class="ser" style="font-size:56px;line-height:1.15;margin-top:18px;color:#0F8FD0">A falta começou no WhatsApp, não no dia da consulta.</div>
<div class="inter" style="margin-top:44px;display:flex;flex-direction:column;gap:22px;font-size:38px;line-height:1.3">
<div><b>Sem lembrete na véspera.</b> O paciente esquece.</div>
<div><b>Sem confirmação no dia.</b> A cadeira fica vazia.</div>
<div><b>Sem dar duas opções.</b> Ele não remarca.</div></div>
<div class="inter" style="margin-top:36px;border-left:8px solid #0F8FD0;padding-left:26px;font-size:32px;color:#33414F;line-height:1.4">A última letra do Método A.G.E.N.D.A. é <b>Assegurar a presença</b>. Com as mensagens prontas.</div>
<div class="foot"><div class="mono" style="font-size:22px">R$ 47</div><div class="btn" style="background:#0B1A28;color:#EEF3F8">Ver as 6 letras</div></div></div>""")

# C1: carrossel das 6 letras (formato que a conta nunca testou), 1:1
LET = [('A', 'Acolher em até 5 minutos', 'Quem pergunta o preço está falando com 3 clínicas ao mesmo tempo. A primeira que acolhe leva.'),
       ('G', 'Gerar valor antes do preço', 'O número sozinho espanta. Antes dele, mostre o que o paciente ganha.'),
       ('E', 'Entender a dor', 'Duas perguntas certas valem mais que o catálogo inteiro.'),
       ('N', 'Neutralizar a objeção', '"Vou pensar" quase sempre quer dizer outra coisa. A recepção precisa saber o quê.'),
       ('D', 'Definir o horário', 'Nunca "qual horário fica melhor?". Sempre duas opções: terça 10h ou quinta 16h.'),
       ('A', 'Assegurar a presença', 'Lembrete na véspera e no dia. Paciente marcado é paciente que aparece.')]
CORES = ['#00AEEF', '#FFD84D', '#7CE0B5', '#FF8A7A', '#00AEEF', '#FFD84D']
P['C1_00'] = (1080, 1080, """<div class="p" style="background:#0E1621;color:#F4F7FA;justify-content:center">
<div class="mono" style="font-size:24px;color:#8FA3B8">Recepção de clínica · WhatsApp</div>
<div class="sans" style="font-size:96px;line-height:1.0;margin-top:26px">6 letras que fazem a recepção <span style="color:#00AEEF">agendar</span></div>
<div class="sans" style="font-size:128px;letter-spacing:.02em;margin-top:40px;color:#FFD84D">A.G.E.N.D.A.</div>
<div class="inter" style="font-size:34px;color:#8FA3B8;margin-top:36px">Arraste para o lado →</div></div>""")
for i, (l, t, d) in enumerate(LET, 1):
    P['C1_%02d' % i] = (1080, 1080, f"""<div class="p" style="background:#0E1621;color:#F4F7FA">
<div class="mono" style="font-size:24px;color:#8FA3B8">Letra {i} de 6</div>
<div class="sans" style="font-size:330px;line-height:.9;margin-top:30px;color:{CORES[i-1]}">{l}</div>
<div class="sans" style="font-size:70px;line-height:1.05;margin-top:24px">{t}</div>
<div class="inter" style="font-size:38px;line-height:1.35;margin-top:28px;color:#C9D3DE">{d}</div>
<div class="foot"><div class="mono" style="font-size:20px;color:#8FA3B8">Método A.G.E.N.D.A.</div><div class="mono" style="font-size:20px;color:#8FA3B8">{'R$ 47 · mensagens prontas' if i == 6 else 'arraste →'}</div></div></div>""")


async def main(out):
    os.makedirs(out, exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(args=['--allow-file-access-from-files'])
        for k, (w, h, html) in P.items():
            pg = await (await b.new_context(viewport={'width': w, 'height': h})).new_page()
            f = os.path.join(out, k + '.html'); open(f, 'w').write(page(w, h, html))
            await pg.goto('file://' + f); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            await pg.screenshot(path=os.path.join(out, k + '.jpg'), type='jpeg', quality=92); print(k)
            os.remove(f)
        await b.close()

asyncio.run(main(sys.argv[1]))
