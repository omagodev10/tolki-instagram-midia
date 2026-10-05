import os
W = os.getcwd()  # rode na pasta de trabalho; grava covers/*.html (render: templates/render.js covers covers_out 1920)
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
CF = REPO + '/templates/fonts'
ICON = 'file://' + REPO + '/templates/assets/icone.png'
FONTS = f"""<style>@font-face{{font-family:Serif;font-style:italic;src:url('file://{CF}/InstrumentSerif-Italic.ttf')}}@font-face{{font-family:Mono;src:url('file://{CF}/DMMono-Regular.ttf')}}</style>"""
def cover(bg, fg, acc, kicker, title, serif, num):
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}</head><body><div style="width:1080px;height:1920px;background:{bg};position:relative;overflow:hidden;font-family:Inter">
<div style="position:absolute;left:90px;right:90px;top:330px;display:flex;justify-content:space-between;align-items:center;font-family:Mono;font-size:26px;letter-spacing:3px;color:{fg};opacity:.85">
<span style="display:flex;align-items:center;gap:14px"><span style="width:56px;height:56px;border-radius:50%;background:#8A3FD1;display:flex;align-items:center;justify-content:center"><img src="{ICON}" style="width:40px"></span>TOLKI</span><span>REEL Nº {num}</span></div>
<div style="position:absolute;left:90px;right:90px;top:620px">
<div style="font-family:Mono;font-size:30px;letter-spacing:3px;text-transform:uppercase;color:{acc};margin-bottom:30px">{kicker}</div>
<div style="font-family:Montserrat;font-weight:900;font-size:120px;line-height:.95;letter-spacing:-3px;text-transform:uppercase;color:{fg}">{title}</div>
<div style="font-family:Serif;font-style:italic;font-size:132px;line-height:1;color:{acc};margin-top:16px">{serif}</div></div>
<div style="position:absolute;left:90px;top:1500px;display:flex;align-items:center;gap:18px;font-family:Mono;font-size:26px;letter-spacing:3px;color:{fg};opacity:.8"><svg width="40" height="40" viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="none" stroke="{fg}" stroke-width="1.6"/><path d="M10 8l6 4-6 4z" fill="{fg}"/></svg>ASSISTA ATÉ O FIM</div>
</div></body></html>"""
C = {
 '01': cover('#1597D4', '#FFFFFF', '#0A1322', 'Pós eleição', 'Quem faz a apuração', 'dos seus pacientes?', '01'),
 '02': cover('#1597D4', '#FFFFFF', '#0A1322', 'Velocidade', 'Responder rápido', 'não é luxo.', '02'),
 '03': cover('#FFFFFF', '#0E1A2B', '#1597D4', 'Fora do horário', 'O paciente das 23h', 'também agenda.', '03'),
 '04': cover('#1597D4', '#FFFFFF', '#0A1322', 'Falta na consulta', 'Faltou?', 'A IA remarca.', '04'),
}
os.makedirs(os.path.join(W, 'covers'), exist_ok=True)
for k, v in C.items():
    open(os.path.join(W, 'covers', k + '.html'), 'w').write(v)
print('ok')
