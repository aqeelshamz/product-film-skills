"""Measure a reference video so you study its grammar from numbers and frames, not from memory.
  python3 study.py <video> <out-dir> [--fps 10] [--sheet-every 2]

Writes to <out-dir>:
  frames/f00001.jpg …       every frame at --fps (640 px wide), for reading frame by frame
  sheets/sheet_000.jpg …    contact sheets, --sheet-every seconds each at 15 fps, labelled with the time
  summary.md                duration/size/fps, hard cuts (two thresholds), motion curve (holds vs moves),
                            audio loudness by 0.5 s, the loudest onsets (where hits land), and the probable drop
  motion.csv / audio.csv    the raw curves
Needs ffmpeg, numpy, pillow, soundfile. Read EVERY sheet afterwards; the numbers only tell you where to look."""
import sys, json, subprocess, os, glob, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

args = [a for a in sys.argv[1:] if not a.startswith('--')]
opt = lambda k, d: type(d)(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
VID, OUT = Path(args[0]), Path(args[1]); FPS = opt('--fps', 10); SE = opt('--sheet-every', 2.0)
OUT.mkdir(parents=True, exist_ok=True)
run = lambda a: subprocess.run(a, capture_output=True, text=True)

pr = json.loads(run(['ffprobe', '-v', 'error', '-print_format', 'json', '-show_streams', '-show_format', str(VID)]).stdout)
vs = next(s for s in pr['streams'] if s['codec_type'] == 'video'); has_a = any(s['codec_type'] == 'audio' for s in pr['streams'])
DUR = float(pr['format']['duration']); num, den = map(int, vs['r_frame_rate'].split('/'))
info = f"{VID.name}: {DUR:.2f} s, {vs['width']}×{vs['height']}, {num / den:.2f} fps, audio: {'yes' if has_a else 'no'}"

# frames
fd = OUT / 'frames'; fd.mkdir(exist_ok=True)
for f in fd.glob('*.jpg'): f.unlink()
run(['ffmpeg', '-y', '-v', 'error', '-i', str(VID), '-vf', f'fps={FPS},scale=640:-2', '-q:v', '3', str(fd / 'f%05d.jpg')])
frames = sorted(fd.glob('*.jpg'))

# hard cuts at two thresholds (a one-take film shows none even at the low one: everything is camera moves and morphs)
def cuts(th):
    e = run(['ffmpeg', '-v', 'info', '-i', str(VID), '-vf', f"select='gt(scene,{th})',showinfo", '-f', 'null', '-']).stderr
    return [round(float(l.split('pts_time:')[1].split()[0]), 2) for l in e.splitlines() if 'pts_time:' in l]
c_hi, c_lo = cuts(0.3), cuts(0.12)

# motion: mean absolute difference between consecutive frames (64 px greyscale)
small = [np.asarray(Image.open(f).convert('L').resize((96, 54)), dtype=np.float32) for f in frames]
mot = [0.0] + [float(np.abs(a - b).mean()) for a, b in zip(small[1:], small[:-1])]
with open(OUT / 'motion.csv', 'w') as fh: fh.write('t,motion\n' + ''.join(f'{i / FPS:.2f},{m:.2f}\n' for i, m in enumerate(mot)))
holds, run_start = [], None
for i, m in enumerate(mot + [99]):
    if m < 1.0 and run_start is None: run_start = i
    if m >= 1.0 and run_start is not None:
        if (i - run_start) / FPS >= 0.5: holds.append((run_start / FPS, i / FPS))
        run_start = None

# audio
aud = ''
if has_a:
    import soundfile as sf
    wav = OUT / 'audio.wav'; run(['ffmpeg', '-y', '-v', 'error', '-i', str(VID), '-ac', '1', '-ar', '22050', str(wav)])
    x, sr = sf.read(wav); hop = int(sr * 0.05)
    rms = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2) + 1e-12) for i in range(0, len(x) - hop, hop)]); db = 20 * np.log10(rms + 1e-9)
    with open(OUT / 'audio.csv', 'w') as fh: fh.write('t,db\n' + ''.join(f'{i * 0.05:.2f},{d:.1f}\n' for i, d in enumerate(db)))
    flux = np.maximum(0, np.diff(db, prepend=db[0])); peaks = [i for i in range(1, len(flux) - 1) if flux[i] > 6 and flux[i] >= flux[i - 1] and flux[i] >= flux[i + 1]]
    onsets = sorted(round(i * 0.05, 2) for i in sorted(peaks, key=lambda i: -flux[i])[:40])
    half = [float(np.mean(db[i:i + 10])) for i in range(0, len(db), 10)]
    jump = max(range(2, len(half)), key=lambda i: np.mean(half[i:i + 4]) - np.mean(half[max(0, i - 4):i])) if len(half) > 6 else None
    gaps = np.diff(onsets) if len(onsets) > 2 else []
    beat = float(np.median([g for g in gaps if 0.25 < g < 1.2])) if len(gaps) else 0
    aud = ('\n## Audio\n\n| 0.5 s from | level dB |\n|---|---|\n' + ''.join(f'| {i * 0.5:.1f} | {v:.1f} |\n' for i, v in enumerate(half)) +
           f'\n**Onsets (where hits land):** {onsets}\n' +
           (f'\n**Typical gap between hits:** {beat:.2f} s (≈ {60 / beat:.0f} bpm if it is a beat)\n' if beat else '') +
           (f'\n**Probable drop / energy jump:** around {jump * 0.5:.1f} s\n' if jump else ''))

