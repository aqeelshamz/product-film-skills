"""Tile stills into one labelled contact sheet you can read in a single look.
  python3 tools/sheet.py review/stills/16x9 review/sheet.jpg 0.48,1.56,2.64 [--cols 8] [--w 320]
Stills are the files render.mjs --at writes (t<sec with 3 decimals>.png)."""
import sys
from PIL import Image, ImageDraw
args = [a for a in sys.argv[1:] if not a.startswith('--')]
opt = lambda k, d: int(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
d, out, ts = args[0], args[1], args[2].split(',')
first = Image.open(f'{d}/t{float(ts[0]):.3f}.png'); W = opt('--w', 320 if first.width >= first.height else 216)
H = round(W * first.height / first.width); cols = opt('--cols', 6 if first.width >= first.height else 10)
im = Image.new('RGB', (cols * W, ((len(ts) + cols - 1) // cols) * (H + 20)), 'white'); dr = ImageDraw.Draw(im)
for i, t in enumerate(ts):
    f = Image.open(f'{d}/t{float(t):.3f}.png').convert('RGB').resize((W, H))
    x, y = (i % cols) * W, (i // cols) * (H + 20); im.paste(f, (x, y + 20)); dr.text((x + 4, y + 4), f'{i}  {float(t):.2f}s', fill='black')
im.save(out, quality=85); print('wrote', out)
