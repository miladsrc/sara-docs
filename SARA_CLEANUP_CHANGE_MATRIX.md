# SARA Cleanup — Change Matrix

| ID | Confirmed Problem | Verification | Current Locations | Proposed Owner | Action | Priority | Risk | Validation |
| -- | ----------------- | ------------ | ----------------- | -------------- | ------ | -------- | ---- | ---------- |
| C1 | `read-terminals` DB path hardcoded to `m.barani` -> broken on this host | VERIFIED (path nonexistent, DB exists at 98903) | `skills/read-terminals/read_terminals.py`, `SKILL.md` | script resolves host-neutrally | FIX | P0 | LOW | `list`/`show`/`todos` run on real DB |
| C2 | `todos` subcommand queried non-existent `todo.data` column | VERIFIED (PRAGMA shows `content`) | `read_terminals.py` | use real schema | FIX | P0 | LOW | `todos` returns rows |
| C3 | Duplicate decision schema | VERIFIED (two full blocks) | `agent/architect.md`, `command/sara-decide.md` | `sara-decide` = canonical | CONSOLIDATE | P1 | MED | grep shows 1 full owner |
| C4 | Duplicate review-tier definitions | VERIFIED (3 sites) | `AGENTS.md`, `sara-decide.md` | `AGENTS.md` = canonical | CONSOLIDATE | P1 | MED | 1 tier owner, N consumers |
| C5 | Complexity taxonomy referenced in 4 places | VERIFIED (names only, full defs only in sara-review) | `sara-review/SKILL.md` + 4 refs | `sara-review` = owner | KEEP | P1 | LOW | refs point to one owner |
| C6 | Debt semantics duplicated | VERIFIED (sara-debt full + auditor re-specified) | `sara-debt/SKILL.md`, `agent/auditor.md` | `sara-debt` = canonical | CONSOLIDATE | P1 | MED | auditor references sara-debt |
| C7 | Stale `m.barani` paths in always-loaded AGENTS.md | VERIFIED (host is 98903) | `AGENTS.md` identity + standing context + v2 section | AGENTS.md host-neutral | FIX | P1 | LOW | grep clean, no behavior loss |
| C8 | Dead v2 Gateway doctrine hardcoded to absent host | VERIFIED (both paths missing, port down) | `AGENTS.md` v2 bridge section | condensed note | FIX | P1 | MED | note preserves intent |
| C9 | Telemetry interface undocumented | VERIFIED (no doc) | `plugin/sara.js` | `SARA_TELEMETRY_CONTRACT.md` | WRAP | P2 | LOW | doc only, no logic change |
| C10 | Docs sprawl, README not a navigation map | VERIFIED (15 md files, mixed live/historical) | `sara-docs/*.md` | README = navigation | ORGANIZE | P2 | LOW | README covers live + archive |
| C11 | Config dir not git-tracked | VERIFIED (home repo, 0 tracked files) | `~/.config/opencode` | local backups | KEEP | P0 | LOW | backup dir created |
| C12 | vendor/temp artifacts untracked in sara-docs | VERIFIED (`ponytail/`, `java/`, `.idea/`) | `sara-docs/` | stay untracked, referenced | KEEP | P2 | LOW | excluded from versioned sara |

## README / archive

- C10 handled in Phase 15/16: README becomes navigation; historical reports move under `archive/` (shown alongside, no deletion).
