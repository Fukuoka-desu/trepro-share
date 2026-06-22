# トレプロハーネス 要件定義書

- **作成日**: 2026-06-18
- **作成者**: 福岡（CAIO）
- **対象リポジトリ**: `github.com/tre-pro/trepro-harness`
- **ローカルパス**: `/Users/fukuokayuuki/trepro-harness/`

---

## 1. プロダクト定義

### 1.1 一言で言うと
**トレプロ全社員の Mac に「同じ Claude Code 環境」を自動配布・自動更新するための社内インフラ。**

CLAUDE.md / スラッシュコマンド / Hook / Skill / 配布スクリプトを 1 つの git リポジトリで一元管理し、Kandji（Apple MDM）または LaunchAgent から各 Mac に自動同期する。

### 1.2 位置付け（5層モデルの L1〜L2 中核）
- L1: 個人作業環境の標準化
- L2: 全社員へのスケール（30名超 / 2026-05時点）
- L3 以降（営業/MM/会計 SaaS 連携、RAG、ダッシュボード）の前提となる「土台」

### 1.3 解決する課題
| 課題 | ハーネス導入前 | 導入後 |
|---|---|---|
| ノウハウの個人滞留 | 福岡の `~/.claude/` だけが進化 | git push で全社員に同日反映 |
| Skill / Hook の品質ばらつき | 各自が独自に作る | 規範（5 prefix・4軸・Generator/Evaluator）で統制 |
| 機密事故・誤操作 | ヒューマンエラー依存 | PreToolUse Hook で物理ブロック |
| 新人キッティング | 半日〜1日 | ワンライナーで 30分以内 |
| 更新の取りこぼし | 各自手動 pull | LaunchAgent / Kandji で毎日自動 |

---

## 2. スコープ

### 2.1 含むもの（In Scope）
1. **`global-config/`** — `~/.claude/` に配布する一式
   - `CLAUDE.md`（全プロジェクト共通ルール）
   - `commands/`（13 個のスラッシュコマンド: `/plan`, `/verify-loop`, `/two-context-review`, `/fresh-review`, `/deploy`, `/hub`, `/hub-end`, `/html`, `/share`, `/codex-review`, `/investigate`, `/context`, `/youtube-report`）
   - `hooks/`（5 個: `pre-bash-guard`, `pre-edit-guard`, `post-edit-validate`, `session-end-reminder`, `session-start-client-context`）
   - `skills/`（46 個の業務スキル）
   - `hub-PROTOCOL.md`（タスク管理ハブ仕様）
   - `ref-skills/`（API リファレンス辞書）
2. **`.agents/skills/`** — Codex 用スキル群（Claude Code と相互利用）
3. **`deploy/`** — 配布インフラ
   - `install.sh`（ワンライナー初期セットアップ）
   - `bootstrap.sh` / `update.sh`（Kandji・LaunchAgent 共通エントリ）
   - `kandji/`（本番 MDM 配布手順）
   - `launchagent/`（個人 / POC 用 plist）
   - `verify.sh`（インストール検証）
4. **`sync.sh`** — `global-config/` → `~/.claude/` 同期スクリプト（manifest 方式で削除追従）
5. **`test-hooks.py`** — Hook 単体テスト

### 2.2 含まないもの（Out of Scope）
- 各社員の `settings.json` / `.env` / MCP 接続設定（個人差分）
- 顧客固有データ（`clients/`, `議事録/`, `tickets/` 等は `.gitignore`）
- 福岡個人作業ファイル（`mdoutput/`, `slide-output/`, `speaking/` 等）
- TrePro AI 本体（別リポ `trepro-ai-v4`）

---

## 3. 機能要件

### 3.1 配布機能

