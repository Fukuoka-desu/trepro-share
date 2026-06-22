# Claude Code 教科書 — 素材Coverage・現行仕様検証表

- **基準日**: 2026-06-22
- **対象素材**: YouTube 10本の完全文字起こし・要点集、トレプロハーネス要件定義書
- **目的**: 素材の全Topicが教科書へ配置され、重複が統合され、変動仕様が補正されていることを確認する

## 判定記号

- **本文**: 原則または標準手順として本文へ統合
- **Recipe**: 具体例として実務ユースケースへ配置
- **Registry**: 変動情報としてFeature Registry管理
- **注意**: 高Risk・Beta・未検証として条件付き記載
- **補正**: 撮影時点から現行仕様へ変更

---

# 1. 動画v01「Claude Code完全入門」

| 元Topic | 配置 | 処理 |
|---|---|---|
| AI Agentの定義 | 第1章 | 本文へ統合 |
| 質問回答だけでなくPC上で作業 | 第1章 | Agent loopとして統合 |
| 請求書をExcel化 | 第28章 | CSV化・経理Review付きRecipe |
| Backup FolderのFile整理 | 第28章 | Dry-run/Manifest/Quarantineへ安全補正 |
| 世界情勢Dashboard | 第30章 | 発展Recipe、Freshness/Sourceを追加 |
| Diet App | 第30章 | 医療Riskを明示したPrototype扱い |
| 株取引支援App | 第30章 | 投資Risk、Bias、Kill Switchを追加 |
| YouTubeネタResearch | 第29章 | Channel Profileと公式検証を追加 |
| AI Agentを育てる | 第1、11〜14章 | Memory/Skill/Rule/Hookへ責務分離 |
| 複数Agentを会社組織化 | 第13、21章 | Subagent/Workflowへ統合 |
| 他社Agentとの比較 | 第1章 | Tool固有評価ではなくAgent概念へ統合 |
| 料金/Plan | Feature Registry | 変動情報として本文から分離 |
| Chat/Cowork/Codeの差 | 第1章 | Designも加えた4面比較 |
| VS Code導入 | 第3章 | 公式Extension確認を追加 |
| Project Folder | 第3章 | 相関あり/なしのFolder設計へ統合 |
| Ask/Edit/Plan/Auto/Bypass | 第7章 | 現行Permission Modeへ補正 |
| Effort | 第8章 | Cost/時間/品質のTrade-off |
| Model選択 | 第8章 | Model名ではなく役割で整理 |
| Slash Commands | 第3、9章 | 代表Command + `/help`優先 |
| `/context` | 第9章 | 固定40%閾値を採用しない |
| `/compact` | 第9章 | 同じ目的の履歴圧縮 |
| 作業別Session | 第9章 | Topic境界で分離 |
| CLI版 | 第3章 | Native Install/CLI基本へ統合 |
| CLAUDE.md | 第11章 | Guidanceであり強制ではないと補正 |
| Global/Project CLAUDE.md | 第11、23章 | Managed Policyを追加 |
| File削除禁止Rule | 第2、7、14、26章 | Permission/Hookで強制 |
| Skills | 第12、25章 | Agent Skills標準へ補正 |
| Global/Project Skill | 第12、23章 | ScopeとCanonical Sourceへ整理 |
| Subagents | 第13章 | Role/Tool/Context分離 |
| SkillをSubagentでReview | 第13、25章 | Fresh Evaluatorへ標準化 |
| MCP | 第15、26章 | Scope/Allowlist/Injectionを追加 |
| Gmail/Calendar/Drive | 第15、18、32章 | Read→Draft→Human Gateへ整理 |
| API連携 | 第15章 | Secret管理と直接APIの責務を追加 |
| API KeyをChatへ貼らない | 第7、15章 | Keychain/Secret Managerへ具体化 |
| Codespacesで隔離 | 第2、7章 | Container/VM/Sandbox選択肢へ統合 |
| 実際に手を動かす | 第4、27、35章 | 成果物Check型の学習へ変更 |

