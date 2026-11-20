# Real recorded sound effects (e.g. Kenney's CC0 packs, in assets/sfx/) at the cues in timeline.json "samples": {at (beats), file, gain}.
# Writes audio/sfx.wav and, while there's no music or voice, audio/mix.wav at a fixed level (no loudness push, so
# sparse clicks stay quiet). Run from the project root with a python that has numpy and soundfile.
import json, numpy as np, soundfile as sf
SR = 48000
TL = json.load(open('timeline.json'))
out = np.zeros((int(SR * TL['duration']) + SR, 2))
for c in TL['samples']:
    x, sr = sf.read(f"assets/sfx/{c['file']}", always_2d=True)
    if sr != SR: x = np.stack([np.interp(np.arange(0, len(x), sr / SR), np.arange(len(x)), x[:, k]) for k in range(x.shape[1])], 1)
    if x.shape[1] == 1: x = np.repeat(x, 2, 1)
    x = x / np.abs(x).max() * c.get('gain', 0.5)
    i = int(round(c['at'] / 2 * SR)); out[i:i + len(x)] += x[: len(out) - i]
out = out[: int(SR * TL['duration'])]
peak = np.abs(out).max()
print(f"{len(TL['samples'])} cues  peak {20 * np.log10(peak):.1f} dBFS")
sf.write('audio/sfx.wav', out.astype(np.float32), SR, subtype='FLOAT')
sf.write('audio/mix.wav', out, SR, subtype='PCM_24')