| ID | 要件 | 受け入れ条件 |
|---|---|---|
| F-1.1 | 新品 Mac をワンライナーで初期化 | PAT を環境変数で渡し `curl ... \| bash` 1 行で完了する |
| F-1.2 | Homebrew / Node.js / Claude Code CLI / gh / リポを自動 install | bootstrap.sh が冪等に走る |
| F-1.3 | PAT を macOS Keychain に保存し、git config / 履歴に残さない | `.git/config` に token を含まない |
| F-1.4 | 毎日 1 回自動更新 | LaunchAgent または Kandji 経由で `update.sh` 実行 |
| F-1.5 | 同時実行を防止 | `mkdir` ロックで競合排除（30 分超でstale判定）|

### 3.2 同期機能

| ID | 要件 | 受け入れ条件 |
|---|---|---|
| F-2.1 | `global-config/` を `~/.claude/` にコピー | sync.sh 実行で 7 ステップ完了 |
| F-2.2 | 削除追従（収束的同期） | 前回 manifest にあって今回ない物は削除 |
| F-2.3 | 個人カスタマイズ層 `~/.claude/local/` を保護 | sync.sh が一切触らない |
| F-2.4 | CLAUDE.md は `.bak` で 1 世代バックアップ | 上書き前に自動保存 |
| F-2.5 | `--dry-run` で差分プレビュー | 実ファイル変更なしで動作確認可能 |
| F-2.6 | `.agents/skills/` も同期、`global-config/skills/` が優先 | 同名スキルは Claude Code 版で上書き |

### 3.3 品質ガード（Hook）

| ID | 要件 | 実装 |
|---|---|---|
| F-3.1 | 危険な DB 操作のブロック | `pre-bash-guard.sh`（`trepro-ai-db` 等の誤名検出） |
| F-3.2 | JST 計算の誤りブロック | `pre-bash-guard.sh`（`Intl.DateTimeFormat` 強制） |
| F-3.3 | テスト・lint 設定の改変ブロック | `pre-edit-guard.sh`（deny リスト） |
| F-3.4 | Edit/Write 後の TypeScript 型チェック自動実行 | `post-edit-validate.sh` |
| F-3.5 | セッション終了時に `/hub-end` リマインド | `session-end-reminder.sh` |
| F-3.6 | プロジェクト起動時に顧客コンテキスト注入 | `session-start-client-context.sh` |

### 3.4 スキル運用

| ID | 要件 | 受け入れ条件 |
|---|---|---|
| F-4.1 | 5 prefix 命名規約に準拠（S_, mm-, sm-, project-, feedback-）| `assign-skill-review-evaluator` で 85 点以上 |
| F-4.2 | Generator / Evaluator のメタスキル分離 | `assign-skill-review-generator` 経由で新規作成 |
| F-4.3 | Progressive Disclosure（SKILL.md → references/）| 1 ファイル 200 行以内 |
| F-4.4 | 4 軸評価（明確性・実用性・保守性・整合性）| 評価器で全軸通過必須 |
| F-4.5 | Codex と Claude Code 両方に配置 | 新規スキルは `~/.claude/skills` と `~/.codex/skills` 両方へ |

### 3.5 安全装置

| ID | 要件 | 実装 |
|---|---|---|
| F-5.1 | 50 ファイル以上削除には destructive-flag 必須 | `safety-rails` スキル |
| F-5.2 | background プロセス 20 分タイムアウト | `safety-rails` スキル |
| F-5.3 | Cloud Run cron ±5 分デプロイブロック | `safety-rails` スキル |
| F-5.4 | Codex 重複指示ブロック | `safety-rails` スキル |

---

## 4. 非機能要件

| 区分 | 要件 |
|---|---|
| 信頼性 | 冪等性（bootstrap / update / sync を何度走らせても破壊しない） |
| 信頼性 | ネット疎通失敗時は skip（次回回復） |
| 観測性 | 全ログを `~/Library/Logs/trepro-harness/` に集約、1MB でローテーション |
| 観測性 | `verify.sh` でインストール後の動作検証 |
| 保守性 | `lib/common.sh` に共通関数を集約（ログ・ロック・疎通） |
| 保守性 | Kandji と LaunchAgent で同じ bootstrap/update を再利用 |
| セキュリティ | PAT は Keychain 保存のみ、リポに含めない |
| セキュリティ | 顧客固有データは `.gitignore` で除外 |
| セキュリティ | 個人作業 465 ファイル除外整理済（2026-05-04） |
| 拡張性 | 環境変数で `HARNESS_REPO_URL` 等を上書き可能 |
| 互換性 | macOS 専用（darwin 24+, Apple Silicon / Intel 両対応） |

