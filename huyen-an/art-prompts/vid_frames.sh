#!/bin/bash
# Tách nền xanh từng khung (lấy 1/3 số khung) của mọi video trong <thư mục video>, ghi ra <thư mục khung>/<tên video>/NNN.png.
# Dùng: vid_frames.sh <thư mục video> <thư mục khung> [tên ...]
src=$1; dst=$2; shift 2
names=${@:-$(ls "$src" | sed -n 's/\.mp4$//p')}
for v in $names; do
  [ -f "$src/$v.mp4" ] || continue
  rm -rf "$dst/$v"; mkdir -p "$dst/$v"
  ffmpeg -loglevel error -y -i "$src/$v.mp4" -vf "select='not(mod(n\,3))',chromakey=0x00b140:0.16:0.07,despill=type=green:mix=0.6:expand=0.2,format=rgba" -vsync vfr "$dst/$v/%03d.png"
  echo "$v $(ls "$dst/$v" | wc -l)"
done
