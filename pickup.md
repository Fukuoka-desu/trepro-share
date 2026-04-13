---
description: 共有された Claude Code セッションを取り込み、受信側で引き継げる状態にする。/pickup <GIST_ID> 形式で使用。
allowed-tools: Bash
user-invocable: true
---

# Claude Code セッション引き継ぎ (Pickup)

送信側から共有された Gist ID を受け取り、現在の作業ディレクトリに対応する
Claude Code セッションとして配置する。

## 使い方

`/pickup <GIST_ID>`

例: `/pickup a2d7e2879e8791300986dead55cb14e2`

## 実行手順

引数として渡された Gist ID を使って、以下の pickup_session.sh を Bash ツールで実行する。
スクリプトは ssh 不要（HTTPS API 経由）で、確認プロンプトなしに自動実行される。

```bash
curl -sSL https://raw.githubusercontent.com/Fukuoka-desu/trepro-share/main/pickup_session.sh | bash -s <GIST_ID>
```

## 実行後の案内

スクリプトが正常終了したら、以下をユーザーに明確に伝えること:

1. **配置完了したセッション ID**
2. **次のコマンドをターミナルで実行する必要があること**:
   - `claude --resume <SESSION_ID>`
   - スクリプトは自動でクリップボードにコピー済み（Ctrl+V / Cmd+V で貼り付け可能）
3. **現在の Claude Code セッションは一度終了する必要がある**こと
   （同じターミナルで別セッションを起動するため）

## エラーハンドリング

- `gh: command not found` → `brew install gh` / `winget install GitHub.cli` を案内
- 認証エラー → `gh auth login` を案内
- Gist が見つからない → ユーザーに Gist ID の再確認を依頼