# contact sheets
sd = OUT / 'sheets'; sd.mkdir(exist_ok=True)
for f in sd.glob('*.jpg'): f.unlink()
n = 0
for t0 in np.arange(0, DUR, SE):
    tmp = OUT / '_s'; tmp.mkdir(exist_ok=True)
    for f in tmp.glob('*'): f.unlink()
    run(['ffmpeg', '-y', '-v', 'error', '-ss', f'{t0:.2f}', '-t', f'{SE:.2f}', '-i', str(VID), '-vf', 'fps=15,scale=320:-2', str(tmp / 'g%03d.jpg')])
    g = sorted(tmp.glob('*.jpg'))
    if not g: continue
    w, h = Image.open(g[0]).size; cols = 6; rows = math.ceil(len(g) / cols)
    sheet = Image.new('RGB', (cols * w, rows * (h + 18)), 'white'); d = ImageDraw.Draw(sheet)
    for i, f in enumerate(g):
        x, y = (i % cols) * w, (i // cols) * (h + 18); sheet.paste(Image.open(f), (x, y + 18)); d.text((x + 3, y + 3), f'{t0 + i / 15:.2f}s', fill='black')
    sheet.save(sd / f'sheet_{n:03d}.jpg', quality=80); n += 1
    for f in tmp.glob('*'): f.unlink()
    tmp.rmdir()

md = [f'# Reference study\n\n{info}\n',
      f'## Cuts\n\n- hard cuts (scene > 0.3): {c_hi or "none"}\n- soft changes (scene > 0.12): {c_lo or "none"}\n',
      '\n## Motion\n\nHolds (≥ 0.5 s nearly still): ' + (', '.join(f'{a:.1f}–{b:.1f}' for a, b in holds) or 'none: the camera never rests') + '\n',
      '\nTop motion peaks (s): ' + str(sorted(round(i / FPS, 1) for i in sorted(range(len(mot)), key=lambda i: -mot[i])[:15])) + '\n',
      aud, f'\n## Files\n\n{len(frames)} frames in frames/, {n} contact sheets in sheets/ ({SE:g} s each, 15 fps). Read them all.\n']
(OUT / 'summary.md').write_text(''.join(md)); print(''.join(md))
