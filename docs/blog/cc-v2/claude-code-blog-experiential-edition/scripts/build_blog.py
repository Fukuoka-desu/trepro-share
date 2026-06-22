#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import mistune
from bs4 import BeautifulSoup
from jinja2 import Template

from content_meta import CHARACTERS, PART_META, CHAPTER_META, EXTRA_VISUALS, LESSON_COURSE

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources" / "original-textbook.md"
OUT_MD = ROOT / "claude-code-blog-complete.md"
SITE = ROOT / "site"
CHAPTER_DIR = SITE / "chapters"
IMAGE_DIR = SITE / "images"
ASSET_DIR = SITE / "assets"
MANIFEST_PATH = ROOT / "image_manifest.json"
COVERAGE_PATH = ROOT / "coverage-report.md"

GLOBAL_ART_DIRECTION = (
    "Sophisticated Japanese editorial technology illustration for a long-form educational blog. "
    "Visual language: midnight navy, warm ivory, cobalt blue, and restrained amber accents; "
    "fine paper grain, subtle depth, clean geometric composition, calm cinematic lighting, "
    "credible Japanese office workers, professional and human rather than futuristic spectacle. "
    "Do not include company logos, product logos, copyrighted characters, photorealistic screenshots, "
    "readable text, watermarks, or decorative gibberish. Important labels will be overlaid in HTML. "
    "Leave intentional negative space for a heading and caption."
)

@dataclass
class Part:
    number: int
    title: str

@dataclass
class Chapter:
    key: str
    title: str
    raw_title: str
    body: str
    part: int


def parse_source(text: str) -> tuple[str, list[Part], list[Chapter]]:
    lines = text.splitlines()
    preamble: list[str] = []
    parts: list[Part] = []
    chapters: list[Chapter] = []
    current_part = 0
    current_chapter: Chapter | None = None
    body_lines: list[str] = []
    seen_first_part = False

    part_re = re.compile(r"^# 第(\d+)部[　 ]+(.+)$")
    chapter_re = re.compile(r"^# 第(\d+)章[　 ]+(.+)$")

    def flush() -> None:
        nonlocal current_chapter, body_lines
        if current_chapter is not None:
            current_chapter.body = "\n".join(body_lines).strip() + "\n"
            chapters.append(current_chapter)
        current_chapter = None
        body_lines = []

    for line in lines:
        pm = part_re.match(line)
        cm = chapter_re.match(line)
        if pm:
            flush()
            seen_first_part = True
            current_part = int(pm.group(1))
            parts.append(Part(current_part, pm.group(2).strip()))
            continue
        if cm:
            flush()
            number = int(cm.group(1))
            key = f"{number:02d}"
            title = cm.group(2).strip()
            current_chapter = Chapter(key, title, line[2:].strip(), "", current_part)
            continue
        if line.startswith("# 終章"):
            flush()
            title = line.split("終章", 1)[1].lstrip("　 ")
            current_chapter = Chapter("final", title, line[2:].strip(), "", 8)
            continue
        if current_chapter is not None:
            body_lines.append(line)
        elif not seen_first_part:
            preamble.append(line)
    flush()
    return "\n".join(preamble).strip(), parts, chapters


def strip_original_title(preamble: str) -> str:
    lines = preamble.splitlines()
    out: list[str] = []
    skipped_title = False
    for line in lines:
        if not skipped_title and line.startswith("# "):
            skipped_title = True
            continue
        out.append(line)
    return "\n".join(out).strip()


def image_filename(prefix: str, key: str, title: str) -> str:
    digest = hashlib.sha1(title.encode("utf-8")).hexdigest()[:6]
    return f"{prefix}-{key}-{digest}.webp"


def build_prompt(concept: str, kind: str, composition: str = "Landscape 3:2 composition") -> str:
    return (
        f"{GLOBAL_ART_DIRECTION}\n\n"
        f"Asset type: {kind}.\n"
        f"Scene and concept: {concept}.\n"
        f"Composition: {composition}. Use visual hierarchy and clear spatial relationships. "
        "Keep the image meaningful without embedded words; reserve text for HTML overlays."
    )


def make_manifest(parts: list[Part], chapters: list[Chapter]) -> dict:
    images: list[dict] = []
    cover_concept = (
        "Four collaborators—a non-engineer learner, a developer, an AI operations administrator, "
        "and a conversational navigator—standing around a desk where a terminal, project files, "
        "a safe workflow loop, reusable skills, and an enterprise distribution map connect into one journey"
    )
    images.append({
        "id": "cover-main",
        "tier": "core",
        "placement": "ブログトップのタイトル直下。HTML見出しを画像の左上へ重ねる。",
        "kind": "cinematic editorial cover illustration",
        "filename": "cover-main.webp",
        "size": "2048x1152",
        "quality": "medium",
        "output_format": "webp",
        "alt": "学習者、開発者、管理者、ナビゲーターがClaude Codeの学習と全社運用を一つの旅として設計する表紙イラスト",
        "caption": "使う、理解する、仕組みにする。その全行程を一つの物語として歩きます。",
        "prompt": build_prompt(cover_concept, "cinematic editorial cover illustration", "Wide 16:9 cover with open space on the upper-left for the Japanese title"),
    })
    for part in parts:
        meta = PART_META[part.number]
        images.append({
            "id": f"part-{part.number:02d}",
            "tier": "core",
            "placement": f"第{part.number}部の導入直後。部全体の空気を切り替える横長バナー。",
            "kind": "editorial section banner",
            "filename": image_filename("part", f"{part.number:02d}", part.title),
            "size": "1536x1024",
            "quality": "medium",
            "output_format": "webp",
            "alt": f"第{part.number}部『{part.title}』の概念イラスト",
            "caption": meta["story"],
            "prompt": build_prompt(meta["image_concept"], "editorial section banner", "Landscape 3:2 with generous horizontal negative space"),
        })
    for chapter in chapters:
        meta = CHAPTER_META[chapter.key]
        label = "終章" if chapter.key == "final" else f"第{int(chapter.key)}章"
        images.append({
            "id": f"chapter-{chapter.key}",
            "tier": "chapter",
            "placement": f"{label}の物語導入と技術解説の間。内容の感覚的な理解を助ける。",
            "kind": meta["image_kind"],
            "filename": image_filename("chapter", chapter.key, chapter.title),
            "size": "1536x1024",
            "quality": "medium",
            "output_format": "webp",
            "alt": f"{label}『{chapter.title}』を表す{meta['image_kind']}",
            "caption": meta["takeaway"],
            "prompt": build_prompt(meta["image_concept"], meta["image_kind"]),
        })
    for item in EXTRA_VISUALS:
        images.append({
            "id": item["id"],
            "tier": item["tier"],
            "placement": item["placement"],
            "kind": item["kind"],
            "filename": f"{item['id']}.webp",
            "size": "1536x1024",
            "quality": "medium",
            "output_format": "webp",
            "alt": item["alt"],
            "caption": item["caption"],
            "prompt": build_prompt(item["concept"], item["kind"]),
        })
    return {
        "schema_version": "1.0",
        "created_for": "Claude Code実践教科書・ブログ完全版",
        "default_model": "gpt-image-2",
        "snapshot_option": "gpt-image-2-2026-04-21",
        "default_output_directory": "site/images",
        "art_direction": GLOBAL_ART_DIRECTION,
        "production_policy": {
            "critical_information_in_images": False,
            "reason": "画像がなくても本文、alt、captionだけで理解できる構造にする。",
            "text_rendering": "重要な日本語ラベルは画像に焼き込まずHTML/CSSで重ねる。",
            "draft_workflow": "low品質で構図確認後、採用画像だけmediumまたはhighで再生成する。",
            "secret_handling": "OPENAI_API_KEYはサーバー側またはBuild時だけで使用し、HTMLへ埋め込まない。",
        },
        "images": images,
    }


