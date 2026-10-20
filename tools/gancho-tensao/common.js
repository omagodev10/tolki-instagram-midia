// ---------- math ----------
const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const P=(t,a,b)=>clamp((t-a)/(b-a));
const lerp=(a,b,k)=>a+(b-a)*k;
const oC=x=>1-Math.pow(1-x,3), oQ=x=>1-Math.pow(1-x,5), iC=x=>x*x*x;
const iO=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
const oB=(x,s=1.7)=>{const c3=s+1;return 1+c3*Math.pow(x-1,3)+s*Math.pow(x-1,2)};
const oE=x=>x===1?1:1-Math.pow(2,-10*x);
const elastic=x=>x===0?0:x===1?1:Math.pow(2,-10*x)*Math.sin((x*10-.75)*(2*Math.PI)/3)+1;
const hash=n=>{const s=Math.sin(n*127.1+311.7)*43758.5453;return s-Math.floor(s)};
const $=id=>document.getElementById(id);
const fmtBR=(n,d=0)=>n.toLocaleString('pt-BR',{minimumFractionDigits:d,maximumFractionDigits:d});

// ---------- sound cues & music (read by the renderer) ----------
window.CUES=[]; window.MUSIC={style:'drive',bpm:124,drop:2,end:14,key:'Fm'};
function cue(t,type,o={}){CUES.push(Object.assign({t,type},o))}

// ---------- text helpers ----------
function splitWords(el){
  const walk=node=>{
    [...node.childNodes].forEach(n=>{
      if(n.nodeType===3){
        const frag=document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(tok=>{
          if(!tok) return;
          if(/^\s+$/.test(tok)){frag.appendChild(document.createTextNode(tok));return}
          const w=document.createElement('span');w.className='w';
          const i=document.createElement('span');i.textContent=tok;w.appendChild(i);frag.appendChild(w);
        });
        n.replaceWith(frag);
      } else if(n.nodeType===1 && !n.classList.contains('w')) walk(n);
    });
  };
  walk(el); return [...el.querySelectorAll('.w>span')];
}
// masked rise of each word, staggered
function wordsIn(words,t,t0,stag=.06,dur=.55,dist=110){
  words.forEach((w,i)=>{const k=oQ(P(t,t0+i*stag,t0+i*stag+dur));w.style.transform=`translateY(${(1-k)*dist}%)`;});
}
function wordsOut(words,t,t0,stag=.03,dur=.35){
  words.forEach((w,i)=>{const k=iC(P(t,t0+i*stag,t0+i*stag+dur));if(k>0)w.style.transform=`translateY(${-k*110}%)`;});
}
function lineIn(el,t,t0,dur=.6,dist=115){const k=oQ(P(t,t0,t0+dur));el.style.transform=`translateY(${(1-k)*dist}%)`;return k}
function show(el,on){el.style.visibility=on?'visible':'hidden'}
function shake(t,t0,amp=14,dur=.35){const k=P(t,t0,t0+dur);if(k<=0||k>=1)return [0,0];const e=(1-k)*(1-k)*amp;return [(hash(t*97)-.5)*2*e,(hash(t*53+7)-.5)*2*e]}

// ---------- grain ----------
let grainFrames=[];
function buildGrain(){
  const GH=window.VERT?960:540;
  const c=document.createElement('canvas');c.id='grain';c.width=540;c.height=GH;$('stage').appendChild(c);
  const v=document.createElement('div');v.id='vig';$('stage').appendChild(v);
  const ctx=c.getContext('2d');
  for(let f=0;f<8;f++){const im=ctx.createImageData(540,GH);let s=f*9973+1;
    for(let i=0;i<im.data.length;i+=4){s=(s*16807)%2147483647;const g=s%256;im.data[i]=im.data[i+1]=im.data[i+2]=g;im.data[i+3]=255}
    grainFrames.push(im)}
}
function drawGrain(t){const c=$('grain');if(!c)return;c.getContext('2d').putImageData(grainFrames[Math.floor(t*24)%8],0,0)}

