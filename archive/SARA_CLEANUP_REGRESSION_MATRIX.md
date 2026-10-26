# SARA Cleanup — Regression Matrix

Date: 2026-08-30. Evidence = inspected/ran this session. No fabricated "same behavior" claims.

| Capability     | Before | After | Status | Evidence |
| -------------- | ------ | ----- | ------ | -------- |
| Decision (`/sara-decide`) | full schema inline | canonical owner, unchanged behavior, +owner declaration | PASS | file inspected; classification intact |
| Architect      | duplicated full schema | references sara-decide; role intact | PASS | file inspected; frontmatter valid; still a read-only subagent |
| Reviewer       | unchanged | unchanged | PASS | file untouched (byte-identical) |
| Auditor        | re-specified debt semantics | references sara-debt; behavior same | PASS | file inspected; still read-only whole-repo scanner |
| sara-review    | taxonomy owner | taxonomy owner (unchanged) | PASS | untouched; still discovered |
| sara-debt      | debt owner | debt owner (unchanged) | PASS | untouched; still discovered |
| read-terminals | broken on this host (wrong DB path + todos crash) | host-neutral DB + todos fixed | PASS | `list`/`show`/`todos` return live data on real DB |
| Telemetry      | works | unchanged | PASS | plugin tests 4/4 pass; plugin untouched |
| Safety         | ask-gates present | ask-gates present (unchanged) | PASS | opencode.jsonc byte-identical |
| Evaluation     | present | present (unchanged) | NOT RUN | `/sara-eval` not run live; process untouched |
| Golden tasks   | frozen | frozen (unchanged) | PASS | `SARA_GOLDEN_TASKS.md` not in git status (untouched) |
| AGENTS.md policy | stale v2 + m.barani paths, full v2 section | host-neutral, condensed v2 note; all doctrine intact | PASS | Decision Ladder, self-review, gates verified present, grep clean |

## Validation detail

- Runtime: `node --test test/sara-plugin.test.mjs` -> 4 pass / 0 fail.
- Skills: `opencode debug skill` lists sara-review, sara-debt, read-terminals.
- read-terminals: `python read_terminals.py list/show/todos` all return data.
- Python: `py_compile` OK.
- Config discovery: commands (4), agents (3), skills (3) all present in scan dirs.
- Safety: `opencode.jsonc` byte-identical to backup (16 lines both).