def manifest_lookup(manifest: dict) -> dict[str, dict]:
    return {i["id"]: i for i in manifest["images"]}


def image_directive_md(item: dict) -> str:
    prompt = item["prompt"].replace("\n", " ")
    return (
        f"> **画像制作指示：`{item['id']}`**  \n"
        f"> **配置**: {item['placement']}  \n"
        f"> **種類**: {item['kind']}  \n"
        f"> **代替テキスト**: {item['alt']}  \n"
        f"> **Caption**: {item['caption']}  \n"
        f"> **推奨設定**: `{item['size']}` / `{item['quality']}` / `{item['output_format']}`  \n"
        f"> **Image API Prompt**: {prompt}\n"
    )


def chapter_markdown(chapter: Chapter, image: dict, extras: list[dict]) -> str:
    meta = CHAPTER_META[chapter.key]
    heading = f"# 終章　{chapter.title}" if chapter.key == "final" else f"# 第{int(chapter.key)}章　{chapter.title}"
    chunks = [
        heading,
        "",
        "## 物語の現在地",
        "",
        meta["scene"],
        "",
        meta["essay"],
        "",
        image_directive_md(image),
        "",
        "## 実装リファレンス",
        "",
        "ここからは、物語でつかんだ考え方を、そのまま実装へ落とせる粒度で確認します。コード、設定、検証条件は省略せず残しています。",
        "",
        chapter.body.strip(),
    ]
    if extras:
        chunks.extend(["", "## 補助図の制作指示", ""])
        for extra in extras:
            chunks.extend([image_directive_md(extra), ""])
    if meta.get("usecases"):
        chunks.extend(["", "## こんな場面で使う", ""])
        chunks.append("章の内容が実務でどう活きるか。架空の場面・行動・効果の三点で示します。")
        chunks.append("")
        for uc in meta["usecases"]:
            chunks.extend([
                f"**場面:** {uc['situation']}",
                "",
                f"**こう使う:** {uc['action']}",
                "",
                f"**得られるもの:** {uc['benefit']}",
                "",
            ])
    chunks.extend([
        "",
        "## 体験ミッション",
        "",
        meta["mission"],
        "",
        "## ナビゲーターのひとこと",
        "",
        f"> {meta['takeaway']}",
        "",
    ])
    return "\n".join(chunks)


def build_markdown(preamble: str, parts: list[Part], chapters: list[Chapter], manifest: dict) -> str:
    lookup = manifest_lookup(manifest)
    extras_by_chapter: dict[str, list[dict]] = {}
    for item in manifest["images"]:
        if item["id"].startswith("diagram-"):
            chapter = next((v["chapter"] for v in EXTRA_VISUALS if v["id"] == item["id"]), None)
            if chapter:
                extras_by_chapter.setdefault(chapter, []).append(item)

    out = [
        "# Claude Code実践教科書 — 物語で歩くブログ完全版",
        "",
        "> **版**: Blog Edition v1.0  ",
        "> **基準日**: 2026-06-22  ",
        "> **形式**: テキストだけでも完結する読み物 + 全実装リファレンス + 画像制作指示  ",
        "> **対象**: 初心者、非エンジニア、開発者、AI推進、情シス、ハーネス管理者",
        "",
        "## はじまり — 『使えている』から『直せる・説明できる・配れる』へ",
        "",
        "営業企画の遥は、Cursorから既存のスライド生成Skillを呼び出せました。けれど、途中で止まったときに原因を追えず、出力が正しいかを証拠で説明できませんでした。開発者の蓮は再現性を、AI推進の美咲は安全と全社配布を気にしています。そこへナビゲーターが加わり、四人はClaude Codeを0から学び直す旅を始めます。",
        "",
        "このブログ版は、各章を『物語の現在地 → 技術の意味 → 実装リファレンス → 体験ミッション → 振り返り』の順で進めます。生成画像は理解を補助しますが、画像が一枚もなくても本文だけで完結します。",
        "",
        image_directive_md(lookup["cover-main"]),
        "",
        "## 登場人物",
        "",
        "| 人物 | 役割 | この旅で向き合うこと |",
        "|---|---|---|",
    ]
    for c in CHARACTERS:
        out.append(f"| {c['name']} | {c['role']} | {c['description']} |")
    out.extend([
        "",
        "## 原典から引き継ぐ前提",
        "",
        strip_original_title(preamble),
        "",
    ])
    chapters_by_part: dict[int, list[Chapter]] = {}
    for ch in chapters:
        chapters_by_part.setdefault(ch.part, []).append(ch)
    for part in parts:
        meta = PART_META[part.number]
        out.extend([
            f"# 第{part.number}部　{part.title}",
            "",
            meta["story"],
            "",
        ])
        if meta.get("usecase"):
            uc = meta["usecase"]
            out.extend([
                "**この部で得られる場面**",
                "",
                f"- 場面: {uc['situation']}",
                f"- こう使う: {uc['action']}",
                f"- 得られるもの: {uc['benefit']}",
                "",
            ])
        out.extend([
            image_directive_md(lookup[f"part-{part.number:02d}"]),
            "",
        ])
        for ch in chapters_by_part.get(part.number, []):
            out.append(chapter_markdown(ch, lookup[f"chapter-{ch.key}"], extras_by_chapter.get(ch.key, [])))
    return "\n".join(out).strip() + "\n"


