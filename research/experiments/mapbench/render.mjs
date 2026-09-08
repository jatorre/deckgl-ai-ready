// Render every generated map headlessly, capture errors/network failures/screenshots, write render/<model>/<task>.json
// Usage: node render.mjs [model-slug ...]
import { chromium } from '/Users/jatorre/workspace/cloud-native/node_modules/playwright/index.mjs';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(HERE, 'out');
const REN = path.join(HERE, 'render');
const PORT = 8765;
const cfg = JSON.parse(fs.readFileSync(path.join(HERE, 'tasks.json'), 'utf8'));
const slugs = process.argv.slice(2).length ? process.argv.slice(2) : Object.keys(cfg.models);

const server = spawn('python3', ['-m', 'http.server', String(PORT), '--bind', '127.0.0.1'], { cwd: OUT, stdio: 'ignore' });
await new Promise(r => setTimeout(r, 800));

const browser = await chromium.launch({
  headless: true,
  args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl']
});

async function renderOne(slug, tkey) {
  const html = path.join(OUT, slug, `${tkey}.html`);
  if (!fs.existsSync(html)) return `missing ${slug}/${tkey}`;
  const dir = path.join(REN, slug); fs.mkdirSync(dir, { recursive: true });
  const report = { slug, task: tkey, console_errors: [], console_warnings: [], page_errors: [], request_failed: [], http_errors: [], scripts: [], screenshots: {} };
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  page.on('console', m => { const t = m.type(); if (t === 'error') report.console_errors.push(m.text().slice(0, 300)); else if (t === 'warning') report.console_warnings.push(m.text().slice(0, 200)); });
  page.on('pageerror', e => report.page_errors.push(String(e.message || e).slice(0, 300)));
  page.on('requestfailed', r => report.request_failed.push(`${r.url().slice(0, 160)} :: ${r.failure()?.errorText}`));
  page.on('response', r => { if (r.status() >= 400) report.http_errors.push(`${r.status()} ${r.url().slice(0, 160)}`); });
  const t0 = Date.now();
  try {
    await page.goto(`http://127.0.0.1:${PORT}/${slug}/${tkey}.html`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    for (const t of [3, 8, 14]) {
      const elapsed = (Date.now() - t0) / 1000;
      if (elapsed < t) await page.waitForTimeout((t - elapsed) * 1000);
      const shot = path.join(dir, `${tkey}.t${t}.png`);
      await page.screenshot({ path: shot, timeout: 15000 });
      report.screenshots[`t${t}`] = path.relative(HERE, shot);
    }
    report.dom = await page.evaluate(() => {
      const canvases = [...document.querySelectorAll('canvas')].map(c => ({ w: c.width, h: c.height, cls: c.className.slice(0, 60), id: c.id }));
      const scripts = [...document.querySelectorAll('script[src]')].map(s => s.src);
      const links = [...document.querySelectorAll('link[rel=stylesheet]')].map(l => l.href);
      return { canvases, scripts, links, hasDeckGlobal: typeof window.deck !== 'undefined', hasMaplibreGlobal: typeof window.maplibregl !== 'undefined',
        hasMapboxGlobal: typeof window.mapboxgl !== 'undefined', bodyText: document.body.innerText.slice(0, 400),
        buttons: [...document.querySelectorAll('button')].map(b => b.innerText.slice(0, 30)), sliders: document.querySelectorAll('input[type=range]').length,
        title: document.title };
    });
    report.scripts = report.dom.scripts;
    const v = report.scripts.map(s => (s.match(/deck\.gl@([^/]+)/) || [])[1]).filter(Boolean);
    report.deckgl_cdn_version = v[0] || null;
    report.maplibre_cdn_version = (report.scripts.map(s => (s.match(/maplibre-gl@([^/]+)/) || [])[1]).filter(Boolean))[0] || null;
  } catch (e) {
    report.fatal = String(e.message || e).slice(0, 300);
  }
  report.total_seconds = Math.round((Date.now() - t0) / 100) / 10;
  await ctx.close();
  fs.writeFileSync(path.join(dir, `${tkey}.json`), JSON.stringify(report, null, 1));
  const flag = report.fatal ? 'FATAL' : (report.page_errors.length || report.console_errors.length || report.http_errors.length || report.request_failed.length) ? 'issues' : 'clean';
  return `${flag.padEnd(6)} ${slug}/${tkey} pageErr=${report.page_errors.length} consoleErr=${report.console_errors.length} http4xx=${report.http_errors.length} reqFail=${report.request_failed.length} canvases=${report.dom?.canvases?.length ?? '?'} deck=${report.deckgl_cdn_version ?? '?'}`;
}

for (const slug of slugs) for (const tkey of Object.keys(cfg.tasks)) console.log(await renderOne(slug, tkey));
await browser.close(); server.kill();
