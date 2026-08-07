#!/usr/bin/env python3
"""Deterministic checks for the standalone Claude Code zero textbook."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources" / "zero-textbook.md"
HTML = ROOT / "site" / "index.html"

EXPECTED_CHAPTERS = [
    ("zch-00", "第0章 この教科書の使い方（10分）"),
    ("zch-01", "第1章 Claude Codeって何？（15分）"),
    ("zch-02", "第2章 準備する（20分）"),
    ("zch-03", "第3章 はじめての依頼（20分）"),
    ("zch-04", "第4章 安全の4つの約束（20分）"),
    ("zch-05", "第5章 ファイルを作ってもらう（30分）"),
    ("zch-06", "第6章 思い通りに直してもらう（30分）"),
    ("zch-07", "第7章 失敗しても戻せる（20分）"),
    ("zch-08", "第8章 毎週の仕事を「レシピ」にする（30分）"),
    ("zch-09", "第9章 見せられる資料にする（30分）"),
    ("zch-10", "第10章 事故カタログ（20分）"),
    ("zch-11", "第11章 卒業制作（60分）"),
    ("zch-12", "第12章 質問のしかた・調べ方（15分）"),
    ("zch-final", "終章 次へ進む（5分）"),
]
PHASED_REQUIRED_IDS = {f"zch-{number:02d}" for number in range(6)}
SECTION_NAMES = [
    "今日のゴール",
    "たとえで言うと",
    "やってみる",
    "できたの確認",
    "困ったときは",
    "ことばのミニ辞典",
]

HEADING_RE = re.compile(
    r"^(#{1,6})\s+(.+?)\s+\{#([A-Za-z][A-Za-z0-9_.:-]*)\}\s*$"
)
FORBIDDEN_PATTERNS = [
    ("ターミナル", re.compile(r"ターミナル", re.IGNORECASE)),
    ("CLI", re.compile(r"(?<![A-Za-z0-9_])CLI(?![A-Za-z0-9_])", re.IGNORECASE)),
    ("コマンド", re.compile(r"コマンド(?:ライン)?", re.IGNORECASE)),
    ("シェル", re.compile(r"シェル", re.IGNORECASE)),
    ("rm", re.compile(r"(?<![A-Za-z0-9_])rm(?![A-Za-z0-9_])", re.IGNORECASE)),
    ("Git", re.compile(r"(?<![A-Za-z0-9_])git(?![A-Za-z0-9_])", re.IGNORECASE)),
    ("コミット", re.compile(r"コミット")),
    ("リポジトリ", re.compile(r"リポジトリ")),
    ("ブランチ", re.compile(r"ブランチ")),
    ("マージ", re.compile(r"マージ")),
    ("ディレクトリ", re.compile(r"ディレクトリ")),
    ("API", re.compile(r"(?<![A-Za-z0-9_])API(?![A-Za-z0-9_])", re.IGNORECASE)),
    ("トークン", re.compile(r"トークン")),
    ("デプロイ", re.compile(r"デプロイ")),
    ("ビルド", re.compile(r"ビルド")),
    ("初心者", re.compile(r"初心者")),
    ("簡単です", re.compile(r"簡単です")),
    ("たったこれだけ", re.compile(r"たったこれだけ")),
    ("いかがでしたか", re.compile(r"いかがでしたか")),
    ("と言えるでしょう", re.compile(r"と言えるでしょう")),
]
COMMAND_LINE_RE = re.compile(
    r"^\s*(?:\$\s+|(?:rm|git|cd|ls|pwd|mkdir|rmdir|cp|mv|touch|cat|echo|sudo|"
    r"curl|wget|python3?|pip|npm|pnpm|yarn|bash|zsh|sh|chmod|chown|find|grep|"
    r"rg|sed|awk)(?:\s+|$))",
    re.IGNORECASE | re.MULTILINE,
)


@dataclass(frozen=True)
class Chapter:
    chapter_id: str
    title: str
    start: int
    end: int
    lines: list[str]


class TextbookHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.links: list[dict[str, str]] = []
        self.external_dependencies: list[str] = []
        self.has_inline_style = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name: value or "" for name, value in attrs}
        if values.get("id"):
            self.ids.append(values["id"])
        if tag == "a" and values.get("href"):
            self.links.append(values)
        if tag == "style":
            self.has_inline_style = True
        if (
            tag == "link"
            and values.get("href")
            and not values["href"].startswith("data:")
        ):
            self.external_dependencies.append(values["href"])
        if tag == "script" and values.get("src"):
            self.external_dependencies.append(values["src"])
        if tag in {"img", "iframe"} and values.get("src"):
            parsed = urlparse(values["src"])
            if parsed.scheme or values["src"].startswith("//"):
                self.external_dependencies.append(values["src"])


def strip_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def parse_chapters(source: str) -> list[Chapter]:
    lines = strip_comments(source).splitlines()
    starts: list[tuple[int, str, str]] = []
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match and len(match.group(1)) == 1:
            starts.append((index, match.group(3), match.group(2)))

    chapters: list[Chapter] = []
    for position, (start, chapter_id, title) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        chapters.append(
            Chapter(chapter_id, title, start, end, lines[start:end])
        )
    return chapters


def section_headings(chapter: Chapter) -> list[tuple[str, str, int]]:
    headings: list[tuple[str, str, int]] = []
    for index, line in enumerate(chapter.lines):
        match = HEADING_RE.match(line)
        if match and len(match.group(1)) == 2:
            headings.append((match.group(2), match.group(3), index))
    return headings


def without_dictionary(chapter: Chapter) -> str:
    lines = chapter.lines
    for _, heading_id, index in section_headings(chapter):
        if heading_id.endswith("-s6"):
            lines = lines[:index]
            break
    return "\n".join(lines)


def try_section_text(chapter: Chapter) -> str:
    headings = section_headings(chapter)
    for position, (name, _, start) in enumerate(headings):
        if name != "やってみる":
            continue
        end = headings[position + 1][2] if position + 1 < len(headings) else len(chapter.lines)
        return "\n".join(chapter.lines[start + 1 : end])
    return ""


def allowed_external_link(href: str) -> bool:
    parsed = urlparse(href)
    if parsed.scheme not in {"http", "https"}:
        return True
    host = (parsed.hostname or "").lower()
    return (
        host == "claude.ai"
        or host.endswith(".claude.ai")
        or host == "anthropic.com"
        or host.endswith(".anthropic.com")
    )


def run_checks(strict: bool) -> list[tuple[str, list[str]]]:
    source = SOURCE.read_text(encoding="utf-8")
    html_text = HTML.read_text(encoding="utf-8")
    chapters = parse_chapters(source)
    chapter_map = {chapter.chapter_id: chapter for chapter in chapters}
    expected_ids = [chapter_id for chapter_id, _ in EXPECTED_CHAPTERS]
    required_ids = set(expected_ids) if strict else PHASED_REQUIRED_IDS
    results: list[tuple[str, list[str]]] = []

    chapter_errors: list[str] = []
    actual_pairs = [(chapter.chapter_id, chapter.title) for chapter in chapters]
    if actual_pairs != EXPECTED_CHAPTERS:
        chapter_errors.append(
            "chapter order/title mismatch: "
            f"expected {EXPECTED_CHAPTERS!r}, got {actual_pairs!r}"
        )
    results.append(("章数14・章順・章タイトル", chapter_errors))

    section_errors: list[str] = []
    for chapter_id in expected_ids:
        chapter = chapter_map.get(chapter_id)
        if chapter is None:
            continue
        headings = section_headings(chapter)
        if chapter_id in required_ids:
            expected_section_ids = [
                f"{chapter_id}-s{number}" for number in range(1, 7)
            ]
            actual_names = [name for name, _, _ in headings]
            actual_ids = [heading_id for _, heading_id, _ in headings]
            if actual_names != SECTION_NAMES:
                section_errors.append(
                    f"{chapter_id}: section names/order {actual_names!r}"
                )
            if actual_ids != expected_section_ids:
                section_errors.append(
                    f"{chapter_id}: section IDs {actual_ids!r}"
                )
        elif headings:
            section_errors.append(
                f"{chapter_id}: phased scaffold must not contain partial sections"
            )
    mode_note = "全章" if strict else "第0〜5章＋後半骨組み"
    results.append((f"6見出しの規定順（{mode_note}）", section_errors))

    forbidden_errors: list[str] = []
    for chapter in chapters:
        if chapter.chapter_id not in required_ids:
            continue
        scan_text = without_dictionary(chapter)
        for label, pattern in FORBIDDEN_PATTERNS:
            for match in pattern.finditer(scan_text):
                line_number = chapter.start + scan_text.count("\n", 0, match.start()) + 1
                forbidden_errors.append(
                    f"{chapter.chapter_id}: line {line_number}: {label!r}"
                )
    results.append(("禁止語・禁止表現（ミニ辞典外）", forbidden_errors))

    prompt_errors: list[str] = []
    for chapter_id in expected_ids:
        if chapter_id not in required_ids:
            continue
        chapter = chapter_map.get(chapter_id)
        if chapter is None:
            continue
        section = try_section_text(chapter)
        fence_count = len(re.findall(r"^```", section, flags=re.MULTILINE))
        if fence_count < 2 or fence_count % 2:
            prompt_errors.append(
                f"{chapter_id}: やってみる節に閉じたコードブロックがない"
            )
    results.append(("やってみる節のコピー用コードブロック", prompt_errors))

    parser = TextbookHTMLParser()
    parser.feed(html_text)
    id_errors: list[str] = []
    counts = Counter(parser.ids)
    missing_chapter_ids = [chapter_id for chapter_id in expected_ids if counts[chapter_id] == 0]
    duplicate_ids = sorted(heading_id for heading_id, count in counts.items() if count > 1)
    if missing_chapter_ids:
        id_errors.append(f"missing chapter IDs: {missing_chapter_ids!r}")
    if duplicate_ids:
        id_errors.append(f"duplicate HTML IDs: {duplicate_ids!r}")
    for chapter_id in required_ids:
        for number in range(1, 7):
            section_id = f"{chapter_id}-s{number}"
            if counts[section_id] != 1:
                id_errors.append(
                    f"{section_id}: expected once, got {counts[section_id]}"
                )
    results.append(("生成HTMLの固定ID・重複なし", id_errors))

    link_errors: list[str] = []
    unexpected_links = [
        link["href"] for link in parser.links if not allowed_external_link(link["href"])
    ]
    if unexpected_links:
        link_errors.append(f"unexpected external links: {unexpected_links!r}")
    main_book_href = "../../cc-v2/claude-code-blog-experiential-edition/site/complete.html"
    main_book_links = [link for link in parser.links if link.get("href") == main_book_href]
    if len(main_book_links) != 1:
        link_errors.append("main textbook link must appear exactly once")
    else:
        main_link = main_book_links[0]
        rel_values = set(main_link.get("rel", "").split())
        if main_link.get("target") != "_blank" or "noopener" not in rel_values:
            link_errors.append("main textbook link requires target=_blank and rel=noopener")
    if parser.external_dependencies:
        link_errors.append(
            f"external page dependencies: {parser.external_dependencies!r}"
        )
    if not parser.has_inline_style or "@media (max-width: 640px)" not in html_text:
        link_errors.append("inline responsive CSS is missing")
    results.append(("外部リンク制限・本編リンク・単一HTML", link_errors))

    command_errors: list[str] = []
    for chapter in chapters:
        scan_text = without_dictionary(chapter)
        for match in COMMAND_LINE_RE.finditer(scan_text):
            line_number = chapter.start + scan_text.count("\n", 0, match.start()) + 1
            preview = match.group(0).strip()
            command_errors.append(
                f"{chapter.chapter_id}: line {line_number}: {preview!r}"
            )
    results.append(("行頭の操作文字列パターン", command_errors))
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strict",
        action="store_true",
        help="require complete content and all six sections for every chapter",
    )
    args = parser.parse_args()

    mode = "strict" if args.strict else "phased-z1"
    print(f"validate_zero: mode={mode}")
    try:
        if not SOURCE.is_file():
            raise FileNotFoundError(f"missing source: {SOURCE}")
        if not HTML.is_file():
            raise FileNotFoundError(f"missing HTML: {HTML}; run build_zero.py first")
        results = run_checks(args.strict)
    except (OSError, UnicodeError) as error:
        print(f"RESULT: FAIL\n- {error}", file=sys.stderr)
        return 1

    failed = False
    for number, (label, errors) in enumerate(results, start=1):
        if errors:
            failed = True
            print(f"FAIL [{number}/7] {label}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS [{number}/7] {label}")

    if failed:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS (7/7)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