CSS = r"""
:root{
  --ink:#172033;--muted:#5f6b7e;--paper:#fbf8f1;--panel:#ffffff;--navy:#14213d;
  --blue:#2456d3;--amber:#d7891c;--line:#d9dee8;--soft:#eef3fb;--success:#176b55;
  /* 3-axis palette (90+ pass) */
  --story-bg:#fbf8f1;--story-ink:#172033;--story-accent:#2456d3;
  --action-accent:#d7891c;--action-bg:#fffaf2;--action-border:#f1c98b;--action-ink:#7a4a10;
  --ref-accent:#2456d3;--ref-bg:#f3f7fc;--ref-border:#cfdcef;--ref-ink:#1f3457;
  /* Legacy aliases retained */
  --usecase-bg:#f3f7fc;--usecase-border:#cfdcef;--usecase-accent:#2456d3;
  --shadow:0 18px 60px rgba(27,39,64,.11);--radius:20px;--max:1480px;--toc-w:280px;
}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Hiragino Sans","Yu Gothic UI","Yu Gothic",Meiryo,sans-serif;line-height:1.95;font-size:1.05rem}
a{color:var(--blue);text-underline-offset:3px}.progress{position:fixed;inset:0 0 auto 0;height:4px;background:transparent;z-index:100}.progress>span{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--blue),var(--amber))}
.site-header{background:linear-gradient(135deg,#101b33,#233961);color:white;padding:14px 24px;position:sticky;top:0;z-index:40;box-shadow:0 8px 28px rgba(0,0,0,.18)}.site-header .inner{max-width:var(--max);margin:auto;display:flex;align-items:center;gap:18px}.brand{font-weight:800;letter-spacing:.02em;color:white;text-decoration:none}.site-header nav{margin-left:auto;display:flex;gap:16px;flex-wrap:wrap}.site-header nav a{color:#e7edff;text-decoration:none;font-size:.92rem}
.toc-toggle{display:none;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.3);color:white;border-radius:10px;padding:6px 12px;font-size:.86rem;font-weight:700;cursor:pointer}
.toc-toggle:hover{background:rgba(255,255,255,.22)}
.hero{max-width:var(--max);margin:0 auto;padding:64px 24px 28px}.hero-grid{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(320px,.95fr);gap:40px;align-items:center}.eyebrow{font-size:.82rem;letter-spacing:.16em;text-transform:uppercase;color:var(--amber);font-weight:800}.hero h1{font-size:clamp(2.25rem,5vw,4.6rem);line-height:1.08;letter-spacing:-.04em;margin:.25em 0}.lede{font-size:1.16rem;color:var(--muted);max-width:64ch}.hero-actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}.button{display:inline-flex;align-items:center;justify-content:center;padding:11px 17px;border-radius:999px;text-decoration:none;font-weight:700;border:1px solid var(--line);background:white;color:var(--ink)}.button.primary{background:var(--blue);border-color:var(--blue);color:white}
.layout{max-width:var(--max);margin:auto;padding:20px 24px 80px;display:grid;grid-template-columns:var(--toc-w) minmax(0,1fr);gap:40px}
.toc{position:sticky;top:78px;align-self:start;max-height:calc(100vh - 100px);overflow:auto;background:rgba(255,255,255,.86);backdrop-filter:blur(14px);border:1px solid var(--line);border-radius:16px;padding:18px;transition:transform .25s ease,box-shadow .25s ease}
.toc h2{font-size:.95rem;margin:0 0 12px}
.toc a{display:block;padding:7px 10px;border-radius:8px;text-decoration:none;color:var(--muted);font-size:.88rem;line-height:1.4;border-left:3px solid transparent;transition:background .15s,color .15s,border-color .15s}
.toc a:hover{background:var(--soft);color:var(--ink)}
.toc .part-link{font-weight:800;color:var(--navy);margin-top:10px;font-size:.92rem}
.toc a.active{background:#e6edff;color:var(--ink);border-left-color:var(--blue);font-weight:700}
.toc a.part-link.active{background:#dde6ff;color:var(--navy);border-left-color:var(--amber)}
.toc-drawer-close{display:none}
.toc-overlay{display:none}
.content{min-width:0}.part{margin:56px 0 80px}.part-header{padding:42px;border-radius:var(--radius);background:linear-gradient(135deg,#13213e,#26406e);color:white;box-shadow:var(--shadow);scroll-margin-top:80px}.part-header h2{font-size:clamp(1.8rem,4vw,3.2rem);line-height:1.2;margin:.2em 0}.part-header p{color:#dbe5ff;max-width:70ch}
.chapter{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:clamp(24px,5vw,56px);margin:34px 0;box-shadow:var(--shadow);scroll-margin-top:80px}
.chapter-head{border-bottom:1px solid var(--line);padding-bottom:20px;margin-bottom:28px}.chapter-head h1{font-size:clamp(1.8rem,4vw,3rem);line-height:1.25;letter-spacing:-.025em;margin:.2em 0}
.story-block{margin:24px 0 26px}
.story-lead{font-family:ui-serif,"Yu Mincho","Hiragino Mincho ProN",serif;font-size:1.12rem;line-height:1.8;color:var(--story-ink);background:transparent;border-left:4px solid var(--story-accent);padding:6px 18px 6px 16px;margin:0 0 14px 0;border-radius:0}
.story-essay{font-size:1.06rem;background:#fff;border:1px solid #e3e9f5;border-radius:14px;padding:22px 26px;margin:0;color:var(--story-ink)}
.story-essay p{margin:0 0 1.1em}
.story-essay p:last-child{margin-bottom:0}
.story-essay p:first-child::first-letter{font-size:3.4em;float:left;line-height:.82;padding:.12em .12em 0 0;color:var(--story-accent);font-weight:800}
/* Legacy .scene kept as fallback alias (no longer emitted by builder, but tolerated) */
.scene{font-family:ui-serif,"Yu Mincho","Hiragino Mincho ProN",serif;font-size:1.1rem;background:transparent;border-left:4px solid var(--story-accent);padding:6px 18px;margin:14px 0;border-radius:0}
.image-shell{margin:34px 0;border:1px solid var(--line);border-radius:18px;overflow:hidden;background:linear-gradient(135deg,#e9effa,#fff4df);min-height:260px;position:relative}.image-shell img{width:100%;height:auto;display:block;aspect-ratio:3/2;object-fit:cover}.image-shell.missing img{display:none}.image-shell.missing:before{content:"生成画像の差し込み位置";display:grid;place-items:center;min-height:320px;color:var(--muted);font-weight:800;letter-spacing:.08em}.image-shell figcaption{padding:14px 18px;background:white;color:var(--muted);font-size:.92rem}.image-brief{border-top:1px solid var(--line);background:#fafcff;padding:0 18px}.image-brief summary{cursor:pointer;padding:12px 0;font-weight:800;color:var(--blue)}.image-brief pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#111827;color:#e6edf7;border-radius:12px;padding:16px;font-size:.8rem}
.reference{margin-top:38px}.reference>h2:first-child{margin-top:0}.reference h2{font-size:1.55rem;margin-top:2.2em;border-left:4px solid var(--blue);padding-left:12px}.reference h3{font-size:1.18rem;margin-top:1.8em}.reference p,.reference li{max-width:76ch}.reference p{margin:1.05em 0}.reference table{width:100%;border-collapse:collapse;display:block;overflow-x:auto;margin:22px 0}.reference th,.reference td{border:1px solid var(--line);padding:10px 12px;vertical-align:top;min-width:130px}.reference th{background:var(--soft);text-align:left}.reference blockquote{margin:20px 0;padding:12px 18px;border-left:4px solid var(--amber);background:#fff9ec;color:#4b5563}.reference code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:#edf1f7;padding:.13em .35em;border-radius:5px;font-size:.9em}.code-wrap{position:relative;margin:22px 0}.code-wrap pre{overflow:auto;background:#101827;color:#e6edf7;padding:20px;border-radius:14px;line-height:1.65}.code-wrap code{background:transparent;color:inherit;padding:0}.copy-code{position:absolute;top:10px;right:10px;border:1px solid #52617c;border-radius:8px;background:#1e2a42;color:white;padding:6px 10px;cursor:pointer;font-size:.78rem}
/* Legacy single blocks kept as aliases */
.mission,.takeaway{border-radius:16px;padding:22px 24px;margin:30px 0}.mission{background:var(--action-bg);border:1px solid var(--action-border)}.takeaway{background:#fff;border:1px solid var(--action-border)}.mission h2,.takeaway h2{margin-top:0;font-size:1.2rem;color:var(--action-ink)}.mission strong{color:var(--action-ink)}
/* Combined mission + takeaway (90+ pass) */
.mission-takeaway{display:grid;grid-template-columns:1.05fr .95fr;gap:14px;margin:30px 0}
.mission-takeaway .mt-mission,.mission-takeaway .mt-takeaway{border-radius:16px;padding:20px 22px}
.mission-takeaway .mt-mission{background:var(--action-bg);border:1px solid var(--action-border)}
.mission-takeaway .mt-takeaway{background:#fff;border:1px solid var(--action-border)}
.mission-takeaway h3{margin:0 0 6px;font-size:1.04rem;color:var(--action-ink);letter-spacing:.02em;display:flex;align-items:center;gap:8px}
.mission-takeaway h3::before{content:"";display:inline-block;width:6px;height:18px;background:var(--action-accent);border-radius:3px}
.mission-takeaway .mt-mission p,.mission-takeaway .mt-takeaway p{margin:0;line-height:1.85}
.mission-takeaway .mt-mission strong{color:var(--action-ink)}
@media(max-width:720px){.mission-takeaway{grid-template-columns:1fr}}
.features{margin:24px 0;padding:24px;border-radius:18px;background:var(--ref-bg);border:1px solid var(--ref-border);box-shadow:0 6px 18px rgba(20,50,100,.04)}
.features>h2{margin:0 0 4px;font-size:1.18rem;color:var(--ref-ink);display:flex;align-items:center;gap:8px}
.features>h2::before{content:"";display:inline-block;width:8px;height:22px;background:var(--ref-accent);border-radius:3px}
.features-lede{margin:0 0 16px;color:#3b5070;font-size:.93rem}
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}
.feature-card{background:white;border:1px solid #d4dff0;border-radius:14px;padding:16px 18px;box-shadow:0 4px 14px rgba(20,50,100,.05);transition:transform .18s ease,box-shadow .18s ease}
.feature-card:hover{transform:translateY(-2px);box-shadow:0 10px 22px rgba(20,50,100,.1)}
.feature-card h3{margin:0 0 6px;font-size:1.02rem;color:#143764}
.feature-summary{margin:0 0 10px;font-size:.92rem;line-height:1.75;color:#2c3e5c}
.feature-io{margin:0;display:grid;grid-template-columns:auto 1fr;gap:4px 12px;font-size:.84rem}
.feature-io dt{color:#5478a8;font-weight:700;letter-spacing:.06em;text-transform:uppercase;font-size:.72rem;padding-top:2px}
.feature-io dd{margin:0;color:#2c3e5c;line-height:1.65}
@media(max-width:520px){.features-grid{grid-template-columns:1fr}}
/* feature-intro: subdued annotation (90+ pass) */
.feature-intro{margin:6px 0 14px;padding:6px 12px;background:transparent;border-left:3px solid #cbd5e1;border-radius:0;font-size:.88rem;line-height:1.7;color:#475569}
.feature-intro-label{display:inline;font-size:.74rem;letter-spacing:.04em;color:#64748b;font-weight:700;margin-right:6px;padding:0;background:transparent;border-radius:0;vertical-align:baseline}
.feature-intro-label::after{content:"："}
.feature-intro-io{display:block;margin-top:4px;font-size:.8rem;color:#64748b}
.feature-intro-io strong{color:#475569;font-weight:700}
.usecases{margin:32px 0;padding:26px;border-radius:18px;background:var(--ref-bg);border:1px solid var(--ref-border);box-shadow:0 6px 18px rgba(20,50,100,.05)}
.usecases>h2{margin:0 0 6px;font-size:1.22rem;color:var(--ref-ink);display:flex;align-items:center;gap:8px}
.usecases>h2::before{content:"";display:inline-block;width:8px;height:22px;background:var(--ref-accent);border-radius:3px}
.usecases-lede{margin:0 0 16px;color:#3b5070;font-size:.94rem}
.usecase-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.usecase-card{background:white;border:1px solid #d4dff0;border-radius:14px;padding:18px 19px;box-shadow:0 4px 14px rgba(20,50,100,.05);transition:transform .18s ease,box-shadow .18s ease}
.usecase-card:hover{transform:translateY(-2px);box-shadow:0 10px 22px rgba(20,50,100,.1)}
.usecase-card h3{margin:0 0 4px;font-size:.76rem;letter-spacing:.13em;text-transform:uppercase;color:var(--ref-accent);font-weight:800}
.usecase-card p{margin:0 0 10px;font-size:.94rem;line-height:1.75;color:var(--story-ink)}
.usecase-card p:last-child{margin-bottom:0}
.part-usecase{margin:22px 0 0;padding:22px 24px;border-radius:16px;background:var(--ref-bg);border:1px solid var(--ref-border);color:var(--story-ink);display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}
.part-usecase h3{grid-column:1/-1;margin:0;font-size:.92rem;letter-spacing:.1em;text-transform:uppercase;color:var(--ref-accent)}
.part-usecase .pu-item h4{margin:0 0 4px;font-size:.74rem;letter-spacing:.12em;text-transform:uppercase;color:var(--ref-accent)}
.part-usecase .pu-item p{margin:0;font-size:.92rem;line-height:1.72}
.course-overview{margin:18px 0 44px;padding:34px clamp(20px,3vw,40px);border-radius:24px;background:linear-gradient(135deg,#7a4a10 0%,#b06a18 55%,var(--action-accent) 100%);color:#fff8ec;box-shadow:0 18px 44px rgba(122,74,16,.25);scroll-margin-top:90px}
.course-overview .course-head{max-width:760px;margin-bottom:22px}
.course-overview .eyebrow{color:#ffe9c2}
.course-overview h2{margin:.2em 0 .4em;font-size:clamp(1.7rem,3.4vw,2.4rem);line-height:1.2;color:white}
.course-lede{margin:0 0 .6em;color:#fdebcb;line-height:1.85;font-size:1rem}
.course-trigger{color:#fff4dc}
.course-trigger code{background:rgba(255,255,255,.16);color:#fff;border-radius:6px;padding:.08em .42em}
.course-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.course-card{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.22);border-radius:16px;padding:18px 19px;backdrop-filter:blur(8px);transition:transform .18s ease,background .18s ease,border-color .18s ease}
.course-card:hover{transform:translateY(-2px);background:rgba(255,255,255,.18);border-color:rgba(255,233,194,.6)}
.course-card-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px}
.course-id{font-weight:800;letter-spacing:.06em;color:#fff4dc;font-size:.92rem;background:rgba(255,255,255,.18);padding:3px 9px;border-radius:999px}
.course-min{font-size:.78rem;color:#fde2b2;letter-spacing:.04em}
.course-card h3{margin:.15em 0 .35em;font-size:1.04rem;line-height:1.45;color:white}
.course-objective{margin:0 0 10px;font-size:.9rem;line-height:1.7;color:#fdebcb}
.course-chapters{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px}
.course-chip{display:inline-block;padding:3px 10px;border-radius:999px;background:rgba(255,255,255,.16);color:#fff;text-decoration:none;font-size:.76rem;border:1px solid rgba(255,255,255,.22);transition:background .15s,border-color .15s}
.course-chip:hover{background:rgba(255,255,255,.28);border-color:rgba(255,233,194,.6);color:#fff}
.course-chip.more{background:transparent;border-style:dashed;color:#fde2b2;cursor:default}
.course-note{margin:0;font-size:.78rem;color:#fde2b2;letter-spacing:.02em}
.toc .course-link{color:#b85a18;background:#fff6ec;border-left-color:var(--action-accent);font-weight:800;font-size:.92rem}
.toc .course-link.active{background:#ffe8c8;color:#9a4a12;border-left-color:var(--action-accent)}
.character-grid,.card-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.card{background:white;border:1px solid var(--line);border-radius:16px;padding:20px;box-shadow:0 8px 28px rgba(27,39,64,.06)}.card h3{margin:.1em 0}.card p{color:var(--muted)}.chapter-nav{display:flex;justify-content:space-between;gap:16px;margin-top:34px}.chapter-nav a{flex:1;background:white;border:1px solid var(--line);border-radius:14px;padding:14px;text-decoration:none}.chapter-nav a:last-child{text-align:right}
.site-footer{background:#111b31;color:#ced7ea;padding:36px 24px}.site-footer .inner{max-width:1200px;margin:auto}.source-note{font-size:.86rem;color:var(--muted);border-top:1px solid var(--line);margin-top:40px;padding-top:20px}
@media(min-width:1281px){
  body{padding-left:calc(var(--toc-w) + 48px)}
  .toc{position:fixed;top:78px;left:24px;width:var(--toc-w);max-height:calc(100vh - 100px);align-self:auto}
  .layout{display:block;padding:20px 24px 80px;max-width:calc(var(--max) - var(--toc-w) - 48px)}
  .site-header .inner,.hero,.site-footer .inner{max-width:calc(var(--max) - var(--toc-w) - 48px)}
}
@media(max-width:1280px) and (min-width:981px){.layout{grid-template-columns:260px minmax(0,1fr);gap:30px}}
@media(max-width:980px){
  .hero-grid{grid-template-columns:1fr;gap:18px}
  .layout{display:block;padding:20px 18px 80px}
  .character-grid,.card-grid{grid-template-columns:1fr}
  .site-header nav{display:none}
  .toc-toggle{display:inline-flex}
  .toc{position:fixed;top:0;left:0;width:min(86vw,320px);height:100vh;max-height:none;border-radius:0;border:none;border-right:1px solid var(--line);transform:translateX(-100%);box-shadow:0 0 40px rgba(0,0,0,.3);z-index:60;padding:18px 18px 60px;background:#fff}
  .toc.open{transform:translateX(0)}
  .toc-drawer-close{display:block;position:absolute;top:10px;right:12px;width:36px;height:36px;border:1px solid var(--line);border-radius:10px;background:white;cursor:pointer;font-size:1.2rem;line-height:1}
  .toc-overlay{display:none;position:fixed;inset:0;background:rgba(10,15,30,.45);z-index:55}
  .toc-overlay.open{display:block}
}
/* Slide carousel (90+ pass) */
.slide-carousel{position:relative;margin:28px 0 36px;border-radius:18px;background:#fff;border:1px solid var(--ref-border);box-shadow:0 8px 24px rgba(20,50,100,.06);overflow:hidden}
.slide-carousel-track{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scroll-behavior:smooth;gap:0;scrollbar-width:none}
.slide-carousel-track::-webkit-scrollbar{display:none}
.slide-carousel-track .lesson-slide{flex:0 0 100%;scroll-snap-align:start;margin:0;border:none;border-radius:0;box-shadow:none;max-width:none}
.slide-carousel-dots{display:flex;justify-content:center;gap:6px;padding:10px 0 14px;background:linear-gradient(to top,#fafcff,transparent)}
.slide-carousel-dots .dot{width:8px;height:8px;border-radius:50%;background:#cfdcef;transition:background .2s}
.slide-carousel-dots .dot.active{background:var(--ref-accent)}
.slide-nav{position:absolute;top:38%;width:38px;height:38px;border-radius:50%;border:none;background:rgba(255,255,255,.85);box-shadow:0 4px 14px rgba(0,0,0,.18);font-size:1.4rem;cursor:pointer;color:var(--ref-ink);transition:background .15s,transform .15s;display:grid;place-items:center;line-height:1;padding:0}
.slide-nav:hover{background:white;transform:scale(1.06)}
.slide-nav.prev{left:12px}
.slide-nav.next{right:12px}
@media(max-width:640px){.slide-nav{display:none}}
@media print{.site-header,.toc,.toc-toggle,.toc-overlay,.progress,.copy-code,.image-brief,.hero-actions,.slide-nav{display:none!important}.layout{display:block;padding:0}.chapter,.part-header,.usecases,.features,.slide-carousel{box-shadow:none;break-inside:avoid;border-color:#bbb}.image-shell{break-inside:avoid}.slide-carousel-track{display:block;overflow:visible}.slide-carousel-track .lesson-slide{flex:none}body{background:white}.chapter{page-break-before:always}}
"""

