#!/usr/bin/env python3
"""build_audio.py: monta o áudio do Reel motion da Tolki.
Uso: python3 build_audio.py job.json   (rodar dentro da pasta do Reel)

job.json:
{
 "lines": [{"text": "frase 1", "audio": "a/l1.mp3"}, ...],   # uma fala por cena, na ordem
 "gap_first": 0.2, "gap": 0.3, "tail": 1.2,                  # respiros (s)
 "music": "musica.mp3", "music_gain": 0.22,                  # trilha (opcional), abaixa sozinha quando a voz fala
 "sfx_dir": "lib",                                           # pasta com SFX_*.mp3 (ver sons.json)
 "sfx": [{"name": "SFX_WHOOSH", "scene": 2, "at": 0.0, "gain": 0.5}, ...]
}
"scene": i usa o início da cena i (o mesmo instante B[i] que o reel.html usa: start - 0.15; cena 0 = 0).
Saídas: timing.json (para o gen_reel.py) e mix.wav (-14 LUFS)."""
import json, subprocess, sys, os


def dur(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]).decode())


def main():
    J = json.load(open(sys.argv[1], encoding='utf-8'))
    L = J['lines']
    t, sc = 0.0, []
    for i, l in enumerate(L):
        t += J.get('gap_first', 0.2) if i == 0 else J.get('gap', 0.3)
        d = dur(l['audio'])
        sc.append({'text': l['text'], 'start': round(t, 3), 'dur': round(d, 3)})
        t += d
    total = round(t + J.get('tail', 1.2), 3)
    json.dump({'scenes': sc, 'total': total}, open('timing.json', 'w'), ensure_ascii=False, indent=1)
    B = [0.0] + [s['start'] - 0.15 for s in sc[1:]]
    ins, fl, n = [], [], 0
    for i, (l, s) in enumerate(zip(L, sc)):
        ins += ['-i', l['audio']]
        ms = int(s['start'] * 1000)
        fl.append(f'[{n}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[v{i}]'); n += 1
    fl.append(''.join(f'[v{i}]' for i in range(len(L))) + f'amix=inputs={len(L)}:normalize=0,apad=whole_dur={total},asplit=2[voz][sc]')
    mixin = ['[voz]']
    if J.get('music') and os.path.exists(J['music']):
        ins += ['-stream_loop', '-1', '-i', J['music']]
        g = J.get('music_gain', 0.22)
        fl.append(f'[{n}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{total},volume={g},afade=t=out:st={total-1.0}:d=1.0[m0]')
        fl.append('[m0][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[m]'); n += 1
        mixin.append('[m]')
    else:
        fl.append('[sc]anullsink')
    for k, e in enumerate(J.get('sfx', [])):
        p = os.path.join(J.get('sfx_dir', 'lib'), e['name'] + '.mp3')
        at = B[e.get('scene', 0)] + e.get('at', 0.0)
        ms = int(max(0, at) * 1000)
        ins += ['-i', p]
        fl.append(f'[{n}:a]aresample=48000,aformat=channel_layouts=stereo,volume={e.get("gain", 0.5)},adelay={ms}|{ms}[e{k}]'); n += 1
        mixin.append(f'[e{k}]')
    fl.append(''.join(mixin) + f'amix=inputs={len(mixin)}:normalize=0,atrim=0:{total},loudnorm=I=-14:TP=-1.5:LRA=11[o]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', ';'.join(fl), '-map', '[o]', '-ar', '48000', 'mix.wav'], check=True)
    print('total', total, 'cenas', [(s['start'], s['dur']) for s in sc])


if __name__ == '__main__':
    main()
