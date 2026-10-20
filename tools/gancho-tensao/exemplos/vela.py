"""Vela: gancho FILMADO (Seedance 6 s, chama quase apagando). Copy da base parada. Prova Gou Odonto. CTA BASE."""
CSS = r'''
#a3a{top:420px;font-size:100px}#a3b{top:520px;font-size:150px}#a3c{top:690px;font-size:90px}
#a4c1{top:720px}#a4c2{top:930px}
#a5a{top:420px;font-size:170px}#a5b{top:590px;font-size:170px}
#a6a{top:470px;font-size:96px}#a6b{top:575px;font-size:112px;color:var(--gr)}#a6k{top:648px}#a6c{top:770px;font-size:210px}#a6d{top:1010px;font-size:78px}
#a7logo{position:absolute;left:280px;top:400px;width:520px}
.rowX{position:absolute;left:110px;width:860px;height:140px;border-radius:28px;border:2px solid var(--line);background:var(--card);display:flex;align-items:center;padding:0 38px;gap:22px}
.rowX .nm{font-family:'Inter Tight';font-weight:800;font-size:40px;color:var(--wh);text-transform:uppercase}
.rowX .ty{font-family:'Inter Tight';font-weight:600;font-size:30px;color:var(--gr)}
.rowX .st{margin-left:auto;font-family:'JetBrains Mono';font-weight:700;font-size:24px;letter-spacing:1px}
#a7ex{left:0;width:1080px;text-align:center;top:1155px}
#a8logo{position:absolute;left:240px;top:470px;width:600px;height:190px;background:#fff;border-radius:28px;display:flex;align-items:center;justify-content:center}
#a8logo img{max-width:78%;max-height:72%}
#a8a{top:720px;font-size:92px}#a8b{top:810px;font-size:120px}#a8c{top:930px;font-size:420px;line-height:1;text-transform:none;letter-spacing:-.05em}#a8d{top:1360px;font-size:36px;letter-spacing:8px;color:var(--cy)}
#h9a{top:560px;font-size:180px}
#inp{position:absolute;left:110px;top:800px;width:860px;height:170px;border-radius:85px;background:var(--card);border:3px solid var(--cy);display:flex;align-items:center;padding:0 50px}
#inp span{font-family:'Inter Tight';font-weight:800;font-size:96px;color:var(--wh);letter-spacing:.02em}
#inp em{display:inline-block;width:6px;height:96px;background:var(--cy);margin-left:10px}
#inp svg{margin-left:auto}
#h9b{top:1040px;font-size:84px}
'''
BODY = '''<div class="sc" id="sA3"><div id="a3a" class="ab ser">tua base de</div><div id="a3b" class="ab sans">pacientes</div><div id="a3c" class="ab ser">está assim.</div></div>
<div class="sc" id="sA4"><div class="chipX" id="a4c1"><b>FEZ AVALIAÇÃO</b><i id="a4i1">SUMIU</i></div><div class="chipX" id="a4c2"><b>PERGUNTOU O PREÇO</b><i id="a4i2">NÃO VOLTOU</i></div></div>
<div class="sc" id="sA5"><div id="a5a" class="ab sans">ninguém</div><div id="a5b" class="ab sans cy">chama.</div></div>
<div class="sc" id="sA6"><div id="a6a" class="ab ser">isso não é</div><div id="a6b" class="ab sans">lista de contato</div><div class="strk2" id="a6k"></div><div id="a6c" class="ab sans cy">é agenda</div><div id="a6d" class="ab ser">esperando alguém chamar.</div></div>
<div class="sc" id="sA7"><img id="a7logo" src="assets/logo_light.png">
 <div class="rowX" id="r1" style="top:640px"><span class="nm">Mariana</span><span class="ty">avaliação</span><span class="st"></span></div>
 <div class="rowX" id="r2" style="top:800px"><span class="nm">Carlos</span><span class="ty">orçamento</span><span class="st"></span></div>
 <div class="rowX" id="r3" style="top:960px"><span class="nm">Ana</span><span class="ty">retorno</span><span class="st"></span></div>
 <div class="lab" id="a7ex">EXEMPLO ILUSTRATIVO</div></div>
<div class="sc" id="sA8"><div id="a8logo"><img src="assets/cl_gou.png"></div><div id="a8a" class="ab ser">dobrou os</div><div id="a8b" class="ab sans">agendamentos</div><div id="a8c" class="ab sans cy">2x</div><div id="a8d" class="ab mono">NO PRIMEIRO DISPARO</div></div>
'''
JS = r'''
const RELIT=TW(7,'marca');
const SC=[['s0h',0,HOOK],['s0',HOOK,LS(2)],['s1',LS(2),LS(3)],['sA3',LS(3),LS(4)],['sA4',LS(4),LS(5)],['sA5',LS(5),LS(6)],['sA6',LS(6),LS(7)],['sA7',LS(7),LS(8)],['sA8',LS(8),LS(9)],['sCTA',LS(9),ENDT]];
const TAGS=[[0,''],[LS(3),'TUA BASE HOJE'],[LS(5),''],[LS(7),'COM A TOLKI'],[LS(8),'RESULTADO REAL · CLIENTE TOLKI'],[LS(9),'']];
const C3=SW(TW(3,'pacientes')-.05,600,.55), C6=SW(TW(6,'contato')+.15,690,.5,140,940), C6b=SW(TW(6,'agenda')-.08,880,.55);
CMp(TW(8,'dobrou')-.1,.9,k=>[lerp(200,880,iO(k)),lerp(1260,980,oC(k))]);
CMp(TW(9,'base')+.45,.7,k=>[lerp(130,960,iO(k)),1000]);
// line-art candle
function candleAt(t){return KF([[0,{cx:540,cy:1060,s:1,a:0,b:0}],[LS(3)-.05,{cx:540,cy:1060,s:1,a:0,b:0}],[LS(3)+.3,{cx:540,cy:1060,s:1,a:1,b:0}],[LS(4)-.1,{cx:540,cy:1060,s:1,a:1,b:0}],
  [LS(4)+.4,{cx:540,cy:1100,s:1.25,a:.12,b:8}],[LS(5)-.1,{cx:540,cy:1100,s:1.25,a:.12,b:8}],[LS(5)+.4,{cx:540,cy:1010,s:1,a:1,b:0}],[LS(6)-.1,{cx:540,cy:1010,s:1,a:1,b:0}],
  [LS(6)+.4,{cx:540,cy:1100,s:1.25,a:.1,b:9}],[LS(7)-.1,{cx:540,cy:1100,s:1.25,a:.1,b:9}],[LS(7)+.4,{cx:540,cy:1330,s:.42,a:1,b:0}],[LS(8)-.1,{cx:540,cy:1330,s:.42,a:1,b:0}],[LS(8)+.4,{cx:540,cy:1100,s:1.3,a:.08,b:10}],[DUR,{cx:540,cy:1100,s:1.3,a:.08,b:10}]],t);}
function flameAt(t){ // 1 = normal, shrinks while nobody calls, relights with Tolki
  if(t<TW(5,'e')) return 1; if(t<RELIT) return lerp(1,.16,oC(P(t,TW(5,'e'),LE(5)+.3)));
  return lerp(.16,1.35,oB(P(t,RELIT,RELIT+.5),1.4));}
function drawArt(t){
  const c=hctx; c.clearRect(0,0,1080,1920); if(t>=HOOK) dust(c,t);
  const g=candleAt(t); $('hgc').style.filter=g.b>.3?`blur(${g.b}px)`:''; if(g.a<.01) return;
  const S=g.s, cx=g.cx, top=g.cy+40*S, Wd=230*S, Hb=430*S, N=54, SEG=8;
  c.save(); c.globalAlpha=g.a;
  for(let i=0;i<N;i++){const u=i/(N-1)*2-1; const x=cx+u*Wd/2; const br=Math.pow(1-Math.abs(u),.6); const y0=top+Wd*.06*Math.sqrt(1-u*u);
    for(let k=0;k<SEG;k++){const fa=1-k/SEG; c.strokeStyle=`rgba(236,244,250,${(.05+.3*br)*fa})`; c.lineWidth=1.1; c.beginPath(); c.moveTo(x,lerp(y0,top+Hb,k/SEG)); c.lineTo(x,lerp(y0,top+Hb,(k+1)/SEG)); c.stroke();}}
  [-1,1].forEach(sd=>{for(let k=0;k<SEG;k++){c.strokeStyle=`rgba(245,250,255,${.95*(1-k/SEG)})`; c.lineWidth=2.2; c.beginPath(); c.moveTo(cx+sd*Wd/2,lerp(top,top+Hb,k/SEG)); c.lineTo(cx+sd*Wd/2,lerp(top,top+Hb,(k+1)/SEG)); c.stroke();}});
  c.strokeStyle='rgba(245,250,255,.95)'; c.lineWidth=2.2;
  c.beginPath(); c.ellipse(cx,top,Wd/2,Wd*.06,0,0,7); c.stroke();
  // wick
  const wy=top-30*S; c.lineWidth=2.5; c.strokeStyle='rgba(245,250,255,.8)'; c.beginPath(); c.moveTo(cx,top); c.quadraticCurveTo(cx+4*S,top-15*S,cx+2*S,wy); c.stroke();
  // flame
  const f=flameAt(t), fl=Math.sin(t*13)*.5+Math.sin(t*7.3)*.5, relit=t>=RELIT;
  const Hf=150*S*f*(1+.06*fl), Wf=46*S*Math.max(.35,f), sx=fl*5*S*f;
  c.save(); c.shadowColor='#1AA6E3'; c.shadowBlur=(relit?90:50)*Math.max(.4,S); c.strokeStyle=relit?'#FFFFFF':'rgba(255,255,255,.9)'; c.lineWidth=2.6;
  c.fillStyle=relit?'rgba(26,166,227,.55)':'rgba(26,166,227,.25)';
  c.beginPath(); c.moveTo(cx+sx,wy-Hf); c.bezierCurveTo(cx+Wf,wy-Hf*.45,cx+Wf*.8,wy+4*S,cx,wy+4*S); c.bezierCurveTo(cx-Wf*.8,wy+4*S,cx-Wf,wy-Hf*.45,cx+sx,wy-Hf); c.fill(); c.stroke();
  c.restore();
  // smoke when the flame is weak
  const sm=clamp((.6-f)/.4)*(relit?clamp(1-(t-RELIT)*2):1);
  if(sm>0){c.strokeStyle=`rgba(200,215,225,${.35*sm})`; c.lineWidth=1.6; c.beginPath(); for(let k=0;k<=40;k++){const y=wy-Hf-k*9*S; const x=cx+Math.sin(k*.35-t*2.2)*k*.9*S; k?c.lineTo(x,y):c.moveTo(x,y);} c.stroke();}
  c.restore();
}
window.bgAt=t=>({show:t<HOOK?1:0, src:t, blur:0, dim:t>HOOK-.12?1:0, scale:1.1+.2*clamp(t/HOOK)});
// cues (lean set)
cue(TW(4,'fez'),F('ui_blip/kint__click_002.ogg'),{g:.45}); cue(TW(4,'perguntou'),F('ui_blip/kint__click_002.ogg'),{g:.45});
cue(TW(6,'agenda'),F('boom/ksci__lowFrequency_explosion_001.ogg'),{g:.55});
[TW(7,'chama'),TW(7,'cada'),TW(7,'desses')].forEach(x=>cue(x,F('ui_blip/kint__click_001.ogg'),{g:.4}));
cue(RELIT,F('boom/kimp__impactSoft_heavy_000.ogg'),{g:.4}); cue(TW(8,'dobrou'),F('boom/ksci__lowFrequency_explosion_000.ogg'),{g:.5});
function render(t){
  scenes(t,SC,TAGS); hookReveal(t);
  if(t>=LS(3)&&t<LS(4)){ rise($('a3a'),t,LS(3)); wipe($('a3b'),t,C3); rise($('a3c'),t,TW(3,'está'));}
  if(t>=LS(4)&&t<LS(5)){ [['a4c1','fez','a4i1','sumiu'],['a4c2','perguntou','a4i2','voltou']].forEach(([c,w,i,w2])=>{const e=$(c); const k=oQ(P(t,TW(4,w)-.1,TW(4,w)+.35)); e.style.opacity=k; e.style.transform=`translateX(${(1-k)*160}px)`;
      const li=$(i); const k2=P(t,TW(4,w2),TW(4,w2)+.25); li.style.opacity=k2; li.style.color=k2>0?'#1AA6E3':'';});}
  if(t>=LS(5)&&t<LS(6)){ rise($('a5a'),t,LS(5)); rise($('a5b'),t,TW(5,'chama'));}
  if(t>=LS(6)&&t<LS(7)){ rise($('a6a'),t,LS(6)); rise($('a6b'),t,TW(6,'lista')); const b=$('a6b'), k=$('a6k'); const r=b.getBoundingClientRect(); const w=Math.min(900,b.scrollWidth||800);
      k.style.left='120px'; k.style.width='840px'; k.style.transform=`scaleX(${sweepK(t,C6)})`; b.style.color=t>CM[C6][1]?'#3A4A58':'';
      wipe($('a6c'),t,C6b); rise($('a6d'),t,TW(6,'esperando'));}
  if(t>=LS(7)&&t<LS(8)){ const lg=$('a7logo'); const p=oQ(P(t,LS(7),LS(7)+.5)); lg.style.opacity=p; lg.style.transform=`scale(${lerp(.85,1,p)})`;
    [['r1','chama'],['r2','cada'],['r3','desses']].forEach(([id,w])=>{const e=$(id); const k=oQ(P(t,TW(7,w)-.08,TW(7,w)+.35)); e.style.opacity=k; e.style.transform=`translateX(${(1-k)*160}px)`;
      const st=q('.st',e); if(t<RELIT){st.textContent='CHAMANDO...'; st.style.color='#8A97A3';} else {st.textContent='AGENDADO ✓'; st.style.color='#1AA6E3';}});
    rise($('a7ex'),t,TW(7,'desses')+.3);}
  if(t>=LS(8)&&t<LS(9)){ pop($('a8logo'),t,LS(8)+.05,.4); rise($('a8a'),t,TW(8,'dobrou')-.05); rise($('a8b'),t,TW(8,'agendamentos')-.1);
    const a=TW(8,'dobrou'); const c=$('a8c'); const k=P(t,a,a+.3); c.style.opacity=t>=a?1:0; c.style.transform=`scale(${t>=a?lerp(1.6,1,oQ(k)):1})`; if(t>=a+.05){const [x,y]=shake(t,a+.05,18,.35); c.style.translate=`${x}px ${y}px`;}
    rise($('a8d'),t,TW(8,'primeiro'));}
  ctaEnd(t,'BASE'); drawArt(t); captions(t); comet(t);
}
'''
