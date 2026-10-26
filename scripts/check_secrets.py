#!/usr/bin/env python3
"""Secret scan for the Sara docs repository.

Two tiers, because an archive of prose and a living operating manual have
different risk profiles:

  Tier A - high-confidence credential patterns. Scanned EVERYWHERE, including
           archive/. A leaked token in a frozen report is still a leaked token.
  Tier B - generic "assignment-looking" heuristics. Scanned only in LIVING docs
           (archive/ excluded), because archived reports legitimately discuss
           password policy in prose.

Exit 0 when clean, 1 when anything is found.
Usage: python scripts/check_secrets.py [--root DIR]
"""
from __future__ import annotations

import argparse
import os
import re
import sys

# --- Tier A: high-confidence credential shapes -------------------------------
TIER_A = [
    ("github-pat", re.compile(r"ghp_[A-Za-z0-9]{30,}")),
    ("github-fine-pat", re.compile(r"github_pat_[A-Za-z0-9_]{50,}")),
    ("gitlab-pat", re.compile(r"glpat-[A-Za-z0-9_\-]{20,}")),
    ("openai-key", re.compile(r"sk-[A-Za-z0-9]{20,}")),
    ("anthropic-key", re.compile(r"sk-ant-[A-Za-z0-9\-_]{20,}")),
    ("aws-access-key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("aws-secret-key", re.compile(r"(?i)aws_?secret_?access_?key\s*[:=]\s*[A-Za-z0-9/+=]{40}")),
    ("slack-token", re.compile(r"xox[baprs]-[A-Za-z0-9\-]{10,}")),
    ("private-key-block", re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----")),
    ("jwt", re.compile(r"eyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}")),
    ("url-with-credentials", re.compile(r"(?i)(postgres|postgresql|mysql|mongodb|redis|amqp)://[^\s:/@]+:[^\s@/]{3,}@")),
]

# --- Tier B: shape heuristics, living docs only ------------------------------
TIER_B = [
    ("password-assignment", re.compile(r"(?i)\b(password|passwd|pwd)\s*[:=]\s*[\"']?[^\s\"'<>]{6,}")),
    ("token-assignment", re.compile(r"(?i)\b(api_?key|secret|token)\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{16,}")),
]

TEXT_EXTS = {".md", ".py", ".json", ".yaml", ".yml", ".txt", ".csv", ".jsonc", ".toml", ".ini", ".cfg"}
SKIP_DIRS = {".git", ".idea", ".venv", "__pycache__", "node_modules", ".pytest_cache"}
# Placeholder shapes that are documentation, not credentials.
PLACEHOLDER = re.compile(r"(?i)^(x{3,}|\.{3,}|<[^>]+>|\$\{?[A-Z_]+\}?|change[-_]?me.*|your[-_].*|example.*|redacted|\*{3,})$")
# Inline escape hatch, same convention as detect-secrets: a fixture that must
# contain a credential-shaped string says so on its own line.
ALLOW_MARKER = "pragma: allowlist secret"


def _is_placeholder(value: str) -> bool:
    return bool(PLACEHOLDER.match(value.strip()))


def _line_of(text: str, pos: int) -> str:
    start = text.rfind("\n", 0, pos) + 1
    end = text.find("\n", pos)
    return text[start: end if end != -1 else len(text)]



def _iter_text_files(root: str):
    for dirpath, dirnames, files in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in files:
            if os.path.splitext(fn)[1].lower() in TEXT_EXTS:
                yield os.path.join(dirpath, fn)


def _read(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def scan(root: str) -> list[dict]:
    findings: list[dict] = []
    archive = os.path.join(root, "archive") + os.sep

    for path in _iter_text_files(root):
        rel = os.path.relpath(path, root).replace("\\", "/")
        in_archive = path.startswith(archive)
        text = _read(path)

        for name, pattern in TIER_A:
            for match in pattern.finditer(text):
                if _is_placeholder(match.group(0)):
                    continue
                if ALLOW_MARKER in _line_of(text, match.start()):
                    continue
                findings.append({
                    "tier": "A", "rule": name, "file": rel,
                    "line": text[: match.start()].count("\n") + 1,
                })

        if in_archive:
            continue

        for name, pattern in TIER_B:
            for match in pattern.finditer(text):
                # Only the assigned value matters for the placeholder test.
                value = re.split(r"[:=]", match.group(0), maxsplit=1)[-1]
                if _is_placeholder(value):
                    continue
                if ALLOW_MARKER in _line_of(text, match.start()):
                    continue
                findings.append({
                    "tier": "B", "rule": name, "file": rel,
                    "line": text[: match.start()].count("\n") + 1,
                })
    return findings


def report(findings: list[dict]) -> bool:
    if not findings:
        print("check_secrets: OK (0 findings)")
        return True
    print("check_secrets: FAILED")
    for f in findings:
        print(f"  [tier {f['tier']}] {f['rule']}: {f['file']}:{f['line']}")
    return False


def main(argv: list[str] | None = None) -> int:
    default_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parser = argparse.ArgumentParser(description="Scan for credential-like content.")
    parser.add_argument("--root", default=default_root)
    args = parser.parse_args(argv)
    return 0 if report(scan(os.path.abspath(args.root))) else 1


if __name__ == "__main__":
    sys.exit(main())
