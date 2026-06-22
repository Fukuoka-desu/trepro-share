#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parents[1]
BASE_HTML = ROOT / 'site' / 'complete.html'
BASE_MD = ROOT / 'claude-code-blog-complete.md'
SLIDE_DIR = ROOT / 'assets' / 'slides'
OUT_HTML = ROOT / 'site' / 'complete.html'
OUT_MD = ROOT / 'claude-code-blog-slide-integrated.md'

# Page, title, target type, exact HTML target id/text.
SLIDES: list[tuple[int, str, str, str]] = [
(1,'最初に読む結論 - 教科書は実行型の組織OS','heading','preface-s1'),
(2,'Claude Code実践教科書 - 個人活用から全社ハーネスまで','hero','main'),
(3,'第0部 最適な教科書の設計','part','part-0'),
(4,'Lessonの標準形','heading','ch-00-s5'),
(5,'3つの学習ルート','heading','ch-00-s1'),
(6,'本書の構成（前半）','heading','preface-s3'),
(7,'本書の構成（後半）','heading','preface-s3'),
(8,'AIコーディングの3世代','heading','ch-01-s2'),
(9,'Chat / Cowork / Code / Design - 4つの利用モード','heading','ch-01-s3'),
(10,'エージェントへ - 回答ではなく成果物','heading','ch-01-s1'),
(11,'「育てる」の正しい意味','heading','ch-01-s4'),
(12,'第1章 Claude Codeは何が違うのか','chapter-cover','chapter-01'),
(13,'初心者が最初に禁止すること','heading','ch-02-s3'),
(14,'安全な練習場の作り方','heading','ch-02-s4'),
(15,'第2章 安全を最初に設計する','chapter-cover','chapter-02'),
(16,'安全の基本式 - Guidance × Enforcement','heading','ch-02-s2'),
(17,'CLIの基本コマンド','heading','ch-03-s7'),
(18,'第3章 導入とProject Folder','chapter-cover','chapter-03'),
(19,'macOS CLIとVS Code導入','heading','ch-03-s2'),
(20,'Project Folderの原則','heading','ch-03-s3'),
(21,'完成形：会議アシスタント','heading','ch-04-s1'),
(22,'第4章 最初の90分実習 - 会議アシスタント','chapter-cover','chapter-04'),
(23,'要件定義テンプレート','heading','ch-04-s2'),
(24,'Skill → Plan → Implement','heading','ch-04-s6'),
(25,'完了報告の型','heading','ch-05-s5'),
(26,'定義で勝つ','heading','ch-05-s1'),
(27,'第5章 強い指示の書き方','chapter-cover','chapter-05'),
(28,'汎用Template 6ブロック','heading','ch-05-s2'),
(29,'7ステップの標準ループ','heading','ch-06-s1'),
(30,'ExploreとSpecify','heading','ch-06-s2'),
(31,'第6章 標準作業ループ','chapter-cover','chapter-06'),
(32,'PlanとImplement','heading','ch-06-s4'),
(33,'Verify → Review → Commit','heading','ch-06-s6'),
(34,'削除の標準手順','heading','ch-07-s6'),
(35,'第7章 Permission Mode、Sandbox','chapter-cover','chapter-07'),
(36,'Permission Modeの3段階','heading','ch-07-s1'),
(37,'Permission Rule - deny/allowの設計','heading','ch-07-s2'),
(38,'SandboxとSecrets','heading','ch-07-s4'),
(39,'AdvisorとFable 5の扱い','heading','ch-08-s4'),
(40,'Effortとultrathink','heading','ch-08-s2'),
(41,'第8章 ModelとEffort','chapter-cover','chapter-08'),
(42,'Model名ではなく役割で選ぶ','heading','ch-08-s1'),
(43,'/clear /compact /context','heading','ch-09-s2'),
(44,'Resumeと履歴を残さない実行','heading','ch-09-s4'),
(45,'第9章 SessionとContext','chapter-cover','chapter-09'),
(46,'Sessionを分ける基準','heading','ch-09-s1'),
(47,'GitとCheckpointは両方必要','heading','ch-10-s1'),
(48,'ClaudeへCommitさせるRule / Worktree','heading','ch-10-s4'),
(49,'第10章 GitとCheckpoint','chapter-cover','chapter-10'),
(50,'最小Git運用','heading','ch-10-s3'),
(51,'第11章 CLAUDE.md、Rules、Auto Memory','chapter-cover','chapter-11'),
(52,'良いCLAUDE.md - 6セクション構造','heading','ch-11-s3'),
(53,'責務の分離 - CLAUDE.md / Rule / Memory','heading','ch-11-s1'),
(54,'RulesとAuto Memory - 強制と個人化','heading','ch-11-s5'),
(55,'Progressive Disclosureと4軸評価','heading','ch-12-s5'),
(56,'SKILL.md標準Template','heading','ch-12-s4'),
(57,'Skillとは / Canonical Name','heading','ch-12-s3'),
(58,'第12章 Skills設計','chapter-cover','chapter-12'),
(59,'並列化に向く仕事','heading','ch-13-s6'),
(60,'Reviewer Agent / Research Agent','heading','ch-13-s2'),
(61,'第13章 Subagents、Agent View、並列','chapter-cover','chapter-13'),
(62,'Subagentを使う理由','heading','ch-13-s1'),
(63,'Hook Security / Plugins','heading','ch-14-s6'),
(64,'第14章 HooksとPlugins','chapter-cover','chapter-14'),
(65,'PreToolUse / PostToolUse','heading','ch-14-s2'),
(66,'SessionStart / Stop / /goal連携','heading','ch-14-s5'),
(67,'外部接続の3方式','heading','ch-15-s1'),
(68,'Prompt Injectionと導入Check','heading','ch-15-s6'),
(69,'第15章 MCP、Connectors、API','chapter-cover','chapter-15'),
(70,'ScopeとSecrets管理 / Read・Write分離','heading','ch-15-s2'),
(71,'形式選択の基準 - MD / HTML / PPTX','heading','ch-16-s1'),
(72,'第16章 MarkdownよりHTMLが向く仕事','chapter-cover','chapter-16'),
(73,'単一HTMLの標準と品質Check','heading','ch-16-s2'),
(74,'第17章 Claude Designから実装へ','chapter-cover','chapter-17'),
(75,'標準Flow：/design → /design-sync → 実装','heading','ch-17-s4'),
(76,'Design SystemとProjectを分離する','heading','ch-17-s2'),
(77,'会議DashboardとAcceptance','heading','ch-18-s6'),
(78,'第18章 CoworkとLive Artifacts','chapter-cover','chapter-18'),
(79,'Cowork向きの仕事','heading','ch-18-s1'),
(80,'Live Artifactの5層','heading','ch-18-s3'),
(81,'外部化する情報','heading','ch-19-s1'),
(82,'Interest Profile Skill / Recency Score','heading','ch-19-s4'),
(83,'第19章 Claude Codeを自分専用に育てる','chapter-cover','chapter-19'),
(84,'Privacy by Design','heading','ch-19-s2'),
(85,'音声・画像・割り込み - 個人化の入口','heading','ch-19-s7'),
(86,'自律化の4要素','heading','ch-20-s1'),
(87,'第20章 /goal、Headless、定期実行','chapter-cover','chapter-20'),
(88,'良いGoal - 終了条件は測定可能に','heading','ch-20-s2'),
(89,'Scheduled必須要件 / 自動化しないもの','heading','ch-20-s5'),
(90,'DynamicのAcceptance','heading','ch-21-s6'),
(91,'Cost ControlとDynamicを使わない判断','heading','ch-21-s3'),
(92,'第21章 Dynamic Workflows','chapter-cover','chapter-21'),
(93,'Dynamic Workflowsとは','heading','ch-21-s1'),
(94,'第22章 信頼できる調査とレポート','chapter-cover','chapter-22'),
(95,'Research Skill - Rules / Workflow / Deliverables','heading','ch-22-s3'),
(96,'Source優先度とClaim Ledger','heading','ch-22-s1'),
(97,'追加すべき4面','heading','ch-23-s3'),
(98,'第23章 最適Architecture','chapter-cover','chapter-23'),
(99,'Product定義と現行資産','heading','ch-23-s1'),
(100,'Release FlowとGuidance/Enforcement Mapping','heading','ch-23-s5'),
(101,'Bootstrap責務 / GitHub認証','heading','ch-24-s1'),
(102,'Convergent SyncとSkill Merge','heading','ch-24-s4'),
(103,'配布方式：Kandji / LaunchAgent','heading','ch-24-s9'),
(104,'第24章 配布、同期、更新、Rollback','chapter-cover','chapter-24'),
(105,'update.sh / verify / Rollback','heading','ch-24-s6'),
(106,'Generator/Evaluator分離・100点・Fixture-driven','heading','ch-25-s3'),
(107,'5 Prefixの移行とLifecycle','heading','ch-25-s1'),
(108,'第25章 Skill Governance','chapter-cover','chapter-25'),
(109,'Validator / 重複統合 / Deprecation','heading','ch-25-s7'),
(110,'Drop-in / Managed MCP / Hook Block Event','heading','ch-26-s3'),
(111,'第26章 Managed Policy、Security、Observability','chapter-cover','chapter-26'),
(112,'指標 / Retention / Incident / KPI','heading','ch-26-s6'),
(113,'Threat ModelとManaged Settings','heading','ch-26-s1'),
(114,'30分Flowと初日Safety','heading','ch-27-s1'),
(115,'認定 / 運用Cadence','heading','ch-27-s7'),
(116,'障害表 / Diagnostics','heading','ch-27-s9'),
(117,'第27章 OnboardingとRunbook','chapter-cover','chapter-27'),
(118,'契約書論点 / 会議Assistant本番化 / 週報','heading','ch-28-s3'),
(119,'第28章 文書・ファイル・会議','chapter-cover','chapter-28'),
(120,'請求書Folder一覧化 / Folder整理','heading','ch-28-s1'),
(121,'第29章 調査・Content・学習','chapter-cover','chapter-29'),
(122,'SNS・動画から教材 / 個人学習 / News Dashboard','heading','ch-29-s3'),
(123,'YouTube Research Skill / 番組Profile','heading','ch-29-s1'),
(124,'第30章 Application開発','chapter-cover','chapter-30'),
(125,'Diet / 投資支援 / 世界Dashboard','heading','ch-30-s5'),
(126,'Local Task Manager','heading','ch-30-s1'),
(127,'Deploy - 公開の安全','heading','ch-31-s4'),
(128,'第31章 Design・資料・公開','chapter-cover','chapter-31'),
(129,'LP / Design System / PPT・PDF Export','heading','ch-31-s1'),
(130,'毎朝Brief / 会議→Task Board','heading','ch-32-s1'),
(131,'第32章 継続業務の自動化','chapter-cover','chapter-32'),
(132,'Skill改善Loopと5段階の自動化Level','heading','ch-32-s3'),
(133,'第33章 失敗Pattern','chapter-cover','chapter-33'),
(134,'失敗トップパターン','heading','story-33'),
(135,'全社共通CLAUDE.md / Project CLAUDE.md','heading','ch-34-s2'),
(136,'Quality Gate Skill / Fresh Reviewer / Definition of Done','heading','ch-34-s8'),
(137,'Requirements / Implementation Plan / Completion Report','heading','ch-34-s3'),
(138,'第34章 コピペ用標準テンプレート','chapter-cover','chapter-34'),
(139,'第35章 教科書アプリの情報設計','chapter-cover','chapter-35'),
(140,'Content ModelとLesson JSON Schema','heading','ch-35-s3'),
(141,'Feature Registry / Progress / 実行連携','heading','ch-35-s6'),
(142,'第36章 30日導入計画','chapter-cover','chapter-36'),
(143,'Week 1〜4と30日後','heading','ch-36-s5'),
(144,'第37・38章 素材補正 / Coverage Map','heading','story-37'),
(145,'原典対応表（38章）','heading','ch-38-s2'),
(146,'終章 最強のまま保つ','chapter-cover','chapter-final'),
(147,'公式確認先','heading-text','公式確認先'),
]

