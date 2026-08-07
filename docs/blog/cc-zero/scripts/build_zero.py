#!/usr/bin/env python3
"""Build the standalone Claude Code zero-beginner textbook page."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources" / "zero-textbook.md"
OUTPUT = ROOT / "site" / "index.html"

HEADING_RE = re.compile(
    r"^(#{1,6})\s+(.+?)\s+\{#([A-Za-z][A-Za-z0-9_.:-]*)\}\s*$"
)
ANY_HEADING_RE = re.compile(r"^#{1,6}\s+")
CHAPTER_ID_RE = re.compile(r"^zch-(?:\d{2}|final)$")
ORDERED_ITEM_RE = re.compile(r"^(\d+)\.\s+(.+)$")
UNORDERED_ITEM_RE = re.compile(r"^[-*]\s+(.+)$")


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


def render_markdown(markdown: str) -> str:
    lines = strip_comments(markdown).splitlines()
    rendered: list[str] = []
    seen_ids: set[str] = set()
    chapter_open = False
    index = 0

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
                if chapter_open:
                    rendered.append("</section>")
                rendered.append(
                    f'<section class="chapter" aria-labelledby="{heading_id}">'
                )
                rendered.append(f'<h2 id="{heading_id}">{render_inline(title)}</h2>')
                chapter_open = True
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
            quote_text = "\n".join(quote_lines)
            if "画像制作指示：" in quote_text:
                quote_class = "production-note"
            elif "読めない黒い文字が出たら" in quote_text:
                quote_class = "safety-note"
            else:
                quote_class = "note"
            rendered.append(f'<blockquote class="{quote_class}">')
            for quote_line in quote_lines:
                if quote_line:
                    rendered.append(f"<p>{render_inline(quote_line)}</p>")
            rendered.append("</blockquote>")
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
            rendered.append(f"<ol{start_attribute}>")
            rendered.extend(f"<li>{render_inline(item)}</li>" for item in items)
            rendered.append("</ol>")
            continue

        unordered_item = UNORDERED_ITEM_RE.match(line)
        if unordered_item:
            items = []
            while index < len(lines):
                item_match = UNORDERED_ITEM_RE.match(lines[index])
                if item_match is None:
                    break
                items.append(item_match.group(1))
                index += 1
            rendered.append("<ul>")
            rendered.extend(f"<li>{render_inline(item)}</li>" for item in items)
            rendered.append("</ul>")
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

    if chapter_open:
        rendered.append("</section>")
    return "\n".join(rendered)


def page_template(chapters: list[tuple[str, str]], body: str) -> str:
    toc_items = "\n".join(
        f'<li><a href="#{chapter_id}">{render_inline(title)}</a></li>'
        for chapter_id, title in chapters
    )
    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="画面操作が初めてでも進められるClaude Code超入門教科書">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%230b1f33'/%3E%3Cpath d='M18 32h28M32 18v28' stroke='%23f6c76b' stroke-width='6'/%3E%3C/svg%3E">
  <title>Claude Code 超入門教科書</title>
  <style>
    :root {{
      --navy-950: #081827;
      --navy-900: #0b1f33;
      --navy-800: #17354f;
      --ivory: #fff8e7;
      --ivory-deep: #f4ead2;
      --amber: #d9911b;
      --amber-light: #f6c76b;
      --ink: #17212b;
      --muted: #5c6570;
      --line: #d9cdb4;
      --white: #ffffff;
    }}

    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; scroll-padding-top: 5.5rem; }}
    body {{
      margin: 0;
      min-width: 0;
      overflow-x: hidden;
      color: var(--ink);
      background: var(--ivory);
      font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans",
        "Yu Gothic", "YuGothic", "Noto Sans JP", sans-serif;
      line-height: 1.85;
      word-break: normal;
      overflow-wrap: anywhere;
    }}
    a {{ color: #8a5200; text-underline-offset: 0.18em; }}
    a:focus-visible {{ outline: 3px solid var(--amber); outline-offset: 3px; }}
    .skip-link {{
      position: absolute;
      left: 1rem;
      top: -5rem;
      z-index: 20;
      padding: 0.65rem 0.9rem;
      color: var(--navy-950);
      background: var(--amber-light);
      border-radius: 0.4rem;
    }}
    .skip-link:focus {{ top: 0.75rem; }}
    .site-header {{
      position: sticky;
      top: 0;
      z-index: 10;
      background: rgba(8, 24, 39, 0.97);
      border-bottom: 1px solid rgba(246, 199, 107, 0.45);
    }}
    .header-inner {{
      width: min(72rem, calc(100% - 2rem));
      margin: 0 auto;
      min-height: 4.25rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
    }}
    .brand {{ color: var(--white); font-weight: 750; letter-spacing: 0.02em; }}
    .main-book-link {{
      flex: 0 1 auto;
      color: var(--amber-light);
      font-weight: 700;
      text-align: right;
    }}
    .hero {{
      color: var(--white);
      background:
        radial-gradient(circle at 82% 15%, rgba(217, 145, 27, 0.24), transparent 30rem),
        linear-gradient(145deg, var(--navy-950), var(--navy-800));
      border-bottom: 0.35rem solid var(--amber);
    }}
    .hero-inner {{ width: min(64rem, calc(100% - 2rem)); margin: 0 auto; padding: 4rem 0 3.5rem; }}
    .eyebrow {{ margin: 0 0 0.65rem; color: var(--amber-light); font-weight: 750; letter-spacing: 0.08em; }}
    .hero h1 {{ margin: 0; max-width: 18ch; font-size: clamp(2rem, 7vw, 4.3rem); line-height: 1.15; }}
    .lead {{ max-width: 39rem; margin: 1.25rem 0 0; color: #f7f0df; font-size: clamp(1rem, 2.4vw, 1.2rem); }}
    .layout {{ width: min(72rem, calc(100% - 2rem)); margin: 0 auto; padding: 2rem 0 5rem; }}
    .toc {{
      margin: 0 0 2rem;
      padding: clamp(1.1rem, 4vw, 2rem);
      background: var(--white);
      border: 1px solid var(--line);
      border-top: 0.32rem solid var(--amber);
      border-radius: 0.8rem;
      box-shadow: 0 0.5rem 1.5rem rgba(8, 24, 39, 0.08);
    }}
    .toc h2 {{ margin: 0 0 0.8rem; color: var(--navy-900); font-size: 1.35rem; }}
    .toc ol {{ columns: 2; column-gap: 2rem; margin: 0; padding-left: 1.5rem; }}
    .toc li {{ break-inside: avoid; margin: 0.25rem 0; }}
    .chapter {{
      margin: 1.4rem 0;
      padding: clamp(1.1rem, 4vw, 2.5rem);
      background: rgba(255, 255, 255, 0.88);
      border: 1px solid var(--line);
      border-radius: 0.8rem;
    }}
    .chapter > h2 {{
      margin: 0 0 1.7rem;
      padding-bottom: 0.85rem;
      color: var(--navy-900);
      border-bottom: 0.2rem solid var(--amber);
      font-size: clamp(1.55rem, 4vw, 2.15rem);
      line-height: 1.4;
    }}
    .chapter h3 {{ margin: 2.2rem 0 0.7rem; color: var(--navy-800); font-size: 1.25rem; line-height: 1.5; }}
    .chapter p {{ max-width: 46rem; margin: 0.7rem 0; }}
    .chapter li {{ margin: 0.45rem 0; padding-left: 0.25rem; }}
    .chapter ol, .chapter ul {{ max-width: 46rem; padding-left: 1.55rem; }}
    .copy-block {{
      width: 100%;
      max-width: 46rem;
      margin: 1rem 0 1.3rem;
      overflow: hidden;
      color: #f8f4e8;
      background: var(--navy-950);
      border: 1px solid #25465f;
      border-radius: 0.65rem;
    }}
    .copy-label {{ display: block; padding: 0.5rem 0.85rem; color: var(--amber-light); background: #102b43; font-size: 0.82rem; font-weight: 750; }}
    pre {{ margin: 0; max-width: 100%; padding: 1rem; white-space: pre-wrap; overflow-wrap: anywhere; word-break: break-word; overflow-x: auto; }}
    pre code {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.94rem; }}
    p code, li code {{ padding: 0.08rem 0.3rem; background: var(--ivory-deep); border-radius: 0.25rem; }}
    blockquote {{ max-width: 46rem; margin: 1.2rem 0; padding: 1rem 1.1rem; border-radius: 0.55rem; }}
    blockquote p {{ margin: 0.32rem 0 !important; }}
    .production-note {{ color: #38414b; background: #f3efe5; border-left: 0.32rem solid #8a7350; }}
    .safety-note {{ color: #f7f3e8; background: #111820; border: 2px solid var(--amber); box-shadow: 0 0.6rem 1.4rem rgba(8, 24, 39, 0.18); }}
    .safety-note strong {{ color: var(--amber-light); }}
    .note {{ background: #fff1cf; border-left: 0.32rem solid var(--amber); }}
    .site-footer {{ padding: 2rem 1rem; color: #dfe7ec; text-align: center; background: var(--navy-950); }}
    .site-footer p {{ margin: 0; }}

    @media (max-width: 640px) {{
      html {{ scroll-padding-top: 7rem; }}
      .header-inner {{ width: min(100% - 1.25rem, 72rem); min-height: 5rem; align-items: flex-start; padding: 0.75rem 0; flex-direction: column; gap: 0.2rem; }}
      .main-book-link {{ text-align: left; font-size: 0.9rem; }}
      .hero-inner, .layout {{ width: min(100% - 1.25rem, 72rem); }}
      .hero-inner {{ padding: 2.6rem 0 2.4rem; }}
      .toc ol {{ columns: 1; }}
      .chapter {{ padding: 1rem; }}
      .chapter ol, .chapter ul {{ padding-left: 1.35rem; }}
      pre {{ padding: 0.85rem; font-size: 0.88rem; }}
    }}

    @media print {{
      .site-header, .skip-link {{ display: none; }}
      body {{ background: #fff; }}
      .chapter {{ break-inside: avoid; box-shadow: none; }}
    }}
  </style>
</head>
<body>
  <a class="skip-link" href="#main-content">本文へ移動</a>
  <header class="site-header">
    <div class="header-inner">
      <span class="brand">Claude Code 超入門</span>
      <a class="main-book-link" href="../../cc-v2/claude-code-blog-experiential-edition/site/complete.html" target="_blank" rel="noopener">本編（実践教科書）へ</a>
    </div>
  </header>
  <section class="hero" aria-labelledby="page-title">
    <div class="hero-inner">
      <p class="eyebrow">はじめての画面操作から、仕事の成果物まで</p>
      <h1 id="page-title">Claude Code 超入門教科書</h1>
      <p class="lead">コードを書かずに、読む・頼む・確かめるを順番に練習します。1章ずつ、自分のペースで進められます。</p>
    </div>
  </section>
  <main id="main-content" class="layout">
    <nav class="toc" aria-labelledby="toc-title">
      <h2 id="toc-title">目次</h2>
      <ol>
        {toc_items}
      </ol>
    </nav>
    {body}
  </main>
  <footer class="site-footer">
    <p>Claude Code 超入門教科書</p>
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
        body = render_markdown(markdown)
        document = page_template(chapters, body)
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(document, encoding="utf-8")
    except (OSError, BuildError) as error:
        print(f"BUILD FAIL: {error}", file=sys.stderr)
        return 1

    print(f"BUILD PASS: {SOURCE.relative_to(ROOT)} -> {OUTPUT.relative_to(ROOT)}")
    print(f"chapters: {len(chapters)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
