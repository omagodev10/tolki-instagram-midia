"""N34 (02/11, pedido do Carlos): a N1 no modelo caixinha de perguntas, 9:16 com a voz da Luana. Prova Odonto Excellence, conversa com exemplo ilustrativo."""
CSS = r'''
#stage{background:#061420}#hgc,#wm,#end,#tag{display:none!important}
#bgf{position:absolute;inset:0;background:radial-gradient(900px 700px at 50% 42%,#123a57 0%,#0a2234 55%,#061420 100%)}
#cap{left:0;width:1080px;top:1205px;padding:0 130px;text-align:center;font-family:'Inter Tight';font-weight:700;font-size:44px;line-height:1.42;color:#fff}
#cap span{background:rgba(0,0,0,.72);padding:2px 11px;margin:0;border-radius:6px}#cap span.on{color:#FFD400}
#qb{position:absolute;left:130px;top:285px;width:820px;border-radius:26px;overflow:hidden;box-shadow:0 14px 40px rgba(0,0,0,.45)}
#qb .h{background:#262626;color:#fff;font-family:Inter;font-size:30px;text-align:center;padding:18px}
#qb .t{background:#fff;color:#111;font-family:Inter;font-size:50px;line-height:1.24;text-align:center;padding:34px 42px;font-weight:500}
.b{position:absolute;left:96px;width:888px}
.h1{font-family:'Inter Tight';font-weight:800;font-size:96px;line-height:1.04;letter-spacing:-.03em;color:#fff}
.h2{font-family:'Instrument Serif';font-style:italic;font-size:82px;line-height:1.08;color:#8FD3F4}
#e1{top:720px}#e2{top:930px}
.bu{position:absolute;font-family:Inter;font-weight:700;font-size:52px;padding:22px 32px;border-radius:26px}
#u1{left:96px;top:690px;background:#fff;color:#111}#u2{right:96px;top:830px;background:#0E7A5F;color:#fff}#u3{left:96px;top:980px;color:#FFD400;font-family:'JetBrains Mono';font-size:36px;padding:0}
#ex{top:1120px;font-family:'JetBrains Mono';font-weight:700;font-size:22px;letter-spacing:3px;color:#cfd8df}
#pc{position:absolute;left:96px;top:680px;width:888px;background:#fff;border-radius:34px;padding:44px 40px;text-align:center}
#pn{font-family:'Inter Tight';font-weight:800;font-size:168px;letter-spacing:-.04em;color:#0B7FC4;line-height:1}
#pa{font-family:'Inter Tight';font-weight:800;font-size:44px;color:#111;margin-top:12px}#pb{font-family:'JetBrains Mono';font-weight:700;font-size:22px;letter-spacing:3px;color:#667;margin-top:14px}
#ls{top:700px;display:grid;grid-template-columns:repeat(6,1fr);gap:12px}.lt{height:150px;background:#fff;color:#0B2239;font-family:'Inter Tight';font-weight:800;font-size:96px;display:flex;align-items:center;justify-content:center;border-radius:14px}
#m2{top:890px}
#cA{top:680px}#cP{top:800px;font-family:'Inter Tight';font-weight:800;font-size:190px;color:#FFD400;letter-spacing:-.04em;line-height:1}
#cB{top:1020px;left:96px;width:auto;background:#fff;color:#111;font-family:'Inter Tight';font-weight:800;font-size:58px;padding:24px 46px;border-radius:60px}
'''
BODY = '''<div id="bgf"></div><div id="qb"><div class="h">Faça uma pergunta</div><div class="t">Passo o preço no WhatsApp e o paciente some. É normal?</div></div>
<div class="sc" id="a1"><div class="b h1" id="e1">É comum, mas não é normal.</div></div>
<div class="sc" id="a2"><div class="bu" id="u1">Quanto custa?</div><div class="bu" id="u2">R$ 900.</div><div class="bu" id="u3">visualizou e sumiu</div><div class="b" id="ex">EXEMPLO ILUSTRATIVO</div></div>
<div class="sc" id="a3"><div id="pc"><div id="pn">15%</div><div id="pa">de agendamento na Odonto Excellence</div><div id="pb">CASO REAL · ATENDIMENTO COM A TOLKI</div></div></div>
<div class="sc" id="a4"><div class="b" id="ls"><div class="lt">A</div><div class="lt">G</div><div class="lt">E</div><div class="lt">N</div><div class="lt">D</div><div class="lt">A</div></div><div class="b h2" id="m2">o que responder, com as mensagens prontas</div></div>
<div class="sc" id="a5"><div class="b h1" id="cA">Aula de 10 minutos</div><div class="b" id="cP">R$ 47</div><div class="b" id="cB">Clique no botão abaixo</div></div>
'''
JS = r'''
window.bgAt=t=>({show:false,src:0,scale:1,blur:0,dim:0});
const SC=[['a1',0,LS(2)],['a2',LS(2),LS(3)],['a3',LS(3),LS(4)],['a4',LS(4),LS(5)],['a5',LS(5),99]];
const T45=TW(3,'quarenta'),LT=qa('.lt');
cue(TW(2,'quanto'),'tick',{g:.35,f:1100});cue(TW(2,'preço'),'tick',{g:.35,f:1100});cue(T45,'tick',{g:.5,f:1600});LT.forEach((e,i)=>cue(TW(4,'agenda')+i*.08,'tick',{g:.22,f:1200+i*80}));cue(TW(5,'quarenta'),'tick',{g:.45,f:1500});
const rs=(id,t,t0,dist=46)=>{const e=$(id),k=oQ(P(t,t0,t0+.45));e.style.opacity=clamp(k*1.6);e.style.transform=`translateY(${(1-k)*dist}px)`};
const pp=(id,t,t0)=>{const e=$(id),k=P(t,t0,t0+.32);e.style.opacity=clamp(k*3);e.style.transform=`scale(${k>0?oB(k,1.4):.7})`};
function render(t){SC.forEach(([id,a,b])=>{$(id).style.display=(t>=a&&t<b)?'block':'none'});captions(t);
 pp('qb',t,0);rs('e1',t,.1);
 pp('u1',t,TW(2,'quanto')-.1);pp('u2',t,TW(2,'preço')-.1);rs('u3',t,TW(2,'vai')-.05,20);rs('ex',t,LS(2));
 pp('pc',t,LS(3)+.1);const k=oC(P(t,T45,T45+.7));$('pn').textContent=Math.round(lerp(15,45,k))+'%';
 LT.forEach((e,i)=>{const a=TW(4,'agenda')+i*.08,q=P(t,a,a+.3);e.style.opacity=clamp(q*3);e.style.transform=`scale(${q>0?oB(q,1.5):.6})`});rs('m2',t,TW(4,'responder')-.1);
 rs('cA',t,LS(5));pp('cP',t,TW(5,'quarenta')-.1);pp('cB',t,TW(5,'clica')-.1);}
'''
