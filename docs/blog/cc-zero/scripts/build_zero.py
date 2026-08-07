#!/usr/bin/env python3
"""Build the standalone Claude Code zero-beginner textbook page."""

from __future__ import annotations

import html
import re
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources" / "zero-textbook.md"
OUTPUT = ROOT / "site" / "index.html"
IMAGES_DIR = ROOT / "site" / "images"
MATERIALS_DIR = ROOT / "site" / "materials"
INTRO_VIDEO = ROOT / "site" / "videos" / "intro.mp4"

HEADING_RE = re.compile(
    r"^(#{1,6})\s+(.+?)\s+\{#([A-Za-z][A-Za-z0-9_.:-]*)\}\s*$"
)
ANY_HEADING_RE = re.compile(r"^#{1,6}\s+")
CHAPTER_ID_RE = re.compile(r"^zch-(?:\d{2}|final)$")
ORDERED_ITEM_RE = re.compile(r"^(\d+)\.\s+(.+)$")
UNORDERED_ITEM_RE = re.compile(r"^[-*]\s+(.+)$")
CHAPTER_TITLE_RE = re.compile(
    r"^(?P<label>第(?P<number>\d+)章|終章)\s+(?P<title>.+?)（(?P<minutes>\d+)分）$"
)
IMAGE_ID_RE = re.compile(r"^(?:cover-zero|zch-(?:\d{2}|final)-img\d+)$")
IMAGE_DIRECTIVE_RE = re.compile(r"^\*\*画像制作指示：([^*]+)\*\*$")

MATERIAL_SPECS = {
    "営業会議メモ.txt": ("zch-03", 0),
}
CHAPTER_MATERIALS = {
    "zch-03": "営業会議メモ.txt",
    "zch-05": "営業会議メモ.txt",
}


class BuildError(RuntimeError):
    """Raised when the source cannot be converted deterministically."""


def render_inline(value: str) -> str:
    """Render the small inline Markdown subset used by this textbook."""
    rendered = html.escape(value, quote=True)
    rendered = re.sub(r"`([^`]+)`", r"<code>\1</code>", rendered)
    rendered = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", rendered)

    def replace_link(match: re.Match[str]) -> str:
        label, href = match.groups()
        return f'<a href="{href}">{label}</a>'

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_link, rendered)


def strip_comments(markdown: str) -> str:
    return re.sub(r"<!--.*?-->", "", markdown, flags=re.DOTALL)


def collect_chapters(markdown: str) -> list[tuple[str, str]]:
    chapters: list[tuple[str, str]] = []
    seen_ids: set[str] = set()
    for line_number, line in enumerate(strip_comments(markdown).splitlines(), start=1):
        if not line.startswith("# "):
            continue
        match = HEADING_RE.match(line)
        if match is None:
            raise BuildError(
                f"line {line_number}: chapter heading requires an explicit ID"
            )
        _, title, heading_id = match.groups()
        if not CHAPTER_ID_RE.fullmatch(heading_id):
            raise BuildError(
                f"line {line_number}: invalid chapter ID {heading_id!r}"
            )
        if heading_id in seen_ids:
            raise BuildError(f"line {line_number}: duplicate ID {heading_id!r}")
        seen_ids.add(heading_id)
        chapters.append((heading_id, title))
    return chapters


def collect_chapter_goals(markdown: str) -> dict[str, str]:
    """Extract each first-section goal without changing the source wording."""
    lines = strip_comments(markdown).splitlines()
    goals: dict[str, str] = {}
    current_chapter = ""
    goal_section = ""
    for line in lines:
        heading = HEADING_RE.match(line)
        if heading:
            hashes, _, heading_id = heading.groups()
            if len(hashes) == 1:
                current_chapter = heading_id
                goal_section = ""
            elif len(hashes) == 2:
                goal_section = heading_id if heading_id == f"{current_chapter}-s1" else ""
            continue
        if goal_section and line.strip():
            goals[current_chapter] = line.strip()
            goal_section = ""
    return goals


def chapter_source(markdown: str, chapter_id: str) -> str:
    """Return one chapter's source, preserving fenced-block newlines."""
    chapter_heading = re.search(
        rf"^#\s+.+?\s+\{{#{re.escape(chapter_id)}\}}\s*$",
        markdown,
        flags=re.MULTILINE,
    )
    if chapter_heading is None:
        raise BuildError(f"missing material chapter: {chapter_id}")
    next_heading = re.search(r"^#\s+", markdown[chapter_heading.end() :], re.MULTILINE)
    end = (
        chapter_heading.end() + next_heading.start()
        if next_heading is not None
        else len(markdown)
    )
    return markdown[chapter_heading.end() : end]


def fenced_blocks(markdown: str, chapter_id: str) -> list[str]:
    chapter = chapter_source(markdown, chapter_id)
    return re.findall(
        r"^```[^\n]*\n(.*?)^```\s*$",
        chapter,
        flags=re.MULTILINE | re.DOTALL,
    )


def write_materials(markdown: str) -> list[Path]:
    """Extract source-backed materials and rebuild a deterministic ZIP."""
    MATERIALS_DIR.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    material_bytes: dict[str, bytes] = {}
    for filename, (chapter_id, block_index) in MATERIAL_SPECS.items():
        blocks = fenced_blocks(markdown, chapter_id)
        if block_index >= len(blocks):
            raise BuildError(
                f"material block {block_index} missing from chapter {chapter_id}"
            )
        content = blocks[block_index]
        destination = MATERIALS_DIR / filename
        destination.write_text(content, encoding="utf-8", newline="")
        written.append(destination)
        material_bytes[filename] = content.encode("utf-8")

    zip_path = MATERIALS_DIR / "教材ぜんぶ入り.zip"
    with zipfile.ZipFile(zip_path, "w") as archive:
        for filename in sorted(material_bytes):
            info = zipfile.ZipInfo(filename, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, material_bytes[filename])
    written.append(zip_path)
    return written


def render_chapter_heading(title: str, heading_id: str) -> str:
    match = CHAPTER_TITLE_RE.fullmatch(title)
    if match is None:
        return f'<h2 id="{heading_id}">{render_inline(title)}</h2>'
    badge = match.group("number") or "終"
    return (
        f'<h2 id="{heading_id}" class="chapter-header">'
        f'<span class="chapter-number" aria-hidden="true">{badge}</span>'
        f'<span class="sr-only">{render_inline(match.group("label"))} </span>'
        f'<span class="chapter-title">{render_inline(match.group("title"))}</span>'
        f'<span class="chapter-time">{match.group("minutes")}分</span>'
        "</h2>"
    )


def subsection_class(heading_id: str) -> str:
    suffix_to_class = {
        "-s1": "section-goal",
        "-s2": "section-analogy",
        "-s3": "section-steps",
        "-s4": "section-check",
        "-s5": "section-qa",
        "-s6": "section-glossary",
    }
    for suffix, css_class in suffix_to_class.items():
        if heading_id.endswith(suffix):
            return css_class
    return "chapter-section"


def image_directive(quote_lines: list[str]) -> tuple[str, str, str] | None:
    """Parse an image-production block into id, alt, and caption."""
    if not quote_lines:
        return None
    match = IMAGE_DIRECTIVE_RE.fullmatch(quote_lines[0])
    if match is None:
        return None
    image_id = match.group(1).strip()
    if not IMAGE_ID_RE.fullmatch(image_id):
        raise BuildError(f"invalid image directive ID: {image_id!r}")
    fields: dict[str, str] = {}
    for line in quote_lines[1:]:
        for label, key in (("代替テキスト：", "alt"), ("Caption：", "caption")):
            if line.startswith(label):
                fields[key] = line[len(label) :].strip()
    if not fields.get("alt") or not fields.get("caption"):
        raise BuildError(f"image directive {image_id} requires alt and Caption")
    return image_id, fields["alt"], fields["caption"]


def collect_image_directives(markdown: str) -> dict[str, tuple[str, str]]:
    lines = strip_comments(markdown).splitlines()
    directives: dict[str, tuple[str, str]] = {}
    index = 0
    while index < len(lines):
        if not lines[index].startswith(">"):
            index += 1
            continue
        quote_lines: list[str] = []
        while index < len(lines) and lines[index].startswith(">"):
            quote_lines.append(lines[index][1:].lstrip())
            index += 1
        directive = image_directive(quote_lines)
        if directive is None:
            continue
        image_id, alt, caption = directive
        if image_id in directives:
            raise BuildError(f"duplicate image directive: {image_id}")
        directives[image_id] = (alt, caption)
    return directives


