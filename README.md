# Product film skills

Claude Code skills for making product launch films in code: a deterministic seek(t) web page rendered to 60 fps video, reviewed by the owner at each stage.

| Skill | Stage |
|---|---|
| `product-film` | The entry point. Runs the stages in order, with the question bank and every past correction (`references/lessons.md`) |
| `film-reference-study` | 1. Study a reference video frame by frame |
| `film-storyboard` | 2. Storyboard of beats and on-screen words, for review |
| `film-build` | 3. Build and render the film (`kit/` is the starter project) |
| `film-sound` | 4. Real recorded sound effects, mix and mux |
| `film-voiceover` | 5. Script, pronunciation test, TTS recording, placement |

## Install

Symlink each folder into `~/.claude/skills/`:

```bash
for d in product-film film-*; do ln -s "$PWD/$d" ~/.claude/skills/$d; done
```