# key: minutes, risk, workspace suffix, primary artifacts, outcome, task focus, terms, analogy.
CHAPTERS: dict[str, dict[str, Any]] = {
'00': {'minutes':25,'risk':'low','slug':'learning-system','artifacts':['learning-contract.md','success-evidence.md'],'outcome':'学習を行動・成果物・証拠・再開地点へ分解する','focus':'自分の学習目標と合格証拠を定義する','terms':{'Lesson':'一回で完結する学習単位','Artifact':'学習後に残る成果物','Evidence':'できたことを示す証拠','Checkpoint':'途中から戻れる保存地点'},'analogy':'ゲームの説明書を暗記するのではなく、短いクエストをクリアしてセーブする。'},
'01': {'minutes':25,'risk':'low','slug':'agent-basics','artifacts':['surface-map.md','agent-loop.md'],'outcome':'チャットAIと作業型エージェントの違いを説明する','focus':'Explore・Edit・Run・Verifyの流れを観察して図にする','terms':{'Agent':'道具を使って作業するAI','Tool':'AIが使う読み書き・実行機能','Command':'パソコンへの一回の命令','Verify':'結果を証拠で確かめること'},'analogy':'質問に答える家庭教師と、工具を使って作業する新人スタッフの違い。'},
'02': {'minutes':30,'risk':'low','slug':'safety','artifacts':['SAFETY.md','risk-matrix.md'],'outcome':'最小権限・隔離・可逆性・検証を組み合わせる','focus':'練習環境の禁止事項と安全境界を文書化する','terms':{'Permission':'許される操作の範囲','Sandbox':'作業範囲を囲う環境','Secret':'漏れると悪用される情報','Reversible':'元に戻せる性質'},'analogy':'理科実験を教室全体ではなく、安全眼鏡と実験台の中で行う。'},
'03': {'minutes':30,'risk':'low','slug':'project-folder','artifacts':['environment-report.md','project-tree.txt'],'outcome':'安全なProject Folderと開発入口を準備する','focus':'専用フォルダを作り、環境と構造を確認する','terms':{'Project Folder':'一つの仕事の作業範囲','Path':'ファイルの住所','Root':'Projectの一番上','CLI':'文字で操作する入口'},'analogy':'課題に必要な資料だけを一つの机へ置く。'},
'04': {'minutes':60,'risk':'low','slug':'meeting-assistant','artifacts':['minutes.md','tasks.json','report.html'],'outcome':'文字起こしから議事録・タスク・HTMLを作り検証する','focus':'Fixtureの会議文字起こしを三種類の成果物へ変換する','terms':{'Input':'処理前の材料','Output':'処理後の成果物','JSON':'機械が読みやすい構造化形式','Acceptance':'合格と判断する条件'},'analogy':'同じ食材から、食事用・保存用・配布用の三つの形を作る。'},
'05': {'minutes':30,'risk':'low','slug':'strong-request','artifacts':['request.md','done-when.md'],'outcome':'曖昧な希望を検証可能な仕事の定義へ変える','focus':'目的・Context・制約・成果物・完了条件・証拠を記述する','terms':{'Prompt':'AIへの依頼文','Context':'依頼の背景','Constraint':'守る条件','Done when':'完了の判定条件'},'analogy':'「いい感じに」ではなく、目的地・予算・時間を伝えて旅行を頼む。'},
'06': {'minutes':45,'risk':'low','slug':'standard-loop','artifacts':['spec.md','plan.md','verification.md'],'outcome':'七段階の標準Loopを一周する','focus':'小さな編集をExploreからCommitまで順に実行する','terms':{'Explore':'現状を調べる','Specify':'要求を決める','Implement':'実装する','Review':'別視点で見直す'},'analogy':'工作を、材料確認・設計・製作・検査・記録の順に進める。'},
'07': {'minutes':35,'risk':'medium','slug':'permissions','artifacts':['permission-matrix.md','deletion-dry-run.txt'],'outcome':'操作ごとに許可・拒否・確認を設計する','focus':'危険操作を分類し、削除はDry-runまで体験する','terms':{'Allow':'自動で許可する','Deny':'実行を拒否する','Bypass':'確認を飛ばす危険設定','Dry-run':'変更せず予定だけ表示する'},'analogy':'校内の部屋ごとに違う鍵と入室ルールを決める。'},
'08': {'minutes':25,'risk':'low','slug':'model-effort','artifacts':['model-effort-matrix.md'],'outcome':'ModelとEffortを仕事の役割で選ぶ','focus':'軽作業・標準作業・難所の選択表を作る','terms':{'Model':'AIの頭脳の種類','Effort':'考える深さ','Token':'AIが処理する情報量','Latency':'結果までの待ち時間'},'analogy':'近所は自転車、旅行は車、荷物運搬はトラックを選ぶ。'},
'09': {'minutes':30,'risk':'low','slug':'session-context','artifacts':['RESUME.md','context-budget.md'],'outcome':'会話に依存せず状態を保存・再開する','focus':'現在地・決定・未完了・次の一操作をRESUMEへ残す','terms':{'Session':'一続きの会話','Context':'AIが参照する情報','Compact':'会話を要約する','Resume':'保存地点から再開する'},'analogy':'机を片付け、必要な要約だけを次の授業へ持っていく。'},
'10': {'minutes':45,'risk':'medium','slug':'git-checkpoint','artifacts':['git-evidence.md','change.txt'],'outcome':'CheckpointとGitを別の時間軸で使い分ける','focus':'小さな変更をDiff確認し、意味あるCommitとして保存する','terms':{'Git':'変更履歴の管理','Commit':'説明付きセーブ地点','Diff':'変更前後の差','Worktree':'別作業を分離する作業木'},'analogy':'短いUndoと、日付付きの正式なセーブデータを両方持つ。'},
'11': {'minutes':40,'risk':'low','slug':'knowledge-layers','artifacts':['CLAUDE.md','rules/example.md','memory-note.md'],'outcome':'方針・Path別Rule・個人Memoryを分離する','focus':'Project方針と局所Ruleを別ファイルへ置く','terms':{'CLAUDE.md':'Project全体の方針','Rule':'条件付きで効く決まり','Scope':'情報が効く範囲','Memory':'短い個人向け記憶'},'analogy':'校則、理科室ルール、個人ノートを別の棚に置く。'},
'12': {'minutes':50,'risk':'low','slug':'skills','artifacts':['my-first-skill/SKILL.md','skill-evaluation.md'],'outcome':'成功手順を再利用可能なSkillへ外部化する','focus':'入力・前提・Workflow・出力契約・品質確認を持つSkillを作る','terms':{'Skill':'再利用する業務手順パッケージ','Trigger':'呼び出す条件','Workflow':'実行手順','Output contract':'成果物形式の約束'},'analogy':'一度きりの会話を、誰でも使える部活の作業マニュアルへ直す。'},
'13': {'minutes':45,'risk':'low','slug':'subagents','artifacts':['research.md','review.md','delegation-plan.md'],'outcome':'作成・調査・評価のContextを分ける','focus':'二つの独立タスクを分担し、統合責任者を決める','terms':{'Subagent':'一部を任せる別役割AI','Parallel':'同時に進める','Reviewer':'評価だけを行う役割','Delegation':'仕事を条件付きで渡す'},'analogy':'班ごとに調査し、別の先生が共通基準で採点する。'},
'14': {'minutes':55,'risk':'medium','slug':'hooks','artifacts':['hooks/pretool_guard.py','hook-test-report.md'],'outcome':'お願いではなく実行時のGuardで制約を強制する','focus':'危険文字列を拒否する小さなHookとFixture Testを作る','terms':{'Hook':'Eventで自動実行する処理','Event':'起動のきっかけ','Exit code':'成功・失敗を示す番号','Plugin':'複数拡張の配布単位'},'analogy':'戸締まりを校則だけでなく自動ロックでも守る。'},
'15': {'minutes':45,'risk':'medium','slug':'mcp-mock','artifacts':['mcp-example.json','trust-boundary.md'],'outcome':'外部接続をRead/Write・Scope・Secretで分ける','focus':'実API Keyを使わずMock接続とHuman Gateを設計する','terms':{'API':'サービス同士の窓口','MCP':'AIへ外部Toolを渡す標準','Scope':'許可する範囲','Prompt Injection':'外部データ内の悪意ある指示'},'analogy':'図書館では閲覧カードと蔵書を書き換える権限を分ける。'},
'16': {'minutes':50,'risk':'low','slug':'html-report','artifacts':['report.md','report.html','quality-check.md'],'outcome':'Markdownを正本にし、伝達用HTMLへ変換する','focus':'同じ内容を長文ブログ型HTMLへ変え、表示を確認する','terms':{'Markdown':'編集しやすい文章形式','HTML':'ブラウザ表示の構造','CSS':'見た目のルール','Responsive':'画面幅へ適応する設計'},'analogy':'下書きノートを、読み手向けの展示パネルへ組み替える。'},
'17': {'minutes':60,'risk':'low','slug':'design-to-code','artifacts':['wireframe.html','design-system.md','sync-rule.md'],'outcome':'情報・見た目・実装を段階的に決める','focus':'白黒WireframeからDesign Ruleと実装へ進む','terms':{'Wireframe':'画面の配置図','Design System':'見た目の共通ルール','Prototype':'操作できる試作品','Component':'再利用する画面部品'},'analogy':'家を建てる前に間取り、材料ルール、模型の順で確認する。'},
'18': {'minutes':60,'risk':'low','slug':'live-artifact','artifacts':['dashboard.html','meetings.json','acceptance.md'],'outcome':'更新・失敗・Cacheを持つ業務Dashboardを作る','focus':'Fixture JSONから再読込可能な会議Dashboardを作る','terms':{'Artifact':'AIが作る成果物','Live data':'再取得される情報','Cache':'結果の一時保存','Stale':'古い可能性がある状態'},'analogy':'貼り紙ではなく、更新時刻と故障表示がある案内板を作る。'},
'19': {'minutes':55,'risk':'medium','slug':'personalization','artifacts':['INTERESTS.md','privacy-notes.md'],'outcome':'会話Logから必要なSignalだけを安全に抽出する','focus':'匿名Fixtureから最近の関心を抽出し本人が修正できるProfileを作る','terms':{'JSONL':'一行一件のLog形式','Signal':'関心を示す手がかり','Recency':'最近さの重み','Opt-in':'本人が明示同意すること'},'analogy':'日記を全部公開せず、本人が選んだ学習テーマだけカードにする。'},
'20': {'minutes':50,'risk':'medium','slug':'goal-runner','artifacts':['goal-spec.md','runner.sh','stop-conditions.md'],'outcome':'達成条件と停止条件を持つ自律実行を設計する','focus':'最大回数・時間・Budget・Logを持つMock Runnerを作る','terms':{'Goal':'検証可能な目標','Headless':'画面操作なしの実行','Timeout':'時間上限','Idempotent':'繰り返しても壊れない性質'},'analogy':'夜間清掃ロボットに、範囲・終了時刻・緊急停止を設定する。'},
'21': {'minutes':55,'risk':'medium','slug':'multi-agent','artifacts':['workflow.md','research.md','verification.md','synthesis.md'],'outcome':'Research・Verify・Synthesizeを分離する','focus':'三役の入力・出力・Cost上限を決めた手動Workflowを実行する','terms':{'Dynamic Workflow':'結果に応じて分岐する流れ','Research':'情報収集','Verify':'独立検証','Synthesize':'統合して結論化する'},'analogy':'資料係、検証係、発表係を分けたグループ研究。'},
'22': {'minutes':60,'risk':'low','slug':'trusted-research','artifacts':['claim-ledger.csv','research-report.md'],'outcome':'主張と根拠を追跡可能にする','focus':'Fixture SourceからClaim Ledgerと反対証拠を持つReportを作る','terms':{'Primary source':'一次資料','Claim':'検証すべき主張','Citation':'根拠の参照','Traceability':'結果から元資料へ戻れること'},'analogy':'理科レポートの各結論へ、実験記録の番号を付ける。'},
'23': {'minutes':50,'risk':'low','slug':'architecture','artifacts':['architecture.md','layer-map.md','release-flow.md'],'outcome':'正本・配布・強制・個人差分を分離する','focus':'個人成功を全社Infrastructureへ広げる構成図を作る','terms':{'Architecture':'部品と関係の全体設計','Source of truth':'公式な正本','Managed layer':'中央管理する層','Canary':'少人数への先行配布'},'analogy':'職員室の公式時間割を配りつつ、生徒のノートは上書きしない。'},
'24': {'minutes':70,'risk':'medium','slug':'sync-rollback','artifacts':['sync.sh','manifest.txt','rollback.md'],'outcome':'冪等・収束的な配布とRollbackを実装する','focus':'Fixture DirectoryでDry-run、同期、削除追従、復旧を試す','terms':{'Bootstrap':'初回導入','Manifest':'配布物一覧','Convergent':'最終的に正本へ一致する','Rollback':'以前の版へ戻す'},'analogy':'荷物の明細を照合し、途中失敗なら前の箱へ戻す。'},
'25': {'minutes':55,'risk':'low','slug':'skill-governance','artifacts':['skill-registry.csv','evaluation.md','deprecation-plan.md'],'outcome':'Skillを作成から廃止まで製品として管理する','focus':'Owner・Fixture・Score・Statusを持つRegistryを作る','terms':{'Governance':'品質と責任の運用','Fixture':'固定テスト入力','Validator':'構造を自動確認するもの','Deprecation':'移行期間を持つ廃止予告'},'analogy':'図書館の本を登録・点検・統合・除籍まで管理する。'},
'26': {'minutes':60,'risk':'medium','slug':'managed-security','artifacts':['threat-model.md','policy-example.json','incident-runbook.md'],'outcome':'Policy・観測・Incident対応を一体化する','focus':'Mock Eventから脅威、強制策、Log、復旧手順を整理する','terms':{'Threat Model':'想定する脅威の整理','Policy':'中央管理する決まり','Observability':'状態を外から理解できること','Incident':'業務へ影響する事故'},'analogy':'薬品庫の鍵、入退室記録、事故連絡網を一緒に設計する。'},
'27': {'minutes':50,'risk':'low','slug':'onboarding','artifacts':['onboarding-30min.md','runbook.md','certification.md'],'outcome':'新人が安全に一周できる導入体験を作る','focus':'30分Flow、認定、障害時Runbookを作る','terms':{'Onboarding':'利用開始までの導入体験','Runbook':'状況別の手順書','Certification':'操作と理解の確認','Cadence':'定期運用の周期'},'analogy':'入部初日に説明だけでなく、実技と困った時の連絡先を渡す。'},
'28': {'minutes':45,'risk':'low','slug':'office-workflows','artifacts':['inventory.csv','dry-run-plan.md','meeting-output.md'],'outcome':'文書・ファイル業務を原本保護とReview付きで処理する','focus':'Fixture一覧を作り、変更予定をDry-runで確認する','terms':{'Original':'変更しない原本','Inventory':'対象一覧','Exception':'通常ルール外の例外','Dry-run':'変更前の試運転'},'analogy':'倉庫の品物を動かす前に、移動表を作って責任者が確認する。'},
'29': {'minutes':60,'risk':'low','slug':'content-learning','artifacts':['content-report.html','source-map.csv','quiz.md'],'outcome':'動画・SNS素材を検証済み教材へ変える','focus':'Source Topicを重複整理し、記事と想起問題を作る','terms':{'Synthesis':'複数情報の統合','Deduplication':'重複の統合','Recall':'答えを見ず思い出す学習','Source Map':'素材と成果物の対応表'},'analogy':'複数のノートを整理し、授業プリントと小テストへ作り直す。'},
'30': {'minutes':75,'risk':'medium','slug':'app-development','artifacts':['app/index.html','test-report.md','rollback-plan.md'],'outcome':'Prototypeを作り、失敗・検証・Rollbackまで確認する','focus':'ローカルTask Managerを作り、入力・保存・Errorを試す','terms':{'Frontend':'利用者が見る画面','Backend':'裏側の処理','Test':'期待動作の確認','Prototype':'アイデア確認用の試作品'},'analogy':'見た目だけの模型ではなく、ブレーキまで試す模型車を作る。'},
'31': {'minutes':55,'risk':'medium','slug':'publish','artifacts':['preview/index.html','publish-checklist.md','rollback-plan.md'],'outcome':'生成と公開を別のQuality Gateにする','focus':'Previewを作り、秘密・Link・Mobile・公開範囲を検査する','terms':{'Deploy':'利用環境へ配置する','Preview':'確認用の版','Production':'本番環境','A11y':'誰でも利用しやすい設計'},'analogy':'展示物を作った後、一般公開前にリハーサルと持ち物検査をする。'},
'32': {'minutes':55,'risk':'medium','slug':'automation','artifacts':['automation-scorecard.md','schedule-plan.md','failure-alert.md'],'outcome':'安定入力と安全な失敗経路を持つ仕事だけ自動化する','focus':'繰り返し業務を採点し、半自動からの成熟計画を作る','terms':{'Schedule':'実行時刻の設定','Retry':'一時失敗の再試行','Alert':'問題通知','Maturity':'自動化の成熟度'},'analogy':'毎日同じ時間割の作業から自動化し、例外は先生へ戻す。'},
'33': {'minutes':40,'risk':'low','slug':'failure-patterns','artifacts':['postmortem.md','prevention-map.md'],'outcome':'失敗をRoot CauseとGuardrailへ変える','focus':'Fixture事故を再現し、Rule・Skill・Hookのどこで防ぐか決める','terms':{'Failure Pattern':'繰り返す失敗の型','Root Cause':'根本原因','Guardrail':'危険を防ぐ安全柵','Postmortem':'事故後の振り返り'},'analogy':'失点映像から、個人を責めず守備位置と練習方法を直す。'},
'34': {'minutes':50,'risk':'low','slug':'templates','artifacts':['requirements.md','implementation-plan.md','completion-report.md'],'outcome':'依頼・計画・完了報告の抜けをTemplateで防ぐ','focus':'PlaceholderをProject固有情報へ置換し三文書を完成させる','terms':{'Template':'再利用するひな形','Placeholder':'後で置換する空欄','Schema':'項目と形式のルール','Definition of Done':'完了の共通定義'},'analogy':'申込書の空欄を具体的に埋め、提出前チェックを行う。'},
'35': {'minutes':60,'risk':'low','slug':'learning-app','artifacts':['lesson.json','state.json','RESUME.md'],'outcome':'本文・状態・証拠・再開を分離した学習Appを設計する','focus':'一章をLesson JSONへ変換し、Stateと再開メモを作る','terms':{'Content Model':'教材部品の構造','State':'現在の進捗','Schema':'保存形式の規則','Feature Registry':'変動仕様の台帳'},'analogy':'教科書ページだけでなく、現在地と提出物を持つ学習アプリ。'},
'36': {'minutes':45,'risk':'low','slug':'rollout','artifacts':['30-day-plan.md','weekly-gates.csv','kpi.md'],'outcome':'安全な実験から全社運用へ段階的に広げる','focus':'四週間のOwner・成果物・Exit Criteria・Rollbackを定義する','terms':{'Milestone':'途中の大きな区切り','Pilot':'小規模な試験導入','KPI':'成果を測る指標','Exit Criteria':'次へ進む条件'},'analogy':'文化祭展示を試作品、クラス内テスト、本番準備へ分ける。'},
'37': {'minutes':40,'risk':'low','slug':'feature-registry','artifacts':['feature-registry.csv','correction-notes.md'],'outcome':'安定原則と変動仕様を別の更新周期で管理する','focus':'古い主張を公式Sourceと照合し、確認日付きRegistryへ移す','terms':{'Stable Principle':'変わりにくい原則','Volatile':'変わりやすい情報','Changelog':'変更履歴','Verified at':'最後の確認日'},'analogy':'物理法則は教科書へ、器具の型番と価格は更新表へ置く。'},
'38': {'minutes':45,'risk':'low','slug':'coverage','artifacts':['coverage-map.csv','gap-report.md'],'outcome':'素材Topicの抜け・重複・配置先を証明する','focus':'Source Topicを章へMappingし未配置を検出する','terms':{'Coverage':'必要範囲の網羅','Mapping':'対応関係','Gap':'未配置の抜け','Traceability':'元資料へ戻れる性質'},'analogy':'試験範囲の各項目が、どのノートページにあるか一覧化する。'},
'final': {'minutes':90,'risk':'medium','slug':'capstone','artifacts':['release/README.md','release/quality-report.md','release/rollback.md'],'outcome':'学習・実務・改善・配布の循環を一つの卒業制作へ統合する','focus':'任意の業務を標準LoopとSkillへ落とし、検証済みReleaseを作る','terms':{'Maintenance':'使い続けるための保守','Owner':'品質責任者','Feedback Loop':'結果を次の改善へ戻す循環','Sunset':'安全な終了・廃止'},'analogy':'強い部活動が練習記録を見直し、試し、標準を更新し続ける。'},
}