---

# 2. 動画v02「Claude Designがさらに便利に」

| 元Topic | 配置 | 処理 |
|---|---|---|
| Web/DesktopのDesign | 第17章 | Surface差ではなく役割中心 |
| Wireframe | 第17、31章 | 情報設計を先に分離 |
| Design System選択 | 第17章 | Token/Component構造へ具体化 |
| Clarifying questions | 第5、17章 | 実装前質問の標準へ統合 |
| Edit UI | 第17章 | 視覚調整として記載 |
| Text/Position/Delete | 第17章 | Beta UIのため概念中心 |
| Layer/Gradient/Font | 第17章 | Design SystemのComponent/Tokenへ統合 |
| PDF Export | 第16、31章 | Export後QAを追加 |
| Mobile版 | 第17章 | Responsive Acceptanceへ統合 |
| Clickable Prototype | 第17章 | State/Transition検証を追加 |
| Variable表現 | 第17章 | DesignとData Bindingの境界として整理 |
| Claude Codeへ送信 | 第17章 | Plan/対応表/Testを挟む |
| Wix/Canva/Adobe等 | 第31章 | 変動連携のため一般化 |
| Vercel Deploy | 第31章 | Preview→Approval→Productionへ補正 |
| `/design-login` | 第37章 | 現行公式入口として未採用 |
| `/design-sync` | 第17章 | 公式現行Commandとして記載 |
| Storybook風System | 第17章 | Local Design System構造へ統合 |
| Brand統一 | 第17、31章 | Token正本と再利用へ整理 |
| Syncの難しさ | 第17章 | 正本、Diff、Git Checkpointを追加 |

---

# 3. 動画v03「Claude Design連携強化」

| 元Topic | 配置 | 処理 |
|---|---|---|
| Design SystemとProjectの違い | 第17章 | 表で明確化 |
| Systemを先に作る | 第17章 | 標準Flowへ採用 |
| Brand/営業資料Theme | 第17、31章 | 共通Token活用 |
| Publish | 第17章 | Beta UI名はRegistry扱い |
| Share/HTML/PPT/PDF | 第16、31章 | 出力形式の選択基準へ統合 |
| Claude Code CLI/Webへ渡す | 第17章 | 実装計画を挟む |
| Project Archive/ZIP | 第17章 | Source/生成物の正本整理 |
| Existing React Component同期 | 第17章 | Component単位のSyncへ統合 |
| Design Sync Tool | 第17章 | `/design-sync`で現行確認 |
| Component単位同期 | 第17章 | 正本/差分運用を追加 |
| Betaの使いにくさ | 第17、37章 | Status表示とFallbackを追加 |

---

# 4. 動画v04「Claude Code超基礎」

| 元Topic | 配置 | 処理 |
|---|---|---|
| 非Engineerの最短入門 | 第0、4章 | Meeting Assistant実習 |
| Desktop App | 第1、18章 | Surface選択へ統合 |
| Pro/Max | Registry | 変動情報 |
| Chatで要件定義 | 第4、5章 | Requirements Templateへ具体化 |
| Coworkで議事録 | 第4、18、28章 | 実務Flowへ統合 |
| CodeでApp化 | 第4、30章 | 外部APIなしの安全な初版 |
| Meeting Assistant | 第4、28章 | Schema/Test/Source Quoteを追加 |
| Project File | 第3、18章 | Project FolderとCowork Projectを区別 |
| Skill化 | 第12、25章 | Fixture/Evaluatorを追加 |
| Plan Mode | 第6、7章 | 標準Loopへ統合 |
| Auto Mode | 第7章 | 現行条件を確認 |
| Opus計画/Sonnet実装 | 第8章 | 固有名でなく役割分担へ一般化 |
| Node.js導入 | 第3、24章 | Bootstrap/Toolchain管理 |
| `/btw` | Command Registry | 変動Commandとして扱う |
| `/compact` | 第9章 | Context整理 |
| `/init` | 第11章 | 生成後Reviewを追加 |

