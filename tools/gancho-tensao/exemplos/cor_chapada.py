"""Estilo COR CHAPADA: fundo inteiro muda por cena, tipografia gigante, cortes secos na voz, sem rastro de luz e sem fundo escuro fixo."""
MF = 'assets/montserrat-900.woff2'
CSS = r'''
@font-face{font-family:'Montserrat';font-weight:900;src:url('__MF__') format('woff2')}
#bgP,#bgW{position:absolute;inset:0;z-index:-1}
.ab.sans{font-family:'Montserrat';font-weight:900;letter-spacing:-.025em;line-height:1;white-space:nowrap}
#cap{font-family:'Montserrat';font-weight:900;font-size:40px;letter-spacing:-.01em}
.nv{color:#0E1A2B!important}.rx{color:#7A32C4!important}.az{color:#1597D4!important}
#spl{position:absolute;left:0;top:960px;width:1080px;height:960px;background:#F1ECE2}
#x1a{top:430px;font-size:84px}#x1b{top:530px;font-size:124px}#x1c{top:1060px;font-size:84px}#x1d{top:1160px;font-size:124px}
#x2a{top:330px;font-size:128px}#x2b{top:450px;font-size:520px;letter-spacing:-.05em}
#x2c{position:absolute;left:150px;top:1080px;width:780px;background:#fff;border-radius:20px;padding:30px 40px;transform-origin:50% 50%;text-align:center}
#x2c b{display:block;font-family:'Montserrat';font-weight:900;font-size:62px;color:#0E1A2B;letter-spacing:-.02em}#x2c small{font-family:'Instrument Serif';font-style:italic;font-size:50px;color:#1597D4}
#x2e{top:1340px;font-size:24px;letter-spacing:5px;color:#fff}
#x3a{top:320px;font-size:84px}#x3b{top:420px;font-size:124px}
#brs{position:absolute;left:70px;right:70px;top:720px;height:800px;display:flex;align-items:flex-end;gap:16px}#brs i{flex:1;background:#7A32C4;transform-origin:50% 100%}
.bbl{position:absolute;background:#fff;border-radius:34px;padding:30px 42px;font-family:'Inter';font-weight:600;font-size:60px;color:#0E1A2B;box-shadow:10px 10px 0 #0E1A2B}
#b1{left:70px;top:330px}#b2{right:70px;top:590px}#b3{left:70px;top:850px}
.stp{position:absolute;font-family:'Montserrat';font-weight:900;font-size:58px;color:#fff;background:#7A32C4;padding:12px 26px;border-radius:12px}
#t1{left:640px;top:370px;rotate:-7deg}#t2{left:120px;top:640px;rotate:5deg}#t3{left:660px;top:900px;rotate:-5deg}
#x3f{top:1200px;font-size:96px}
#x4a{top:540px;font-size:136px}#x4b{top:700px;font-size:136px}#x4c{top:860px;font-size:136px}
#x4d{top:600px;font-size:200px}#x4e{top:810px;font-size:200px}
#x4f{top:350px;font-size:128px}#x4g{top:490px;font-size:470px;letter-spacing:-.04em}#x4h{top:1040px;font-size:112px}
#x5l{position:absolute;left:190px;top:470px;width:700px}#x5a{top:800px;font-size:164px}#x5b{top:990px;font-size:104px}
#x5h{top:290px;font-size:66px}
.ln{position:absolute;left:0;width:1080px;height:230px;display:flex;align-items:center;justify-content:space-between;padding:0 64px;font-family:'Montserrat';font-weight:900;font-size:56px;letter-spacing:-.02em;color:#0E1A2B;background:#E4E0D7}
.ln span:last-child{font-size:50px}
#l1{top:420px}#l2{top:680px}#l3{top:940px}
#x5e{top:1200px;font-size:24px;letter-spacing:5px;color:#0E1A2B}
#x6p{top:800px;font-size:220px}#x6a{top:330px;font-size:112px}#x6b{top:430px;font-size:760px;letter-spacing:-.05em}#x6c{top:1260px;font-size:140px}
#h9a{top:520px;font-size:180px}
#inp{position:absolute;left:110px;top:770px;width:860px;height:190px;border-radius:95px;background:#fff;display:flex;align-items:center;padding:0 54px}
#inp span{font-family:'Montserrat';font-weight:900;font-size:96px;color:#0E1A2B}
#inp em{display:inline-block;width:6px;height:96px;background:#7A32C4;margin-left:10px}#inp svg{margin-left:auto}#inp svg path{fill:#7A32C4}
#h9b{top:1030px;font-size:76px}
'''.replace('__MF__', MF)
BODY = '''<div id="bgP"></div><div id="bgW"></div>
<div class="sc" id="sA"><div id="x1a" class="ab ser">sua agência diz:</div><div id="x1b" class="ab sans">anúncio ótimo.</div><div id="spl"></div><div id="x1c" class="ab ser nv">sua recepção diz:</div><div id="x1d" class="ab sans rx">paciente ruim.</div></div>
<div class="sc" id="sB"><div id="x2a" class="ab sans">segunda</div><div id="x2b" class="ab sans">9h</div><div id="x2c"><b>DOUTORA PAULA</b><small>ouviu as duas</small></div><div id="x2e" class="ab mono">HISTÓRIA ILUSTRATIVA</div></div>
<div class="sc" id="sC"><div id="x3a" class="ab ser nv">o relatório tava</div><div id="x3b" class="ab sans nv">cheio de<br>conversa</div><div id="brs"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div></div>
<div class="sc" id="sD"><div class="bbl" id="b1">Oi, quanto custa?</div><div class="bbl" id="b2">Qual o valor?</div><div class="bbl" id="b3">Me passa o preço?</div><div class="stp" id="t1">SUMIU</div><div class="stp" id="t2">SUMIU</div><div class="stp" id="t3">SUMIU</div><div id="x3f" class="ab sans nv">antes de marcar.</div></div>
<div class="sc" id="sE"><div id="x4a" class="ab sans">quem marcou</div><div id="x4b" class="ab sans">veio de</div><div id="x4c" class="ab sans az">qual anúncio?</div></div>
<div class="sc" id="sF"><div id="x4d" class="ab sans">ninguém</div><div id="x4e" class="ab sans">sabia.</div></div>
<div class="sc" id="sG"><div id="x4f" class="ab sans nv">até sexta</div><div id="x4g" class="ab sans az">R$ ?</div><div id="x4h" class="ab sans nv">na black friday</div></div>
<div class="sc" id="sH"><img id="x5l" src="assets/logo_light.png"><div id="x5a" class="ab sans">responde</div><div id="x5b" class="ab ser">no WhatsApp</div></div>
<div class="sc" id="sI"><div id="x5h" class="ab sans nv">e mostra de onde veio</div><div class="ln" id="l1"><span>ANÚNCIO A</span><span id="r1">PERGUNTOU</span></div><div class="ln" id="l2"><span>ANÚNCIO B</span><span id="r2">AGENDOU</span></div><div class="ln" id="l3"><span>ANÚNCIO C</span><span id="r3">PERGUNTOU</span></div><div id="x5e" class="ab mono">EXEMPLO ILUSTRATIVO</div></div>
<div class="sc" id="sJ"><div id="x6p" class="ab sans nv">pronto.</div><div id="x6a" class="ab ser nv">reunião de</div><div id="x6b" class="ab sans rx">10</div><div id="x6c" class="ab sans nv">minutos.</div></div>
'''
JS = r'''
document.fonts.load('900 100px Montserrat');
$('h9b').textContent='que a gente te mostra funcionando.'; $('tag').style.display='none'; $('hgc').style.display='none';
const RX='#7A32C4',AZ='#1597D4',BR='#FFFFFF',CR='#F1ECE2',PT='#000000',NV='#0E1A2B';
const tW3=TW(3,'WhatsApp')-.28, tN=TW(4,'Ninguém')-.05, tA=TW(4,'até')-.05, tM=TW(5,'mostra')-.05;
const CUTS=[[-1,RX,'#fff','#F1E6FB'],[LS(2),AZ,'#fff',NV],[LS(3),BR,NV,RX],[tW3,CR,NV,RX],[LS(4),PT,'#fff',AZ],[tN,RX,'#fff','#F1E6FB'],[tA,BR,NV,AZ],[LS(5),RX,'#fff','#F1E6FB'],[tM,BR,NV,AZ],[LS(6),CR,NV,RX],[LS(7),AZ,'#fff',NV],[ENDT,RX,'#fff','#fff']];
const SC=[['sA',-1,LS(2)],['sB',LS(2),LS(3)],['sC',LS(3),tW3],['sD',tW3,LS(4)],['sE',LS(4),tN],['sF',tN,tA],['sG',tA,LS(5)],['sH',LS(5),tM],['sI',tM,LS(6)],['sJ',LS(6),LS(7)],['sCTA',LS(7),ENDT]];
const slam=(el,t,t0,d=.2,s=1.3)=>{const k=oQ(P(t,t0,t0+d)); el.style.opacity=t>=t0?1:0; el.style.transform=`scale(${lerp(s,1,k)})`;};
const inL=(el,t,t0,d=.22)=>{const k=oQ(P(t,t0,t0+d)); el.style.opacity=t>=t0?1:0; el.style.transform=`translateX(${(1-k)*-1080}px)`;};
const up=(el,t,t0,d=.22,dist=240)=>{const k=oQ(P(t,t0,t0+d)); el.style.opacity=t>=t0?1:0; el.style.transform=`translateY(${(1-k)*dist}px)`;};
function bgs(t){let i=0; CUTS.forEach((c,j)=>{if(t>=c[0])i=j}); const c=CUTS[i],p=CUTS[Math.max(0,i-1)]; const k=oQ(P(t,c[0],c[0]+.16)); $('bgP').style.background=p[1]; const W=$('bgW'); W.style.background=c[1];
  W.style.transform=i%2?`translateX(${(1-k)*100}%)`:`translateY(${(1-k)*100}%)`; return c;}
function inks(t,c){let ink=c[2],acc=c[3]; if(t>=TW(1,'recepção')-.3&&t<LS(2)){ink=NV;acc=RX} const C=$('cap'); C.style.color=ink; qa('span.on',C).forEach(s=>s.style.color=acc); $('wm').style.color=t<LS(2)||c[2]==='#fff'?'#fff':NV;}
window.bgAt=t=>({show:0,src:0,blur:0,dim:1,scale:1});
const CL=F('ui_blip/kint__click_002.ogg'), BM=F('boom/kimp__impactSoft_heavy_000.ogg');
[TW(1,'recepção')-.28,LS(2),LS(3),tW3,LS(4),tN,tA,LS(5),tM,LS(6),LS(7)].forEach(x=>cue(x,CL,{g:.35}));
[0,1,2].forEach(i=>cue(TW(3,'sumiu')+i*.13,CL,{g:.45}));
cue(TW(1,'ruim'),BM,{g:.4}); cue(tN,BM,{g:.45}); cue(TW(5,'agendou'),CL,{g:.45}); cue(TW(5,'apareceu'),CL,{g:.45}); cue(TW(6,'dez'),F('boom/ksci__lowFrequency_explosion_001.ogg'),{g:.5});
function render(t){
  scenes(t,SC,[]); const c=bgs(t);
  if(t<LS(2)){ up($('x1a'),t,-.1); slam($('x1b'),t,.05); const a=TW(1,'recepção')-.3,k=oQ(P(t,a,a+.22)); $('spl').style.transform=`translateY(${(1-k)*960}px)`; up($('x1c'),t,a+.08); slam($('x1d'),t,TW(1,'paciente')-.05);
    const r=TW(1,'ruim'); if(t>=r){const [x,y]=shake(t,r,12,.28); $('x1d').style.translate=`${x}px ${y}px`;}}
  if(t>=LS(2)&&t<LS(3)){ slam($('x2a'),t,LS(2)); slam($('x2b'),t,TW(2,'nove'),.22,1.5); up($('x2c'),t,TW(2,'doutora')-.05); $('x2c').style.rotate='-3deg'; $('x2e').style.opacity=t>=TW(2,'doutora')?1:0;}
  if(t>=LS(3)&&t<tW3){ up($('x3a'),t,LS(3)); slam($('x3b'),t,TW(3,'cheio')-.05); qa('#brs i').forEach((b,i)=>{b.style.height=(22+i*11)+'%'; b.style.transform=`scaleY(${oQ(P(t,TW(3,'cheio')+i*.07,TW(3,'cheio')+.3+i*.07))})`;});}
  if(t>=tW3&&t<LS(4)){ slam($('b1'),t,TW(3,'gente')-.1,.18,.7); slam($('b2'),t,TW(3,'perguntou'),.18,.7); slam($('b3'),t,TW(3,'preço'),.18,.7); const s=TW(3,'sumiu'); slam($('t1'),t,s,.14,1.8); slam($('t2'),t,s+.13,.14,1.8); slam($('t3'),t,s+.26,.14,1.8); up($('x3f'),t,TW(3,'antes')-.05);}
  if(t>=LS(4)&&t<tN){ slam($('x4a'),t,LS(4)); slam($('x4b'),t,TW(4,'veio')-.05); slam($('x4c'),t,TW(4,'qual')-.05);}
  if(t>=tN&&t<tA){ slam($('x4d'),t,tN,.2,1.5); slam($('x4e'),t,TW(4,'sabia')-.05,.2,1.5); const r=TW(4,'sabia'); if(t>=r){const [x,y]=shake(t,r,10,.25); $('x4e').style.translate=`${x}px ${y}px`;}}
  if(t>=tA&&t<LS(5)){ slam($('x4f'),t,tA); slam($('x4g'),t,TW(4,'decide')-.05,.22,1.5); up($('x4h'),t,TW(4,'Black')-.1);}
  if(t>=LS(5)&&t<tM){ slam($('x5l'),t,LS(5),.22,.8); slam($('x5a'),t,TW(5,'responde')-.05); up($('x5b'),t,TW(5,'WhatsApp')-.1);}
  if(t>=tM&&t<LS(6)){ const q=TW(5,'qual'); up($('x5h'),t,tM); inL($('l1'),t,q-.2); inL($('l2'),t,q); inL($('l3'),t,q+.2); const v=TW(5,'veio'),a=TW(5,'agendou'),p=TW(5,'apareceu'); $('r1').style.opacity=$('r3').style.opacity=t>=v?1:0; $('r2').style.opacity=t>=a?1:0; const L=$('l2'); L.style.background=t>=a?AZ:'#E4E0D7'; L.style.color=t>=a?'#fff':NV; $('r2').textContent=t>=p?'APARECEU':'AGENDOU'; if(t>=p)L.style.background=RX; $('x5e').style.opacity=t>=v?1:0;}
  if(t>=LS(6)&&t<LS(7)){ const a=TW(6,'Reunião')-.05; $('x6p').style.opacity=t<a?1:0; if(t<a)slam($('x6p'),t,LS(6),.18,1.5); slam($('x6a'),t,a); slam($('x6b'),t,TW(6,'dez')-.05,.2,1.5); slam($('x6c'),t,TW(6,'minutos')-.05);}
  ctaEnd(t,'ANÚNCIO'); captions(t); inks(t,c);
}
'''