def render_image_figure(image_id: str, alt: str, caption: str) -> str:
    if image_id == "cover-zero" or not (IMAGES_DIR / f"{image_id}.webp").is_file():
        return ""
    return (
        f'<figure class="lesson-figure" data-image-id="{image_id}">'
        f'<img loading="lazy" decoding="async" src="images/{image_id}.webp" '
        f'alt="{html.escape(alt, quote=True)}">'
        f'<figcaption>{render_inline(caption)}</figcaption>'
        "</figure>"
    )


def render_material_download(chapter_id: str) -> str:
    filename = CHAPTER_MATERIALS.get(chapter_id)
    if filename is None or not (MATERIALS_DIR / filename).is_file():
        return ""
    escaped_filename = html.escape(filename, quote=True)
    return (
        '<div class="material-download">'
        f'<a download href="materials/{escaped_filename}">'
        '<span aria-hidden="true">📄</span> 練習用ファイルをダウンロード</a>'
        '<p>ダウンロードできない環境では、下の枠をコピーしても同じものが作れます。</p>'
        "</div>"
    )


def render_chapter_achievement(chapter_id: str, goals: dict[str, str]) -> str:
    goal = goals.get(chapter_id)
    if not goal:
        raise BuildError(f"missing goal for {chapter_id}")
    return (
        '<div class="chapter-achievement">'
        '<span aria-hidden="true">✓</span>'
        '<p><strong>この章でできるようになったこと</strong>'
        f'{render_inline(goal)}</p></div>'
    )


def concept_diagram(diagram_id: str) -> str:
    """Render one source-backed concept as HTML-labelled, card-contained SVG."""
    diagrams = {
        "desk-assistant": """<figure class="concept-diagram" style="min-width:0" data-diagram="desk-assistant" aria-labelledby="diagram-desk-title">
  <figcaption id="diagram-desk-title"><span>RELATION</span>仕事机とアシスタントの関係</figcaption>
  <div class="diagram-graphic desk-relation" style="min-width:0">
    <div class="diagram-node cy">
      <svg viewBox="0 0 120 90" aria-hidden="true"><path d="M14 31h38l9 10h45v35H14z"/><path d="M27 76v9M93 76v9M22 25h31l8 8"/></svg>
      <div><b>練習用フォルダ</b><span>アシスタントへ渡す仕事机</span></div>
    </div>
    <svg class="relation-arrow" viewBox="0 0 100 38" aria-hidden="true"><path d="M5 19h82M73 7l14 12-14 12"/></svg>
    <div class="diagram-node pk">
      <svg viewBox="0 0 120 90" aria-hidden="true"><circle cx="60" cy="27" r="15"/><path d="M31 75c3-20 13-29 29-29s26 9 29 29M24 75h72"/></svg>
      <div><b>Claude</b><span>机の隣に座る新人アシスタント</span></div>
    </div>
  </div>
  <p class="diagram-note">机に置いた練習用ファイルだけを、今回の仕事に使います。</p>
</figure>""",
        "request-four": """<figure class="concept-diagram" style="min-width:0" data-diagram="request-four" aria-labelledby="diagram-request-title">
  <figcaption id="diagram-request-title"><span>REQUEST FLOW</span>依頼の型4点セット</figcaption>
  <div class="diagram-graphic four-flow" style="min-width:0">
    <div class="flow-node cy"><span class="flow-number">01</span><svg viewBox="0 0 72 56" aria-hidden="true"><circle cx="36" cy="28" r="18"/><path d="M36 4v12M36 40v12M12 28h12M48 28h12"/></svg><b>何を</b><small>頼みたい仕事</small></div>
    <div class="flow-node tl"><span class="flow-number">02</span><svg viewBox="0 0 72 56" aria-hidden="true"><path d="M8 14h23l6 7h27v28H8z"/><path d="M18 31h36M18 39h25"/></svg><b>どこから</b><small>使う元ネタ</small></div>
    <div class="flow-node pu"><span class="flow-number">03</span><svg viewBox="0 0 72 56" aria-hidden="true"><path d="M14 5h34l10 10v36H14zM48 5v11h10M23 28h26M23 37h20"/></svg><b>どんな形に</b><small>名前と並び</small></div>
    <div class="flow-node or"><span class="flow-number">04</span><svg viewBox="0 0 72 56" aria-hidden="true"><circle cx="36" cy="28" r="23"/><path d="M23 29l9 9 18-21"/></svg><b>どうなったら完成</b><small>自分で確かめる条件</small></div>
  </div>
</figure>""",
        "permission-three": """<figure class="concept-diagram dark-diagram" style="min-width:0" data-diagram="permission-three" aria-labelledby="diagram-permission-title">
  <figcaption id="diagram-permission-title"><span>PERMISSION CHECK</span>黒画面の見方は3点だけ</figcaption>
  <div class="diagram-graphic permission-flow" style="min-width:0">
    <div class="permission-start"><svg viewBox="0 0 76 56" aria-hidden="true"><rect x="4" y="5" width="68" height="46" rx="4"/><circle cx="15" cy="15" r="2"/><circle cx="23" cy="15" r="2"/><path d="M14 28h48M14 37h31"/></svg><b>確認画面</b></div>
    <div class="check-stack">
      <div><span>1</span><p><b>作業内容</b>削除・送信・公開・購入ではないか</p></div>
      <div><span>2</span><p><b>対象</b>練習用フォルダの中か</p></div>
      <div><span>3</span><p><b>自分の判断</b>少しでも不安がないか</p></div>
    </div>
    <svg class="branch-lines" viewBox="0 0 110 120" preserveAspectRatio="none" aria-hidden="true"><path d="M4 60h35M39 60c25 0 18-38 42-38h24M39 60c25 0 18 38 42 38h24"/></svg>
    <div class="decision-stack"><div class="decision-ok"><b>問題なし</b><span>進める</span></div><div class="decision-stop"><b>不安あり</b><span>断って説明を聞く</span></div></div>
  </div>
</figure>""",
        "history-cycle": """<figure class="concept-diagram" style="min-width:0" data-diagram="history-cycle" aria-labelledby="diagram-history-title">
  <figcaption id="diagram-history-title"><span>SAFE RETRY</span>失敗しても戻せる</figcaption>
  <div class="diagram-graphic history-cycle" style="min-width:0">
    <svg class="cycle-ring" viewBox="0 0 520 250" aria-hidden="true"><defs><marker id="cycle-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0l10 5-10 5z"/></marker></defs><path d="M146 69c75-58 171-51 235 1"/><path d="M411 105c22 69-8 116-67 139"/><path d="M296 231c-91 22-172-13-190-83"/></svg>
    <div class="cycle-node change"><span>01</span><svg viewBox="0 0 64 48" aria-hidden="true"><path d="M12 5h31l9 9v29H12zM43 5v10h9M21 25h22M21 33h15"/></svg><b>変更する</b></div>
    <div class="cycle-node notice"><span>02</span><svg viewBox="0 0 64 48" aria-hidden="true"><circle cx="27" cy="22" r="14"/><path d="M38 33l13 11M27 13v10M27 29h.1"/></svg><b>違いに気づく</b></div>
    <div class="cycle-node restore"><span>03</span><svg viewBox="0 0 64 48" aria-hidden="true"><path d="M17 17H6L17 6M7 17c7-10 26-13 38-3 13 11 8 28-6 32"/></svg><b>履歴から戻す</b></div>
  </div>
  <p class="diagram-note">戻したあとは、意図した変更だけが消えたかを自分で確かめます。</p>
</figure>""",
    }
    try:
        return diagrams[diagram_id]
    except KeyError as error:
        raise BuildError(f"unknown concept diagram: {diagram_id}") from error


