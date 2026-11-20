"""Cut a sprite sheet (default 4x3 = 12 frames, as ChatGPT draws them) into one strip of equal cells for sprite() in
film.js: feet on one ground line, the body centred from the feet so sparkles and smoke don't shift it, faint halos
removed. A sheet on plain white is keyed to transparent from its edges (white inside the character stays).

  python3 tools/pack_grid.py <sheet.png> <out.webp> [--cols 4] [--rows 3] [--height 360] [--halo 70]

It prints the cell size: pass it to sprite(parent, src, cellW, cellH, h)."""
import argparse
from PIL import Image, ImageChops, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('out')
ap.add_argument('--cols', type=int, default=4); ap.add_argument('--rows', type=int, default=3)
ap.add_argument('--height', type=int, default=360, help='cell height in px')
ap.add_argument('--halo', type=int, default=70, help='alpha below this is dropped (glow, stray fringe)')
o = ap.parse_args()
COLS, ROWS, CELL_H = o.cols, o.rows, o.height


def unwhite(im):
    # Flood the background from every edge pixel that is near white, so a white eye or highlight inside the figure,
    # which the flood can't reach, stays opaque (keying every white pixel would punch holes in it).
    rgb = im.convert('RGB'); w, h = rgb.size
    MAGIC = (255, 0, 255)
    px = rgb.load()
    edge = [(x, 0) for x in range(0, w, 8)] + [(x, h - 1) for x in range(0, w, 8)] + [(0, y) for y in range(0, h, 8)] + [(w - 1, y) for y in range(0, h, 8)]
    for xy in edge:
        if px[xy] != MAGIC and min(px[xy]) > 235:
            ImageDraw.floodfill(rgb, xy, MAGIC, thresh=40)
    bg = ImageChops.difference(rgb, Image.new('RGB', rgb.size, MAGIC)).convert('L').point(lambda v: 255 if v > 8 else 0)
    out = im.convert('RGBA'); out.putalpha(ImageChops.multiply(out.getchannel('A'), bg))
    return out


im = Image.open(src := o.src).convert('RGBA')
if im.getchannel('A').getextrema()[0] == 255:   # fully opaque: a sheet on a plain background
    im = unwhite(im)
r, g, b, a = im.split()
a = a.point(lambda v: 0 if v < o.halo else v)
im = Image.merge('RGBA', (r, g, b, a))
w, h = im.size
A = a.load()


def runs(n, filled, want):
    # Spans of filled lines, merged across small gaps, then the closest pair joined until there are `want`.
    out, start = [], None
    for i in range(n + 1):
        f = i < n and filled[i]
        if f and start is None: start = i
        if not f and start is not None:
            out.append([start, i]); start = None
    out = [s for s in out if s[1] - s[0] > 6]
    while len(out) > want:
        k = min(range(len(out) - 1), key=lambda j: out[j + 1][0] - out[j][1])
        out[k:k + 2] = [[out[k][0], out[k + 1][1]]]
    return out


rows = runs(h, [sum(1 for x in range(0, w, 3) if A[x, y] > 0) > 2 for y in range(h)], ROWS)
assert len(rows) == ROWS, f'found {len(rows)} rows, expected {ROWS}: {rows}'
frames = []
for y0, y1 in rows:
    cov = [sum(1 for y in range(y0, y1, 3) if A[x, y] > 0) for x in range(w)]
    cols = runs(w, [c > 2 for c in cov], COLS)
    while len(cols) < COLS:  # glow joined two frames: cut the widest at its thinnest column
        s = max(cols, key=lambda c: c[1] - c[0]); lo, hi = s[0] + (s[1] - s[0]) // 3, s[1] - (s[1] - s[0]) // 3
        cut = min(range(lo, hi), key=lambda x: cov[x]); i = cols.index(s)
        cols[i:i + 1] = [[s[0], cut], [cut, s[1]]]
    assert len(cols) == COLS, f'found {len(cols)} frames in a row, expected {COLS}: {cols}'
    frames += [im.crop((x0, y0, x1, y1)) for x0, x1 in cols]


def body(f):
    # Solid pixels only: the figure's bbox, and the feet's centre (bottom 12 % of it) as the horizontal anchor.
    s = f.getchannel('A').point(lambda v: 255 if v > 200 else 0)
    x0, t, x1, bot = s.getbbox()
    S = s.load(); band = range(bot - max(4, (bot - t) * 12 // 100), bot)
    xs = [x for y in band for x in range(x0, x1) if S[x, y]]
    return t, bot, sum(xs) / len(xs)


info = [body(f) for f in frames]
tall = max(bot - t for t, bot, _ in info)
scale = (CELL_H - 12) / tall
# Each frame keeps its glow: place it so its feet land on the ground line at the cell's centre.
fx = [cx * scale for _, _, cx in info]
left = max(fx); right = max(f.width * scale - c for f, c in zip(frames, fx))
CELL_W = int(left + right) + 8
strip = Image.new('RGBA', (CELL_W * len(frames), CELL_H), (0, 0, 0, 0))
for i, (f, (t, bot, cx)) in enumerate(zip(frames, info)):
    f = f.resize((round(f.width * scale), round(f.height * scale)), Image.LANCZOS)
    x = i * CELL_W + 4 + round(left - cx * scale)
    y = CELL_H - 4 - round(bot * scale)
    cell = Image.new('RGBA', strip.size, (0, 0, 0, 0)); cell.paste(f, (x, y), f)
    strip.alpha_composite(cell.crop((i * CELL_W, 0, (i + 1) * CELL_W, CELL_H)), (i * CELL_W, 0))
strip.save(o.out, 'WEBP', quality=90, method=6)
print(f'{o.out}  {len(frames)} frames  cell {CELL_W}x{CELL_H}  scale {scale:.3f}')