FIXTURES = {
'04':['meeting-transcript.md'], '05':['vague-request.txt'], '15':['mock-mcp-data.json'],
'18':['meetings.json'], '19':['sample-log.jsonl'], '22':['source-pack.md'], '28':['office-files.csv'],
'29':['source-topics.csv'], '32':['recurring-work.csv'], '33':['failure-case.md'],
'37':['volatile-claims.md'], '38':['source-topics.csv'], 'final':['meeting-transcript.md','source-pack.md']
}


def label_for(key: str) -> str:
    return '終章' if key == 'final' else f'第{int(key)}章'


def chapter_id_from_target(target: str) -> str | None:
    m = re.match(r'(?:ch|chapter|story)-(\d+)', target)
    if m: return f'{int(m.group(1)):02d}'
    if target == 'chapter-final' or target == '公式確認先': return 'final'
    return None


def expected_target_label(soup: BeautifulSoup, target_type: str, target: str) -> str:
    if target_type == 'heading-text': return target
    node = soup.find(id=target)
    if not node: return target
    if target_type == 'chapter-cover':
        h = node.select_one('.chapter-head h1')
        return f"{label_for(chapter_id_from_target(target) or 'final')} {h.get_text(' ',strip=True) if h else ''}".strip()
    if target_type == 'part':
        h = node.select_one('.part-header h2')
        return h.get_text(' ',strip=True) if h else target
    return node.get_text(' ',strip=True)


