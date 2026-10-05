#!/usr/bin/env python3
"""gen_reel.py: injeta tempos, ícone e fontes no reel_tpl.html e grava reel.html.
Uso (na pasta do Reel, com node_modules/@fontsource instalado ali):
  python3 <repo>/tools/reel-motion/gen_reel.py reel_tpl.html
Placeholders do template: __ICON__, __F__ (fontsource), __CF__ (fontes extras do repo), __SCENES__, __TOTAL__."""
import json, os, sys
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
tpl = sys.argv[1] if len(sys.argv) > 1 else 'reel_tpl.html'
T = json.load(open('timing.json'))
h = open(tpl).read()
h = (h.replace('__ICON__', 'file://' + REPO + '/templates/assets/icone.png')
      .replace('__F__', 'file://' + os.path.abspath('node_modules/@fontsource'))
      .replace('__CF__', 'file://' + REPO + '/templates/fonts')
      .replace('__SCENES__', json.dumps(T['scenes'], ensure_ascii=False))
      .replace('__TOTAL__', str(T['total'])))
open('reel.html', 'w').write(h)
print('reel.html ok', T['total'], 's')