JS = r"""
(() => {
  const bar = document.querySelector('.progress > span');
  const update = () => {
    const h = document.documentElement;
    const max = h.scrollHeight - h.clientHeight;
    if (bar) bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
  };
  document.addEventListener('scroll', update, {passive:true}); update();
  document.querySelectorAll('.image-shell img').forEach(img => {
    const markMissing = () => img.closest('.image-shell')?.classList.add('missing');
    if (img.complete && img.naturalWidth === 0) markMissing();
    img.addEventListener('error', markMissing);
  });
  document.querySelectorAll('pre code').forEach(code => {
    const pre = code.parentElement;
    if (!pre || pre.closest('.image-brief')) return;
    const wrap = document.createElement('div'); wrap.className = 'code-wrap';
    pre.parentNode.insertBefore(wrap, pre); wrap.appendChild(pre);
    const btn = document.createElement('button'); btn.className='copy-code'; btn.textContent='コピー';
    btn.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(code.textContent || ''); btn.textContent='コピー済み'; setTimeout(()=>btn.textContent='コピー',1200); }
      catch { btn.textContent='失敗'; }
    });
    wrap.appendChild(btn);
  });

  // TOC active highlight via IntersectionObserver
  const toc = document.querySelector('.toc');
  if (toc) {
    const links = Array.from(toc.querySelectorAll('a[href^="#"]'));
    const map = new Map();
    links.forEach(a => {
      const id = a.getAttribute('href').slice(1);
      if (id) map.set(id, a);
    });
    const targets = [];
    map.forEach((_, id) => { const el = document.getElementById(id); if (el) targets.push(el); });
    if (targets.length && 'IntersectionObserver' in window) {
      const visible = new Set();
      const setActive = () => {
        if (!visible.size) return;
        // pick the topmost visible target
        let topId = null, topY = Infinity;
        visible.forEach(id => {
          const el = document.getElementById(id);
          if (!el) return;
          const y = el.getBoundingClientRect().top;
          if (y >= -40 && y < topY) { topY = y; topId = id; }
        });
        if (!topId) {
          // fallback to any visible
          topId = Array.from(visible)[0];
        }
        links.forEach(a => a.classList.remove('active'));
        const link = map.get(topId);
        if (link) {
          link.classList.add('active');
          // also activate the part-link of the surrounding part if chapter
          const el = document.getElementById(topId);
          const part = el?.closest('section.part');
          if (part && part.id) {
            const partLink = map.get(part.id);
            if (partLink && partLink !== link) partLink.classList.add('active');
          }
        }
      };
      const io = new IntersectionObserver(entries => {
        entries.forEach(e => {
          const id = e.target.id;
          if (e.isIntersecting) visible.add(id); else visible.delete(id);
        });
        setActive();
      }, {rootMargin: '-80px 0px -70% 0px', threshold: 0});
      targets.forEach(t => io.observe(t));
    }

    // Slide carousel (90+ pass): scroll-snap with dots/buttons
    document.querySelectorAll('.slide-carousel').forEach(car => {
      const track = car.querySelector('.slide-carousel-track');
      if (!track) return;
      const slides = track.querySelectorAll('.lesson-slide');
      const dotsWrap = car.querySelector('.slide-carousel-dots');
      const prev = car.querySelector('.slide-nav.prev');
      const next = car.querySelector('.slide-nav.next');
      if (slides.length < 2) return;
      const updateDots = () => {
        if (!dotsWrap) return;
        const w = track.clientWidth || 1;
        const i = Math.round(track.scrollLeft / w);
        dotsWrap.querySelectorAll('.dot').forEach((d, j) => d.classList.toggle('active', i === j));
      };
      track.addEventListener('scroll', () => requestAnimationFrame(updateDots), {passive: true});
      prev && prev.addEventListener('click', () => track.scrollBy({left: -track.clientWidth, behavior: 'smooth'}));
      next && next.addEventListener('click', () => track.scrollBy({left:  track.clientWidth, behavior: 'smooth'}));
      updateDots();
    });

    // Drawer toggle for mobile
    const toggle = document.querySelector('.toc-toggle');
    const overlay = document.querySelector('.toc-overlay');
    const closeBtn = toc.querySelector('.toc-drawer-close');
    const openDrawer = () => { toc.classList.add('open'); overlay && overlay.classList.add('open'); };
    const closeDrawer = () => { toc.classList.remove('open'); overlay && overlay.classList.remove('open'); };
    toggle && toggle.addEventListener('click', () => {
      if (toc.classList.contains('open')) closeDrawer(); else openDrawer();
    });
    overlay && overlay.addEventListener('click', closeDrawer);
    closeBtn && closeBtn.addEventListener('click', closeDrawer);
    // Close drawer on link click (mobile only)
    toc.addEventListener('click', e => {
      if (e.target.tagName === 'A' && window.matchMedia('(max-width:980px)').matches) {
        closeDrawer();
      }
    });
  }
})();
"""


