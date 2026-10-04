# reelkit (Tolki)

Editor automático de Reels no visual da @tolkibrasil.

- `analyze.py bruto.mp4 roteiro.txt out/`: vídeo cru em selfie. Corta silêncios, erros e regravações (fica a última tomada de cada frase), transcreve e cronometra cada palavra. Usa sherpa-onnx (Whisper small + Silero VAD).
- `align_fw.py video.mp4 roteiro.txt out/`: vídeo sem cortes (avatar). Só cronometra as palavras com faster-whisper.
- `render.py video.mp4 out/edit.json plano.json final.mp4`: legenda palavra a palavra, cartões (topo, lista, número grande, virada), zoom alternado, whoosh, loudnorm -14 LUFS, 1080x1920 30fps.

`plan_exemplo.json` mostra o formato do plano de cartões (cada cartão aponta para a linha do roteiro).