def render_markdown(markdown: str, goals: dict[str, str]) -> str:
    lines = strip_comments(markdown).splitlines()
    rendered: list[str] = []
    seen_ids: set[str] = set()
    chapter_open = False
    subsection_open = False
    current_chapter_id = ""
    current_section_id = ""
    inserted_diagrams: set[str] = set()
    index = 0

    def close_subsection() -> None:
        nonlocal subsection_open, current_section_id
        if not subsection_open:
            return
        section_diagram = {
            "zch-02-s2": "desk-assistant",
            "zch-07-s2": "history-cycle",
        }.get(current_section_id)
        if section_diagram and section_diagram not in inserted_diagrams:
            rendered.append(concept_diagram(section_diagram))
            inserted_diagrams.add(section_diagram)
        rendered.append("</section>")
        subsection_open = False
        current_section_id = ""

    def close_chapter() -> None:
        nonlocal chapter_open
        if not chapter_open:
            return
        rendered.append(render_chapter_achievement(current_chapter_id, goals))
        rendered.append("</section>")
        chapter_open = False

    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue

        heading = HEADING_RE.match(line)
        if heading:
            hashes, title, heading_id = heading.groups()
            if heading_id in seen_ids:
                raise BuildError(f"duplicate heading ID: {heading_id}")
            seen_ids.add(heading_id)
            source_level = len(hashes)
            if source_level == 1:
                close_subsection()
                close_chapter()
                current_chapter_id = heading_id
                rendered.append(
                    f'<section class="chapter" aria-labelledby="{heading_id}">'
                )
                rendered.append(render_chapter_heading(title, heading_id))
                chapter_open = True
            elif source_level == 2:
                close_subsection()
                current_section_id = heading_id
                rendered.append(f'<section class="{subsection_class(heading_id)}">')
                rendered.append(
                    f'<h3 id="{heading_id}">{render_inline(title)}</h3>'
                )
                if heading_id.endswith("-s3"):
                    download = render_material_download(current_chapter_id)
                    if download:
                        rendered.append(download)
                subsection_open = True
            else:
                output_level = min(source_level + 1, 6)
                rendered.append(
                    f'<h{output_level} id="{heading_id}">'
                    f"{render_inline(title)}</h{output_level}>"
                )
            index += 1
            continue

        if ANY_HEADING_RE.match(line):
            raise BuildError(
                f"line {index + 1}: every heading requires an explicit {{#id}}"
            )

        if line.startswith("```"):
            language = line[3:].strip()
            code_lines: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].startswith("```"):
                code_lines.append(lines[index])
                index += 1
            if index >= len(lines):
                raise BuildError("unclosed fenced code block")
            index += 1
            language_class = ""
            if language:
                safe_language = re.sub(r"[^A-Za-z0-9_-]", "", language)
                language_class = f' class="language-{safe_language}"'
            code = html.escape("\n".join(code_lines), quote=False)
            rendered.append(
                '<div class="copy-block" aria-label="コピー用の文章">'
                '<span class="copy-label">このままコピー</span>'
                f"<pre><code{language_class}>{code}</code></pre>"
                "</div>"
            )
            continue

        if line.startswith(">"):
            quote_lines: list[str] = []
            while index < len(lines) and lines[index].startswith(">"):
                quote_lines.append(lines[index][1:].lstrip())
                index += 1
            directive = image_directive(quote_lines)
            if directive is not None:
                figure = render_image_figure(*directive)
                if figure:
                    rendered.append(figure)
                continue
            quote_text = "\n".join(quote_lines)
            if "読めない黒い文字が出たら" in quote_text:
                quote_class = "safety-note"
            else:
                quote_class = "note"
            rendered.append(f'<blockquote class="{quote_class}">')
            for quote_line in quote_lines:
                if quote_line:
                    rendered.append(f"<p>{render_inline(quote_line)}</p>")
            rendered.append("</blockquote>")
            if (
                current_section_id == "zch-04-s3"
                and quote_class == "safety-note"
                and "permission-three" not in inserted_diagrams
            ):
                rendered.append(concept_diagram("permission-three"))
                inserted_diagrams.add("permission-three")
            continue

        ordered_item = ORDERED_ITEM_RE.match(line)
        if ordered_item:
            first_number = int(ordered_item.group(1))
            items: list[str] = []
            while index < len(lines):
                item_match = ORDERED_ITEM_RE.match(lines[index])
                if item_match is None:
                    break
                items.append(item_match.group(2))
                index += 1
            start_attribute = "" if first_number == 1 else f' start="{first_number}"'
            counter_style = f' style="--step-start: {first_number - 1}"'
            rendered.append(f"<ol{start_attribute}{counter_style}>")
            rendered.extend(f"<li>{render_inline(item)}</li>" for item in items)
            rendered.append("</ol>")
            continue

        unordered_item = UNORDERED_ITEM_RE.match(line)
        if unordered_item:
            items: list[str] = []
            while index < len(lines):
                item_match = UNORDERED_ITEM_RE.match(lines[index])
                if item_match is None:
                    break
                items.append(item_match.group(1))
                index += 1
            rendered.append("<ul>")
            rendered.extend(f"<li>{render_inline(item)}</li>" for item in items)
            rendered.append("</ul>")
            if (
                current_section_id == "zch-06-s3"
                and "request-four" not in inserted_diagrams
            ):
                rendered.append(concept_diagram("request-four"))
                inserted_diagrams.add("request-four")
            continue

        paragraph_lines = [line.strip()]
        index += 1
        while index < len(lines):
            candidate = lines[index]
            if not candidate.strip():
                break
            if (
                HEADING_RE.match(candidate)
                or ANY_HEADING_RE.match(candidate)
                or candidate.startswith("```")
                or candidate.startswith(">")
                or ORDERED_ITEM_RE.match(candidate)
                or UNORDERED_ITEM_RE.match(candidate)
            ):
                break
            paragraph_lines.append(candidate.strip())
            index += 1
        rendered.append(f"<p>{render_inline(' '.join(paragraph_lines))}</p>")

    close_subsection()
    close_chapter()
    expected_diagrams = {
        "desk-assistant",
        "request-four",
        "permission-three",
        "history-cycle",
    }
    if inserted_diagrams != expected_diagrams:
        raise BuildError(
            "concept diagram placement mismatch: "
            f"expected {sorted(expected_diagrams)!r}, got {sorted(inserted_diagrams)!r}"
        )
    return "\n".join(rendered)


def render_toc_item(chapter_id: str, title: str, goal: str) -> str:
    match = CHAPTER_TITLE_RE.fullmatch(title)
    if match is None:
        return f'<li><a href="#{chapter_id}">{render_inline(title)}</a></li>'
    badge = match.group("number") or "終"
    return (
        f'<li><a href="#{chapter_id}">'
        f'<span class="toc-number" aria-hidden="true">{badge}</span>'
        f'<span class="toc-copy"><span class="sr-only">'
        f'{render_inline(match.group("label"))} </span>'
        f'<span class="toc-title">{render_inline(match.group("title"))}</span>'
        f'<span class="toc-goal">{render_inline(goal)}</span></span>'
        f'<span class="toc-time">{match.group("minutes")}分</span>'
        "</a></li>"
    )


