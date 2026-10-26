# SARA Post-Cleanup Duplication Audit

Date: 2026-08-30. Method: grep of the Sara config surface (`~/.config/opencode`)
after cleanup. Classified per Phase 19.

## Decision schema

| Location | Class | Note |
| -------- | ----- | ---- |
| `command/sara-decide.md` | canonical owner | full field + classification enum |
| `agent/architect.md` | derived / interface | lists required fields, defers values to sara-decide |

Verdict: 1 authoritative owner; architect holds the stable interface only.
No competing full copy. PASS.

## Classification

Single enum source (`EXISTING-CAPABILITY | CONFIGURATION | ...`) — only in
`sara-decide.md`. Consumers use the enum name. PASS.

## Review tiers

| Location | Class | Note |
| -------- | ----- | ---- |
| `AGENTS.md` (Review routing) | canonical owner | Tier 0-3 definitions |
| `sara-decide.md` | consumer | assigns tier value + routes by it, references AGENTS.md |
| `sara-review.md` | consumer | routes by risk scope, references |

Verdict: 1 authoritative definition; consumers assign/reference. PASS.

## Complexity taxonomy

| Location | Class | Note |
| -------- | ----- | ---- |
| `skills/sara-review/SKILL.md` | canonical owner | full 5-tag definitions + examples |
| `reviewer.md`, `auditor.md`, `sara-review.md`, `sara-audit.md` | consumers | name the tags, reference |

Verdict: 1 owner of the full taxonomy; consumers name tags only. PASS.

## Debt semantics

| Location | Class | Note |
| -------- | ----- | ---- |
| `skills/sara-debt/SKILL.md` | canonical owner | sara: marker, ceiling/upgrade, no-trigger, output |
| `agent/auditor.md` | consumer (now references) | step 3 defers debt semantics to sara-debt |

Verdict: 1 owner; auditor points to it. PASS.

## Safety inventory

- `opencode.jsonc` = mechanism (ask-gates). `AGENTS.md` = policy/intent.
- No duplicated mechanical inventory removed; policy now frames the boundary.
  PASS.

## Telemetry schema

- Producer: `plugin/sara.js`. Interface: `SARA_TELEMETRY_CONTRACT.md`.
  No duplicated implementation logic. PASS.

## Success criterion

> **No competing source of truth.**

Remaining textual repetition is intentional interface naming (consumers
reference the concept) — classified as `derived`/`harmless`, never a competing
owner. Criterion met.
