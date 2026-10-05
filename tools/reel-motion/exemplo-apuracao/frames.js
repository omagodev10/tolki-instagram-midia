const {chromium}=require('/tmp/claude-0/-home-claude-tolki-instagram-midia/3da1e8ac-fdd4-5d65-bb02-a0eb10d52cec/scratchpad/noite/node_modules/playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/reel.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
const FPS=30,T=+process.argv[2],only=process.argv[3];fs.mkdirSync('f',{recursive:true});
const list=only?only.split(',').map(Number):[...Array(Math.ceil(T*FPS)).keys()];
for(const i of list){await p.evaluate(t=>window.__tick(t),i/FPS);await p.screenshot({path:'f/'+String(i).padStart(5,'0')+'.jpg',type:'jpeg',quality:92});}
await b.close();})();
