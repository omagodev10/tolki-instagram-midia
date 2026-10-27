// v2 dos estáticos editoriais (27/10/2026, pedido do Carlos): só tipografia, sem foto de cliente.
// Linha da referência dele: cabeçalho de publicação, faixa de seção, rótulo vermelho, manchete grande em sans pesada,
// linha fina em serifa itálica, rodapé com rótulo mono e botão pílula preto.
// Regras: sem preço, sem travessão, só provas liberadas, "conteúdo de marca" assumido (nada imitando veículo real).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const OUT = process.argv[2] || 'out2';
fs.mkdirSync(OUT, { recursive: true });
const b64 = f => fs.readFileSync(f).toString('base64');
const font = f => `url(data:font/woff2;base64,${b64(f)}) format('woff2')`;
const SS = 'node_modules/@fontsource/source-serif-4/files/source-serif-4-latin-';
const JB = 'node_modules/@fontsource/jetbrains-mono/files/jetbrains-mono-latin-';

const ITENS = [
  { id: 'N01_edson_15_45', sec: ['ATENDIMENTO', 'WHATSAPP'], kick: 'CASO REAL · ATENDIMENTO COM A TOLKI',
    h: 'Mesmo WhatsApp, mesma clínica: de <span class="hl">15% para 45%</span> de agendamento',
    deck: 'A Odonto Excellence mudou o jeito de responder o paciente no WhatsApp. O dono conta o que fez.' },
  { id: 'N02_fabio_62', sec: ['ORTODONTIA', 'RECORDE'], kick: 'CASO REAL · ATENDIMENTO COM A TOLKI',
    h: '<span class="hl">62 contratos novos</span> em um mês e recorde da franquia',
    deck: 'A OrthoDontic foi de 59 para 121 contratos e passou a responder cada paciente no WhatsApp com a Tolki.' },
  { id: 'N03_luis_dobrou', sec: ['BASE DE PACIENTES', 'DISPARO'], kick: 'CASO REAL · BASE DE PACIENTES',
    h: 'Um disparo para pacientes antigos e a agenda <span class="hl">dobrou</span>',
    deck: 'A Gou Odonto voltou a falar com quem já era paciente. Os agendamentos dobraram no primeiro disparo.' },
  { id: 'N04_victor_60mil', sec: ['CUSTOS', 'WHATSAPP'], kick: 'CASO REAL · CUSTO DE MENSAGENS',
    h: '<span class="hl">R$ 60 mil</span> a menos em mensagens de WhatsApp em seis meses',
    deck: 'O Instituto Victor Santos enviou 200 mil mensagens no período e mudou o tipo de mensagem que usa.' },
  { id: 'N05_felipe_38', sec: ['AGENDA', 'TRÁFEGO'], kick: 'CASO REAL · ATENDIMENTO COM A TOLKI',
    h: '<span class="hl">+38% de agendamentos</span> em 10 meses na mesma clínica',
    deck: 'Mais agendamento e um tráfego de melhor qualidade, segundo o Dr. Felipe Mafra, da Dental Clinic.' },
  { id: 'N06_preco_e_some', sec: ['ATENDIMENTO', 'WHATSAPP'], kick: 'CURIOSIDADE · ATENDIMENTO',
    h: 'Por que o paciente pergunta o preço e <span class="hl">some?</span>',
    deck: 'O problema quase nunca é o valor. As clínicas que agendam fazem uma coisa diferente na primeira resposta.' },
  { id: 'N07_horario', sec: ['ATENDIMENTO', 'HORÁRIO'], kick: 'CURIOSIDADE · ATENDIMENTO',
    h: 'O horário em que a clínica mais perde paciente <span class="hl">não é o que você imagina</span>',
    deck: 'E é justamente quando quase nenhuma recepção está lá para responder.' },
  { id: 'N08_metodo_30mil', sec: ['MÉTODO', 'AGENDA'], kick: 'MÉTODO · CLÍNICAS ACIMA DE R$ 30 MIL/MÊS',
    h: 'O método para <span class="hl">triplicar a taxa de agendamento</span> sem gastar mais em anúncio',
    deck: 'O mesmo que clínicas acima de R$ 30 mil por mês usam. A apresentação completa tem menos de 5 minutos.' },
  { id: 'N09_470_clinicas', sec: ['TENDÊNCIA', 'IA'], kick: 'TENDÊNCIA · IA NO ATENDIMENTO',
    h: '<span class="hl">+470 clínicas</span> já colocaram IA para responder o WhatsApp',
    deck: 'Resposta em segundos, 24 horas por dia, inclusive no fim de semana. O que elas descobriram.' },
  { id: 'N10_base_parada', sec: ['BASE DE PACIENTES', 'WHATSAPP'], kick: 'CURIOSIDADE · BASE DE PACIENTES',
    h: 'A lista de pacientes parada no seu WhatsApp vale mais que o <span class="hl">próximo anúncio</span>',
    deck: 'Clínicas estão enchendo a agenda com quem já foi paciente, sem aumentar o tráfego.' },
];

