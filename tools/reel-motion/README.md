# reel-motion (Reel narrado em motion graphics, padrão da noite)

Aprovado pelo Carlos em 05/10/2026: todo dia sai 1 carrossel (manhã) e 1 Reel motion narrado (noite).
Exemplo completo e aprovado: `exemplo-apuracao/` (vídeo publicado em `posts/2026-10-05-0800-reel/`).

## Formato
- 1080x1920, 30 fps, 25 a 35 s, 5 a 7 cenas (uma frase narrada por cena).
- Visual da grade: cores chapadas da paleta Tolki, sem degradê, Montserrat 900 + Instrument Serif itálico + DM Mono, ícone e @tolkibrasil no topo (y 150), legenda em caixa na y 1540. Texto importante entre y 260 e y 1580 (fora disso a interface do Instagram cobre).
- Estrutura: gancho do assunto do momento (0 a 4 s), a dor, a virada "a Tolki resolve", "Comenta PALAVRA". Cada cena tem uma animação própria (contador, lista, carimbo, agenda enchendo, digitação...). Conversas e listas ilustrativas levam "exemplo ilustrativo".
- Capa separada (1080x1920) no modelo de `exemplo-apuracao/gen_covers.py`: título no centro, sobrevive ao recorte 3:4 da grade. A cor da capa segue as regras de rodízio da grade (capa.txt).

## Passo a passo (na pasta de trabalho do Reel)
1. `npm i @fontsource/montserrat @fontsource/inter playwright`
2. Voz: Higgsfield `generate_audio_batch`, model `text2speech_v2`, variant `elevenlabs`, voice_type `element`, voice_id `6023c405-cacc-42fd-b42b-c7d78f657c32` (Luana Tolki BR). Uma frase por pedido. Baixe em `a/l1.mp3`, `a/l2.mp3`...
3. Trilha: Runway `generate_music` (lyria-3-clip, instrumental, sem voz) e baixe a URL de `get_task` em `musica.mp3`; ou use `MUSIC_TECHHOUSE` de `tools/reelkit/sons.json`.
4. Efeitos: baixe as URLs de `tools/reelkit/sons.json` para `lib/<CHAVE>.mp3`.
5. `job.json` (ver o do exemplo) e `python3 <repo>/tools/reel-motion/build_audio.py job.json` gera `timing.json` e `mix.wav` (-14 LUFS, trilha abaixa sozinha na voz).
6. Copie `exemplo-apuracao/reel_tpl.html` para `reel_tpl.html`, reescreva as cenas (`<div class="sc" id="s0">`...) e a função `window.__tick(t)`. Use `B[i]` (início da cena i) para cronometrar as animações.
7. `python3 <repo>/tools/reel-motion/gen_reel.py reel_tpl.html`, confira quadros soltos com `node <repo>/tools/reel-motion/frames.js <total> 60,200,400` (ferramenta Read em `f/*.jpg`), depois gere todos: `node <repo>/tools/reel-motion/frames.js <total>`.
8. `ffmpeg -framerate 30 -i f/%05d.jpg -i mix.wav -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart reel.mp4`
9. Publicação: `posts/AAAA-MM-DD-noite/reel.mp4`, `capa.jpg`, `capa.txt` ("REEL CAPA <COR> · #hex"), `legenda.txt`. Metricool: instagramData.type "REEL", media = URL raw do mp4, videoThumbnailUrl = URL raw da capa, isAiGenerated false.