def md_renderer() -> mistune.Markdown:
    return mistune.create_markdown(
        renderer=mistune.HTMLRenderer(escape=False),
        plugins=["table", "strikethrough", "task_lists", "url"],
    )


def add_heading_ids(fragment: str, prefix: str) -> str:
    soup = BeautifulSoup(fragment, "html.parser")
    used: set[str] = set()
    for idx, heading in enumerate(soup.find_all(["h2", "h3", "h4"])):
        base = f"{prefix}-s{idx+1}"
        while base in used:
            base += "x"
        used.add(base)
        heading["id"] = base
    return str(soup)


# Heading text patterns that are structural (章共通) and should never receive a feature intro.
_FEATURE_INTRO_SKIP_KEYWORDS = (
    "物語の現在地",
    "実装リファレンス",
    "補助図",
    "体験ミッション",
    "ナビゲーター",
    "この章で扱う機能",
    "この章の概観",
    "こんな場面で使う",
)


def _normalize_heading_text(text: str) -> str:
    """Strip section number prefix (e.g. '32.1 ') and surrounding whitespace from heading text."""
    # Drop numeric prefixes like "32.1", "32.1.2", "32-1", "1." etc.
    cleaned = re.sub(r"^[\s]*[\d０-９]+([\.\-－・][\d０-９]+)*[\s\.\-：:、　]*", "", text)
    return cleaned.strip()


