"""Specs dos anúncios do low ticket no visual do gancho de tensão (lote 2026-10-20). Copy livre, cores e ganchos variados."""

CNT = r'''
function countdown(c,t,col,y){const v=Math.max(0,HOOK-t); c.save(); c.font='700 118px "JetBrains Mono"'; c.textAlign='center'; c.fillStyle=col;
  const ph=t%1, s=1+.06*Math.exp(-ph*9); c.translate(540,y); c.scale(s,s); c.globalAlpha=clamp(t*3)*(v<.02?0:1); c.fillText(v.toFixed(2),0,0); c.restore();}
'''

# ---------------- T32: notificação que não abre (o "digitando" nunca vira resposta) ----------------
HOOK32 = CNT + r'''
function lineRect(c,x,y,w,h,r,col,lw){c.strokeStyle=col;c.lineWidth=lw;c.beginPath();c.roundRect(x,y,w,h,r);c.stroke();}
function drawHook(c,t){
  countdown(c,t,'#FFFFFF',480);
  c.save(); c.globalAlpha=clamp(t*2.5);
  // telefone em traço fino (linhas paralelas)
  const X=250,Y=560,Wd=580,Hd=660;
  for(let i=0;i<6;i++) lineRect(c,X-i*3,Y-i*3,Wd+i*6,Hd+i*6,60+i*3,`rgba(220,236,248,${.5-i*.07})`,1.2);
  c.font='700 22px "JetBrains Mono"'; c.fillStyle='#8A97A3'; c.textAlign='center'; c.fillText('PACIENTE · WHATSAPP',540,Y+60);
  c.strokeStyle='rgba(138,151,163,.35)'; c.lineWidth=1; c.beginPath(); c.moveTo(X+30,Y+90); c.lineTo(X+Wd-30,Y+90); c.stroke();
  // mensagem do paciente
  const k1=oB(P(t,.25,.6),1.6); if(t>.25){ c.save(); c.translate(X+40,Y+130); c.scale(k1,k1); c.fillStyle='#152C40'; c.beginPath(); c.roundRect(0,0,400,96,24); c.fill();
    c.fillStyle='#fff'; c.font='500 32px Inter'; c.textAlign='left'; c.fillText('Quanto custa?',28,58); c.restore(); }
  // "digitando" que nunca termina
  if(t>.9){ const bx=X+Wd-40-170, by=Y+270; c.strokeStyle='#1AA6E3'; c.lineWidth=2; c.beginPath(); c.roundRect(bx,by,170,80,24); c.stroke();
    for(let i=0;i<3;i++){ const ph=t*6-i*.9; const yy=by+40-Math.max(0,Math.sin(ph))*10; c.fillStyle='#1AA6E3'; c.beginPath(); c.arc(bx+50+i*35,yy,9,0,7); c.fill(); }
    c.font='700 20px "JetBrains Mono"'; c.fillStyle='#1AA6E3'; c.textAlign='right'; c.fillText('RECEPÇÃO DIGITANDO...',X+Wd-40,by+120);}
  // brilho de tensão
  c.shadowColor='#1AA6E3'; c.shadowBlur=60; c.fillStyle='rgba(26,166,227,.25)'; c.beginPath(); c.arc(X+Wd-125,Y+310,10+4*Math.sin(t*8),0,7); c.fill();
  c.restore();
}
'''

