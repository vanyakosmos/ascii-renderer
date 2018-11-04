#!/usr/bin/env bash

# see https://github.com/cyburgee/ffmpeg-guide
ffmpeg -y -i ${1} -filter_complex "[0:v] fps=12,scale=480:-1,split [a][b];[a] palettegen [p];[b][p] paletteuse" ${2}