def make_slide_manifest(base_soup: BeautifulSoup) -> list[dict[str, Any]]:
    items=[]
    for page,title,typ,target in SLIDES:
        p=SLIDE_DIR/f'slide-{page:03d}.webp'
        if not p.exists() or p.stat().st_size == 0: raise SystemExit(f'Missing slide {page}')
        data=p.read_bytes()
        items.append({
            'page':page,'filename':p.name,'title':title,'target_type':typ,'target':target,
            'target_label':expected_target_label(base_soup,typ,target),
            'width':1920,'height':1072,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
            'html_id':f'slide-page-{page:03d}'
        })
    return items


def slide_figure_html(item: dict[str, Any], prefix: str='../') -> Tag:
    s=BeautifulSoup('', 'html.parser')
    fig=s.new_tag('figure',attrs={'class':'lesson-slide' + (' is-cover' if item['target_type']=='chapter-cover' else ''),'id':item['html_id'],'data-slide-page':str(item['page'])})
    a=s.new_tag('a',href=f"{prefix}assets/slides/{item['filename']}")
    img=s.new_tag('img',src=f"{prefix}assets/slides/{item['filename']}",alt=f"{item['title']}を図解したスライド（元PDF {item['page']}ページ）",loading='lazy',decoding='async')
    a.append(img);fig.append(a)
    cap=s.new_tag('figcaption');strong=s.new_tag('strong');strong.string=f"PDF p.{item['page']} - {item['title']}";cap.append(strong);cap.append(s.new_tag('br'));cap.append(f"本文「{item['target_label']}」の理解を助ける図解。クリックすると拡大表示します。")
    fig.append(cap);return fig


