// frames.js: captura o reel.html quadro a quadro (30 fps) chamando window.__tick(t).
// Uso (na pasta do Reel, com playwright instalado ali): node <repo>/tools/reel-motion/frames.js <segundos> [quadros,separados,por,vírgula]
const path=require('path');const {chromium}=require(require.resolve('playwright',{paths:[process.cwd()]}));const fs=require('fs');
(async()=>{const X='/opt/pw-browsers/chromium';const b=await chromium.launch(fs.existsSync(X)?{executablePath:X}:{});const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.resolve('reel.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
const FPS=30,T=+process.argv[2],only=process.argv[3];fs.mkdirSync('f',{recursive:true});
const list=only?only.split(',').map(Number):[...Array(Math.ceil(T*FPS)).keys()];
for(const i of list){await p.evaluate(t=>window.__tick(t),i/FPS);await p.screenshot({path:'f/'+String(i).padStart(5,'0')+'.jpg',type:'jpeg',quality:92});}
await b.close();})();
