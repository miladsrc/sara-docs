# SARA Architecture Cleanup — Final Report

Date: 2026-08-30 · OpenCode 1.18.25 · Host user `98903`

## 1. Executive Summary

Sara was **under-organized, not over-engineered**. Cleanup removed stale
host-specific doctrine, repaired a broken capability (`read-terminals`), gave
each shared concept a single owner, and added navigation to the docs — without
adding capabilities, weakening safety, or touching runtime logic of the plugin.
End state: same capabilities, clearer ownership, less duplication, fewer stale
paths, less always-loaded context.

## 2. Starting Architecture

- Runtime = opencode config surface at `~/.config/opencode/` (commands, agents,
  skills, plugin, AGENTS.md, opencode.jsonc). No separate Sara process.
- Config dir was **not under git** (home repo has 0 tracked files) -> backups
  were required and created.
- Host is `98903`; many files referenced `m.barani` (stale from another machine).
- v2 Gateway referenced in AGENTS.md but **absent on this host** (both paths
  missing, port 8800 down).

## 3. Confirmed Problems (evidence)

| # | Problem | Level |
| - | ------- | ----- |
| 1 | Decision schema duplicated (sara-decide + architect) | VERIFIED |
| 2 | Review-tier definitions duplicated (AGENTS + sara-decide) | VERIFIED |
| 3 | Complexity taxonomy referenced in 4 places (owner was already sara-review) | VERIFIED (low) |
| 4 | Debt semantics duplicated (sara-debt full + auditor re-specified) | VERIFIED |
| 5 | sara-debt / auditor overlap | VERIFIED (kept both, deduped doctrine) |
| 6 | read-terminals broken on this host (stale `m.barani` DB path) | VERIFIED (P0) |
| 7 | read-terminals `todos` queried nonexistent `todo.data` column | VERIFIED (P0) |
| 8 | Stale `m.barani` paths in always-loaded AGENTS.md | VERIFIED |
| 9 | Dead v2 Gateway doctrine hardcoded to absent host | VERIFIED |
| 10 | Documentation sprawl, README not a navigation map | VERIFIED |
| 11 | Config surface not version-controlled | VERIFIED |

## 4. Target Architecture

See `SARA_TARGET_ARCHITECTURE.md`. Owner map:

| Concept            | Canonical Owner                  |
| ------------------ | -------------------------------- |
| Decision schema    | `command/sara-decide.md`         |
| Classification     | `command/sara-decide.md`         |
| Review tiers       | `AGENTS.md` (Review routing)     |
| Complexity taxonomy| `skills/sara-review/SKILL.md`    |
| Debt semantics     | `skills/sara-debt/SKILL.md`      |
| Safety mechanism   | `opencode.jsonc` (permission)    |
| Telemetry contract | `SARA_TELEMETRY_CONTRACT.md`     |

## 5. Changes Executed

| Problem | Old location | New owner | Action | Reason | Behavior impact | Risk | Validation |
| ------- | ------------ | --------- | ------ | ------ | --------------- | ---- | ---------- |
| P0 read-terminals DB path | `read_terminals.py` `m.barani` literal | script resolves via `Path.home()` + `OPENCODE_DB` override | FIX | path was wrong on this host | DB resolved correctly; `list` works | LOW | `list` returns live sessions |
| P0 `todos` crash | `SELECT data FROM todo` | use real `content/status/position` columns | FIX | queried nonexistent column | `todos` returns rows | LOW | `todos` returns real todos |
| Decision dup | architect copy | `sara-decide.md`; architect references | CONSOLIDATE | one owner | architect still returns a decision record; no competing enum | MED | grep: enum only in sara-decide |
| Tier dup | sara-decide copy | `AGENTS.md`; sara-decide routes by ref | CONSOLIDATE | one owner | no behavior change | MED | grep: definitions only in AGENTS |
| Debt dup | auditor re-spec | `sara-debt`; auditor references | CONSOLIDATE | one owner | auditor still produces debt ledger | MED | file inspected |
| Taxonomy | refs only | `sara-review` (already owner) | KEEP | no competing full copy existed | none | LOW | grep verified |
| Stale AGENTS paths | `m.barani` paths | host-neutral wording | FIX | wrong host | context accurate, no doctrine lost | LOW | grep clean |
| Dead v2 section | full v2 bridge | condensed note | FIX | v2 absent on host | routing intent preserved | MED | inspected |

## 6. Source-of-Truth Map

