#!/usr/bin/env python3
"""gen_ad.py: monta o reel.html de um anúncio a partir de spec.json + timing.json.
Uso (na pasta do anúncio, com node_modules/@fontsource ali):
  python3 <repo>/tools/ads-motion/gen_ad.py spec.json
spec.json: {"id": "...", "lines": [...], "scenes": [{"type": "text|big|beforeafter|chat|reply|stack|calc|grid|list|cta", "bg": "#hex", ...}]}
Uma cena por fala (lines). Depois: node <repo>/tools/reel-motion/frames.js <total>."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
spec = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'spec.json', encoding='utf-8'))
T = json.load(open('timing.json'))
assert len(spec['scenes']) == len(T['scenes']), 'uma cena por fala'
h = open(os.path.join(HERE, 'engine_tpl.html'), encoding='utf-8').read()
h = (h.replace('__ICON__', 'file://' + REPO + '/templates/assets/icone.png')
      .replace('__F__', 'file://' + os.path.abspath('node_modules/@fontsource'))
      .replace('__CF__', 'file://' + REPO + '/templates/fonts')
      .replace('__SPEC__', json.dumps(spec, ensure_ascii=False))
      .replace('__SCENES__', json.dumps(T['scenes'], ensure_ascii=False))
      .replace('__TOTAL__', str(T['total'])))
open('reel.html', 'w', encoding='utf-8').write(h)
print('reel.html ok', T['total'], 's')
