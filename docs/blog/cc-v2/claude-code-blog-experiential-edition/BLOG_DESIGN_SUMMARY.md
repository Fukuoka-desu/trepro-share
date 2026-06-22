# ブログ版の最適構成サマリー

## 結論

最適なのは、教科書の内容を薄い読み物へ要約することではなく、**物語層と実装層を同じ章に重ねる構成**です。

```text
物語の現在地
  読者が「なぜ必要か」を理解する
        ↓
意味の解説
  概念同士の関係を会話調でつかむ
        ↓
実装リファレンス
  Command、File、Code、検証条件を省略せず確認する
        ↓
体験ミッション
  Cursor / Claude Code / Codex上で一操作する
        ↓
Takeaway
  次章へ持ち越す原則を一文で固定する
```

この二層構造にすると、初心者は物語から入れ、実装者はCodeへ直接移動でき、管理者は後半のPolicyとHarnessだけを参照できます。

## Story Arc

主人公は、既存Skillを使えるが内部を説明できない非エンジニアの遥です。開発者の蓮が再現性とGitを、AI推進・情シスの美咲が安全と全社配布を、ナビゲーターが次の一操作と証拠を担当します。

1. 使えるが直せない状態から始まる。
2. 会議アシスタントを0から完成させる。
3. 成功を標準Loopへ変える。
4. 知見をCLAUDE.md、Rules、Skills、Agents、Hooksへ分ける。
5. HTML、Design、Artifacts、MCPへ広げる。
6. パーソナライズと自律化に停止条件を入れる。
7. 個人の成功をトレプロハーネスで全社員へ配る。
8. 教材自体を保存・再開可能な学習Applicationへする。

## 画像の役割

画像は三種類に限定します。

- **Editorial Illustration**: 章の感情・状況・人物関係を伝える。
- **Concept Diagram**: Layer、Loop、Trust Boundary、Release Flowを俯瞰する。
- **Product Concept**: 将来の学習ApplicationやDashboardの体験を示す。

製品の操作画面は変化しやすいため、画像生成で偽Screenshotを作りません。操作説明には実機Capture、Concept説明には生成画像を使います。重要な日本語Label、Command、数値はHTMLで重ね、生成画像だけに情報を閉じ込めません。

## HTMLの役割

- 章別Pageと全章一括Pageを用意。
- Sticky目次、Reading Progress、Code Copy、Print CSSを実装。
- 画像未生成時はPlaceholderを表示。
- 各画像のPrompt、種類、配置を折りたたみで確認可能。
- AltとCaptionだけでも画像の意味が伝わる。
- 将来はLesson JSONと進捗Stateへ分離できる構造。

## 収録結果

- 全40章（第0〜38章 + 終章）
- 元小見出し285件を保持
- 元Code Fenceを全保持
- 全章にStory、Mission、Takeaway
- 63件の画像Brief
- GPT Image 2 API実行Script
- 章別40Page、Index、全章一括、画像Pipelineの計43 HTML