| Concept             | Canonical Owner                  | Consumers |
| ------------------- | -------------------------------- | --------- |
| Decision schema     | `command/sara-decide.md`         | architect |
| Classification      | `command/sara-decide.md`         | architect |
| Review tiers        | `AGENTS.md` (Review routing)     | sara-decide, sara-review |
| Complexity taxonomy | `skills/sara-review/SKILL.md`    | reviewer, auditor, sara-review, sara-audit |
| Debt semantics      | `skills/sara-debt/SKILL.md`      | auditor |
| Safety mechanism    | `opencode.jsonc`                 | AGENTS.md (policy text) |
| Telemetry contract  | `SARA_TELEMETRY_CONTRACT.md`     | /sara-eval |

## 7. File structure before vs after (sara-docs root, .md)

Before (11 root .md): PROGRESS-PHASE-2, README, SARA-GOLDEN-RESULTS,
SARA_ARCHITECTURE_CLEANUP_REPORT, SARA_GOLDEN_TASKS, SARA_SELF_BOUNDARY,
SARA_SYSTEM_MAP, + 6 round-2/ponytail reports mixed in.

After: 6 historical reports moved to `archive/`; README = navigation; live
root now holds current architecture/evaluation/cleanup docs; added
`SARA_CLEANUP_BASELINE.md`, `SARA_CLEANUP_CHANGE_MATRIX.md`,
`SARA_TARGET_ARCHITECTURE.md`, `SARA_TELEMETRY_CONTRACT.md`,
`SARA_CLEANUP_REGRESSION_MATRIX.md`, `SARA_POST_CLEANUP_DUPLICATION_AUDIT.md`,
`SARA_ARCHITECTURE_CLEANUP_FINAL_REPORT.md`.

## 8. P0 Results

`P0 STATUS: PASS`
- DB path host-neutral (Path.home + OPENCODE_DB). DB exists.
- `list` -> live sessions; `show` -> messages; `todos` -> rows.
- No stale user path controls behavior (grep clean).

## 9. P1 Results

- `P1-DECISION STATUS: PASS` (1 authoritative schema)
- `P1-TIER STATUS: PASS` (1 tier owner, N consumers)
- `P1-TAXONOMY STATUS: PASS` (1 owner, consumers reference tags)
- `P1-DEBT STATUS: PASS` (sara-debt owner; auditor references)

## 10. P2 Results

- Telemetry contract documented (no producer change). PASS.
- Docs organized; README navigation added; history archived (not deleted). PASS.
- Temp/vendored artifacts (`ponytail/`, `java/`, `.idea/`) left untracked/out of
  versioned Sara layout. KEEP.
- Memory left intact (continuity). PASS.

## 11. Runtime Impact

List of exact runtime changes:
- `skills/read-terminals/read_terminals.py` — DB path resolution + `todos` query.
All other runtime files unchanged. `plugin/sara.js` untouched.
`NO OTHER RUNTIME LOGIC CHANGED.`

## 12. Safety Verification

- `opencode.jsonc` ask-gates byte-identical (git push*, reset --hard, clean -fd,
  rm -rf, docker compose down -v, dropdb). PASS.
- Boundary restated in AGENTS.md: opencode.jsonc = mechanism, AGENTS.md = policy.
- No gate weakened. PASS.

## 13. Evaluation Verification

- Plugin tests: 4/4 pass (unchanged).
- `/sara-eval` process untouched; golden-run workflow unchanged.
- Golden tasks frozen (not in git status). PASS.

## 14. Regression Matrix

See `SARA_CLEANUP_REGRESSION_MATRIX.md`. All capabilities PASS or unchanged;
evaluation NOT RUN live (out of scope for this session), no regression observed.

## 15. Duplication Audit

See `SARA_POST_CLEANUP_DUPLICATION_AUDIT.md`. Criterion met: no competing
source of truth.

## 16. Context Delta

- AGENTS.md (always-loaded): 134 -> 117 lines (-17). Removed stale v2 section
  and machine-specific paths; all doctrine (Ladder, self-review, gates) kept.
  This is the only always-loaded context change; it shrank.

## 17. Complexity Delta

| Metric | Value |
| ------ | ----- |
| Files modified (runtime config) | 6 (AGENTS, sara-decide, architect, auditor, read_terminals.py, read-terminals SKILL) |
| Files added (docs) | 7 (baseline, matrix, target, telemetry, audit, regression, final-report) |
| Files moved to archive | 6 |
| Files modified (sara-docs) | README |
| Lines added / removed (runtime) | +19 / -22 (net -3) |
| Duplicate doctrine removed | decision schema copy, tier definition copy, debt re-spec |
| Broken capabilities repaired | 1 (read-terminals, incl. latent todos defect) |
| Dependencies added | 0 |
| Dependencies removed | 0 |
| Behavior changes (runtime) | 1 repaired capability; all else unchanged |
| NOT MEASURED | duplicate-doctrine line count across all files (best-effort above) |

