# Padrão de voz da Tolki (Gemini 3.8 TTS) · aprovado em 26/10/2026

Use este padrão em toda narração e em todo áudio "da IA" dos vídeos da Tolki (Reels orgânicos e anúncios). Ele saiu de muitas rodadas de teste. Os itens em "Não faça" já foram testados e reprovados. Ele substitui o rodízio de 6 vozes e a geração fala por fala.

No motor `tools/gancho-tensao`, use `python3 voz_continua.py roteiro.json WORK` (faz os passos 1 a 6 abaixo e grava `a/voz.wav` + `tl.json`; o `render.py` coloca a voz inteira, contínua, com um ganho só).

---

## 1. Narração (locução do vídeo)

**Configuração**
- Modelo: `gemini-3.8-flash-tts`
- Voz: `pt-br-commercial-7` (a mesma da Luana)
- Estilo num campo separado (`speech_metadata.style`), em inglês, sempre este:
  ```
  warm, confident and engaging female narrator, like a friendly expert talking to one person, natural pacing, smiling voice, clear diction
  ```
- Chave só na variável `GEMINI_API_KEY` (nunca em arquivo).

**Como gerar**
1. **Uma tomada só para o texto inteiro** do vídeo (até ~35 s). Gerar frase por frase muda o tom entre as frases.
2. **Gere 3 tomadas** e escolha automaticamente:
   - descarte a que trocou palavra (transcreva e compare com o roteiro; o transcritor escreve número em algarismo, então compare com a melhor tomada e aceite até 4 pontos abaixo dela);
   - entre as que sobram, fique com a de **menor deriva de tom**, ou seja, a que menos muda a altura média da voz entre trechos de 5 s.
3. **Apare só o silêncio do começo e do fim.** Não corte nem reespace as frases por dentro: o áudio entra contínuo no vídeo.
4. **Acelere só no fim, o áudio inteiro, em 1,20x:** `ffmpeg -i in.wav -af atempo=1.2 out.wav`.
5. **Volume com um ganho só** para a voz inteira (ex.: -16 LUFS), e master do vídeo em -14 LUFS com pico em -1 dB (`alimiter`).
6. **Sincronia:** transcreva a tomada final com tempo por palavra (Parakeet/sherpa-onnx ou Whisper) e use esses tempos só para fazer texto e animação entrarem junto da palavra. Não use para recortar o áudio.

**Regras do texto**
- Não escreva "Tolki" (ela pronuncia errado). Use "a nossa IA" ou "a gente". Se o nome for obrigatório, escreva `Tolki /ˈtɔwki/` e confira ouvindo.
- Números por extenso: "oitenta reais", "vinte e quatro horas", "dez e meia".
- Sem MAIÚSCULAS de ênfase e sem reticências (as duas atrapalham a pronúncia e deixam a voz forçada). Use vírgulas para respirar.
- CTA de comentário: escreva "Comenta a palavra implante" (só "Comenta implante" ela lê "comenta a implante"). Na tela, a palavra continua em maiúscula.
- Frases curtas, de fala, como quem conversa nos stories.

**Chamada da API (uma tomada)**
```bash
curl -s https://generativelanguage.googleapis.com/v1beta/interactions \
  -H "x-goog-api-key: $GEMINI_API_KEY" -H "Content-Type: application/json" \
  -d '{
  "model": "gemini-3.8-flash-tts",
  "input": [{"type": "user_input", "content": [{"type": "text",
    "text": "TEXTO INTEIRO DO VÍDEO AQUI",
    "annotations": [{"type": "speech_metadata",
      "style": "warm, confident and engaging female narrator, like a friendly expert talking to one person, natural pacing, smiling voice, clear diction"}]}]}],
  "response_format": {"type": "audio"},
  "generation_config": {"speech_config": [{"voice": "pt-br-commercial-7"}]}
}'
```
O áudio volta em base64. Se não vier como WAV, é PCM de 16 bits, mono, 24 kHz: `ffmpeg -f s16le -ar 24000 -ac 1 -i voz.pcm voz.wav`.

---

## 2. Áudio "da IA" com sotaque regional

Serve para quando o vídeo mostra a IA mandando áudio com o sotaque do paciente.

**Configuração**
- Mesma voz (`pt-br-commercial-7`), **um sotaque por pedido**. Quando um pedido mistura várias regiões, o sotaque fica fraco.
- Estilo com os **traços fonéticos da região**, descritos assim:
  - **Base de todas:** `friendly clinic receptionist sending a WhatsApp voice note, warm and natural, `
  - **São Paulo:** `very strong and thick São Paulo city (paulistano) accent: tapped R in 'certo', strong nasal vowels, the 'meu' stretched and sung, lively and upbeat with the same energy as the rest of the message, natural fast pace`
  - **Rio:** `very strong and thick carioca accent from Rio de Janeiro: every syllable-final S sounds like 'sh', guttural R, drawling sing-song cadence`
  - **Recife:** `very strong and thick Recife (Pernambuco) accent: T and D before I stay hard with no 'tch' or 'dj', S before consonants sounds like 'sh', open vowels, very musical rising and falling melody`
  - **Porto Alegre:** `very strong and thick gaúcho accent from Porto Alegre: final E pronounced as a clear 'e' not 'i', rising sing-song intonation, emphatic 'bah' and 'tchê'`
- **No texto, uma marca da região:** meu (SP), oxe e visse (PE), bah, tchê e "pra ti/tua" (RS). Evite gíria forçada ("maneiro" foi reprovado).
- **Não use IPA nem descrição de sotaque no texto.** O teste mostrou que o estilo com os traços sozinho (versão A) soa melhor.

**Como montar várias regiões numa fala só**
1. Gere **8 tomadas por região**.
2. Transcreva e descarte as que trocaram palavra.
3. Meça em cada tomada a altura média da voz (F0), o ritmo (sílabas/s), a variação de tom (desvio em semitons) e o volume.
4. Teste todas as combinações (uma tomada por região) e fique com a de **voz mais parecida entre as regiões**, dando peso extra a cada emenda (a SP → Rio era a mais sensível).
5. Iguale o **volume de cada trecho** (-18 LUFS). Aqui pode, porque são gravações separadas.
6. Se uma região ficou mais lenta que as outras, acelere **só ela, no máximo 12%**, para casar o ritmo.
7. Emende com **0,15 s** de respiro e acelere tudo em **1,10x** no fim.
8. Para um áudio com uma região só (ex.: o do Aristides), basta uma tomada boa em 1,10x.

---

## 3. Não faça (testado e reprovado)
- Gerar a narração frase por frase ou nivelar o volume frase a frase: a voz oscila.
- Acelerar 1,16x ou mais **e** nivelar por frase: fica robótica.
- Estilo longo ou em português, com muita instrução: a voz varia.
- Pedir sotaque no estilo de uma voz pronta sem os traços fonéticos: fica fraco.
- Voice design (voz criada por descrição) e ElevenLabs: reprovados pelo usuário.
- Reticências e "Olha..." no texto: erros de pronúncia.

## 4. Conferência antes de entregar
- Transcrever o áudio final inteiro: nenhuma palavra trocada ou a mais.
- Ouvir o nome da clínica e da marca, porque o transcritor não confirma pronúncia de nome próprio.
- No vídeo, cortar 1,2 s começando em 3 palavras-chave e transcrever: a palavra tem que abrir o trecho (sincronia).