function html(it) {
  return `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:SS;font-weight:600;src:${font(SS+'600-normal.woff2')}}
@font-face{font-family:SS;font-style:italic;font-weight:400;src:${font(SS+'400-italic.woff2')}}
@font-face{font-family:JB;font-weight:500;src:${font(JB+'500-normal.woff2')}}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;background:#F5F1E8;color:#141414;overflow:hidden;position:relative;font-family:Inter}
.wrap{position:absolute;inset:0;padding:70px 76px 0}
.mast{display:flex;align-items:flex-end;justify-content:space-between;padding-bottom:22px;border-bottom:3px solid #141414}
.mast b{font-family:SS;font-weight:600;font-size:58px;letter-spacing:-.01em;line-height:1}
.mast span{font-family:JB;font-weight:500;font-size:19px;letter-spacing:.18em;color:#555;padding-bottom:6px}
.sec{display:flex;justify-content:space-between;padding:16px 0;border-bottom:1px solid #b9b2a4;font-family:JB;font-weight:500;font-size:18px;letter-spacing:.2em;color:#555}
.kick{margin-top:56px;font-family:JB;font-weight:500;font-size:21px;letter-spacing:.14em;color:#D93A2B}
h1{margin-top:22px;font-family:Inter;font-weight:800;font-size:var(--fs,96px);line-height:1.02;letter-spacing:-.035em}
h1 .hl{background:linear-gradient(transparent 70%,rgba(0,173,238,.35) 70%)}
.deck{margin-top:34px;font-family:SS;font-style:italic;font-size:40px;line-height:1.32;color:#3d3d3d;max-width:900px}
.foot{position:absolute;left:76px;right:76px;bottom:70px;display:flex;align-items:center;justify-content:space-between;padding-top:30px;border-top:1px solid #b9b2a4}
.foot span{font-family:JB;font-weight:500;font-size:19px;letter-spacing:.2em;color:#333}
.foot b{display:inline-flex;align-items:center;gap:14px;background:#141414;color:#fff;font-family:Inter;font-weight:700;font-size:28px;padding:22px 40px;border-radius:60px}
.foot b i{font-style:normal;color:#00ADEE}
.brand{position:absolute;right:76px;top:76px}
</style></head><body><div class="wrap">
<div class="mast"><b>Gestão de Clínicas</b><span>CONTEÚDO DE MARCA · TOLKI</span></div>
<div class="sec"><span>${it.sec[0]}</span><span>${it.sec[1]}</span></div>
<div class="kick">${it.kick}</div>
<h1>${it.h}</h1>
<p class="deck">${it.deck}</p>
<div class="foot"><span>APRESENTAÇÃO · MENOS DE 5 MIN</span><b>Assistir <i>→</i></b></div>
</div></body></html>`;
}

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const it of ITENS) {
    await p.setContent(html(it), { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    // encolhe a manchete até o texto inteiro caber acima do rodapé, com folga
    const fs_ = await p.evaluate(() => {
      const h = document.querySelector('h1'), d = document.querySelector('.deck'), f = document.querySelector('.foot');
      let s = 132;
      while (s > 60) { h.style.setProperty('--fs', s + 'px'); if (d.getBoundingClientRect().bottom < f.getBoundingClientRect().top - 60) break; s -= 2; }
      return s;
    });
    await p.screenshot({ path: path.join(OUT, it.id + '.png') });
    console.log(it.id, 'manchete', fs_ + 'px');
  }
  await b.close();
})();
