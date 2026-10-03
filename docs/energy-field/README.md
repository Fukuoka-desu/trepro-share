# エネルギー体背景（energy-field.js）

講演スライドの後ろで、AIの「エネルギー体」がじんわり動く背景部品です。WebGL で描く1ファイルの JavaScript で、ほかのライブラリは要りません。

- 光の核が20〜40秒の周期で呼吸し、まわりをプラズマの筋と光の粒がゆっくり巡ります
- 濃紺と白地の2テーマ。画面の種類（表紙・扉・本文カードなど）ごとに強さと位置が変わります
- 文字の下だけ光を抑えるので、どこに文字があっても読みやすさが落ちません（実測の最低コントラスト 5.3 : 1 以上）
- 1秒30コマ・画面の半分の解像度で描き、90分つけっぱなしでもメモリが増え続けない作りです

見本ページは `demo.html` です。全画面 × 2テーマの見え方は `report/contact-sheet.jpg` にまとめています。

---

## 資料への組み込み

### 1. ファイルを置いて読み込む

`energy-field.js` を資料の `assets/js/` に置き、`index.html` の最後で読み込みます。

```html
<script src="assets/js/energy-field.js"></script>
<script>
  const energy = EnergyField.mount({
    container: '#deck',            // スライドを並べている一番外の要素。省略すると画面全体に固定
    theme: 'navy',                 // 'navy'（濃紺）か 'white'（白地）
    preset: 'cover',               // 最初の画面の種類
    protect: '.slide.is-active',   // 表示中の画面。この中の文字の下だけ光を抑える
  });
</script>
```

### 2. スライドの背景を透明にする

背景はエネルギー体が描くので、スライド自身の背景色は透明にします。起動すると `<html>` に `energy-field-on` が付くので、それを使えば元の CSS を残したまま切り替えられます。

```css
.energy-field-on .slide { background: transparent; }
```

### 3. 画面が変わるたびに1行呼ぶ

```js
energy.set({ preset: 'content', theme: 'white' });
```

拍（→キー）ごとに呼んでも大丈夫です。同じ値なら何も起きず、違えば1〜2秒かけてなめらかに移ります。呼ぶたびに文字の位置も測り直すので、拍ごとに文字が増える画面では、拍ごとに呼ぶと増えた文字の下もすぐに守られます。呼び出しの代わりに、`<html>` の属性を書き換えても同じように動きます。

```js
document.documentElement.dataset.energy = 'content';     // 画面の種類
document.documentElement.dataset.energyTheme = 'white';  // テーマ
```

---

## 画面の種類

`preset` には英語名のほか、日本語の呼び名もそのまま渡せます（例：`'表紙'` `'本文'` `'見せ場'` `'持ち帰り'`）。知らない名前は `content` として扱い、コンソールに一度だけ警告を出します。

| 名前 | 日本語の呼び名 | 強さ | 置き場所 | 向いている画面 |
|---|---|---:|---|---|
| `cover` | 表紙 | 100% | 右寄り | 表紙。演題は左に置く |
| `section` | 扉・章扉・セクション | 85% | 右寄り | セクションの扉 |
| `statement` | 主張・一言 | 55% | 中央の下 | 一文だけの大きなメッセージ |
| `content` | 本文・カード | 42% | 右下の隅 | 箇条書き、カード型の画面 |
| `dense` | 表 | 24% | 右下の隅 | 表や数字の多い画面 |
| `visual` | 図解・見せ場・図 | 22% | 中央に大きく薄く | コードで描く図（地球儀・年表など） |
| `video` | 動画・実演 | 8% | 中央 | 実演動画 |
| `ending` | 締め・持ち帰り・まとめ | 90% | 中央の下 | 最後の持ち帰り |
| `quiet` | 静か | 14% | 右下 | 質疑など |
| `off` | 暗転・なし | 0% | — | 光を消す（描画も止まる） |

数値は `EnergyField.presets` で書き換えられます。

```js
EnergyField.presets.content.intensity = 0.3;   // 本文の画面を少し弱く
energy.set({ preset: 'content' });              // 次に呼んだときから反映
```

1枚だけ変えたいときは、`set` に数値を直接渡します。

```js
energy.set({ preset: 'cover', x: 0.8, radius: 0.35 });   // x, y は画面に対する比率（y は上が 0）
```

---

## 文字の読みやすさ

明るさを2段階で抑えています。

1. **文字の下**：`protect` で指定した範囲の文字を1行ずつ測り、その下だけ明るさに上限をかけます。濃紺テーマでは相対輝度 0.08 以下（白文字で 11 : 1、薄い青 `#C8D5F0` の文字でも 5.5 : 1）、白地テーマでは 0.70 以上（`#0B1630` の文字で 12.7 : 1、青 `#1F4FD8` の文字でも 5 : 1）です。境目はぼかしてあるので、四角く暗くなったようには見えません。
2. **画面全体**：画面の種類ごとに明るさの上限（濃紺）と下限（白地）を決めています。たとえば本文カードの画面は、文字がどこにあっても白文字で 7.5 : 1 を下回りません。

