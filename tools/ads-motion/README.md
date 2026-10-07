# ads-motion (anúncios motion da Tolki para Meta Ads)

Motor de cenas para anúncios 9:16 narrados. Área útil y 260 a 1250 (rodapé coberto pela interface dos Reels), legenda em caixa na y 1290.

1. Pasta do anúncio com `spec.json` (lines + scenes, uma cena por fala). Tipos de cena: text, big, beforeafter, chat, reply, stack, calc, grid, list, cta.
2. Voz: as 3 vozes oficiais em rodízio (1 Bernard, 4 Brooks, 6 Sandra), como em `../reel-motion/README.md`. Take único, depois `python3 ../reel-motion/split_take.py v/take.mp3 roteiro.json a` (corta as falas, encurta pausas e acelera para 3,3 palavras/s, entre 1,0x e 1,3x).
3. Áudio: `job.json` + `python3 ../reel-motion/mix_motion.py job.json` (timing.json e mix.wav). Música da biblioteca remixada com cues (drop na virada ou na prova, break antes do CTA, hit no CTA) ou sem música, conforme o criativo. Depoimento real vai sem música ou com música bem baixa.
4. `python3 <repo>/tools/ads-motion/gen_ad.py spec.json`, conferir quadros com `node <repo>/tools/reel-motion/frames.js <total> 60,200`, depois todos e ffmpeg (igual ao reel-motion).
5. Anúncios publicados ficam em `ads/AAAA-MM-DD/` (mp4, capa jpg e spec). No spec, grave também `angulo`, `voz` e `musica` para o painel de tráfego.

Ângulos: prova, dor, conta (custo), resposta rápida, ICP e **história narrada com personagem** (`../reel-motion/HISTORIA.md`).
Regras: sem preço, sem travessão, número só com prova liberada, conversa ou personagem ilustrativo leva "exemplo ilustrativo", CTA de toque no botão (diagnóstico comercial gratuito).
