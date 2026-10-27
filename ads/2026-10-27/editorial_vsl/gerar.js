// Gera 10 estáticos "editorial Tolki" (estilo notícia/curiosidade), 1080x1350, para a VSL /v7/.
// Regras: sem preço, sem travessão, só provas liberadas, sem imitar veículo real (marca própria "Tolki Insights").
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const LP = '/home/claude/tolki-landpage/public';
const OUT = process.argv[2] || 'out';
fs.mkdirSync(OUT, { recursive: true });
const b64 = f => fs.readFileSync(f).toString('base64');
const font = (f) => `url(data:font/woff2;base64,${b64(f)}) format('woff2')`;
const FS = 'node_modules/@fontsource/source-serif-4/files/source-serif-4-latin-';
const SA = LP + '/assets/fonts/sarabun-latin-';
const img = n => fs.existsSync('img/'+n+'.jpg') ? `data:image/jpeg;base64,${b64('img/'+n+'.jpg')}` : `data:image/webp;base64,${b64(LP + '/v2/img/' + n + '.webp')}`;
const logo = 'data:image/svg+xml;base64,' + b64(LP + '/assets/logo.svg');

const ITENS = [
  { id: 'N01_edson_15_45', kick: 'Caso real', h: 'Clínica odontológica triplica a taxa de agendamento: de <em>15% para 45%</em>', deck: 'O que mudou no atendimento da Odonto Excellence, segundo o próprio dono.', vis: 'salto' },
  { id: 'N02_fabio_54', kick: 'Recorde', h: 'Franquia de ortodontia fecha <em>54 contratos</em> em um mês e bate recorde de faturamento', deck: 'A OrthoDontic mudou a forma de responder os pacientes no WhatsApp.', foto: 'fabio', quem: 'Fabio, OrthoDontic', num: '54', numl: 'contratos em um mês' },
  { id: 'N03_luis_dobrou', kick: 'Caso real', h: 'Clínica <em>dobra os agendamentos</em> no primeiro disparo para pacientes antigos', deck: 'A Gou Odonto voltou a falar com quem já era paciente.', foto: 'luis', quem: 'Luis, Gou Odonto', num: '2x', numl: 'agendamentos no 1º disparo' },
  { id: 'N04_victor_60mil', kick: 'Economia', h: 'Instituto economiza <em>R$ 60 mil</em> em mensagens de WhatsApp em 6 meses', deck: 'Foram 200 mil mensagens no Instituto Victor Santos.', foto: 'victor', quem: 'Dr. Victor Santos, Instituto Victor Santos', num: 'R$ 60 mil', numl: 'economizados em 6 meses' },
  { id: 'N05_felipe_38', kick: 'Caso real', h: '<em>+38% de agendamentos</em> em 10 meses: o que mudou na recepção da Dental Clinic', deck: 'Mais agendamento e mais qualidade no tráfego, segundo o Dr. Felipe Mafra.', foto: 'felipe', quem: 'Dr. Felipe Mafra, Dental Clinic', num: '+38%', numl: 'em 10 meses' },
  { id: 'N06_preco_e_some', kick: 'Curiosidade', h: 'Por que o paciente pergunta o preço e <em>some</em> (e o que as clínicas que agendam fazem diferente)', deck: 'O problema quase nunca é o valor.', vis: 'chat' },
  { id: 'N07_horario', kick: 'Curiosidade', h: 'O horário em que a sua clínica mais perde pacientes <em>não é o que você imagina</em>', deck: 'E quase nenhuma recepção está lá para responder.', vis: 'relogio' },
  { id: 'N08_metodo_30mil', kick: 'Método', h: 'O método que clínicas acima de <em>R$ 30 mil/mês</em> usam para triplicar a taxa de agendamento', deck: 'Sem gastar mais em anúncio. A apresentação completa tem menos de 5 minutos.', vis: 'agenda' },
  { id: 'N09_470_clinicas', kick: 'Tendência', h: '<em>+470 clínicas</em> já colocaram IA para responder o WhatsApp. O que elas descobriram', deck: 'Resposta em segundos, 24 horas, inclusive no fim de semana.', vis: 'contador' },
  { id: 'N10_base_parada', kick: 'Curiosidade', h: 'A lista de pacientes parada no seu WhatsApp vale mais que o <em>próximo anúncio</em>', deck: 'Clínicas estão enchendo a agenda com quem já foi paciente.', vis: 'lista' },
];