def first_explanation_end(heading: Tag) -> Tag:
    # Put the image after the first meaningful explanatory block, before the next heading.
    node=heading.find_next_sibling()
    last=heading
    while node:
        if isinstance(node,Tag) and node.name in {'h1','h2','h3'}: break
        if isinstance(node,Tag) and node.name in {'p','ul','ol','pre','blockquote','table','div'}:
            last=node
            if node.get_text(' ',strip=True): break
        node=node.find_next_sibling()
    return last


def make_beginner_section(key: str, spec: dict[str, Any]) -> Tag:
    s=BeautifulSoup('', 'html.parser')
    sec=s.new_tag('section',attrs={'class':'beginner-primer','id':f'beginner-{key}'})
    eyebrow=s.new_tag('div',attrs={'class':'beginner-eyebrow'});eyebrow.string='完全初心者のための準備';sec.append(eyebrow)
    h=s.new_tag('h2');h.string='この章に入る前に';sec.append(h)
    p=s.new_tag('p',attrs={'class':'beginner-lead'});p.string=f"この章では、{spec['outcome']}ことを学びます。最初に専門用語を暗記するのではなく、{spec['focus']}小さな実習から理解します。";sec.append(p)
    grid=s.new_tag('div',attrs={'class':'beginner-grid'})
    card=s.new_tag('article',attrs={'class':'primer-card'});h3=s.new_tag('h3');h3.string='まず知っておくこと';card.append(h3);ul=s.new_tag('ul',attrs={'class':'beginner-basics'})
    basics=[f"この章の中心は「{spec['outcome']}」です。",f"練習は `learning-lab/chapter-{key}-{spec['slug']}` の中だけで行います。",f"完成は感覚ではなく、{spec['artifacts'][0]} と確認結果で判断します。"]
    for b in basics: li=s.new_tag('li');li.string=b;ul.append(li)
    card.append(ul);grid.append(card)
    card2=s.new_tag('article',attrs={'class':'primer-card'});h3=s.new_tag('h3');h3.string='身近なたとえ';card2.append(h3);p2=s.new_tag('p',attrs={'class':'beginner-analogy'});p2.string=spec['analogy'];card2.append(p2);grid.append(card2);sec.append(grid)
    h3=s.new_tag('h3');h3.string='この章で出てくる言葉';sec.append(h3)
    dl=s.new_tag('dl',attrs={'class':'beginner-terms'})
    for term,meaning in spec['terms'].items():
        dt=s.new_tag('dt');dt.string=term;dd=s.new_tag('dd');dd.string=meaning;dl.append(dt);dl.append(dd)
    sec.append(dl)
    note=s.new_tag('div',attrs={'class':'beginner-note'});strong=s.new_tag('strong');strong.string='今は覚えなくてよいこと: ';note.append(strong);note.append('すべてのコマンドや設定を暗記する必要はありません。章番号でLabを開始し、次の一操作と証拠を順番に確認してください。');sec.append(note)
    details=s.new_tag('details',attrs={'class':'mini-check'});summary=s.new_tag('summary');summary.string=f"30秒チェック - この章の合格を何で示しますか？";details.append(summary);ans=s.new_tag('p');ans.string=f"主な成果物 {', '.join(spec['artifacts'])} と、内容を確認した具体的な証拠で示します。";details.append(ans);sec.append(details)
    return sec


