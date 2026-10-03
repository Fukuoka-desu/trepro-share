// 動作の確認: スクリーンショットでは見えない部分 (ループ・切り替え・復帰・後片付け)
//   node test/behavior.mjs
import { launch, serve } from './lib.mjs';

const browser = await launch();
const { srv, base } = await serve();
const results = [];
const check = (name, ok, detail = '') => { results.push({ name, ok }); console.log(`${ok ? 'OK  ' : 'FAIL'} ${name}${detail ? '  (' + detail + ')' : ''}`); };
const wait = (page, ms) => page.waitForTimeout(ms);

async function fresh(opts = {}, before = '') {
  const page = await browser.newPage({ viewport: { width: 800, height: 450 } });
  const warnings = [];
  page.on('console', (m) => { if (m.type() === 'warning') warnings.push(m.text()); });
  page.on('pageerror', (e) => warnings.push('pageerror: ' + e));
  if (opts.reducedMotion) await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.setContent(`<!doctype html><html lang="ja"><body style="margin:0">
    <div id="deck" style="position:relative;width:800px;height:450px"><p id="t" style="position:absolute;left:40px;top:40px;font-size:40px;color:#fff">見出しの文字</p></div>
    <script>${before}</script>
    <script src="${base}/energy-field.js"></script>
    <script>window.ef = EnergyField.mount(${JSON.stringify(opts.mount || { container: '#deck', protect: '#t', autoQuality: false })});</script>
  </body></html>`);
  await page.evaluate(() => window.ef.ready);
  return { page, warnings };
}
const frames = (page) => page.evaluate(() => window.ef.stats.frames);

// 1. 動き続ける / 切り替えが目標に届く
{
  const { page, warnings } = await fresh();
  const f0 = await frames(page); await wait(page, 1500); const f1 = await frames(page);
  check('live: コマが進む', f1 > f0 + 5, `${f0} → ${f1}`);
  check('protect: 文字の範囲を見つける', (await page.evaluate(() => window.ef.state().protectedAreas)) === 1);
  await page.evaluate(() => window.ef.set({ preset: 'content', theme: 'white' }));
  await wait(page, 3500);
  const st = await page.evaluate(() => window.ef.state());
  check('set: 強さが目標に届く', Math.abs(st.intensity - 0.42) < 0.03, st.intensity.toFixed(3));
  check('set: テーマが切り替わる', st.theme === 1);

  // 2. GPU のコンテキストが失われても戻る
  await page.evaluate(() => { window.__lc = window.ef.canvas.getContext('webgl').getExtension('WEBGL_lose_context'); window.__lc.loseContext(); });
  await wait(page, 400);
  const g0 = await frames(page); await wait(page, 600); const g1 = await frames(page);
  check('context lost: 描画が止まる', g1 === g0, `${g0} → ${g1}`);
  await page.evaluate(() => window.__lc.restoreContext());
  await wait(page, 1500);
  const g2 = await frames(page);
  check('context restored: 描画が戻る', g2 > g1 + 3, `${g1} → ${g2}`);

  // 3. タブが裏に回ると止まる
  await page.evaluate(() => { Object.defineProperty(document, 'hidden', { configurable: true, get: () => true }); document.dispatchEvent(new Event('visibilitychange')); });
  await wait(page, 300);
  const h0 = await frames(page); await wait(page, 800); const h1 = await frames(page);
  check('hidden: 描画が止まる', h1 === h0, `${h0} → ${h1}`);
  await page.evaluate(() => { Object.defineProperty(document, 'hidden', { configurable: true, get: () => false }); document.dispatchEvent(new Event('visibilitychange')); });
  await wait(page, 1000);
  check('visible: 描画が戻る', (await frames(page)) > h1 + 3);

  // 4. pause / resume
  await page.evaluate(() => window.ef.pause()); await wait(page, 200);
  const p0 = await frames(page); await wait(page, 700); const p1 = await frames(page);
  check('pause: 止まる', p1 === p0);
  await page.evaluate(() => window.ef.resume()); await wait(page, 900);
  check('resume: 戻る', (await frames(page)) > p1 + 3);

  // 5. off にすると、消え終わったあとループが止まる
  await page.evaluate(() => window.ef.set({ preset: 'off' }));
  await wait(page, 4500);
  const o0 = await frames(page); await wait(page, 800); const o1 = await frames(page);
  check('off: 消え終わるとループが止まる', o1 === o0 && !(await page.evaluate(() => window.ef.state().running)), `${o0} → ${o1}`);
  await page.evaluate(() => window.ef.set({ preset: 'cover' })); await wait(page, 800);
  check('off から戻る', (await frames(page)) > o1 + 3);

  // 6. <html data-energy> で切り替わる
  await page.evaluate(() => { document.documentElement.dataset.energy = '動画'; });
  await wait(page, 100);
  check('data-energy: 日本語名で切り替わる', (await page.evaluate(() => window.ef.stats.preset)) === 'video');

  // 7. 知らない名前は content にして警告は一度だけ
  await page.evaluate(() => { window.ef.set({ preset: 'ないもの' }); window.ef.set({ preset: 'ないもの' }); });
  check('知らない名前: content として扱う', (await page.evaluate(() => window.ef.stats.preset)) === 'content');
  check('知らない名前: 警告は一度だけ', warnings.filter((w) => w.includes('ないもの')).length === 1);

  // 8. 後片付け
  await page.evaluate(() => window.ef.destroy());
  await wait(page, 200);
  const gone = await page.evaluate(() => ({ canvas: !!document.querySelector('canvas.energy-field'), cls: document.documentElement.classList.contains('energy-field-on'), iso: document.getElementById('deck').style.isolation }));
  check('destroy: canvas と目印を外す', !gone.canvas && !gone.cls && gone.iso === '');
  check('エラーが出ていない', !warnings.some((w) => w.startsWith('pageerror')));
  await page.close();
}

// 9. 「視差効果を減らす」がオンなら止めた絵になる
{
  const { page } = await fresh({ reducedMotion: true });
  await wait(page, 300);
  const r0 = await frames(page); await wait(page, 1000); const r1 = await frames(page);
  check('reduced motion: 1枚の絵で止まる', r1 === r0 && r0 >= 1, `${r0} → ${r1}`);
  await page.close();
}

// 10. WebGL が使えないときは CSS の背景に切り替わる
{
  const { page } = await fresh({}, "HTMLCanvasElement.prototype.getContext = function () { return null; };");
  const fb = await page.evaluate(() => ({ el: !!document.querySelector('.energy-field--fallback'), mode: window.ef.stats.mode, bg: getComputedStyle(document.querySelector('.energy-field--fallback')).backgroundImage.slice(0, 15) }));
  check('WebGL なし: CSS の背景で代用', fb.el && fb.mode === 'fallback' && fb.bg.startsWith('radial-gradient'), fb.bg);
  await page.close();
}

// 11. mode: 'off' は何も置かない
{
  const { page } = await fresh({ mount: { container: '#deck', mode: 'off' } });
  check("mode 'off': canvas を置かない", !(await page.evaluate(() => !!document.querySelector('canvas.energy-field'))));
  await page.close();
}

const failed = results.filter((r) => !r.ok).length;
console.log(`\n${results.length - failed}/${results.length} passed`);
await browser.close();
srv.close();
process.exit(failed ? 1 : 0);
