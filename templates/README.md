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
| foto/recepcao-cheia | balcão da recepção lotado (telefone, papéis, celular) | foto clara | manhã |
| foto/agenda-papel | mesa com agenda de papel + post-it escrito à mão | foto navy | manhã |

Fotos em `assets/fotos/` (geradas com IA, sem pessoas identificáveis). Regra: no máximo 1 foto a cada 5 ou 6 posts, só como capa da manhã, nunca duas fotos lado a lado nem na mesma coluna da grade. Reaproveite as fotos de `assets/fotos/` antes de gerar nova. Foto nova: Higgsfield (gpt_image_2_5, 4:5, quality high, 2k) ou Runway (o download direto do Runway é bloqueado nesta rede; use a cópia que a ferramenta get_task salva em tool-results, em 1536x1920), sem texto, sem rosto, com espaço vazio para o título; salve em 1080x1350 em `assets/fotos/`. No Metricool, isAiGenerated fica false (decisão do Carlos).

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

## Ângulos extras do instagram-skills (opcionais, aprovados pelo Carlos em 10/10/2026)
Não é obrigação usar. São possibilidades novas de ângulo e formato para a fatia de teste da regra 70/30 (ou quando o tema pedir). Os 70% continuam explorando o que já dá resultado. Vale para carrossel, Reel e criativo de anúncio.
1. Objetivo do post: escolha um (SALVAR, ENVIAR, COMENTAR ou SEGUIR) e diga na entrega "Objetivo: X". Formatos que combinam: SALVAR = lista, passo a passo, antes e depois; ENVIAR = mito e verdade, opinião contrária defensável; COMENTAR = cena que o dono de clínica reconhece; SEGUIR = transformação com prova.
2. CTA: "Comente PALAVRA" continua o padrão (o ManyChat entrega algo real). Em post de SALVAR ou ENVIAR pode trocar por "Salva pra usar na próxima campanha" ou "Manda pra quem ainda acha que [mito]". Nunca "comenta SIM", "marca 3 amigos" ou "o que você acha?".
3. Esqueletos novos:
   - Antes e depois: o primeiro slide ou cena mostra o DEPOIS, o segundo o ANTES, depois o caminho (encaixa na prova Odonto Excellence, 15% para 45%).
   - Mito e verdade: o mito precisa ser crença real do dono de clínica (não invente mito); a verdade só com prova permitida. Último slide ou cena pede envio.
4. Ganchos: "Como a [cliente real] fez X" em vez de "Como fazer X"; número exato com o nome do cliente junto (só provas permitidas, número solto não conta); laço aberto ("o terceiro sai caro", "o 4º quase todo mundo erra").
5. Carrossel: o ponto mais forte no slide 2 ou 3; penúltimo slide resume tudo numa tela (o que se salva); com menos de 4 pontos reais vira post único.
6. Reel: laço visual, o último quadro conversa com o primeiro (mesma cor, objeto ou frase).
7. Cortes de cara de IA em roteiro e legenda: "O resultado?", "A verdade?", "Papo reto", "Vou ser sincero", "Sem X. Sem Y. Só Z.", "Pare de X, comece Y"; no máximo 2 frases soltas de efeito por legenda; evite abrir frase com gerúndio ("Pensando nisso,").
8. Hashtags: 2 ou 3 de nicho (menos de 50 mil posts), 1 ou 2 médias, no máximo 1 ampla. Métricas e agendamento continuam no Metricool.
9. Quando usar um destes, registre no painel (campo angulo, ex.: "mito e verdade · objetivo ENVIAR") para comparar salvamentos, envios e CPL com os ângulos de sempre.