---

# 5. 動画v05「非Engineer向けClaude完全解説」

| 元Topic | 配置 | 処理 |
|---|---|---|
| 日本語の自然さ | 第1章 | Product選択の一観点として簡潔化 |
| Coding性能 | 第1、30章 | 非EngineerでもPrototype可能 |
| Prompt呪文不要 | 第5章 | 仕事定義が重要と統合 |
| Chatの新規会話 | 第9章 | Session境界へ統合 |
| File/PDF読解 | 第28章 | 契約書は法務Review付き |
| Sonnetを基本 | 第8章 | 標準Modelの考え方へ一般化 |
| Calendar Connector | 第15、32章 | Read-onlyから開始 |
| Gmail検索 | 第15、32章 | Draftまで |
| Slack/Notion | 第15章 | Connector/MCPへ統合 |
| 会社の許可 | 第2、15、26章 | Managed Policy/データ統制を追加 |
| Projectsで定型指示 | 第11、18章 | CLAUDE.md/Skill/Project責務へ分解 |
| Cowork Scheduled | 第18、20章 | 冪等/Lock/Retryを追加 |
| Claude Codeは初心者に危険 | 第2、7章 | 段階的権限付与へ標準化 |
| 実際に使う | 第4、27、35章 | Hands-on/verified進捗 |

---

# 6. 動画v06「Claude Code完全入門」

| 元Topic | 配置 | 処理 |
|---|---|---|
| AI Coding 3世代 | 第1章 | 表へ統合 |
| Claude Code/Codex比較 | 第1、12、25章 | Tool選択より共通Skill標準を重視 |
| CLI/IDE/Desktop/Web | 第1、3章 | Surface別役割 |
| Native Install | 第3、24章 | 公式推奨へ補正 |
| `claude` | 第3章 | 基本Command |
| `claude -p` | 第3、20章 | Headlessと安全条件 |
| `--resume/--continue` | 第3、9章 | File状態再確認を追加 |
| `/clear` | 第9章 | Topic分離 |
| `/stats` | 第3章 | Registry/現行Help |
| Plan Mode | 第6、7章 | 標準Loop |
| 音声入力 | 第19章 | 復唱と誤変換対策 |
| Git | 第10章 | Checkpointとの併用 |
| `--dangerously-skip-permissions` | 第7、26章 | 全社禁止推奨 |
| Docker隔離 | 第2、7章 | 使い捨て環境条件 |
| Sandbox | 第7、26章 | Managed強制例 |
| `/rewind` | 第10章 | Gitの代替ではない |
| CLAUDE.md | 第11章 | Scope/短文化 |
| Rules | 第11章 | Path別Rule |
| Thinking/ultrathink | 第8章 | 制約と比較軸を追加 |
| Plugins | 第14、26章 | Supply Chain統制 |
| Custom Commands | 第12、37章 | Skills統合へ補正 |
| Agents | 第13章 | Role/Tool制限 |
| Hooks | 第14、26章 | Deterministic Control |
| Skills | 第12、25章 | Lifecycle/Test/Build |
| MCP | 第15、26章 | Allowlist/Managed MCP |
| 画像Input | 第9、19章 | Secret Mask |
| 割り込みInput | 第9、19章 | 緊急停止との違い |
| Frontend Design Skill | 第12、17章 | Design Systemへ統合 |

---

# 7. 動画v07「Claude Codeを自分専用に育てる」

| 元Topic | 配置 | 処理 |
|---|---|---|
| JSONL会話Log | 第19章 | Schema変化とPrivacyを追加 |
| 興味関心抽出 | 第19章 | Opt-in/Review可能にする |
| `INTERESTS.md` | 第19章 | 15 Topic上限・Change Log |
| `interest-profile` Skill | 第19章 | 実装Template |
| 未分析Log管理 | 第19章 | state.jsonのIncremental処理 |
| Noise除外 | 第19章 | Greeting/Command/Paste除外 |
| 深掘りScore | 第19章 | Frequency/Depth/Explicit |
| 時間重み | 第19章 | Half-life式 |
| 自分向け調査 | 第19、29章 | Primary-source Researchと接続 |
| 学習問題HTML | 第19、29章 | Retrieval Practiceへ拡張 |
| Routine定期実行 | 第20章 | Scheduled/LaunchAgentへ一般化 |
| 会話LogのPrivacy | 第19、26章 | 過収集/人事利用禁止を追加 |

