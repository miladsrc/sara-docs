# SARA DECISIONS

Persistent decision ledger. One record per non-trivial decision. Tags:
FACT / OBSERVATION / ASSUMPTION / HYPOTHESIS / MEASURED RESULT.

---

## DECISION 001 — Version the whole Sara runtime surface in-place

**Date:** 2026-08-30
**Trigger:** Owner request — "fix it up, i want whole of you not just some docs
inside you." Prior cleanup left claims unverified: config changed but never
re-validated, evaluation never run live, runtime config dir untracked.

### Decision

Initialize a git repo directly in `~/.config/opencode` (the live runtime
surface) and commit the WHOLE of Sara: AGENTS.md, opencode.jsonc, tui.json,
command/, agent/, skills/, plugin/sara.js, package.json + package-lock.json,
memory/, test/. Ignore runtime artifacts (state/, node_modules/, __pycache__/)
and pre-git backups (*.bak*, cleanup-backup-*/) and IDE state (.idea/).

Rejected alternatives (architect second opinion, `ses_fae140be8ffeEkQMpkRl5l2r4k`):
- Mirror config into `sara-docs/opencode/` + sync script — rejected: creates a
  second copy of live truth, demands a bespoke sync mechanism, guarantees drift.
  Native tooling (git) already solves this.
- Keep relying on `.bak*` / `cleanup-backup-*` snapshots — rejected: manual,
  point-in-time, no history or diffing.

### Cost / unchanged behavior

Zero new mechanisms, zero new dependencies. Runtime behavior unchanged — this
task only adds versioning + validation, no code edits to plugin/skills/agents.

### Facts & tags

- FACT: `~/.config/opencode` was not a git repo; `.gitignore` there was the
  opencode default template (ignored package.json, lockfile, and itself) —
  contradicted the plan, rewritten.
- FACT: `memory/sara.md` contains infra-sensitive PROSE (internal IP
  192.168.236.22, gitlab.sidg.ir, PAT-handling notes) but zero literal secret
  strings. GitLab host already lives in AGENTS.md (also committed); the repo is
  local-only. Kept unscrubbed to preserve continuity.
- ASSUMPTION: no remote is added now. Adding a remote later bumps this to
  Tier 3 (credentials + memory/ exposure) and requires owner approval.
- ASSUMPTION: `.bak*` / `cleanup-backup-*` are now redundant (git history
  supersedes them); their deletion is a separate, later cleanup.

### Gates honored

- Task class: config/existing-capability. Complexity: L2. Review tier: 2.
- Architect second opinion: delivered (see record above).
- Gateway v2 absent on host — L1+ actions performed directly, disclosed.

### Verification (complete when all green)

1. `git status` clean after commit; expected tracked set matches SELF list.
2. Plugin test suite passes (`node test/sara-plugin.test.mjs`).
3. `opencode.jsonc` parses as valid JSON.
4. Capabilities live: `read-terminals` list/todos against live DB.
5. One golden eval task run live, recorded to `SARA-GOLDEN-RESULTS.md`.
6. Owner restarts opencode to load new config (config is not hot-reloaded).

---

**End of DECISION 001**