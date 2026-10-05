import json, os
W = os.path.dirname(os.path.abspath(__file__))
NB = '/tmp/claude-0/-home-claude-tolki-instagram-midia/3da1e8ac-fdd4-5d65-bb02-a0eb10d52cec/scratchpad/noite'
CF = '/root/.claude/skills/synced/bf6da4dc-ca23-4736-a0eb-c1837c9b7e91_e4ef817b-ed22-4555-92b5-ecd36c327b8c/canvas-design/canvas-fonts'
ICON = 'file://' + NB + '/1ad8e04cdc2248e24a886f3aa1a7882f.png'
F = NB + '/node_modules/@fontsource'
T = json.load(open(os.path.join(W, 'timing.json')))
html = open(os.path.join(W, 'reel_tpl.html')).read()
html = (html.replace('__ICON__', ICON).replace('__F__', 'file://' + F).replace('__CF__', 'file://' + CF)
        .replace('__SCENES__', json.dumps(T['scenes'], ensure_ascii=False)).replace('__TOTAL__', str(T['total'])))
open(os.path.join(W, 'reel.html'), 'w').write(html)
print('ok')
