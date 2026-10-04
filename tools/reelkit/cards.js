// uso: node cards.js <pasta_html> <pasta_png>  (1080x1920, fundo transparente)
const fs=require('fs'),path=require('path');const {chromium}=require('playwright');
const SRC=path.resolve(process.argv[2]),OUT=path.resolve(process.argv[3]);
const F=path.resolve(__dirname,'node_modules/@fontsource');
const ff=(fam,d,w)=>`@font-face{font-family:'${fam}';font-weight:${w};src:url('file://${F}/${d}/files/${d}-latin-${w}-normal.woff2') format('woff2')}`;
const css=!fs.existsSync(F)?'':[700,800,900].map(w=>ff('Montserrat','montserrat',w)).join('')+[400,500,600,700,800].map(w=>ff('Inter','inter',w)).join('');
(async()=>{const X='/opt/pw-browsers/chromium';const b=await chromium.launch(fs.existsSync(X)?{executablePath:X}:{});
const p=await b.newPage({viewport:{width:1080,height:1920}});fs.mkdirSync(OUT,{recursive:true});
for(const f of fs.readdirSync(SRC).filter(f=>f.endsWith('.html')&&!f.startsWith('.')).sort()){
 let h=fs.readFileSync(path.join(SRC,f),'utf8').replace('</head>',`<style>${css}html,body{margin:0;background:transparent}</style></head>`);
 const tmp=path.join(SRC,'.tmp.html');fs.writeFileSync(tmp,h);await p.goto('file://'+tmp);
 await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(150);
 const out=path.join(OUT,f.replace('.html','.png'));await p.screenshot({path:out,omitBackground:true});console.log(out);}
fs.rmSync(path.join(SRC,'.tmp.html'),{force:true});await b.close();})();
