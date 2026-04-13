#!/bin/bash
# ============================================================
# pickup_session.sh v2
# 共有された Claude Code セッション Gist を引き継ぐ
#
# 改善点:
#   - gh gist view --raw を使用（ssh 不要、HTTPS API 経由）
#   - 確認プロンプト削除（curl|bash でも完走）
#   - Claude Code 実装準拠の CWD→ディレクトリ名変換
#     (Windows Git Bash の /c/Users/... にも対応)
#   - resume コマンドを自動クリップボードコピー
#
# 使い方:
#   curl -sSL https://raw.githubusercontent.com/Fukuoka-desu/trepro-share/main/pickup_session.sh | bash -s <GIST_ID>
# ============================================================
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

GIST_ID="${1:-}"

if [ -z "$GIST_ID" ]; then
    echo -e "${RED}エラー: Gist IDを指定してください${NC}"
    echo "使い方: bash pickup_session.sh <GIST_ID>"
    exit 1
fi

# ---- 前提チェック ----
if ! command -v gh &> /dev/null; then
    echo -e "${RED}GitHub CLI (gh) が必要です${NC}"
    echo "  macOS:    brew install gh"
    echo "  Windows:  winget install GitHub.cli"
    echo "  Linux:    https://github.com/cli/cli#installation"
    exit 1
fi

if ! gh auth status &>/dev/null; then
    echo -e "${RED}GitHub認証が必要です。以下を実行してください:${NC}"
    echo "  gh auth login"
    exit 1
fi

echo -e "${CYAN}📥 Gist からセッション取得中...${NC}"

TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

# ---- Gist 内の .jsonl ファイル名を取得 ----
JSONL_NAME=$(gh gist view "$GIST_ID" --files 2>/dev/null | grep '\.jsonl$' | head -1 || true)
if [ -z "$JSONL_NAME" ]; then
    echo -e "${RED}エラー: Gist 内に .jsonl ファイルが見つかりません${NC}"
    echo "  Gist ID: $GIST_ID"
    exit 1
fi

# ---- raw 経由で取得（ssh 不要、HTTPS API） ----
gh gist view "$GIST_ID" --raw --filename "$JSONL_NAME" > "$TMPDIR/$JSONL_NAME"

if [ ! -s "$TMPDIR/$JSONL_NAME" ]; then
    echo -e "${RED}エラー: ファイル取得に失敗しました${NC}"
    exit 1
fi

SESSION_ID=$(basename "$JSONL_NAME" .jsonl)

# ---- CWD → Claude Code プロジェクトディレクトリ名変換 ----
# Mac/Linux:  /Users/foo/bar        → -Users-foo-bar
# Win GitBash: /c/Users/foo/bar     → c--Users-foo-bar
CWD=$(pwd)
if [[ "$CWD" =~ ^/([a-zA-Z])/ ]]; then
    # Windows Git Bash 形式（/c/Users/... など）
    DRIVE="${BASH_REMATCH[1]}"
    REST="${CWD#/$DRIVE/}"
    CWD_KEY="${DRIVE}--$(echo "$REST" | sed 's|/|-|g')"
else
    # Mac/Linux 形式（/Users/... or /home/...）
    CWD_KEY=$(echo "$CWD" | sed 's|/|-|g')
fi

TARGET_DIR="$HOME/.claude/projects/${CWD_KEY}"

echo -e "${CYAN}📁 配置先: ${TARGET_DIR}${NC}"

mkdir -p "$TARGET_DIR"

# ---- 無条件上書き（確認なし） ----
cp "$TMPDIR/$JSONL_NAME" "${TARGET_DIR}/${SESSION_ID}.jsonl"

RESUME_CMD="claude --resume ${SESSION_ID}"

# ---- OS別クリップボードコピー ----
COPIED=""
if command -v pbcopy &>/dev/null; then
    # macOS
    echo -n "$RESUME_CMD" | pbcopy 2>/dev/null && COPIED="macOS"
elif command -v clip.exe &>/dev/null; then
    # Windows Git Bash / WSL
    echo -n "$RESUME_CMD" | clip.exe 2>/dev/null && COPIED="Windows"
elif command -v clip &>/dev/null; then
    # Windows native
    echo -n "$RESUME_CMD" | clip 2>/dev/null && COPIED="Windows"
elif command -v xclip &>/dev/null; then
    # Linux (xclip)
    echo -n "$RESUME_CMD" | xclip -selection clipboard 2>/dev/null && COPIED="xclip"
elif command -v xsel &>/dev/null; then
    # Linux (xsel)
    echo -n "$RESUME_CMD" | xsel -ib 2>/dev/null && COPIED="xsel"
elif command -v wl-copy &>/dev/null; then
    # Wayland
    echo -n "$RESUME_CMD" | wl-copy 2>/dev/null && COPIED="wl-copy"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ✅ セッション配置完了${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "セッションID: ${CYAN}${SESSION_ID}${NC}"
echo -e "ファイル:     ${TARGET_DIR}/${SESSION_ID}.jsonl"
echo ""
echo -e "${YELLOW}▶ 次の1コマンドで会話を再開:${NC}"
echo ""
echo -e "    ${CYAN}${RESUME_CMD}${NC}"
echo ""
if [ -n "$COPIED" ]; then
    echo -e "${GREEN}✓ クリップボードにコピー済み（Ctrl+V / Cmd+V で貼り付け）${NC}"
else
    echo -e "${YELLOW}（クリップボード未対応環境: 上記を手動コピーしてください）${NC}"
fi
echo ""
