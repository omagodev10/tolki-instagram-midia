"""Render do modelo gancho de tensão: página de motion (WORK/page.html) quadro a quadro + filmagem do gancho (opcional) + mix.
python3 render.py WORK --out nome.mp4 [--plate gancho.mp4] [--music trilha.mp3 --moff 13 --music-swell 30.95 --swell-line 7] [--prev 1 5.5 12 | --audio-only]
WORK tem tl.json, tl.js, a/l1.wav... (de voz.py). Sem --plate o gancho é 100% desenhado. Sem --music fica só voz + efeitos."""
import asyncio, json, subprocess, os, sys
import numpy as np, cv2, pyloudnorm as pyln
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, resample_poly
from playwright.async_api import async_playwright
import argparse
ap_ = argparse.ArgumentParser(); ap_.add_argument('work'); ap_.add_argument('--out', required=True); ap_.add_argument('--plate'); ap_.add_argument('--music'); ap_.add_argument('--moff', type=float, default=0)
ap_.add_argument('--music-swell', type=float, help='segundo da música onde ela cresce'); ap_.add_argument('--swell-line', type=int, help='fala onde a música deve crescer'); ap_.add_argument('--music-gain-max', type=float, default=7.5)
ap_.add_argument('--prev', type=float, nargs='*'); ap_.add_argument('--audio-only', action='store_true'); ARGS = ap_.parse_args()
ENGINE = os.path.dirname(os.path.abspath(__file__)); HERE = os.path.abspath(ARGS.work); PLATE = ARGS.plate; OUTNAME = ARGS.out; OUT = os.path.join(HERE, 'out'); os.makedirs(OUT, exist_ok=True)
TL = json.load(open(os.path.join(HERE, 'tl.json'))); MOFF = ARGS.moff; DUR = TL['dur']; W, H, FPS, SR = 1080, 1920, 30, 48000
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sfx_synth as A
meter = pyln.Meter(SR)
def load(p, ch=1):
    a = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', p, '-ac', str(ch), '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    a = np.frombuffer(a, np.float32).astype(np.float64); return a.reshape(-1, ch) if ch > 1 else a
def smooth(x, ta, tr, cr=1000):
    h = SR // cr; xc = x[::h]; y = np.empty_like(xc); y[0] = xc[0]; ka, kr = np.exp(-1 / (ta * cr)), np.exp(-1 / (tr * cr))
    for i in range(1, len(xc)):
        k = ka if xc[i] < y[i - 1] else kr; y[i] = k * y[i - 1] + (1 - k) * xc[i]
    return np.interp(np.arange(len(x)), np.arange(len(xc)) * h, y)
def build_audio(cues):
    N = int(DUR * SR) + SR; voice = np.zeros(N)
    for l in TL['lines']:
        v = load(os.path.join(HERE, 'a', f"l{l['n']}.wav")); v *= 10 ** ((-17 - meter.integrated_loudness(v)) / 20) if len(v) > SR * .5 else 10 ** (2 / 20)
        a = int(l['t'] * SR); voice[a:a + len(v)] += v[:N - a]
    env = smooth(np.abs(voice), .005, .12); thr = 10 ** (-14 / 20)
    voice *= np.where(env > thr, (thr + (env - thr) * .4) / np.maximum(env, 1e-9), 1)
    mus = np.zeros((N, 2)); MST = TL['hook'] + .25
    if ARGS.music:
        if ARGS.music_swell is not None and ARGS.swell_line: MST = max(TL['hook'] + .25, TL['lines'][ARGS.swell_line - 1]['t'] - .05 - (ARGS.music_swell - MOFF))
        m = load(ARGS.music, 2)[int(MOFF * SR):][:N - int(MST * SR)]; mus[int(MST * SR):int(MST * SR) + len(m)] = m
        print('música entra em', round(MST, 2), 's (offset', MOFF, ')')
    pb = butter(4, [300, 8000], 'bandpass', fs=SR, output='sos')
    act = np.convolve((np.abs(voice) > 10 ** (-40 / 20)).astype(float), np.ones(int(.25 * SR)), 'same') > 0
    vb = sosfilt(pb, voice); mb = sosfilt(pb, mus.mean(1)); me = np.convolve(np.abs(mb), np.ones(4800) / 4800, 'same'); loud = me > max(me.max() * .1, 1e-5)
    g = 10 * np.log10((vb[act] ** 2).mean()) - 9 - 10 * np.log10((mb[loud] ** 2).mean() + 1e-12)
    g = min(g, ARGS.music_gain_max) if np.isfinite(g) else 0   # 7,5 dB = nível aprovado na ampulheta v4
    tt = np.arange(N) / SR; end_v = TL['lines'][-1]['t'] + TL['lines'][-1]['d']
    gdb = np.where(act, g, g + 3.5); gdb = np.where(tt > end_v + .05, g + 6, gdb); gdb = smooth(gdb, .04, .3)
    mus *= (10 ** (gdb / 20) * np.clip((tt - MST) / 1.5, 0, 1) * np.clip((DUR - tt) / 1.2, 0, 1) ** 1.5)[:, None]
    fx = np.zeros((int((DUR + 3) * A.SR), 2), np.float32)
    for c in cues:
        try:
            if c['type'].startswith('file:'):
                a_ = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', os.path.join(ENGINE, 'sfx', c['type'][5:]), '-ac', '2', '-ar', str(A.SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout, np.float32).reshape(-1, 2)
                a_ = a_ / (np.abs(a_).max() + 1e-9) * c.get('g', .5); i0 = int(c['t'] * A.SR); n_ = min(len(a_), len(fx) - i0); fx[i0:i0 + n_] += a_[:n_]
            else: A.place(fx, A.sfx(c['type'], c), c['t'], g=.55)
        except Exception as e: print('cue fail', c['type'], e)
    fx = resample_poly(fx, 160, 147, axis=0)[:N]; fx = np.pad(fx, ((0, N - len(fx)), (0, 0)))
    va = np.convolve(np.abs(voice), np.ones(2400) / 2400, 'same'); va = np.clip(va / (np.percentile(va[va > 1e-4], 90) + 1e-9), 0, 1)
    fx *= (1 - .5 * va)[:, None]
    fx *= 10 ** ((10 * np.log10((voice[act] ** 2).mean() + 1e-12) - 16 - 10 * np.log10((fx ** 2).mean() + 1e-12)) / 20)
    mix = (np.stack([voice, voice], 1) + mus + fx)[:int(DUR * SR)]
    mix *= 10 ** ((-14 - meter.integrated_loudness(mix)) / 20)
    pre = os.path.join(OUT, '_pre.wav'); wavfile.write(pre, SR, mix.astype(np.float32)); p = os.path.join(OUT, 'audio.wav')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', pre, '-af', 'alimiter=limit=0.89:attack=3:release=60:level=false', '-c:a', 'pcm_s16le', p], check=True)
    fin = wavfile.read(p)[1].astype(np.float64) / 32768
    print('audio LUFS', round(meter.integrated_loudness(fin), 1), 'peak', round(20 * np.log10(np.abs(fin).max()), 1), 'music gain', round(g, 1))
    return p


