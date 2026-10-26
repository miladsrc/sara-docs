#!/usr/bin/env python3
"""Structural validation gate for the Sara docs repository.

This is the gate that keeps documentation from silently drifting away from
reality. It exists because a doc set was once found to contain eight stale
claims across three files, none of which anything checked.

Rules enforced
--------------
R1  Required files exist and are non-empty                  (the skeleton contract)
R2  No foreign host/user references                          (98903, C:\\Users\\<other>)
R3  Absolute paths written in backticks must exist on disk   (host drift killer)
R4  Relative markdown links resolve                          (delegated to check_links)
R5  No credential-like content                               (delegated to check_secrets)
R6  Verified-dated docs carry a valid `Verified: YYYY-MM-DD` (or `Last updated:`)
R7  No TODO/FIXME markers in living docs                     (warn only)

archive/ is frozen history: R2/R3/R6/R7 skip it. R4/R5 apply selectively
(links skipped, secrets still scanned).

Exit 0 when all blocking rules pass, 1 otherwise.
Usage: python scripts/validate_docs.py [--root DIR] [--quiet]
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import check_links  # noqa: E402
import check_secrets  # noqa: E402

# --- R1: the skeleton contract ----------------------------------------------
# Extend this list whenever the architecture gains a required file.
REQUIRED = [
    "README.md",
    "AGENTS.md",
    "memory/README.md",
    "memory/current-state.md",
    "backlog/open-questions.md",
    "architecture/OPERATING-MODEL.md",
    "architecture/SYSTEM-MAP.md",
    "architecture/SELF-BOUNDARY.md",
    "workflows/feature.md",
    "workflows/bugfix.md",
    "workflows/refactor.md",
    "workflows/db-migration.md",
    "workflows/code-review.md",
    "workflows/incident.md",
    "workflows/delegation.md",
    "workflows/self-upgrade.md",
    "roster/README.md",
    "evaluation/GOLDEN-TASKS.md",
    "evaluation/telemetry-contract.md",
    "scripts/validate_docs.py",
    "scripts/check_links.py",
    "scripts/check_secrets.py",
]

# --- R6: files that make factual claims must say when they were checked -----
VERIFIED_REQUIRED = [
    "architecture/OPERATING-MODEL.md",
    "architecture/SYSTEM-MAP.md",
    "architecture/SELF-BOUNDARY.md",
    "memory/current-state.md",
    "roster/README.md",
]

DATE_RE = re.compile(r"(?:Verified|Last updated):\s*(\d{4}-\d{2}-\d{2})")
STALE_AFTER_DAYS = 90

# --- R2: foreign host / user references -------------------------------------
FOREIGN_LITERALS = ["98903"]
FOREIGN_USER_RE = re.compile(r"C:[\\/]Users[\\/]([A-Za-z0-9._\-]+)")
ALLOWED_USERS = {
    "m.barani",
    # 8.3 short-name alias of the SAME profile on this host: $env:USERPROFILE
    # resolves to C:\Users\M4436~1.BAR, which is m.barani. Not a foreign machine.
    "M4436",
}
# Files whose PURPOSE is to name a foreign host: the drift-correction table, the
# ADR that records it, and dated records that cite an external baseline.
# Explicit and reviewable on purpose - adding an entry here is a visible act.
# memory/daily/ and evaluation/results/ hold DATED records: like archive/, they
# must be able to name what they observed or compared against. Living *claims*
# stay in current-state.md, which is allowlisted only because its job is to state
# the corrections.
FOREIGN_ALLOWLIST = (
    "memory/current-state.md",          # corrections table: names what was claimed
    "memory/daily/",                    # dated records: history, not current claims
    "memory/decisions/ADR-001",         # records the drift as context
    "evaluation/results/",              # dated runs: cite external baselines
)

# --- R3: absolute local paths in backticks ----------------------------------
BACKTICK = re.compile(r"`([^`\n]+)`")
ABS_PATH_RE = re.compile(r"^(?:[A-Za-z]:[\\/]|~[\\/])")

TODO_RE = re.compile(r"\b(TODO|FIXME|XXX)\b")

SKIP_DIRS = {".git", ".idea", ".venv", "__pycache__", "node_modules", ".pytest_cache"}


def _living_docs(root: str):
    archive = os.path.join(root, "archive") + os.sep
    for dirpath, dirnames, files in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in files:
            if fn.lower().endswith(".md"):
                path = os.path.join(dirpath, fn)
                if not path.startswith(archive):
                    yield path


def _read(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def _expand(path: str) -> str:
    if path.startswith("~"):
        return os.path.expanduser(path)
    return path


def check_required(root: str) -> list[str]:
    problems = []
    for rel in REQUIRED:
        full = os.path.join(root, rel.replace("/", os.sep))
        if not os.path.isfile(full):
            problems.append(f"R1 missing required file: {rel}")
        elif os.path.getsize(full) == 0:
            problems.append(f"R1 empty required file: {rel}")
    return problems


def check_host_refs(root: str) -> list[str]:
    problems = []
    for doc in _living_docs(root):
        rel = os.path.relpath(doc, root).replace("\\", "/")
        if any(rel.startswith(prefix) for prefix in FOREIGN_ALLOWLIST):
            continue
        text = _read(doc)
        for literal in FOREIGN_LITERALS:
            for match in re.finditer(re.escape(literal), text):
                line = text[: match.start()].count("\n") + 1
                problems.append(f"R2 foreign host reference '{literal}': {rel}:{line}")
        for match in FOREIGN_USER_RE.finditer(text):
            user = match.group(1)
            if user not in ALLOWED_USERS:
                line = text[: match.start()].count("\n") + 1
                problems.append(f"R2 foreign user path 'C:\\Users\\{user}': {rel}:{line}")
    return problems


def check_abs_paths(root: str) -> list[str]:
    problems = []
    for doc in _living_docs(root):
        rel = os.path.relpath(doc, root).replace("\\", "/")
        text = _read(doc)
        for match in BACKTICK.finditer(text):
            candidate = match.group(1).strip()
            if not ABS_PATH_RE.match(candidate):
                continue
            # Skip templates, globs and multi-path snippets: those are shapes, not claims.
            if any(token in candidate for token in ("<", ">", "*", "...", "$")):
                continue
            resolved = _expand(candidate)
            if not os.path.exists(resolved):
                line = text[: match.start()].count("\n") + 1
                problems.append(f"R3 referenced path does not exist: {rel}:{line} -> {candidate}")
    return problems


def check_verified_dates(root: str) -> tuple[list[str], list[str]]:
    failures, warnings = [], []
    today = dt.date.today()
    for rel in VERIFIED_REQUIRED:
        full = os.path.join(root, rel.replace("/", os.sep))
        if not os.path.isfile(full):
            continue
        text = _read(full)
        match = DATE_RE.search(text)
        if not match:
            failures.append(f"R6 no 'Verified: YYYY-MM-DD' line: {rel}")
            continue
        try:
            stamp = dt.date.fromisoformat(match.group(1))
        except ValueError:
            failures.append(f"R6 invalid date '{match.group(1)}': {rel}")
            continue
        age = (today - stamp).days
        if age > STALE_AFTER_DAYS:
            warnings.append(f"R6 verification is {age} days old (> {STALE_AFTER_DAYS}): {rel}")
    return failures, warnings


def check_todos(root: str) -> list[str]:
    warnings = []
    for doc in _living_docs(root):
        rel = os.path.relpath(doc, root).replace("\\", "/")
        # The validators themselves and this doc legitimately name the markers.
        if rel.startswith("scripts/"):
            continue
        text = _read(doc)
        for match in TODO_RE.finditer(text):
            line = text[: match.start()].count("\n") + 1
            warnings.append(f"R7 open marker '{match.group(0)}': {rel}:{line}")
    return warnings


def main(argv: list[str] | None = None) -> int:
    default_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parser = argparse.ArgumentParser(description="Validate the Sara docs structure.")
    parser.add_argument("--root", default=default_root)
    parser.add_argument("--quiet", action="store_true", help="only print the verdict line")
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)

    failures: list[str] = []
    failures += check_required(root)
    failures += check_host_refs(root)
    failures += check_abs_paths(root)
    date_failures, date_warnings = check_verified_dates(root)
    failures += date_failures

    link_broken = check_links.scan(root)
    for item in link_broken:
        failures.append(f"R4 broken link: {item['file']}:{item['line']} -> {item['target']}")

    secret_hits = check_secrets.scan(root)
    for hit in secret_hits:
        failures.append(f"R5 {hit['rule']}: {hit['file']}:{hit['line']}")

    warnings = date_warnings + check_todos(root)

    if not args.quiet:
        for w in warnings:
            print(f"WARN  {w}")
        for f in failures:
            print(f"FAIL  {f}")

    if failures:
        print(f"validate_docs: FAILED ({len(failures)} blocking, {len(warnings)} warnings)")
        return 1
    print(f"validate_docs: OK ({len(REQUIRED)} required files, {len(warnings)} warnings)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