def _match_feature(heading_body: str, features: list[dict]) -> dict | None:
    """Find the best matching feature for a heading. Returns None if no good match."""
    if not heading_body or not features:
        return None
    best: tuple[int, dict] | None = None
    for feat in features:
        name = (feat.get("name") or "").strip()
        if not name:
            continue
        # Two-way containment check
        if name in heading_body:
            score = len(name)
        elif heading_body in name:
            score = len(heading_body)
        else:
            continue
        if best is None or score > best[0]:
            best = (score, feat)
    return best[1] if best else None


def inject_feature_intros(fragment: str, features: list[dict]) -> str:
    """Inject a <p class="feature-intro"> right after each h2/h3 that matches a feature name."""
    if not features:
        return fragment
    # Wrap to ensure consistent parsing
    soup = BeautifulSoup(f"<div>{fragment}</div>", "html.parser")
    root = soup.div if soup.div else soup
    for heading in root.find_all(["h2", "h3"]):
        heading_text = heading.get_text(strip=True)
        if not heading_text:
            continue
        # Skip structural headings
        if any(kw in heading_text for kw in _FEATURE_INTRO_SKIP_KEYWORDS):
            continue
        body = _normalize_heading_text(heading_text)
        if not body:
            continue
        # Guard against double-insertion
        nxt = heading.find_next_sibling()
        if nxt is not None and nxt.name == "p" and "feature-intro" in (nxt.get("class") or []):
            continue
        match = _match_feature(body, features)
        if not match:
            continue
        summary = (match.get("summary") or "").strip()
        if not summary:
            continue
        input_text = (match.get("input") or "").strip()
        output_text = (match.get("output") or "").strip()
        p = soup.new_tag("p")
        p["class"] = ["feature-intro"]
        label = soup.new_tag("strong")
        label["class"] = ["feature-intro-label"]
        label.string = "メモ"
        p.append(label)
        p.append(summary)
        if input_text or output_text:
            br = soup.new_tag("br")
            p.append(br)
            io_span = soup.new_tag("span")
            io_span["class"] = ["feature-intro-io"]
            if input_text:
                io_in = soup.new_tag("strong")
                io_in.string = "入力:"
                io_span.append(io_in)
                io_span.append(f" {input_text}　")
            if output_text:
                io_out = soup.new_tag("strong")
                io_out.string = "出力:"
                io_span.append(io_out)
                io_span.append(f" {output_text}")
            p.append(io_span)
        heading.insert_after(p)
    # Unwrap our wrapper div
    return root.decode_contents() if root.name == "div" else str(soup)


def image_figure(item: dict, image_path_prefix: str) -> str:
    prompt = html.escape(item["prompt"])
    return f"""
<figure class="image-shell" data-image-id="{html.escape(item['id'])}">
  <img src="{image_path_prefix}{html.escape(item['filename'])}" alt="{html.escape(item['alt'])}" loading="lazy" decoding="async">
  <figcaption>{html.escape(item['caption'])}</figcaption>
  <details class="image-brief">
    <summary>この画像の制作指示を見る</summary>
    <p><strong>配置:</strong> {html.escape(item['placement'])}</p>
    <p><strong>種類:</strong> {html.escape(item['kind'])}</p>
    <p><strong>設定:</strong> {html.escape(item['size'])} / {html.escape(item['quality'])} / {html.escape(item['output_format'])}</p>
    <pre>{prompt}</pre>
  </details>
</figure>
"""


def render_reference(body: str, prefix: str, features: list[dict] | None = None) -> str:
    rendered = md_renderer()(body)
    rendered = add_heading_ids(rendered, prefix)
    if features:
        rendered = inject_feature_intros(rendered, features)
    return rendered


def story_paragraphs(text: str) -> str:
    return "".join(f"<p>{html.escape(p.strip())}</p>" for p in text.split("\n\n") if p.strip())


def features_html(meta: dict) -> str:
    items = meta.get("features") or []
    if not items:
        return ""
    cards = []
    for f in items:
        cards.append(
            '<article class="feature-card">'
            f'<h3>{html.escape(f["name"])}</h3>'
            f'<p class="feature-summary">{html.escape(f["summary"])}</p>'
            '<dl class="feature-io">'
            f'<dt>入力</dt><dd>{html.escape(f["input"])}</dd>'
            f'<dt>出力</dt><dd>{html.escape(f["output"])}</dd>'
            '</dl>'
            '</article>'
        )
    return (
        '<section class="features" aria-label="この章の概観">'
        '<h2>この章の概観 ／ 何を扱い、何ができるか</h2>'
        '<p class="features-lede">この章で扱う機能と、それで何ができるようになるか。実装に入る前に、全体像をここでつかみます。</p>'
        f'<div class="features-grid">{"".join(cards)}</div>'
        '</section>'
    )


def usecases_html(meta: dict) -> str:
    items = meta.get("usecases") or []
    if not items:
        return ""
    cards = []
    for uc in items:
        cards.append(
            '<article class="usecase-card">'
            f'<h3>場面</h3><p>{html.escape(uc["situation"])}</p>'
            f'<h3>こう使う</h3><p>{html.escape(uc["action"])}</p>'
            f'<h3>得られるもの</h3><p>{html.escape(uc["benefit"])}</p>'
            '</article>'
        )
    return (
        '<section class="usecases" aria-label="こんな場面で使う">'
        '<h2>こんな場面で使う</h2>'
        '<p class="usecases-lede">章の内容が実務でどう活きるか。架空の場面・行動・効果の三点で示します。</p>'
        f'<div class="usecase-grid">{"".join(cards)}</div>'
        '</section>'
    )


def chapter_article(ch: Chapter, manifest: dict, image_prefix: str, include_extras: bool = True) -> str:
    lookup = manifest_lookup(manifest)
    meta = CHAPTER_META[ch.key]
    label = "終章" if ch.key == "final" else f"第{int(ch.key)}章"
    extras = []
    if include_extras:
        for x in EXTRA_VISUALS:
            if x["chapter"] == ch.key:
                extras.append(lookup[x["id"]])
    extra_html = ""
    if extras:
        extra_html = '<section class="reference"><h2>補助図の制作指示</h2>' + "".join(image_figure(x, image_prefix) for x in extras) + "</section>"
    return f"""
<article class="chapter" id="chapter-{html.escape(ch.key)}">
  <header class="chapter-head">
    <div class="eyebrow">{label}</div>
    <h1>{html.escape(ch.title)}</h1>
  </header>
  {features_html(meta)}
  {image_figure(lookup[f'chapter-{ch.key}'], image_prefix)}
  <section class="reference" aria-label="実装リファレンス">
    <h2>実装リファレンス</h2>
    {render_reference(ch.body, f'ch-{ch.key}', meta.get('features'))}
  </section>
  {extra_html}
  <section class="mission-takeaway" aria-label="体験ミッションとポイント">
    <div class="mt-mission"><h3>体験ミッション</h3><p><strong>次の一操作:</strong> {html.escape(meta['mission'])}</p></div>
    <div class="mt-takeaway"><h3>このページのポイント</h3><p>{html.escape(meta['takeaway'])}</p></div>
  </section>
  {usecases_html(meta)}
</article>
"""


