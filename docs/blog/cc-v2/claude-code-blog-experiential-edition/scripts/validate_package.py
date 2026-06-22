#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
MANIFEST = ROOT / "image_manifest.json"
BLOG_MD = ROOT / "claude-code-blog-complete.md"
ORIGINAL = ROOT / "sources" / "original-textbook.md"


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_links(path: Path, errors: list[str]) -> None:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    ids = {tag.get("id") for tag in soup.find_all(attrs={"id": True})}
    for a in soup.find_all("a", href=True):
        href = a["href"]
        parsed = urlparse(href)
        if parsed.scheme or href.startswith("mailto:"):
            continue
        target_path = path
        if parsed.path:
            target_path = (path.parent / unquote(parsed.path)).resolve()
            if not target_path.exists():
                fail(errors, f"Broken file link in {path.relative_to(ROOT)}: {href}")
                continue
        if parsed.fragment:
            target_soup = soup if target_path == path.resolve() else BeautifulSoup(target_path.read_text(encoding="utf-8"), "html.parser")
            target_ids = ids if target_path == path.resolve() else {tag.get("id") for tag in target_soup.find_all(attrs={"id": True})}
            if parsed.fragment not in target_ids:
                fail(errors, f"Broken anchor in {path.relative_to(ROOT)}: {href}")


def main() -> int:
    errors: list[str] = []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    images = manifest["images"]
    ids = [i["id"] for i in images]
    filenames = [i["filename"] for i in images]
    if len(ids) != len(set(ids)):
        fail(errors, "Duplicate image IDs")
    if len(filenames) != len(set(filenames)):
        fail(errors, "Duplicate image filenames")
    for item in images:
        for field in ["id", "placement", "kind", "filename", "alt", "caption", "prompt", "size", "quality", "output_format"]:
            if not item.get(field):
                fail(errors, f"Image {item.get('id')} missing {field}")
        if "OPENAI_API_KEY" in item["prompt"]:
            fail(errors, f"Secret-like text in prompt {item['id']}")

    original = ORIGINAL.read_text(encoding="utf-8")
    blog = BLOG_MD.read_text(encoding="utf-8")
    original_chapters = re.findall(r"^# (?:第\d+章|終章).+$", original, flags=re.M)
    blog_chapters = re.findall(r"^# (?:第\d+章|終章).+$", blog, flags=re.M)
    if len(original_chapters) != len(blog_chapters):
        fail(errors, f"Chapter count mismatch original={len(original_chapters)} blog={len(blog_chapters)}")
    original_h2 = re.findall(r"^## .+$", original, flags=re.M)
    missing_h2 = [h for h in original_h2 if h not in blog]
    if missing_h2:
        fail(errors, f"Missing original H2 headings: {missing_h2[:5]}")
    if blog.count("```") < original.count("```"):
        fail(errors, "Fenced code blocks were lost")

    html_files = sorted(SITE.rglob("*.html"))
    expected_html = 1 + 1 + 1 + len(original_chapters)  # index, complete, image guide, chapter pages
    if len(html_files) != expected_html:
        fail(errors, f"HTML file count mismatch expected={expected_html} actual={len(html_files)}")
    for path in html_files:
        text = path.read_text(encoding="utf-8")
        if "<title>" not in text or "</html>" not in text:
            fail(errors, f"Incomplete HTML: {path.relative_to(ROOT)}")
        validate_links(path, errors)

    complete = (SITE / "complete.html").read_text(encoding="utf-8")
    for item in images:
        if item["filename"] not in complete and item["filename"] not in (SITE / "index.html").read_text(encoding="utf-8"):
            fail(errors, f"Image manifest item not referenced in site: {item['id']}")
    for key in [f"{i:02d}" for i in range(39)] + ["final"]:
        path = SITE / "chapters" / f"{key}.html"
        if not path.exists():
            fail(errors, f"Missing chapter page {key}")

    dry_run = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "generate_images.py"), "--tier", "core", "--quality", "low", "--dry-run"],
        capture_output=True,
        text=True,
    )
    if dry_run.returncode != 0:
        fail(errors, f"Image generator dry-run failed: {dry_run.stderr}")
    if "DRY RUN" not in dry_run.stdout:
        fail(errors, "Image generator dry-run did not report selection")

    if errors:
        print("VALIDATION FAILED")
        for e in errors:
            print(f"- {e}")
        return 1
    print("VALIDATION PASS")
    print(f"- chapters: {len(original_chapters)}")
    print(f"- original subsection headings retained: {len(original_h2)}")
    print(f"- image directives: {len(images)}")
    print(f"- html files: {len(html_files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
