# Chapter Hands-on Guide

## 最短の開始

1. このFolderをCursor、Claude Code、Codexのいずれかで開く。
2. ブログの読みたい章を開く。
3. Agentへ `第12章を開始` のように伝える。
4. 表示された一操作だけを行う。
5. Evidenceを確認してから「できた」と返す。
6. 中断時は「保存」、次回は「再開」。

## 章番号の表現

次を同じ章として認識します。

```text
12
第12章
第12章を開始
チャプター12
chapter 12
ch-12
```

`終章`、`final`、`最後` は終章です。

## Runtime切替

Claude Codeで途中保存し、Cursorへ移る例:

```bash
./trepro-textbook save --summary "第12章 Step 2の前"
./trepro-textbook switch-runtime --runtime cursor
./trepro-textbook resume
```

会話履歴ではなくProject内Stateを使うため、別Runtimeでも同じ地点を復元できます。

## 質問

質問だけではStepを完了しません。Navigatorは次の順で答えます。

```text
直接回答
→ なぜそうなるか
→ 今のStepへ戻る一操作
```

## Evidence

- `file`: Workspace内の空でないFile
- `answer`: 自分の言葉による具体的説明
- `review`: 要件に照らした確認内容
- `command`: `exit=0` または `PASS` を含む実行結果

## Labをやり直す

```bash
./trepro-textbook start 12 --restart
```

Stateを直接編集せず、CLI経由で操作します。
