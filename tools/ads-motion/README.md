# ads-motion (anúncios motion da Tolki para Meta Ads)

Motor de cenas para anúncios 9:16 narrados. Área útil y 260 a 1250 (rodapé coberto pela interface dos Reels), legenda em caixa na y 1290.

1. Pasta do anúncio com `spec.json` (lines + scenes, uma cena por fala). Tipos de cena: text, big, beforeafter, chat, reply, stack, calc, grid, list, cta.
2. Voz: Higgsfield text2speech_v2, elevenlabs, element 6023c405-cacc-42fd-b42b-c7d78f657c32 (Luana). Uma fala por pedido, em `a/l1.mp3`...
3. `job.json` + `python3 ../tools/reel-motion/build_audio.py job.json` (timing.json e mix.wav).
4. `python3 <repo>/tools/ads-motion/gen_ad.py spec.json`, conferir quadros com `node <repo>/tools/reel-motion/frames.js <total> 60,200`, depois todos e ffmpeg (igual ao reel-motion).
5. Anúncios publicados ficam em `ads/AAAA-MM-DD/` (mp4, capa jpg e spec).

Regras: sem preço, sem travessão, número só com prova liberada, conversa ilustrativa leva "exemplo ilustrativo", CTA de toque no botão (diagnóstico comercial gratuito).
