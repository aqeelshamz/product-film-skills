#!/bin/sh
# Scaffold a film project:  sh ~/.claude/skills/film-build/kit/init.sh <project-dir>
set -e
KIT="$(cd "$(dirname "$0")" && pwd)"; DEST="$1"
[ -z "$DEST" ] && { echo "usage: sh $0 <project-dir>"; exit 1; }
if [ -d "$DEST" ] && [ -n "$(ls -A "$DEST" 2>/dev/null)" ]; then echo "REFUSING: $DEST is not empty. Pick a new folder."; exit 2; fi
mkdir -p "$DEST"/assets/characters "$DEST"/film/lib "$DEST"/scripts "$DEST"/tools "$DEST"/assets/fonts "$DEST"/assets/sfx "$DEST"/assets/logos "$DEST"/audio/vo "$DEST"/renders "$DEST"/review "$DEST"/reference
cp "$KIT"/film/*.js "$KIT"/film/index.html "$DEST"/film/; cp "$KIT"/film/lib/motion.js "$DEST"/film/lib/
cp "$KIT"/scripts/* "$DEST"/scripts/; cp "$KIT"/tools/* "$DEST"/tools/
cp "$KIT"/timeline.json "$KIT"/vo.json "$KIT"/package.json "$DEST"/; cp "$KIT"/gitignore "$DEST"/.gitignore
cp "$KIT"/assets/characters/*.webp "$DEST"/assets/characters/; touch "$DEST"/assets/CREDITS.md
cd "$DEST"
node scripts/sync.mjs >/dev/null 2>&1 || echo "WARN: scripts/sync.mjs failed; run it after editing timeline.json"
echo "scaffolded $DEST"
command -v ffmpeg >/dev/null || echo "WARN: ffmpeg not on PATH"
node -e "require.resolve('playwright', { paths: [process.cwd()] })" 2>/dev/null || echo "NEXT: npm i && npx playwright install chromium"
python3 -c "import numpy, scipy, soundfile, PIL" 2>/dev/null || echo "NEXT: pip install numpy scipy soundfile pillow (for vo.py, mix.py, sfx_samples.py, tools/sheet.py, tools/pack_grid.py)"