## 18. Documentation Changes

- README rebuilt as navigation (live / evaluation / cleanup / archive / external).
- Telemetry interface documented in `SARA_TELEMETRY_CONTRACT.md`.
- History moved to `archive/` (not deleted).
- `PROGRESS-PHASE-2.md` (ai-swe-engine) left as external-project doc.

## 19. Remaining Technical Debt

- `read-terminals` `show` assumes `part.data` text parts; not all messages have
  them — acceptable (best-effort read).
- Sara config surface still not git-tracked; backups remain the rollback
  mechanism. Consider tracking it (`sara:` note).
- `/sara-eval` still uses a hardcoded temp path — left as-is (not justified to
  change; matches this host).

## 20. Deferred Work

- Running `/sara-eval` live golden-run in this session (would alter evidence
  state; out of scope).
- Restarting opencode to validate full config load (config is not hot-reloaded;
  the running session uses the old config). Required before full trust.

## 21. What Was Intentionally NOT Changed

Preserved: `architect`, `reviewer`, `auditor` agents · `/sara-decide`,
`/sara-review`, `/sara-audit`, `/sara-eval` · `sara-review`, `sara-debt` skills ·
telemetry (plugin untouched) · permissions (opencode.jsonc identical) · golden
tasks (frozen) · evaluation pipeline · Decision Ladder · self-review ·
memory/history.

## 22. Final Verdict

- Better organized? YES — docs navigable, live vs archive split.
- Ownership clearer? YES — 1 owner per shared concept.
- Duplication lower? YES — decision, tier, debt copies removed.
- Architecture simpler? YES — net -3 lines runtime, fewer stale paths.
- Capabilities preserved? YES — all present, one repaired.
- Behavior intentionally changed? Only `read-terminals` repair (broken -> working).
- Regressions found? None in the tested surface.
- Another cleanup necessary now? No. Next step is a restart + optional
  `/sara-eval` run, not another cleanup.

---

## 26. Final Truth Table

| Statement                                     | Result | Evidence |
| --------------------------------------------- | ------ | -------- |
| Sara was fundamentally over-engineered        | FALSE  | diagnosis: under-organized |
| Sara was under-organized                      | TRUE   | dup doctrine + stale paths |
| Decision schema has one owner                 | TRUE   | sara-decide |
| Classification has one owner                  | TRUE   | sara-decide |
| Review tiers have one owner                   | TRUE   | AGENTS.md |
| Complexity taxonomy has one owner             | TRUE   | sara-review |
| Debt semantics have one owner                 | TRUE   | sara-debt |
| Mechanical safety remains centralized         | TRUE   | opencode.jsonc byte-identical |
| read-terminals works on this host             | TRUE   | list/show/todos return data |
| Telemetry remains intact                      | TRUE   | plugin untouched; tests 4/4 |
| Evaluation remains intact                     | UNKNOWN| not run live this session |
| Golden tasks remained unchanged               | TRUE   | not in git status |
| No unrelated project was modified             | TRUE   | ai-swe-engine, ponytail, java untouched |
| Duplication was reduced                       | TRUE   | decision/tier/debt deduped |
| Cleanup introduced significant new complexity | FALSE  | net runtime -3 lines, 0 deps |

---

## 27. Commit Readiness

```
READY TO COMMIT: NO — review before any commit, and I do not auto-commit.
```

State: `sara-docs` has pre-existing staged changes
(`SARA_ARCHITECTURE_CLEANUP_REPORT.md`, `SARA_CLEANUP_BASELINE.md`) that were
staged externally (likely IDE), plus this cleanup's unstaged/untracked changes.
The runtime config dir (`~/.config/opencode`) is not tracked and is not part of
this repo.

If you choose to commit in `sara-docs`, suggested message:
`refactor(sara): consolidate architecture and sources of truth`

Exact files to consider (worktree + new docs):
- Modified: `README.md`
- New docs: `SARA_CLEANUP_BASELINE.md`, `SARA_CLEANUP_CHANGE_MATRIX.md`,
  `SARA_TARGET_ARCHITECTURE.md`, `SARA_TELEMETRY_CONTRACT.md`,
  `SARA_CLEANUP_REGRESSION_MATRIX.md`, `SARA_POST_CLEANUP_DUPLICATION_AUDIT.md`,
  `SARA_ARCHITECTURE_CLEANUP_FINAL_REPORT.md`
- Moved to archive: the 6 historical reports (git mv in archive/)
- Must remain untracked/excluded: `ponytail/`, `java/`, `.idea/`,
  `PROGRESS-PHASE-2.md` (external-project content) — unless you decide otherwise.

Review the externally-staged set before committing; I have not committed or
pushed anything.
```
```
