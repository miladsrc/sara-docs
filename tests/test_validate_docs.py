"""Tests for the documentation validators.

These tests are the reason the validators can be trusted: each rule is proven
to fire on a bad fixture and stay silent on a good one.

Run: python -m pytest tests -q
"""
from __future__ import annotations

import os
import sys

import pytest

SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, SCRIPTS)

import check_links  # noqa: E402
import check_secrets  # noqa: E402
import validate_docs  # noqa: E402


def write(root, rel, text):
    path = os.path.join(root, rel.replace("/", os.sep))
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


# --- check_links ------------------------------------------------------------

def test_links_pass_when_target_exists(tmp_path):
    root = str(tmp_path)
    write(root, "README.md", "see [doc](docs/a.md)\n")
    write(root, "docs/a.md", "content\n")
    assert check_links.scan(root) == []


def test_links_fail_when_target_missing(tmp_path):
    root = str(tmp_path)
    write(root, "README.md", "see [gone](docs/missing.md)\n")
    broken = check_links.scan(root)
    assert len(broken) == 1
    assert broken[0]["target"] == "docs/missing.md"


def test_links_ignore_external_and_anchors(tmp_path):
    root = str(tmp_path)
    write(root, "README.md", "[a](https://x.test) [b](#local) [c](mailto:a@b.test)\n")
    assert check_links.scan(root) == []


def test_links_strip_anchor_before_resolving(tmp_path):
    root = str(tmp_path)
    write(root, "README.md", "[a](docs/a.md#section)\n")
    write(root, "docs/a.md", "x\n")
    assert check_links.scan(root) == []


def test_links_skip_archive(tmp_path):
    root = str(tmp_path)
    write(root, "archive/old.md", "[dead](nowhere.md)\n")
    assert check_links.scan(root) == []


# --- check_secrets ----------------------------------------------------------

def test_secrets_detect_github_pat(tmp_path):
    root = str(tmp_path)
    write(root, "memory/notes.md", "token ghp_" + "a" * 36 + "\n")
    hits = check_secrets.scan(root)
    assert any(h["rule"] == "github-pat" for h in hits)


def test_secrets_detect_private_key(tmp_path):
    root = str(tmp_path)
    write(root, "memory/notes.md", "-----BEGIN RSA PRIVATE KEY-----\nabc\n")  # pragma: allowlist secret
    assert check_secrets.scan(root)


def test_secrets_detect_credentials_in_url(tmp_path):
    root = str(tmp_path)
    write(root, "memory/notes.md", "postgres://admin:hunter2super@db.local:5432/x\n")  # pragma: allowlist secret
    assert any(h["rule"] == "url-with-credentials" for h in check_secrets.scan(root))


def test_secrets_tier_a_applies_to_archive(tmp_path):
    root = str(tmp_path)
    write(root, "archive/old.md", "ghp_" + "b" * 36 + "\n")
    assert check_secrets.scan(root)


def test_secrets_tier_b_skips_archive(tmp_path):
    root = str(tmp_path)
    write(root, "archive/old.md", "password: Sup3rS3cret!\n")  # pragma: allowlist secret
    assert check_secrets.scan(root) == []


def test_secrets_honour_inline_allowlist_marker(tmp_path):
    root = str(tmp_path)
    write(root, "tests/fixture.py", 'KEY = "ghp_' + "c" * 36 + '"  # pragma: allowlist secret\n')
    assert check_secrets.scan(root) == []


def test_secrets_marker_does_not_cover_other_lines(tmp_path):
    root = str(tmp_path)
    write(root, "tests/fixture.py", "# pragma: allowlist secret\nKEY = \"ghp_" + "d" * 36 + "\"\n")
    assert check_secrets.scan(root) != []


def test_secrets_allow_placeholders(tmp_path):
    root = str(tmp_path)
    write(root, "memory/notes.md", "password: <your-password>\napi_key: ${API_KEY}\ntoken: xxxxxxxx\n")
    assert check_secrets.scan(root) == []


# --- validate_docs rules ----------------------------------------------------

def test_host_refs_flag_foreign_literal(tmp_path):
    root = str(tmp_path)
    write(root, "README.md", "lives at C:\\Users\\98903\\x\n")
    problems = validate_docs.check_host_refs(root)
    assert any("98903" in p for p in problems)


def test_host_refs_flag_foreign_user_path(tmp_path):
    root = str(tmp_path)
    write(root, "README.md", "path `C:/Users/someoneelse/docs`\n")
    assert validate_docs.check_host_refs(root)


def test_host_refs_allow_current_user(tmp_path):
    root = str(tmp_path)
    write(root, "README.md", "path `C:/Users/m.barani/docs`\n")
    assert validate_docs.check_host_refs(root) == []


def test_host_refs_allow_8_3_shortname_alias(tmp_path):
    root = str(tmp_path)
    write(root, "README.md", "temp lives under C:\\Users\\M4436~1.BAR\\AppData\n")
    assert validate_docs.check_host_refs(root) == []


def test_host_refs_skip_archive(tmp_path):
    root = str(tmp_path)
    write(root, "archive/old.md", "was on 98903\n")
    assert validate_docs.check_host_refs(root) == []


def test_host_refs_respect_allowlist(tmp_path, monkeypatch):
    root = str(tmp_path)
    monkeypatch.setattr(validate_docs, "FOREIGN_ALLOWLIST", ("memory/current-state.md",))
    write(root, "memory/current-state.md", "previously claimed host 98903\n")
    assert validate_docs.check_host_refs(root) == []


