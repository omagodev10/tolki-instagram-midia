#!/usr/bin/env python3
"""gemini_tts.py: narração com o Gemini 3.8 Flash TTS (voz brasileira nativa, direção por fala e expressões).

Uso:
  GEMINI_API_KEY=... python3 <repo>/tools/reel-motion/gemini_tts.py roteiro.json v/take.mp3 [voz] [modelo]
  voz padrão: pt-br-podcaster-1 · modelo padrão: gemini-3.8-flash-tts
  python3 gemini_tts.py --vozes            lista as vozes pt-BR da biblioteca do Google (107 vozes)

roteiro.json aceita dois formatos:
  {"lines": ["fala 1", "fala 2"], "estilo": "tom geral"}                     (o mesmo do split_take.py)
  {"falas": [{"texto": "fala 1 <short pause> Sei. <laugh>", "estilo": "irônico, segurando o riso"}, ...],
   "estilo": "tom geral, vale para as falas sem estilo próprio"}
Direção (como um diretor de dublagem):
  - "estilo" = como falar a fala inteira (emoção, ritmo, intenção). Escreva em português, curto e concreto:
    "animado, sorriso na voz, ritmo rápido", "irônico, debochado", "sério e baixo, quase confidência".
  - Expressões no meio do texto, entre < >: <laugh> <sigh> <breath> <gasp> <short pause> <long pause> <whispering>...
    Elas acontecem naquele ponto e não são lidas. Use pouco: 1 ou 2 por fala.
  - O texto é lido ao pé da letra: nada de instrução dentro do texto.
Depois rode split_take.py com o <saida>_lines.json que este script grava (textos sem as etiquetas).
A chave nunca vai para o repositório: só por variável de ambiente GEMINI_API_KEY."""
import base64, json, os, re, subprocess, sys, urllib.request, urllib.error

API = 'https://generativelanguage.googleapis.com/v1beta'
ESTILO = 'português do Brasil natural, conversa de Reels: confiante, animado e direto, ritmo ágil, sem tom de locutor'


def call(path, key, body=None):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body else None,
                                 headers={'Content-Type': 'application/json', 'x-goog-api-key': key})
    try:
        return json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as e:
        sys.exit(f'erro {e.code}: {e.read().decode()[:600]}')


def find_audio(o):
    if isinstance(o, dict):
        if isinstance(o.get('data'), str) and len(o['data']) > 1000: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            a = find_audio(v)
            if a: return a


def main():
    key = os.environ.get('GEMINI_API_KEY') or sys.exit('defina GEMINI_API_KEY')
    if sys.argv[1] == '--vozes':
        tok, n = '', 0
        while True:
            r = call('/voices?pageSize=1000' + (f'&pageToken={tok}' if tok else ''), key)
            for v in r.get('voices', []):
                if (v.get('language_code') or '').startswith('pt-BR'):
                    n += 1; print(v['id'], v.get('gender'), v.get('pitch'), '|', v.get('description', ''))
            tok = r.get('next_page_token') or r.get('nextPageToken')
            if not tok: break
        return print(n, 'vozes pt-BR')
    rot, out = sys.argv[1], sys.argv[2]
    voz = sys.argv[3] if len(sys.argv) > 3 else 'pt-br-podcaster-1'
    modelo = sys.argv[4] if len(sys.argv) > 4 else 'gemini-3.8-flash-tts'
    C = json.load(open(rot, encoding='utf-8'))
    geral = C.get('estilo') or ESTILO
    falas = C.get('falas') or [{'texto': l} for l in C['lines']]
    content = [{'type': 'text', 'text': f['texto'] + ('\n' if i < len(falas) - 1 else ''),
                'annotations': [{'type': 'speech_metadata', 'style': f.get('estilo') or geral}]} for i, f in enumerate(falas)]
    body = {'model': modelo, 'input': [{'type': 'user_input', 'content': content}],
            'response_format': {'type': 'audio'}, 'generation_config': {'speech_config': [{'voice': voz}]}}
    a = find_audio(call('/interactions', key, body)) or sys.exit('a resposta veio sem áudio')
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '-', '-b:a', '192k', out], input=base64.b64decode(a['data']), check=True)
    dur = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out], capture_output=True, text=True).stdout.strip()
    print('ok', out, voz, modelo, dur + 's')
    lim = os.path.splitext(out)[0] + '_lines.json'   # roteiro limpo (sem etiquetas) para o split_take.py
    json.dump({'lines': [re.sub(r'\s*<[^>]+>\s*', ' ', f['texto']).strip() for f in falas]}, open(lim, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
