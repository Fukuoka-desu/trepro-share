# Claude Code 教科書用 YouTube 文字起こし素材まとめ

作成日: 2026-06-22

## 成果物

- 完全文字起こし: `mdoutput/2026-06-22_claudecode_youtube_transcripts_complete.md`
- URL一覧: `mdoutput/2026-06-22_claudecode_youtube_urls.txt`
- 元のGemini実行結果: `mdoutput/2026-06-22_claudecode_youtube_transcripts_raw.md`
- 初回補正版: `mdoutput/2026-06-22_claudecode_youtube_transcripts_repaired.md`

## 文字起こし品質

- 対象: 10本
- 完全文字起こし収録: 10 / 10
- Gemini直接文字起こし: v04, v05, v06, v07, v09, v10
- YouTube自動字幕補完: v01, v02, v03, v08
- 注意: 自動字幕補完分は話者分離なし。固有名詞や英語コマンドの誤変換があるため、教科書本文化の前に重要語だけ確認推奨。

## 動画別メモ

### 1. 【神回！】『Claude Code』完全入門マニュアル！

- URL: https://www.youtube.com/watch?v=DkClEbyXyq4&t=233s
- チャンネル: パソコン博士TAIKI
- 長さ: 57:42
- 品質: YouTube自動字幕補完
- 主題: 初心者向けのClaude Code/AIエージェント全体像。
- 要点: AIエージェントの概念、請求書整理・ファイル整理・個人アプリ作成などの例、Claude Code/Cowork/Chatの違い、VS Code導入、プロジェクトフォルダ、許可モード、モデル選択、コンテキスト管理、CLAUDE.md、Skills、Subagents、MCP/API連携、安全ルール。

### 2. Claude Designがさらに便利に！

- URL: https://www.youtube.com/watch?v=cRTtuaL7pII
- チャンネル: KEITO【AI&WEB ch】
- 長さ: 25:07
- 品質: YouTube自動字幕補完
- 主題: Claude DesignとClaude Code連携。
- 要点: Claude DesignのWeb/デスクトップ利用、ワイヤーフレーム作成、デザインシステム、編集UI、プロトタイプ、PDFエクスポート、Claude Codeへ送信、Vercel公開、`/design-login` と `/design-sync`、ローカルのStorybook風デザインシステム同期、ブランド統一。

### 3. Claude Design が Claude Code と連携強化

- URL: https://www.youtube.com/watch?v=KhztBLfkaRw
- チャンネル: まさおAIじっくり解説ch
- 長さ: 11:21
- 品質: YouTube自動字幕補完
- 主題: Claude Designの概念整理。
- 要点: デザインシステムとプロジェクトの違い、デザインシステムを先に作りプロジェクトへ展開する流れ、Publish/Share/Export、Claude Codeへの受け渡し、Design Sync Tool、コンポーネント単位の同期、ベータ版としての使いにくさ。

### 4. Claude Codeの超基礎

- URL: https://www.youtube.com/watch?v=Y0a0zqSPtss
- チャンネル: AKIYA MOVIE
- 長さ: 18:58
- 品質: Gemini直接文字起こし
- 主題: 非エンジニア向けの最短入門。
- 要点: Claudeデスクトップアプリ、Pro/Maxプラン、Coworkで要件定義・議事録・タスク整理、Claude Codeでアプリ化、Plan/Autoなどのモード、Opusは計画・Sonnetは実装寄りに使う考え方、会議アシスタント作成デモ。

### 5. 非エンジニア向けClaude完全解説

- URL: https://www.youtube.com/watch?v=n6T4a_AKldc
- チャンネル: #usutaku_channel
- 長さ: 26:01
- 品質: Gemini直接文字起こし
- 主題: Claude全体の使い方とClaude Codeへの導線。
- 要点: Claudeは日本語が自然、Sonnetを基本モデルにする、ファイル読解、コネクタ連携、Googleカレンダー/Gmail/Slack活用、Projectsで定型指示を保存、Cowork/Codeは有料プランから、Claude Codeは便利だが初心者は危険性も理解してから使う。

### 6. Claude Code完全入門

- URL: https://www.youtube.com/watch?v=_OiMAiaG1js
- チャンネル: にゃんたのAIチャンネル
- 長さ: 56:23
- 品質: Gemini直接文字起こし
- 主題: Claude Codeの中核機能。
- 要点: AIコーディングの3世代、Claude CodeとCodex CLI比較、CLI/IDE/デスクトップ/クラウド環境、`claude`, `claude -p`, `claude --resume`, `claude --continue`, `/clear`, `/stats`、Plan Mode、音声入力、Git、`--dangerously-skip-permissions`、Sandbox、`/rewind`、CLAUDE.md、Rules、Thinking/ultrathink、Plugins、Custom commands、Agents、Hooks、Skills、MCP、画像入力、割り込み入力。

### 7. Claude Codeを自分専用に育てる

- URL: https://www.youtube.com/watch?v=2JOLh8vtJS0
- チャンネル: にゃんたのAIチャンネル
- 長さ: 17:22
- 品質: Gemini直接文字起こし
- 主題: 会話履歴を使ったパーソナライズ。
- 要点: Claude CodeのJSONL会話ログ、興味関心抽出、`INTERESTS.md`、`interest-profile` Skill、未分析ログ管理、ノイズ除外、質問深掘りスコア、時間重み、学習問題集HTML、自分専用の調査・学習体験、Routineによる定期実行。

### 8. Claude Codeで資料作成

