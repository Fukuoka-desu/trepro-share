// 検証スクリプト共通: 静的サーバーと Chromium の起動
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const REPORT = path.join(ROOT, 'report');

const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.md': 'text/markdown; charset=utf-8' };

export function serve() {
  return new Promise((resolve) => {
    const srv = http.createServer((req, res) => {
      const u = new URL(req.url, 'http://local');
      const f = path.join(ROOT, decodeURIComponent(u.pathname === '/' ? '/demo.html' : u.pathname));
      if (!f.startsWith(ROOT)) { res.writeHead(403); res.end(); return; }
      fs.readFile(f, (err, buf) => {
        if (err) { res.writeHead(404); res.end(); return; }
        res.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream', 'cache-control': 'no-store' });
        res.end(buf);
      });
    });
    srv.listen(0, '127.0.0.1', () => resolve({ srv, base: `http://127.0.0.1:${srv.address().port}` }));
  });
}

async function loadChromium() {
  const tries = [process.env.PLAYWRIGHT_MODULE, 'playwright', '@playwright/test', '/opt/node22/lib/node_modules/playwright/index.mjs'].filter(Boolean);
  for (const t of tries) {
    try {
      const m = await import(t);
      const chromium = m.chromium || (m.default && m.default.chromium);
      if (chromium) return chromium;
    } catch (e) { /* 次を試す */ }
  }
  throw new Error('playwright が見つかりません (npm i -D playwright)');
}

export async function launch() {
  const chromium = await loadChromium();
  // GPU の無い Linux コンテナでは SwiftShader (CPU) で WebGL を動かす。Mac では実 GPU を使う。
  const args = process.platform === 'linux' ? ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] : [];
  return chromium.launch({ args });
}

// 検証では Google Fonts を読みに行かず、手元に入れたフォント (Noto Sans JP など) で描く
const REMOTE_FONTS = /fonts\.(googleapis|gstatic)\.com/;
export async function localFontsOnly(page) {
  await page.route(REMOTE_FONTS, (route) => route.abort());
}

export async function openDemo(browser, query, viewport = { width: 1920, height: 1080 }) {
  const { srv, base } = await serve();
  const page = await browser.newPage({ viewport, deviceScaleFactor: 1 });
  const errors = [];
  await localFontsOnly(page);
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('requestfailed', (r) => { if (!REMOTE_FONTS.test(r.url())) errors.push('request failed: ' + r.url()); });
  page.on('console', (m) => {
    if (m.type() !== 'error' && m.type() !== 'warning') return;
    if (/Failed to load resource/.test(m.text())) return; // 失敗したリクエストは requestfailed で拾う
    errors.push(m.text());
  });
  await page.goto(`${base}/demo.html?${query}`);
  await page.evaluate(() => window.demo.ef.ready);
  await page.evaluate(() => document.fonts.ready);
  await settle(page);
  return { page, srv, errors };
}

// 2 フレーム待って、背景が描き終わった状態にする
export async function settle(page) {
  const frames = () => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(() => setTimeout(r, 30))));
  await page.evaluate(frames);
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(frames);
}

export const SLIDES = ['cover', 'section', 'statement', 'content', 'visual', 'video', 'ending'];
export const LABEL = { cover: '表紙', section: '扉', statement: '主張', content: '本文カード', visual: '図解', video: '動画', ending: '締め' };
export const THEMES = ['navy', 'white'];
export const THEME_LABEL = { navy: '濃紺', white: '白地' };