# assets/example.html の <style> ブロックを無改変でコピーしたCSS正本。
BASE_CSS = r""":root{
  color-scheme: light;
  --ink:#33363c;
  --ink-strong:#22242a;
  --sub:#7a808a;
  --line:#ebebee;
  --bg:#ffffff;
  --bg-soft:#fbfbfc;
  --cy:#2ec9e0;
  --tl:#3fd0bd;
  --pk:#f0399b;
  --pu:#9163f2;
  --or:#ff8a3d;
  --cr:#ff6a6a;
  --num:"Helvetica Neue",Helvetica,Arial,sans-serif;
  --jp:-apple-system,BlinkMacSystemFont,"Hiragino Sans","Noto Sans JP",sans-serif;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:var(--jp); font-size:16.5px; font-weight:500; line-height:1.95;
  -webkit-font-smoothing:antialiased; overflow-x:hidden;
}
a{color:inherit}
.wrap{max-width:1120px; margin:0 auto; padding:0 24px}

/* ---------- header ---------- */
.site{
  position:sticky; top:0; z-index:50; background:rgba(255,255,255,.94);
  backdrop-filter:saturate(180%) blur(12px);
  border-bottom:1px solid var(--line);
}
.site .bar{display:flex; align-items:center; gap:16px; height:58px; max-width:1120px; margin:0 auto; padding:0 24px}
.mark{
  width:34px; height:34px; border-radius:9px; flex:none;
  background:linear-gradient(135deg,var(--cy),var(--pu) 48%,var(--pk));
  display:flex; align-items:center; justify-content:center;
  color:#fff; font:700 13px/1 var(--num); letter-spacing:.04em;
}
.brand{font:700 14.5px/1.2 var(--jp); letter-spacing:.02em; color:var(--ink-strong)}
.brand span{display:block; font:600 11px/1.4 var(--num); letter-spacing:.18em; color:var(--sub); text-transform:uppercase}
.site nav{margin-left:auto; display:flex; gap:24px; font-size:13.5px; color:var(--sub)}
.site nav a{text-decoration:none}
.site nav a:hover{color:var(--pk)}
@media(max-width:760px){.site nav{display:none}}
.btn-entry{
  margin-left:auto; text-decoration:none; color:#fff; font:700 12.5px/1 var(--num);
  letter-spacing:.14em; padding:11px 18px; border-radius:2px;
  background:linear-gradient(100deg,var(--pk),var(--or));
}
.site nav + .btn-entry{margin-left:22px}

/* ---------- hero ---------- */
.hero{--bh:clamp(150px,16.5vw,198px); position:relative; overflow:hidden; background:#fff}
.hero .bandbg{
  position:absolute; left:0; right:0; bottom:0; height:var(--bh); z-index:0;
  background:linear-gradient(96deg,#2ec9e0 0%,#48c8d8 19%,#9163f2 43%,#f0399b 63%,#ff7a5c 83%,#ffb03c 100%);
}
.hero svg.bgart{position:absolute; inset:0; width:100%; height:100%; z-index:1; pointer-events:none}
.hrow{position:relative; z-index:2}
.hrow .in2{
  max-width:1120px; margin:0 auto; padding:0 24px; height:100%; position:relative;
  display:flex; flex-direction:column; justify-content:flex-end;
}
.htop{height:clamp(238px,27vw,318px)}
.hband{height:var(--bh)}
.hband .in2{justify-content:center}
.kicker{position:absolute; left:24px; top:clamp(56px,8vw,100px); padding-top:22px}
.kicker::before{
  content:""; position:absolute; top:0; left:0; width:52px; height:3px;
  background:linear-gradient(90deg,var(--cy),var(--pk));
}
.kicker b{font:700 17px/1.6 var(--jp); letter-spacing:.14em; color:var(--ink-strong)}
.l1{
  display:block; text-align:right; padding-bottom:8px;
  font:300 clamp(48px,8.2vw,104px)/1 var(--num); letter-spacing:.01em;
  background:linear-gradient(92deg,var(--pk) 8%,var(--or) 92%);
  -webkit-background-clip:text; background-clip:text; color:transparent;
}
.l2{
  display:block; text-align:right;
  font:300 clamp(50px,9.4vw,118px)/1 var(--num);
  letter-spacing:.16em; color:rgba(255,255,255,.72);
}
@media(max-width:700px){
  .htop{height:clamp(212px,44vw,268px)}
  .htop .in2{justify-content:flex-start}
  .kicker{position:static; margin-bottom:auto; padding-top:66px}
  .kicker::before{top:44px}
  .l1,.l2{text-align:left}
  .l1{margin-top:auto}
}

/* ---------- lead ---------- */
.lead{padding:64px 24px 8px; text-align:center; max-width:760px; margin:0 auto}
.lead p{margin:0; font-size:16.5px; color:#4c5058; line-height:2}
.lead p b{color:var(--ink-strong)}

/* ---------- number grid ---------- */
.dataarea{background:var(--bg-soft); padding:44px 0 60px; margin-top:44px}
.grid{display:grid; grid-template-columns:repeat(12,1fr); gap:12px}
.cell{
  grid-column:span 4; background:#fff; border:1px solid var(--line);
  padding:32px 30px 22px; display:flex; flex-direction:column; min-height:254px;
}
.cell.w5{grid-column:span 5} .cell.w4{grid-column:span 4} .cell.w3{grid-column:span 3}
.cell.w7{grid-column:span 7} .cell.w12{grid-column:span 12}
@media(max-width:880px){ .cell,.cell.w5,.cell.w4,.cell.w3,.cell.w7{grid-column:span 6} }
@media(max-width:560px){ .cell,.cell.w5,.cell.w4,.cell.w3,.cell.w7,.cell.w12{grid-column:span 12} }

.cell .row{display:flex; align-items:center; gap:24px; flex:1}
.cell .row.col{flex-direction:column; align-items:flex-start; gap:6px}
.cell .art{flex:none}
.cell .fig{flex:1; min-width:0}
.lab{font:700 14px/1.6 var(--jp); letter-spacing:.03em; margin-bottom:2px}
.lab.cy{color:var(--cy)} .lab.pk{color:var(--pk)} .lab.pu{color:var(--pu)}
.lab.or{color:var(--or)} .lab.tl{color:var(--tl)} .lab.cr{color:var(--cr)}
.big{font:300 clamp(56px,7.4vw,86px)/1 var(--num); color:#42444a; letter-spacing:-.015em; white-space:nowrap}
.big small{font:600 15.5px/1 var(--jp); color:#666b73; margin-left:7px; letter-spacing:.04em}
.note{font-size:13px; color:#6f7580; margin-top:7px; line-height:1.8}
.more{
  margin-top:auto; align-self:flex-end; text-decoration:none;
  font:600 11.5px/1 var(--num); letter-spacing:.1em; color:#969ba3; padding-top:14px;
}
.more::before{content:"＋ "; color:#c3c7cd}
.more:hover{color:var(--pk)}

/* ---------- sections ---------- */
section.blk{padding:76px 0 4px}
.shead{margin-bottom:34px; position:relative; padding-top:20px}
.shead::before{
  content:""; position:absolute; top:0; left:0; width:44px; height:3px;
  background:linear-gradient(90deg,var(--cy),var(--pk));
}
.shead .en{
  display:block; font:600 11.5px/1 var(--num); letter-spacing:.24em;
  text-transform:uppercase; color:#b7bcc4; margin-bottom:10px;
}
.shead h2{margin:0; font:500 clamp(26px,3.9vw,36px)/1.5 var(--jp); letter-spacing:.02em; color:var(--ink-strong)}
.shead p{margin:12px 0 0; font-size:15.5px; color:#5a5f68; max-width:700px}

/* compare */
.cmp{display:grid; grid-template-columns:1fr 1fr; gap:12px}
@media(max-width:700px){.cmp{grid-template-columns:1fr}}
.cmp>div{background:#fff; border:1px solid var(--line); padding:28px 28px 24px; position:relative}
.cmp>div::before{content:""; position:absolute; inset:0 0 auto 0; height:3px}
.cmp .x::before{background:linear-gradient(90deg,var(--cr),var(--pk))}
.cmp .o::before{background:linear-gradient(90deg,var(--cy),var(--tl))}
.cmp h3{margin:0 0 16px; font:700 15.5px/1.6 var(--jp); letter-spacing:.04em}
.cmp .x h3{color:var(--cr)} .cmp .o h3{color:#1fb2a6}
.cmp ul{margin:0; padding-left:1.1em; font-size:15px; color:#4c5058; line-height:2}
.cmp li{margin-bottom:7px}

/* two-col compare table */
.tbl{width:100%; border-collapse:collapse; background:#fff; border:1px solid var(--line)}
.tblwrap{overflow-x:auto}
.tbl th,.tbl td{padding:17px 20px; text-align:left; border-bottom:1px solid var(--line); font-size:15px; color:#4c5058; vertical-align:top}
.tbl thead th{background:#fafafb; font:700 12px/1 var(--num); letter-spacing:.14em; text-transform:uppercase; color:#8b919a}
.tbl tbody tr:last-child td{border-bottom:none}
.tbl td strong{color:var(--ink-strong)}
.tbl code{font:600 13.5px/1 var(--num); color:var(--pk); background:#fdf2f8; padding:2px 7px; border-radius:2px}
@media(max-width:640px){.tbl{min-width:520px}}

/* term cards */
.terms{display:grid; grid-template-columns:repeat(12,1fr); gap:12px}
.tcard{background:#fff; border:1px solid var(--line); padding:28px; grid-column:span 4; display:flex; flex-direction:column}
.tcard.wide{grid-column:span 6}
@media(max-width:880px){.tcard,.tcard.wide{grid-column:span 6}}
@media(max-width:560px){.tcard,.tcard.wide{grid-column:span 12}}
.tcard .ico{margin-bottom:16px}
.tcard .en2{font:600 11px/1 var(--num); letter-spacing:.2em; text-transform:uppercase; color:#a6acb5}
.tcard h3{margin:8px 0 12px; font:500 23px/1.45 var(--jp); color:var(--ink-strong); letter-spacing:.02em}
.tcard p{margin:0 0 12px; font-size:15px; color:#4c5058; line-height:2}
.tcard .an{margin:auto 0 0; padding-top:12px; border-top:1px dashed #e8e8ec; font-size:13.5px; color:#6f7580; line-height:1.85}

/* flow */
.flow{border-top:1px solid var(--line)}
.fstep{display:grid; grid-template-columns:76px 1fr; gap:0; border-bottom:1px solid var(--line); background:#fff}
.fstep .n{
  display:flex; align-items:center; justify-content:center;
  font:300 34px/1 var(--num); color:#fff; letter-spacing:0;
}
.fstep:nth-child(1) .n{background:linear-gradient(160deg,#2ec9e0,#3fd0bd)}
.fstep:nth-child(2) .n{background:linear-gradient(160deg,#35c3e6,#6aa8f0)}
.fstep:nth-child(3) .n{background:linear-gradient(160deg,#7b8bf2,#9163f2)}
.fstep:nth-child(4) .n{background:linear-gradient(160deg,#a45cf5,#f0399b)}
.fstep:nth-child(5) .n{background:linear-gradient(160deg,#f0399b,#ff6a8a)}
.fstep:nth-child(6) .n{background:linear-gradient(160deg,#ff6a6a,#ff8a3d)}
.fstep:nth-child(7) .n{background:linear-gradient(160deg,#ff9a3c,#ffc148)}
.fstep .txt{padding:22px 26px}
.fstep h4{margin:0 0 4px; font:700 16px/1.6 var(--jp); color:var(--ink-strong); letter-spacing:.02em}
.fstep p{margin:0; font-size:15px; color:#575c65}
.cmd{
  display:inline-block; margin-top:10px; font:600 13.5px/1.7 var(--num);
  background:#f7f7f9; border:1px solid var(--line); padding:5px 12px; color:#4b4d52;
}

/* myths */
.myths{display:grid; grid-template-columns:repeat(12,1fr); gap:12px}
.myth{background:#fff; border:1px solid var(--line); padding:26px 28px; grid-column:span 6}
@media(max-width:700px){.myth{grid-column:span 12}}
.myth .q{margin:0 0 10px; font:700 15.5px/1.7 var(--jp); color:var(--ink-strong)}
.myth .q i{font-style:normal; color:var(--pk); margin-right:8px; font:700 14px/1 var(--num); letter-spacing:.1em}
.myth .a{margin:0; font-size:15px; color:#4c5058; line-height:2}
.myth .a b{color:#1fb2a6}

/* steps list */
.startbox{background:#fff; border:1px solid var(--line); padding:34px 34px 28px}
.startbox ol{margin:0; padding:0; list-style:none; counter-reset:s}
.startbox li{
  counter-increment:s; position:relative; padding:0 0 22px 50px; font-size:15px; color:#4c5058; line-height:2;
}
.startbox li:last-child{padding-bottom:0}
.startbox li::before{
  content:counter(s,decimal-leading-zero); position:absolute; left:0; top:1px;
  font:700 13px/1.6 var(--num); letter-spacing:.06em; color:var(--pk);
}
.startbox li b{color:var(--ink-strong)}

/* figure */
.figwrap{background:#fff; border:1px solid var(--line); padding:30px 22px 22px; overflow-x:auto}
.figwrap svg{display:block; margin:0 auto; min-width:540px}
.figcap{text-align:center; font-size:13.5px; color:#6f7580; margin:16px 0 0}

/* cta */
.cta{position:relative; margin-top:88px; overflow:hidden; display:block; text-decoration:none}
.cta svg{position:absolute; inset:0; width:100%; height:100%}
.cta .in{
  position:relative; z-index:2; height:clamp(190px,22vw,260px);
  display:flex; align-items:center; justify-content:center; gap:26px;
}
.cta .t{font:300 clamp(32px,5.9vw,58px)/1 var(--num); letter-spacing:.3em; color:rgba(255,255,255,.95); padding-left:.3em}
.cta .ar{width:clamp(70px,11vw,130px); height:2px; background:rgba(255,255,255,.9); position:relative}
.cta .ar::after{
  content:""; position:absolute; right:0; top:-5px; width:12px; height:12px;
  border-top:2px solid rgba(255,255,255,.9); border-right:2px solid rgba(255,255,255,.9);
  transform:rotate(45deg);
}
.cta:hover .ar{width:clamp(90px,14vw,160px); transition:width .3s}

footer{background:#fff; border-top:1px solid var(--line)}
footer .bar{
  max-width:1120px; margin:0 auto; padding:22px 24px; display:flex; flex-wrap:wrap; gap:18px;
  font:600 12px/1.8 var(--jp); color:#969ba3; letter-spacing:.04em;
}
footer .bar .r{margin-left:auto; font-family:var(--num); letter-spacing:.06em}
"""


