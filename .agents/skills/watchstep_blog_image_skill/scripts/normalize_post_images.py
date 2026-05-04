#!/usr/bin/env python3
"""
Normalize local images in a Hugo post index.md.

Behavior:
- Finds Markdown image links in order.
- Renames referenced local image files to image_1.png, image_2.png, ...
- Replaces Markdown image syntax with:
  <img width="500" height="auto" alt="" src="image_1.png" />

Usage:
  python3 scripts/normalize_post_images.py content/posts/my-post/index.md
  python3 scripts/normalize_post_images.py content/posts/my-post/index.md --dry-run
"""

from __future__ import annotations

import argparse
import html
import os
import re
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg"}
MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\n]+)\)")


@dataclass
class ImageRef:
    span: tuple[int, int]
    original_markup: str
    alt: str
    raw_target: str
    source_path: Path | None
    new_src: str | None
    replacement: str | None


@dataclass
class RenameOp:
    source: Path
    target: Path


def parse_target(raw_target: str) -> str:
    """Return only the URL/path part, ignoring optional title text for common cases."""
    value = raw_target.strip()

    if value.startswith("<") and ">" in value:
        return value[1:value.index(">")].strip()

    # Common Markdown form: ![alt](path "title")
    # This intentionally handles simple quoted-title cases.
    for quote in [' "', " '"]:
        marker_index = value.find(quote)
        if marker_index != -1:
            return value[:marker_index].strip()

    return value


def is_remote_or_special(target: str) -> bool:
    parsed = urlparse(target)
    return parsed.scheme in {"http", "https", "data", "mailto"}


def strip_query_and_fragment(target: str) -> str:
    parsed = urlparse(target)
    if parsed.scheme or parsed.netloc:
        return target
    return parsed.path


def resolve_local_image(md_dir: Path, raw_target: str) -> Path | None:
    target = parse_target(raw_target)

    if is_remote_or_special(target):
        return None

    path_only = strip_query_and_fragment(target)
    decoded = unquote(path_only)

    candidates = [
        md_dir / decoded,
        md_dir / Path(decoded).name,
        md_dir / path_only,
        md_dir / Path(path_only).name,
    ]

    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except OSError:
            continue

        if resolved.exists() and resolved.is_file() and resolved.suffix.lower() in IMAGE_EXTENSIONS:
            return resolved

    return None


def make_html_img(src: str, alt: str, width: int, preserve_alt: bool) -> str:
    alt_value = alt if preserve_alt else ""
    return (
        f'<img width="{width}" height="auto" '
        f'alt="{html.escape(alt_value, quote=True)}" '
        f'src="{html.escape(src, quote=True)}" />'
    )


def collect_refs_and_ops(
    text: str,
    md_path: Path,
    width: int,
    prefix: str,
    preserve_alt: bool,
) -> tuple[list[ImageRef], list[RenameOp], list[str]]:
    md_dir = md_path.parent.resolve()
    refs: list[ImageRef] = []
    ops: list[RenameOp] = []
    warnings: list[str] = []

    seen_sources: dict[Path, str] = {}
    next_index = 1

    for match in MARKDOWN_IMAGE_RE.finditer(text):
        alt = match.group(1)
        raw_target = match.group(2)
        source_path = resolve_local_image(md_dir, raw_target)

        if source_path is None:
            target = parse_target(raw_target)
            if not is_remote_or_special(target):
                warnings.append(f"Image not found, left unchanged: {raw_target}")
            refs.append(
                ImageRef(
                    span=match.span(),
                    original_markup=match.group(0),
                    alt=alt,
                    raw_target=raw_target,
                    source_path=None,
                    new_src=None,
                    replacement=None,
                )
            )
            continue

        if source_path not in seen_sources:
            suffix = source_path.suffix.lower()
            if suffix == ".jpeg":
                suffix = ".jpg"

            new_name = f"{prefix}{next_index}{suffix}"
            seen_sources[source_path] = new_name
            next_index += 1

            target_path = md_dir / new_name
            if source_path.resolve() != target_path.resolve():
                ops.append(RenameOp(source=source_path, target=target_path.resolve()))

        new_src = seen_sources[source_path]
        replacement = make_html_img(new_src, alt, width, preserve_alt)

        refs.append(
            ImageRef(
                span=match.span(),
                original_markup=match.group(0),
                alt=alt,
                raw_target=raw_target,
                source_path=source_path,
                new_src=new_src,
                replacement=replacement,
            )
        )

    return refs, ops, warnings