PF = 24
def plate_frames():
    p = PLATE; o = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'json', p], capture_output=True, text=True).stdout)['streams'][0]
    w, h = o['width'], o['height']; raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', p, '-vf', f'scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},unsharp=5:5:0.8', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
yy, xx = np.mgrid[0:H, 0:W]; VIG = (1 - .28 * (((xx - W / 2) / (W * .7)) ** 2 + ((yy - H / 2) / (H * .7)) ** 2)).clip(.55, 1).astype(np.float32)[..., None]
BGC = np.zeros((H, W, 3), np.float32); BGC[:] = (18, 11, 5)
def bg(PL, b):
    if not b['show'] or PL is None: return BGC
    f = min(max(b['src'], 0) * PF, len(PL) - 1.001); i = int(f); a = f - i
    img = PL[i].astype(np.float32) * (1 - a) + PL[i + 1].astype(np.float32) * a
    if abs(b['scale'] - 1) > 1e-3:
        M = cv2.getRotationMatrix2D((W / 2, H * .46), 0, b['scale']); img = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    if b['blur'] > .3: img = cv2.GaussianBlur(img, (0, 0), b['blur'] / 2)
    return img * (1 - b['dim']) * VIG
def comp(img, png):
    fg = cv2.imdecode(np.frombuffer(png, np.uint8), cv2.IMREAD_UNCHANGED).astype(np.float32); a = fg[..., 3:4] / 255
    return np.clip(img * (1 - a) + fg[..., :3] * a, 0, 255).astype(np.uint8)
async def run(prev):
    PL = plate_frames() if PLATE else None
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path=('/opt/pw-browsers/chromium' if os.path.exists('/opt/pw-browsers/chromium') else None), args=['--allow-file-access-from-files'])
        pg = await (await b.new_context(viewport={'width': W, 'height': H})).new_page()
        pg.on('pageerror', lambda e: print('ERR', e))
        await pg.goto('file://' + os.path.join(HERE, 'page.html')); await pg.wait_for_function('window.READY===true', timeout=30000); await pg.wait_for_timeout(400)
        async def frame(t):
            await pg.evaluate(f'renderAll({t})'); bb = await pg.evaluate(f'bgAt({t})')
            return comp(bg(PL, bb), await pg.screenshot(type='png', omit_background=True))
        if prev:
            ims = [cv2.resize(await frame(t), (360, 640)) for t in prev]
            while len(ims) % 6: ims.append(ims[0] * 0)
            cv2.imwrite(os.path.join(OUT, 'prev.jpg'), np.vstack([np.hstack(ims[i:i + 6]) for i in range(0, len(ims), 6)])); await b.close(); return
        cues = await pg.evaluate('CUES'); ap = build_audio(cues); mid = os.path.join(OUT, '_v.mp4')
        if AUDIO_ONLY: await b.close()
        else:
            ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                                   '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', mid], stdin=subprocess.PIPE)
            n = int(round(DUR * FPS))
            for i in range(n):
                ff.stdin.write((await frame(i / FPS)).tobytes())
                if i % 150 == 0: print('frame', i, '/', n, flush=True)
            ff.stdin.close(); ff.wait(); await b.close()
    fin = os.path.join(OUT, OUTNAME)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mid, '-i', ap, '-c:v', 'libx264', '-crf', '19', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', fin], check=True)
    print('done', fin, round(os.path.getsize(fin) / 1e6, 1), 'MB')
AUDIO_ONLY = ARGS.audio_only
asyncio.run(run(ARGS.prev or None))
