# ADR-002 — Integrate Ponytail v5.3.2 through Sara's existing owners

**Status:** accepted
**Date:** 2026-10-26
**Owner:** m.barani
**Supersedes:** the capability design recorded in
`archive/PONYTAIL_SELF_UPGRADE_REPORT.md` (v4.9.0 adaptation) — its history is
kept, its *claims about the live host* are corrected here.

## Context

The archived report describes a v4.9.0 adaptation that added a decision ladder
and self-review section to `AGENTS.md` plus two skills, `sara-review` (complexity
only) and `sara-debt`, on top of `/sara-*` command gates, three reviewer agents,
and `plugin/sara.js` telemetry.

**FACT (re-verified 2026-10-26 with `opencode debug config`, `opencode debug
agents`, and directory listings):** none of that exists on this host. The live
runtime is `C:\Users\m.barani\.config\opencode` — single config source, no
overrides, opencode `v2.1.4`, not a git repository. It holds 14 agents (`sara`,
`hmyar` + 12 specialists), 9 skills before this change, `AGENTS.md` at 3699 B
with **no** ladder, self-review, or `sara:` rule, and no `command/`, `test/`,
`state/`, or `plugin/sara.js`. Agents `architect`, `reviewer`, `auditor` do not
exist; the equivalent roles are `review` and `security`.

Consequence: "preserve the existing ownership map" could not be honoured
literally — there was nothing there to preserve. Per owner decision of
2026-10-26, the integration adapts to the owners that *do* exist and adds only
what has no owner at all.

Upstream pinned for this work: **Ponytail v5.3.2**, tag commit
`16352ac229eb08a9598dcae48fe9f2b342567d86` (npm `@dietrichgebert/ponytail`
5.3.2), MIT. The previous adaptation was v4.9.0 (`0a4dd63a`).

## Decision

Integrate the current Ponytail capability set **through Sara's existing owners**,
adapt-and-add only where no owner exists. Concretely:

| Upstream capability | Action | Owner after this change |
|---|---|---|
| Smallest-complete-change ladder (`skills/ponytail/SKILL.md`, upstream `AGENTS.md`) | **add missing** (adapted, compact) | `<config>/AGENTS.md` — always-on policy is the only place it can actually fire |
| Quality review, change-scoped (`ponytail-review`) | **add missing** | `skills/sara-review/SKILL.md`, executed by the `review` agent |
| Whole-repo audit (`ponytail-audit`) | **upgrade existing** — same procedure, `repo` scope | `skills/sara-review/SKILL.md` (one owner, two scopes; no third skill) |
| Debt ledger (`ponytail-debt`) | **add missing** (marker adapted) | `skills/sara-debt/SKILL.md` |
| `shortcut:` marker rename | **recognized, not adopted** | `sara:` stays primary; `shortcut:` and `ponytail:` remain valid |
| Mode intensity (lite/full/ultra) | **omitted** | not applicable — see below |
| Always-on plugin (`opencode plugin add`) | **omitted** | not installed — see below |
| `/ponytail*` commands | **omitted** | command gates remain OQ-003 |
| Benchmarks, judges, gain scoreboard, 20+ adapters | **omitted** | upstream's own numbers are not Sara's results |

### Why the plugin is not installed

`ponytail.mjs` does three things: appends its ruleset to the system prompt on
every turn (context + compaction hooks), registers its own commands and skills,
and persists a mode in `<config>/.ponytail-active`. Installing it
would inject a second always-on policy next to `AGENTS.md` (the same rule stated
twice, competing for precedence), register `/ponytail*` commands beside the
project's own owner map, and add mode state that nothing in Sara's operating
model reads. The chosen capabilities are reachable through skills, which load on
demand. Compatibility was not the blocker: the plugin supports both OpenCode
plugin APIs (V2 `setup(ctx)` and V1 `server()`), and this host runs v2.1.4 — but
the benefit is zero and the duplication risk is real.

### Why mode intensity is omitted

Sara is a supervisor, not a code generator with a dial. Adding lite/full/ultra
means three rule variants × persisted state × user confusion, to express a
preference the ladder already handles by judgement. Same reasoning as the v4.9.0
report; this ADR re-affirms it rather than inheriting it unexamined.

## Ownership map as it actually is

| Concept | Canonical owner |
|---|---|
| Task class, complexity L0–L4, **review tiers**, gates | `architecture/OPERATING-MODEL.md` |
| Review procedure + lean/complexity taxonomy | `<config>/skills/sara-review/SKILL.md` |
| Debt semantics + marker forms | `<config>/skills/sara-debt/SKILL.md` |
| Shortcut convention (`sara:`) | `<config>/AGENTS.md` |
| Permission enforcement | `<config>/agent/*.md` frontmatter (`edit: deny` on review/security) — `opencode.jsonc` carries no permission block on this host |
| Telemetry | none produced (OQ-002) |

The review skill **references** tiers and never restates them; the `review`
agent's contract gained a procedure pointer, not a copy.

## Consequences

- **Behaviour change:** new sessions get the ladder from `AGENTS.md`; `sara-review`
  and `sara-debt` are discoverable and route to the `review` agent. Existing
  skills, agents, memory, models, providers and permissions are untouched.
- **Context cost:** `AGENTS.md` 3699 B → 5120 B (+29 lines, +1421 B), always
  loaded. Accepted because the ladder governs every coding task and its failure
  mode (under-engineering) is the one the v4.9.0 wording invited.
- **Cost of omission:** no telemetry, no slash gates, no mode switching — none of
  which was claimed as delivered.
- **Reversibility:** delete the two skill directories and restore
  `.sara-backup-2026-10-26-ponytail-v5/AGENTS.md` +
  `.sara-backup-2026-10-26-ponytail-v5/agent/review.md` (SHA-256 recorded in the
  2026-10-26 daily record). Each is a single-file operation.
- **INHERITED OBLIGATION:** the live runtime is still not git-tracked (OQ-001), so
  these edits exist as files plus a backup, not as history.

## Verification (what actually ran — full detail in the daily record)

- [x] `opencode debug config` — config parses; single source, no overrides
- [x] `opencode debug agents` — all 14 Sara agents still load
- [x] both new skills registered live in a running session (runtime notice), and
      their descriptions match the intent
- [x] debt scan on a fixture: 4/4 marker forms found, 1 `no-trigger` flagged,
      prose mentioning the convention excluded
- [x] review on a fixture commit: caller-break, SQL injection, wrong-day bug,
      missing test, and lean findings all reported in the skill's format; the
      fixture was left byte-identical (read-only respected)
- [x] `sara:` markers across 32 local repos: 0 code annotations exist, so nothing
      was renamed or rewritten
- [x] `python scripts/validate_docs.py` and `python -m pytest tests -q`
- [ ] one golden task as an AFTER-only probe (no before-run on this host, so no
      improvement claim — OQ-006)
- [ ] fresh interactive opencode session restarted by the owner

## Evidence

- FACT: upstream `v5.3.2` = `16352ac2`; `npm view @dietrichgebert/ponytail
  version` → 5.3.2 (this session).
- FACT: upstream renamed its own marker `ponytail:` → `shortcut:` in v5
  (`skills/ponytail-debt/SKILL.md` at that tag).
- INFERRED: the archived v4.9.0 report was written on a different host; the live
  surface here never received it. Impact if wrong: the files would exist twice —
  they do not.
