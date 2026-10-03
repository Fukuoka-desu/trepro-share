// 全画面 × 2テーマのコンタクトシート、長時間つけっぱなしの見え方、動きのコマ送りを撮る
//   node test/shots.mjs
import fs from 'node:fs';
import path from 'node:path';
import { launch, openDemo, settle, localFontsOnly, REPORT, SLIDES, LABEL, THEMES, THEME_LABEL } from './lib.mjs';

const SHOTS = path.join(REPORT, 'shots');
fs.mkdirSync(SHOTS, { recursive: true });

const browser = await launch();
const { page, srv, errors } = await openDemo(browser, 'shot=1&energy-time=13');

async function grab(slide, theme, t, file) {
  await page.evaluate(([s, th, tt]) => {
    window.demo.ef.freeze(tt);
    window.demo.show(window.demo.slides.indexOf(s));
    window.demo.setTheme(th);
  }, [slide, theme, t]);
  await settle(page);
  const buf = await page.screenshot({ type: 'jpeg', quality: 88 });
  if (file) fs.writeFileSync(path.join(SHOTS, file), buf);
  return buf.toString('base64');
}

async function compose(items, cols, title, out, thumbW = 720) {
  const sheet = await browser.newPage({ viewport: { width: cols * (thumbW + 20) + 40, height: 400 }, deviceScaleFactor: 1 });
  await localFontsOnly(sheet);
  const cells = items.map((it) => `<figure><img src="data:image/jpeg;base64,${it.b64}"><figcaption>${it.label}</figcaption></figure>`).join('');
  await sheet.setContent(`<!doctype html><html lang="ja"><head><meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@700;800&display=swap" rel="stylesheet">
    <style>
      body{margin:0;padding:20px;background:#05070F;color:#E9EEF9;font-family:"Hiragino Sans","Noto Sans JP",sans-serif}
      h1{margin:0 0 14px;font-size:22px;font-weight:800}
      .g{display:grid;grid-template-columns:repeat(${cols},${thumbW}px);gap:20px}
      figure{margin:0} img{display:block;width:${thumbW}px;height:auto;border-radius:6px;box-shadow:0 0 0 1px #1B2440}
      figcaption{margin-top:6px;font-size:15px;font-weight:700;color:#8E9AB8}
    </style></head><body><h1>${title}</h1><div class="g">${cells}</div></body></html>`);
  await sheet.evaluate(() => document.fonts.ready);
  await sheet.waitForTimeout(300);
  fs.writeFileSync(path.join(REPORT, out), await sheet.screenshot({ type: 'jpeg', quality: 82, fullPage: true }));
  await sheet.close();
}

// 1) コンタクトシート
const sheetItems = [];
for (const s of SLIDES) {
  for (const th of THEMES) {
    sheetItems.push({ b64: await grab(s, th, 13, `${s}-${th}.jpg`), label: `${LABEL[s]} ／ ${THEME_LABEL[th]}` });
  }
}
await compose(sheetItems, 2, 'エネルギー体背景 ／ 全画面 × 2テーマ（t = 13秒）', 'contact-sheet.jpg');

// 2) 長時間つけっぱなし: 時刻の数値が大きくなっても模様が崩れないか
const longItems = [];
for (const [t, label] of [[13, '開始直後'], [3613, '1時間後'], [14413, '4時間後'], [86413, '24時間後']]) {
  longItems.push({ b64: await grab('cover', 'navy', t, `long-${t}.jpg`), label });
}
await compose(longItems, 4, '長時間つけっぱなしでも模様が崩れないか（表紙 ／ 濃紺）', 'long-run.jpg', 560);

// 3) 動きのコマ送り: 6秒ごと
const motionItems = [];
for (let t = 0; t <= 30; t += 6) {
  motionItems.push({ b64: await grab('cover', 'navy', t, `motion-${t}.jpg`), label: `${t}秒` });
}
await compose(motionItems, 3, '6秒ごとのコマ送り（表紙 ／ 濃紺）', 'motion-strip.jpg', 560);

console.log('errors:', errors.length ? errors : 'none');
await browser.close();
srv.close();