---

# 8. 動画v08「MarkdownよりHTML」

| 元Topic | 配置 | 処理 |
|---|---|---|
| Markdown/HTMLの違い | 第16章 | 正本/Viewの分離 |
| 情報密度 | 第16章 | KPI/Graph/Table標準 |
| 可読性 | 第16章 | Mobile/A11y/Print |
| 共有性 | 第16章 | 機密と公開範囲を追加 |
| 双方向操作 | 第16章 | Discussion Board |
| MCP Data取込 | 第15、16、18章 | Source/Freshnessへ統合 |
| CSV分析Report | 第16章 | Prompt/QA付き |
| PPT風HTML Slide | 第16、31章 | Story構成とExport QA |
| Drag&Drop Board | 第16章 | Local Storage安全を追加 |
| 社内文書HTML化 | 第16章 | Markdown/JSON正本を維持 |
| Code Review HTML | 第16章 | Report用途へ包含 |
| Design Prototype | 第17章 | Design Flowへ統合 |
| Token消費 | 第16、21章 | Cost Controlへ追加 |

---

# 9. 動画v09「Fable 5 / Dynamic Workflows」

| 元Topic | 配置 | 処理 |
|---|---|---|
| Fable 5 | 第8、37章 | 2026-06-12停止へ補正 |
| 長時間複雑Task | 第20、21章 | Goal/Workflow設計 |
| Cost/従量課金 | 第8、21、26章 | Registry/予算/停止条件 |
| What's New/Changelog | 第22、37章 | 更新Source優先 |
| Dynamic Workflows | 第21章 | 現行Plan条件へ補正 |
| `ultracode` | 第21章 | Workflow入口 |
| `/workflows` | 第21章 | 進行確認 |
| Research/Verify/Synthesize | 第21、22章 | 標準Workflow |
| Workflow保存 | 第21章 | 再利用とVersion管理 |
| Manual Workflow | 第21章 | Cost制御の代替 |
| Advisor | 第8章 | 標準+難所高性能 |
| Agent View | 第13、21章 | Worktree/編集範囲を追加 |
| `goal` | 第14、20章 | Verifier/Budget/Stopを追加 |
| 長時間分析 | 第20、30章 | 最大Turn/再現性を追加 |

---

# 10. 動画v10「Cowork Live Artifacts」

| 元Topic | 配置 | 処理 |
|---|---|---|
| Coworkは非Engineer向け | 第1、18章 | Code移行条件も追加 |
| Folderを読む | 第18、28章 | Project Contextへ統合 |
| 週報/議事録/Task | 第18、28、32章 | Human Review付きPipeline |
| Project | 第18章 | Folder/Instruction/Asset |
| Artifacts | 第18章 | Persistent View |
| Scheduled | 第18、20章 | Lock/Retry/Timezone |
| Dispatch | 第18章 | 役割のみ、UI変動扱い |
| Customize | 第18章 | Skill/Connector |
| Drive連携 | 第18章 | Source/Fetch/Transform/Cache/View |
| Live Data Refresh | 第18章 | Hash/部分更新/失敗State |
| Haiku要約 | 第18章 | Model Class一般化、原文区別 |
| Local Storage Cache | 第18章 | Secret/原文非保存 |
| `window.cowork.askClaude` | 第18章 | Beta APIとして現行Help優先 |
| Claude Design改善 | 第17、18章 | View改善Flow |

---

# 11. トレプロハーネス要件Coverage