def test_host_refs_allowlist_is_not_a_wildcard(tmp_path, monkeypatch):
    root = str(tmp_path)
    monkeypatch.setattr(validate_docs, "FOREIGN_ALLOWLIST", ("memory/current-state.md",))
    write(root, "memory/other.md", "claims host 98903\n")
    assert validate_docs.check_host_refs(root) != []


def test_abs_paths_flag_nonexistent(tmp_path, monkeypatch):
    root = str(tmp_path)
    monkeypatch.setattr(validate_docs, "HOST_PATH_CHECKS", True)
    write(root, "README.md", "config at `C:/definitely/not/here/x.md`\n")
    problems = validate_docs.check_abs_paths(root)
    assert any("does not exist" in p for p in problems)


def test_abs_paths_skipped_off_host_platform(tmp_path, monkeypatch):
    """R3 cannot verify another machine's paths: it must skip, not fail."""
    root = str(tmp_path)
    monkeypatch.setattr(validate_docs, "HOST_PATH_CHECKS", False)
    write(root, "README.md", "config at `C:/definitely/not/here/x.md`\n")
    assert validate_docs.check_abs_paths(root) == []


def test_abs_paths_allow_existing(tmp_path):
    root = str(tmp_path)
    write(root, "real/file.md", "x\n")
    target = os.path.join(root, "real", "file.md").replace("\\", "/")
    write(root, "README.md", f"config at `{target}`\n")
    assert validate_docs.check_abs_paths(root) == []


def test_main_reports_skipped_host_check_without_failing(tmp_path, monkeypatch, capsys):
    """Off the owner's platform the gate must still pass, and must say why."""
    root = str(tmp_path)
    monkeypatch.setattr(validate_docs, "REQUIRED", ["README.md"])
    monkeypatch.setattr(validate_docs, "VERIFIED_REQUIRED", [])
    monkeypatch.setattr(validate_docs, "HOST_PATH_CHECKS", False)
    write(root, "README.md", "# ok\nconfig at `C:/definitely/not/here/x.md`\n")
    assert validate_docs.main(["--root", root]) == 0
    assert "R3 skipped" in capsys.readouterr().out


def test_abs_paths_skip_placeholders(tmp_path):
    root = str(tmp_path)
    write(root, "README.md", "agent at `C:/Users/m.barani/.config/opencode/agent/<name>.md`\n")
    assert validate_docs.check_abs_paths(root) == []


def test_verified_date_missing_is_failure(tmp_path, monkeypatch):
    root = str(tmp_path)
    monkeypatch.setattr(validate_docs, "VERIFIED_REQUIRED", ["architecture/SYSTEM-MAP.md"])
    write(root, "architecture/SYSTEM-MAP.md", "no date here\n")
    failures, _ = validate_docs.check_verified_dates(root)
    assert failures


def test_verified_date_present_is_ok(tmp_path, monkeypatch):
    root = str(tmp_path)
    monkeypatch.setattr(validate_docs, "VERIFIED_REQUIRED", ["architecture/SYSTEM-MAP.md"])
    write(root, "architecture/SYSTEM-MAP.md", "Verified: 2026-10-25\nbody\n")
    failures, warnings = validate_docs.check_verified_dates(root)
    assert failures == [] and warnings == []


def test_verified_date_old_raises_warning(tmp_path, monkeypatch):
    root = str(tmp_path)
    monkeypatch.setattr(validate_docs, "VERIFIED_REQUIRED", ["architecture/SYSTEM-MAP.md"])
    write(root, "architecture/SYSTEM-MAP.md", "Verified: 2020-01-01\nbody\n")
    failures, warnings = validate_docs.check_verified_dates(root)
    assert failures == [] and warnings


def test_required_detects_missing_and_empty(tmp_path, monkeypatch):
    root = str(tmp_path)
    monkeypatch.setattr(validate_docs, "REQUIRED", ["README.md", "empty.md", "never-created.md"])
    write(root, "README.md", "ok\n")
    write(root, "empty.md", "")
    problems = validate_docs.check_required(root)
    assert any("never-created.md" in p and "missing" in p for p in problems)
    assert any("empty.md" in p and "empty" in p for p in problems)


def test_todo_markers_warn_but_do_not_fail(tmp_path):
    root = str(tmp_path)
    write(root, "workflows/x.md", "TODO: fill this in\n")
    warnings = validate_docs.check_todos(root)
    assert warnings


# --- end to end -------------------------------------------------------------

def test_main_fails_on_broken_repo(tmp_path, monkeypatch):
    root = str(tmp_path)
    monkeypatch.setattr(validate_docs, "REQUIRED", ["README.md"])
    monkeypatch.setattr(validate_docs, "VERIFIED_REQUIRED", [])
    write(root, "README.md", "[dead](gone.md)\n")
    assert validate_docs.main(["--root", root, "--quiet"]) == 1


def test_main_passes_on_minimal_good_repo(tmp_path, monkeypatch):
    root = str(tmp_path)
    monkeypatch.setattr(validate_docs, "REQUIRED", ["README.md"])
    monkeypatch.setattr(validate_docs, "VERIFIED_REQUIRED", [])
    write(root, "README.md", "# ok\n")
    assert validate_docs.main(["--root", root, "--quiet"]) == 0
