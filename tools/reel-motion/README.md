# reel-motion (Reel narrado em motion graphics, padrão da noite e dos anúncios)

Aprovado pelo Carlos em 05/10/2026 (formato) e 07/10/2026 (vozes novas, ritmo, música remixada, ângulo história).
Exemplos: `exemplo-historia-camila/` (Bernard + Seven Nation Army), `exemplo-historia-rafael/` (Brooks + Timeless) e `exemplo-apuracao/` (formato original).
O ângulo "história narrada com personagem" está em `HISTORIA.md`.

## Formato
- 1080x1920, 30 fps, 25 a 35 s, 5 a 7 cenas (uma frase narrada por cena).
- Visual da grade: cores chapadas da paleta Tolki, sem degradê, sem emoji, Montserrat 900 + Instrument Serif itálico + DM Mono, ícone e @tolkibrasil no topo (y 150), legenda em caixa na y 1540. Texto importante entre y 260 e y 1580.
- Estrutura: gancho (0 a 3 s), a dor, a virada "a Tolki resolve", "Comenta PALAVRA". Cada cena tem uma animação própria. Conversas, listas e personagens ilustrativos levam "exemplo ilustrativo".
- Capa separada (1080x1920) no modelo de `exemplo-apuracao/gen_covers.py`, seguindo o rodízio de cor da grade (capa.txt).

## Vozes oficiais (só estas 3, em rodízio; não repita a voz do motion anterior)
| Voz | Clima | Onde gerar |
|---|---|---|
| 1 · Bernard | masculina, confiante, narrador de história | Runway `generate_speech`: model `eleven_v3`, voice `Bernard`, languageCode `pt`, speed 1.2 |
| 4 · Brooks | masculina, leve, conversa | Higgsfield `generate_audio`: model `elevenlabs_v4`, prompt = roteiro, `dialogue` = [{"text": roteiro, "voice_type": "preset", "voice_id": "c2acff45-84b2-4974-892d-89fa2d4e5598"}] (confira com `models_explore` se o formato mudar) |
| 6 · Sandra | feminina, debochada, ironia | Runway `generate_speech`: model `eleven_v3`, voice `Sandra`, languageCode `pt`, speed 1.2, texto começa com `[sarcastic]` |

Combine voz e roteiro: história e virada pedem Bernard; ironia e "faz sentido? não" pedem Sandra; papo leve, bastidor e dica rápida pedem Brooks. Sem o conector Higgsfield na sessão, alterne só Bernard e Sandra e diga isso na entrega.
Nunca clone a voz de uma pessoa real (dublador, influenciador, celebridade). A voz antiga (Luana) saiu do padrão.

**Take único (soa mais natural que uma frase por pedido):** mande o roteiro inteiro num pedido, uma fala por linha, sem etiquetas de pausa (elas mudam o jeito de falar).
Runway: espere o `get_task` dar a URL (dnznrvs05pmza.cloudfront.net) e baixe com curl em `v/take.mp3`. Higgsfield: baixe o resultado do `jobs_wait`.
Se o `split_take.py` avisar "divisão incerta", gere uma fala por pedido (mesma voz e parâmetros) e passe os arquivos separados por vírgula.

## Ritmo (regra aprovada)
`python3 <repo>/tools/reel-motion/split_take.py v/take.mp3 roteiro.json a` faz tudo: corta uma fala por cena, encurta pausas acima de 0,38 s para 0,30 s (a pausa cômica curta fica) e acelera para 3,3 palavras por segundo, entre 1,0x e 1,3x, sem mudar o tom. `roteiro.json` = `{"lines": [...]}`. Leia o que ele imprime: com "ATENÇÃO", refaça a voz antes de seguir.

## Música (remix: o melhor momento cai na hora certa)
As instrumentais (sem a voz do cantor) ficam numa biblioteca privada (artifact "Biblioteca de músicas Tolki"; o link está no prompt da tarefa). Não suba música com direitos neste repositório.
1. `ArtifactData` list, collection `musicas`: cada doc tem `slug`, `audio` (id do mp4), `analise` (id do song.json), `drops`, `breaks`, `clima`, `combina_com`, `ativa`, `usos`.
2. `Artifact` read com `path` = id do áudio (um id por chamada, use `path` e não `paths`) e `out_dir` = `songs/<slug>`; ele salva `<id>.mp4`: renomeie para `songs/<slug>/inst.mp4`. Faça o mesmo com `analise` (salva `<id>.json`) e renomeie para `song.json`.
3. No `job.json`: `"music": {"song": "songs/<slug>", "rel_db": -15, "cues": [...]}`.

Receitas de cue (`scene` = índice da cena, `at` = segundos a partir do início dela):
- **Virada (padrão):** `{"scene": <cena em que a Tolki entra>, "kind": "drop"}`, `{"scene": <cena do CTA>, "at": -0.15, "kind": "break"}`, `{"scene": <cena do CTA>, "at": 1.2, "kind": "hit"}`.
- **Abrindo com energia (gancho forte):** `{"scene": <cena da moral ou da dor>, "at": 1.1, "kind": "break"}`, `{"scene": <solução>, "kind": "drop"}` e o mesmo break e hit do CTA.
- **Sem música:** apague `"music"`. Use em depoimento real, assunto sério, explicação com número ou quando a ironia da voz precisa de silêncio. Os efeitos continuam.

Rodízio: não repita a música do motion anterior e alterne com e sem música conforme o conteúdo. Depois do `mix_motion.py`, cada cue imprime a variação da música: drop e hit pedem +3 dB ou mais, break pede -6 dB ou menos. "FRACO" = troque o cue ou a música.
Música nova: o Carlos manda o arquivo numa conversa com o Claude, que tira a voz, marca os momentos e coloca na biblioteca.

## Passo a passo (na pasta de trabalho)
1. `npm i @fontsource/montserrat @fontsource/inter playwright` e `pip install --break-system-packages pyloudnorm`
2. Voz (acima) e `split_take.py` (gera `a/l1.wav`...).
3. Efeitos: baixe as URLs de `tools/reelkit/sons.json` para `lib/<CHAVE>.mp3`. Música da biblioteca em `songs/<slug>/`.
4. `job.json` (veja os exemplos de história) e `python3 <repo>/tools/reel-motion/mix_motion.py job.json` gera `timing.json` e `mix.wav` (-14 LUFS). O `build_audio.py` antigo continua funcionando, mas sem remix.
5. Copie o `reel_tpl.html` de um exemplo, reescreva as cenas (`<div class="sc" id="s0">`...) e a função `window.__tick(t)`. Use `B[i]` (início da cena i) para cronometrar as animações e acerte os momentos visuais fortes nos mesmos instantes dos cues da música.
6. `python3 <repo>/tools/reel-motion/gen_reel.py reel_tpl.html`, confira quadros soltos com `node <repo>/tools/reel-motion/frames.js <total> 60,200,400` (ferramenta Read em `f/*.jpg`), depois gere todos: `node <repo>/tools/reel-motion/frames.js <total>`.
7. `ffmpeg -framerate 30 -i f/%05d.jpg -i mix.wav -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart reel.mp4`
8. Publicação: `posts/AAAA-MM-DD-noite/reel.mp4`, `capa.jpg`, `capa.txt` ("REEL CAPA <COR> · #hex"), `legenda.txt`. Metricool: instagramData.type "REEL", media = URL raw do mp4, videoThumbnailUrl = URL raw da capa, isAiGenerated false.

O vídeo final vai para o repositório público com a música dentro (o Carlos liberou o uso das duas músicas); só os arquivos de música soltos ficam fora.