---

## 5. 配布対象ポリシー

### 5.1 配布する
- 全社共通の CLAUDE.md / コマンド / Hook
- 業務スキル（営業・MM・会計・分析・スライド生成系）
- API リファレンス辞書

### 5.2 配布しない
- `tickets/`, `clients/`, `議事録/` 等のローカル属人ディレクトリ
- `~/.claude/local/`（個人カスタマイズ層）
- `~/.claude/settings.local.json`
- `global-config/skills/` 配下で `.gitignore` ホワイトリスト外（社内専用スキル）

---

## 6. ユーザー / 利用シナリオ

### 6.1 ユーザー区分
| 区分 | 人数 | 利用形態 |
|---|---|---|
| 管理者（福岡） | 1 名 | 編集・push・配布判断 |
| 開発者社員 | 数名 | sync.sh 手動運用 + ローカル PR |
| 一般社員 | 30 名超 | Kandji / LaunchAgent で自動受信のみ |

### 6.2 主要シナリオ
1. **新人キッティング**: PAT を渡す → ワンライナー実行 → ブラウザ認証 2 回（Claude / gh） → 30 分で稼働開始
2. **スキル追加配信**: 福岡が `git push` → 翌朝までに全社員の Mac に反映
3. **障害対応**: `~/Library/Logs/trepro-harness/update.log` 確認 → 該当 Mac で `update.sh` 手動再実行
4. **個人カスタマイズ**: 各自 `~/.claude/local/` に独自 commands / skills を置く → MDM 配布の影響を受けない

---

## 7. 制約条件

- **OS**: macOS 専用（Linux / Windows は非対応）
- **リポジトリ**: Private（PAT 必須）
- **MDM**: Kandji 想定（他 MDM への移植性は維持するが未検証）
- **Claude Code バージョン**: Opus 4.7（1M context）想定、4.6 以前との互換は試験中
- **TS 型チェック**: 各プロジェクトに `tsconfig.json` がある前提

---

## 8. 成功指標（KPI）

| 指標 | 目標 |
|---|---|
| 新人キッティング所要時間 | 30 分以内 |
| 全社員への新スキル反映時間 | push から 24 時間以内 |
| Hook によるブロック実績 | 月 1 件以上（誤操作防止が機能） |
| `/review-harness` 月初診断 | 月 1 回必ず実行、スコア 80+ 維持 |
| ハーネス起因の業務停止 | 0 件 / 月 |

---

## 9. 既知の課題・宿題

- `~/.claude/CLAUDE.md` への個人差し込み機構が未提供（現状 MDM 完全管理）
- Codex 側との skill 同期は手動 cp（自動化未済）
- Kandji 契約待ち（現状 LaunchAgent POC で代用中）
- `settings.json` は個人セッション差があり `--settings` フラグ任意（デフォルト非配布）

---

## 10. 参照

- `/Users/fukuokayuuki/trepro-harness/CLAUDE.md` — プロジェクト指示
- `/Users/fukuokayuuki/trepro-harness/deploy/README.md` — 配布インフラ詳細
- `/Users/fukuokayuuki/trepro-harness/deploy/POC_NEW_MAC.md` — 新品 Mac キッティング手順
- `/Users/fukuokayuuki/trepro-harness/deploy/kandji/README.md` — Kandji 配布手順
- `/Users/fukuokayuuki/trepro-harness/sync.sh` — 同期スクリプト本体
- `/Users/fukuokayuuki/trepro-harness/global-config/CLAUDE.md` — 配布される全社共通ルール
- `/Users/fukuokayuuki/trepro-harness/前提_Claude.md` — 会社前提・組織構造
