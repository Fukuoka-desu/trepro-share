#!/bin/bash
# ============================================================
# share.sh - Claude Code 成果物をGitHub Pagesで即共有
# 株式会社トレプロ
# ============================================================
set -euo pipefail

# ---- 設定 ----
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
DOCS_DIR="${REPO_DIR}/docs"
TEMPLATE="${REPO_DIR}/.template.html"
BRANCH="main"

# ---- 色付き出力 ----
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

# ---- 引数チェック ----
if [ $# -eq 0 ]; then
    echo -e "${RED}エラー: ファイルを指定してください${NC}"
    echo ""
    echo "使い方:"
    echo "  ./share.sh output.md              # Markdownファイルを共有"
    echo "  ./share.sh result.html             # HTMLファイルをそのまま共有"
    echo "  ./share.sh report.md \"月次レポート\"  # タイトル付きで共有"
    exit 1
fi

INPUT_FILE="$1"
CUSTOM_TITLE="${2:-}"

if [ ! -f "$INPUT_FILE" ]; then
    echo -e "${RED}エラー: ファイルが見つかりません: ${INPUT_FILE}${NC}"
    exit 1
fi

# ---- ファイル情報 ----
FILENAME=$(basename "$INPUT_FILE")
EXTENSION="${FILENAME##*.}"
NAME="${FILENAME%.*}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DATE_DISPLAY=$(date +"%Y年%m月%d日 %H:%M")
AUTHOR=$(git config user.name 2>/dev/null || echo "TrePro")

# タイトル決定
if [ -n "$CUSTOM_TITLE" ]; then
    TITLE="$CUSTOM_TITLE"
else
    TITLE="$NAME"
fi

OUTPUT_NAME="${TIMESTAMP}_${NAME}.html"

# ---- docsディレクトリ確認 ----
mkdir -p "$DOCS_DIR"

# ---- HTML生成関数 ----
generate_html() {
    local md_content="$1"
    cat << HTMLEOF
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${TITLE} - TrePro Share</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #f5f5f5;
    color: #333;
    line-height: 1.8;
  }
  .header {
    background: linear-gradient(135deg, #1A1A1A 0%, #292F33 100%);
    color: white;
    padding: 24px 32px;
    border-bottom: 4px solid #D20B00;
  }
  .header h1 { font-size: 1.4rem; font-weight: 700; }
  .header .meta { font-size: 0.85rem; color: #aaa; margin-top: 4px; }
  .header .logo { font-size: 0.75rem; color: #D20B00; font-weight: 700; letter-spacing: 0.1em; margin-bottom: 8px; }
  .content {
    max-width: 860px;
    margin: 32px auto;
    background: white;
    padding: 40px 48px;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  }
  .content h1 { font-size: 1.5rem; margin: 32px 0 16px; color: #1A1A1A; border-bottom: 2px solid #D20B00; padding-bottom: 8px; }
  .content h2 { font-size: 1.25rem; margin: 28px 0 12px; color: #1A1A1A; }
  .content h3 { font-size: 1.1rem; margin: 24px 0 8px; color: #333; }
  .content p { margin: 12px 0; }
  .content ul, .content ol { margin: 12px 0 12px 24px; }
  .content li { margin: 4px 0; }
  .content code {
    background: #f0f0f0;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 0.9em;
    font-family: 'SF Mono', 'Fira Code', monospace;
  }
  .content pre {
    background: #1e1e1e;
    color: #d4d4d4;
    padding: 20px;
    border-radius: 6px;
    overflow-x: auto;
    margin: 16px 0;
    line-height: 1.5;
  }
  .content pre code { background: none; padding: 0; color: inherit; }
  .content blockquote {
    border-left: 4px solid #D20B00;
    padding: 12px 20px;
    margin: 16px 0;
    background: #fdf5f5;
    color: #555;
  }
  .content table { width: 100%; border-collapse: collapse; margin: 16px 0; }
  .content th, .content td { border: 1px solid #ddd; padding: 10px 14px; text-align: left; }
  .content th { background: #1A1A1A; color: white; font-weight: 600; }
  .content tr:nth-child(even) { background: #f9f9f9; }
  .footer { text-align: center; padding: 24px; color: #999; font-size: 0.8rem; }
  @media (max-width: 640px) {
    .content { padding: 24px 20px; margin: 16px; }
    .header { padding: 16px 20px; }
  }
</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
<div class="header">
  <div class="logo">TREPRO SHARE</div>
  <h1>${TITLE}</h1>
  <div class="meta">${DATE_DISPLAY} / ${AUTHOR}</div>
</div>
<div class="content">
HTMLEOF

    # Markdown → HTML変換（pandocがあれば使用）
    if command -v pandoc &> /dev/null; then
        echo "$md_content" | pandoc -f markdown -t html
    else
        # pandocなしの簡易変換
        echo "$md_content" | sed \
            -e 's/^### \(.*\)/<h3>\1<\/h3>/' \
            -e 's/^## \(.*\)/<h2>\1<\/h2>/' \
            -e 's/^# \(.*\)/<h1>\1<\/h1>/' \
            -e 's/^\* \(.*\)/<li>\1<\/li>/' \
            -e 's/^- \(.*\)/<li>\1<\/li>/' \
            -e 's/`\([^`]*\)`/<code>\1<\/code>/g' \
            -e 's/\*\*\([^*]*\)\*\*/<strong>\1<\/strong>/g' \
            -e '/^[^<]/s/.*/<p>&<\/p>/'
    fi

    cat << HTMLEOF
</div>
<div class="footer">
  Powered by TrePro Share | Claude Code → GitHub Pages
</div>
</body>
</html>
HTMLEOF
}

# ---- メイン処理 ----
echo -e "${CYAN}📦 共有準備中...${NC}"

case "$EXTENSION" in
    md|markdown|txt)
        echo "  Markdown → HTML 変換中..."
        md_content=$(cat "$INPUT_FILE")
        generate_html "$md_content" > "${DOCS_DIR}/${OUTPUT_NAME}"
        ;;
    html|htm)
        echo "  HTMLファイルをコピー中..."
        cp "$INPUT_FILE" "${DOCS_DIR}/${OUTPUT_NAME}"
        ;;
    *)
        echo -e "${RED}エラー: 未対応のファイル形式です (.md / .html のみ)${NC}"
        exit 1
        ;;
esac

# ---- インデックスページ再生成 ----
echo "  インデックスページ更新中..."

cat > "${DOCS_DIR}/index.html" << 'INDEXHEAD'
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TrePro Share</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Noto Sans JP', -apple-system, sans-serif; background: #f5f5f5; color: #333; }
  .header {
    background: linear-gradient(135deg, #1A1A1A 0%, #292F33 100%);
    color: white; padding: 32px; border-bottom: 4px solid #D20B00; text-align: center;
  }
  .header h1 { font-size: 1.6rem; }
  .header .logo { color: #D20B00; font-weight: 700; letter-spacing: 0.15em; margin-bottom: 8px; font-size: 0.8rem; }
  .header p { color: #aaa; font-size: 0.9rem; margin-top: 8px; }
  .list { max-width: 700px; margin: 32px auto; padding: 0 16px; }
  .item {
    background: white; border-radius: 8px; padding: 20px 24px; margin-bottom: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06); display: flex; justify-content: space-between;
    align-items: center; text-decoration: none; color: #333; transition: box-shadow 0.2s;
  }
  .item:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.12); }
  .item .title { font-weight: 700; font-size: 1rem; }
  .item .date { color: #999; font-size: 0.85rem; }
  .empty { text-align: center; color: #999; padding: 48px; }
</style>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
<div class="header">
  <div class="logo">TREPRO SHARE</div>
  <h1>共有ファイル一覧</h1>
  <p>Claude Code の成果物を共有するページです</p>
</div>
<div class="list">
INDEXHEAD

# HTMLファイルを日付逆順でリスト化（index.html自体は除外）
found=0
for f in $(ls -r "${DOCS_DIR}"/*.html 2>/dev/null); do
    fname=$(basename "$f")
    [ "$fname" = "index.html" ] && continue
    found=1

    file_date=$(echo "$fname" | grep -oE '^[0-9]{8}' | sed 's/\(....\)\(..\)\(..\)/\1\/\2\/\3/' || echo "")
    file_title=$(echo "$fname" | sed 's/^[0-9_]*//; s/\.html$//' | sed 's/_/ /g')
    [ -z "$file_title" ] && file_title="$fname"

    cat >> "${DOCS_DIR}/index.html" << ITEM
  <a class="item" href="${fname}">
    <span class="title">${file_title}</span>
    <span class="date">${file_date}</span>
  </a>
ITEM
done

if [ "$found" -eq 0 ]; then
    echo '<div class="empty">まだ共有ファイルはありません</div>' >> "${DOCS_DIR}/index.html"
fi

cat >> "${DOCS_DIR}/index.html" << 'INDEXFOOT'
</div>
</body>
</html>
INDEXFOOT

# ---- Git push ----
echo -e "${CYAN}🚀 GitHubにpush中...${NC}"
cd "$REPO_DIR"
git add docs/
git commit -m "share: ${TITLE} (${TIMESTAMP})" --quiet 2>/dev/null || true
git push origin "$BRANCH" --quiet 2>/dev/null

# ---- URL取得 ----
REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
if echo "$REMOTE_URL" | grep -q "github.com"; then
    REPO_PATH=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/](.+)(\.git)?$|\1|' | sed 's/\.git$//')
    OWNER=$(echo "$REPO_PATH" | cut -d'/' -f1)
    REPO_NAME=$(echo "$REPO_PATH" | cut -d'/' -f2)
    PAGE_URL="https://${OWNER}.github.io/${REPO_NAME}/${OUTPUT_NAME}"
    INDEX_URL="https://${OWNER}.github.io/${REPO_NAME}/"
else
    PAGE_URL="(GitHub PagesのURLを確認してください)"
    INDEX_URL=""
fi

echo ""
echo -e "${GREEN}✅ 共有完了！${NC}"
echo ""
echo -e "📄 ページURL:"
echo -e "   ${CYAN}${PAGE_URL}${NC}"
echo ""
echo -e "📋 一覧URL:"
echo -e "   ${CYAN}${INDEX_URL}${NC}"
echo ""
echo -e "このURLをSlack・LINEに貼ればOKです 🎉"