// ---------- end card (official logo reveal + CTA bubble) ----------
const LOGO={
  light:{src:'assets/logo_light.png',w:1688,h:498,oc:[548.7,250.8],icon:{x:302.9,y:-7.0,s:1.154}},
  dark :{src:'assets/logo_dark.png', w:1749,h:483,oc:[567.1,241.0],icon:{x:287.4,y:-52.3,s:1.313}},
};
const ICON={w:425,h:438};
let EC=null;
function buildEndCard(o){
  // o: {t0, theme:'dark'|'light', cta:html, logoW, logoTop, bubbleTop, url, bg:false}
  const theme=o.theme||'dark', L=LOGO[theme==='dark'?'light':'dark'];
  const vy=window.VERT?(o.vy??400):0;
  const logoW=o.logoW||600, sc=logoW/L.w, logoH=L.h*sc, logoLeft=540-logoW/2, logoTop=(o.logoTop||300)+vy;
  o.iconY=(o.iconY||430)+vy;
  const ec=document.createElement('div');ec.id='ec';ec.className='ec-'+theme;
  ec.innerHTML=`<div id="ecBg"></div><img id="ecLogo" src="${L.src}"><img id="ecIcon" src="assets/icon.png">
    <div id="ecBubble"><svg class="tail" viewBox="0 0 40 34" style="position:absolute;left:-16px;bottom:0;width:40px;height:34px;overflow:visible"><path d="M40 0 C40 20 30 32 0 34 C20 26 24 14 24 0 Z" fill="currentColor"/></svg>
      <div id="ecDots"><i></i><i></i><i></i></div><div id="ecTxt">${o.cta||'Envie uma mensagem<br>para agendar <b>um papo conosco.</b>'}</div></div>
    ${o.url===false?'':'<div id="ecUrl">TOLKI.COM.BR</div>'}`;
  $('stage').appendChild(ec);
  if(o.bg===false) $('ecBg').style.display='none';
  const logo=$('ecLogo');Object.assign(logo.style,{left:logoLeft+'px',top:logoTop+'px',width:logoW+'px',height:logoH+'px'});
  const it={x:logoLeft+L.icon.x*sc, y:logoTop+L.icon.y*sc, w:ICON.w*L.icon.s*sc, h:ICON.h*L.icon.s*sc};
  const icon=$('ecIcon');Object.assign(icon.style,{left:it.x+'px',top:it.y+'px',width:it.w+'px',height:it.h+'px'});
  const bub=$('ecBubble'); bub.style.color=''; bub.querySelector('.tail').style.color=theme==='dark'?'#fff':'var(--navy)';
  const txt=$('ecTxt'); const words=splitWords(txt);
  EC={o,theme,L,sc,logoW,logoLeft,logoTop,it,words,bubbleTop:o.bubbleTop||(logoTop+logoH+90)};
  bub.style.top=EC.bubbleTop+'px';
  requestAnimationFrame(()=>{});
  const t0=o.t0;
  cue(t0+.18,'pop',{g:.9,f:420}); cue(t0+.2,'whooshUp',{g:.5});
  cue(t0+.95,'whoosh',{g:.55,d:.5}); cue(t0+1.28,'hit',{g:.7});
  cue(t0+1.75,'notif',{g:.75}); cue(t0+2.45,'typeBurst',{g:.35,d:.55});
  return EC;
}
function renderEndCard(t){
  if(!EC) return; const {o,theme,L,sc,logoW,logoLeft,logoTop,it,words}=EC; const t0=o.t0;
  const ec=$('ec'); if(t<t0){ec.style.opacity=0;ec.style.visibility='hidden';return}
  ec.style.visibility='visible';
  const fade=o.bgIn==='cut'?1:oC(P(t,t0,t0+.35)); ec.style.opacity=fade;
  // icon: pop in big at center, then fly into the O
  const pop=P(t,t0+.12,t0+.72), fly=iO(P(t,t0+.85,t0+1.35));
  const bigW=o.iconBig||300, bigS=bigW/it.w;
  const cx0=540, cy0=o.iconY||430, cx1=it.x+it.w/2, cy1=it.y+it.h/2;
  const s=pop<=0?0:lerp(bigS*oB(pop,2.2),1,fly);
  const rot=lerp(-18,0,oC(pop))*(1-fly);
  const cx=lerp(cx0,cx1,fly), cy=lerp(cy0,cy1,fly)-Math.sin(fly*Math.PI)*40;
  const icon=$('ecIcon');
  icon.style.transform=`translate(${cx-cx1}px,${cy-cy1}px) rotate(${rot}deg) scale(${s})`;
  // idle float before flying
  let iconOp=1;
  if(theme==='light') iconOp=1-oC(P(t,t0+1.45,t0+1.8));   // hand over to the flat official O
  icon.style.opacity=iconOp;
  // wordmark reveals outward from the O
  const rv=oQ(P(t,t0+1.02,t0+1.62)); const ocx=L.oc[0]*sc;
  const left=ocx*(1-rv), right=(logoW-ocx)*(1-rv);
  const logo=$('ecLogo');
  logo.style.clipPath=`inset(-20px ${right}px -20px ${left}px)`;
  logo.style.opacity=rv>0?1:0;
  logo.style.transform=`scale(${lerp(.94,1,oC(P(t,t0+1.02,t0+2.2)))})`;
  // subtle settle bounce on whole lockup after landing
  // bubble
  const bub=$('ecBubble'); const bp=P(t,t0+1.7,t0+2.2);
  const w=bub.offsetWidth; bub.style.left=(540-w/2)+'px';
  bub.style.opacity=bp>0?1:0; bub.style.transform=`scale(${bp>0?oB(bp,2):0})`;
  // typing dots then text
  const dotsOn=t<t0+2.45; const dots=$('ecDots'); dots.style.opacity=dotsOn?1:0;
  [...dots.children].forEach((d,i)=>{const ph=(t*6-i*.9);d.style.transform=`translateY(${-Math.max(0,Math.sin(ph))*12}px)`});
  $('ecTxt').style.opacity=dotsOn?0:1;
  words.forEach((wd,i)=>{const k=oQ(P(t,t0+2.45+i*.045,t0+2.45+i*.045+.4));wd.style.transform=`translateY(${(1-k)*110}%)`});
  const u=$('ecUrl'); if(u) u.style.opacity=oC(P(t,t0+2.9,t0+3.4));
}

