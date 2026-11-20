// Ask the film page for numbers you need for cues and the voiceover (video seconds, after the pacing warp).
//   node tools/probe.mjs cuts                     every hard cut, then the middle of every shot (for one still per shot)
//   node tools/probe.mjs "window.UNWARP(12.4)"    any expression, evaluated after the film loads
//   node tools/probe.mjs --fmt 9x16 cuts
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { createRequire } from 'node:module';
const ROOT = process.cwd();
const { chromium } = createRequire(path.join(ROOT, 'package.json'))('playwright');
const argv = process.argv.slice(2), fi = argv.indexOf('--fmt'), fmt = fi >= 0 ? argv.splice(fi, 2)[1] : '16x9';
const MIME = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.png': 'image/png', '.webp': 'image/webp', '.jpg': 'image/jpeg' };
const server = http.createServer((req, res) => {
  const f = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res);
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const browser = await chromium.launch();
const [w, h] = fmt === '9x16' ? [1080, 1920] : fmt === '1x1' ? [1080, 1080] : fmt === '4x5' ? [1080, 1350] : [1920, 1080];
const page = await browser.newPage({ viewport: { width: w, height: h } });
await page.goto(`http://127.0.0.1:${server.address().port}/film/index.html?fmt=${fmt}`);
await page.waitForFunction(() => window.READY && typeof window.seek === 'function', null, { timeout: 120000 });
await page.evaluate(() => window.seek(0.01));
for (const q of argv) {
  if (q === 'cuts') {
    const { cuts, dur } = await page.evaluate(() => ({ cuts: window.CUTS || [], dur: window.DURATION }));
    const c = [0, ...cuts, dur];
    console.log('cuts ', JSON.stringify(cuts.map((x) => +x.toFixed(2))));
    console.log('mids ', c.slice(1).map((z, i) => ((c[i] + z) / 2).toFixed(2)).join(','));
  } else console.log(q, '→', JSON.stringify(await page.evaluate(q)));
}
await browser.close(); server.close();
