#!/usr/bin/env bash
# uso: avatar_build.sh <pasta_trabalho> <roteiro.txt> <plano.json> <saida.mp4> clipe1.mp4:audio1.wav [clipe2.mp4:audio2.wav ...]
# Normaliza cada clipe (1080x1920, 30fps), troca o áudio pelo áudio limpo da voz, emenda, cronometra e renderiza.
set -euo pipefail
W=$1; SCRIPT=$2; PLAN=$3; OUT=$4; shift 4
RK=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$W"; : > "$W/list.txt"; i=0
for pair in "$@"; do
  v=${pair%%:*}; a=${pair#*:}
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$a")
  ffmpeg -v error -y -i "$v" -i "$a" -map 0:v -map 1:a -t "$d" \
    -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,tpad=stop_mode=clone:stop_duration=2" \
    -af "apad" -c:v libx264 -preset veryfast -crf 16 -pix_fmt yuv420p -c:a pcm_s16le -ar 48000 -ac 2 "$W/p$i.mkv"
  echo "file 'p$i.mkv'" >> "$W/list.txt"; i=$((i+1))
done
ffmpeg -v error -y -f concat -safe 0 -i "$W/list.txt" -c copy "$W/joined.mkv"
python3 "$RK/align_fw.py" "$W/joined.mkv" "$SCRIPT" "$W/out" small
python3 "$RK/render.py" "$W/joined.mkv" "$W/out/edit.json" "$PLAN" "$OUT"