上限をかけるときは青を残して赤と緑を多めに落とすので、光が灰色にくすまず、青く光ったまま暗くなります。

見本ページの全画面を実測した結果は `report/contrast.md` にあります。いちばん悪い値でも 5.3 : 1 で、WCAG の AA（4.5 : 1）を超えています。

文字の位置は `set()` を呼んだときと、その0.7秒後（出だしのアニメーションが終わるころ）に測ります。`visibility: hidden` や `display: none` の文字は数えず、`opacity: 0` で隠れている文字は数えます（先に守っておくので、出てきた瞬間に背景が変わりません）。寄る（Z）などで中身が動いたあとは `energy.protect()` を呼ぶと測り直します。

コードで描いた図の文字（canvas に直接描いた文字など）は自動では見つけられないので、矩形を渡してください。

```js
energy.protect([document.querySelector('#globe-label'), { left: 120, top: 80, width: 600, height: 90 }]);
```

---

## 講師用・復習用の画面

| 画面 | おすすめの設定 |
|---|---|
| `index.html`（観客用） | 上の設定のまま |
| `presenter.html` のプレビュー（iframe） | URL に `?energy=low` を付ける。1秒20コマ・解像度35%で軽く動きます。止めたいときは `?energy=static`、消すなら `?energy=off` |
| `read.html`（復習用・スマホ） | `EnergyField.mount({ mode: 'static' })`。1枚の絵として描き、電池を使いません |

### 暗転（B キー）・一覧（G キー）・見せ場

```js
energy.pause();                      // 暗転中は描画を止める
energy.resume();                     // 戻す
energy.set({ preset: 'quiet' });     // 一覧を開いている間は静かにして、サムネイルを見やすく
energy.pulse(0.3);                   // 見せ場で一瞬だけ光を強める（2〜3秒で元に戻る）
```

---

## 検品（スクリーンショット）

URL に `?energy-time=秒数` を付けると時間が止まり、何度撮っても同じ絵になります。画面の切り替えも一瞬で終わります。

```js
// Playwright の例
await page.goto('http://127.0.0.1:8765/index.html?energy-time=13');
await page.evaluate(() => EnergyField.current.ready);   // 最初の1コマが描けるまで待つ
await page.screenshot({ path: 'cover.png' });
```

`?energy-debug=1` を付けると、左下にコマ数・解像度・画面の種類が出ます。本番の Mac で重さを確かめるときに使ってください。

---

## 色を資料に合わせる

`:root` に CSS 変数を書くと、その色で描きます（`#` から始まる16進数で）。

```css
:root {
  --energy-navy-top: #0B1736;      /* 濃紺テーマの上端 */
  --energy-navy-bottom: #050B1F;   /* 濃紺テーマの下端 */
  --energy-white-top: #FFFFFF;
  --energy-white-bottom: #F2F5FB;
  --energy-deep: #1A3C9E;          /* まわりの光 */
  --energy-blue: #2F6BFF;          /* 本体 */
  --energy-cyan: #5AD8FF;          /* 光の筋と粒 */
  --energy-violet: #7C5CFF;        /* 本体の差し色 */
}
```

`mount({ colors: { navyTop: '#0A1A3F' } })` のように JavaScript から渡すこともできます。

---

## 90分の本番に向けて

- **重さ**：1秒30コマ、内部の解像度は画面の半分（1920×1080 の投影なら 960×540）。描画が目標の1.6倍以上遅い状態が90コマ（数秒）続くと、自動で解像度を2割ずつ下げます（25% まで。上げ直しはしません）
- **メモリ**：毎コマの処理では新しいオブジェクトを作りません。画像やバッファも起動時に1つ作るだけです。`report/soak.md` に、画面とテーマを切り替えながら回し続けた試験の結果があります
- **止める条件**：タブが裏に回ると描画を止め、戻ると再開します。強さ 0 の画面（`off`）でも止まります
- **GPU が落ちたとき**：WebGL のコンテキストが失われても、戻り次第自動で描き直します
- **WebGL が使えない環境**：CSS のグラデーションで代わりの背景を出します（動きません）
- **時間の数え方**：その日の0時からの秒数で描くので、観客用と講師用のウィンドウでほぼ同じ模様になり、ページを開き直しても模様が飛びません。24時間分の数値でも模様が崩れないことを `report/long-run.jpg` で確かめています
- **「視差効果を減らす」**：Mac の設定（アクセシビリティ → ディスプレイ → 視差効果を減らす）がオンだと、動かない1枚の絵になります。本番の Mac で動かないときはここを確認してください。設定に関係なく動かすなら `respectReducedMotion: false`

---

## 設定一覧（`EnergyField.mount` に渡す）

