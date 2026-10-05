// uso: node templates/render.js <pasta_html> <pasta_saida> [altura 1350|1920]
// Rode na pasta onde instalou: npm i @fontsource/montserrat @fontsource/inter playwright
// Troca __TPL__ pelo caminho absoluto desta pasta templates/ (ícone e fontes extras).
const fs=require('fs'),path=require('path');const {chromium}=require(require.resolve('playwright',{paths:[process.cwd()]}));
const TPL=path.resolve(__dirname);
const SRC=path.resolve(process.argv[2]),OUT=path.resolve(process.argv[3]),H=+(process.argv[4]||1350);
const F=path.resolve(process.cwd(),'node_modules/@fontsource');
const ff=(fam,d,w)=>`@font-face{font-family:'${fam}';font-weight:${w};src:url('file://${F}/${d}/files/${d}-latin-${w}-normal.woff2') format('woff2')}`;
const css=[700,800,900].map(w=>ff('Montserrat','montserrat',w)).join('')+[400,500,600,700].map(w=>ff('Inter','inter',w)).join('');
(async()=>{const X='/opt/pw-browsers/chromium';const b=await chromium.launch(fs.existsSync(X)?{executablePath:X}:{});const p=await b.newPage({viewport:{width:1080,height:H}});
fs.mkdirSync(OUT,{recursive:true});
const files=fs.readdirSync(SRC).filter(f=>f.endsWith('.html')&&!f.startsWith('.')).sort();
for(const [i,f] of files.entries()){let h=fs.readFileSync(path.join(SRC,f),'utf8').split('__TPL__').join(TPL);
h=h.replace(/<link[^>]*fonts\.googleapis[^>]*>/g,'').replace('</head>',`<style>${css}body{margin:0}</style></head>`);
const tmp=path.join(SRC,'.tmp.html');fs.writeFileSync(tmp,h);await p.goto('file://'+tmp);
await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
const out=path.join(OUT,String(i+1).padStart(2,'0')+'.png');await (await p.$('body > div')).screenshot({path:out});console.log(out);}
fs.rmSync(path.join(SRC,'.tmp.html'),{force:true});await b.close();})();