# ---------------- T33: carregamento travado em 99% ----------------
HOOK33 = CNT + r'''
function drawHook(c,t){
  c.save(); c.globalAlpha=clamp(t*3);
  c.font='700 28px "JetBrains Mono"'; c.fillStyle='#5B6B7A'; c.textAlign='center'; c.fillText('AGENDANDO PACIENTE',540,560);
  // barra em traço fino
  const X=120,Y=600,Wd=840,Hd=80; for(let i=0;i<4;i++){c.strokeStyle=`rgba(11,26,40,${.7-i*.15})`;c.lineWidth=1.3;c.beginPath();c.roundRect(X-i*4,Y-i*4,Wd+i*8,Hd+i*8,40+i*4);c.stroke();}
  const pct=t<2.2?99*oC(P(t,.2,2.2)):99; c.fillStyle='#0F8FD0'; c.beginPath(); c.roundRect(X+8,Y+8,(Wd-16)*pct/100,Hd-16,32); c.fill();
  // hachura de lápis sobre o preenchimento
  c.strokeStyle='rgba(255,255,255,.25)'; c.lineWidth=1; for(let x=X+20;x<X+8+(Wd-16)*pct/100;x+=14){c.beginPath();c.moveTo(x,Y+10);c.lineTo(x-14,Y+Hd-10);c.stroke();}
  const flick=t>2.2&&Math.floor(t*7)%2;
  c.font='800 230px "Inter Tight"'; c.fillStyle='#0B1A28'; c.textAlign='center'; c.fillText(Math.floor(pct)+'%',540,960);
  if(t>2.2){ c.fillStyle=flick?'#0F8FD0':'#5B6B7A'; c.font='700 26px "JetBrains Mono"'; c.fillText('AGUARDANDO RESPOSTA DO PACIENTE',540,1060);}
  // spinner fino
  c.translate(540,420); c.rotate(t*5); c.strokeStyle='#0F8FD0'; c.lineWidth=4; c.beginPath(); c.arc(0,0,34,0,4.6); c.stroke();
  c.restore();
}
for(let k=0;k<6;k++) cue(.3+k*.32,F('type/key__keypress-00'+(k%3+1)+'.ogg'),{g:.18});
'''

# ---------------- T34: a gota que não cai (torneira em traço fino, âmbar) ----------------
HOOK34 = CNT + r'''
function drawHook(c,t){
  countdown(c,t,'#F5A524',410);
  c.save(); c.globalAlpha=clamp(t*2.5);
  // torneira: linhas paralelas formando o cano e o bico
  for(let i=0;i<9;i++){ const o=i*6; const a=.55-i*.05; c.strokeStyle=`rgba(255,239,214,${a})`; c.lineWidth=1.2;
    c.beginPath(); c.moveTo(80,560+o); c.lineTo(470,560+o); c.quadraticCurveTo(530+o*.3,560+o,530+o*.3,640); c.lineTo(530+o*.3,700); c.stroke(); }
  c.strokeStyle='rgba(255,239,214,.7)'; c.lineWidth=1.5; c.beginPath(); c.moveTo(500,700); c.lineTo(590,700); c.stroke();
  for(let i=0;i<7;i++){c.strokeStyle=`rgba(255,239,214,${.4-i*.05})`; c.beginPath(); c.roundRect(300-i*3,470-i*3,140+i*6,60+i*6,14); c.stroke();}
  // gota crescendo e balançando, sem cair
  const g=P(t,.2,HOOK); const r=14+30*Math.pow(g,1.2); const sw=Math.sin(t*6)*2.5*g; const cx=545, cy=712+r*1.15+sw;
  c.save(); c.shadowColor='#F5A524'; c.shadowBlur=50; c.strokeStyle='#F5A524'; c.lineWidth=2.4;
  c.beginPath(); c.moveTo(cx-8,702); c.bezierCurveTo(cx-r*1.1,cy-r*.2,cx-r,cy+r,cx,cy+r); c.bezierCurveTo(cx+r,cy+r,cx+r*1.1,cy-r*.2,cx+8,702); c.stroke(); c.restore();
  c.strokeStyle='rgba(245,165,36,.35)'; c.lineWidth=1; for(let i=1;i<6;i++){ c.beginPath(); c.arc(cx,cy+r*.2,r*i/6,Math.PI*.15,Math.PI*.85); c.stroke(); }
  // chão e alvo em traço fino
  c.strokeStyle='rgba(255,239,214,.25)'; c.lineWidth=1; c.beginPath(); c.moveTo(150,1180); c.lineTo(930,1180); c.stroke();
  for(let i=1;i<4;i++){c.beginPath(); c.ellipse(545,1180,40*i,8*i,0,0,7); c.stroke();}
  c.restore();
}
'''

