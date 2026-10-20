"""Procedural music + SFX for the Tolki motions. Everything is synthesized (no samples, no copyrighted audio)."""
import numpy as np, json, sys
from scipy import signal
from scipy.io import wavfile

SR = 44100
rng = np.random.default_rng(7)

def T(d): return np.arange(int(d * SR)) / SR
def env_exp(d, tau): return np.exp(-T(d) / tau)
def adsr(n, a=.005, r=.05):
    e = np.ones(n); na = max(1, int(a*SR)); nr = max(1, int(r*SR))
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return e
def bp(x, lo, hi, order=2):
    sos = signal.butter(order, [lo, hi], 'bandpass', fs=SR, output='sos'); return signal.sosfilt(sos, x)
def lp(x, f, order=2):
    sos = signal.butter(order, f, 'lowpass', fs=SR, output='sos'); return signal.sosfilt(sos, x)
def hp(x, f, order=2):
    sos = signal.butter(order, f, 'highpass', fs=SR, output='sos'); return signal.sosfilt(sos, x)
def noise(d): return rng.standard_normal(int(d*SR))
def midi(n): return 440 * 2 ** ((n - 69) / 12)

def sweep_filter(x, f0, f1, width=.6, mode='bp'):
    """time-varying filter via STFT masking (vectorised)"""
    f, tt, Z = signal.stft(x, SR, nperseg=1024)
    k = np.linspace(0, 1, Z.shape[1])
    fc = f0 * (f1 / f0) ** k
    F = f[:, None]; C = fc[None, :]
    if mode == 'bp':
        m = np.exp(-(np.log2(np.maximum(F, 1) / C) ** 2) / (2 * width ** 2))
    else:  # lowpass
        m = 1 / (1 + (F / C) ** 4)
    _, y = signal.istft(Z * m, SR, nperseg=1024)
    return y[:len(x)]

def reverb_ir(d=1.8, tau=.5, seed=1):
    r = np.random.default_rng(seed); n = int(d * SR)
    ir = r.standard_normal((n, 2)) * np.exp(-np.arange(n) / SR / tau)[:, None]
    ir = np.stack([lp(ir[:, 0], 6000), lp(ir[:, 1], 6000)], 1); ir[:int(.012*SR)] *= np.linspace(0, 1, int(.012*SR))[:, None]
    return ir / np.sqrt((ir ** 2).sum(0)).max()
IR = reverb_ir(); IR_BIG = reverb_ir(3.2, .9, 3)
def verb(x, mix=.25, big=False):
    x = st(x); ir = IR_BIG if big else IR
    w = np.stack([signal.fftconvolve(x[:, 0], ir[:, 0]), signal.fftconvolve(x[:, 1], ir[:, 1])], 1)
    out = np.zeros_like(w); out[:len(x)] = x; return out * (1 - mix) + w * mix
def st(x, pan=0.):
    if x.ndim == 2: return x
    l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
    return np.stack([x * l * 1.414, x * r * 1.414], 1)

# ------------------------------------------------------------------ drums
def kick(g=1., punch=1.):
    t = T(.5); f = 45 + 110 * np.exp(-t / .045) * punch
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * np.exp(-t / .28) + noise(.5) * np.exp(-t / .003) * .25
    return np.tanh(x * 1.6) * g * .9
def clap(g=1.):
    d = .35; x = np.zeros(int(d*SR))
    for i, o in enumerate([0, .011, .022, .031]):
        n = noise(d - o) * np.exp(-T(d - o) / (.006 if i < 3 else .09))
        x[int(o*SR):] += n
    return bp(x, 900, 4200) * g * .55
def hat(g=1., open_=False):
    d = .25 if open_ else .06; x = hp(noise(d), 7500, 4) * np.exp(-T(d) / (.07 if open_ else .014))
    return x * g * .45
def rim(g=1.):
    t = T(.08); x = (np.sin(2*np.pi*1750*t) * .6 + bp(noise(.08), 2000, 6000)) * np.exp(-t / .012)
    return x * g * .5
def shaker(g=1.):
    d = .09; x = bp(noise(d), 5000, 11000) * np.sin(np.linspace(0, np.pi, int(d*SR))) ** 2
    return x * g * .3