def hands_on_panel(key: str, spec: dict[str, Any]) -> Tag:
    s=BeautifulSoup('', 'html.parser')
    sec=s.new_tag('section',attrs={'class':'hands-on-launcher','id':f'hands-on-{key}','data-chapter-lab':key})
    e=s.new_tag('div',attrs={'class':'eyebrow'});e.string='Chapter Hands-on Skill';sec.append(e)
    h=s.new_tag('h2');h.string='この章を実際に操作する';sec.append(h)
    p=s.new_tag('p');p.string=f"章番号を伝えると、{spec['focus']}Labをすぐ開始します。進捗はProject内へ保存され、Cursor・Claude Code・Codex間で再開できます。";sec.append(p)
    start=f"{label_for(key)}を開始"
    u=s.new_tag('p',attrs={'class':'hands-on-universal'});st=s.new_tag('strong');st.string='共通の開始文: ';u.append(st);code=s.new_tag('code');code.string=start;u.append(code);btn=s.new_tag('button',attrs={'class':'copy-lab','data-copy-lab':start});btn.string='コピー';u.append(' ');u.append(btn);sec.append(u)
    meta=s.new_tag('div',attrs={'class':'hands-on-meta'})
    for text in [f"目安 {spec['minutes']}分",f"Risk {spec['risk']}",'4 Steps']:
        x=s.new_tag('span',attrs={'class':'hands-on-pill'});x.string=text;meta.append(x)
    sec.append(meta)
    grid=s.new_tag('div',attrs={'class':'hands-on-command-grid'})
    commands=[('Cursor',start),('Claude Code',f"/textbook-chapter-lab {'final' if key=='final' else int(key)}"),('Codex',f"$textbook-chapter-lab {start}")]
    for runtime,cmd in commands:
        box=s.new_tag('div',attrs={'class':'hands-on-command'});strong=s.new_tag('strong');strong.string=runtime;box.append(strong);c=s.new_tag('code');c.string=cmd;box.append(c);b=s.new_tag('button',attrs={'class':'copy-lab','data-copy-lab':cmd});b.string='コピー';box.append(b);grid.append(box)
    sec.append(grid)
    ul=s.new_tag('ul')
    for text in [f"主な成果物: {', '.join(spec['artifacts'])}",f"保存先: learning-lab/chapter-{key}-{spec['slug']}","返答は『できた』『できない』『質問』『保存』のいずれかで進めます。"]:
        li=s.new_tag('li');li.string=text;ul.append(li)
    sec.append(ul)
    return sec


EXTRA_CSS = r'''
/* Experiential edition */
.lesson-slide{max-width:920px;margin:28px 0 42px;border:1px solid #ead4b9;border-radius:20px;overflow:hidden;background:#fff;box-shadow:0 16px 45px rgba(85,48,18,.12)}.lesson-slide a{display:block}.lesson-slide img{width:100%;height:auto;display:block;aspect-ratio:120/67;object-fit:cover}.lesson-slide figcaption{padding:12px 17px;color:#5c5148;font-size:.9rem;background:#fffaf3}.lesson-slide.is-cover{margin-top:8px}.beginner-foundation{background:linear-gradient(145deg,#eff8f5,#fffaf0);border-top:1px solid #d7e7e2;border-bottom:1px solid #eadfca}.beginner-foundation-body{max-width:1050px;margin:0 auto}.beginner-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin:22px 0}.beginner-primer{margin:30px 0 38px;padding:28px;border:1px solid #bcd8ce;border-radius:22px;background:linear-gradient(145deg,#f2fbf7,#fffdf7);box-shadow:0 12px 34px rgba(23,54,48,.08)}.beginner-primer .beginner-eyebrow{font-size:.76rem;letter-spacing:.14em;text-transform:uppercase;font-weight:800;color:#24665a;margin-bottom:8px}.beginner-primer h2{margin-top:0;color:#173d37}.beginner-primer h3{font-size:1.06rem;margin:18px 0 8px;color:#244b45}.beginner-lead{font-size:1.08rem;line-height:1.9}.primer-card{padding:18px;border:1px solid #d7e7e2;border-radius:16px;background:rgba(255,255,255,.86)}.beginner-basics{margin:0;padding-left:1.35rem}.beginner-basics li{margin:.55rem 0}.beginner-analogy{border-left:5px solid #e6a75a;background:#fff6e8;padding:16px 18px;border-radius:0 14px 14px 0}.beginner-terms{display:grid;grid-template-columns:minmax(120px,.35fr) 1fr;border:1px solid #d7e7e2;border-radius:14px;overflow:hidden;margin:10px 0 18px}.beginner-terms dt,.beginner-terms dd{padding:11px 14px;margin:0;border-bottom:1px solid #e3eee9}.beginner-terms dt{font-weight:800;background:#eef7f3}.beginner-terms dd{background:#fff}.beginner-note{padding:15px 17px;border-radius:13px;background:#edf4ff;border:1px solid #cbdcf5}.mini-check{margin-top:16px;padding:12px 16px;border:1px solid #d9e5df;border-radius:13px;background:#fff}.mini-check summary{cursor:pointer;font-weight:800;color:#245c52}.hands-on-launcher{margin:30px 0 38px;padding:24px;border:2px solid #f2b36d;border-radius:20px;background:linear-gradient(135deg,#fff8ec,#f4f8ff);box-shadow:0 14px 36px rgba(78,49,20,.08)}.hands-on-launcher .eyebrow{font-size:.76rem;letter-spacing:.13em;text-transform:uppercase;color:#d64a15;font-weight:900}.hands-on-launcher h2{margin:.25rem 0 .5rem}.hands-on-meta{display:flex;gap:9px;flex-wrap:wrap;margin:12px 0}.hands-on-pill{background:white;border:1px solid #ead7bd;border-radius:999px;padding:5px 10px;font-size:.82rem}.hands-on-command-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:16px 0}.hands-on-command{border:1px solid #d8c6ac;border-radius:13px;background:white;padding:13px;text-align:left}.hands-on-command strong{display:block;margin-bottom:6px}.hands-on-command code{display:block;overflow-wrap:anywhere;white-space:normal}.copy-lab{margin-top:9px;border:0;border-radius:999px;background:#e85019;color:white;padding:7px 11px;font-weight:800;cursor:pointer}.hands-on-universal{border-left:5px solid #2669d8;background:#edf4ff;padding:13px 15px;border-radius:0 12px 12px 0}.chapter-quickstart{margin:22px 0;padding:18px;border:1px solid #f0cfaa;border-radius:16px;background:#fffaf2}.chapter-quickstart-row{display:flex;gap:9px;flex-wrap:wrap}.chapter-quickstart input{min-width:180px;flex:1;padding:11px 13px;border:1px solid #cdbca5;border-radius:10px;font-size:1rem}.chapter-quickstart button{border:0;border-radius:10px;padding:11px 15px;background:#e85019;color:white;font-weight:800;cursor:pointer}.copy-toast{position:fixed;right:18px;bottom:18px;background:#1d2d28;color:white;padding:11px 16px;border-radius:12px;opacity:0;transform:translateY(8px);transition:.2s;z-index:9999}.copy-toast.show{opacity:1;transform:none}.dark .beginner-primer,.dark .hands-on-launcher,.dark .chapter-quickstart{background:#241d17;border-color:#6c4b2d}.dark .hands-on-command,.dark .primer-card,.dark .mini-check{background:#181818;border-color:#555}.dark .hands-on-universal{background:#17243a}@media(max-width:820px){.hands-on-command-grid,.beginner-grid{grid-template-columns:1fr}.beginner-primer{padding:20px}.beginner-terms{grid-template-columns:1fr}}@media print{.copy-lab,.chapter-quickstart{display:none}.hands-on-launcher,.beginner-primer,.lesson-slide{box-shadow:none;break-inside:avoid}}
'''

