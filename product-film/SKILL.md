---
name: product-film
description: Make a product launch / promo / explainer film that sells and does not look or sound AI-made, through review gates the owner signs off one at a time. Study a reference video for its grammar (never copy it), then storyboard, build the film in code, add sound, write and record the voiceover, and deliver 16:9 and 9:16. Use when someone wants a launch video, promo, product film, explainer, ad, "a video like this one" for their product, or says the last video looked like "AI slop" or "vibe coded". Entry point for the film-* skills (film-reference-study, film-storyboard, film-build, film-sound, film-voiceover).
---

# Product film

A product film is judged by one person first: the owner. They correct what's wrong, you fix it, and the film gets
better a round at a time. This skill exists so that you make the owner's corrections unnecessary: every rule here
came from a correction someone had to make by hand. Read `references/lessons.md` before you start, and again before
each review you send. It is the record of what owners rejected and why.

## The pipeline and its gates

Nothing moves to the next stage until the owner has approved the current one. Approval is a clear yes in chat, not
silence and not "looks good but…". After any change the owner asks for, send it back for review again.

| Stage | Skill | You send for review | Gate |
|---|---|---|---|
| 0 · Brief | this one | the brief: product, buyer, the one thing to convince them of, length, formats, where it will play | owner approves the brief |
| 1 · Reference | `film-reference-study` | what the reference does and what to borrow, as numbers and frames | owner agrees what's borrowed and what isn't |
| 2 · Storyboard | `film-storyboard` | a storyboard page: one frame per beat, on-screen words, why each beat is there; 2–4 directions if the story is open | owner picks a direction and approves the beats |
| 3 · Picture | `film-build` | stills first, then a 30 fps draft, never a final render first | owner approves the picture ("render final") |
| 4 · Sound | `film-sound` | the final with sound effects, and the music decision | owner approves the sound |
| 5 · Voiceover | `film-voiceover` | the script on a storyboard of REAL frames, then name tests, then the voiced cut | owner approves script, pronunciation, then the cut |
| 6 · Formats | `film-build` (formats) | 9:16 stills, then the 9:16 render | owner approves; 16:9 provably unchanged |
| 7 · Deliver | this one | the files, captions, credits, what isn't verified | done |

"Before rendering let me review": the owner wants to see the plan and stills before you spend 30 minutes on a
render. A final render without an approved draft is wasted time and wastes their trust.

## How to ask (every gate)

At each gate, ask concrete choices rather than open questions, and make every option something a real editor would
pick. Generic options ("modern", "clean", "dynamic") are how a film turns into AI slop. `references/question-bank.md`
has the questions and options for each stage: look, motion, pace, transitions, typing, characters, sound, music,
voice, delivery. Rules:

- Two to four options per question, each with what it looks or sounds like and its cost or risk. Put your pick
  first and say why in one line.
- Ask only what changes the work. Decide the rest from the brand and the reference, and say what you decided.
- When the owner talks through ideas out loud, don't implement each sentence. Research, then come back with 2–4
  directions and their trade-offs, and let them pick ("give me some directions with the trade-offs so that I can
  decide").
- When the owner says "wait, I'll tell you more", stop and wait. Don't keep editing.
- When a correction comes in, find the rule behind it and check the whole film for the same mistake, not just the
  one spot they pointed at.

## Rules that hold at every stage

1. **Real only.** Every feature, widget, screen, number source and claim in the film works in the product today.
   If the film needs something the product can't do, either build it in the product (and log the decision) or drop
   it. Every spoken or shown claim has a source you can point to (a file, a doc, a test).
2. **Specific, not generic.** Real logos from the brands' own sites. Real OS chrome with apps that actually exist on
   that OS. Real device sizes. Real wallpapers (licensed). Rich, detailed product UI: "too simple" reads as
   "why would I pay for this". See `film-build/references/realism.md`.
3. **The viewer's point of view.** The film is for a stranger who has never heard of the product. Test every beat:
   would they understand it? Could they misread it (for example, think the product IS the AI)? Is it about their
   life or about our features?
4. **Not AI-made.** No synthesized beeps, no minimal mockups, no icon-font look-alikes of real brands, no triads and
   "your X, your Y" copy, no scene-describing voiceover. Owners know these tells, and so do their buyers. One
   competitor got publicly dragged for a launch video that looked "made with Claude".
5. **Readable and smooth.** Every line holds long enough to read to the end. Typing looks like a keyboard. Nothing
   clips, overlaps or flashes empty. Pace for humans: first cuts are almost always too fast.
6. **Determinism.** The film is a pure function of time; `render.mjs --verify` must pass before any render you send.
7. **Small, honest reports.** When you send a review, say what changed, what's still open, and what you could not
   check (you can't hear audio: say so and ask). Never call something verified that you didn't check.
8. **Commit often** (code, scripts, storyboard, VO script). Renders, audio and stills stay out of git.

## Project layout

```
<film>/
  brief.md                 stage 0
  reference/               study output (frames, sheets, summary.md, NOTES.md)
  storyboard.json          stage 2 source → review/storyboard.html
  film/                    the film page (core.js, film.js, mock.js, index.html)
  scripts/ tools/          render, sync, sound, voice, mix, probes (from film-build's kit)
  timeline.json vo.json    picture timing and sound cues; voiceover phrases
  VO-SCRIPT.md             the approved voiceover with where each claim comes from
  assets/                  fonts, logos, wallpapers, sfx, characters, CREDITS.md
  renders/ audio/ review/  (git-ignored)
```

Start with `sh ~/.claude/skills/film-build/kit/init.sh <film>`.

## Stage 0 · Brief

Before anything else, write `brief.md` and get it approved:

- **Product, in one sentence a stranger understands.** Not the tagline.
- **Who buys, in their words.** Several kinds of people if the product serves several (personas): what each one
  checks or needs every day.
- **The one thing the film must convince them of**, and the one misunderstanding it must prevent.
- **Proof available:** what's real today, what has been built and recorded, what may be shown.
- **Length and formats:** a launch film that shows range needs about 45–65 s. 20 s is too short to show several
  people and their use cases. Formats: 16:9 first, then 9:16, unless the owner says otherwise.
- **Where it plays** (site hero, X, Reels, YouTube) and the brand rules (colours, type, words never to use, logos).
- **What the product must never be shown as** (e.g. "never a dock"), and any competitor to stay clear of.

## Stage 7 · Deliver

- `renders/16x9.mp4` and `renders/9x16.mp4` (60 fps, motion blur, voice and sound muxed).
- `assets/CREDITS.md`: every wallpaper, logo, font, sound and character, with its licence.
- If brands appear: a nominative-use line on screen while they show ("Product names and logos belong to their
  owners…").
- A plain list of what is not verified (e.g. "the four requests haven't been built in the real app yet").
- Captions and a thumbnail if asked (use the owner's social and copywriting skills; no AI tells).

## After the film

Add every new correction the owner made to `references/lessons.md`, under the stage it belongs to, with what was
wrong and the rule that prevents it. That file is how the next film starts ahead of this one.