# 教科書固有の構造を正本CSSへ追加する。正本の宣言は上で保持する。
TEXTBOOK_CSS = r"""
html{scroll-behavior:smooth;scroll-padding-top:76px}
.tbl,.figwrap svg{min-width:0}
.sr-only{
  position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
  clip:rect(0,0,0,0);white-space:nowrap;border:0;
}
.skip-link{
  position:fixed;left:16px;top:-80px;z-index:80;padding:10px 16px;
  color:#fff;background:var(--ink-strong);text-decoration:none;
}
.skip-link:focus{top:10px}
.site .bar{min-width:0}
.brand{min-width:0}
.brand span{white-space:nowrap}
.site nav{min-width:0}
.btn-entry{white-space:nowrap}
.site nav + .btn-entry{margin-left:22px}
.hero .l1{letter-spacing:-.015em}
.hero .l2{font-family:var(--jp);letter-spacing:.08em}
.hero h1.l2{margin:0}
.lead{padding-bottom:16px}
.lead p{overflow-wrap:anywhere}
.dataarea{scroll-margin-top:72px}
.cell{min-width:0;box-shadow:0 14px 34px rgba(34,36,42,.055)}
.cell .row{min-width:0}
.cell .art{min-width:0}
.cell .art svg{display:block;max-width:100%;height:auto}
.cell .fig{max-width:100%}
.big{max-width:100%}
.numbers-title{margin:0 0 24px;font:500 clamp(24px,3.5vw,34px)/1.5 var(--jp);color:var(--ink-strong)}
.numbers-title span{display:block;margin-bottom:7px;font:600 11px/1 var(--num);letter-spacing:.23em;color:#a6acb5;text-transform:uppercase}
.toc-area{padding-top:76px;padding-bottom:54px}
.toc{margin:0;padding:0}
.toc .shead{margin-bottom:28px}
.toc ol{
  display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;
  margin:0;padding:0;list-style:none;
}
.toc li{min-width:0;margin:0}
.toc a{
  display:grid;grid-template-columns:46px minmax(0,1fr) auto;align-items:center;
  gap:14px;min-height:86px;padding:16px 18px;color:var(--ink-strong);
  background:#fff;border:1px solid var(--line);text-decoration:none;
  transition:border-color .18s ease,transform .18s ease,box-shadow .18s ease;
}
.toc a:hover,.toc a:focus-visible{
  border-color:var(--pk);transform:translateY(-2px);box-shadow:0 12px 24px rgba(240,57,155,.08);
}
.toc-number{
  display:grid;width:46px;height:46px;place-items:center;color:#fff;
  background:linear-gradient(145deg,var(--pu),var(--pk));
  font:300 22px/1 var(--num);
}
.toc-copy{min-width:0}
.toc-title{display:block;font-size:15px;font-weight:700;line-height:1.55}
.toc-time{font:600 12px/1 var(--num);color:var(--sub);white-space:nowrap}
.chapters-area{padding:68px 24px 20px;background:var(--bg-soft)}
.chapter{
  max-width:960px;min-width:0;margin:0 auto 28px;padding:0 0 42px;
  overflow:hidden;background:#fff;border:1px solid var(--line);
  box-shadow:0 18px 52px rgba(34,36,42,.06);
}
.chapter-header{
  display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:center;
  gap:18px;margin:0 0 38px;padding:26px 34px;color:#fff;
  background:linear-gradient(96deg,#2ec9e0 0%,#48c8d8 19%,#9163f2 43%,#f0399b 63%,#ff7a5c 83%,#ffb03c 100%);
  font:500 clamp(23px,3.4vw,34px)/1.45 var(--jp);letter-spacing:.02em;
}
.chapter-number{
  display:grid;width:52px;height:52px;place-items:center;flex:none;
  border:1px solid rgba(255,255,255,.72);color:rgba(255,255,255,.9);
  font:300 26px/1 var(--num);
}
.chapter-title{min-width:0}
.chapter-time{
  padding:7px 10px;border:1px solid rgba(255,255,255,.64);
  background:rgba(255,255,255,.12);font:600 12px/1 var(--num);white-space:nowrap;
}
.chapter>section{max-width:800px;margin:32px auto 0;padding:0 34px;min-width:0}
.chapter>section h3{
  position:relative;margin:0 0 15px;padding-top:18px;
  font:500 clamp(21px,3vw,27px)/1.5 var(--jp);color:var(--ink-strong);
}
.chapter>section h3::before{
  content:"";position:absolute;top:0;left:0;width:40px;height:3px;
  background:linear-gradient(90deg,var(--cy),var(--pk));
}
.chapter p,.chapter ol,.chapter ul,.chapter blockquote,.copy-block{max-width:720px}
.chapter p{margin:10px 0;line-height:2;overflow-wrap:anywhere}
.chapter ol,.chapter ul{margin:14px 0;padding-left:1.55em}
.chapter li{margin:7px 0;line-height:1.95}
.chapter strong{color:var(--ink-strong)}
.chapter p code,.chapter li code{
  padding:2px 6px;color:var(--pk);background:#fdf2f8;border-radius:2px;
  font:600 13.5px/1.7 var(--num);overflow-wrap:anywhere;
}
.section-goal,.section-check,.section-qa,.section-glossary{
  padding-top:26px!important;padding-bottom:24px!important;border:1px solid var(--line);
}
.section-goal{background:#f3fcfd;border-top:3px solid var(--cy)!important}
.section-check{background:#f4fcfa;border-top:3px solid var(--tl)!important}
.section-qa{background:#fdf5fa;border-top:3px solid var(--pk)!important}
.section-glossary{background:#f7f4fe;border-top:3px solid var(--pu)!important}
.section-analogy{padding-bottom:6px!important}
.section-steps>ol{
  padding:0;list-style:none;counter-reset:step var(--step-start,0);
}
.section-steps>ol>li{
  display:grid;grid-template-columns:38px minmax(0,1fr);align-items:start;
  gap:12px;padding:6px 0;counter-increment:step;
}
.section-steps>ol>li::before{
  content:counter(step,decimal-leading-zero);display:grid;width:34px;height:34px;
  place-items:center;margin-top:2px;color:#fff;background:linear-gradient(145deg,var(--pu),var(--pk));
  font:600 11px/1 var(--num);letter-spacing:.04em;
}
.copy-block{
  width:100%;min-width:0;margin:18px 0 22px;overflow:hidden;
  color:#f7f8fb;background:#171923;border:1px solid #333744;
  box-shadow:0 13px 30px rgba(23,25,35,.13);
}
.copy-label{
  display:block;padding:8px 14px;color:#ffd4ec;background:#242633;
  border-bottom:1px solid #393c49;font:700 12px/1.6 var(--jp);letter-spacing:.04em;
}
pre{max-width:100%;margin:0;padding:18px;overflow-x:auto;white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word}
pre code{font:500 14px/1.8 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
blockquote{margin:20px 0;padding:18px 20px}
blockquote p{margin:5px 0!important}
blockquote.note{font-size:15px;background:#fff8e8;border-left:4px solid var(--or)}
blockquote.safety-note{
  position:relative;max-width:720px;padding:24px 26px;color:#fff;
  background:#10121b;border:3px solid var(--pk);
  box-shadow:0 18px 42px rgba(16,18,27,.28),inset 0 0 0 1px rgba(255,255,255,.05);
}
blockquote.safety-note::before{
  content:"CHECK THE DARK SCREEN";display:block;margin-bottom:13px;
  color:var(--cy);font:700 10px/1 var(--num);letter-spacing:.2em;
}
blockquote.safety-note p{color:#f6f7fb}
blockquote.safety-note p:first-child{font-size:19px;line-height:1.55}
blockquote.safety-note strong{color:#ff9dce}
.cta{
  background:linear-gradient(96deg,#2ec9e0 0%,#48c8d8 19%,#9163f2 43%,#f0399b 63%,#ff7a5c 83%,#ffb03c 100%);
}
.cta:focus-visible{outline:4px solid var(--ink-strong);outline-offset:-8px}
footer .bar{align-items:center}

/* ---------- Z5 media, materials, and concept diagrams ---------- */
.worldview,.intro-video{padding:64px 24px 8px;background:var(--bg-soft)}
.worldview .inner,.intro-video .inner{max-width:960px;min-width:0;margin:0 auto}
.worldview .shead,.intro-video .shead{margin-bottom:22px}
.worldview .lesson-figure{max-width:960px;margin:0}
.intro-video video{display:block;width:100%;height:auto;background:#10121b;border:1px solid var(--line)}
.intro-video .sound-note{margin:10px 0 0;color:var(--sub);font-size:13px}
.lesson-figure{
  width:100%;min-width:0;max-width:720px;margin:24px 0 8px;padding:14px;
  background:#fff;border:1px solid var(--line);box-shadow:0 14px 34px rgba(34,36,42,.07);
}
.lesson-figure img{display:block;width:100%;height:auto;object-fit:contain;background:#f8f8fa}
.lesson-figure figcaption{padding:12px 8px 1px;color:var(--sub);font-size:13.5px;line-height:1.8}
.material-download{
  max-width:720px;min-width:0;margin:0 0 24px;padding:18px;
  background:#f5f2fe;border:1px solid #e6defb;border-left:4px solid var(--pu);
}
.material-download a,.materials-bundle{
  display:inline-flex;align-items:center;gap:8px;padding:12px 16px;color:#fff;
  background:linear-gradient(100deg,var(--pu),var(--pk));text-decoration:none;
  font-size:14px;font-weight:700;line-height:1.4;box-shadow:0 9px 20px rgba(145,99,242,.18);
}
.material-download a:hover,.materials-bundle:hover{transform:translateY(-1px)}
.material-download p{margin:9px 0 0!important;color:#646977;font-size:13px;line-height:1.7}
.materials-bundle{margin-top:18px;background:linear-gradient(100deg,var(--cy),var(--pu))}
.chapter-achievement{
  display:grid;grid-template-columns:42px minmax(0,1fr);align-items:center;gap:14px;
  max-width:800px;min-width:0;margin:34px auto 0;padding:18px 34px;
  background:linear-gradient(100deg,#effcfd,#f8f1fc);border:1px solid #dceff2;
}
.chapter-achievement>span{display:grid;width:36px;height:36px;place-items:center;color:#fff;background:var(--tl);border-radius:50%;font-weight:800}
.chapter-achievement p{margin:0!important;font-size:14px;line-height:1.75}
.chapter-achievement strong{display:block;margin-bottom:2px;color:#169e93!important;font-size:12px;letter-spacing:.04em}
.toc-goal{display:block;min-width:0;margin-top:4px;overflow:hidden;color:var(--sub);font-size:12.5px;font-weight:500;line-height:1.5;text-overflow:ellipsis;white-space:nowrap}

.concept-diagram{
  width:100%;min-width:0;max-width:720px;margin:26px 0 12px;padding:24px;
  overflow:hidden;background:#fff;border:1px solid var(--line);box-shadow:0 14px 34px rgba(34,36,42,.07);
}
.concept-diagram>figcaption{margin-bottom:20px;color:var(--ink-strong);font-size:18px;font-weight:700;line-height:1.5}
.concept-diagram>figcaption span{display:block;margin-bottom:5px;color:var(--pk);font:700 10px/1 var(--num);letter-spacing:.2em}
.diagram-graphic{width:100%;min-width:0}
.diagram-graphic svg{display:block;width:100%;height:auto;fill:none;stroke:currentColor;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}
.diagram-note{margin:17px 0 0!important;color:var(--sub);font-size:13.5px;line-height:1.8}

.desk-relation{display:grid;grid-template-columns:minmax(0,1fr) 80px minmax(0,1fr);align-items:center;gap:12px}
.diagram-node{min-width:0;padding:18px;text-align:center;background:#fbfbfc;border:1px solid var(--line)}
.diagram-node svg{width:112px;max-width:100%;margin:0 auto 10px}
.diagram-node.cy{color:var(--cy);border-top:3px solid var(--cy)}
.diagram-node.pk{color:var(--pk);border-top:3px solid var(--pk)}
.diagram-node b,.diagram-node span{display:block;color:var(--ink-strong)}
.diagram-node span{margin-top:4px;color:var(--sub);font-size:12.5px;line-height:1.6}
.relation-arrow{color:var(--pu)}

.four-flow{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.flow-node{position:relative;min-width:0;padding:15px 10px;text-align:center;background:#fbfbfc;border-top:3px solid currentColor}
.flow-node:not(:last-child)::after{content:"›";position:absolute;z-index:2;right:-10px;top:48%;color:#b7bcc4;font-size:25px;line-height:1}
.flow-node.cy{color:var(--cy)}.flow-node.tl{color:var(--tl)}.flow-node.pu{color:var(--pu)}.flow-node.or{color:var(--or)}
.flow-node svg{width:62px;max-width:100%;margin:4px auto 8px}
.flow-number{display:block;color:currentColor;font:600 10px/1 var(--num);letter-spacing:.13em;text-align:left}
.flow-node b,.flow-node small{display:block;color:var(--ink-strong)}
.flow-node b{font-size:14px;line-height:1.5}.flow-node small{margin-top:3px;color:var(--sub);font-size:11.5px;line-height:1.45}

.dark-diagram{color:#fff;background:#10121b;border:3px solid var(--pk);box-shadow:0 18px 42px rgba(16,18,27,.24)}
.dark-diagram>figcaption{color:#fff}.dark-diagram>figcaption span{color:var(--cy)}
.permission-flow{display:grid;grid-template-columns:minmax(100px,.8fr) minmax(210px,1.5fr) 80px minmax(120px,.9fr);align-items:center;gap:12px}
.permission-start{min-width:0;padding:15px;color:var(--cy);text-align:center;border:1px solid #3d4558}
.permission-start svg{max-width:76px;margin:0 auto 8px}.permission-start b{display:block;color:#fff;font-size:13px}
.check-stack,.decision-stack{display:grid;min-width:0;gap:8px}
.check-stack>div{display:grid;grid-template-columns:28px minmax(0,1fr);align-items:center;gap:8px;padding:9px;background:#1c1f2b;border:1px solid #343847}
.check-stack>div>span{display:grid;width:26px;height:26px;place-items:center;color:#fff;background:var(--pu);font:700 11px/1 var(--num);border-radius:50%}
.check-stack p{margin:0!important;color:#dfe2ea;font-size:11.5px;line-height:1.45}.check-stack b{display:block;color:#fff;font-size:12px}
.branch-lines{color:#9da4b4;height:120px}
.decision-stack>div{padding:13px;text-align:center;border:1px solid}.decision-stack b,.decision-stack span{display:block}.decision-stack b{font-size:12px}.decision-stack span{font-size:11px}
.decision-ok{color:#55d9c6;background:#102a29;border-color:#2e9589!important}.decision-stop{color:#ff8fc9;background:#32162a;border-color:#ad3c7a!important}

.history-cycle{position:relative;min-height:300px}
.cycle-ring{position:absolute;inset:22px 9%;width:82%!important;color:#c3b2f5}
.cycle-ring>path{marker-end:url(#cycle-arrow)}
.cycle-ring marker path{fill:#9163f2;stroke:none}
.cycle-node{position:absolute;display:grid;width:142px;min-width:0;place-items:center;padding:12px;background:#fff;border:1px solid var(--line);box-shadow:0 10px 24px rgba(34,36,42,.08)}
.cycle-node>span{justify-self:start;color:currentColor;font:700 10px/1 var(--num);letter-spacing:.12em}.cycle-node svg{width:58px;margin:3px auto}.cycle-node b{color:var(--ink-strong);font-size:13.5px}
.cycle-node.change{left:0;top:72px;color:var(--cy);border-top:3px solid var(--cy)}
.cycle-node.notice{right:0;top:72px;color:var(--pk);border-top:3px solid var(--pk)}
.cycle-node.restore{left:calc(50% - 71px);bottom:0;color:var(--pu);border-top:3px solid var(--pu)}

@media (max-width: 760px){
  .site nav+ .btn-entry,.site nav + .btn-entry{margin-left:auto}
  .hero .l2{font-size:clamp(38px,11vw,50px);letter-spacing:.045em}
  .toc ol{grid-template-columns:minmax(0,1fr)}
  .chapter-header{gap:12px;padding:22px 20px}
  .chapter-number{width:44px;height:44px;font-size:21px}
  .chapter>section{margin-left:18px;margin-right:18px;padding-left:22px;padding-right:22px}
  .four-flow{grid-template-columns:repeat(2,minmax(0,1fr))}
  .flow-node:nth-child(2)::after{display:none}
  .permission-flow{grid-template-columns:minmax(0,1fr)}
  .diagram-graphic svg.branch-lines{display:none}
  .decision-stack{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width: 640px){
  html{scroll-padding-top:92px}
  .site .bar{height:auto;min-height:64px;padding:10px 14px;gap:8px;flex-wrap:wrap}
  .mark{width:30px;height:30px;font-size:11px}
  .brand{font-size:12.5px}
  .brand span{font-size:9.5px;letter-spacing:.12em}
  .btn-entry{padding:10px 12px;font-size:10.5px;letter-spacing:.08em}
  .hero .kicker b{font-size:14px;letter-spacing:.08em}
  .hero .l1{font-size:clamp(42px,13vw,58px)}
  .dataarea{padding-top:36px}
  .cell{padding:26px 22px 20px;min-height:230px}
  .cell .row{gap:18px}
  .cell .art svg{width:104px}
  .big{font-size:clamp(54px,20vw,76px)}
  .toc-area{padding-top:60px}
  .toc a{grid-template-columns:40px minmax(0,1fr) auto;gap:10px;padding:13px}
  .toc-number{width:40px;height:40px;font-size:19px}
  .toc-title{font-size:14px}
  .chapters-area{padding:48px 12px 10px}
  .chapter{margin-bottom:22px;padding-bottom:30px}
  .chapter-header{grid-template-columns:auto minmax(0,1fr) auto;font-size:21px}
  .chapter-time{padding:6px 7px;font-size:10px}
  .chapter>section{margin-top:26px;margin-left:12px;margin-right:12px;padding-left:16px;padding-right:16px}
  .chapter>section h3{font-size:20px}
  .chapter-achievement{margin-left:12px;margin-right:12px;padding:16px;grid-template-columns:34px minmax(0,1fr)}
  .chapter-achievement>span{width:32px;height:32px}
  .worldview,.intro-video{padding:48px 12px 4px}
  .lesson-figure{padding:9px}
  .concept-diagram{padding:18px 14px}
  .desk-relation{grid-template-columns:minmax(0,1fr)}
  .relation-arrow{width:64px!important;margin:0 auto;transform:rotate(90deg)}
  .four-flow{grid-template-columns:minmax(0,1fr)}
  .flow-node:not(:last-child)::after{display:none}
  .history-cycle{display:grid;min-height:0;gap:10px}
  .diagram-graphic svg.cycle-ring{display:none}
  .cycle-node{position:static;width:100%}
  .section-steps>ol>li{grid-template-columns:34px minmax(0,1fr);gap:9px}
  .section-steps>ol>li::before{width:31px;height:31px}
  blockquote.safety-note{padding:20px 17px}
  .cta .in{height:180px;gap:15px}
  .cta .t{font-size:30px;letter-spacing:.17em}
}
@media print{
  .site,.skip-link,.cta{display:none}
  .chapter{break-inside:avoid;box-shadow:none}
}
"""


