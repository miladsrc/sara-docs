# sara-docs

Navigation entry for Sara (opencode supervisor meta-agent) documentation.

> Still in progress: this README is updated as the architecture-cleanup (2026-08-30) lands its final reports.

## Live — Current Architecture & Policy

- **SARA_ARCHITECTURE_CLEANUP_REPORT.md** — read-only architecture inventory and cleanup analysis (input to this cleanup).
- **SARA_CLEANUP_BASELINE.md** — frozen starting state before the cleanup.
- **SARA_TARGET_ARCHITECTURE.md** — intended policy/execution structure and source-of-truth owners.
- **SARA_CLEANUP_CHANGE_MATRIX.md** — confirmed issues, owners, and actions.
- **SARA_SYSTEM_MAP.md** — component inventory of Sara on this host.

## Current Evaluation & Boundaries

- **SARA_GOLDEN_TASKS.md** — golden probe set (frozen during cleanup).
- **SARA-GOLDEN-RESULTS.md** — evidence records from golden-task runs.
- **SARA_SELF_BOUNDARY.md** — rules for when Sara may modify herself.
- **SARA_TELEMETRY_CONTRACT.md** — telemetry event interface (producer/consumer boundary).

## Cleanup output (2026-08-30)

- `SARA_ARCHITECTURE_CLEANUP_FINAL_REPORT.md` — final report + regression matrix + duplication audit + truth table.

## Historical Reports (archive/)

- **archive/SARA_SELF_UPGRADE_ROUND2_BASELINE.md** — pre-Round-2 baseline.
- **archive/SARA_SELF_UPGRADE_ROUND2_FINAL_REPORT.md** — Round 2 final report.
- **archive/SARA_UPGRADE_CANDIDATES.md** — Round 2 candidate items.
- **archive/SARA_ROUND2_CONTROLLED_TEST_REPORT.md** — Round 2 controlled test.
- **archive/PONYTAIL_SELF_UPGRADE_REPORT.md** — vendored ponytail audit.
- **archive/SARA_ARCHITECTURE_AFTER_ROUND2.md** — Round 2 architecture (superseded).

## External project docs

- **PROGRESS-PHASE-2.md** — ai-swe-engine Phase 2 progress manifest (not Sara itself).

## Not part of Sara

- **ponytail/** — vendored `@dietrichgebert/ponytail` plugin project (3rd-party).
- **java/** — temporary Java scaffold.
- **.idea/** — JetBrains IDE state.

These are intentionally left untracked/out of the versioned Sara layout.