def apply_text_replacements(text: str, refs: list[ImageRef]) -> str:
    pieces: list[str] = []
    cursor = 0

    for ref in refs:
        start, end = ref.span
        pieces.append(text[cursor:start])
        pieces.append(ref.replacement if ref.replacement is not None else ref.original_markup)
        cursor = end

    pieces.append(text[cursor:])
    return "".join(pieces)


def validate_ops(ops: list[RenameOp]) -> None:
    sources = {op.source.resolve() for op in ops}

    for op in ops:
        if op.target.exists() and op.target.resolve() not in sources:
            raise FileExistsError(
                f"Refusing to overwrite existing unrelated file: {op.target}"
            )


def perform_renames(ops: list[RenameOp], dry_run: bool) -> None:
    validate_ops(ops)

    if dry_run:
        for op in ops:
            print(f"[dry-run] rename: {op.source.name} -> {op.target.name}")
        return

    temp_ops: list[tuple[Path, Path, Path]] = []

    for op in ops:
        source = op.source.resolve()
        target = op.target.resolve()

        if source == target:
            continue

        temp_name = f".{source.name}.normalizing-{uuid.uuid4().hex}.tmp"
        temp_path = source.with_name(temp_name)
        source.rename(temp_path)
        temp_ops.append((temp_path, target, source))

    try:
        for temp_path, target, _original_source in temp_ops:
            target.parent.mkdir(parents=True, exist_ok=True)
            temp_path.rename(target)
    except Exception:
        # Best-effort rollback for files that have not been moved to final destinations yet.
        for temp_path, _target, original_source in temp_ops:
            if temp_path.exists() and not original_source.exists():
                temp_path.rename(original_source)
        raise


def normalize_post(
    input_path: Path,
    width: int,
    prefix: str,
    preserve_alt: bool,
    dry_run: bool,
) -> int:
    md_path = input_path
    if input_path.is_dir():
        md_path = input_path / "index.md"

    if not md_path.exists():
        print(f"Error: index.md not found: {md_path}", file=sys.stderr)
        return 1

    if md_path.name != "index.md":
        print(f"Warning: target file is not named index.md: {md_path}", file=sys.stderr)

    text = md_path.read_text(encoding="utf-8")
    refs, ops, warnings = collect_refs_and_ops(
        text=text,
        md_path=md_path,
        width=width,
        prefix=prefix,
        preserve_alt=preserve_alt,
    )
    new_text = apply_text_replacements(text, refs)

    changed_refs = [ref for ref in refs if ref.replacement is not None]

    if not changed_refs:
        print("No local Markdown image references found.")
        for warning in warnings:
            print(f"Warning: {warning}", file=sys.stderr)
        return 0

    print(f"Found {len(changed_refs)} local Markdown image reference(s).")
    print(f"Planned rename operation(s): {len(ops)}")

    for warning in warnings:
        print(f"Warning: {warning}", file=sys.stderr)

    perform_renames(ops, dry_run=dry_run)

    if dry_run:
        if new_text != text:
            print("[dry-run] index.md would be updated.")
        return 0

    if new_text != text:
        md_path.write_text(new_text, encoding="utf-8")
        print(f"Updated: {md_path}")
    else:
        print("No text changes needed.")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rename post images by index.md order and convert Markdown images to HTML tags."
    )
    parser.add_argument(
        "path",
        type=Path,
        help="Path to a post directory or its index.md file.",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=500,
        help="HTML image width. Default: 500",
    )
    parser.add_argument(
        "--prefix",
        default="image_",
        help="Output image filename prefix. Default: image_",
    )
    parser.add_argument(
        "--preserve-alt",
        action="store_true",
        help="Use Markdown alt text in HTML alt instead of forcing alt=\"\".",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without editing files.",
    )

    args = parser.parse_args()

    try:
        return normalize_post(
            input_path=args.path,
            width=args.width,
            prefix=args.prefix,
            preserve_alt=args.preserve_alt,
            dry_run=args.dry_run,
        )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
