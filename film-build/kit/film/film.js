// FILM STARTER. Replace the example shots with your storyboard; keep the helpers.
// The film is a pure function of time: window.seek(t) paints frame t. 2D transforms only (no translate3d, no
// will-change, no CSS transitions, no Math.random): any frame must paint the same whether it's rendered first or
// after any other frame (scripts/render.mjs --verify checks this).
//
// Every helper below exists because a reviewer rejected the version without it. The comments say what went wrong.
(() => {
  const { put, reg, el, scene } = C;
  C.fonts = ['800 100px Display', '700 100px Display', '600 40px UI'];
  const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const W = (t, a, z) => cl((t - a) / (z - a));          // 0→1 as t goes a→z
  const L = (a, b, x) => a + (b - a) * x;
  const io = (x) => x * x * x * (x * (x * 6 - 15) + 10);  // quintic in-out: camera moves and morphs
  const oc = (x) => 1 - Math.pow(1 - x, 3);
  const oq = (x) => 1 - Math.pow(1 - x, 5);               // quint-out: entrances
  const back = (x) => { const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
  const b = (s) => s * 2;                                 // seconds → beats (scene() takes beats at 120 bpm)
  const VW = C.W, VH = C.H, MX = VW / 2, MY = VH / 2;
  // formats: write the film for 16:9, then give 9:16 its own framing with pk(a16, a9). Never let a 9:16 change touch
  // 16:9: compare 16:9 stills before and after (PSNR must be inf). Shots that are words + picture side by side stack
  // vertically in 9:16; desktops are cropped (camD), never letterboxed.
  const PT = C.FMT === '9x16', pk = (a, c) => (PT ? c : a);
  const div = (parent, style, html = '') => el('div', { class: 'abs', style }, parent, html);
  const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
  const blurOf = (px) => (px > 0.05 ? `blur(${px.toFixed(2)}px)` : undefined);

  // ------------------------------------------------------------------ camera
  // cam: show content point (fx, fy) at frame point (cx, cy), scaled s
  const cam = (e, s, fx, fy, cx = MX, cy = MY) => put(e, { css: { transform: `translate(${(cx - fx * s).toFixed(2)}px,${(cy - fy * s).toFixed(2)}px) scale(${s.toFixed(5)})` } });
  // camD: the same for a full-screen 1920×1080 surface (a desktop, a dashboard), clamped so it always covers the frame:
  // no paper showing at the edges in any format
  const camD = (e, s, fx, fy, w = 1920, h = 1080) => {
    s = Math.max(s, VW / w, VH / h);
    const tx = cl(MX - fx * s, VW - w * s, 0), ty = cl(MY - fy * s, VH - h * s, 0);
    put(e, { css: { transform: `translate(${tx.toFixed(2)}px,${ty.toFixed(2)}px) scale(${s.toFixed(5)})` } });
  };
  const camRoot = (root, w = 1920, h = 1080) => div(root, `width:${w}px;height:${h}px;transform-origin:0 0`);
  // where an element sits inside a content root, from the offset chain (camera transforms don't affect it). Measure
  // only static layout this way: text you set with put() this frame isn't laid out until commit.
  const posIn = (e, root) => { let x = 0, y = 0, n = e; while (n && n !== root) { x += n.offsetLeft; y += n.offsetTop; n = n.offsetParent; } return { x, y, w: e.offsetWidth, h: e.offsetHeight, cx: x + e.offsetWidth / 2, cy: y + e.offsetHeight / 2 }; };

  // ------------------------------------------------------------------ text
  const hex = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const mix = (a, c, k) => { const A = hex(a), B = hex(c); return `rgb(${A.map((v, i) => Math.round(L(v, B[i], k))).join(',')})`; };
  // titles typed on screen: each character arrives pale and settles to ink in 0.13 s
  const typed = (txt, t, a, z, ink, pale) => {
    const n = txt.length, shown = Math.floor(W(t, a, z) * n + 1e-6);
    let out = '';
    for (let i = 0; i < shown; i++) {
      const ta = a + ((z - a) * i) / n, k = W(t, ta, ta + 0.13);
      out += k >= 1 ? esc(txt[i]) : `<span style="color:${mix(pale, ink, k)}">${esc(txt[i])}</span>`;
    }
    return out;
  };
  // a prompt typed into an app's input. Rejected version: characters fading in ("looks fading instead of typing").
  // Real typing: each key lands solid, at an uneven rhythm (longer after spaces), with a caret that blinks only when idle.
  const keyed = (txt, t, a, z, ink) => {
    const g = [...txt].map((c, i) => 0.7 + 0.6 * ((Math.sin(i * 12.9898) * 43758.5453) % 1 + 1) % 1 + (c === ' ' ? 0.7 : 0));
    const sum = g.reduce((x, y) => x + y, 0);
    let acc = 0, shown = 0;
    for (let i = 0; i < g.length; i++) { if (t >= a + ((z - a) * acc) / sum) shown = i + 1; acc += g[i]; }
    const on = (t >= a && t < z + 0.15) || Math.floor((t - z) / 0.53) % 2 === 0;
    return `<span style="color:${ink}">${esc(txt.slice(0, shown))}</span><span style="display:inline-block;width:2px;height:1.15em;margin-left:1px;vertical-align:-0.2em;background:${ink};opacity:${on ? 1 : 0}"></span>`;
  };
  // word by word, each word pale → ink. Lay the line out at its FINAL width from the start (words not yet shown are
  // invisible, not missing), so it never re-centres while it builds: a re-centring line was rejected as "not smooth".
  const wordsHTML = (items, t, ink, pale) => items.map(([w, at, acc]) => {
    const k = W(t, at, at + 0.13), col = acc || ink;
    return `<span style="color:${t < at ? 'transparent' : k >= 1 ? col : mix(pale, col, k)}">${esc(w)}</span>`;
  }).join(' ');

  // ------------------------------------------------------------------ cursor (macOS arrow), widget pop
  const CUR = '<svg viewBox="0 0 24 24" width="44" height="44" style="display:block;overflow:visible"><path d="M5 2.5l13.2 13.1-6 .3 3.6 7.3-2.6 1.2-3.6-7.4-4.6 4.2z" fill="#111" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/></svg>';
  const cursor = (root) => reg(div(root, 'width:44px;height:44px;z-index:5;filter:drop-shadow(0 3px 5px rgba(0,0,0,.3))', CUR), { o: 0 });
  // the cursor arrives a beat before the click and dips 15 % on it
  const putCursor = (e, x, y, o, dip = 0) => put(e, { o, css: { transform: `translate(${(x - 7).toFixed(2)}px,${(y - 3).toFixed(2)}px) scale(${(1 - 0.15 * cl(dip)).toFixed(4)})` } });
  const bump = (t, at, w) => Math.exp(-Math.pow((t - at) / w, 2));
  // a card/widget pops in: scale 0.55 → 1 with overshoot. Start it within ~0.06 s of the cut: a shot that opens on
  // empty paper for a third of a second reads as a glitch.
  const pop = (e, t, at) => { const k = W(t, at, at + 0.42); put(e, { o: cl(k * 4), css: { transform: `scale(${L(0.55, 1, back(k)).toFixed(4)})`, transformOrigin: '50% 50%' } }); };

  // ------------------------------------------------------------------ shots
  // shot(name, t0, t1, build(root, S), run(t, S)): a hard cut at t0 (story seconds), paper underneath
  const UI = { bg: '#FCFCFA', ink: '#191815', ink2: '#54524D', pale: '#D9D6CF', acc: '#FFCF33', accInk: '#816500' };   // ← your brand tokens
  const shot = (name, t0, t1, build, run) => scene({ name, from: b(t0), to: b(t1),
    build(root, S) { root.style.background = UI.bg; build(root, S); }, run(t, bb, S) { run(t, S); } });

  // --- EXAMPLE 1 · 0–2.4 · a line of words, typed, with a slow push (the camera never sits still)
  shot('line', 0, 2.4, (root, S) => {
    S.g = reg(div(root, `left:${pk(0, 60)}px;top:${MY - 60}px;width:${VW - 2 * pk(0, 60)}px;text-align:center;font-family:Display;font-weight:800;font-size:${pk(96, 84)}px;line-height:1.1;letter-spacing:-0.04em;color:${UI.ink}`));
  }, (t, S) => {
    put(S.g, { html: typed('Your opening line.', t, 0.1, 0.8, UI.ink, UI.pale), css: { transform: `scale(${L(1, 1.03, W(t, 0, 2.4)).toFixed(4)})` } });
  });
  // --- EXAMPLE 2 · 2.4–5 · a prompt typed into an input, then a click on send
  shot('prompt', 2.4, 5, (root, S) => {
    S.c = camRoot(root);
    S.box = div(S.c, 'left:460px;top:480px;width:1000px;height:120px;border-radius:22px;background:#fff;box-shadow:0 0 0 1px #E3E1DC,0 6px 24px -10px rgba(0,0,0,.15)');
    S.inp = reg(div(S.box, 'left:28px;top:26px;font-size:24px;white-space:nowrap'));
    S.send = div(S.box, 'left:936px;top:64px;width:40px;height:40px;border-radius:10px;background:#D97757');
    S.cur = cursor(S.c);
  }, (t, S) => {
    const typeA = 2.6, typeZ = 4.0, sendAt = 4.5;
    cam(S.c, pk(1.0, 1.6) * L(1, 1.04, W(t, 2.4, 5)), L(960, 1300, io(W(t, typeZ, sendAt))), 540);
    put(S.inp, { html: keyed('Describe what you want, in plain words', t, typeA, typeZ, '#141413') });
    const k = io(W(t, typeZ + 0.05, sendAt - 0.05));
    putCursor(S.cur, L(1240, 1416, k), L(700, 604, k), W(t, typeZ, typeZ + 0.1), bump(t, sendAt, 0.07));
  });
  // --- EXAMPLE 3 · 5–7.4 · words on one side, picture on the other (stacked in 9:16)
  shot('split', 5, 7.4, (root, S) => {
    S.pan = div(root, PT ? 'left:40px;top:200px;width:1000px;height:940px' : 'left:40px;top:40px;width:900px;height:1000px', '');
    S.pan.style.cssText += ';border-radius:28px;overflow:hidden;background:#F1F0EC;box-shadow:0 0 0 1.5px #DEDCD8';
    S.say = reg(div(root, `${PT ? 'left:80px;top:1240px;width:920px;font-size:76px' : 'left:1000px;top:480px;width:840px;font-size:60px'};font-family:Display;font-weight:700;line-height:1.15;letter-spacing:-0.03em;color:${UI.ink}`));
  }, (t, S) => {
    put(S.say, { html: typed('Straight from the source.', t, 5.1, 5.7, UI.ink, UI.pale) });
  });

  C.start();

  // ------------------------------------------------------------------ pacing (after C.start, wraps window.seek)
  // Write the film in "story time", then stretch it here instead of editing every timing:
  //  · SLOW: the whole film plays at 1/SLOW speed, so every cut, push, typing beat and cue moves together and the rhythm
  //    holds. First cuts are almost always too fast for a viewer ("looks a bit faster"); 1.2 fixed it.
  //  · reading holds: at story time a, h seconds where the clock runs at E speed, so a line can be read to the end while
  //    things still drift ("too fast, I cannot even complete reading"). Rule of thumb: words ÷ 3 + 0.5 s on screen.
  //  · inserts (to: storyTime): jump to a shot that lives past the end of the story (a persona card, a montage wall)
  // The timeline's sfx/samples and the voiceover are placed in VIDEO seconds: run scripts/cuts.mjs to print the cuts and
  // UNWARP(storyTime) for any moment you need to cue.
  const SLOW = 1.0, E = 0.15, seek0 = window.seek;
  const EV = [
    // { a: 0.8, h: 1.0, d: 1.0 * (1 - E) },        // hold the opening line ~1 s
    // { a: 2.4, h: 1.4, d: 1.4, to: 40 },          // insert the shot living at story 40–41.4 before 'prompt'
  ].sort((x, y) => x.a - y.a);
  const warp = (u) => { let off = 0; for (const e of EV) { const ua = e.a + off; if (u < ua) return u - off; if (u < ua + e.h) return e.to != null ? e.to + (u - ua) : e.a + (u - ua) * E; off += e.d; } return u - off; };
  const unwarp = (f) => { let off = 0; for (const e of EV) { if (f < e.a) return f + off; off += e.d; } return f + off; };
  window.seek = (t) => seek0(warp(t / SLOW));
  window.CUTS = (window.CUTS || []).map((c) => unwarp(c) * SLOW).sort((a, b) => a - b);
  window.UNWARP = (f) => unwarp(f) * SLOW;
})();
