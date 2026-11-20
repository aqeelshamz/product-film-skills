#!/bin/sh
# Prove a change didn't touch an approved format: render the same stills before and after and compare.
#   sh tools/same.sh save 16x9 0.5,4.2,9.8      (before the change: keeps copies in review/baseline/<fmt>/)
#   sh tools/same.sh check 16x9 0.5,4.2,9.8     (after: prints PSNR per still; every line must say inf)
set -e; MODE=$1; FMT=$2; TS=$3
node scripts/render.mjs --fmt "$FMT" --at "$TS" >/dev/null
mkdir -p review/baseline/$FMT
for t in $(echo "$TS" | tr ',' ' '); do
  n=$(printf "t%.3f.png" "$t")
  if [ "$MODE" = save ]; then cp review/stills/$FMT/$n review/baseline/$FMT/$n
  else printf "%s " "$n"; ffmpeg -i review/baseline/$FMT/$n -i review/stills/$FMT/$n -lavfi psnr -f null - 2>&1 | grep -o "average:[a-z0-9.]*"; fi
done
