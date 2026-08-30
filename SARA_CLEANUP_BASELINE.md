# SARA Cleanup — Baseline

Date: 2026-08-30
OpenCode version: 1.18.25
Sara runtime: opencode config surface at `C:\Users\98903\.config\opencode\` (no separate Sara process)
Current branch: n/a (config dir not git-tracked; sara-docs on `main`)
Current commit (sara-docs): `daf7c71 feat(sara): complete round 2 self-upgrade`
Working tree (sara-docs): clean except untracked `.idea/`, `java/`, `ponytail/`, `PROGRESS-PHASE-2.md`, `SARA_ARCHITECTURE_CLEANUP_REPORT.md`

## Host identity

- OS username: `98903`
- User profile: `C:\Users\98903`
- NOTE: several Sara files still reference `m.barani` (another machine/user). Those are stale on this host.

## Repositories inspected

| Repo / dir | Tracked? | Notes |
| ---------- | -------- | ----- |
| `C:\Users\98903\IdeaProjects\sara-docs` | git (origin github.com/miladsrc/sara-docs.git) | docs only |
| `C:\Users\98903\.config\opencode` | NOT git-tracked (0 tracked files) | full Sara runtime surface |
| `sara-docs/ponytail/` | vendored upstream (own .git) | unrelated 3rd-party plugin project |
| `sara-docs/java/` | untracked | trivial Java scaffold (PositiveSum) |
| `sara-docs/.idea/` | untracked | JetBrains IDE state |

## Files in scope (Sara runtime config)

- `~/.config/opencode/AGENTS.md`
- `~/.config/opencode/opencode.jsonc`
- `~/.config/opencode/command/sara-decide.md`, `sara-review.md`, `sara-audit.md`, `sara-eval.md`
- `~/.config/opencode/agent/architect.md`, `reviewer.md`, `auditor.md`
- `~/.config/opencode/skills/sara-review/SKILL.md`, `sara-debt/SKILL.md`, `read-terminals/SKILL.md`, `read-terminals/read_terminals.py`
- `~/.config/opencode/plugin/sara.js`, `test/sara-plugin.test.mjs`
- `~/.config/opencode/memory/sara.md`

## Files excluded

- `ponytail/`, `java/`, `.idea/` — unrelated / temp / IDE state (stay out of versioned Sara layout)
- `SARA_GOLDEN_TASKS.md` — frozen per Phase 13

## Known risks

1. Config dir not under git -> every edit needs a local backup (in `cleanup-backup-20260830/`).
2. Stale `m.barani` paths break read-terminals and mislead context on this host.
3. Filing decision schema in a bare `policy/` file would NOT be auto-loaded (see OpenCode discovery constraints).
4. Several Sara files describe a v2 Gateway that is NOT present on this host.

## OpenCode discovery constraints (verified via `opencode debug skill`)

Only these locations are auto-discovered/loaded:
- Commands: `~/.config/opencode/command/*.md`
- Agents: `~/.config/opencode/agent(s)/*.md`
- Skills: `~/.config/opencode/skill(s)/<name>/SKILL.md`
- Global instructions: `~/.config/opencode/AGENTS.md`

A bare `policy/decision-block.md` or any arbitrary nested markdown is NOT loaded by any mechanism. Any canonical doctrine must live at one of the discovery locations above, or be explicitly read by a consumer prompt.
