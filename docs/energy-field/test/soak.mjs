// つけっぱなし試験: 画面とテーマを自動で切り替えながら回し、メモリが増え続けないかを見る
//   node test/soak.mjs [分]   (既定 30 分)
// 30秒ごとに GC をかけてから、JS ヒープ・DOM ノード数・イベントリスナー数・描いたコマ数を記録する。
import fs from 'node:fs';
import path from 'node:path';
import { launch, serve, REPORT } from './lib.mjs';

const minutes = parseFloat(process.argv[2] || '30');
const browser = await launch();
const { srv, base } = await serve();
const page = await browser.newPage({ viewport: { width: 960, height: 720 }, deviceScaleFactor: 1 });
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto(`${base}/demo.html?soak=1&energy-autoq=0`);
await page.evaluate(() => window.demo.ef.ready);
const cdp = await page.context().newCDPSession(page);
await cdp.send('Performance.enable');

const rows = [];
const started = Date.now();
async function sample() {
  await cdp.send('HeapProfiler.collectGarbage');
  const { metrics } = await cdp.send('Performance.getMetrics');
  const m = Object.fromEntries(metrics.map((x) => [x.name, x.value]));
  const st = await page.evaluate(() => ({ frames: window.demo.ef.stats.frames, fps: window.demo.ef.stats.fps, w: window.demo.ef.stats.width, h: window.demo.ef.stats.height }));
  const row = { min: (Date.now() - started) / 60000, heapMB: m.JSHeapUsedSize / 1048576, nodes: m.Nodes, listeners: m.JSEventListeners, frames: st.frames, fps: st.fps };
  rows.push(row);
  console.log(`${row.min.toFixed(1)}min heap=${row.heapMB.toFixed(2)}MB nodes=${row.nodes} listeners=${row.listeners} frames=${row.frames} fps=${row.fps} ${st.w}x${st.h}`);
}

await sample();
while ((Date.now() - started) / 60000 < minutes) {
  await page.waitForTimeout(30000);
  await sample();
}

// 最初の2分は立ち上がり (JIT やキャッシュ) として除き、残りで傾きを出す
const steady = rows.filter((r) => r.min >= 2);
const n = steady.length;
const mx = steady.reduce((a, r) => a + r.min, 0) / n;
const my = steady.reduce((a, r) => a + r.heapMB, 0) / n;
const slope = steady.reduce((a, r) => a + (r.min - mx) * (r.heapMB - my), 0) / steady.reduce((a, r) => a + (r.min - mx) ** 2, 0);
const first = steady[0], last = rows[rows.length - 1];
const summary = {
  minutes: last.min, frames: last.frames, avgFps: last.frames / (last.min * 60),
  heapStartMB: first.heapMB, heapEndMB: last.heapMB, heapMaxMB: Math.max(...steady.map((r) => r.heapMB)), heapMinMB: Math.min(...steady.map((r) => r.heapMB)),
  slopeKBperMin: slope * 1024, projected90minKB: slope * 1024 * 90,
  nodes: [Math.min(...rows.map((r) => r.nodes)), Math.max(...rows.map((r) => r.nodes))],
  listeners: [Math.min(...rows.map((r) => r.listeners)), Math.max(...rows.map((r) => r.listeners))],
  errors
};
fs.mkdirSync(REPORT, { recursive: true });
fs.writeFileSync(path.join(REPORT, 'soak.json'), JSON.stringify({ summary, rows }, null, 2));
const md = [
  '# つけっぱなし試験',
  '',
  `\`node test/soak.mjs ${minutes}\` の結果です。見本ページを4秒ごとに次の画面へ、12秒ごとに濃紺と白地を切り替えながら回し、30秒ごとにガベージコレクションをかけてからメモリを測りました（この試験機は GPU が無いので、ソフトウェア描画です）。`,
  '',
  '| 項目 | 結果 |',
  '|---|---|',
  `| 回した時間 | ${summary.minutes.toFixed(1)} 分 |`,
  `| 描いたコマ数 | ${summary.frames.toLocaleString('en-US')} コマ（平均 ${summary.avgFps.toFixed(1)} コマ/秒） |`,
  `| 画面の切り替え | 約 ${Math.round(summary.minutes * 15)} 回（テーマの切り替え 約 ${Math.round(summary.minutes * 5)} 回） |`,
  `| JS ヒープ（2分後 → 終了時） | ${summary.heapStartMB.toFixed(2)} MB → ${summary.heapEndMB.toFixed(2)} MB（幅 ${summary.heapMinMB.toFixed(2)}〜${summary.heapMaxMB.toFixed(2)} MB） |`,
  `| 増え方の傾き | ${summary.slopeKBperMin.toFixed(1)} KB/分（90分に換算して ${summary.projected90minKB.toFixed(0)} KB） |`,
  `| DOM ノード数 | ${summary.nodes[0]}〜${summary.nodes[1]} |`,
  `| イベントリスナー数 | ${summary.listeners[0]}〜${summary.listeners[1]} |`,
  `| ページのエラー | ${errors.length ? errors.join(' / ') : 'なし'} |`,
  ''
].join('\n');
fs.writeFileSync(path.join(REPORT, 'soak.md'), md);
console.log(JSON.stringify(summary));
await browser.close();
srv.close();