| 設定 | 既定値 | 内容 |
|---|---|---|
| `container` | body | 背景を入れる要素（セレクタでも可）。省略すると画面全体に固定 |
| `theme` | `'navy'` | `'navy'` か `'white'` |
| `preset` | `'cover'` | 最初の画面の種類 |
| `protect` | なし | 文字を守る範囲（セレクタ・要素・要素や矩形の配列） |
| `mode` | `'live'` | `'live'` / `'low'`（軽量）/ `'static'`（止めた絵）/ `'off'`（描かない） |
| `fps` | 30 | 1秒あたりのコマ数 |
| `scale` | 0.5 | 内部の解像度（CSS ピクセルに対する比率） |
| `safeCap` | 0.08 | 文字の下の明るさの上限（濃紺テーマ） |
| `safeFloor` | 0.70 | 文字の下の明るさの下限（白地テーマ） |
| `fadeDuration` | 1.4 | 強さが変わるのにかける秒数 |
| `moveDuration` | 2.2 | 位置・大きさが変わるのにかける秒数 |
| `themeDuration` | 0.35 | 濃紺と白地を切り替える秒数（文字色の切り替えと合わせる） |
| `colors` | なし | 色の指定（上の CSS 変数と同じ8色） |
| `zIndex` | -1 | canvas の重なり順 |
| `respectReducedMotion` | true | 「視差効果を減らす」がオンなら止めた絵にする |
| `autoQuality` | true | 重いときに自動で解像度を下げる |
| `observe` | true | `<html data-energy>` の書き換えを見張る |
| `debug` | false | 左下にコマ数などを出す |
| `freeze` | なし | 秒数を入れると時間を止める |

URL でも同じものを上書きできます：`?energy=low|static|off|live`、`?energy-time=13`、`?energy-debug=1`、`?energy-fps=20`、`?energy-scale=0.4`、`?energy-preset=content`、`?energy-theme=white`。

## 操作（`mount` が返すもの）

| 呼び方 | 内容 |
|---|---|
| `set({ preset, theme, intensity, x, y, radius, cap, floor, aurora, particles, protect, colors })` | 見え方を変える。2つ目の引数に `{ instant: true }` で一瞬で切り替え |
| `protect(範囲)` | 文字を守る範囲を変えて、すぐ測り直す。`null` で解除 |
| `pulse(量)` | 一瞬だけ光を強める（既定 0.25） |
| `pause()` / `resume()` | 描画を止める・再開する |
| `freeze(秒)` / `freeze(null)` | 時間を止める・動かす |
| `destroy()` | 背景を取り外す（GPU の資源も返す） |
| `state()` | いまの強さ・位置・テーマ・守っている文字の範囲の数など（調整や検証用） |
| `ready` | 最初の1コマが描けたら解決する Promise |
| `stats` | コマ数・実測 fps・内部の解像度など |

`EnergyField.contrast('#FFFFFF', '#0B1736')` で2色のコントラスト比、`EnergyField.guarantee('content', '#FFFFFF')` でその画面の種類で「どこに重なっても下回らない値」を返します。

---

## 検証スクリプト

Playwright（Chromium）を使います。Mac なら実際の GPU で描きます。

```bash
node test/shots.mjs               # 全画面 × 2テーマ、長時間、6秒ごとのコマ送りを撮る → report/*.jpg
node test/contrast.mjs --write-demo   # 文字の後ろを実測 → report/contrast.md（見本ページの表示も更新）
node test/behavior.mjs            # ループ・切り替え・GPU の復帰・後片付けなど 20 項目を確かめる
node test/soak.mjs 30             # 30分つけっぱなしにしてメモリを測る → report/soak.md
```

## フォント（見本ページの設定）

見本ページは、投影で細く見えないように太字のゴシックで組んでいます。資料側の書体を決めるときの参考にしてください。

```css
--font-display: "Hiragino Sans", "Hiragino Kaku Gothic StdN", "Noto Sans JP", "Yu Gothic", YuGothic, Meiryo, sans-serif;
h1, h2, h3 { font-weight: 800; font-feature-settings: "palt" 1; letter-spacing: 0.02em; text-wrap: balance; word-break: auto-phrase; }
本文 { font-weight: 700; word-break: auto-phrase; text-wrap: pretty; }
```

- 見出しは 800（ヒラギノ角ゴの W8 相当）、本文は 700、いちばん大きい一文は 900
- `word-break: auto-phrase` で、日本語を文節の切れ目で折り返します（Chrome 119 以降）。Safari では効かないので、演題など崩したくない行は `<span style="display:inline-block">` で文節ごとに包むと確実です
- 検証スクリプトの撮影は Linux 上なので Noto Sans JP で描いています。Mac ではヒラギノで表示されます

## ライセンス

シェーダーの中に、MIT ライセンスのコードを2つ含みます（3D simplex noise：Ian McEwan, Stefan Gustavson / Hash without Sine：Dave Hoskins）。著作権表示は `energy-field.js` の先頭にあります。