PAGE_TEMPLATE = Template(r"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ title }}</title><meta name="description" content="{{ description }}">
{% if inline_assets %}<style>{{ css }}</style>{% else %}<link rel="stylesheet" href="{{ asset_prefix }}assets/styles.css">{% endif %}
</head><body><div class="progress" aria-hidden="true"><span></span></div>
<header class="site-header"><div class="inner"><button class="toc-toggle" type="button" aria-label="目次を開く" aria-controls="site-toc">☰ 目次</button><a class="brand" href="{{ home_href }}">Claude Code 教科書・ブログ版</a><nav><a href="{{ home_href }}">目次</a><a href="{{ complete_href }}">全章一括</a><a href="{{ image_guide_href }}">画像実装</a></nav></div></header>
<div class="toc-overlay" aria-hidden="true"></div>
{{ body }}
<footer class="site-footer"><div class="inner"><strong>Claude Code実践教科書 — ブログ完全版</strong><p>画像は補助情報です。本文、Alt、Captionのみでも内容が完結するよう設計しています。</p></div></footer>
{% if inline_assets %}<script>{{ js }}</script>{% else %}<script src="{{ asset_prefix }}assets/app.js"></script>{% endif %}
</body></html>""")


def build_toc(parts: list[Part], chapters: list[Chapter], chapter_prefix: str | None = None) -> str:
    """Build a TOC. chapter_prefix=None means anchors in the complete page.

    On the home page, pass chapter_prefix="chapters/" so part links stay local
    anchors while chapter links open their individual pages.
    """
    chapters_by_part: dict[int, list[Chapter]] = {}
    for ch in chapters:
        chapters_by_part.setdefault(ch.part, []).append(ch)
    links: list[str] = ['<button class="toc-drawer-close" type="button" aria-label="目次を閉じる">×</button>', "<h2>目次</h2>"]
    if chapter_prefix is None:
        links.append('<a class="part-link course-link" href="#course-overview">14レッスン体験コース</a>')
    for part in parts:
        links.append(f'<a class="part-link" href="#part-{part.number}">第{part.number}部 {html.escape(part.title)}</a>')
        for ch in chapters_by_part.get(part.number, []):
            label = "終章" if ch.key == "final" else f"第{int(ch.key)}章"
            href = f"#chapter-{ch.key}" if chapter_prefix is None else f"{chapter_prefix}{ch.key}.html"
            links.append(f'<a href="{href}">{label} {html.escape(ch.title)}</a>')
    return "".join(links)


def intro_html(preamble: str, manifest: dict, image_prefix: str) -> str:
    lookup = manifest_lookup(manifest)
    chars = "".join(
        f'<article class="card"><div class="eyebrow">{html.escape(c["role"])}</div><h3>{html.escape(c["name"])}</h3><p>{html.escape(c["description"])}</p></article>'
        for c in CHARACTERS
    )
    preamble_html = render_reference(strip_original_title(preamble), "preface")
    return f"""
<section class="hero"><div class="hero-grid"><div><div class="eyebrow">Practical edition</div><h1>Claude Code実践教科書<br>ブログ完全版</h1><p class="lede">『使えている』から、『直せる・説明できる・安全に配れる』へ。最初の一操作から、Skills、Hooks、MCP、HTML、全社ハーネスまでを実装可能な粒度で扱います。</p><div class="hero-actions"><a class="button primary" href="#course-overview">14レッスンで始める</a><a class="button" href="#part-0">第0部から読む</a></div></div>{image_figure(lookup['cover-main'], image_prefix)}</div></section>
<section class="hero"><div class="chapter"><header class="chapter-head"><div class="eyebrow">Before you start</div><h1>原典から引き継ぐ前提</h1></header><div class="reference">{preamble_html}</div></div></section>
"""


def course_section_html(chapter_prefix: str = "") -> str:
    """14レッスン体験コース overview. chapter_prefix='' for complete.html, 'chapters/' for index."""
    def chap_anchor(c) -> str:
        if c == "final":
            return f'{chapter_prefix}final.html' if chapter_prefix else "#chapter-final"
        key = f"{int(c):02d}"
        return f'{chapter_prefix}{key}.html' if chapter_prefix else f"#chapter-{key}"

    def chap_label(c) -> str:
        return "終章" if c == "final" else f"第{int(c)}章"

    cards = []
    for lesson in LESSON_COURSE:
        chip_links = " ".join(
            f'<a class="course-chip" href="{chap_anchor(c)}">{chap_label(c)}</a>'
            for c in lesson["chapters"][:6]
        )
        more = "" if len(lesson["chapters"]) <= 6 else f'<span class="course-chip more">＋{len(lesson["chapters"]) - 6}章</span>'
        cards.append(
            f'<article class="course-card">'
            f'<div class="course-card-head"><span class="course-id">{html.escape(lesson["id"])}</span>'
            f'<span class="course-min">約{lesson["minutes"]}分</span></div>'
            f'<h3>{html.escape(lesson["title"])}</h3>'
            f'<p class="course-objective">{html.escape(lesson["objective"])}</p>'
            f'<div class="course-chapters">{chip_links}{more}</div>'
            f'<p class="course-note">{html.escape(lesson["note"])}</p>'
            f'</article>'
        )
    return (
        '<section class="course-overview" id="course-overview">'
        '<div class="course-head">'
        '<div class="eyebrow">体験コース／14レッスン</div>'
        '<h2>0から順番に手を動かす学習ルート</h2>'
        '<p class="course-lede">Claude Codeを使ったことが無い人が、F00から順番に14レッスンで「直せる・説明できる・安全に配れる」までを体験するコース設計です。各レッスンに対応する本書の章へジャンプできます。</p>'
        '<p class="course-lede course-trigger">スキル<code>claude-code-handson-navigator</code>と連動。Claude Code（または Cursor／Codex）で「Claude Codeを0から学びたい」と話しかけると、このコース順に1ターン1操作で伴走します。</p>'
        '</div>'
        f'<div class="course-grid">{"".join(cards)}</div>'
        '</section>'
    )


def part_usecase_html(meta: dict) -> str:
    uc = meta.get("usecase")
    if not uc:
        return ""
    return (
        '<section class="part-usecase" aria-label="この部で得られる場面">'
        '<h3>この部で得られる場面</h3>'
        f'<div class="pu-item"><h4>場面</h4><p>{html.escape(uc["situation"])}</p></div>'
        f'<div class="pu-item"><h4>こう使う</h4><p>{html.escape(uc["action"])}</p></div>'
        f'<div class="pu-item"><h4>得られるもの</h4><p>{html.escape(uc["benefit"])}</p></div>'
        '</section>'
    )


def part_html(part: Part, chapters: list[Chapter], manifest: dict, image_prefix: str) -> str:
    lookup = manifest_lookup(manifest)
    meta = PART_META[part.number]
    articles = "".join(chapter_article(ch, manifest, image_prefix) for ch in chapters)
    return f"""
<section class="part" id="part-{part.number}">
  <header class="part-header"><div class="eyebrow">Part {part.number}</div><h2>第{part.number}部　{html.escape(part.title)}</h2></header>
  {part_usecase_html(meta)}
  {image_figure(lookup[f'part-{part.number:02d}'], image_prefix)}
  {articles}
</section>
"""


def write_page(path: Path, title: str, description: str, body: str, *, asset_prefix: str, home_href: str, complete_href: str, image_guide_href: str, inline_assets: bool = False) -> None:
    page = PAGE_TEMPLATE.render(
        title=title,
        description=description,
        body=body,
        asset_prefix=asset_prefix,
        home_href=home_href,
        complete_href=complete_href,
        image_guide_href=image_guide_href,
        inline_assets=inline_assets,
        css=CSS,
        js=JS,
    )
    path.write_text(page, encoding="utf-8")


def build_site(preamble: str, parts: list[Part], chapters: list[Chapter], manifest: dict) -> None:
    SITE.mkdir(parents=True, exist_ok=True)
    CHAPTER_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    (ASSET_DIR / "styles.css").write_text(CSS, encoding="utf-8")
    (ASSET_DIR / "app.js").write_text(JS, encoding="utf-8")

    chapters_by_part: dict[int, list[Chapter]] = {}
    for ch in chapters:
        chapters_by_part.setdefault(ch.part, []).append(ch)

    home_main = intro_html(preamble, manifest, "images/")
    home_main += '<div class="layout"><aside class="toc" id="site-toc">' + build_toc(parts, chapters, "chapters/") + '</aside><main class="content">'
    for part in parts:
        meta = PART_META[part.number]
        cards = []
        for ch in chapters_by_part.get(part.number, []):
            label = "終章" if ch.key == "final" else f"第{int(ch.key)}章"
            cards.append(f'<a class="card" href="chapters/{ch.key}.html"><div class="eyebrow">{label}</div><h3>{html.escape(ch.title)}</h3><p>{html.escape(CHAPTER_META[ch.key]["takeaway"])}</p></a>')
        home_main += f'<section class="part" id="part-{part.number}"><header class="part-header"><div class="eyebrow">Part {part.number}</div><h2>第{part.number}部　{html.escape(part.title)}</h2></header>{part_usecase_html(meta)}{image_figure(manifest_lookup(manifest)[f"part-{part.number:02d}"], "images/")}<div class="card-grid">{"".join(cards)}</div></section>'
    home_main += '</main></div>'
    write_page(SITE / "index.html", "Claude Code実践教科書 — ブログ完全版", "Claude Codeを物語と実装で学ぶ完全版ブログ", home_main, asset_prefix="", home_href="index.html", complete_href="complete.html", image_guide_href="image-pipeline.html")

    complete_body = intro_html(preamble, manifest, "images/")
    complete_body += '<div class="layout"><aside class="toc" id="site-toc">' + build_toc(parts, chapters, None) + '</aside><main class="content">'
    complete_body += course_section_html("")
    for part in parts:
        complete_body += part_html(part, chapters_by_part.get(part.number, []), manifest, "images/")
    complete_body += '<p class="source-note">本版は、元教科書の全章・全小見出し・コードブロックを保持し、各章に機能概観・ユースケース・体験ミッションを追加しています。</p></main></div>'
    write_page(SITE / "complete.html", "Claude Code実践教科書 — 全章一括", "機能と実装を一つのHTMLで読む完全版", complete_body, asset_prefix="", home_href="index.html", complete_href="complete.html", image_guide_href="image-pipeline.html", inline_assets=True)

    pipeline_md_path = ROOT / "IMAGE_PIPELINE.md"
    if pipeline_md_path.exists():
        pipeline_html = render_reference(pipeline_md_path.read_text(encoding="utf-8"), "image-pipeline")
        pipeline_body = '<div class="layout"><aside class="toc" id="site-toc"><h2>画像制作</h2><a href="#image-pipeline-s1">API上の名称</a><a href="index.html">全体目次</a></aside><main class="content"><article class="chapter"><header class="chapter-head"><div class="eyebrow">GPT Image 2</div><h1>画像制作・差し込みパイプライン</h1></header><div class="reference">' + pipeline_html + '</div></article></main></div>'
        write_page(SITE / "image-pipeline.html", "GPT Image 2 画像制作パイプライン", "ブログ挿絵をGPT Image 2 APIで生成し差し込む手順", pipeline_body, asset_prefix="", home_href="index.html", complete_href="complete.html", image_guide_href="image-pipeline.html")

    for idx, ch in enumerate(chapters):
        prev_ch = chapters[idx - 1] if idx > 0 else None
        next_ch = chapters[idx + 1] if idx + 1 < len(chapters) else None
        nav = '<nav class="chapter-nav">'
        nav += (f'<a href="{prev_ch.key}.html">← {html.escape(prev_ch.title)}</a>' if prev_ch else '<span></span>')
        nav += (f'<a href="{next_ch.key}.html">{html.escape(next_ch.title)} →</a>' if next_ch else '<a href="../index.html">目次へ →</a>')
        nav += '</nav>'
        body = '<div class="layout"><aside class="toc" id="site-toc"><h2>この章</h2><a href="#chapter-' + ch.key + '">' + html.escape(ch.title) + '</a><a href="../index.html">全体目次</a><a href="../complete.html#chapter-' + ch.key + '">一括版で開く</a></aside><main class="content">'
        body += chapter_article(ch, manifest, "../images/") + nav + '</main></div>'
        write_page(CHAPTER_DIR / f"{ch.key}.html", f"{ch.raw_title} — ブログ版", CHAPTER_META[ch.key]["takeaway"], body, asset_prefix="../", home_href="../index.html", complete_href="../complete.html", image_guide_href="../image-pipeline.html")


def build_coverage(original_text: str, blog_md: str, chapters: list[Chapter], manifest: dict) -> str:
    original_h2 = re.findall(r"^## .+$", original_text, flags=re.M)
    missing_h2 = [h for h in original_h2 if h not in blog_md]
    original_fences = original_text.count("```")
    blog_fences = blog_md.count("```")
    return f"""# Blog Edition Coverage Report

- Original chapter count: {len(chapters)}
- Blog chapter count: {len(re.findall(r'^# (?:第\d+章|終章)', blog_md, flags=re.M))}
- Original subsection headings: {len(original_h2)}
- Missing original subsection headings: {len(missing_h2)}
- Original code-fence markers: {original_fences}
- Blog code-fence markers: {blog_fences}
- Image directives: {len(manifest['images'])}
- Core image directives: {sum(1 for i in manifest['images'] if i['tier'] == 'core')}
- Chapter image directives: {sum(1 for i in manifest['images'] if i['tier'] == 'chapter')}

## Missing subsection headings

{chr(10).join('- ' + h for h in missing_h2) if missing_h2 else 'None. All original subsection headings are retained.'}

## Validation result

{'PASS' if not missing_h2 and blog_fences >= original_fences else 'REVIEW REQUIRED'}
"""


def main() -> None:
    original_text = SOURCE.read_text(encoding="utf-8")
    preamble, parts, chapters = parse_source(original_text)
    expected = set(CHAPTER_META)
    actual = {c.key for c in chapters}
    if expected != actual:
        raise SystemExit(f"Chapter metadata mismatch: missing={actual-expected}, extra={expected-actual}")
    manifest = make_manifest(parts, chapters)
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    blog_md = build_markdown(preamble, parts, chapters, manifest)
    OUT_MD.write_text(blog_md, encoding="utf-8")
    build_site(preamble, parts, chapters, manifest)
    COVERAGE_PATH.write_text(build_coverage(original_text, blog_md, chapters, manifest), encoding="utf-8")
    print(json.dumps({
        "markdown": str(OUT_MD),
        "site": str(SITE),
        "chapters": len(chapters),
        "images": len(manifest["images"]),
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