def number_grid() -> str:
    """Render only source-backed figures from the textbook itself."""
    return """<section class="dataarea" id="numbers" aria-labelledby="numbers-title">
  <div class="wrap">
    <h2 class="numbers-title" id="numbers-title"><span>Textbook in numbers</span>数字でみる超入門教科書</h2>
    <div class="grid">
      <article class="cell w5">
        <div class="row">
          <div class="art">
            <svg width="128" height="104" viewBox="0 0 128 104" aria-hidden="true">
              <g fill="none" stroke="#2ec9e0" stroke-width="3">
                <path d="M8 14h46v32H8zM74 14h46v32H74zM8 59h46v32H8zM74 59h46v32H74z"/>
                <path d="M18 24h26M18 33h18M84 24h26M84 33h18M18 69h26M18 78h18M84 69h26M84 78h18" stroke-linecap="round"/>
              </g>
            </svg>
          </div>
          <div class="fig">
            <div class="lab cy">教科書の構成</div>
            <div class="big">14<small>章</small></div>
            <div class="note">第0章〜第12章と終章。目次と原稿の章見出しに基づきます。</div>
          </div>
        </div>
        <a class="more" href="#toc-title">目次を見る</a>
      </article>
      <article class="cell w7">
        <div class="row">
          <div class="art">
            <svg width="150" height="106" viewBox="0 0 150 106" aria-hidden="true">
              <g fill="none" stroke="#f0399b" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 18h24v24H12zM12 64h24v24H12zM82 18h24v24H82zM82 64h24v24H82z"/>
                <path d="M18 29l6 6 13-15M18 75l6 6 13-15M88 29l6 6 13-15M88 75l6 6 13-15"/>
              </g>
            </svg>
          </div>
          <div class="fig">
            <div class="lab pk">安全の約束</div>
            <div class="big">4<small>つ</small></div>
            <div class="note">練習用コピー・秘密を貼らない・危険な操作前に止まる・成果物と証拠で確認。</div>
          </div>
        </div>
        <a class="more" href="#zch-04">第4章へ</a>
      </article>
      <article class="cell w7">
        <div class="row">
          <div class="art">
            <svg width="150" height="106" viewBox="0 0 150 106" aria-hidden="true">
              <path d="M8 12h134v82H8z" fill="#f4f1ff" stroke="#9163f2" stroke-width="3"/>
              <path d="M8 12h134v20H8z" fill="#9163f2"/>
              <g fill="#9163f2"><circle cx="33" cy="52" r="9"/><circle cx="75" cy="52" r="9"/><circle cx="117" cy="52" r="9"/></g>
              <g stroke="#9163f2" stroke-width="4" stroke-linecap="round"><path d="M20 76h26M62 76h26M104 76h26"/></g>
            </svg>
          </div>
          <div class="fig">
            <div class="lab pu">黒画面で見るポイント</div>
            <div class="big">3<small>点</small></div>
            <div class="note">危険な行動の有無・対象の場所・不安なら許可しない、の3点だけを確認します。</div>
          </div>
        </div>
        <a class="more" href="#zch-04-s3">確認方法へ</a>
      </article>
      <article class="cell w5">
        <div class="row">
          <div class="art">
            <svg width="128" height="104" viewBox="0 0 128 104" aria-hidden="true">
              <path d="M8 14h112v76H8z" fill="#fff3ea" stroke="#ff8a3d" stroke-width="3"/>
              <path d="M8 14h112v18H8z" fill="#ff8a3d"/>
              <path d="M25 51l10 9-10 9M47 70h41" fill="none" stroke="#ff8a3d" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="fig">
            <div class="lab or">覚えるコマンド</div>
            <div class="big">0<small>行</small></div>
            <div class="note">原稿は「コードを1行も書きません」と明記。枠内の依頼文をコピーして進めます。</div>
          </div>
        </div>
        <a class="more" href="#zch-00-s3">進め方へ</a>
      </article>
    </div>
  </div>
</section>"""


