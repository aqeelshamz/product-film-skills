---
name: film-build
description: Build a product film in code as a deterministic seek(t) web page (real product UI, real OS chrome, kinetic text, typed prompts, a cursor, morphs and camera moves), review it as stills and drafts, render it at 60 fps with motion blur, and adapt it to 9:16 without changing 16:9. Ships a project kit (init.sh, film engine, render/sync/probe/sheet/regression tools). Stage 3 and 6 of product-film. Use when building, fixing or rendering the picture of a launch/promo film, or making its vertical version.
---

# Film build

## Start

```bash
sh ~/.claude/skills/film-build/kit/init.sh marketing/videos/<film>   # refuses a non-empty folder
cd marketing/videos/<film> && npm i && npx playwright install chromium   # if it says NEXT
```

The kit gives you:

| File | What it is |
|---|---|
| `film/core.js` | the engine: `scene({name, from, to, build, run, after})` (times in beats = s × 2), `put(el, {o, css})`, `reg(el, base)`, `C.W/C.H/C.FMT`, `C.start()` |
| `film/film.js` | a starter with every helper below and three example shots (line, prompt, split). Each helper's comment says which rejection it came from. Replace the shots, keep the helpers. |
| `film/mock.js` | `window.MOCK`: HTML for real UI pieces (dashboards, windows, phone screens), in screen px |
| `film/index.html` | loads fonts from `assets/fonts/{display,ui}.woff2` (with local sans fallbacks) |
| `scripts/render.mjs` | `--sheet`, `--at t1,t2`, `--draft`, `--range a,b`, `--verify`, final, `--mux`, `--fmt 9x16`, `--all` |
| `scripts/sync.mjs` | copies `timeline.json` into the page |
| `scripts/review.py` | critique kit from the rendered MP4: contact sheet, fastest-action strips, phone view, 9:16 safe zones, metrics |
| `tools/probe.mjs` | `cuts` (every cut and each shot's midpoint, in video seconds) or any expression, e.g. `"window.UNWARP(12.4)"` |
| `tools/sheet.py` | tile stills into one labelled sheet |
| `tools/same.sh` | `save` / `check` PSNR regression between before and after stills |

## Helpers in the starter (use them, don't reinvent)

- `io` (quintic in-out) for camera moves and morphs; `oq` (quint-out) for entrances; `back` for a small overshoot.
- `cam(e, s, fx, fy)` puts focus point (fx, fy) of a 1920×1080 plane at the frame centre at scale s.
  `camD` does the same but never shows past the plane's edges (cover scale; essential in 9:16).
- `posIn(e, root)` reads an element's position inside the moving plane (for cursor targets, caret follow).
- `typed()` for words appearing letter by letter in a line; `keyed()` for a real keyboard: irregular per-character
  timing, longer pauses on spaces, a blinking caret after.
- `wordsHTML()` lays every word out at its final width from the first frame, transparent until its time, so the line
  never re-flows ("text transition is not at all smooth").
- `cursor()/putCursor()/bump()`: a real arrow cursor that glides, arrives early, dips 15 % on a click.
- `pop()` for small items landing.
- `shot(name, t0, t1, build, run)` wraps `scene` in seconds.
- Pacing warp at the bottom: `SLOW` (global stretch), `EV` holds (freeze a moment for reading) and inserts;
  `window.CUTS` and `window.UNWARP` give video times for sound and voice placement.
- `PT` / `pk(a16, a9)` choose per-format values in one file.

## Rules of the engine (determinism)

The film is a pure function of t. Any frame must paint the same whether rendered first or after any other frame.

- 2D transforms only: no `translate3d`, no `will-change`, no CSS transitions, no `Math.random` (use a hash of an index).
- Hidden-at-start elements: `reg(el, {o: 0})`, never inline `opacity:0`.
- Measure layout in `after()` or once in `build`, never inside `run` (it reads the previous frame).
- 3D views: re-insert each frame with `insertBefore(v, firstChild)` so no cached raster survives.
- Embedded CSS animations (e.g. a product widget's own): pause them and set `animation-delay: calc(-1s * var(--t))`.
- Wait for images and fonts (`decode()`, `document.fonts.ready`) before the first frame.
- Scope product CSS under a unique root class; use unique class names in the film (`.w` leaked once).
- `classList.add`, never `className =`.
- `node scripts/render.mjs --verify` must print 12/12 before any render you send.

## Realism: read `references/realism.md` before building any screen

Short version: real apps at real density, real logos from brands' own sites, OS chrome with apps that exist on that
OS, real wallpapers, phones on the real launcher grid at real dp sizes drawn by the product's own renderer, product
UI richer than you think it needs to be, a nominative-use line whenever a brand mark shows.

## Build loop (review-driven)

1. **Shot list from the approved storyboard** into `film.js`, one `shot()` each, overlapping for hand-offs.
2. **Stills first.** `node tools/probe.mjs cuts` → render a still at every shot midpoint and every hand-off:
   `node scripts/render.mjs --at …` then `python3 tools/sheet.py review/stills/16x9 review/sheet.jpg <times>`.
   Read the sheet yourself. Fix. Repeat. (About 1–2 min a round, vs 25+ for a full render.)
3. **QA pass before ANY review you send:** step through the film at ≤ 1.5 s and at every hand-off (10–15 fps
   contact sheet over each transition). Check `references/qa.md` line by line: overlaps, clipping, blank frames,
   reading time, text smoothness, typing, logo notice, OS realism, phone sizes.
4. **Send stills** (the sheet) to the owner for the first look. Wait.
5. **Draft:** `node scripts/render.mjs --draft` (30 fps, ~4 min), `python3 scripts/review.py 1 --draft`, read the
   strips. Send the draft MP4. Say clearly it's a 30 fps draft without blur (looks choppier than the final).
6. **On "render final":** `node scripts/render.mjs` in the background (60 fps, motion blur; ~25–35 min for 60 s).
   Never edit `film.js` while it renders: copy the project first if you need to keep working.
7. **Commit** film code and timeline after each approved round.

## Pace

First cuts are almost always too fast. On-screen text needs about 0.3 s per word + 1 s at full opacity (never under
1.5 s). Prefer the warp (`SLOW` 1.1–1.25, `EV` holds on lines) to retiming every shot. After any pace change, re-run
`probe.mjs cuts` because sound and voice positions move.

## 9:16: read `references/formats.md`

Reframe the same film in one file with `pk()`; prove 16:9 unchanged with `tools/same.sh` (every still PSNR = inf);
`--verify --fmt 9x16`; stills sheet for the owner; then `--fmt 9x16` final in the background, then `--mux --fmt 9x16`.
