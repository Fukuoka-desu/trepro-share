#!/usr/bin/env bash
set -euo pipefail
RUNTIME="";SCOPE="project";TARGET="";DRY_RUN=0
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)";SOURCE="$ROOT/skill/textbook-chapter-lab"
usage(){ echo "Usage: ./install.sh --runtime cursor|claude|codex|all [--scope project|user] [--target PATH] [--dry-run]"; }
while [[ $# -gt 0 ]];do case "$1" in --runtime)RUNTIME="${2:-}";shift 2;;--scope)SCOPE="${2:-}";shift 2;;--target)TARGET="${2:-}";shift 2;;--dry-run)DRY_RUN=1;shift;;-h|--help)usage;exit 0;;*)echo "Unknown: $1" >&2;usage;exit 2;;esac;done
[[ "$RUNTIME" =~ ^(cursor|claude|codex|all)$ ]]||{ echo "--runtime required" >&2;exit 2; };[[ "$SCOPE" =~ ^(project|user)$ ]]||{ echo "invalid scope" >&2;exit 2; }
if [[ "$SCOPE" == project ]];then TARGET="${TARGET:-$PWD}";mkdir -p "$TARGET";TARGET="$(cd "$TARGET"&&pwd)";else TARGET="${TARGET:-$HOME}";fi
copy_skill(){ local dst="$1";if [[ $DRY_RUN -eq 1 ]];then echo "Would install: $dst";return;fi;mkdir -p "$(dirname "$dst")";[[ -e "$dst" ]]&&mv "$dst" "$dst.bak.$(date +%Y%m%d%H%M%S)";cp -R "$SOURCE" "$dst";echo "Installed: $dst"; }
case "$RUNTIME" in cursor)copy_skill "$TARGET/.cursor/skills/textbook-chapter-lab";;claude)copy_skill "$TARGET/.claude/skills/textbook-chapter-lab";;codex)copy_skill "$TARGET/.agents/skills/textbook-chapter-lab";;all)copy_skill "$TARGET/.cursor/skills/textbook-chapter-lab";copy_skill "$TARGET/.claude/skills/textbook-chapter-lab";copy_skill "$TARGET/.agents/skills/textbook-chapter-lab";;esac
if [[ $DRY_RUN -eq 0 ]];then
 if [[ "$SCOPE" == project ]];then cat > "$TARGET/trepro-textbook" <<EOF
#!/usr/bin/env bash
set -euo pipefail
ROOT="\$(cd "\$(dirname "\${BASH_SOURCE[0]}")" && pwd)"
for P in "\$ROOT/.agents/skills/textbook-chapter-lab/scripts/textbook_lab.py" "\$ROOT/.claude/skills/textbook-chapter-lab/scripts/textbook_lab.py" "\$ROOT/.cursor/skills/textbook-chapter-lab/scripts/textbook_lab.py";do [[ -f "\$P" ]]&&exec python3 "\$P" "\$@";done
echo "Skill script not found" >&2;exit 1
EOF
 chmod +x "$TARGET/trepro-textbook";echo "CLI: $TARGET/trepro-textbook"
 else BIN="$HOME/.local/bin";SHARE="$HOME/.local/share/trepro-textbook-chapter-lab";mkdir -p "$BIN" "$SHARE";rm -rf "$SHARE/skill";cp -R "$SOURCE" "$SHARE/skill";cat > "$BIN/trepro-textbook" <<EOF
#!/usr/bin/env bash
exec python3 "$SHARE/skill/scripts/textbook_lab.py" "\$@"
EOF
 chmod +x "$BIN/trepro-textbook";echo "CLI: $BIN/trepro-textbook";fi
fi