// ---------- time warp (design time <-> real time), set by the renderer ----------
window.WARP=null;
function _pw(x,xs,ys){if(x<=xs[0])return ys[0]+(x-xs[0]);const L=xs.length-1;if(x>=xs[L])return ys[L]+(x-xs[L]);
  for(let i=0;i<L;i++){if(x<=xs[i+1]){const k=(x-xs[i])/(xs[i+1]-xs[i]||1);return ys[i]+(ys[i+1]-ys[i])*k}}}
function r2d(r){if(!WARP)return r;return _pw(r,WARP.map(p=>p[1]),WARP.map(p=>p[0]))}
function d2r(d){if(!WARP)return d;return _pw(d,WARP.map(p=>p[0]),WARP.map(p=>p[1]))}
// ---------- vertical adapter: full-frame backgrounds, content moved into the Reels safe band ----------
window.VERT=false;
function vertify(o={}){
  document.documentElement.classList.add('vert'); window.VERT=true;
  const Y=o.y??360, S=o.s??.94, X=(1080-1080*S)/2, tf=`translate(${X}px,${Y}px) scale(${S})`;
  const mk=()=>{const d=document.createElement('div');d.className='C abs';
    d.style.cssText=`left:0;top:0;width:1080px;height:1080px;transform-origin:0 0;transform:${tf}`;return d};
  const bg=new Set(o.bg||[]), inner=new Set(o.inner||[]);
  const wrapKids=(parent,skip)=>{let cur=null;[...parent.children].forEach(el=>{
    if(skip(el)){cur=null;return} if(!cur){cur=mk();parent.insertBefore(cur,el)} cur.appendChild(el)})};
  wrapKids($('stage'),el=>bg.has(el.id)||inner.has(el.id));
  inner.forEach(id=>wrapKids($(id),()=>false));
}
function vertNative(){document.documentElement.classList.add('vert'); window.VERT=true;}
// count-up helper
function countTo(el,t,a,b,v0,v1,fmt=v=>fmtBR(Math.round(v)),ease=oC){const k=ease(P(t,a,b));el.textContent=fmt(lerp(v0,v1,k));return k}
// ---------- boot ----------
function boot(render,opts={}){
  window.DUR=opts.dur; window.COVER=opts.cover??null; if(opts.music) Object.assign(MUSIC,opts.music);
  if(opts.grain!==false) buildGrain();
  if(opts.grain!==undefined && typeof opts.grain==='number') $('stage').style.setProperty('--grain',opts.grain);
  if(opts.vig) $('stage').style.setProperty('--vig',opts.vig);
  window.renderAll=r=>{const t=r2d(r);render(t);renderEndCard(t);drawGrain(r)};
  const q=new URLSearchParams(location.search);
  document.fonts.ready.then(()=>{renderAll(q.has('t')?+q.get('t'):0);window.READY=true});
}
