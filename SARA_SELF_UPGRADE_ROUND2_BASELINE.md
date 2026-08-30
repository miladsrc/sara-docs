# SARA SELF-UPGRADE ROUND 2 — TRUE BASELINE

Version: 2026-08-30 | Evidence-driven, reflects what EXISTS, not aspiration.

| Layer | Current Implementation | Actual Capability | Limitation | Upgrade Opportunity |
|-------|----------------------|-------------------|------------|---------------------|
| Interface | opencode TUI/CLI v1.18.25, model `opencode/big-pickle` | Full agent I/O, tools, subagents | Config not hot-reloaded | none within scope |
| Instructions | `AGENTS.md` (96 lines): identity, ladder, self-review, v2 bridge | Good instructions; always in context | No operational gating; relies on model compliance | Wire instructions to invokable gates + telemetry |
| Skills | 3 (`read-terminals`, `sara-review`, `sara-debt`) | On-demand review/debt/terminal procs | Advisory; no invocation record; no routing | Commands that invoke skills deterministically |
| Decision | Decision Ladder in AGENTS.md (instruction-only) | Heuristic advice | No classification, no record, no routing, unenforced | `/sara-decide` gate + persistent decision records |
| Task classification | none | all tasks same path | no class→route→review | classification block in `/sara-decide` |
| Orchestration | manual/ad-hoc | flexible manual control | no state, no failure taxonomy, no retry policy | commands + agent routing + decision records |
| Subagents | built-ins `build/plan/general/explore` | exploration + delegation | no architect/reviewer/auditor roles | 3 role agents w/ deny-edit perms |
| Tools | opencode built-ins | full read/edit/bash/search/web | no usage telemetry, redundancy invisible | plugin hook `tool.execute.after` → state NDJSON |
| Memory | `memory/sara.md` manual append | session continuity | unstructured, manual, single file | decision records + telemetry as durable state |
| Models | single model, no `small_model` | one size fits all | no routing by task class | deferred (not justified on this host yet) |
| Execution | opencode primary loop | runs whatever Sara decides | no gate before heavy execution | decision gate before multi-step work |
| Verification | manual tests/lint + self-review checklist | correctness checks on demand | no counterparty review; no review routing | reviewer/architect subagents by risk tier |
| Evaluation | none | — | cannot measure improvement or regression | telemetry + golden tasks + before/after records |
| Feedback | memory/sara.md | note-taking | no failure classification, no loop | failure taxonomy in decision records |
| Persistence | memory/sara.md | survives sessions | no records of decisions/actions | `state/tool-events.ndjson`, `SARA-DECISIONS.md` |

## Honest summary

- **L1 (instructions):** strong — decision ladder + self-review are real heuristics.
- **L2 (skills):** 3 focused skills exist.
- **L3 (workflow/orchestration):** **absent** — no gates, no routing, no tiers.
- **L4 (runtime):** nothing Sara-owned runs at runtime (no hooks, no plugin).
- **L5 (measured behavior):** absent — Round 1 itself is "NOT MEASURED".

Round 2's job is therefore L3/L4 with an L5 attempt, not more L1/L2.