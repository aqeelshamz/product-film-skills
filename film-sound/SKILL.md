---
name: film-sound
description: Add sound to a finished product-film picture with real recorded sound effects (CC0 packs such as Kenney's) placed only on real on-screen events, decide with the owner whether there's a music bed, mix to -14 LUFS and mux into the renders without re-rendering. Stage 4 of product-film. Use when a film's picture is approved and needs sound effects or music, or when the owner says the sounds feel fake, synthetic or "AI slop".
---

# Film sound

"The SFX sounds like absolute AI slop" was said about synthesized beeps, whooshes and ticks on every cut. What the
owner then approved: real recordings, sparse, only where something actually happens on screen.

## Choices to put to the owner first

From `product-film/references/question-bank.md` › Sound: sound-effect density (sparse real / rich foley / none) and
music (dry / soft bed / music-led with a drop). Recommend sparse real + dry for a product demo with a voiceover.
Don't assume music.

## Rules

- **Real recordings only.** Kenney CC0 packs work well: *UI Audio*, *Interface Sounds*, *Impact Sounds*,
  *Digital Audio* (sparingly). Credit them in `assets/CREDITS.md` even though CC0.
- **About 20 cues in 60 s,** each on a real event: a cursor click, a send, a widget landing, a key moment, the logo.
- **Never:** a tick on every typed letter, a whoosh on every camera move, a riser into everything, stacked hits.
- **Quiet:** cues sit under the voice (mix `sfx` around -10 dB vs voice 0); gain per cue 0.2–0.5. Repeated events
  vary (different click files, ±small gain) so they don't sound machine-made.
- **Timing:** cues land on the visual onset (the frame where the widget lands), not the start of its move. A click
  sound lands on the cursor's dip.

## Steps

1. **Get the packs.** Kenney blocks curl (403). In the browser on kenney.nl, run in the page:
   `fetch('https://kenney.nl/download-link/' + hex('assets/<pack-slug>'))`, where `hex` hex-encodes the string
   (`[...s].map(c => c.charCodeAt(0).toString(16).padStart(2,'0')).join('')`; if it fails, read how the page's own
   download button builds the link). That returns a signed link; download, unzip into its own new folder, copy the
   chosen `.ogg` files to `assets/sfx/`. You can't hear audio: pick by file name and pack purpose, and say so.
2. **Get event times in video seconds** (after the pacing warp): `node tools/probe.mjs cuts`, plus
   `node tools/probe.mjs "window.UNWARP(<story time>)"` for events inside shots.
3. **Write cues** in `timeline.json` › `samples`: `{ "at": <video seconds × 2>, "file": "click_002.ogg", "gain": 0.35,
   "what": "cursor clicks Send" }`. The `what` is required: it's how the owner reviews the list.
4. **Render the sound:** `node scripts/sync.mjs && python3 scripts/sfx_samples.py && python3 scripts/mix.py`
   (no `audio/music.wav` → mix.py makes silence and sets music to -100). Target -14 LUFS, ≤ -1 dBTP.
5. **Mux** into the existing render: `node scripts/render.mjs --mux [--fmt 9x16]`. No re-render needed.
6. **Review gate.** Send the MP4 and the cue list (time · sound · event). Say plainly that you can't hear it and ask
   about level, density and any cue that feels fake. Wait for approval.

## When the picture's timing changes later

Re-probe, move every cue, re-run steps 4–5. Cues drift silently when the warp changes.
