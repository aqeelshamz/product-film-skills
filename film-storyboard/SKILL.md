---
name: film-storyboard
description: Write the story of a product film as beats (what the viewer sees, the words on screen, the voice, the sound, why the beat exists, and where each claim is proven) and send it to the owner as a one-page storyboard with frames for review, with 2–4 directions when the story is open. Stage 2 of product-film, and the review format reused for the voiceover. Use when planning a launch/promo film's story, shot list, or script, or when the owner says "give me a storyboard", "give me directions", "I'll review and decide".
---

# Film storyboard

The storyboard is where most of the owner's corrections should happen, because changing a sentence costs a minute and
changing a rendered shot costs an hour. Send it before you build, and send it again (with real frames) before you
record a voice.

## What makes a good product-film story

Check each beat against these. Every one came from a rejected draft (see `product-film/references/lessons.md`).

1. **The viewer's pain, in their day.** Name the habit or annoyance the way the viewer would say it. Test the line:
   after hearing it, what would a stranger think we sell? "Same numbers every day" made people think of analytics
   software, so it failed.
2. **Roles can't be misread.** Show real tools by name and logo. Check every pair of adjacent lines: "Ask the AI you
   already pay for. It's called Nimbet." makes the product sound like the AI. Attach the name to what the product does.
3. **Specific, not abstract.** "Your AI" as a label was unclear; Claude Desktop's real window was clear. A real
   Stripe dashboard beats a box labelled "Revenue".
4. **Range needs room.** If the promise is "whatever YOU need", show 8+ kinds of people (full-screen card each),
   then a wall of many items mixing work, life and fun (games, pets, stickers). Fewer than ~6 "feels stuck". This
   needs 45–65 s; 20 s is too short.
5. **Real only.** Every item, capability and claim works in the product today. Fill the `claim` field with where it's
   proven (a file, a doc, a test). If the story needs something the product can't do, raise it with the owner:
   build it or cut it.
6. **Understand each shot before you write about it.** Write the `why` for every beat. If you can't say what a shot
   is for, ask the owner. (A pet line was written over a shot that actually showed people's own custom widgets.)
7. **Every line readable.** On-screen text: ~0.3 s per word + 1 s, never under 1.5 s fully visible.
8. **End on the action,** with the name and the URL, and the nominative-use line if any brand appeared.

## Steps

1. **Read** the approved brief, `reference/NOTES.md`, the live product and site, and the lessons file.
2. **Draft beats** in `storyboard.json` (format in the script's header):
   ```json
   { "title": "…", "subtitle": "draft 1 · 16:9 · 60 s", "directions": ["A · …", "B · …"],
     "beats": [{ "t": "0.0–4.0", "still": "review/sketches/01.png", "picture": "…", "onscreen": "…",
                 "vo": {"A · …": "…", "B · …": "…"}, "sfx": "…", "why": "…", "claim": "…" }] }
   ```
   Before the film exists, `still` can be a quick sketch or a frame from the reference with a note; after, always a
   REAL rendered frame (`node scripts/render.mjs --at …`).
3. **Directions.** When the angle is open, write 2–4 directions that differ in idea, not wording (e.g. "Tips the
   viewer can use", "The daily annoyance", "What your AI already knows about you"). For each: one-line idea, the risk,
   and who it suits. Put your pick first.
4. **Build the page:**
   ```bash
   python3 ~/.claude/skills/film-storyboard/scripts/storyboard.py storyboard.json review/storyboard.html
   ```
   It opens with each direction's voiceover as one paragraph (the eyes-closed read), then every beat with its frame.
5. **Self-check** before sending: read only the transcript paragraph. Does it make sense with eyes closed? Any line
   that could be misread? Any "your X, your Y" list, triad, or repeated word? Any claim with no proof?
6. **Review gate.** Send the page (SendUserFile, display render) and ask: which direction, and which beats to change.
   Add the stage-2 questions from `product-film/references/question-bank.md` (opening, how roles are shown, persona
   format, characters, UI realism). Wait for a clear yes. Commit `storyboard.json`.

## After approval

Keep `storyboard.json` as the source of truth: shot timing in the film and phrase placement in the voiceover both come
from it. When the owner changes a beat later, change it here first and regenerate the page.
