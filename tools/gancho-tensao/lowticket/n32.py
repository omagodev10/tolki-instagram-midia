"""N32 (02/11): a N1 vencedora em vídeo curto 9:16 para Reels e Stories (70%), voz da Luana no padrão de 26/10, sem gancho de 6 s.
Hipótese H25: no Reels o clique custa R$ 1 a 1,60 contra R$ 4,50 no feed; um vídeo nativo com a mesma manchete compra esse clique sem perder a venda.
Só prova permitida (Odonto Excellence 15% para 45%, atendimento com a Tolki); conversa com "exemplo ilustrativo"."""
INK = '#15120E'; PAPER = '#F4EFE6'; RED = '#B3261E'; MUTE = '#7A6E5E'
CSS = r'''
#stage{background:#F4EFE6}#hgc,#wm,#end,#tag{display:none!important}
#cap{left:0;width:1080px;top:1205px;padding:0 130px;text-align:center;font-family:'Inter Tight';font-weight:700;font-size:44px;line-height:1.42;color:#F4EFE6}
#cap span{background:#15120E;padding:2px 11px;margin:0;border-radius:6px}#cap span.on{color:#FFD400}
.b{position:absolute;left:72px;width:936px}
.t{font-family:'Inter Tight';font-weight:800;letter-spacing:-.03em;color:#15120E;text-transform:none}
.m{font-family:'JetBrains Mono';font-weight:700;letter-spacing:5px;text-transform:uppercase}
.s{font-family:'Instrument Serif';font-style:italic;color:#4A4036}
#mast{top:280px}#mast .n{font-family:'Instrument Serif';font-size:68px;color:#15120E;letter-spacing:-1px}
#mast .r{height:3px;background:#15120E;margin:14px 0}
#mast .x{font-size:20px;color:#7A6E5E;display:flex;justify-content:space-between}
#hK{top:470px;font-size:24px;color:#B3261E}#hT{top:520px;font-size:124px;line-height:1.02}
#sK{top:300px;font-size:26px;color:#B3261E}#sN{top:345px;font-size:76px}
#nums{top:470px;display:flex;align-items:flex-end;gap:26px}
.big{font-family:'Inter Tight';font-weight:800;letter-spacing:-.05em;line-height:.9}
#n1{font-size:150px;color:#7A6E5E}#ar{font-size:90px;color:#15120E;font-family:'Inter Tight';font-weight:800;padding-bottom:30px}#n2{font-size:262px;color:#B3261E}
#bar{top:850px;height:46px;background:#E4DBCB;border-radius:8px;overflow:hidden}#bf{height:100%;background:#B3261E;width:15%}
#sD{top:930px;font-size:64px;line-height:1.12}
#chat{top:300px;background:#fff;border:3px solid #15120E;border-radius:30px;padding:30px 34px;height:800px}
#chat .e{font-size:22px;color:#B3261E;display:flex;justify-content:space-between;letter-spacing:3px}
.bb{position:absolute;max-width:720px;font-family:Inter;font-weight:700;font-size:62px;line-height:1.15;padding:26px 36px;border-radius:30px}
#b1{left:34px;top:130px;background:#EDE6D8;color:#15120E}#b2{right:34px;top:320px;background:#15120E;color:#F4EFE6}
#b3{left:34px;top:530px;width:720px;background:none;color:#B3261E;font-family:'JetBrains Mono';font-size:40px;letter-spacing:1px;padding:0;line-height:1.25}
#mT{top:300px;font-size:30px;color:#B3261E}#mH{top:350px;font-size:96px;line-height:1.02}
#ls{top:590px;display:grid;grid-template-columns:repeat(6,1fr);gap:14px}
.lt{height:170px;background:#15120E;color:#F4EFE6;font-family:'Inter Tight';font-weight:800;font-size:110px;display:flex;align-items:center;justify-content:center;border-radius:14px}
#pl{top:810px;background:#FFD400;color:#15120E;font-size:66px;padding:22px 34px;border-radius:16px;width:auto}
#mP{top:960px;font-size:62px}
#cA{top:330px;font-size:112px;line-height:1.02}#cP{top:600px;font-size:300px;color:#B3261E}
#cB{top:930px;width:auto;left:190px;background:#15120E;color:#F4EFE6;font-family:'Inter Tight';font-weight:800;font-size:72px;padding:30px 70px;border-radius:70px}
#cS{top:1115px;font-size:22px;color:#7A6E5E;width:936px;text-align:center}
'''
BODY = '''<div class="sc" id="a1"><div class="b" id="mast"><div class="n">Gestão de Clínicas</div><div class="r"></div><div class="m x"><span>Atendimento</span><span>WhatsApp</span></div></div>
<div class="b m" id="hK">Caso real · atendimento com a Tolki</div><div class="b t" id="hT">Clínica triplica a taxa de agendamento</div></div>
<div class="sc" id="a2"><div class="b m" id="sK">Caso real · atendimento com a Tolki</div><div class="b t" id="sN">Odonto Excellence</div>
<div class="b" id="nums"><div class="big" id="n1">15%</div><div id="ar">→</div><div class="big" id="n2">15%</div></div><div class="b" id="bar"><div id="bf"></div></div><div class="b s" id="sD">depois de mudar o atendimento</div></div>
<div class="sc" id="a3"><div class="b" id="chat"><div class="m e"><span>WhatsApp da clínica</span><span>Exemplo ilustrativo</span></div>
<div class="bb" id="b1">Oi! Quanto custa?</div><div class="bb" id="b2">R$ 900.</div><div class="bb" id="b3">visualizou e sumiu</div></div></div>
<div class="sc" id="a4"><div class="b m" id="mT">Método A.G.E.N.D.A.</div><div class="b t" id="mH">Da pergunta do preço ao horário marcado</div>
<div class="b" id="ls"><div class="lt">A</div><div class="lt">G</div><div class="lt">E</div><div class="lt">N</div><div class="lt">D</div><div class="lt">A</div></div>
<div class="b t" id="pl">Horário marcado</div><div class="b s" id="mP">com as mensagens prontas</div></div>
<div class="sc" id="a5"><div class="b t" id="cA">Aula de 10 minutos</div><div class="b big" id="cP">R$ 47</div><div class="b" id="cB">Saiba mais →</div><div class="b m" id="cS">Método A.G.E.N.D.A. · garantia de 7 dias</div></div>
'''
JS = r'''
window.bgAt=t=>({show:false,src:0,scale:1,blur:0,dim:0});
const SC=[['a1',0,LS(2)],['a2',LS(2),LS(3)],['a3',LS(3),LS(4)],['a4',LS(4),LS(5)],['a5',LS(5),99]];
const T45=TW(2,'quarenta'), TDEP=TW(2,'depois');
const LT=qa('.lt');
cue(T(1,0),'tick',{g:.3,f:900}); cue(TW(1,'triplicou'),'tick',{g:.4,f:1400}); cue(T45,'tick',{g:.5,f:1600});
cue(TW(3,'quanto'),'tick',{g:.35,f:1100}); cue(TW(3,'preço'),'tick',{g:.35,f:1100}); cue(TW(3,'some'),'tick',{g:.4,f:500});
LT.forEach((e,i)=>cue(TW(4,'agenda')+i*.08,'tick',{g:.22,f:1200+i*80})); cue(TW(5,'quarenta'),'tick',{g:.45,f:1500});
const rs=(id,t,t0,dist=46)=>{const e=$(id),k=oQ(P(t,t0,t0+.45));e.style.opacity=clamp(k*1.6);e.style.transform=`translateY(${(1-k)*dist}px)`};
const pp=(id,t,t0)=>{const e=$(id),k=P(t,t0,t0+.32);e.style.opacity=clamp(k*3);e.style.transform=`scale(${k>0?oB(k,1.4):.7})`};
function render(t){SC.forEach(([id,a,b])=>{$(id).style.display=(t>=a&&t<b)?'block':'none'});
  captions(t);
  rs('hK',t,0);rs('hT',t,.15);
  rs('sK',t,LS(2));rs('sN',t,LS(2)+.08);rs('sD',t,TDEP);
  const k=oC(P(t,T45,T45+.75)),v=Math.round(lerp(15,45,k));$('n2').textContent=v+'%';$('bf').style.width=lerp(15,45,k)+'%';
  $('n2').style.transform=`scale(${t>=T45?1+.08*Math.exp(-(t-T45-.75>0?t-T45-.75:0)*6):1})`;$('n2').style.transformOrigin='0 100%';
  pp('b1',t,TW(3,'quanto')-.12);pp('b2',t,TW(3,'preço')-.1);rs('b3',t,TW(3,'some')-.05,20);
  rs('mT',t,LS(4));rs('mH',t,LS(4)+.1);LT.forEach((e,i)=>{const a=TW(4,'agenda')+i*.08,q=P(t,a,a+.3);e.style.opacity=clamp(q*3);e.style.transform=`scale(${q>0?oB(q,1.5):.6})`});
  pp('pl',t,TW(4,'horário'));rs('mP',t,TW(4,'mensagens')-.1);
  rs('cA',t,LS(5));pp('cP',t,TW(5,'quarenta')-.1);pp('cB',t,TW(5,'toca')-.1);rs('cS',t,TW(5,'toca'));
  const u=TW(5,'toca')+.5;if(t>u){$('cB').style.transform=`scale(${1+.035*Math.sin((t-u)*5)})`}
}
'''
