"""Gerador de cenas do low ticket (Método A.G.E.N.D.A.) no padrão visual do gancho de tensão.
Só o visual do modelo: fundo chapado, três vozes de tipografia (serif itálico, Inter Tight 800, mono), traço fino,
rastro de luz, legenda palavra a palavra. Copy, cores, ganchos e elementos variam por vídeo (spec em specs.py).
Área útil do Reels para anúncio: conteúdo entre y 290 e 1250, legenda em y 1300.
Uso: python3 gen.py T32 WORK  -> WORK/page.html (WORK tem tl.js do voz.py)"""
import json, os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import core

PAL = {
    'dark':  dict(bg='#050B12', fg='#FFFFFF', ac='#1AA6E3', sub='#8A97A3', card='#0B1A28', line='#1C3347', bub='#152C40'),
    'white': dict(bg='#F6F8FA', fg='#0B1A28', ac='#0F8FD0', sub='#5B6B7A', card='#FFFFFF', line='#D5DEE8', bub='#EEF3F7'),
    'cyan':  dict(bg='#1AA6E3', fg='#06233A', ac='#FFFFFF', sub='#0B4A6E', card='#0B6E9E', line='#5CC3EE', bub='#0E5A80'),
    'amber': dict(bg='#0C0906', fg='#FFF7EC', ac='#F5A524', sub='#A8977F', card='#1A140D', line='#3A2C1B', bub='#2A2014'),
    'navy':  dict(bg='#071827', fg='#FFFFFF', ac='#F5A524', sub='#8FA3B8', card='#0E2438', line='#1F3A55', bub='#163049'),
}


def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;')


