# QA before any review you send

Step through the film at ≤ 1.5 s intervals (`probe.mjs cuts` midpoints plus extra times) AND every hand-off at
10–15 fps (`render.mjs --range a,b --blur 0`, then frames → `tools/sheet.py`). Check each line. A miss here costs
the owner a review round.

## Every frame
- [ ] Nothing overlaps that shouldn't (widgets, text, cursor over important words).
- [ ] Nothing is clipped at the frame edge (logos, last letters, phone corners). 9:16: also outside the safe zones.
- [ ] No blank, white or half-built frames, especially the first frame of each shot and inside hand-offs.
- [ ] No element popping in or out: every appearance eases.
- [ ] Brand marks on screen → nominative-use line visible.

## Text
- [ ] Every line fully visible for ≥ 0.3 s × words + 1 s (≥ 1.5 s).
- [ ] Lines don't re-flow as words arrive (laid out at final width).
- [ ] Entry and exit are smooth at 60 fps (check the 10–15 fps sheet: no jumps between adjacent frames).
- [ ] Words read correctly next to each other (no line that could be misread, e.g. product = the AI).

## Typing
- [ ] Character by character, irregular, pauses at spaces/punctuation, caret visible and blinking after.
- [ ] Camera follows the caret; the line is never cut off while typing.
- [ ] Not a fade, wipe or instant paste.

## Realism
- [ ] Every app icon exists on that OS.
- [ ] Phone screens at real grid and sizes, nothing stacked.
- [ ] Product UI detailed; real logos; plausible data.
- [ ] Only real, working capabilities shown.

## Shots
- [ ] Repeated sections (one per persona) don't repeat the same five shots: the first gets the full version, later
      ones 2–3 varied shots each.
- [ ] The result is the hero: a new widget ends on a push-in at full size, not small in a corner behind a window.
- [ ] Split shots fill the frame (no half-empty side with a small caption).
- [ ] No still frame holds longer than ~2 s without a slow push or drift (end cards included).

## Pace
- [ ] A first-time viewer could follow every beat. When unsure, slower.
- [ ] Holds give the eye somewhere to land after each fast move.

## Engine
- [ ] `node scripts/render.mjs --verify` (and `--fmt 9x16`) → 12/12.
- [ ] After a 9:16 change: `sh tools/same.sh check 16x9 <times>` → every line `inf`.