# ------------------------------------------------------------------ tonal
def additive(f, d, harm=10, decay=(1.5, 3.), bright=1., detune=0., saw=True):
    t = T(d); x = np.zeros_like(t)
    for k in range(1, harm + 1):
        amp = (1 / k if saw else (1 / k if k % 2 else 0)) * np.exp(-t * (decay[0] + k * decay[1] / bright))
        x += amp * np.sin(2 * np.pi * f * k * (1 + detune) * t + rng.uniform(0, 6.28))
    return x
def pluck(n, d=.4, g=1., bright=1.):
    f = midi(n); x = additive(f, d, 12, (3., 2.2), bright) + .5 * additive(f * 1.004, d, 8, (3., 2.6), bright)
    return x * adsr(len(x), .002, .03) * g * .22
def keys(n, d=1.2, g=1.):  # soft electric-piano-ish
    f = midi(n); t = T(d)
    x = np.sin(2*np.pi*f*t) * np.exp(-t/.9) + .35*np.sin(2*np.pi*2*f*t)*np.exp(-t/.35) + .12*np.sin(2*np.pi*3.01*f*t)*np.exp(-t/.15)
    x += .08 * np.sin(2*np.pi*14*f*t) * np.exp(-t/.02)
    return x * adsr(len(x), .003, .08) * g * .28
def pad(notes, d, g=1., cutoff=1800):
    t = T(d); x = np.zeros_like(t)
    for n in notes:
        for dt in (-.006, 0, .007):
            f = midi(n) * (1 + dt); ph = rng.uniform(0, 6.28)
            x += signal.sawtooth(2 * np.pi * f * t + ph) * .33
    x = lp(x, cutoff, 2)
    return x * adsr(len(x), min(.4, d/3), min(.6, d/3)) * g * .07
def sub(n, d, g=1.):
    t = T(d); f = midi(n); x = np.sin(2*np.pi*f*t) + .25*np.sin(4*np.pi*f*t)
    return np.tanh(x * 1.2) * adsr(len(x), .006, .04) * g * .5

