"""Motor do modelo "gancho de tensão" da Tolki: monta a página de motion (HTML, quadro a quadro) a partir de uma cena.
Cada vídeo é um módulo em exemplos/ (ou o seu) com CSS, BODY e JS; core.page() junta com as partes comuns:
gancho de 6 s com contador, revelação "VOCÊ FICOU 6 SEGUNDOS", "e ainda está aqui", CTA "comenta PALAVRA" e cartela final.
Uso: python3 core.py <modulo.py> <pasta_do_video>   (escreve <pasta>/page.html; a pasta tem tl.js de tl.py)"""
import os, sys, importlib.util
ENGINE = os.path.dirname(os.path.abspath(__file__))
COMMON_CSS = r'''
#hk{top:250px;font-size:118px;color:#fff;letter-spacing:-.01em}
#v1{top:560px;font-size:104px}#v2{top:650px;font-size:640px;line-height:1;text-transform:none;letter-spacing:-.05em}#v3{top:1340px;font-size:54px;letter-spacing:20px;color:#fff;padding-left:20px}
#h1a{top:760px;font-size:150px}#h1b{top:930px;font-size:170px}
.chipX{position:absolute;left:110px;width:860px;height:170px;border-radius:30px;border:2px solid var(--line);background:var(--card);display:flex;align-items:center;padding:0 44px;gap:24px}
.chipX b{font-family:'Inter Tight';font-weight:800;font-size:44px;color:var(--wh);letter-spacing:-.02em}
.chipX i{margin-left:auto;font-style:normal;font-family:'JetBrains Mono';font-weight:700;font-size:24px;letter-spacing:2px;color:var(--gr)}
.strk2{position:absolute;height:12px;background:var(--cy);transform-origin:0 50%}
.lab{position:absolute;font-family:'JetBrains Mono';font-weight:700;font-size:22px;letter-spacing:3px;color:var(--gr)}
'''
COMMON_BODY_TOP = '''<div id="stage">
<canvas id="hgc" width="1080" height="1920"></canvas>
<div id="tag" class="ab mono"></div>
<div class="sc" id="s0h"><div id="hk" class="ab mono">6.00</div></div>
<div class="sc" id="s0"><div id="v1" class="ab sans">você ficou</div><div id="v2" class="ab sans cy">6</div><div id="v3" class="ab mono">SEGUNDOS</div></div>
<div class="sc" id="s1"><div id="h1a" class="ab ser">e ainda</div><div id="h1b" class="ab sans">está <span class="cy">aqui.</span></div></div>
'''
COMMON_BODY_END = '''<div class="sc" id="sCTA"><div id="h9a" class="ab sans">comenta</div><div id="inp"><span id="typ"></span><em id="cur"></em><svg width="80" height="80" viewBox="0 0 24 24"><path d="M3 11.5 21 3l-8.5 18-2.2-7.3z" fill="#1AA6E3"/></svg></div>
 <div id="h9b" class="ab ser">que eu te mostro como funciona.</div></div>
<div id="end"><img id="eLogo" src="assets/logo_light.png"><div id="eH" class="ab mono">@TOLKIBRASIL</div></div>
<div id="cap" class="ab"></div>
<canvas id="fx" width="1080" height="1920"></canvas>
<div id="wm"><svg width="26" height="26" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5" stroke="currentColor" stroke-width="2.2" fill="none"/><circle cx="12" cy="12" r="4.2" stroke="currentColor" stroke-width="2.2" fill="none"/><circle cx="17.3" cy="6.7" r="1.3" fill="currentColor"/></svg>@tolkibrasil</div>
</div>
'''
CORE_JS = r'''
const LN=TL.lines, DUR=TL.dur, HOOK=TL.hook;
const T=(l,w)=>LN[l-1].wt[w]-.03, LS=l=>LN[l-1].t-.05, LE=l=>LN[l-1].t+LN[l-1].d;
const nzw=w=>w.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^a-z0-9]/g,'');
const WI=(l,txt)=>{const i=LN[l-1].words.findIndex(w=>nzw(w).startsWith(nzw(txt)));if(i<0)console.log('WORD?',l,txt);return i<0?0:i};
const TW=(l,txt)=>T(l,WI(l,txt));
const NL=LN.length, ENDT=LE(NL)+.35;
const q=(s,r=document)=>r.querySelector(s), qa=(s,r=document)=>[...r.querySelectorAll(s)];
const ctx=$('fx').getContext('2d'), hctx=$('hgc').getContext('2d');
const RN=(i,sd)=>hash(i*12.9898+sd*78.233);
const arc=(a,b,h)=>k=>[lerp(a[0],b[0],k),lerp(a[1],b[1],k)-Math.sin(k*Math.PI)*h];
const CM=[]; const SW=(t0,y,d=.6,x0=80,x1=1000)=>{CM.push([t0,t0+d,k=>[lerp(x0,x1,iO(k)),y]]);return CM.length-1};
const CMp=(t0,d,f)=>{CM.push([t0,t0+d,f]);return CM.length-1};
function sweepK(t,i){const s=CM[i];return clamp((t-s[0])/(s[1]-s[0]))}
function comet(t){
  ctx.clearRect(0,0,1080,1920);
  CM.forEach(([t0,t1,f])=>{ if(t<t0||t>t1+.45) return;
    const N=34, span=Math.min(.32,(t1-t0)*.6);
    ctx.save(); ctx.globalCompositeOperation='lighter';
    for(let j=N;j>=0;j--){const tt=t-j*span/N; if(tt<t0) continue; const k=clamp((tt-t0)/(t1-t0)); const [x,y]=f(k);
      const fade=t>t1?clamp(1-(t-t1)/.45):1; const a=(1-j/N)*fade;
      ctx.fillStyle=`rgba(26,166,227,${.55*a})`; ctx.beginPath(); ctx.arc(x,y,3+14*(1-j/N),0,7); ctx.fill();}
    if(t<=t1){const [x,y]=f(clamp((t-t0)/(t1-t0)));
      ctx.shadowColor='#1AA6E3'; ctx.shadowBlur=80; ctx.fillStyle='#BFEAFF'; ctx.beginPath(); ctx.arc(x,y,17,0,7); ctx.fill();
      ctx.shadowBlur=24; ctx.fillStyle='#FFFFFF'; ctx.beginPath(); ctx.arc(x,y,9,0,7); ctx.fill();}
    ctx.restore();});
}
const CHUNK=LN.map(l=>{const g=[];for(let i=0;i<l.words.length;i+=5){let e=Math.min(l.words.length,i+5); if(l.words.length-e===1) e++; g.push([i,e]); if(e>=l.words.length)break; i=e-5;} return g});
function captions(t){const c=$('cap'); let html=''; if(t<LN[0].t-.05||t>=ENDT){c.innerHTML='';return} const li=LN.findIndex((l,i)=>t>=l.t-.05&&t<(i<LN.length-1?LN[i+1].t-.05:ENDT));
  if(li>=0){const l=LN[li]; let wi=-1; l.wt.forEach((x,i)=>{if(t>=x-.03)wi=i}); if(wi<0)wi=0;
    const [a,b]=CHUNK[li].find(([a,b])=>wi>=a&&wi<b)||CHUNK[li][0];
    for(let i=a;i<b;i++){const k=P(t,l.wt[i]-.03,l.wt[i]+.12); html+=`<span class="${i===wi?'on':''}" style="opacity:${k};transform:translateY(${(1-oC(k))*18}px)">${l.words[i]}</span>`;}}
  c.innerHTML=html;}
const rise=(el,t,t0,d=.5,dist=60)=>{const k=oQ(P(t,t0,t0+d)); el.style.opacity=clamp(k*1.6); el.style.transform=`translateY(${(1-k)*dist}px)`; el.style.filter=k<1?`blur(${(1-k)*14}px)`:''; return k};
const wipe=(el,t,i)=>{const k=sweepK(t,i); el.style.clipPath=`inset(-20% ${100-k*100}% -20% 0)`; el.style.opacity=k>0?1:0;};
const pop=(el,t,t0,d=.35)=>{const k=P(t,t0,t0+d); el.style.opacity=clamp(k*3); el.style.transform=`scale(${k>0?oB(k,1.5):.6})`; return k};
const F=(n)=>'file:'+n;
const KF=(K,t)=>{let i=0; while(i<K.length-2&&t>=K[i+1][0]) i++; const [t0,A]=K[i],[t1,B]=K[i+1]; const k=iO(P(t,t0,t1)); const o={}; for(const key in A) o[key]=lerp(A[key],B[key],k); return o;};
// hook + reveal (shared)
const C_SEG=HOOK>0?SW(TW(1,'segundos')-.05,1420,.7):-1, C_AQ=HOOK>0?SW(LS(2),1000,.75):-1;
function hookReveal(t){
  if(t<HOOK){ const v=Math.max(0,HOOK-t); const h=$('hk'); h.textContent=v.toFixed(2); const ph=t%1; h.style.transform=`scale(${1+.06*Math.exp(-ph*9)})`; h.style.opacity=clamp(t*3)*(v<.02?0:1);}
  if(t>=HOOK&&t<LS(2)){ rise($('v1'),t,T(1,0)); const a=TW(1,'seis'); const v2=$('v2'); const k=P(t,a,a+.3); v2.style.opacity=t>=a?1:0; v2.style.transform=`scale(${t>=a?lerp(1.6,1,oQ(k)):1})`; v2.style.filter=k<1&&t>=a?`blur(${(1-k)*20}px)`:'';
    if(t>=a+.05){const [x,y]=shake(t,a+.05,22,.4); v2.style.translate=`${x}px ${y}px`;} rise($('v3'),t,TW(1,'segundos'));}
  if(t>=LS(2)&&t<LS(3)){ rise($('h1a'),t,LS(2)); wipe($('h1b'),t,C_AQ);}
}
function ctaEnd(t,word){
  if(t>=LS(NL)&&t<ENDT){ rise($('h9a'),t,LS(NL)); const ip=$('inp'); const k=oQ(P(t,LS(NL)+.15,LS(NL)+.55)); ip.style.opacity=k; ip.style.transform=`scale(${lerp(.9,1,k)})`;
    const a=TW(NL,word)-.1; const n=Math.floor(clamp((t-a)/.42)*word.length); $('typ').textContent=word.slice(0,n); $('cur').style.opacity=(Math.floor(t*2.5)%2||n<word.length)?1:0;
    rise($('h9b'),t,TW(NL,'que'));}
  if(t>=ENDT){const k=t-ENDT,p=oQ(P(k,0,.6)); const lg=$('eLogo'); lg.style.clipPath=`inset(-20px ${(1-p)*50}% -20px ${(1-p)*50}%)`; $('eH').style.opacity=oC(P(k,.4,.8));}
}
function scenes(t,SC,TAGS){SC.forEach(([id,a,b])=>{$(id).style.display=(t>=a&&t<b)?'block':'none'}); $('end').style.display=t>=ENDT?'block':'none';
  let tag=''; TAGS.forEach(([a,s])=>{if(t>=a)tag=s}); $('tag').textContent=tag; $('tag').style.opacity=tag?1:0;}
const DUST=[...Array(60)].map((_,i)=>({x:RN(i,7)*1080,y:RN(i,8)*1920,sp:14+RN(i,9)*30,r:1+RN(i,10)*2}));
function dust(c,t){DUST.forEach(d=>{const y=(d.y-t*d.sp+1920*4)%1920; c.fillStyle='rgba(150,205,235,.16)'; c.beginPath(); c.arc(d.x+Math.sin(t*.4+d.y)*12,y,d.r,0,7); c.fill();});}
// shared cues
// sons do gancho só quando houver gancho (TL.hook > 0); sem gancho, a cena começa direto na fala 1 e não usa s0h/s0/s1
if(HOOK>0){ for(let k=0;k<Math.round(HOOK);k++) cue(k+.02,'tick',{g:.42,f:1500});
  cue(TW(1,'seis'),F('boom/ksci__lowFrequency_explosion_000.ogg'),{g:.6}); }
'''
READY_JS = r'''
window.DUR=DUR; window.renderAll=t=>render(t);
Promise.all(['italic 400 100px "Instrument Serif"','800 100px "Inter Tight"','600 100px "Inter Tight"','700 30px "JetBrains Mono"','700 30px Inter','400 30px Inter'].map(f=>document.fonts.load(f))).then(()=>document.fonts.ready).then(()=>{
  qa('.sans,.ser').forEach(e=>{if(!e.classList.contains('ab'))return; const host=e.closest('.sc'); if(host)host.style.display='block';
    const fs=parseFloat(getComputedStyle(e).fontSize); e.style.display='inline-block'; e.style.width='auto'; const w=e.getBoundingClientRect().width; e.style.display=''; e.style.width='';
    if(w>960) e.style.fontSize=(fs*960/w)+'px'; if(host)host.style.display='none';});
  render(0); window.READY=true;});
'''
def page(work, css, body, js):
    work = os.path.abspath(work)
    html = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><base href="file://{ENGINE}/">'
            '<link rel="stylesheet" href="fonts.css"><link rel="stylesheet" href="base.css"><style>' + COMMON_CSS + css + '</style></head><body>\n'
            + COMMON_BODY_TOP + body + COMMON_BODY_END
            + f'<script src="file://{work}/tl.js"></script>\n<script src="common.js"></script>\n<script>\n' + CORE_JS + js + READY_JS + '</script></body></html>')
    open(os.path.join(work, 'page.html'), 'w').write(html); return os.path.join(work, 'page.html')
def from_html(src_html, work):
    """Página escrita à mão (ex.: exemplos/ampulheta.html): aponta a base para o motor e o tl.js para a pasta do vídeo."""
    work = os.path.abspath(work); h = open(src_html).read()
    h = h.replace('<head><meta charset="utf-8">', f'<head><meta charset="utf-8"><base href="file://{ENGINE}/">', 1).replace('src="hg/tl.js"', f'src="file://{work}/tl.js"')
    open(os.path.join(work, 'page.html'), 'w').write(h); return os.path.join(work, 'page.html')
if __name__ == '__main__':
    mod, work = sys.argv[1], sys.argv[2]
    if mod.endswith('.html'): print(from_html(mod, work)); sys.exit()
    spec = importlib.util.spec_from_file_location('m', mod); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    print(page(work, m.CSS, m.BODY, m.JS))
