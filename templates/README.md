# Modelos da grade @tolkibrasil (versão 4, aprovada pelo Carlos em 05/10/2026)

Regra de ouro: intercalar **elaborados** com o **padrão** anterior. Cores chapadas, **sem degradê**. Textura de papel (grain) só nos elaborados.

| pasta | modelo | fundo | uso sugerido |
|---|---|---|---|
| elaborados/celular-whatsapp | iPhone com conversa de WhatsApp + cartão "agendado" | navy #0A1322 | manhã (carrossel) |
| elaborados/antes-depois | Sem IA x Com a Tolki | preto + roxo #7A32C4 | manhã |
| elaborados/aspas | frase entre aspas gigantes, serifada itálica | navy #0A1322 | manhã |
| elaborados/palavra-gigante | uma palavra enorme ("SUMIU.") + detalhe que conta a história | roxo #7A32C4 | manhã |
| elaborados/recibo | cupom fiscal do problema | cinza quente #E4E0D7 | manhã |
| padrao/branco-frase | frase em caixa alta, destaque roxo | branco | noite (post leve) |
| padrao/tweet-sobre-cor | card de tweet branco sobre cor | azul #1597D4 | noite |
| padrao/numero-grande | número com fonte ou prova permitida | branco | noite |
| padrao/notas | lista estilo Notas + Comente PALAVRA | preto | noite |

| foto/recepcao-noite | foto da recepção vazia à noite + notificação | foto escura | manhã |
| foto/cadeira-vazia | cadeira de dentista vazia + cartão "Faltou" | foto clara | manhã |
| foto/mao-celular | mão com celular no escuro | foto escura | manhã |
| foto/agenda-papel | mesa com agenda de papel + post-it escrito à mão | foto navy | manhã |

Fotos em `assets/fotos/` (geradas com IA, sem pessoas identificáveis). Regra: no máximo 1 foto a cada 5 ou 6 posts, só como capa da manhã, nunca duas fotos lado a lado nem na mesma coluna da grade. Reaproveite as fotos de `assets/fotos/` antes de gerar nova. Foto nova: Higgsfield (gpt_image_2_5, 4:5, quality high, 2k) ou Runway, sem texto, sem rosto, com espaço vazio para o título; salve em 1080x1350 em `assets/fotos/`. No Metricool, isAiGenerated fica false (decisão do Carlos).

Previews em `previas/` (`_grade.png` mostra o feed intercalado).

## Como usar
1. Copie o HTML do modelo para a pasta de slides do post (01.html, 02.html...) e troque só os textos. Mantenha a moldura (ícone, "TOLKI", "Nº XX · TEMA", fio e @tolkibrasil) nos elaborados.
2. Na pasta de trabalho: `npm i @fontsource/montserrat @fontsource/inter playwright` e `node <repo>/templates/render.js slides out 1350`.
3. Confira cada PNG com a ferramenta Read (corte, sobreposição, contraste).

## Regras
- Nunca dois posts seguidos no mesmo fundo; alternar claro e escuro (xadrez); no máximo 1 capa branca a cada 4 posts.
- Conversa, agenda ou recibo ilustrativos levam a marca "exemplo" quando parecerem reais. Sem nome, foto ou número real de paciente.
- Números só com fonte ou prova permitida (ex.: Odonto Excellence 15% para 45%).
- Sem emoji, sem travessão, sem degradê.