const visual = {
  chat: `<div class="vis chat"><div class="bub in">Oi! Quanto custa o clareamento?<span>21:47</span></div><div class="seen">Visualizada · sem resposta</div><div class="bub in late">Oi?? 🙁<span>09:12</span></div><div class="tag">exemplo ilustrativo</div></div>`,
  relogio: `<div class="vis clock"><div class="dial"><i class="h"></i><i class="m"></i><b></b></div><div class="clk-r"><div class="clk-t">22:00</div><div class="pill">12 mensagens sem resposta</div></div><div class="tag">exemplo ilustrativo</div></div>`,
  agenda: `<div class="vis cal">${['Seg','Ter','Qua','Qui','Sex'].map((d,i)=>`<div class="col"><b>${d}</b>${[0,1,2,3,4].map(j=>`<i class="${(i*5+j)%7<5?'on':''}"></i>`).join('')}</div>`).join('')}<div class="tag">exemplo ilustrativo</div></div>`,
  salto: `<div class="vis big salto"><s>15%</s><b>45%</b><span>de agendamento · Edson, Odonto Excellence</span></div>`,
  contador: `<div class="vis big"><b>+470</b><span>clínicas usam a Tolki</span></div>`,
  lista: `<div class="vis list">${['Mariana C.','Roberto L.','Patrícia S.','Fernanda M.','Carlos E.'].map((n,i)=>`<div class="row"><i>${n[0]}</i><b>${n}</b><span>última conversa há ${[7,11,4,9,14,6,8][i]} meses</span></div>`).join('')}<div class="tag">exemplo ilustrativo</div></div>`,
};