D = 'dark'
SPECS = {
 'T32': dict(pal='dark', hook_bg='#050B12', hook_ac='#1AA6E3', hook_js=HOOK32, tags=[[0, 'TEMPO DE RESPOSTA'], [1, ''], [6, 'RESULTADO REAL'], [7, '']], scenes=[
   dict(line=1, els=[('t', 'mono', 'VOCÊ ESPEROU', 34, 400, 'esperou', 'rise'), ('t', 'sans', '4 SEGUNDOS', 140, 460, 'quatro', 'slam', 'A'),
                     ('t', 'ser', 'o seu paciente espera', 92, 700, 'paciente', 'rise'), ('t', 'sans', '3 HORAS.', 230, 820, 'três', 'slam', 'A')]),
   dict(line=2, pal='white', els=[('t', 'ser', 'e quando a resposta chega,', 84, 400, 'quando', 'rise'),
                     ('chat', 540, 'Mariana', [('i', 'Oi! Quanto custa o clareamento?', '14:02', None), ('o', 'R$ 900.', '17:10', 'preço')], ['preço', 'visto por último às 17:11'])]),
   dict(line=3, els=[('t', 'sans', 'ELE SOME.', 170, 470, 'some', 'slam'), ('t', 'ser', 'e você culpa', 92, 720, 'você', 'rise'), ('t', 'sans', 'O LEAD.', 180, 830, 'lead', 'wipe', 'A')]),
   dict(line=4, pal='cyan', els=[('t', 'sans', 'NÃO É O LEAD.', 120, 430, 'Não', 'rise'), ('t', 'ser', 'ninguém ensinou a recepção a', 76, 640, 'Ninguém', 'rise'),
                     ('t', 'sans', 'CONDUZIR.', 180, 760, 'conduzir', 'slam', 'A')]),
   dict(line=5, els=[('t', 'mono', 'MÉTODO A.G.E.N.D.A.', 34, 400, 'Método', 'rise', 'A'), ('t', 'sans', '10 MINUTOS', 180, 470, 'dez', 'slam'),
                     ('t', 'ser', 'e as mensagens prontas', 90, 730, 'mensagens', 'rise'), ('t', 'sans', 'PARA COPIAR.', 130, 850, 'prontas', 'wipe', 'A')]),
   dict(line=6, pal='white', els=[('logo', 400, 'cl_odonto.png'), ('t', 'mono', 'ATENDIMENTO COM A TOLKI', 28, 610, 'mudou', 'rise', 'S'),
                     ('num', 690, 300, 15, 45, 'quinze', 'quarenta', '', '%', 'A'), ('t', 'ser', 'de agendamento', 90, 1020, 'agendamento', 'rise')]),
   dict(line=7, els=[('t', 'mono', 'MÉTODO A.G.E.N.D.A.', 34, 400, None, 'rise', 'A'), ('t', 'sans', 'R$ 47', 260, 470, 'Quarenta', 'slam'),
                     ('btn', 840, 'Toque em Saiba mais', 'Toca'), ('t', 'ser', 'acesso no WhatsApp em 1 minuto', 62, 1020, 'saiba', 'rise', 'S')]),
 ]),
 'T33': dict(pal='white', hook_bg='#F6F8FA', hook_ac='#0F8FD0', hook_js=HOOK33, tags=[], scenes=[
   dict(line=1, els=[('t', 'mono', 'AGENDANDO PACIENTE', 30, 420, None, 'rise', 'S'), ('bar', 500, 99, 'noventa'), ('t', 'sans', '99%', 260, 640, 'noventa', 'slam', 'A')]),
   dict(line=2, pal=D, els=[('t', 'ser', 'é assim que a recepção perde paciente:', 70, 440, 'assim', 'rise'), ('t', 'sans', 'QUASE', 200, 590, 'quase', 'slam'),
                     ('t', 'sans', 'AGENDADO.', 170, 800, 'agendado', 'wipe', 'A')]),
   dict(line=3, els=[('chat', 400, 'Rafael', [('i', 'Quanto fica o aparelho?', '15:00', 'perguntou'), ('o', 'R$ 3.500.', '15:03', 'Recebeu')], ['sumiu', 'visto por último às 15:04']),
                     ('t', 'sans', 'E SUMIU.', 150, 1010, 'sumiu', 'slam', 'A')]),
   dict(line=4, pal='cyan', els=[('t', 'ser', 'o último passo:', 90, 400, 'último', 'rise'), ('t', 'sans', 'DOIS HORÁRIOS.', 130, 510, 'dois', 'slam'),
                     ('t', 'mono', 'TERÇA 10:00 · QUINTA 15:00', 36, 700, 'horários', 'rise', 'A'), ('t', 'ser', 'em vez de', 70, 830, 'vez', 'rise'),
                     ('t', 'sans', '"QUAL FICA MELHOR?"', 90, 920, 'qual', 'wipe')]),
   dict(line=5, pal=D, els=[('t', 'mono', 'MÉTODO A.G.E.N.D.A.', 34, 400, 'São', 'rise', 'A'), ('t', 'sans', 'ACOLHE. GERA VALOR.', 96, 480, 'seis', 'rise'),
                     ('t', 'sans', 'ENTENDE. NEUTRALIZA.', 96, 590, 'passos', 'rise'), ('t', 'sans', 'DEFINE. ASSEGURA.', 96, 700, 'frase', 'rise', 'A'),
                     ('t', 'ser', 'com a frase pronta para cada um', 70, 850, 'pronta', 'rise')]),
   dict(line=6, els=[('t', 'mono', 'CLÍNICAS QUE ATENDEM COM A TOLKI', 28, 420, None, 'rise', 'S'), ('num', 520, 280, 0, 470, 'quatrocentas', 'clínicas', '+', '', 'A'),
                     ('t', 'ser', 'e contando', 84, 860, 'atendem', 'rise')]),
   dict(line=7, pal='cyan', els=[('bar', 430, 100, 'cem'), ('t', 'sans', '100%', 220, 540, 'cem', 'slam'), ('btn', 840, 'Toque em Saiba mais', 'Toca'),
                     ('t', 'ser', 'Método A.G.E.N.D.A. · R$ 47', 62, 1020, 'saiba', 'rise')]),
 ]),
 'T34': dict(pal='amber', hook_bg='#0C0906', hook_ac='#F5A524', hook_js=HOOK34, tags=[[3, 'A CONTA'], [4, ''], [6, 'RESULTADO REAL'], [7, '']], scenes=[
   dict(line=1, els=[('t', 'ser', 'uma gota', 120, 480, 'gota', 'rise'), ('t', 'sans', 'NÃO PARECE NADA.', 120, 650, 'parece', 'wipe', 'A')]),
   dict(line=2, els=[('t', 'ser', 'um paciente perdido por dia', 84, 470, 'paciente', 'rise'), ('t', 'sans', 'TAMBÉM NÃO.', 160, 610, 'também', 'slam')]),
   dict(line=3, pal='navy', els=[('t', 'mono', 'EXEMPLO ILUSTRATIVO', 24, 380, None, 'rise', 'S'), ('num', 440, 180, 0, 22, 'vinte', 'por', '', ' / mês'),
                     ('t', 'ser', 'x tratamento de R$ 900', 72, 680, 'tratamento', 'rise'), ('num', 800, 190, 0, 19800, 'quase', 'mil', 'R$ ', '', 'A')]),
   dict(line=4, els=[('t', 'ser', 'e quase sempre ele escapa no mesmo lugar:', 64, 440, 'escapa', 'rise'), ('t', 'sans', '"QUANTO CUSTA?"', 140, 600, 'quanto', 'slam', 'A')]),
   dict(line=5, pal='navy', els=[('t', 'mono', 'MÉTODO A.G.E.N.D.A.', 34, 420, 'Método', 'rise', 'A'), ('t', 'ser', 'fecha essa torneira em', 86, 520, 'fecha', 'rise'),
                     ('t', 'sans', '10 MINUTOS.', 190, 650, 'dez', 'slam', 'A')]),
   dict(line=6, els=[('t', 'mono', 'CLÍNICA QUE ATENDE COM A TOLKI', 26, 400, None, 'rise', 'S'), ('t', 'ser', 'uma atendente', 86, 470, 'atendente', 'rise'),
                     ('num', 580, 300, 21, 62, 'vinte', 'sessenta', '', '', 'A'), ('t', 'ser', 'contratos em um mês', 86, 920, 'contratos', 'rise')]),
   dict(line=7, pal='navy', els=[('t', 'mono', 'MÉTODO A.G.E.N.D.A.', 34, 400, None, 'rise', 'A'), ('t', 'sans', 'R$ 47', 260, 470, 'Quarenta', 'slam'),
                     ('btn', 840, 'Toque em Saiba mais', 'Toca'), ('t', 'ser', 'acesso no WhatsApp em 1 minuto', 62, 1020, 'saiba', 'rise', 'S')]),
 ]),
}
