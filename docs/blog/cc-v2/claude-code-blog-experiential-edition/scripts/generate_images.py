#!/usr/bin/env python3
"""Generate blog images from image_manifest.json with OpenAI's GPT Image API.

Usage examples:
  python scripts/generate_images.py --tier core --quality low --dry-run
  python scripts/generate_images.py --tier core --quality low
  python scripts/generate_images.py --ids cover-main,chapter-04 --quality medium --force
  python scripts/generate_images.py --tier all --model gpt-image-2-2026-04-21

The API key is read only from OPENAI_API_KEY. It is never written to disk.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "image_manifest.json"
DEFAULT_OUTPUT = ROOT / "site" / "images"
LOG_PATH = ROOT / "image-generation-log.jsonl"

TRANSIENT_STATUS = {408, 409, 429, 500, 502, 503, 504}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate blog images from the manifest.")
    p.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    p.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    p.add_argument("--tier", choices=["core", "chapter", "all"], default="core")
    p.add_argument("--ids", help="Comma-separated image IDs. Overrides --tier selection.")
    p.add_argument("--model", default=None, help="Default: manifest default_model (gpt-image-2).")
    p.add_argument("--quality", choices=["manifest", "low", "medium", "high"], default="manifest")
    p.add_argument("--size", default=None, help="Override all sizes, e.g. 1536x1024.")
    p.add_argument("--format", choices=["png", "jpeg", "webp"], default=None)
    p.add_argument("--compression", type=int, default=88, help="JPEG/WebP compression, 0-100.")
    p.add_argument("--moderation", choices=["auto", "low"], default="auto")
    p.add_argument("--max-retries", type=int, default=4)
    p.add_argument("--force", action="store_true", help="Regenerate even if output exists.")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--list", action="store_true", help="List selected assets and exit.")
    return p.parse_args()


def load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data.get("images"), list):
        raise ValueError("Manifest must contain an images array.")
    return data


def select_images(manifest: dict[str, Any], args: argparse.Namespace) -> list[dict[str, Any]]:
    images = manifest["images"]
    if args.ids:
        wanted = {x.strip() for x in args.ids.split(",") if x.strip()}
        selected = [i for i in images if i["id"] in wanted]
        missing = wanted - {i["id"] for i in selected}
        if missing:
            raise ValueError(f"Unknown image IDs: {', '.join(sorted(missing))}")
        return selected
    if args.tier == "all":
        return images
    return [i for i in images if i.get("tier") == args.tier]


def log_event(payload: dict[str, Any]) -> None:
    payload = {"timestamp": datetime.now(timezone.utc).isoformat(), **payload}
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def exception_details(exc: Exception) -> tuple[int | None, str | None, str | None]:
    status = getattr(exc, "status_code", None)
    code = getattr(exc, "code", None)
    request_id = getattr(exc, "request_id", None)
    body = getattr(exc, "body", None)
    if isinstance(body, dict):
        err = body.get("error") if isinstance(body.get("error"), dict) else body
        code = code or err.get("code")
    return status, code, request_id


def generate_one(client: Any, item: dict[str, Any], *, model: str, quality: str, size: str, output_format: str, compression: int, moderation: str, max_retries: int) -> tuple[bytes, str | None]:
    kwargs: dict[str, Any] = {
        "model": model,
        "prompt": item["prompt"],
        "size": size,
        "quality": quality,
        "output_format": output_format,
        "moderation": moderation,
        "n": 1,
    }
    if output_format in {"jpeg", "webp"}:
        kwargs["output_compression"] = compression

    last_exc: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            result = client.images.generate(**kwargs)
            datum = result.data[0]
            encoded = getattr(datum, "b64_json", None)
            if not encoded:
                raise RuntimeError("The API response did not contain data[0].b64_json")
            request_id = getattr(result, "_request_id", None)
            return base64.b64decode(encoded), request_id
        except Exception as exc:  # SDK exception classes vary by version.
            last_exc = exc
            status, code, request_id = exception_details(exc)
            if code == "moderation_blocked":
                raise RuntimeError(
                    f"Image request was blocked by moderation (request_id={request_id}). "
                    "Revise the prompt; do not retry unchanged."
                ) from exc
            if status not in TRANSIENT_STATUS or attempt >= max_retries:
                raise
            delay = min(30.0, (2 ** attempt) + random.random())
            print(f"  transient error status={status}; retrying in {delay:.1f}s", file=sys.stderr)
            time.sleep(delay)
    assert last_exc is not None
    raise last_exc


def main() -> int:
    args = parse_args()
    manifest = load_manifest(args.manifest)
    selected = select_images(manifest, args)
    model = args.model or manifest.get("default_model", "gpt-image-2")

    if args.list or args.dry_run:
        for item in selected:
            quality = item.get("quality", "medium") if args.quality == "manifest" else args.quality
            size = args.size or item.get("size", "1536x1024")
            fmt = args.format or item.get("output_format", "webp")
            print(f"{item['id']}: {item['filename']} | {size} | {quality} | {fmt} | {item.get('placement','')}")
        if args.dry_run:
            print(f"DRY RUN: {len(selected)} request(s), model={model}")
        return 0

    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set.", file=sys.stderr)
        return 2

    try:
        from openai import OpenAI
    except ImportError:
        print("Install the SDK first: python -m pip install 'openai>=2.0.0'", file=sys.stderr)
        return 2

    args.output_dir.mkdir(parents=True, exist_ok=True)
    client = OpenAI()
    ok = 0
    failed = 0

    for index, item in enumerate(selected, 1):
        out = args.output_dir / item["filename"]
        quality = item.get("quality", "medium") if args.quality == "manifest" else args.quality
        size = args.size or item.get("size", "1536x1024")
        fmt = args.format or item.get("output_format", "webp")
        prompt_hash = hashlib.sha256(item["prompt"].encode("utf-8")).hexdigest()

        if out.exists() and not args.force:
            print(f"[{index}/{len(selected)}] skip {item['id']} (exists)")
            continue

        print(f"[{index}/{len(selected)}] generate {item['id']} -> {out.name}")
        started = time.monotonic()
        try:
            data, request_id = generate_one(
                client,
                item,
                model=model,
                quality=quality,
                size=size,
                output_format=fmt,
                compression=args.compression,
                moderation=args.moderation,
                max_retries=args.max_retries,
            )
            tmp = out.with_suffix(out.suffix + ".tmp")
            tmp.write_bytes(data)
            tmp.replace(out)
            elapsed = round(time.monotonic() - started, 3)
            log_event({
                "event": "generated",
                "id": item["id"],
                "file": str(out.relative_to(ROOT)),
                "model": model,
                "size": size,
                "quality": quality,
                "format": fmt,
                "prompt_sha256": prompt_hash,
                "request_id": request_id,
                "bytes": len(data),
                "elapsed_seconds": elapsed,
            })
            ok += 1
        except Exception as exc:
            elapsed = round(time.monotonic() - started, 3)
            status, code, request_id = exception_details(exc)
            log_event({
                "event": "failed",
                "id": item["id"],
                "model": model,
                "prompt_sha256": prompt_hash,
                "status": status,
                "code": code,
                "request_id": request_id,
                "elapsed_seconds": elapsed,
                "error": str(exc),
            })
            print(f"  FAILED: {exc}", file=sys.stderr)
            failed += 1

    print(f"completed: generated={ok}, failed={failed}, selected={len(selected)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
