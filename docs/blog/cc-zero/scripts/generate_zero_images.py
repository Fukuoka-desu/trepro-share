#!/usr/bin/env python3
"""Generate cc-zero illustrations from image_manifest.json.

The API key is read only from OPENAI_API_KEY. It is never written to disk or
printed. Existing output files are skipped unless --force is supplied, and
failed assets do not stop the remaining batch.
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
    parser = argparse.ArgumentParser(
        description="Generate Claude Code zero-beginner textbook images."
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--ids", help="Comma-separated image IDs.")
    parser.add_argument("--model", default=None)
    parser.add_argument(
        "--quality",
        choices=["manifest", "low", "medium", "high"],
        default="manifest",
    )
    parser.add_argument("--size", default=None)
    parser.add_argument("--format", choices=["png", "jpeg", "webp"], default=None)
    parser.add_argument("--compression", type=int, default=88)
    parser.add_argument("--moderation", choices=["auto", "low"], default="auto")
    parser.add_argument("--max-retries", type=int, default=4)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--list", action="store_true")
    return parser.parse_args()


def load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    images = data.get("images")
    if not isinstance(images, list):
        raise ValueError("Manifest must contain an images array.")
    required = {"id", "size", "quality", "format", "prompt", "alt", "caption"}
    seen: set[str] = set()
    for index, item in enumerate(images, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"images[{index}] must be an object.")
        missing = sorted(required - item.keys())
        if missing:
            raise ValueError(f"images[{index}] is missing: {', '.join(missing)}")
        image_id = item["id"]
        if image_id in seen:
            raise ValueError(f"Duplicate image ID: {image_id}")
        seen.add(image_id)
    return data


def select_images(
    manifest: dict[str, Any], args: argparse.Namespace
) -> list[dict[str, Any]]:
    images = manifest["images"]
    if not args.ids:
        return images
    wanted = {value.strip() for value in args.ids.split(",") if value.strip()}
    selected = [item for item in images if item["id"] in wanted]
    missing = wanted - {item["id"] for item in selected}
    if missing:
        raise ValueError(f"Unknown image IDs: {', '.join(sorted(missing))}")
    return selected


def log_event(payload: dict[str, Any]) -> None:
    event = {"timestamp": datetime.now(timezone.utc).isoformat(), **payload}
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def exception_details(
    exception: Exception,
) -> tuple[int | None, str | None, str | None]:
    status = getattr(exception, "status_code", None)
    code = getattr(exception, "code", None)
    request_id = getattr(exception, "request_id", None)
    body = getattr(exception, "body", None)
    if isinstance(body, dict):
        error = body.get("error") if isinstance(body.get("error"), dict) else body
        code = code or error.get("code")
    return status, code, request_id


def generate_one(
    client: Any,
    item: dict[str, Any],
    *,
    model: str,
    quality: str,
    size: str,
    output_format: str,
    compression: int,
    moderation: str,
    max_retries: int,
) -> tuple[bytes, str | None]:
    request: dict[str, Any] = {
        "model": model,
        "prompt": item["prompt"],
        "size": size,
        "quality": quality,
        "output_format": output_format,
        "moderation": moderation,
        "n": 1,
    }
    if output_format in {"jpeg", "webp"}:
        request["output_compression"] = compression

    last_exception: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            result = client.images.generate(**request)
            encoded = getattr(result.data[0], "b64_json", None)
            if not encoded:
                raise RuntimeError("The API response did not contain data[0].b64_json")
            return base64.b64decode(encoded), getattr(result, "_request_id", None)
        except Exception as exception:  # SDK exception classes vary by version.
            last_exception = exception
            status, code, request_id = exception_details(exception)
            if code == "moderation_blocked":
                raise RuntimeError(
                    "Image request was blocked by moderation "
                    f"(request_id={request_id}); prompt revision is required."
                ) from exception
            if status not in TRANSIENT_STATUS or attempt >= max_retries:
                raise
            delay = min(30.0, (2**attempt) + random.random())
            print(
                f"  transient error status={status}; retrying in {delay:.1f}s",
                file=sys.stderr,
            )
            time.sleep(delay)
    assert last_exception is not None
    raise last_exception


def main() -> int:
    args = parse_args()
    try:
        manifest = load_manifest(args.manifest)
        selected = select_images(manifest, args)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exception:
        print(f"MANIFEST ERROR: {exception}", file=sys.stderr)
        return 2

    model = args.model or manifest.get("default_model", "gpt-image-2")
    if args.list or args.dry_run:
        for item in selected:
            quality = item["quality"] if args.quality == "manifest" else args.quality
            size = args.size or item["size"]
            output_format = args.format or item["format"]
            filename = item.get("filename", f"{item['id']}.{output_format}")
            print(
                f"{item['id']}: {filename} | {size} | {quality} | "
                f"{output_format} | {item.get('placement', '')}"
            )
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
    generated = 0
    skipped = 0
    failed = 0

    for index, item in enumerate(selected, start=1):
        quality = item["quality"] if args.quality == "manifest" else args.quality
        size = args.size or item["size"]
        output_format = args.format or item["format"]
        filename = item.get("filename", f"{item['id']}.{output_format}")
        output = args.output_dir / filename
        prompt_hash = hashlib.sha256(item["prompt"].encode("utf-8")).hexdigest()

        if output.exists() and not args.force:
            print(f"[{index}/{len(selected)}] skip {item['id']} (exists)")
            skipped += 1
            continue

        print(f"[{index}/{len(selected)}] generate {item['id']} -> {output.name}")
        started = time.monotonic()
        try:
            data, request_id = generate_one(
                client,
                item,
                model=model,
                quality=quality,
                size=size,
                output_format=output_format,
                compression=args.compression,
                moderation=args.moderation,
                max_retries=args.max_retries,
            )
            temporary = output.with_suffix(output.suffix + ".tmp")
            temporary.write_bytes(data)
            temporary.replace(output)
            elapsed = round(time.monotonic() - started, 3)
            log_event(
                {
                    "event": "generated",
                    "id": item["id"],
                    "file": str(output.relative_to(ROOT)),
                    "model": model,
                    "size": size,
                    "quality": quality,
                    "format": output_format,
                    "prompt_sha256": prompt_hash,
                    "request_id": request_id,
                    "bytes": len(data),
                    "elapsed_seconds": elapsed,
                }
            )
            generated += 1
        except Exception as exception:
            elapsed = round(time.monotonic() - started, 3)
            status, code, request_id = exception_details(exception)
            log_event(
                {
                    "event": "failed",
                    "id": item["id"],
                    "model": model,
                    "prompt_sha256": prompt_hash,
                    "status": status,
                    "code": code,
                    "request_id": request_id,
                    "elapsed_seconds": elapsed,
                    "error": str(exception),
                }
            )
            print(f"  FAILED: {exception}", file=sys.stderr)
            failed += 1

    print(
        f"completed: generated={generated}, skipped={skipped}, "
        f"failed={failed}, selected={len(selected)}"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
