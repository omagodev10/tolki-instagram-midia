"""Dominó: gancho 100% DESENHADO (dominós 3D em traço fino). Copy do paciente sem resposta. Prova OrthoDontic. CTA AGENDA."""
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

#b3a{top:400px;font-size:100px}#b3b{top:500px;font-size:140px}
#b5a{top:380px;font-size:120px}
#b6a{top:400px;font-size:110px}#b6b{top:520px;font-size:150px}#b6c{top:690px;font-size:120px}
#b7logo{position:absolute;left:280px;top:390px;width:520px}#b7a{top:590px;font-size:96px}#b7b{top:690px;font-size:150px}
#b8a{top:820px;font-size:430px;line-height:1;letter-spacing:-.05em}#b8b{top:1280px;font-size:70px}#b8c{top:1370px;font-size:34px;letter-spacing:8px;color:var(--cy)}
#chat{position:absolute;left:90px;top:640px;width:900px;background:var(--card);border:2px solid var(--line);border-radius:36px;overflow:hidden}
#chat .hd{display:flex;align-items:center;gap:22px;padding:30px 34px;border-bottom:2px solid var(--line)}
#chat .av{width:76px;height:76px;border-radius:50%;background:#173049;display:flex;align-items:center;justify-content:center;font-family:'Inter Tight';font-weight:800;font-size:32px;color:var(--wh)}
#chat .nm{font-family:'Inter Tight';font-weight:700;font-size:36px;color:var(--wh)}#chat .st{font-family:'Inter';font-size:24px;color:var(--gr)}
#chat .ex{margin-left:auto;font-family:'JetBrains Mono';font-weight:700;font-size:17px;letter-spacing:2px;color:var(--gr);text-align:right;line-height:1.35}
#chat .bd{padding:34px;display:flex;flex-direction:column;gap:22px;min-height:300px}
.bub{max-width:680px;padding:22px 28px 14px;border-radius:28px;font-family:'Inter';font-size:38px;line-height:1.3;color:var(--wh)}
.bub small{display:block;text-align:right;font-size:20px;color:rgba(255,255,255,.55);margin-top:6px}
.in{align-self:flex-start;background:#152C40;border-top-left-radius:8px}
#wait{align-self:center;margin-top:8px;font-family:'JetBrains Mono';font-weight:700;font-size:28px;letter-spacing:2px;color:var(--cy);border:2px solid var(--cy);border-radius:40px;padding:14px 30px}
'''
BODY = '''<div class="sc" id="sB3"><div id="b3a" class="ab ser">na tua clínica,</div><div id="b3b" class="ab sans">a primeira peça</div></div>
<div class="sc" id="sB4"><div id="chat"><div class="hd"><div class="av">J</div><div><div class="nm">Juliana</div><div class="st" id="cst">online</div></div><div class="ex">EXEMPLO<br>ILUSTRATIVO</div></div>
 <div class="bd"><div class="bub in" id="m1">Oi! Quanto custa o clareamento?<small>19:42</small></div><div id="wait">SEM RESPOSTA HÁ <span id="wt">00:00:00</span></div></div></div></div>
<div class="sc" id="sB5"><div id="b5a" class="ab sans">efeito dominó</div></div>
<div class="sc" id="sB6"><div id="b6a" class="ab ser">uma peça</div><div id="b6b" class="ab sans">derruba a</div><div id="b6c" class="ab sans cy">agenda inteira.</div></div>
<div class="sc" id="sB7"><img id="b7logo" src="assets/logo_light.png"><div id="b7a" class="ab ser">responde em</div><div id="b7b" class="ab sans">segundos.</div></div>
<div class="sc" id="sB8"><div id="a8logo"><img src="assets/cl_ortho.png"></div><div id="b8a" class="ab sans cy">0</div><div id="b8b" class="ab ser">contratos em um mês</div></div>
'''
JS = r'''
const fmt=s=>{s=Math.max(0,Math.floor(s));const h=Math.floor(s/3600),m=Math.floor(s/60)%60,ss=s%60;return [h,m,ss].map(v=>String(v).padStart(2,'0')).join(':')};
const SC=[['s0h',0,HOOK],['s0',HOOK,LS(2)],['s1',LS(2),LS(3)],['sB3',LS(3),LS(4)],['sB4',LS(4),LS(5)],['sB5',LS(5),LS(6)],['sB6',LS(6),LS(7)],['sB7',LS(7),LS(8)],['sB8',LS(8),LS(9)],['sCTA',LS(9),ENDT]];
const TAGS=[[0,''],[LS(4),'TEMPO DE RESPOSTA'],[LS(5),''],[LS(7),'COM A TOLKI'],[LS(8),'RESULTADO REAL · CLIENTE TOLKI'],[LS(9),'']];
const C3=SW(TW(3,'primeira')-.05,590,.6), C6=SW(TW(6,'agenda')-.08,760,.55);
CMp(TW(8,'cinquenta')-.1,.9,k=>[lerp(200,880,iO(k)),lerp(1240,960,oC(k))]);
CMp(TW(9,'agenda')+.6,.7,k=>[lerp(130,960,iO(k)),1000]);
const HOLD=TW(7,'segura');
// ---- 3D line-art dominoes
const ND=7, DW=1.7, DH=3.4, DD=.55, GAP=2.3;
function cam(L){ // look-at camera
  const e=L.eye, tg=L.tg; let fz=[tg[0]-e[0],tg[1]-e[1],tg[2]-e[2]]; let n=Math.hypot(...fz); fz=fz.map(v=>v/n);
  let rx=[-fz[2],0,fz[0]]; n=Math.hypot(...rx); rx=rx.map(v=>v/n); const up=[rx[1]*fz[2]-rx[2]*fz[1], rx[2]*fz[0]-rx[0]*fz[2], rx[0]*fz[1]-rx[1]*fz[0]];
  return p=>{const d=[p[0]-e[0],p[1]-e[1],p[2]-e[2]]; const x=d[0]*rx[0]+d[1]*rx[1]+d[2]*rx[2], y=d[0]*up[0]+d[1]*up[1]+d[2]*up[2], z=d[0]*fz[0]+d[1]*fz[1]+d[2]*fz[2];
    return [L.cx+x*L.f/z, L.cy-y*L.f/z, z];};}
function domAt(t){const V=(a,b,cx,cy,f)=>({a,b,cx,cy,f,ex:-8.5,ey:4.2,ez:-2.6});return KF([[0,V(1,0,540,1060,820)],[HOOK-.01,V(1,0,540,1060,820)],[HOOK,V(0,0,540,1060,820)],
  [LS(3)-.05,V(0,0,540,1200,780)],[LS(3)+.35,V(1,0,540,1200,780)],[LS(4)-.1,V(1,0,540,1200,780)],
  [LS(4)+.4,V(.12,8,540,1150,860)],[LS(5)-.1,V(.12,8,540,1150,860)],
  [LS(5)+.4,V(1,0,540,1060,800)],[LS(7)-.1,V(1,0,540,1100,800)],
  [LS(7)+.4,V(1,0,540,1400,560)],[LS(8)-.1,V(1,0,540,1400,560)],
  [LS(8)+.4,V(.08,10,540,1100,860)],[DUR,V(.08,10,540,1100,860)]],t);}
const REST=Math.asin(Math.min(1,(GAP-DD)/DH))*180/Math.PI;   // leaning angle on the next piece
const FALLS=()=>{const f=[TW(5,'desiste'),TW(5,'avaliação'),TW(5,'tratamento')]; const d=TW(6,'derruba'); for(let i=3;i<ND;i++) f.push(d+(i-3)*.16); return f;};
function angles(t){ const A=Array(ND).fill(0);
  if(t<HOOK){ const k=P(t,0,HOOK); A[0]=4+15*Math.pow(k,1.3)+Math.sin(t*5.5)*2.5*k; return A;}
  if(t<LS(5)){ A[0]=t>=LS(3)?10+Math.sin(t*4)*2:0; return A;}
  if(t<LS(7)){ const fs=FALLS(); for(let i=0;i<ND;i++){const t0=fs[i]-.25; const k=P(t,t0,t0+.45); const rest=i===ND-1?88:REST; A[i]=k*k*rest;} return A;}
  A[0]=Math.min(10,lerp(0,14,P(t,LS(7)+.4,HOLD)))*(t<HOLD+.1?1:1); return A;}
function drawArt(t){
  const c=hctx; c.clearRect(0,0,1080,1920); if(t>=HOOK) dust(c,t);
  const L=domAt(t); $('hgc').style.filter=L.b>.3?`blur(${L.b}px)`:''; if(L.a<.01) return;
  const pr=cam({eye:[L.ex,L.ey,L.ez],tg:[0,1.5,4.6],cx:L.cx,cy:L.cy,f:L.f}); const A=angles(t);
  c.save(); c.globalAlpha=L.a;
  // ground line
  const g0=pr([-1.4,0,-2]), g1=pr([-1.4,0,ND*GAP+2]), g2=pr([1.4,0,-2]), g3=pr([1.4,0,ND*GAP+2]);
  c.strokeStyle='rgba(200,220,235,.18)'; c.lineWidth=1.2; [[g0,g1],[g2,g3]].forEach(([a,b])=>{c.beginPath(); c.moveTo(a[0],a[1]); c.lineTo(b[0],b[1]); c.stroke();});
  for(let i=ND-1;i>=0;i--){ const th=A[i]*Math.PI/180, z0=i*GAP;
    const V=[]; for(const x of [-DW/2,DW/2]) for(const y of [0,DH]) for(const z of [-DD/2,DD/2]){ const zz=z-DD/2; const yr=y*Math.cos(th)-zz*Math.sin(th), zr=y*Math.sin(th)+zz*Math.cos(th); V.push(pr([x,yr,zr+DD/2+z0]));}
    const idx=(x,y,z)=>x*4+y*2+z; const faces=[[idx(0,0,0),idx(1,0,0),idx(1,1,0),idx(0,1,0)],[idx(0,0,1),idx(1,0,1),idx(1,1,1),idx(0,1,1)],[idx(0,0,0),idx(0,1,0),idx(0,1,1),idx(0,0,1)],[idx(1,0,0),idx(1,1,0),idx(1,1,1),idx(1,0,1)],[idx(0,1,0),idx(1,1,0),idx(1,1,1),idx(0,1,1)],[idx(0,0,0),idx(1,0,0),idx(1,0,1),idx(0,0,1)]];
    faces.map(f=>({f,z:f.reduce((s,k)=>s+V[k][2],0)/4})).sort((a,b)=>b.z-a.z).forEach(({f})=>{
      c.fillStyle='#050B12'; c.beginPath(); f.forEach((k,j)=>j?c.lineTo(V[k][0],V[k][1]):c.moveTo(V[k][0],V[k][1])); c.closePath(); c.fill();
      c.strokeStyle=i===0?'rgba(26,166,227,.95)':'rgba(240,248,255,.85)'; c.lineWidth=i===0?2.6:1.8; c.stroke();});
    // front-face hatching + divider (pencil-line texture of ref 2)
    const F0=[V[idx(0,0,0)],V[idx(1,0,0)],V[idx(1,1,0)],V[idx(0,1,0)]];
    c.strokeStyle=i===0?'rgba(26,166,227,.25)':'rgba(236,244,250,.14)'; c.lineWidth=1;
    for(let k=1;k<12;k++){const u=k/12; const a=[lerp(F0[0][0],F0[1][0],u),lerp(F0[0][1],F0[1][1],u)], b=[lerp(F0[3][0],F0[2][0],u),lerp(F0[3][1],F0[2][1],u)]; c.beginPath(); c.moveTo(a[0],a[1]); c.lineTo(b[0],b[1]); c.stroke();}
    const m0=[lerp(F0[0][0],F0[3][0],.5),lerp(F0[0][1],F0[3][1],.5)], m1=[lerp(F0[1][0],F0[2][0],.5),lerp(F0[1][1],F0[2][1],.5)];
    c.strokeStyle=i===0?'rgba(26,166,227,.9)':'rgba(240,248,255,.6)'; c.lineWidth=1.6; c.beginPath(); c.moveTo(m0[0],m0[1]); c.lineTo(m1[0],m1[1]); c.stroke();
    if(i===0){ const ct=[(F0[0][0]+F0[2][0])/2,(F0[0][1]+F0[2][1])/2]; c.save(); c.shadowColor='#1AA6E3'; c.shadowBlur=60; c.fillStyle='rgba(26,166,227,.35)'; c.beginPath(); c.arc(ct[0],ct[1],8,0,7); c.fill(); c.restore();}
    domLabelPos[i]=pr([DW/2+.25,0,z0]);
  }
  // stopper that holds the first piece (Tolki)
  if(t>=HOLD-.05&&t<LS(8)+.4){ const k=oB(P(t,HOLD-.05,HOLD+.3),1.6); const p0=pr([0,0,DD+.45]), p1=pr([0,DH*.85,DD+.45]);
    c.save(); c.shadowColor='#1AA6E3'; c.shadowBlur=50; c.strokeStyle='#1AA6E3'; c.lineWidth=10*k; c.lineCap='round'; c.beginPath(); c.moveTo(p0[0],p0[1]); c.lineTo(lerp(p0[0],p1[0],k),lerp(p0[1],p1[1],k)); c.stroke(); c.restore();}
  // labels
  c.globalAlpha=L.a; c.font='700 22px "JetBrains Mono"'; c.textAlign='left';
  if(t>=LS(3)&&t<LS(4)){ const k=oC(P(t,TW(3,'mensagem'),TW(3,'mensagem')+.4)); const p=pr([0,DH+.1,0]); c.globalAlpha=L.a*k; c.strokeStyle='#1AA6E3'; c.lineWidth=2; c.setLineDash([6,8]);
    c.beginPath(); c.moveTo(p[0],p[1]-8); c.lineTo(p[0],p[1]-90); c.stroke(); c.setLineDash([]); c.fillStyle='#1AA6E3'; c.font='700 26px "JetBrains Mono"'; c.textAlign='left'; c.fillText('MENSAGEM',p[0]-20,p[1]-136); c.fillText('SEM RESPOSTA',p[0]-20,p[1]-102);}
  if(t>=LS(5)&&t<LS(7)){ const fs=FALLS(); [['DESISTE',0],['SEM AVALIAÇÃO',1],['SEM TRATAMENTO',2]].forEach(([s,i])=>{const k=oC(P(t,fs[i],fs[i]+.3)); if(k<=0) return; const p=pr([0,0,i*GAP]); const base=pr([0,0,0])[1]; const ly=base+90+i*52, lx=130;
      c.globalAlpha=L.a*k; c.strokeStyle='rgba(26,166,227,.6)'; c.lineWidth=1.5; c.beginPath(); c.moveTo(p[0],p[1]+10); c.lineTo(p[0],ly-9); c.lineTo(lx+300,ly-9); c.stroke();
      c.fillStyle='#1AA6E3'; c.beginPath(); c.arc(p[0],p[1]+10,4,0,7); c.fill(); c.font='700 28px "JetBrains Mono"'; c.textAlign='left'; c.fillText(s,lx,ly);});}
  c.restore();
}
const domLabelPos=[];
window.bgAt=t=>({show:0, src:0, blur:0, dim:1, scale:1});
// cues
cue(LS(4)+.4,F('ui_blip/kint__click_002.ogg'),{g:.5});
FALLS().forEach((x,i)=>cue(x+.15,F('hit/kimp__impactPlate_heavy_00'+(i%2?'3':'1')+'.ogg'),{g:i<3?.45:.32}));
cue(TW(6,'agenda'),F('boom/ksci__lowFrequency_explosion_001.ogg'),{g:.55});
cue(HOLD,F('boom/kimp__impactSoft_heavy_000.ogg'),{g:.45}); cue(TW(8,'cinquenta'),F('boom/ksci__lowFrequency_explosion_000.ogg'),{g:.5});
function render(t){
  scenes(t,SC,TAGS); hookReveal(t);
  if(t>=LS(3)&&t<LS(4)){ rise($('b3a'),t,LS(3)); wipe($('b3b'),t,C3);}
  if(t>=LS(4)&&t<LS(5)){ const k=oQ(P(t,LS(4)-.05,LS(4)+.5)); $('chat').style.transform=`translateY(${(1-k)*260}px)`; $('chat').style.opacity=k; pop($('m1'),t,LS(4)+.35);
    const w0=TW(4,'ninguém'); $('wait').style.opacity=t>=w0?1:0; const sec=t<w0?0:Math.pow(P(t,w0,LE(4)+.3),2.2)*(15*3600+21*60+8); $('wt').textContent=fmt(sec); $('cst').textContent=t>=w0?'visto por último às 19:42':'online';}
  if(t>=LS(5)&&t<LS(6)){ rise($('b5a'),t,LS(5)+.1);}
  if(t>=LS(6)&&t<LS(7)){ rise($('b6a'),t,LS(6)); rise($('b6b'),t,TW(6,'derruba')); wipe($('b6c'),t,C6);
    const ag=TW(6,'agenda'); if(t>=ag){const [x,y]=shake(t,ag,16,.35); $('sB6').style.transform=`translate(${x}px,${y}px)`;}}
  if(t>=LS(7)&&t<LS(8)){ const lg=$('b7logo'); const p=oQ(P(t,LS(7),LS(7)+.5)); lg.style.opacity=p; lg.style.transform=`scale(${lerp(.85,1,p)})`; rise($('b7a'),t,TW(7,'responde')); rise($('b7b'),t,TW(7,'segundos'));}
  if(t>=LS(8)&&t<LS(9)){ pop($('a8logo'),t,LS(8)+.05,.4); const a=TW(8,'cinquenta'), b=TW(8,'contratos'); const B=$('b8a'); const k=oC(P(t,a,b)); B.style.opacity=t>=a-.05?1:0; B.textContent=Math.round(lerp(0,54,k));
    if(t>=b){const [x,y]=shake(t,b,16,.3); B.style.translate=`${x}px ${y}px`;} rise($('b8b'),t,b-.05);}
  ctaEnd(t,'AGENDA'); drawArt(t); captions(t); comet(t);
}
'''
