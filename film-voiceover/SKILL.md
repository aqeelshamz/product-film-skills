---
name: film-voiceover
description: Write, review, test and record the voiceover for a product film after its picture is approved, as a script on a storyboard of the film's real frames, with directions to choose from, an eyes-closed coherence check, a pronunciation test for the product name, TTS recording per section (Fish Audio), phrase placement on the film's timeline, mixing and muxing. Stage 5 of product-film. Use when a launch/promo film needs narration, or the owner says the voiceover sounds like AI, doesn't match the frames, or mispronounces the name.
---

# Film voiceover

Voice comes AFTER the picture is approved, and is fitted to it. The picture never moves to fit the voice unless the
owner asks. Read `references/writing.md` (every rejected pattern, with before/after) before writing a word, and use
the copywriting and humanizer skills on every draft.

## Gate 1 · Directions and script (no recording yet)

1. **Understand every shot.** For each beat in `storyboard.json`, write in one line what the shot is FOR. If you
   can't, ask the owner. Lines written about what a shot seemed to show (a pet on a wall of tiny items) got rejected.
2. **Directions.** When the angle is open, write 2–4 full directions that differ in what they give the viewer, e.g.:
   *Tips the viewer can use* · *The daily annoyance* · *How it works* · *Doubts answered* (key safety, cost,
   platforms). For each: the full transcript, what it's good at, its risk. Put your pick first.
3. **Put them on the storyboard** with REAL frames: render a still per beat (`node scripts/render.mjs --at …`), set
   `vo` per direction in `storyboard.json`, build `review/storyboard.html` (film-storyboard's script). The page opens
   with each direction as one paragraph: the eyes-closed read.
4. **Self-check** with the five tests in `references/writing.md` (eyes-closed, frame, stranger, slop scan, claims).
5. **Send** the storyboard; ask which direction and what to change. Ask the voiceover questions from
   `product-film/references/question-bank.md` (voice, who it talks to, tone, how much voice). Iterate until a clear
   yes. Write the approved script to `VO-SCRIPT.md` with the time range per line and "where each claim comes from".
   Commit.

## Gate 2 · Pronunciation (before the full record)

1. **Ask** how the product name (and any other unusual word) is said, in the owner's words ("WIZ-get, hard g").
2. **Test spellings, one short clip each** (a short sentence with the name): the plain name, hyphenated, doubled
   consonant (e.g. "Nimbet", "Nim-bet", "Nimbbet"). Several spellings in one take come out shorter and confused.
   Name each file by its spelling. Send them; the owner picks.
3. **Record the winner** in `vo.json › voice.note`, in `VO-SCRIPT.md`, and in memory for future films. Never send the
   correct spelling to the engine if it mispronounces it: send the respelling everywhere.

## Gate 3 · Record, place, mix

1. **Credits first:** check the TTS balance. Fish Audio: max ~500 bytes per call, billed per byte. Record per
   section (`audio/vo/l1.wav`, `l2.wav`…), not the whole script in one call.
2. **Voice:** the one the owner chose from samples (Fish "Ethan" was approved for a calm product film). Fit pace with
   per-phrase `tempo` ≤ 1.1–1.15; never speed up a whole take.
3. **Cut into phrases:** `python3 scripts/vo.py --scan` lists speech segments per take; write `vo.json` phrases with
   `take`, `from`, `to`, `text`.
4. **Place** each phrase's `at` (beats = video seconds × 2) so its key word lands with the matching picture or on-screen
   words. Get video times with `node tools/probe.mjs cuts` and `"window.UNWARP(<story t>)"`. Run
   `python3 scripts/vo.py` until it reports `overlaps: none`; leave ≥ 0.25 s between phrases.
5. **Mix and mux:** `python3 scripts/sfx_samples.py && python3 scripts/mix.py` (-14 LUFS, ≤ -1 dBTP; voice 0, sfx
   about -10, music per the owner's choice) then `node scripts/render.mjs --mux [--fmt 9x16]`.
6. **Send** the voiced cut with the transcript and a table of where each line lands. Say you can't hear it; ask about
   pronunciation, pace, level and any line that lands on the wrong frame. Iterate. Commit `vo.json` and
   `VO-SCRIPT.md`.

## When the picture changes later

Re-probe, re-place phrases (`at`), re-mix, re-mux. For 9:16, the same `audio/mix.wav` works if the timing is shared.