def hero() -> str:
    """Render the two-level vivid hero with a CSS band and SVG chevrons."""
    return """<div class="hero">
  <div class="bandbg"></div>
  <svg class="bgart" viewBox="0 0 1200 530" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
    <defs>
      <linearGradient id="gcy" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#39d6ea"/><stop offset="1" stop-color="#48d8bd"/></linearGradient>
      <linearGradient id="gpk" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f0399b"/><stop offset="1" stop-color="#a45cf5"/></linearGradient>
      <linearGradient id="gor" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffb03c"/><stop offset="1" stop-color="#ff5f8f"/></linearGradient>
      <linearGradient id="gwt" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".95"/><stop offset="1" stop-color="#ffffff" stop-opacity=".45"/></linearGradient>
      <linearGradient id="gtop" x1="0" y1="0" x2="1" y2=".4"><stop offset="0" stop-color="#2ec9e0" stop-opacity="0"/><stop offset=".5" stop-color="#9163f2" stop-opacity=".16"/><stop offset="1" stop-color="#ff8a3d" stop-opacity=".22"/></linearGradient>
      <path id="cv" d="M0 0H72L136 66 72 132H0L64 66Z"/>
    </defs>
    <path d="M330-40h900v300H330z" fill="url(#gtop)"/>
    <use href="#cv" transform="translate(452,-46) scale(2.35)" fill="url(#gcy)" opacity=".9"/>
    <use href="#cv" transform="translate(700,-70) scale(1.75)" fill="url(#gpk)" opacity=".55" style="mix-blend-mode:multiply"/>
    <use href="#cv" transform="translate(880,-20) scale(1.35)" fill="url(#gor)" opacity=".5"/>
    <use href="#cv" transform="translate(320,96) scale(.78)" fill="url(#gcy)" opacity=".55"/>
    <use href="#cv" transform="translate(196,206) scale(2.9)" fill="url(#gwt)" opacity=".34"/>
    <use href="#cv" transform="translate(560,150) scale(2.5)" fill="url(#gor)" opacity=".45" style="mix-blend-mode:screen"/>
    <use href="#cv" transform="translate(742,232) scale(1.5)" fill="#fff" opacity=".22"/>
    <use href="#cv" transform="translate(286,300) scale(.66)" fill="#fff" opacity=".55"/>
    <use href="#cv" transform="translate(1004,168) scale(1.15)" fill="url(#gcy)" opacity=".38" style="mix-blend-mode:screen"/>
    <path d="M330 352h130M520 30h120" fill="none" stroke="#fff" stroke-width="3" opacity=".7"/>
  </svg>
  <div class="hrow htop">
    <div class="in2">
      <div class="kicker"><b>読む・頼む・確かめる</b></div>
      <span class="l1">Claude Code</span>
    </div>
  </div>
  <div class="hrow hband">
    <div class="in2"><h1 class="l2" id="page-title"><span class="sr-only">Claude Code </span>超入門教科書</h1></div>
  </div>
</div>"""