| ID | 要件 | 教科書 | 実装補足 |
|---|---|---|---|
| F-1.1 | ワンライナー初期化 | 第24、27章 | 内部URL/署名検証を追加 |
| F-1.2 | Brew/Node/Claude/gh/Repo | 第24章 | 冪等Bootstrap |
| F-1.3 | PAT Keychain、安全なGit | 第24章 | Fine-grained/短期限/将来SSO |
| F-1.4 | 毎日更新 | 第20、24章 | Lock/Retry/Channel |
| F-1.5 | 同時実行防止 | 第24章 | mkdir Lock/Stale 30分 |
| F-2.1 | global-config同期 | 第24章 | Manifest所有範囲 |
| F-2.2 | 削除追従 | 第24章 | Previous-Current |
| F-2.3 | local保護 | 第23、24章 | 自動発見/Overlay仕様を明文化 |
| F-2.4 | CLAUDE.md backup | 第24章 | 1世代Backup |
| F-2.5 | dry-run | 第24章 | 実変更なし |
| F-2.6 | Codex/Claude Skill merge | 第24、25章 | 長期はCanonical Build |
| F-3.1 | DB誤操作Block | 第14、26章 | Rule ID/Telemetry |
| F-3.2 | JST誤りBlock | 第14、25章 | Hook Fixtureへ追加対象 |
| F-3.3 | Test/Lint改変Block | 第14、26章 | PreEdit/Managed Ask |
| F-3.4 | TS Typecheck | 第14章 | Debounce/Timeout |
| F-3.5 | Session End Reminder | 第14章 | Stop/SessionEnd責務 |
| F-3.6 | 顧客Context | 第14章 | 公開Runbookのみ、秘密禁止 |
| F-4.1 | 5 Prefix/85点 | 第25章 | Agent Skills名制約へ移行 |
| F-4.2 | Generator/Evaluator | 第25章 | Fresh Context分離 |
| F-4.3 | Progressive Disclosure | 第12、25章 | Root 200行目安 |
| F-4.4 | 4軸評価 | 第12、25章 | 各軸Minimumも追加 |
| F-4.5 | Claude/Codex両配置 | 第12、25章 | 正本1か所からBuild |
| F-5.1 | 50 File削除Flag | 第2、7、14章 | Manifest/Quarantine/Human Gate |
| F-5.2 | 20分Timeout | 第20、24章 | Scheduled/Lock/Stop |
| F-5.3 | Cron近接Deploy Block | 第14、26章 | Hook Fixture/Timezone |
| F-5.4 | Codex重複指示Block | 第25章 | Canonical Skill/重複検査 |
| NF Reliability | 冪等/Offline | 第20、24章 | 前回成功保持 |
| NF Observability | Log/Verify | 第24、26章 | Version/Block/Failure |
| NF Maintainability | common.sh/再利用 | 第23、24章 | Release Channel追加 |
| NF Security | PAT/顧客除外 | 第15、24、26章 | Managed Policy追加 |
| NF Compatibility | macOS | 第3、23、24章 | Sandbox/Kandji前提 |
| KPI | 時間/反映/Block/Score/停止 | 第26章 | 誤検知/成功率/Cost追加 |
| Known issue | 個人差込未提供 | 第23章 | Local Overlay案 |
| Known issue | Codex同期手動 | 第25章 | Build自動化 |
| Known issue | Kandji待ち | 第24章 | LaunchAgentをPOC限定 |
| Known issue | settings非配布 | 第23、26章 | Managed Settingsを正式Scope化 |

---

# 12. 未確認・変動項目の管理

次は教材本文へ固定せず、Feature Registryで管理する。

```text
- Model名、利用可否、料金、上限
- Auto ModeのProvider/Plan条件
- Dynamic WorkflowsのUI・提供条件
- DesignのBeta操作・連携先
- Cowork/Artifacts内API
- Advisor、Agent View、GoalのCommand詳細
- Changelog上の最低Version
```

Registry Entryは`status`、`verified_at`、`minimum_version`、`plans`、`official_source`、`migration_note`を必須にする。
