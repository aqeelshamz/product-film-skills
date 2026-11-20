# 9:16 (and other formats) from one film.js

The approved 16:9 must not change by a single pixel. Reframe the same scenes with per-format values.

## Method

1. Before touching anything: `sh tools/same.sh save 16x9 <15–25 times across the film>` and back up `film.js`.
2. At the top of `film.js`: `const PT = C.FMT === '9x16', pk = (a, c) => (PT ? c : a);`
   Name the flag something unmistakable. (`P` once collided with a per-person loop variable `P`.)
3. Change values only through `pk(a16, a9)` or `PT ? … : …` so the 16:9 branch keeps the exact same numbers and
   expressions. Never "tidy" the 16:9 values while you're there.
4. After each round: `sh tools/same.sh check 16x9 <same times>` → all `inf`; then 9:16 stills sheet; read it.
5. `node scripts/render.mjs --verify --fmt 9x16` → 12/12.
6. Owner reviews the 9:16 stills, then final: `node scripts/render.mjs --fmt 9x16` (background), then
   `node scripts/render.mjs --mux --fmt 9x16`.

## Reframing patterns that worked

| 16:9 shot | 9:16 version |
|---|---|
| Wide desktop (1920×1080 plane) | `camD` with cover scale `s = max(s, VW/1920, VH/1080)`, focus moved to the part that matters (the widget, not the empty wallpaper) |
| Phone on a desktop | Phone larger (≈ 1.8×) and centred |
| Side-by-side split (UI left, words right) | Stacked: UI panel on top (≈ 1000×940 at top 200), words below (≈ 76 px) |
| Persona card (character left, label right) | Character over label, both centred |
| Wall of items in 3 rows | 4 rows; greedy placement into the shortest row so rows stay even |
| Row of 4 widgets | 2×2 grid, scaled up ≈ 1.28 |
| Big centred headline | Smaller (≈ 0.9×), wraps to 2–3 lines, measured at final width |
| Typed prompt in a wide input | Scale ≈ 0.82, camera follows the caret using the full text width measured once |
| Nominative-use line at the bottom | Higher (`VH − 150`), clear of Reels/TikTok UI |

## Safe zones (Reels/TikTok/Shorts)

Keep text and key UI out of the top 14 %, bottom 20 % and right 12 %. `python3 scripts/review.py <n>` writes
`safe_9x16.jpg` with those zones shaded.