# ------------------------------------------------------------------ sfx
def sfx(kind, o):
    g = o.get('g', 1.); d = o.get('d', .5)
    if kind == 'whoosh':
        x = sweep_filter(noise(d), 300, 5000, .7) * np.sin(np.linspace(0, np.pi, int(d*SR))) ** 1.5
        return verb(x * g * 1.1, .2)
    if kind == 'whooshUp':
        d = o.get('d', .45); x = sweep_filter(noise(d), 800, 9000, .5) * np.linspace(0, 1, int(d*SR)) ** 2
        return verb(x * g * .9, .25)
    if kind == 'whooshDown':
        d = o.get('d', .5); x = sweep_filter(noise(d), 6000, 300, .6) * np.linspace(1, 0, int(d*SR)) ** 1.2
        return verb(x * g * .9, .2)
    if kind == 'riser':
        t = T(d); x = sweep_filter(noise(d), 200, 8000, .5) * (t / d) ** 2.2
        tone = np.sin(2*np.pi*np.cumsum(200 + 900*(t/d)**2)/SR) * (t/d)**3 * .15
        return verb((x + tone) * g, .3)
    if kind == 'impact':
        t = T(1.6); f = 32 + 60*np.exp(-t/.08)
        x = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/.5) + lp(noise(1.6), 900)*np.exp(-t/.09)*.9
        return verb(np.tanh(x*2)*g*.8, .35, True)
    if kind == 'hit':
        t = T(.6)
        k = np.zeros(len(t)); kk = kick(1, 1.3); k[:len(kk)] = kk[:len(t)]; c = np.zeros(len(t)); cl = clap(1.); c[:len(cl)] = cl
        return verb((k*.8 + c*.7) * g, .25)
    if kind == 'tick':
        t = T(.05); x = np.sin(2*np.pi*o.get('f', 2400)*t) * np.exp(-t/.006) + hp(noise(.05), 4000)*np.exp(-t/.003)*.4
        return st(x * g * .5)
    if kind == 'click':
        t = T(.04); x = bp(noise(.04), 1500, 7000) * np.exp(-t/.004)
        return st(x * g * .8)
    if kind == 'pop':
        t = T(.18); f = o.get('f', 520); fr = f * (1 + 1.2*np.exp(-t/.02))
        x = np.sin(2*np.pi*np.cumsum(fr)/SR) * np.exp(-t/.05)
        return verb(x * g * .55, .15)
    if kind == 'typeBurst':
        x = np.zeros(int(d*SR)); tt = 0
        while tt < d - .05:
            n = int(tt*SR); c = bp(noise(.03), 1800, 6500) * np.exp(-T(.03)/.004) * rng.uniform(.5, 1)
            x[n:n+len(c)] += c[:len(x)-n]; tt += rng.uniform(.05, .11)
        return verb(x * g * .7, .1)
    if kind == 'notif':   # generic 2-note chime (not any app's real sound)
        out = np.zeros(int(.9*SR))
        for i, (n, o_) in enumerate([(84, 0), (91, .09)]):
            t = T(.8); f = midi(n); x = (np.sin(2*np.pi*f*t) + .3*np.sin(2*np.pi*2*f*t)) * np.exp(-t/.22)
            s = int(o_*SR); out[s:s+len(x)] += x[:len(out)-s]
        return verb(out * g * .35, .25)
    if kind == 'send':
        t = T(.22); f = 500 + 1400 * (t/.22)
        x = np.sin(2*np.pi*np.cumsum(f)/SR) * np.sin(np.linspace(0, np.pi, len(t))) * .5 + sweep_filter(noise(.22), 1000, 6000, .5)*.4
        return verb(x * g * .5, .2)
    if kind == 'ding':  # bell / register ding
        t = T(1.4); f = o.get('f', 1568); x = np.zeros_like(t)
        for r, a, dc in [(1, 1, .6), (2.76, .5, .3), (5.4, .25, .15), (8.93, .12, .08)]:
            x += a * np.sin(2*np.pi*f*r*t) * np.exp(-t/dc)
        return verb(x * g * .3, .3)
    if kind == 'cash':
        out = np.zeros(int(1.5*SR)); d1 = sfx('click', {'g': 1})[:, 0]; out[:len(d1)] += d1
        mech = bp(noise(.12), 400, 3000) * np.exp(-T(.12)/.03); s = int(.05*SR); out[s:s+len(mech)] += mech*.8
        dg = sfx('ding', {'g': 1.2, 'f': 2093})[:, 0]; s = int(.12*SR); out[s:s+len(dg)] += dg[:len(out)-s]
        return st(out * g)
    if kind == 'stamp':
        t = T(.5); x = lp(noise(.5), 700)*np.exp(-t/.03)*1.5 + np.sin(2*np.pi*70*t)*np.exp(-t/.08)
        return verb(np.tanh(x*2) * g * .8, .2)
    if kind == 'counter':  # fast ticking while numbers roll
        x = np.zeros(int(d*SR)); rate = o.get('rate', 22)
        for i in range(int(d*rate)):
            s = int(i/rate*SR); c = sfx('tick', {'g': .6, 'f': 3000 + (i % 3)*300})[:, 0]; x[s:s+len(c)] += c[:len(x)-s]
        return st(x * g)
    if kind == 'glitch':
        x = np.zeros(int(d*SR)); i = 0
        while i < len(x):
            l = int(rng.uniform(.01, .04)*SR); seg = np.sign(np.sin(2*np.pi*rng.uniform(80, 900)*np.arange(l)/SR)) * rng.uniform(.2, .6)
            x[i:i+l] = seg[:len(x)-i] * (rng.random() > .3); i += l
        return st(bp(x, 150, 6000) * g * .35)
    if kind == 'strike':  # marker scratch
        t = T(d); x = bp(noise(d), 2000, 7000) * (0.6 + .4*np.sin(2*np.pi*38*t)) * np.sin(np.linspace(0, np.pi, len(t)))
        return st(x * g * .6)
    if kind == 'drop':  # water-drop / bubble for dots
        t = T(.15); f = o.get('f', 900) * (1 + 1.5*np.exp(-t/.015))
        return st(np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t/.04) * g * .4)
    if kind == 'boom':
        t = T(2.5); x = np.sin(2*np.pi*np.cumsum(38+30*np.exp(-t/.15))/SR)*np.exp(-t/.9)
        return verb(np.tanh(x*1.5)*g*.8, .3, True)
    if kind == 'clock':
        x = np.zeros(int(d*SR)); per = o.get('per', .5)
        for i in range(int(d/per)+1):
            s = int(i*per*SR); c = sfx('tick', {'g': .9 if i % 2 == 0 else .6, 'f': 1600 if i % 2 == 0 else 1300})[:, 0]
            x[s:s+len(c)] += c[:len(x)-s]
        return verb(x * g, .3)
    if kind == 'heartbeat':
        x = np.zeros(int(d*SR)); per = o.get('per', .9)
        for i in range(int(d/per)+1):
            for o_, a in [(0, 1), (.18, .7)]:
                s = int((i*per+o_)*SR); t = T(.25); b = np.sin(2*np.pi*55*t)*np.exp(-t/.07)*a
                x[s:s+len(b)] += b[:max(0, len(x)-s)]
        return st(x * g * .9)
    raise ValueError(kind)

