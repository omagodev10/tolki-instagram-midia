#!/bin/sh
# Prepara o motor do gancho de tensão (uma vez por sessão). Rode dentro de tools/gancho-tensao.
set -e
cd "$(dirname "$0")"
[ -d node_modules/@fontsource/inter-tight ] || npm i --no-save --silent @fontsource/instrument-serif @fontsource/inter-tight @fontsource/inter @fontsource/jetbrains-mono
python3 -c "import playwright, pyloudnorm, sherpa_onnx, cv2, scipy" 2>/dev/null || pip install --break-system-packages -q playwright pyloudnorm sherpa-onnx opencv-python-headless scipy
M=~/.cache/gancho-tensao; mkdir -p $M
[ -d $M/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8 ] || (curl -sSL -o $M/p.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8.tar.bz2 && tar xjf $M/p.tar.bz2 -C $M && rm $M/p.tar.bz2)
echo "pronto"