EXTRA_JS = r'''
(() => {
  const toast=document.createElement('div');toast.className='copy-toast';toast.textContent='コピーしました';document.body.appendChild(toast);
  const copy=async text=>{try{await navigator.clipboard.writeText(text);toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),1200)}catch(e){window.prompt('コピーしてください',text)}};
  document.querySelectorAll('[data-copy-lab]').forEach(b=>b.addEventListener('click',()=>copy(b.dataset.copyLab)));
  const input=document.getElementById('chapter-quick-input');
  const norm=()=>{let v=(input?.value||'').trim();if(/^(終章|final|最後)$/i.test(v))return 'final';v=v.replace(/chapter|chap|ch|第|章|[-_ ]/gi,'');const n=Number(v);return Number.isInteger(n)&&n>=0&&n<=38?String(n).padStart(2,'0'):null};
  document.getElementById('chapter-quick-jump')?.addEventListener('click',()=>{const k=norm();if(!k)return alert('0〜38、または終章を入力してください');document.getElementById('hands-on-'+k)?.scrollIntoView({behavior:'smooth',block:'start'})});
  document.getElementById('chapter-quick-copy')?.addEventListener('click',()=>{const k=norm();if(!k)return alert('0〜38、または終章を入力してください');copy(k==='final'?'終章を開始':`第${Number(k)}章を開始`)});
})();
'''


def build_html(manifest: list[dict[str, Any]]) -> None:
    original=BASE_HTML.read_text(encoding='utf-8')
    (ROOT/'site'/'complete-text-only.html').write_text(original,encoding='utf-8')
    soup=BeautifulSoup(original,'html.parser')
    soup.title.string='Claude Code実践教科書 - 完全初心者・スライド・ハンズオン統合版'
    # Remove generated placeholders and prompt panels from reading flow; keep manifests in package.
    for fig in soup.select('figure.image-shell'): fig.decompose()
    for sec in list(soup.select('section.reference')):
        h=sec.find(['h2','h3'])
        if h and '補助図の制作指示' in h.get_text(): sec.decompose()
    # Header link.
    nav=soup.select_one('.site-header nav')
    if nav:
        a=soup.new_tag('a',href='hands-on.html');a.string='章番号ハンズオン';nav.append(a)
    hero=soup.select_one('.hero-grid > div')
    if hero:
        quick=BeautifulSoup('''<div class="chapter-quickstart"><strong>章番号からハンズオンへ</strong><p>0〜38、または「終章」を入力します。本文の該当章へ移動し、開始文をコピーできます。</p><div class="chapter-quickstart-row"><input id="chapter-quick-input" placeholder="例: 12 / 終章" inputmode="text"><button id="chapter-quick-jump">本文へ移動</button><button id="chapter-quick-copy">開始文をコピー</button></div></div>''','html.parser').div
        hero.append(quick)
    # Zero-start primer.
    first_part=soup.find(id='part-0')
    if first_part:
        primer=BeautifulSoup('''<section class="hero beginner-foundation" aria-labelledby="zero-start-title"><div class="chapter"><header class="chapter-head"><div class="eyebrow">Zero-start foundation</div><h1 id="zero-start-title">本当に0から読む人のための5分準備</h1></header><div class="beginner-foundation-body"><p class="lede">ファイルは情報を保存する箱、フォルダは箱をまとめる引き出し、Cursorは作業机、ターミナルは文字で命令する画面、ブラウザはHTMLを見る窓です。分からない言葉は各章で必要な分だけ説明します。</p><div class="beginner-note"><strong>四つの約束:</strong> 練習用コピーを使う。秘密を貼らない。削除・送信・公開・課金では止まる。「できた」は成果物と証拠で確認する。</div></div></div></section>''','html.parser').section
        first_part.insert_before(primer)
    # Chapter supplements and launchers.
    for key,spec in CHAPTERS.items():
        art=soup.find(id=f'chapter-{key}')
        if not art: raise SystemExit(f'chapter missing {key}')
        story=art.find('section',attrs={'aria-labelledby':f'story-{key}'})
        anchor=story if story else art.select_one('.chapter-head')
        b=make_beginner_section(key,spec);anchor.insert_after(b);b.insert_after(hands_on_panel(key,spec))
    # Insert slides grouped by exact target.
    groups: dict[tuple[str,str], list[dict[str,Any]]] = {}
    for item in manifest: groups.setdefault((item['target_type'],item['target']),[]).append(item)
    for (typ,target),items in groups.items():
        items=sorted(items,key=lambda x:x['page'])
        if typ=='hero':
            anchor=soup.select_one('.hero-grid')
            if not anchor: raise SystemExit('hero missing')
            for item in reversed(items): anchor.insert_before(slide_figure_html(item,prefix='../'))
            continue
        if typ=='heading-text':
            anchor=next((h for h in soup.find_all(['h1','h2','h3']) if h.get_text(' ',strip=True)==target),None)
        else: anchor=soup.find(id=target)
        if not anchor: raise SystemExit(f'target missing {typ} {target}')
        if typ=='chapter-cover': insert_after=anchor.select_one('.chapter-head') or anchor
        elif typ=='part': insert_after=anchor.select_one('.part-header') or anchor
        else: insert_after=first_explanation_end(anchor)
        # Insert in natural order.
        current=insert_after
        for item in items:
            fig=slide_figure_html(item,prefix='../');current.insert_after(fig);current=fig
    # CSS and JS.
    style=soup.find('style')
    if style: style.append(EXTRA_CSS)
    else:
        style=soup.new_tag('style');style.string=EXTRA_CSS;soup.head.append(style)
    script=soup.find('script')
    if script: script.append(EXTRA_JS)
    else:
        script=soup.new_tag('script');script.string=EXTRA_JS;soup.body.append(script)
    OUT_HTML.write_text('<!doctype html>\n'+str(soup).replace('<!DOCTYPE html>','',1).lstrip(),encoding='utf-8')


def strip_image_directives(md: str) -> str:
    lines=md.splitlines();out=[];i=0
    while i<len(lines):
        if lines[i].startswith('> **画像制作指示：'):
            while i<len(lines) and (lines[i].startswith('>') or not lines[i].strip()): i+=1
            continue
        if lines[i].strip()=='## 補助図の制作指示':
            i+=1
            while i<len(lines) and not lines[i].startswith('## 体験ミッション'): i+=1
            continue
        out.append(lines[i]);i+=1
    return '\n'.join(out)


