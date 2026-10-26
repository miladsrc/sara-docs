#!/usr/bin/env python3
"""Relative markdown link checker for the Sara docs repository.

Checks [text](target) links inside living docs (archive/ excluded - frozen
history keeps its original, possibly dead, links).

Skipped targets: http(s)://, mailto:, tel:, and pure #anchors.
Anchors are stripped before resolution: README.md#section -> README.md

Exit 0 when every link resolves, 1 otherwise.
Usage: python scripts/check_links.py [--root DIR]
"""
from __future__ import annotations

import argparse
import os
import re
import sys

SKIP_DIRS = {".git", ".idea", ".venv", "__pycache__", "node_modules", ".pytest_cache"}
SKIP_SCHEMES = ("http://", "https://", "mailto:", "tel:", "ftp://")

# [label](target) - not images, which begin with !
LINK = re.compile(r"(?<!!)\[[^\]\n]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def _iter_docs(root: str):
    for dirpath, dirnames, files in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in files:
            if fn.lower().endswith(".md"):
                yield os.path.join(dirpath, fn)


def extract_targets(text: str) -> list[tuple[int, str]]:
    out = []
    for match in LINK.finditer(text):
        target = match.group(1).strip()
        line = text[: match.start()].count("\n") + 1
        out.append((line, target))
    return out


def resolve(doc_path: str, target: str, root: str) -> str | None:
    """Return the resolved absolute path, or None when the target is skippable."""
    if target.startswith(SKIP_SCHEMES) or target.startswith("#"):
        return None
    target = target.split("#", 1)[0].split("?", 1)[0]
    if not target:
        return None
    # Percent-encoding (spaces) and Windows separators.
    target = target.replace("%20", " ").replace("\\", "/")
    if target.startswith("/"):
        return os.path.normpath(os.path.join(root, target.lstrip("/")))
    return os.path.normpath(os.path.join(os.path.dirname(doc_path), target))


def scan(root: str) -> list[dict]:
    archive = os.path.join(root, "archive") + os.sep
    broken = []
    for doc in _iter_docs(root):
        if doc.startswith(archive):
            continue
        rel = os.path.relpath(doc, root).replace("\\", "/")
        try:
            with open(doc, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        for line, target in extract_targets(text):
            resolved = resolve(doc, target, root)
            if resolved is None:
                continue
            if not os.path.exists(resolved):
                broken.append({
                    "file": rel, "line": line, "target": target,
                    "resolved": os.path.relpath(resolved, root).replace("\\", "/"),
                })
    return broken


def report(broken: list[dict]) -> bool:
    if not broken:
        print("check_links: OK (all relative links resolve)")
        return True
    print("check_links: FAILED")
    for item in broken:
        print(f"  {item['file']}:{item['line']} -> {item['target']}  (resolved: {item['resolved']})")
    return False


def main(argv: list[str] | None = None) -> int:
    default_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parser = argparse.ArgumentParser(description="Check relative markdown links.")
    parser.add_argument("--root", default=default_root)
    args = parser.parse_args(argv)
    return 0 if report(scan(os.path.abspath(args.root))) else 1


if __name__ == "__main__":
    sys.exit(main())