def build(spec):
    css, body, js_el = [], [], []
    css.append('#wm{display:none}#end{display:none!important}'
               '#tag{top:300px}#cap{top:1300px;font-size:44px;padding:0 100px}'
               '.btn{position:absolute;left:190px;width:700px;height:130px;border-radius:65px;display:flex;align-items:center;justify-content:center;'
               'font-family:"Inter Tight";font-weight:800;font-size:50px;letter-spacing:-.01em}'
               '.cbox{position:absolute;left:290px;width:500px;height:170px;background:#fff;border-radius:28px;display:flex;align-items:center;justify-content:center}'
               '.cbox img{max-width:76%;max-height:70%}'
               '.chat2{position:absolute;left:90px;width:900px;border-radius:36px;overflow:hidden;border:2px solid}'
               '.chat2 .hd{display:flex;align-items:center;gap:22px;padding:26px 32px;border-bottom:2px solid}'
               '.chat2 .av{width:70px;height:70px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:"Inter Tight";font-weight:800;font-size:30px}'
               '.chat2 .nm{font-family:"Inter Tight";font-weight:700;font-size:34px}.chat2 .st{font-family:Inter;font-size:23px}'
               '.chat2 .ex{margin-left:auto;font-family:"JetBrains Mono";font-weight:700;font-size:16px;letter-spacing:2px;text-align:right;line-height:1.35}'
               '.chat2 .bd{padding:30px;display:flex;flex-direction:column;gap:20px}'
               '.b2{max-width:690px;padding:20px 26px 12px;border-radius:26px;font-family:Inter;font-size:36px;line-height:1.3}'
               '.b2 small{display:block;text-align:right;font-size:19px;opacity:.6;margin-top:6px}'
               '.b2.i{align-self:flex-start;border-top-left-radius:8px}.b2.o{align-self:flex-end;border-top-right-radius:8px}'
               '.barw{position:absolute;left:120px;width:840px;height:70px;border-radius:35px;border:3px solid;overflow:hidden}'
               '.barf{height:100%;width:0}')
    scs, bgs = [], []
    nid = 0
    for si, sc in enumerate(spec['scenes']):
        p = PAL[sc.get('pal', spec['pal'])]
        sid = f'z{si}'; inner = []
        bgs.append([sc['line'], p['bg'], p['fg'], p['ac']])
        for it in sc['els']:
            nid += 1; eid = f'e{nid}'; k = it[0]
            if k == 't':
                _, cls, txt, size, y, word, anim = it[:7]
                col = p['ac'] if 'A' in it[7:] else (p['sub'] if 'S' in it[7:] else p['fg'])
                cl = {'ser': 'ab ser', 'sans': 'ab sans', 'mono': 'ab mono'}[cls]
                extra = 'letter-spacing:6px;' if cls == 'mono' else ''
                inner.append(f'<div id="{eid}" class="{cl}" style="top:{y}px;font-size:{size}px;color:{col};{extra}">{esc(txt)}</div>')
                js_el.append(dict(id=eid, l=sc['line'], w=word, a=anim, y=y + size * .55))
            elif k == 'chat':
                _, y, name, msgs, status = it
                rows = ''.join(f'<div id="{eid}m{j}" class="b2 {"i" if s == "i" else "o"}" style="background:{p["bub"] if s == "i" else p["ac"]};color:{p["fg"] if s == "i" else p["bg"]}">{esc(tx)}<small>{tm}</small></div>'
                               for j, (s, tx, tm, w) in enumerate(msgs))
                inner.append(f'<div id="{eid}" class="chat2" style="top:{y}px;background:{p["card"]};border-color:{p["line"]};color:{p["fg"]}">'
                             f'<div class="hd" style="border-color:{p["line"]}"><div class="av" style="background:{p["bub"]};color:{p["fg"]}">{name[0]}</div><div><div class="nm">{name}</div>'
                             f'<div class="st" id="{eid}st" style="color:{p["sub"]}">online</div></div><div class="ex" style="color:{p["sub"]}">EXEMPLO<br>ILUSTRATIVO</div></div>'
                             f'<div class="bd">{rows}</div></div>')
                js_el.append(dict(id=eid, l=sc['line'], w=None, a='chat', msgs=[[j, w] for j, (_, _, _, w) in enumerate(msgs)], status=status))
            elif k == 'num':
                _, y, size, v0, v1, w0, w1, pre, suf = it[:9]
                col = p['ac'] if 'A' in it[9:] else p['fg']
                inner.append(f'<div id="{eid}" class="ab sans" style="top:{y}px;font-size:{size}px;line-height:1;color:{col};text-transform:none;letter-spacing:-.04em"></div>')
                js_el.append(dict(id=eid, l=sc['line'], w=w0, w1=w1, a='num', v0=v0, v1=v1, pre=pre, suf=suf))
            elif k == 'logo':
                _, y, src = it
                inner.append(f'<div id="{eid}" class="cbox" style="top:{y}px"><img src="assets/{src}"></div>')
                js_el.append(dict(id=eid, l=sc['line'], w=None, a='pop'))
            elif k == 'btn':
                _, y, txt, word = it
                inner.append(f'<div id="{eid}" class="btn" style="top:{y}px;background:{p["ac"]};color:{p["bg"]};box-shadow:0 0 60px {p["ac"]}88">{esc(txt)}</div>')
                js_el.append(dict(id=eid, l=sc['line'], w=word, a='pop'))
            elif k == 'bar':
                _, y, pct, w0 = it
                inner.append(f'<div id="{eid}" class="barw" style="top:{y}px;border-color:{p["ac"]}"><div class="barf" id="{eid}f" style="background:{p["ac"]}"></div></div>')
                js_el.append(dict(id=eid, l=sc['line'], w=w0, a='bar', pct=pct))
        end = 'ENDT+3' if si == len(spec['scenes']) - 1 else f'LS({spec["scenes"][si + 1]["line"]})'
        scs.append(f"['{sid}',LS({sc['line']}),{end}]")
        body.append(f'<div class="sc" id="{sid}">' + ''.join(inner) + '</div>')
    first_bg = PAL[spec['pal']]['bg']
    body.insert(0, '<div class="sc" id="zH"></div>')
    tags = json.dumps(spec.get('tags', []))
    js = r'''
CM.length=0; window.bgAt=t=>({show:0,src:0,blur:0,dim:1,scale:1});
const EL=__EL__, BGS=__BGS__, PALBG='__BG0__';
const SC=[['zH',0,LS(1)],__SCS__];
const TAGS=__TAGS__.map(([l,s])=>[l===0?0:LS(l),s]);
const WT=(l,w)=>w==null?LS(l)+.05:(typeof w==='number'?LS(l)+w:TW(l,w));
EL.forEach(e=>{ if(e.a==='wipe'){ e.cm=SW(WT(e.l,e.w)-.06,e.y,.6);} });
__COMETS__
function bgNow(t){let b=[0,PALBG,'#FFFFFF','#1AA6E3']; if(t<HOOK) return [0,'__HOOKBG__','#FFFFFF','__HOOKAC__']; BGS.forEach(x=>{if(t>=LS(x[0]))b=x}); return b;}
function render(t){
  scenes(t,SC,TAGS);
  const B=bgNow(t); $('stage').style.background=B[1]; $('cap').style.color=B[2]; $('tag').style.color=B[3];
  document.querySelectorAll('#cap span.on').forEach(s=>s.style.color=B[3]);
  EL.forEach(e=>{ const el=$(e.id); if(t<LS(e.l)-.1||t>(e.l<NL?LS(e.l+1):ENDT+3)) return; const t0=WT(e.l,e.w);
    if(e.a==='rise') rise(el,t,t0);
    else if(e.a==='wipe') wipe(el,t,e.cm);
    else if(e.a==='pop') pop(el,t,t0,.4);
    else if(e.a==='slam'){ const k=P(t,t0,t0+.3); el.style.opacity=t>=t0?1:0; el.style.transform=`scale(${t>=t0?lerp(1.5,1,oQ(k)):1})`; el.style.filter=k<1&&t>=t0?`blur(${(1-k)*16}px)`:''; if(t>=t0+.05){const [x,y]=shake(t,t0+.05,16,.35); el.style.translate=`${x}px ${y}px`;}}
    else if(e.a==='num'){ const a=t0, b=TW(e.l,e.w1); const k=oC(P(t,a,b)); el.style.opacity=t>=a-.05?1:0; el.textContent=e.pre+fmtBR(Math.round(lerp(e.v0,e.v1,k)))+e.suf; if(t>=b){const [x,y]=shake(t,b,14,.3); el.style.translate=`${x}px ${y}px`;}}
    else if(e.a==='chat'){ const k=oQ(P(t,LS(e.l)-.05,LS(e.l)+.45)); el.style.opacity=k; el.style.transform=`translateY(${(1-k)*200}px)`;
      e.msgs.forEach(([j,w])=>{const m=$(e.id+'m'+j); const tt=WT(e.l,w); m.style.opacity=t>=tt?1:0; m.style.transform=`scale(${t>=tt?oB(P(t,tt,tt+.3),1.5):.6})`;});
      if(e.status){const [w,s]=e.status; if(t>=WT(e.l,w)) $(e.id+'st').textContent=s;} }
    else if(e.a==='bar'){ const k=P(t,LS(e.l),t0); $(e.id+'f').style.width=(lerp(0,e.pct,oC(k)))+'%'; rise(el,t,LS(e.l));}
  });
  hctx.clearRect(0,0,1080,1920); if(t<HOOK) drawHook(hctx,t); else if(typeof drawArt==='function') drawArt(hctx,t);
  captions(t); document.querySelectorAll('#cap span.on').forEach(s=>s.style.color=B[3]); comet(t);
}
__HOOKJS__
'''
    rep = {'__EL__': json.dumps(js_el, ensure_ascii=False), '__BGS__': json.dumps(bgs), '__BG0__': first_bg, '__SCS__': ','.join(scs),
           '__TAGS__': tags, '__HOOKJS__': spec['hook_js'], '__HOOKBG__': spec.get('hook_bg', '#050B12'), '__HOOKAC__': spec.get('hook_ac', '#1AA6E3'),
           '__COMETS__': spec.get('comets', '')}
    for a, b in rep.items(): js = js.replace(a, b)
    return '\n'.join(css), '\n'.join(body), js


if __name__ == '__main__':
    k, work = sys.argv[1], sys.argv[2]
    sp = importlib.util.spec_from_file_location('s', os.path.join(HERE, 'specs.py')); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    css, body, js = build(m.SPECS[k])
    print(core.page(work, css, body, js))
