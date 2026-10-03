// 文字の後ろの背景を実測して、最低コントラスト比を出す
//   node test/contrast.mjs            → report/contrast.json, report/contrast.md
//   node test/contrast.mjs --write-demo  → demo.html の実測値も更新
//
// 1. 表示中の画面の文字を1行ずつ (Range の矩形) 取り出し、文字色を記録
// 2. 文字だけ透明にして撮影 (カードの下地などはそのまま)
// 3. 各矩形の中で、文字色にいちばん近い明るさの画素を探し、WCAG のコントラスト比を計算
// 4. 呼吸のひと回り (37秒) 以上を10回に分けて撮り、いちばん悪い値を採用
import fs from 'node:fs';
import path from 'node:path';
import { launch, openDemo, settle, ROOT, REPORT, SLIDES, LABEL, THEMES, THEME_LABEL } from './lib.mjs';

const TIMES = [0, 3.7, 7.4, 11.1, 14.8, 18.5, 22.2, 25.9, 29.6, 33.3, 37];
const writeDemo = process.argv.includes('--write-demo');

const browser = await launch();
const { page, srv, errors } = await openDemo(browser, 'shot=1&energy-time=0');

const results = {};
for (const slide of SLIDES) {
  for (const theme of THEMES) {
    await page.evaluate(([s, th]) => {
      window.demo.ef.freeze(0);
      window.demo.show(window.demo.slides.indexOf(s));
      window.demo.setTheme(th);
    }, [slide, theme]);
    await settle(page);

    const runs = await page.evaluate(() => {
      const out = [];
      const slideEl = document.querySelector('.slide.is-active');
      const walker = document.createTreeWalker(slideEl, NodeFilter.SHOW_TEXT, {
        acceptNode: (n) => (n.textContent.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT)
      });
      let n;
      while ((n = walker.nextNode())) {
        const el = n.parentElement;
        const cs = getComputedStyle(el);
        const m = cs.color.match(/[\d.]+/g).map(Number);
        const range = document.createRange();
        range.selectNodeContents(n);
        for (const r of range.getClientRects()) {
          if (r.width < 2 || r.height < 2) continue;
          out.push({ x: r.left, y: r.top, w: r.width, h: r.height, rgb: m.slice(0, 3), px: parseFloat(cs.fontSize), weight: cs.fontWeight, text: n.textContent.trim().slice(0, 20) });
        }
      }
      return out;
    });

    await page.addStyleTag({ content: '.slide.is-active, .slide.is-active * { color: transparent !important; text-shadow: none !important; }' });

    let worst = null;
    for (const t of TIMES) {
      await page.evaluate((tt) => window.demo.ef.freeze(tt), t);
      await settle(page);
      const b64 = (await page.screenshot({ type: 'png' })).toString('base64');
      const measured = await page.evaluate(async ([b, rs]) => {
        const img = new Image();
        img.src = 'data:image/png;base64,' + b;
        await img.decode();
        const c = document.createElement('canvas');
        c.width = img.width; c.height = img.height;
        const ctx = c.getContext('2d', { willReadFrequently: true });
        ctx.drawImage(img, 0, 0);
        const LUT = new Float64Array(256);
        for (let i = 0; i < 256; i++) { const v = i / 255; LUT[i] = v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }
        const lum = (r, g, b) => 0.2126 * LUT[r] + 0.7152 * LUT[g] + 0.0722 * LUT[b];
        return rs.map((r) => {
          const x0 = Math.max(0, Math.floor(r.x)), y0 = Math.max(0, Math.floor(r.y));
          const w = Math.max(1, Math.min(c.width - x0, Math.ceil(r.w))), h = Math.max(1, Math.min(c.height - y0, Math.ceil(r.h)));
          const d = ctx.getImageData(x0, y0, w, h).data;
          let lmin = 1, lmax = 0;
          for (let i = 0; i < d.length; i += 4) {
            const L = lum(d[i], d[i + 1], d[i + 2]);
            if (L < lmin) lmin = L;
            if (L > lmax) lmax = L;
          }
          const Lt = lum(Math.round(r.rgb[0]), Math.round(r.rgb[1]), Math.round(r.rgb[2]));
          const bg = Lt >= lmax ? lmax : Lt <= lmin ? lmin : Lt;
          const cr = (Math.max(Lt, bg) + 0.05) / (Math.min(Lt, bg) + 0.05);
          return { cr, lmin, lmax };
        });
      }, [b64, runs]);
      measured.forEach((m, i) => {
        if (!worst || m.cr < worst.cr) worst = { cr: m.cr, t, text: runs[i].text, px: runs[i].px, bgMin: m.lmin, bgMax: m.lmax };
      });
    }

    await page.evaluate(() => { const s = document.head.querySelectorAll('style'); s[s.length - 1].remove(); });
    results[`${slide}:${theme}`] = { slide, theme, runs: runs.length, ...worst };
    console.log(`${slide}:${theme}`, worst.cr.toFixed(2), `"${worst.text}"`, `t=${worst.t}`);
  }
}

fs.mkdirSync(REPORT, { recursive: true });
fs.writeFileSync(path.join(REPORT, 'contrast.json'), JSON.stringify(results, null, 2));

const grade = (v) => (v >= 7 ? 'AAA' : v >= 4.5 ? 'AA' : v >= 3 ? '大きい文字のみ可' : '要修正');
const lines = [
  '# 文字の上で測ったコントラスト',
  '',
  '`node test/contrast.mjs` の結果です。表示中の画面の文字を1行ずつ取り出し、文字だけ透明にした画面を、背景の呼吸のひと回り（37秒）以上を10回に分けて撮りました。各行の範囲の中で文字色にいちばん近い明るさの画素を探し、WCAG のコントラスト比を計算しています。表の値は、その画面のすべての行・すべての時刻の中で、いちばん悪い値です。',
  '',
  '| 画面 | テーマ | 最低コントラスト | 判定 | いちばん厳しかった文字 | 文字サイズ（1920×1080で） |',
  '|---|---|---:|---|---|---:|'
];
for (const r of Object.values(results)) {
  lines.push(`| ${LABEL[r.slide]} | ${THEME_LABEL[r.theme]} | ${(Math.floor(r.cr * 10) / 10).toFixed(1)} : 1 | ${grade(r.cr)} | ${r.text} | ${Math.round(r.px)}px |`);
}
lines.push('', '判定の目安: AA は 4.5 : 1 以上、AAA は 7 : 1 以上（WCAG 2.x）。値は小数第2位を切り捨てています。');
fs.writeFileSync(path.join(REPORT, 'contrast.md'), lines.join('\n') + '\n');

if (writeDemo) {
  const map = {};
  for (const [k, r] of Object.entries(results)) map[k] = Math.floor(r.cr * 10) / 10;
  const file = path.join(ROOT, 'demo.html');
  const html = fs.readFileSync(file, 'utf8');
  const next = html.replace(/\/\*CONTRAST:BEGIN\*\/[\s\S]*?\/\*CONTRAST:END\*\//, `/*CONTRAST:BEGIN*/${JSON.stringify(map)}/*CONTRAST:END*/`);
  fs.writeFileSync(file, next);
  console.log('demo.html updated');
}

console.log('errors:', errors.length ? errors : 'none');
await browser.close();
srv.close();
