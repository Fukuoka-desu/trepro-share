#!/bin/bash
# ============================================================
# pickup_session.sh
# 共有されたClaude CodeセッションGistを引き継ぐ
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
    exit 1
fi

if ! command -v claude &> /dev/null; then
    echo -e "${YELLOW}警告: claude コマンドが見つかりません${NC}"
    echo "  Claude Code をインストールしてから再度実行してください"
fi

echo -e "${CYAN}📥 セッションJSONL取得中...${NC}"

TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

gh gist clone "$GIST_ID" "$TMPDIR/session" 2>&1 | tail -3

JSONL_FILE=$(ls "$TMPDIR/session"/*.jsonl 2>/dev/null | head -1)
if [ -z "$JSONL_FILE" ]; then
    echo -e "${RED}エラー: JSONLファイルが見つかりません${NC}"
    exit 1
fi

SESSION_ID=$(basename "$JSONL_FILE" .jsonl)
CWD_KEY=$(pwd | sed 's|/|-|g')
TARGET_DIR="$HOME/.claude/projects/${CWD_KEY}"

echo -e "${CYAN}📁 プロジェクトディレクトリに配置中...${NC}"
echo "  宛先: ${TARGET_DIR}"

mkdir -p "$TARGET_DIR"

# 既存ファイルチェック
if [ -f "${TARGET_DIR}/${SESSION_ID}.jsonl" ]; then
    echo -e "${YELLOW}既に同じセッションIDが存在します。上書きしますか? [y/N]${NC}"
    read -r confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "中止しました"
        exit 0
    fi
fi

cp "$JSONL_FILE" "${TARGET_DIR}/${SESSION_ID}.jsonl"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ✅ セッション取り込み完了${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "セッションID: ${CYAN}${SESSION_ID}${NC}"
echo -e "配置先: ${TARGET_DIR}/${SESSION_ID}.jsonl"
echo ""
echo -e "${YELLOW}▶ 次のコマンドで会話を継続できます:${NC}"
echo ""
echo -e "   ${CYAN}claude --resume ${SESSION_ID}${NC}"
echo ""
echo -e "または ${CYAN}claude${NC} を起動して対話式で選択してください"
