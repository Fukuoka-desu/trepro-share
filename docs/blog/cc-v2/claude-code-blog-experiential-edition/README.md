# Claude Code実践教科書 - スライド×ブログ×章番号ハンズオン統合版

この版は、次の三つを一つの学習体験へ統合しています。

1. ストーリー形式の長文ブログ
2. アップロードされたスライドPDF全147ページ
3. Cursor・Claude Code・Codexで章番号から起動する共通Skill

## まず開くファイル

- `index.html` - パッケージ入口
- `site/complete.html` - 全40章・147枚・ハンズオン起動欄を含む一括HTML
- `site/hands-on.html` - 章番号から実習を選ぶ一覧
- `claude-code-blog-slide-integrated.md` - 画像参照付きMarkdown完全版

ローカルサーバーで開く場合:

```bash
cd site
python3 -m http.server 8000
```

ブラウザで `http://localhost:8000/` を開きます。

## スライドの配置

PDFの各ページを一律に章末へ並べず、内容で分類しました。

- オレンジ背景の章扉: 章タイトル直後
- 概念図: 対応する小見出しの最初の説明直後
- 手順図: 実装手順・Template・Workflowの説明箇所
- 注意図: 安全、削除、公開、秘密情報、失敗Patternの該当箇所

画像は `assets/slides/slide-001.webp` 〜 `slide-147.webp` です。ブログ向けに1920×1072 WebPへ変換し、クリックで原寸表示できます。配置の正本は `slide_integration_manifest.json`、人向け一覧は `SLIDE_PLACEMENT_MAP.md` です。

## 章番号ハンズオン

パッケージには次の三つのProject Skill配置を同梱しています。

```text
.cursor/skills/textbook-chapter-lab/
.claude/skills/textbook-chapter-lab/
.agents/skills/textbook-chapter-lab/
```

展開したフォルダをCursor、Claude Code、Codexで開いた後、章番号を伝えます。

```text
第12章を開始
```

Runtime別の明示呼び出し:

```text
Cursor:      第12章を開始
Claude Code: /textbook-chapter-lab 12
Codex:       $textbook-chapter-lab 第12章を開始
```

全40章が4 Step、合計160 StepのLabに対応します。進捗の正本は次です。

```text
.trepro-learning/
├── textbook-state.json
├── RESUME.md
└── checkpoints/
```

「保存」でCheckpointを作り、「再開」で現在の章・Step・次の操作を復元します。Runtimeを切り替える場合も同じStateを使います。

## 別ProjectへSkillを導入

Project単位:

```bash
./hands-on/install.sh \
  --runtime all \
  --scope project \
  --target /path/to/project
```

個人の全Projectへ導入:

```bash
./hands-on/install.sh --runtime all --scope user
```

対象確認だけなら `--dry-run` を付けます。

## 安全設計

- 実習は章専用の `learning-lab/` 以下だけ
- Secret、顧客データ、本番DBを使わない
- 外部送信、公開、課金、Git push、Bypass、破壊的削除を行わない
- 第15章はMock接続、第31章はPreviewまで
- 管理者向け章もFixtureとDry-runを既定にする
- 「できた」という自己申告だけで完了にせず、File・Review・回答などのEvidenceを確認する

## 構造化データ

- `beginner_supplements.json` - 全40章の初心者補足と実習Metadata
- `slide_integration_manifest.json` - 147画像の配置、Target、Hash
- `hands-on/skill/textbook-chapter-lab/course/chapter-index.json` - 章一覧
- `hands-on/skill/textbook-chapter-lab/course/chapters/` - 40章のLesson JSON
- `CHAPTER_HANDS_ON_MAP.md` - 人向けの章・成果物対応表

## 検証

```bash
python3 scripts/validate_experiential_edition.py
./trepro-textbook validate-course --json
```

検証対象は、PDFページ数、画像ファイル、配置の一意性と章一致、HTML/Markdown、全40章の初心者補足、全40章の起動欄、160 Step、保存・再開、順不同拒否、Secretマスキング、Installerです。
