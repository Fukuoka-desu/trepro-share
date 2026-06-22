# GPT Image 2 画像制作・差し込みパイプライン

このブログは、画像が未生成でも本文・代替テキスト・Captionだけで理解できます。画像は概念理解と読後感を補助する編集素材として扱い、重要な手順や数値を画像だけに載せません。

## API上の名称

ChatGPT上の製品名は **ChatGPT Images 2.0** ですが、APIで直接指定する現行モデル名は **`gpt-image-2`** です。再現性を固定したいReleaseでは、Manifestに記載したSnapshot **`gpt-image-2-2026-04-21`** へ切り替えられます。

- 1 Promptから1枚を生成するBuild処理: Image APIのGenerationsを使う。
- 既存画像を参照した編集、人物やブランドの反復調整: Image APIのEditsを使う。
- 会話しながら複数回編集する制作UI: Responses APIのImage Generation Toolを使う。

公式資料:

- https://developers.openai.com/api/docs/guides/image-generation
- https://developers.openai.com/api/docs/models/gpt-image-2

## ファイル構成

```text
image_manifest.json          # 63枚の配置・種類・Alt・Caption・Prompt
scripts/generate_images.py   # API実行Script
site/images/                 # 生成画像の保存先
site/complete.html           # 全章一括ブログ
site/index.html              # 目次ページ
site/chapters/*.html         # 章別ページ
```

## 1. Setup

```bash
cd claude-code-blog-edition
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install "openai>=2.0.0"
export OPENAI_API_KEY="YOUR_API_KEY"
```

API KeyはHTML、JavaScript、Git、チャット本文へ埋め込まないでください。Build端末の環境変数またはSecret Managerから読み込みます。

## 2. まず構図だけ確認する

`core`は表紙、各部のバナー、理解に必須の補助図です。最初は`low`品質で生成し、構図とトーンを確認します。

```bash
python scripts/generate_images.py --tier core --quality low --dry-run
python scripts/generate_images.py --tier core --quality low
```

確認項目:

1. 重要情報が画像内の読めない文字に依存していない。
2. 実在製品のUIスクリーンショットに見えない。
3. 人物の役割と場面が本文に合っている。
4. 見出しをHTMLで重ねる余白がある。
5. 色・粒状感・光が他章と大きくずれていない。

## 3. 採用画像を本番品質へ上げる

```bash
python scripts/generate_images.py \
  --ids cover-main,part-00,diagram-ch06-standard-loop \
  --quality medium \
  --force
```

印刷や大きなHeroへ使う画像だけ`high`へ上げます。全63枚を最初から高品質で生成するより、`low → 選定 → medium/high`の順が安全です。

## 4. 全章の挿絵を生成する

```bash
python scripts/generate_images.py --tier chapter --quality medium
```

全Manifestを一括実行する場合:

```bash
python scripts/generate_images.py --tier all --quality medium
```

既存ファイルは自動でSkipします。再生成する場合だけ`--force`を付けます。

## 5. ReleaseでModel挙動を固定する

Aliasの`gpt-image-2`は将来改善される可能性があります。公開済み教材の絵柄を揃えたいReleaseではSnapshotを使います。

```bash
python scripts/generate_images.py \
  --tier core \
  --model gpt-image-2-2026-04-21 \
  --quality medium
```

## 6. 人物や世界観を反復編集する

物語の登場人物を複数画像で厳密に揃える場合は、最初に採用した表紙またはCharacter Sheetを入力画像として、Image APIのEditsを使います。`gpt-image-2`は入力画像を高忠実度で処理するため、参照画像を増やすと入力Costも増えます。全章へ機械的に付けず、人物の連続性が重要なHeroだけに限定してください。

概念例:

```python
from openai import OpenAI
import base64

client = OpenAI()
result = client.images.edit(
    model="gpt-image-2",
    image=open("site/images/cover-main.webp", "rb"),
    prompt="""
Keep the same four characters and editorial art direction.
Create a new landscape scene in which they review an independent quality gate.
Do not copy the original composition. No text, logos, or watermarks.
""",
    size="1536x1024",
    quality="medium",
    output_format="webp",
)

with open("site/images/chapter-13-review.webp", "wb") as f:
    f.write(base64.b64decode(result.data[0].b64_json))
```

## 7. HTMLへの差し込み

Manifestの`filename`とHTMLの`img src`は一致しています。画像を`site/images/`へ保存すれば、再Buildなしで表示されます。未生成時はCSSのPlaceholderが表示されます。

```html
<figure class="image-shell" data-image-id="chapter-04">
  <img
    src="images/chapter-04-xxxxxx.webp"
    alt="文字起こしから議事録、タスク、HTML、Skillへ展開する概念図"
    loading="lazy"
    decoding="async"
  >
  <figcaption>最初の成果物は、作る・確かめる・再利用するまでを一周できるものが最適です。</figcaption>
</figure>
```

## 8. エラー処理

`generate_images.py`は次の方針です。

- `429`と一時的な`5xx`は指数Backoffで再試行。
- `moderation_blocked`は同じPromptの自動再試行をしない。
- Request ID、Prompt Hash、Size、Quality、処理時間を`image-generation-log.jsonl`へ記録。
- 生成途中のFileは`.tmp`へ書き、完了後にAtomic Replace。
- API KeyとPrompt本文はLogへ書かない。

## 9. 編集ルール

- スクリーンショットが必要な操作説明は、画像生成ではなく実機Captureを使用する。
- 製品UIは変化するため、生成画像で偽のUIを作らない。
- Flowの日本語LabelはHTML/CSSまたはSVGで重ねる。
- 画像内に重要なCommand、API Key、File Pathを描かない。
- Altは画像の見た目ではなく、本文上の役割を説明する。
- Captionは章のTakeawayとして読める文章にする。