function html(it) {
  const media = it.foto
    ? `<div class="photo"><img src="${img(it.foto)}"><div class="cap">${it.quem}</div><div class="num" style="--nf:${it.num.length>5?64:92}px"><b>${it.num}</b><span>${it.numl}</span></div></div>`
    : visual[it.vis];
  return `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:SS;font-weight:600;src:${font(FS+'600-normal.woff2')}}
@font-face{font-family:SS;font-weight:700;src:${font(FS+'700-normal.woff2')}}
@font-face{font-family:SA;font-weight:400;src:${font(SA+'400-normal.woff2')}}
@font-face{font-family:SA;font-weight:500;src:${font(SA+'500-normal.woff2')}}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;background:#F6F3EC;color:#112E4A;font-family:SA;overflow:hidden;position:relative}
.mast{display:flex;align-items:center;justify-content:space-between;padding:44px 64px 22px}
.mast .brand{display:flex;align-items:center;gap:16px}
.mast img{height:34px}
.mast .ins{font-family:SS;font-weight:700;font-size:30px;letter-spacing:.02em;border-left:2px solid #112E4A;padding-left:16px}
.mast .ed{font-size:20px;letter-spacing:.14em;text-transform:uppercase;opacity:.7}
.rule{height:4px;margin:0 64px;background:linear-gradient(90deg,#192D48,#3A80C5,#00ADEE,#9D66C6,#C9A6E4)}
.rule2{height:1px;margin:6px 64px 0;background:#112E4A;opacity:.35}
.kick{margin:40px 64px 0;display:inline-block;font-size:22px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:#fff;background:#E5484D;padding:8px 16px 6px;border-radius:4px}
h1{margin:22px 64px 0;font-family:SS;font-weight:700;font-size:${it.foto?72:76}px;line-height:1.08;letter-spacing:-.01em}
h1 em{font-style:normal;background:linear-gradient(transparent 62%,rgba(0,173,238,.35) 62%)}
.deck{margin:20px 64px 0;font-size:30px;line-height:1.35;opacity:.82}
.photo{position:absolute;left:64px;right:64px;bottom:150px;height:600px;border-radius:14px;overflow:hidden;background:#dfe6ee}
.photo img{position:absolute;right:0;top:0;height:100%;width:62%;object-fit:cover;object-position:center 20%}
.photo .cap{position:absolute;left:0;bottom:0;width:38%;padding:0 30px 26px;font-size:21px;line-height:1.3;opacity:.75}
.photo .num{position:absolute;left:30px;top:50%;transform:translateY(-60%);width:36%}
.photo .num b{display:block;font-family:SS;font-weight:700;font-size:var(--nf,92px);white-space:nowrap;line-height:1;color:#112E4A}
.photo .num span{display:block;margin-top:10px;font-size:27px;line-height:1.25;opacity:.85}
.foot{position:absolute;left:0;right:0;bottom:0;height:116px;background:#112E4A;color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 64px}
.foot b{font-weight:500;font-size:30px}
.foot b i{font-style:normal;color:#00ADEE}
.foot span{font-size:20px;opacity:.7;letter-spacing:.06em}
.vis{position:absolute;left:64px;right:64px;bottom:150px;height:540px;border-radius:14px;background:#fff;border:1px solid rgba(17,46,74,.12)}
.tag{position:absolute;right:20px;bottom:14px;font-size:18px;opacity:.55}
.chat{background:#ECE5DD;padding:60px 54px}
.bub{position:relative;display:inline-block;max-width:75%;background:#fff;border-radius:16px;padding:20px 26px 34px;font-size:34px;box-shadow:0 2px 3px rgba(0,0,0,.08)}
.bub span{position:absolute;right:16px;bottom:8px;font-size:18px;opacity:.5}
.seen{margin:16px 6px 40px;font-size:22px;color:#E5484D}
.chat .late{display:block;width:fit-content}
.clock{display:flex;align-items:center;gap:48px;padding:0 70px}
.dial{position:relative;flex:0 0 280px;height:280px;border-radius:50%;border:12px solid #112E4A}
.dial i{position:absolute;left:50%;bottom:50%;transform-origin:50% 100%;background:#112E4A;border-radius:6px}
.dial .h{width:14px;height:80px;margin-left:-7px;transform:rotate(300deg)}
.dial .m{width:9px;height:118px;margin-left:-4.5px;transform:rotate(0deg)}
.dial b{position:absolute;left:50%;top:50%;width:24px;height:24px;margin:-12px;border-radius:50%;background:#E5484D}
.clk-t{font-family:SS;font-weight:700;font-size:120px}
.clock .pill{display:inline-block;margin-top:14px;background:#E5484D;color:#fff;font-size:26px;padding:10px 20px;border-radius:30px}
.cal{display:flex;gap:18px;padding:40px 50px 60px}
.cal .col{flex:1;display:flex;flex-direction:column;gap:14px}
.cal .col b{font-size:26px;font-weight:500;text-align:center;margin-bottom:4px}
.cal .col i{height:56px;border-radius:10px;background:#E8EEF4}
.cal .col i.on{background:linear-gradient(135deg,#00ADEE,#9D66C6)}
.big{display:flex;flex-direction:column;align-items:center;justify-content:center;background:#112E4A;color:#fff}
.big b{font-family:SS;font-weight:700;font-size:220px;line-height:1;background:linear-gradient(90deg,#00ADEE,#C9A6E4);-webkit-background-clip:text;color:transparent}
.salto s{font-family:SS;font-weight:700;font-size:110px;line-height:1;color:rgba(255,255,255,.45);text-decoration-color:#E5484D;text-decoration-thickness:8px}
.big span{font-size:36px;margin-top:10px;opacity:.85}
.list{padding:22px 40px 50px}
.list .row{display:flex;align-items:center;gap:20px;padding:13px 0;border-bottom:1px solid rgba(17,46,74,.1)}
.list .row i{flex:0 0 52px;height:52px;border-radius:50%;background:#E8EEF4;font-style:normal;font-weight:500;font-size:24px;display:flex;align-items:center;justify-content:center}
.list .row b{font-weight:500;font-size:28px;flex:1}
.list .row span{font-size:22px;color:#E5484D}
</style></head><body>
<div class="mast"><div class="brand"><img src="${logo}"><span class="ins">Insights</span></div><span class="ed">Gestão de clínicas</span></div>
<div class="rule"></div><div class="rule2"></div>
<span class="kick">${it.kick}</span>
<h1>${it.h}</h1>
<p class="deck">${it.deck}</p>
${media}
<div class="foot"><b>Assista à apresentação completa <i>→</i></b><span>CONTEÚDO TOLKI</span></div>
</body></html>`;
}

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const it of ITENS) {
    await p.setContent(html(it), { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    await p.evaluate(() => { const d = document.querySelector('.deck').getBoundingClientRect().bottom, m = document.querySelector('.photo,.vis'); if (m) { m.style.top = (d + 30) + 'px'; m.style.height = 'auto'; } });
    const over = await p.evaluate(() => { const h = document.querySelector('.deck').getBoundingClientRect().bottom, m = (document.querySelector('.photo,.vis') || {}).getBoundingClientRect(); return m ? Math.round(m.top - h) : 999; });
    await p.screenshot({ path: path.join(OUT, it.id + '.png') });
    console.log(it.id, 'folga texto/imagem:', over);
  }
  fs.writeFileSync(path.join(OUT, 'itens.json'), JSON.stringify(ITENS.map(i => ({ id: i.id, kick: i.kick, titulo: i.h.replace(/<[^>]+>/g, '') })), null, 1));
  await b.close();
})();
