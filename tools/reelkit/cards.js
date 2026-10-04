// uso: node cards.js <pasta_html> <pasta_png>  (1080x1920, fundo transparente)
// arquivos "nome.html" viram nome.png; "nome__N.seq.html" viram N quadros em nome/0001.png...
// (as animações CSS são pausadas e posicionadas quadro a quadro, 30 fps)
const fs=require('fs'),path=require('path');const {chromium}=require('playwright');
const SRC=path.resolve(process.argv[2]),OUT=path.resolve(process.argv[3]),FPS=30;
const F=path.resolve(__dirname,'node_modules/@fontsource');
const ff=(fam,d,w)=>`@font-face{font-family:'${fam}';font-weight:${w};src:url('file://${F}/${d}/files/${d}-latin-${w}-normal.woff2') format('woff2')}`;
const css=!fs.existsSync(F)?'':[700,800,900].map(w=>ff('Montserrat','montserrat',w)).join('')+[400,500,600,700,800].map(w=>ff('Inter','inter',w)).join('');
(async()=>{const X='/opt/pw-browsers/chromium';const b=await chromium.launch(fs.existsSync(X)?{executablePath:X}:{});
const p=await b.newPage({viewport:{width:1080,height:1920}});fs.mkdirSync(OUT,{recursive:true});
for(const f of fs.readdirSync(SRC).filter(f=>f.endsWith('.html')&&!f.startsWith('.')).sort()){
 let h=fs.readFileSync(path.join(SRC,f),'utf8').replace('</head>',`<style>${css}html,body{margin:0;background:transparent}</style></head>`);
 const tmp=path.join(SRC,'.tmp.html');fs.writeFileSync(tmp,h);await p.goto('file://'+tmp);
 await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(150);
 const m=f.match(/^(.*)__(\d+)\.seq\.html$/);
 if(!m){const out=path.join(OUT,f.replace('.html','.png'));await p.screenshot({path:out,omitBackground:true});console.log(out);continue;}
 const name=m[1],N=+m[2],dir=path.join(OUT,name);fs.mkdirSync(dir,{recursive:true});
 for(let i=0;i<N;i++){const t=i*1000/FPS;
  await p.evaluate(t=>{document.getAnimations().forEach(a=>{a.pause();a.currentTime=t;});},t);
  await p.screenshot({path:path.join(dir,String(i+1).padStart(4,'0')+'.png'),omitBackground:true});}
 console.log(dir,N);}
fs.rmSync(path.join(SRC,'.tmp.html'),{force:true});await b.close();})();