def place(buf, x, t, g=1., pan=0.):
    x = st(x, pan) * g; s = int(round(t * SR))
    if s < 0: x = x[-s:]; s = 0
    if s >= len(buf) or len(x) == 0: return
    e = min(len(buf), s + len(x)); buf[s:e] += x[:e - s]

# ------------------------------------------------------------------ music
PROG = {  # minor progressions, (root midi for sub, chord notes)
    'Fm': [(41, [65, 68, 72, 75]), (37, [61, 65, 68, 72]), (44, [63, 68, 72, 75]), (39, [63, 67, 70, 74])],
    'Am': [(45, [69, 72, 76, 79]), (41, [65, 69, 72, 76]), (48, [67, 72, 76, 79]), (43, [67, 71, 74, 79])],
    'Dm': [(38, [62, 65, 69, 72]), (46, [62, 65, 70, 74]), (41, [60, 65, 69, 72]), (45, [61, 64, 69, 73])],
    'Cm': [(36, [60, 63, 67, 70]), (44, [60, 63, 68, 72]), (39, [58, 63, 67, 70]), (43, [59, 62, 67, 70])],
}

def music(M, dur):
    bpm = M.get('bpm', 124); beat = 60 / bpm; bar = 4 * beat; style = M.get('style', 'drive')
    drop = M.get('drop', 2.); end = M.get('end', dur - 4); prog = PROG[M.get('key', 'Fm')]
    L = int((dur + 3) * SR); mus = np.zeros((L, 2)); drums = np.zeros((L, 2)); side = np.ones(L)
    nbars = int(dur / bar) + 2
    # grid starts so that a downbeat lands exactly on the drop
    t_start = drop - np.ceil(drop / bar) * bar
    for b in range(nbars + 2):
        tb = t_start + b * bar
        if tb > dur + .5: break
        root, ch = prog[b % 4]
        live = tb >= drop - 1e-6 and tb < end - 1e-3
        outro = tb >= end - 1e-3
        pre = tb < drop - 1e-6
        # pads everywhere (quiet in pre/outro filtered)
        if tb + bar > 0:
            cut = 900 if pre else (2600 if live else 1400)
            gp = {'drive': 1., 'editorial': .8, 'cinematic': 1.3}[style]
            place(mus, pad(ch, bar + .3, gp, cut), tb, 1.)
        for i in range(16):  # 16th steps
            ts = tb + i * beat / 4
            if ts < 0 or ts > dur + .2: continue
            if style == 'drive':
                if live:
                    if i % 4 == 0: place(drums, kick(1.), ts); side_dip(side, ts, beat)
                    if i in (4, 12): place(drums, clap(.9), ts, pan=.05)
                    if i % 4 == 2: place(drums, hat(.9, open_=(i == 14)), ts, pan=.25)
                    elif i % 2 == 1: place(drums, hat(.35), ts, pan=-.2)
                    if i % 2 == 0: place(mus, sub(root + 12 if i % 8 == 6 else root, beat/2 * .9, .9), ts)
                    arp = [ch[0], ch[2], ch[1] + 12, ch[3], ch[2] + 12, ch[1], ch[3] + 12, ch[2]]
                    if i % 2 == 0: place(mus, pluck(arp[(i // 2) % 8], .3, .8), ts, pan=(-.35 if i % 4 == 0 else .35))
                elif pre:
                    if i % 4 == 2: place(drums, hat(.4), ts, pan=.2)
                    if i % 8 == 0: place(mus, pluck(ch[0] + 12, .5, .45, .6), ts)
                else:  # outro: sparse
                    if i == 0 and b % 2 == 0: place(mus, sub(root, bar * .9, .6), ts)
                    if i % 4 == 2: place(drums, hat(.25), ts, pan=.2)
            elif style == 'editorial':
                if live:
                    if i in (0, 10): place(drums, kick(.85, .8), ts); side_dip(side, ts, beat, .45)
                    if i in (4, 12): place(drums, rim(.9), ts, pan=-.1)
                    place(drums, shaker(.8 if i % 2 else .45), ts, pan=.3)
                    if i in (0, 3, 6, 8, 11, 14):
                        place(mus, keys(ch[(i // 3) % 4] + (12 if i in (8, 14) else 0), .9, .75), ts, pan=(-.25 if i < 8 else .25))
                    if i in (0, 6, 8): place(mus, sub(root + 12, beat * 1.3, .55), ts)
                elif pre:
                    if i in (0, 8): place(mus, keys(ch[i // 8] + 12, 1.2, .5), ts)
                    place(drums, shaker(.3), ts, pan=.3) if i % 2 else None
                else:
                    if i in (0, 8): place(mus, keys(ch[(i // 8) * 2], 1.6, .5), ts)
            elif style == 'cinematic':
                if live:
                    if i in (0, 7, 10): place(drums, kick(.9, .7), ts); side_dip(side, ts, beat, .35)
                    if i in (4, 12): place(drums, clap(.7), ts)
                    if i % 2 == 0: place(drums, hat(.5 if i % 4 else .25), ts, pan=.3)
                    if i in (0, 8): place(mus, sub(root, beat * 1.8, .7), ts)
                    if i in (0, 3, 6, 10, 13): place(mus, pluck(ch[(i * 3) % 4] + 12, .5, .55, .7), ts, pan=(-.3 if i % 2 else .3))
                elif pre:
                    if i in (0, 8): place(mus, pluck(ch[0] + 12, .9, .3, .5), ts)
                else:
                    if i == 0: place(mus, sub(root, bar * .9, .5), ts)
    # sidechain the tonal bus, glue, add space
    mus[:, 0] *= side; mus[:, 1] *= side
    mus = verb(mus, .22)[:L]
    out = mus * .9 + drums * .8
    return out, beat, bar

def side_dip(side, t, beat, depth=.55):
    s = int(t * SR); n = int(beat * .9 * SR)
    if s >= len(side): return
    e = 1 - depth * np.exp(-np.arange(n) / SR / .09)
    side[s:s+n] = np.minimum(side[s:s+n], e[:len(side[s:s+n])])

def build(meta_path, out_wav):
    meta = json.load(open(meta_path)); dur = meta['dur']; M = meta['music']
    mus, beat, bar = music(M, dur)
    L = mus.shape[0]; fx = np.zeros((L, 2))
    # automatic transitions: riser + impact into the drop, soft end hit
    drop = M.get('drop', 2.)
    if drop > 1.2 and not M.get('noRiser'): place(fx, sfx('riser', {'d': min(1.6, drop - .1), 'g': .55}), drop - min(1.6, drop - .1))
    if not M.get('noImpact'): place(fx, sfx('impact', {'g': .75}), drop)
    for c in meta['cues']:
        try: place(fx, sfx(c['type'], c), c['t'], pan=c.get('pan', 0.))
        except Exception as e: print('cue fail', c, e)
    mix = mus * M.get('musicGain', .55) + fx * .9
    n = int(dur * SR); mix = mix[:n]
    fo = int(.8 * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
    mix = np.tanh(mix * 1.1) / 1.1
    mix /= max(1e-6, np.abs(mix).max()) / .89
    wavfile.write(out_wav, SR, (mix * 32767).astype(np.int16))

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])