- URL: https://www.youtube.com/watch?v=c_C4io1p3zE&t=3s
- チャンネル: にゃんたのAIチャンネル
- 長さ: 18:46
- 品質: YouTube自動字幕補完
- 主題: MarkdownよりHTMLで資料化する実践。
- 要点: HTMLは情報密度・可読性・共有性・操作性が高い、アンケートCSVからHTMLレポート作成、PowerPoint風HTMLスライド、インタラクティブなディスカッションボード、MCP/外部データ取り込み、社内ドキュメントのHTML化、トークン消費が増える注意点。

### 9. Fable 5 / Dynamic Workflows

- URL: https://www.youtube.com/watch?v=yedAfXfNXbE
- チャンネル: にゃんたのAIチャンネル
- 長さ: 28:05
- 品質: Gemini直接文字起こし
- 主題: 最新モデルとClaude Code最新機能。
- 要点: Fable 5の概要、長く複雑なタスクへの強さ、利用制限/従量課金への注意、What's New/Changelogの追い方、Dynamic Workflows、`ultracode`、`/workflows`、複数エージェントによるResearch/Verify/Synthesize、ワークフロー保存、`goal`コマンド、長時間分析タスク、コスト注意。

### 10. Claude Cowork Live Artifacts

- URL: https://www.youtube.com/watch?v=7lJyLVoIja4
- チャンネル: にゃんたのAIチャンネル
- 長さ: 21:02
- 品質: Gemini直接文字起こし
- 主題: 非エンジニア向けCowork業務自動化。
- 要点: Coworkは非エンジニア向け、フォルダを読ませて週報・議事録・タスクを作る、Project/Artifacts/Scheduled/Dispatch/Customize、Google Drive連携、Live Artifactsで最新データを読み込むダッシュボード、Artifacts内でHaikuを使った要約、Local Storageキャッシュ、`window.cowork.askClaude` によるチャット追加、Claude Designで見た目改善。

## 重複統合マップ

### 重複が多い中核テーマ

1. Claude Codeは「チャットAI」ではなく、ファイル操作・コマンド実行・修正ループまで担うAIエージェント。
2. 最初に計画を立てる。いきなり実装より、Plan Modeや要件整理を挟む方が手戻りが減る。
3. 権限と安全性が重要。Ask/Edit/Plan/Auto、Bypass、`--dangerously-skip-permissions`、Sandbox、削除禁止ルールなど。
4. コンテキスト管理が重要。新規チャット、`/clear`、`--resume`、`--continue`、CLAUDE.md、Rules、Skillsを使い分ける。
5. モデル選択は用途別。Sonnetは基本、Opus/Fableは計画・複雑タスク向け、Haikuは軽量用途。
6. Gitや`/rewind`で戻れる状態を作る。Claude Code任せにするほど履歴管理が必要。
7. MCP/API/コネクタで外部サービスとつなぐと、カレンダー・メール・Drive・Slackなど実務範囲が広がる。
8. 実際に手を動かすことが最重要。動画を見るだけではなく、エラーや試行錯誤で理解が深まる。

### 非重複で追加すべき発展テーマ

1. Claude Design連携: デザインシステム、ワイヤーフレーム、プロトタイプ、Claude Code実装、Vercel公開、Design Sync。
2. パーソナライズ: 会話ログから興味関心・学習内容を抽出し、`INTERESTS.md`や問題集にする。
3. HTML資料化: CSV分析、社内レポート、スライド風HTML、操作できるディスカッションボード。
4. Dynamic Workflows: 複数エージェントでResearch/Verify/Synthesizeを分担し、ワークフローとして保存する。
5. Cowork Live Artifacts: 非エンジニア向けに、DriveやMCPと連動する業務ダッシュボードを作る。
6. Skills/Subagents/Hooks/Custom commands: Claude Codeを「育てる」ための拡張レイヤー。

## 教科書化するときの仮章立て

1. Claude Codeとは何か: Chat/Cowork/Codeの違い、AIエージェントの概念。
2. 導入: プラン、デスクトップ、CLI、IDE/VS Code、プロジェクトフォルダ。
3. 最初の使い方: ファイルを読ませる、資料化する、簡単なアプリを作る。
4. 作業の型: Plan -> 実装 -> テスト -> 修正 -> 確認。
5. 安全設計: 許可モード、削除禁止、Sandbox、Git、Rewind。
6. コンテキスト設計: CLAUDE.md、Rules、Skills、会話の切り替え。
7. 拡張: MCP、API、コネクタ、外部サービス連携。
8. デザイン/資料: Claude Design、HTMLレポート、スライド、Artifacts。
9. 自分専用化: 会話ログ、興味関心抽出、学習問題集、Routine。
10. 高度な自律化: Dynamic Workflows、goal、複数エージェント、長時間タスク。
11. 実務ユースケース集: 議事録、週報、タスク管理、調査、営業資料、データ分析、社内ダッシュボード。
12. 運用ルール: 会社利用時の許可、情報漏えい、APIキー、コスト、品質確認。

## 次セッションへの申し送り

- このファイルは「素材整理」であり、教科書本文ではない。
- 重要語は、公式ドキュメントまたは実機で最新確認すること。動画内のモデル名・価格・制限・機能名は変わる可能性がある。
- 自動字幕補完分は誤変換が混ざるため、特にコマンド名、ファイル名、製品名は本文化前に原文確認すること。
- 最終教科書では「初心者向け導線」と「上級者向け拡張」を分けると読みやすい。