def cover_section(directives: dict[str, tuple[str, str]]) -> str:
    image_path = IMAGES_DIR / "cover-zero.webp"
    metadata = directives.get("cover-zero")
    if not image_path.is_file() or metadata is None:
        return ""
    alt, caption = metadata
    return f"""<section class="worldview" aria-labelledby="worldview-title">
  <div class="inner">
    <div class="shead">
      <span class="en">Visual story</span>
      <h2 id="worldview-title">この教科書の世界観</h2>
      <p>仕事机と新人アシスタントの関係を、1枚の絵で見渡します。</p>
    </div>
    <figure class="lesson-figure" data-image-id="cover-zero">
      <img loading="lazy" decoding="async" src="images/cover-zero.webp" alt="{html.escape(alt, quote=True)}">
      <figcaption>{render_inline(caption)}</figcaption>
    </figure>
  </div>
</section>"""


def video_section() -> str:
    if not INTRO_VIDEO.is_file():
        return ""
    return """<section class="intro-video" aria-labelledby="intro-video-title">
  <div class="inner">
    <div class="shead">
      <span class="en">3 minute overview</span>
      <h2 id="intro-video-title">動画でざっくり知る（3分）</h2>
    </div>
    <video controls preload="none">
      <source src="videos/intro.mp4" type="video/mp4">
      お使いの環境では動画を再生できません。
    </video>
    <p class="sound-note">※ 音が出ます。</p>
  </div>
</section>"""


def page_template(
    chapters: list[tuple[str, str]],
    goals: dict[str, str],
    directives: dict[str, tuple[str, str]],
    body: str,
) -> str:
    toc_items = "\n".join(
        render_toc_item(chapter_id, title, goals[chapter_id])
        for chapter_id, title in chapters
    )
    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="画面操作が初めてでも進められるClaude Code超入門教科書">
  <title>Claude Code 超入門教科書</title>
  <style>
{BASE_CSS}
{TEXTBOOK_CSS}
  </style>
</head>
<body>
  <a class="skip-link" href="#main-content">本文へ移動</a>
  <header class="site">
    <div class="bar">
      <div class="mark" aria-hidden="true">CC</div>
      <div class="brand">Claude Code 超入門<span>Zero Beginner Textbook</span></div>
      <nav aria-label="ページ内ナビゲーション">
        <a href="#numbers">数字で見る</a>
        <a href="#toc-title">目次</a>
        <a href="#zch-04">安全の約束</a>
      </nav>
      <a class="btn-entry" href="../../cc-v2/claude-code-blog-experiential-edition/site/complete.html" target="_blank" rel="noopener">本編（実践教科書）へ</a>
    </div>
  </header>
{hero()}
{video_section()}
{cover_section(directives)}
  <div class="lead">
    <p>コードを書かずに、<b>読む・頼む・確かめる</b>を順番に練習します。<br>1章ずつ、自分のペースで進められます。</p>
  </div>
  <main id="main-content">
    {number_grid()}
    <section class="toc-area wrap">
      <nav class="toc" aria-labelledby="toc-title">
        <div class="shead">
          <span class="en">Table of contents</span>
          <h2 id="toc-title">目次</h2>
          <p>PCでは2列、スマートフォンでは1列で表示します。章ごとの時間は原稿の見出しに基づきます。</p>
          <a class="materials-bundle" download href="materials/教材ぜんぶ入り.zip"><span aria-hidden="true">🗂️</span> 教材をまとめてダウンロード</a>
        </div>
        <ol>
          {toc_items}
        </ol>
      </nav>
    </section>
    <div class="chapters-area">
      {body}
    </div>
  </main>
  <a class="cta" href="#zch-00">
    <span class="in"><span class="t">START</span><span class="ar"></span></span>
  </a>
  <footer>
    <div class="bar"><span>Claude Code 超入門教科書</span><span class="r">Zero Beginner Textbook</span></div>
  </footer>
</body>
</html>
"""


def main() -> int:
    try:
        markdown = SOURCE.read_text(encoding="utf-8")
        chapters = collect_chapters(markdown)
        if not chapters:
            raise BuildError("no chapter headings found")
        goals = collect_chapter_goals(markdown)
        missing_goals = [chapter_id for chapter_id, _ in chapters if chapter_id not in goals]
        if missing_goals:
            raise BuildError(f"missing chapter goals: {missing_goals!r}")
        directives = collect_image_directives(markdown)
        materials = write_materials(markdown)
        body = render_markdown(markdown, goals)
        document = page_template(chapters, goals, directives, body)
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(document, encoding="utf-8")
    except (OSError, BuildError) as error:
        print(f"BUILD FAIL: {error}", file=sys.stderr)
        return 1

    print(f"BUILD PASS: {SOURCE.relative_to(ROOT)} -> {OUTPUT.relative_to(ROOT)}")
    print(f"chapters: {len(chapters)}")
    integrated_images = sorted(
        image_id
        for image_id in directives
        if (IMAGES_DIR / f"{image_id}.webp").is_file()
    )
    print(f"images integrated: {len(integrated_images)}")
    print(f"materials generated: {len(materials)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
