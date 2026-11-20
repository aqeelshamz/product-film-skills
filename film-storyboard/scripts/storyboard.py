"""Build a one-file storyboard review page (images embedded) from storyboard.json.
  python3 storyboard.py storyboard.json review/storyboard.html

storyboard.json:
{ "title": "Acme launch film", "subtitle": "draft 3 · 16:9 · 62 s",
  "directions": ["A · Tips", "B · The daily annoyance"],          # optional: one VO column per direction
  "beats": [
    { "t": "0.4–7.4", "still": "review/stills/16x9/t3.000.png",   # a REAL rendered frame (or a sketch) for this beat
      "picture": "Widgets on a Mac, a Windows PC and a phone",     # what the viewer sees
      "onscreen": "Widgets for anything you keep an eye on.",       # words on screen, verbatim
      "vo": "Most of us open the same tabs all day…",               # or {"A · Tips": "...", "B · ...": "..."}; "" = silent
      "sfx": "one soft drop as each widget lands",
      "why": "names the habit before showing the fix",              # what this beat does for the viewer
      "claim": "spec/SKILL.md › Keys" } ] }                         # where a spoken/shown claim is proven

The page opens with the voiceover as a listener hears it (eyes closed), one paragraph per direction, then every beat
with its frame. Read the transcript alone first: if it doesn't make sense without the pictures, the voiceover is wrong."""
import sys, json, base64, io, html
from pathlib import Path
from PIL import Image
src, out = Path(sys.argv[1]), Path(sys.argv[2])
S = json.loads(src.read_text()); base = src.parent
dirs = S.get('directions') or ['Voiceover']
def vo(b, d): v = b.get('vo', ''); return (v.get(d, '') if isinstance(v, dict) else v) or ''
def img(p):
    if not p: return ''
    q = (base / p) if not Path(p).is_absolute() else Path(p)
    if not q.exists(): return f'<div class="miss">missing {html.escape(p)}</div>'
    im = Image.open(q).convert('RGB'); im.thumbnail((720, 720)); buf = io.BytesIO(); im.save(buf, 'JPEG', quality=82)
    return f'<img src="data:image/jpeg;base64,{base64.b64encode(buf.getvalue()).decode()}">'
e = lambda s: html.escape(s or '')
listen = ''.join(f'<h3>{e(d)}</h3><blockquote>{e(" ".join(vo(b, d) for b in S["beats"] if vo(b, d)))}</blockquote>' for d in dirs)
rows = []
for i, b in enumerate(S['beats']):
    cols = ''.join(f'<div class="vo"><span>{e(d) if len(dirs) > 1 else "Voice"}</span>{e(vo(b, d)) or "<em>(silent)</em>"}</div>' for d in dirs)
    meta = ''.join(f'<div class="m"><span>{k}</span>{e(b.get(f))}</div>' for k, f in [('On screen', 'onscreen'), ('Picture', 'picture'), ('Sound', 'sfx'), ('Why', 'why'), ('Proof', 'claim')] if b.get(f))
    rows.append(f'<figure><div class="t">{i + 1} · {e(b.get("t"))}</div>{img(b.get("still"))}<figcaption>{meta}{cols}</figcaption></figure>')
page = f'''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(S.get("title"))}</title>
<style>:root{{--bg:#FAFAF8;--ink:#1A1A18;--mute:#66645F;--line:#E2E0DB;--card:#fff}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151513;--ink:#EDEBE6;--mute:#A3A09A;--line:#33322F;--card:#1D1D1B}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,Helvetica,Arial,sans-serif;padding:24px 16px}}
h1{{margin:0 0 4px;font-size:26px}} .sub{{color:var(--mute);margin-bottom:22px}} h2{{font-size:18px;margin:28px 0 8px}} h3{{font-size:14px;margin:14px 0 4px;color:var(--mute)}}
blockquote{{margin:0;padding:12px 16px;background:var(--card);border:1px solid var(--line);border-radius:10px;font-size:17px;line-height:1.6}}
main{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:16px}}
figure{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}}
figure img{{width:100%;display:block;border-bottom:1px solid var(--line)}} .t{{padding:8px 12px;font-weight:600}}
figcaption{{padding:10px 12px;display:grid;gap:6px}} .m span,.vo span{{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--mute)}}
.vo{{font-size:16px}} .miss{{padding:40px;color:#c33}} em{{color:var(--mute)}}</style>
<h1>{e(S.get("title"))}</h1><div class="sub">{e(S.get("subtitle"))}</div>
<h2>Listen only (read this with the pictures covered)</h2>{listen}
<h2>Frame by frame</h2><main>{"".join(rows)}</main>'''
out.parent.mkdir(parents=True, exist_ok=True); out.write_text(page); print('wrote', out, f'({len(S["beats"])} beats, {len(dirs)} direction(s))')
