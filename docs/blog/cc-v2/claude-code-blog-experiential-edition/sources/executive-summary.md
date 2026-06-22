# Claude Code最強教科書 — エグゼクティブサマリー

- **基準日**: 2026-06-22
- **対象**: トレプロの全社員、AI推進、開発、情シス、管理者
- **詳細本文**: `2026-06-22_claude-code_ultimate_textbook_v1.md`

## 結論

最適な教科書は、Claude Codeの機能を順番に説明する百科事典ではありません。次を一体化した**実行型の組織OS**です。

1. **最短実習** — 60〜90分で会議アシスタントを完成させる。
2. **標準作業ループ** — `Explore → Specify → Plan → Implement → Verify → Review → Commit`。
3. **責務分離** — CLAUDE.md、Rules、Skills、Subagents、Hooks、MCPを混同しない。
4. **実務レシピ** — 議事録、週報、調査、HTML、Design、Artifacts、アプリを再現する。
5. **全社ハーネス** — 配布、強制Policy、Skill評価、Canary、Rollback、監査を含める。
6. **アプリ化前提** — Lessonを構造化Dataとして持ち、進捗、実行Check、Version差分を管理する。

## 読者別の最短導線

### 非エンジニア

全体像、安全、Project Folder、会議アシスタント、Cowork、HTML、実務レシピの順で学びます。最初からCLIの全機能を暗記させません。

### 開発者

標準ループ、Permission/Sandbox、Git/Context、Skills、Subagents、Hooks、MCP、自律化へ進みます。

### 管理者

Managed Settings、Managed MCP、Skill Governance、Kandji配布、Telemetry、Incident、Rollbackを中心に学びます。

## 教材の中心原則

```text
目的を定義する
  ↓
現状を読む
  ↓
計画を作る
  ↓
小さく実装する
  ↓
証拠で検証する
  ↓
別文脈でレビューする
  ↓
良い状態を保存する
  ↓
再利用価値をSkill/Rule/Hookへ昇格する
```

## 重要な責務分離

| 内容 | 置き場所 |
|---|---|
| Projectの概要、Command、常設方針 | CLAUDE.md |
| Path別の開発Rule | `.claude/rules/` |
| 繰り返す業務手順 | Skill |
| 独立した専門家 | Subagent |
| 必ず実行・拒否する制御 | Hook / Permission |
| 外部System | MCP / Connector |
| 組織で外せない安全Policy | Managed Settings |
| Claudeが発見した短い知識 | Auto Memory |

CLAUDE.mdは強制力のあるFirewallではありません。秘密Read禁止、Bypass禁止、Deploy承認はManaged Settings、Sandbox、Hookで実装します。

## 素材から補正した重要事項

| 動画内の説明 | 現行の扱い |
|---|---|
| Fable 5を積極利用 | 2026-06-12からアクセス停止中。標準手順は依存させない |
| Dynamic WorkflowsはMax限定 | 現行は有料プラン対象。最低Versionと設定を確認 |
| Custom CommandsとSkillsは別 | 新規資産はSkillsへ統合 |
| Skill名は日本語や任意文字でよい | Claude/Codex共通正本は小文字英数字とHyphen |
| `/design-login` が入口 | 現行の公式入口として `/design`、`/design-sync` を確認 |
| Context 40%が固定性能低下点 | 固定閾値にしない。`/context`と成果品質で判断 |
| Bypassは効率化に便利 | 使い捨て隔離環境のみ。全社Macでは禁止推奨 |

## トレプロハーネスへの主要提案

### 1. Managed Policyを正式なIn Scopeにする

`~/.claude/CLAUDE.md`の配布だけでは安全を強制できません。Kandjiから次を配布します。

```text
/Library/Application Support/ClaudeCode/CLAUDE.md
/Library/Application Support/ClaudeCode/managed-settings.json
/Library/Application Support/ClaudeCode/managed-mcp.json
```

### 2. Skillの正本を1か所にする

`skill-src/`を正本とし、`global-config/skills/`と`.agents/skills/`はBuild生成物にします。Claude用とCodex用を手動で二重編集しません。

### 3. 5 Prefixの互換移行

`S_`はCanonical Nameの制約と衝突します。例として`S_customer-research`を`s-customer-research`へ移し、Legacy名とCategoryをMetadataへ保持します。

### 4. 即時全社配布をやめる

```text
PR → Test/Evaluator → Canary → Pilot → Stable → 全社員
```

署名Tag、Version Inventory、1 Command Rollbackを持ちます。

### 5. Block件数だけで安全を測らない

Hook Block件数に加え、誤検知率、Update成功率、Skill失敗率、Incident、1成果物Costを測ります。

## 最初に作る教材

1. 安全なLabの準備。
2. Meeting Assistantの要件定義。
3. Plan Modeで実装計画。
4. Markdown/JSON/HTMLを生成。
5. JSON SchemaとTestで検証。
6. Git diffと`/rewind`。
7. 成功手順をSkill化。
8. Fresh Reviewerで評価。

これをBronze認定の標準実習にします。

## 教科書アプリの最適形

PDF Viewerではなく、次を持つLearning Systemにします。

- Role別Learning Path。
- `seen / practiced / verified / applied` の4段階進捗。
- Copy可能なPromptとCode。
- Command Exit CodeやArtifactによるCheck。
- Feature RegistryによるBeta・Suspended・Version差分。
- Skill Catalogと評価Score。
- Harness Version/Update Status。
- Admin向けTopic Coverage Dashboard。

ブラウザから任意Shellを直接実行せず、将来はAllowlist付きLocal Companion CLIと連携します。

## 30日導入案

### Week 1

Skill Inventory、命名移行表、Managed Settings Canary、Release Policy。

### Week 2

`skill-src/`正本化、Build/Validator、Hook Fixture、sync/verify/Rollback Test。

### Week 3

管理者・開発者Canary、Bronze研修、Meeting Assistant、誤検知とSandbox例外の観測。

### Week 4

Pilot部署、Incident/Help Desk、Version Dashboard、Stable Release、全社員研修。

## 30日後の成功条件

```text
[ ] 新人が30分以内に導入
[ ] Bronze実習を自力完了
[ ] Stable端末95%以上が24時間以内に更新
[ ] CanaryからStableへの昇格記録
[ ] Rollback Drill成功
[ ] Skill正本の二重編集0
[ ] Critical Security Gap 0
[ ] 全素材Topic Coverage 100%
```
