#!/usr/bin/env bash
# Zet ruwe simulator-PNG's (1206×2622) om naar 780px brede JPEG's voor de site.
#   tools/convert_shots.sh <rawdir>
set -euo pipefail
RAW="$1"; OUT="$(dirname "$0")/../img"; mkdir -p "$OUT"
for f in "$RAW"/*.png; do
  n=$(basename "$f" .png)
  sips -s format jpeg -s formatOptions 76 --resampleWidth 780 "$f" --out "$OUT/$n.jpg" >/dev/null
  printf "%-14s %6d KB\n" "$n.jpg" $(( $(stat -f%z "$OUT/$n.jpg") / 1024 ))
done