def beginner_md(key:str,spec:dict[str,Any])->str:
    terms='\n'.join(f'| {k} | {v} |' for k,v in spec['terms'].items())
    return f'''## 完全初心者のための準備

> **この章に入る前に**  
> この章では、{spec['outcome']}ことを学びます。最初に専門用語を暗記するのではなく、{spec['focus']}小さな実習から理解します。

### まず知っておくこと

- この章の中心は「{spec['outcome']}」です。
- 練習は `learning-lab/chapter-{key}-{spec['slug']}` の中だけで行います。
- 完成は感覚ではなく、`{spec['artifacts'][0]}` と確認結果で判断します。

### 身近なたとえ

{spec['analogy']}

### この章で出てくる言葉

| 用語 | 中学生・高校生向けの意味 |
|---|---|
{terms}

> **今は覚えなくてよいこと**  
> すべてのコマンドや設定を暗記する必要はありません。章番号でLabを開始し、次の一操作と証拠を順番に確認してください。

<details><summary><strong>30秒チェック</strong> - この章の合格を何で示しますか？</summary>

主な成果物 `{', '.join(spec['artifacts'])}` と、内容を確認した具体的な証拠で示します。

</details>
'''


def hands_md(key:str,spec:dict[str,Any])->str:
    start=f'{label_for(key)}を開始'; num='final' if key=='final' else str(int(key))
    return f'''## この章をハンズオンで開始する

章番号を伝えるだけで、Cursor・Claude Code・Codexの共通Skillがこの章のLabを開始します。進捗はProject内へ保存され、Runtimeを変えても再開できます。

| Runtime | 入力する言葉 |
|---|---|
| Cursor | `{start}` |
| Claude Code | `/textbook-chapter-lab {num}` |
| Codex | `$textbook-chapter-lab {start}` |

- 目安: {spec['minutes']}分
- Risk: `{spec['risk']}`
- 主な成果物: `{ '`, `'.join(spec['artifacts']) }`
- 保存先: `learning-lab/chapter-{key}-{spec['slug']}`
'''


def slide_md(item:dict[str,Any])->str:
    cls='lesson-slide is-cover' if item['target_type']=='chapter-cover' else 'lesson-slide'
    return f'''<figure class="{cls}" id="{item['html_id']}" data-slide-page="{item['page']}">
  <a href="assets/slides/{item['filename']}"><img src="assets/slides/{item['filename']}" alt="{item['title']}を図解したスライド（元PDF {item['page']}ページ）" loading="lazy"></a>
  <figcaption><strong>PDF p.{item['page']} - {item['title']}</strong><br>本文「{item['target_label']}」の理解を助ける図解。クリックすると拡大表示します。</figcaption>
</figure>'''


def normalize_heading(s:str)->str:
    return re.sub(r'[^0-9a-zA-Z一-龥ぁ-んァ-ヶ]+','',s.lower().replace('`',''))


def markdown_target_line(lines:list[str], item:dict[str,Any]) -> int:
    typ,target=item['target_type'],item['target']
    if typ=='hero':
        # after introductory story paragraphs, before characters.
        for i,l in enumerate(lines):
            if l.startswith('## 登場人物'): return i
    if typ=='part':
        m=re.match(r'part-(\d+)',target);needle=f'# 第{int(m.group(1))}部' if m else ''
        for i,l in enumerate(lines):
            if l.startswith(needle): return i+1
    if typ=='chapter-cover':
        key=chapter_id_from_target(target)
        needle='# 終章' if key=='final' else f'# 第{int(key)}章'
        for i,l in enumerate(lines):
            if l.startswith(needle): return i+1
    if typ=='heading-text':
        for i,l in enumerate(lines):
            if l.lstrip('# ').strip()==target: return i+1
    # Heading IDs: restrict to chapter, or global preface.
    key=chapter_id_from_target(target)
    start=0;end=len(lines)
    if key:
        needle='# 終章' if key=='final' else f'# 第{int(key)}章'
        for i,l in enumerate(lines):
            if l.startswith(needle): start=i;break
        for j in range(start+1,len(lines)):
            if lines[j].startswith('# 第') and ('章' in lines[j] or '部' in lines[j]) or lines[j].startswith('# 終章') or lines[j].startswith('# 公式確認先'):
                end=j;break
    label=normalize_heading(item['target_label'])
    for i in range(start,end):
        if lines[i].startswith('#') and normalize_heading(lines[i].lstrip('# ').strip())==label:
            # Insert after the first explanatory block.
            j=i+1
            while j<end and not lines[j].strip(): j+=1
            if j<end:
                # Handle paragraph/list/code block until following blank.
                if lines[j].startswith('```'):
                    j+=1
                    while j<end and not lines[j].startswith('```'): j+=1
                    return min(j+1,end)
                while j<end and lines[j].strip() and not lines[j].startswith('#'): j+=1
                return j
            return i+1
    raise RuntimeError(f"Markdown target missing page {item['page']}: {item['target']} / {item['target_label']}")


def build_markdown(manifest:list[dict[str,Any]]) -> None:
    original=BASE_MD.read_text(encoding='utf-8')
    (ROOT/'claude-code-blog-complete-beginner-original.md').write_text(original,encoding='utf-8')
    md=strip_image_directives(original)
    lines=md.splitlines()
    # Global primer before first part.
    part0=next(i for i,l in enumerate(lines) if l.startswith('# 第0部'))
    global_primer='''## 本当に0から読む人のための5分準備

ファイルは情報を保存する箱、フォルダは箱をまとめる引き出し、Cursorは作業机、ターミナルは文字で命令する画面、ブラウザはHTMLを見る窓です。分からない言葉は各章で必要な分だけ説明します。

> **四つの約束**: 練習用コピーを使う。秘密を貼らない。削除・送信・公開・課金では止まる。「できた」は成果物と証拠で確認する。
'''.splitlines()
    lines[part0:part0]=['']+global_primer+['']
    # Beginner and hands-on blocks before each implementation reference.
    for key in reversed(list(CHAPTERS.keys())):
        needle='# 終章' if key=='final' else f'# 第{int(key)}章'
        start=next(i for i,l in enumerate(lines) if l.startswith(needle))
        end=len(lines)
        for j in range(start+1,len(lines)):
            if (lines[j].startswith('# 第') and ('章' in lines[j] or '部' in lines[j])) or lines[j].startswith('# 終章') or lines[j].startswith('# 公式確認先'):
                end=j;break
        impl=next((i for i in range(start,end) if lines[i].strip()=='## 実装リファレンス'),None)
        if impl is None: raise RuntimeError(f'Implementation heading missing {key}')
        block=(beginner_md(key,CHAPTERS[key])+'\n\n'+hands_md(key,CHAPTERS[key])+'\n').splitlines()
        lines[impl:impl]=block
    # Slides: calculate positions against the current text, insert from bottom to top. Multiple same positions keep page order.
    positions=[]
    for item in manifest: positions.append((markdown_target_line(lines,item),item))
    bypos:dict[int,list[dict[str,Any]]]={}
    for pos,item in positions:bypos.setdefault(pos,[]).append(item)
    for pos in sorted(bypos,reverse=True):
        block=[]
        for item in sorted(bypos[pos],key=lambda x:x['page']): block+=['',slide_md(item),'']
        lines[pos:pos]=block
    text='\n'.join(lines).replace('# Claude Code実践教科書 — 物語で歩くブログ完全版','# Claude Code実践教科書 - 完全初心者・スライド・ハンズオン統合版',1)
    OUT_MD.write_text(text.strip()+'\n',encoding='utf-8')
    (ROOT/'claude-code-blog-complete.md').write_text(text.strip()+'\n',encoding='utf-8')


def main():
    base_soup=BeautifulSoup(BASE_HTML.read_text(encoding='utf-8'),'html.parser')
    manifest=make_slide_manifest(base_soup)
    (ROOT/'slide_integration_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'beginner_supplements.json').write_text(json.dumps(CHAPTERS,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    build_html(manifest)
    build_markdown(manifest)
    print(json.dumps({'slides':len(manifest),'chapters':len(CHAPTERS),'html':str(OUT_HTML),'markdown':str(OUT_MD)},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
