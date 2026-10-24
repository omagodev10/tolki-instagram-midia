"""Estáticos 4:5 no 'modelo notícia' com a tipografia do gancho de tensão (serif itálico, Inter Tight 800, mono).
Manchetes só com fatos permitidos (provas liberadas) ou com a dor como reportagem; selo 'CONTEÚDO DE MARCA' para não
parecer veículo real. Lote 3 (24/10): N10 a N12. Uso: python3 noticias3.py OUTDIR"""
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
# Lote 24/10. N10: variação da S3 (lista vendeu 24/10) em "troque isto por isto", exemplo ilustrativo
N['N10'] = """<div class="p" style="background:#FFFDF6;color:#1C2230">
<div class="mono" style="font-size:22px;color:#B3261E">Recepção de clínica · WhatsApp</div>
<div class="sans" style="font-size:86px;line-height:1.02;margin-top:22px">3 trocas que fazem o paciente marcar em vez de sumir</div>
<div style="margin-top:44px;display:flex;flex-direction:column;gap:26px" class="inter">
%s
</div>
<div class="mono" style="font-size:18px;color:#8A93A0;margin-top:22px;text-align:right">Exemplo ilustrativo</div>
<div class="foot"><div class="mono" style="font-size:22px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#1C2230;color:#FFFDF6">Ver as respostas</div></div></div>""" % "\n".join(
 f'<div style="display:flex;flex-direction:column;gap:10px"><div style="font-size:36px;color:#B3261E;text-decoration:line-through;text-decoration-thickness:3px">✕ {a}</div><div style="font-size:38px;font-weight:700;color:#127A47">✓ {b}</div></div>'
 for a,b in [('"R$ 900."','"Depende do caso. Posso te fazer 2 perguntas rápidas?"'),('"Qual horário fica melhor pra você?"','"Tenho terça 10h ou quinta 16h. Qual prefere?"'),('"Vou verificar e te retorno."','"Já confiro e te respondo em 5 minutos."')])
# N11: variação da S3 em checklist (autoavaliação), jornal escuro
N['N11'] = """<div class="p" style="background:#0E1621;color:#F4F7FA">
<div style="display:flex;justify-content:space-between;align-items:flex-end"><div class="sern" style="font-size:60px">Teste da recepção</div><div class="mono" style="font-size:18px;color:#8FA3B8">Conteúdo de marca</div></div>
<div class="rule" style="background:#F4F7FA"></div>
<div class="sans" style="font-size:80px;line-height:1.04;margin-top:40px">A sua recepção já disse isso hoje?</div>
<div style="margin-top:44px;display:flex;flex-direction:column;gap:30px" class="inter">
%s
</div>
<div class="ser" style="font-size:48px;line-height:1.2;margin-top:46px;color:#FFD84D">Marcou 2? Você está pagando anúncio para o paciente ir embora.</div>
<div class="foot"><div class="mono" style="font-size:22px;color:#8FA3B8">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#00AEEF;color:#0E1621">Fazer o teste</div></div></div>""" % "\n".join(
 f'<div style="display:flex;align-items:center;gap:26px;font-size:42px"><div style="width:52px;height:52px;border:4px solid #8FA3B8;border-radius:10px;flex:none"></div><div>{t}</div></div>'
 for t in ['Só o preço, sem pergunta antes','"Qual horário fica melhor?"','"Vou pensar" e ficou por isso','Respondeu depois de 1 hora'])
# N12: conceito novo (concorrência na Biblioteca vende robô de IA): rapidez sem condução não agenda
N['N12'] = """<div class="p" style="background:#EEF3F8;color:#0B1A28">
<div style="display:flex;justify-content:space-between;align-items:flex-end"><div class="sern" style="font-size:64px;letter-spacing:-1px">Gestão de Clínicas</div><div class="mono" style="font-size:18px;color:#5B6B7A">Conteúdo de marca</div></div>
<div class="rule" style="background:#0B1A28"></div><div class="mono" style="font-size:20px;color:#5B6B7A;display:flex;justify-content:space-between"><span>Atendimento</span><span>Análise</span></div>
<div class="sans" style="font-size:96px;line-height:1.0;margin-top:60px">Vai colocar um robô no WhatsApp da clínica?</div>
<div class="ser" style="font-size:50px;line-height:1.22;margin-top:34px;color:#33414F">Rápido ou devagar, gente ou robô: se a resposta do "quanto custa?" é só o número, o paciente some. O que agenda é a ordem da conversa.</div>
<div style="margin-top:40px;border-left:8px solid #0F8FD0;padding-left:28px;font-size:36px;color:#5B6B7A;line-height:1.4" class="inter">Mais de 470 clínicas usam a Tolki para conduzir a conversa até o horário marcado.</div>
<div class="foot"><div class="mono" style="font-size:22px">Método A.G.E.N.D.A. · R$ 47</div><div class="btn" style="background:#0B1A28;color:#EEF3F8">Ler o método</div></div></div>"""


async def main(out):
    os.makedirs(out, exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(args=['--allow-file-access-from-files'])
        pg = await (await b.new_context(viewport={'width': 1080, 'height': 1350})).new_page()
        for k, html in N.items():
            f = os.path.join(out, k + '.html'); open(f, 'w').write(BASE % (ENGINE, html))
            await pg.goto('file://' + f); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            await pg.screenshot(path=os.path.join(out, k + '.jpg'), type='jpeg', quality=92); print(k)
        await b.close()

asyncio.run(main(sys.argv[1]))
