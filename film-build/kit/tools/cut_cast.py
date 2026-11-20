"""Cut a one-row lineup of characters (transparent, or on plain white) into single toys, each trimmed, scaled to one
height and saved as WebP: for a wall or a crowd of personas, where each one stands still.

  python3 tools/cut_cast.py <sheet.png> <out_dir> name1,name2,… [height=360] [halo=70]"""
import sys, os
from PIL import Image, ImageChops, ImageDraw


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


src, out, names = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
H = int(sys.argv[4]) if len(sys.argv) > 4 else 360
halo = int(sys.argv[5]) if len(sys.argv) > 5 else 70
im = Image.open(src).convert('RGBA')
if im.getchannel('A').getextrema()[0] == 255:   # fully opaque: a lineup on a plain background
    im = unwhite(im)
r, g, b, a = im.split()
a = a.point(lambda v: 0 if v < halo else v)
im = Image.merge('RGBA', (r, g, b, a))
w, h = im.size
A = a.load()
cov = [sum(1 for y in range(0, h, 2) if A[x, y] > 0) for x in range(w)]
# spans of filled columns; join the closest pair until there's one per name (props can leave small gaps)
spans, start = [], None
for x in range(w + 1):
    f = x < w and cov[x] > 1
    if f and start is None: start = x
    if not f and start is not None: spans.append([start, x]); start = None
spans = [s for s in spans if s[1] - s[0] > 4]
while len(spans) > len(names):
    k = min(range(len(spans) - 1), key=lambda j: spans[j + 1][0] - spans[j][1])
    spans[k:k + 2] = [[spans[k][0], spans[k + 1][1]]]
while len(spans) < len(names):  # a prop touching a neighbour joined two toys: cut the widest at its thinnest column
    s = max(spans, key=lambda c: c[1] - c[0]); lo, hi = s[0] + (s[1] - s[0]) // 3, s[1] - (s[1] - s[0]) // 3
    cut = min(range(lo, hi), key=lambda x: cov[x]); i = spans.index(s)
    spans[i:i + 1] = [[s[0], cut], [cut, s[1]]]
assert len(spans) == len(names), (len(spans), spans)
os.makedirs(out, exist_ok=True)
for name, (x0, x1) in zip(names, spans):
    # keep the widest run of filled columns and whatever touches it, dropping slivers of the neighbours
    runs, st = [], None
    for x in range(x0, x1 + 1):
        f = x < x1 and cov[x] > 1
        if f and st is None: st = x
        if not f and st is not None: runs.append([st, x]); st = None
    k = max(range(len(runs)), key=lambda j: runs[j][1] - runs[j][0]); lo, hi = runs[k]
    for r0, r1 in runs[k + 1:]:
        if r0 - hi <= 4: hi = r1
    for r0, r1 in reversed(runs[:k]):
        if lo - r1 <= 4: lo = r0
    t = im.crop((lo, 0, hi, h)); t = t.crop(t.getbbox())
    t = t.resize((round(t.width * H / t.height), H), Image.LANCZOS)
    t.save(os.path.join(out, name + '.webp'), 'WEBP', quality=90, method=6)
    print(name, t.size)
