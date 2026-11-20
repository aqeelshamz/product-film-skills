---
name: film-reference-study
description: Study a reference video (a competitor's launch film, an ad the owner likes, "make it like this") frame by frame and write down its grammar as numbers (cuts, holds, camera pushes, hand-offs, typing speed, text treatment, beat and drop) so a new product film can borrow how it moves without copying what it shows. Stage 1 of product-film. Use when the user shares a video and says reverse engineer, get inspiration, similar to this, borrow the transitions, or "like this one".
---

# Film reference study

The owner likes how a video FEELS. Your job is to find out why, in numbers, so the new film can feel that way while
being its own film. A first attempt that "looked vibe-coded, not a reverse-engineering of the reference" was
rejected outright: it borrowed a vague mood and nothing measurable.

**Borrow:** cut timing, hold lengths, camera move speed and easing, how one shot becomes the next, typing and cursor
behaviour, text size/entry/exit, where the beat drops, overall pace curve.
**Never copy:** the product, its UI, words, colours, characters, story order beat for beat, music, logo. The story
must suit the owner's product.

## Steps

1. **Get the file.** Ask for the file or a screen recording if it's on a site you can't download. Put it in
   `reference/`.
2. **Measure.**
   ```bash
   python3 ~/.claude/skills/film-reference-study/scripts/study.py reference/ref.mp4 reference/study --fps 10
   ```
   Writes `summary.md` (duration, hard cuts at two thresholds, holds, motion peaks, loudness per 0.5 s, onsets, beat
   and probable drop), `frames/`, `sheets/` (2 s each at 15 fps, time-labelled), `motion.csv`, `audio.csv`. Needs
   ffmpeg, numpy, pillow, soundfile.
3. **Read every contact sheet.** The numbers only say where to look. For each sheet note what moves, how, and how the
   shot hands off. Zoom into transitions with `ffmpeg -ss <t> -t 1 -vf fps=30` frames when a hand-off is fast.
4. **Write `reference/NOTES.md`** with:
   - **Shot table:** start, end, what's on screen, camera move (from → to, speed), how it hands to the next shot.
   - **Grammar:** the 5–10 moves that make it work, each with a reference time ("0:03.2 the card morphs into the
     window: width/height/radius, 0.5 s, quint in-out").
   - **Pace curve:** shots per 5 s, longest hold, where it speeds up, where the drop is (and whether picture lands on it).
   - **Text:** size relative to frame height, words per line, entry/exit, how long a line holds vs its word count.
   - **Typing:** characters per second, pauses, caret, camera behaviour.
   - **Sound:** music structure, what gets a hit, density of effects, voice or not.
   - **Borrow / never copy** list, explicit.
   - **What won't fit our product** and what replaces it.
5. **Review gate.** Send NOTES.md's borrow list plus 2–3 key frames from the sheets, and ask the reference questions
   from `product-film/references/question-bank.md` (what to borrow, how close). Wait for the owner's yes.

## Pitfalls

- One watch is not a study. Read every sheet; the easing lives in the middle frames.
- A one-take film shows no hard cuts even at the low threshold: then the grammar is all in morphs and camera; the
  motion curve's holds and peaks are your shot list.
- Screen recordings of someone else's site carry browser chrome, a cursor and compression: crop them out before
  measuring motion.
- If the reference is well known, a close homage reads as a copy. Default to grammar only.
- The reference's length is not your length. A 20 s ad's pace stretched over 60 s with more personas needs a new
  pace curve, borrowed per section.
