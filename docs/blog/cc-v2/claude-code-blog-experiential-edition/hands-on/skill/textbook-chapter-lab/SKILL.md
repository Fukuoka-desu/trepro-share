---
name: textbook-chapter-lab
description: Claude Code実践教科書の第0章〜第38章・終章を、Cursor、Claude Code、Codexで実際に操作しながら学ぶ章番号ハンズオン。ユーザーが「第12章を開始」「チャプター4」「23章から実践」「保存」「再開」「この章で質問」と言った時に使う。通常の開発代行だけを求める依頼には使わない。
---

# Textbook Chapter Lab

## Mission

章番号を受け取ったら、確認質問で止めずに該当Labを開き、1Turnに1操作ずつ案内する。進捗の正本は会話ではなく `.trepro-learning/textbook-state.json` とする。

## Chapter routing

- `0`〜`38`、`第12章`、`チャプター12`、`chapter 12`、`ch-12` を認識する。
- `final`、`終章`、`最後` は終章へ対応する。
- 前提章が未完了でも開始できる。必要な前提だけ短く表示する。
- 章番号がない「再開」は保存済みCurrent Chapterを使う。

## CLI locator

最初に `command -v trepro-textbook` を確認する。なければProject内の `./trepro-textbook`、`.agents/skills/.../scripts/textbook_lab.py`、`.claude/skills/...`、`.cursor/skills/...`、`hands-on/skill/...` の順で探す。Python Scriptを直接使う場合は `python3 <path>` とする。Stateを手編集しない。

## Start immediately

```bash
trepro-textbook start <chapter> --runtime <cursor|claude|codex> --json
```

同じ章が進行中なら `resume --json` を使う。返された `step` と `runtime_instruction` から、次の一操作だけを提示する。

## Turn format

```text
[第X章 | Step A/B | Runtime | Status]
目的: このStepで身につけること
今やること: 一つの具体操作
期待結果: 何が見えれば成功か
証拠: 完了に必要なEvidence
困った時: 最初に確認する一点
返答: 「できた」「できない」「質問」「保存」
```

## Progress and evidence

- 「できた」だけで完了にしない。Current StepのEvidenceを確認する。
- `file` はWorkspace内の空でないFile、`answer`・`review`は具体的説明、`command`は`exit=0`または`PASS`を要求する。
- 質問だけでは進捗を変更しない。順不同完了を認めない。

```bash
trepro-textbook complete --step-id <id> --evidence-type <type> --evidence <value> --json
```

## Save and resume

```bash
trepro-textbook save --summary "現在地と次の一操作" --json
trepro-textbook resume --json
trepro-textbook switch-runtime --runtime <cursor|claude|codex> --json
```

## Support protocol

質問には、直接回答 → なぜ → 今のStepへ戻る一操作、の順で答える。Error時は全文、Working Directory、直前操作を確認し、読み取り専用診断から始める。

## Safety

- Current Chapterの `learning-lab/` 以下だけを編集する。
- Secret、顧客データ、本番DBを使わない。
- Bypass、外部送信、Deploy、Git push、課金、破壊的削除、無断Installを行わない。
- 管理者章もFixtureとDry-runが既定。第31章はPreviewまで、第15章はMock接続だけ。

## Runtime invocation

- Cursor: `第12章を開始`
- Claude Code: `/textbook-chapter-lab 12`
- Codex: `$textbook-chapter-lab 第12章を開始`

全章一覧は `references/chapter-map.md`、Runtime差分は `references/runtime-guide.md`、安全規則は `references/safety-policy.md` を必要時だけ読む。
