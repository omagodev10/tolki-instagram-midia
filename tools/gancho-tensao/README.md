# gancho-tensao (modelo de motion "gancho de tensão" da Tolki)

Vídeo 9:16 de 35 a 50 s, aprovado pelo Carlos em 20/10/2026 (ampulheta v4, vela e dominó).
A skill `tolki-gancho-tensao` explica o padrão e a estratégia; aqui fica só o motor.

## Peças

| Arquivo | O que faz |
|---|---|
| `setup.sh` | Uma vez por sessão: fontes (npm), libs Python e o modelo Parakeet (ASR com tempo por palavra) |
| `voz_continua.py roteiro.json WORK` | **Padrão de voz de 26/10/2026** (`../reel-motion/VOZ_PADRAO_TOLKI.md`): commercial-7, uma tomada para o texto inteiro, 3 tomadas e escolha automática (texto e deriva de tom), 1,20x, ganho único; grava `a/voz.wav` e `tl.json` (o `render.py` usa a voz contínua) |
| `voz.py roteiro.json WORK` | (antigo, fala por fala: não use mais para narração) Voz Gemini fala por fala (usa `../reel-motion/gemini_tts.py`), apara silêncio, mede o início real de cada palavra e grava `tl.json`/`tl.js` |
| `core.py cena.py WORK` | Monta `WORK/page.html` juntando a cena com as partes comuns (gancho 6 s com contador, revelação, CTA, cartela) |
| `render.py WORK --out x.mp4` | Renderiza quadro a quadro (Playwright), compõe a filmagem do gancho se houver e mixa voz, efeitos e música |
| `exemplos/` | `ampulheta.html` (gancho filmado + cones em traço fino), `vela.py` (filmado), `domino.py` (100% desenhado) e os roteiros |
| `sfx/` | Efeitos gravados CC0 usados no modelo (`LICENSES.txt`); `sfx_synth.py` faz o tique |
| `assets/` | Logo Tolki e logos de clientes com prova liberada |

## Passo a passo

```sh
cd tools/gancho-tensao && ./setup.sh
W=/tmp/v1 && mkdir -p $W
python3 voz_continua.py meu.roteiro.json $W      # GEMINI_API_KEY no ambiente (padrão de voz de 26/10)
python3 core.py minha_cena.py $W                # copie e adapte um exemplo
python3 render.py $W --out teste.mp4 --prev 1 5.5 8 15 25 35   # folha de prévia em $W/out/prev.jpg
python3 render.py $W --out final.mp4 [--plate gancho.mp4] [--music trilha.mp3 --moff 13 --music-swell 30.95 --swell-line 7]
python3 render.py $W --out final.mp4 --audio-only ...           # só refaz o áudio (reaproveita o vídeo)
```

- Sem gancho de 6 s: ponha `"hook": 0` no roteiro e, na cena, não use `s0h`/`s0`/`s1` nem `hookReveal` (o visual continua o mesmo; a cena começa direto na fala 1).
- `--plate`: filmagem de 6 s do gancho (Seedance 720p 6 s, a partir de uma foto Soul Cinema). Sem ele, o gancho é desenhado na própria cena.
- Música: nunca vai para o repositório. `--moff` é onde começa o trecho, `--music-swell` o segundo em que a música cresce, `--swell-line` a fala onde esse crescimento deve cair. O volume fica limitado a +7,5 dB e, desde 26/10/2026, a música fica 3 dB mais baixa em relação à voz (o Carlos achou alta no Reel do convênio).
- A cena define `window.bgAt(t)` (fundo filmado no gancho), as cenas por fala (`SC`), o desenho em canvas (`drawArt`) e os efeitos (`cue(t, F('pasta/arquivo.ogg'), {g})`).
- Confira a sincronia transcrevendo trechos do vídeo final nos pontos-chave (a palavra tem que abrir o trecho).
