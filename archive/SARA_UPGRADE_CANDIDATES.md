# SARA UPGRADE CANDIDATES — ROUND 2

Version: 2026-08-30 | Decision: IMPLEMENT / ADAPT / CONFIGURE / DEFER / REJECT

Driven by baseline: the gaps are operational (L3/L4 absent). Candidates that
would only add more instructions/skills are rejected or folded into the
minimum runtime set.

| # | Candidate | Current Layer | Desired Layer | Problem | Benefit | Complexity | Risk | Evidence Needed | Decision |
|---|-----------|---------------|---------------|---------|---------|------------|------|-----------------|----------|
| 1 | Architecture decision gate | L1 (instructions) | L3 | No structured pre-implementation classification | Correct route chosen; persistent decision record | LOW (1 command + schema) | LOW | Record exists | **IMPLEMENT** |
| 2 | AI suitability decision | L1 | L3 | No "when NOT to use AI" data | Avoids AI where deterministic code suffices | LOW | LOW | Decision record field | **ADAPT** (folded into candidate 1 — one gate, three decisions) |
| 3 | Agent suitability decision | L1 | L3 | No yes/no-agent reasoning | Avoids agent spawn for workflows/functions | LOW | LOW | Decision record field | **ADAPT** (folded into candidate 1) |
| 4 | Multi-agent routing | none | L3/L4 | Only generic explore/general | Real role separation | MED (3 role agents) | MED | Role used in recorded decisions | **IMPLEMENT** (subset: architect, reviewer, auditor) |
| 5 | Review routing (tiers) | none | L3 | Every task same no-review path | Risk-proportional verification | LOW-MED | MED | Tier chosen in decision records | **IMPLEMENT** (tier logic in `/sara-decide` + routed agents) |
| 6 | Evidence / decision records | none | L3 | No persistence of decisions | Facts vs assumptions traceable | LOW | LOW | Records exist in repo | **IMPLEMENT** |
| 7 | Tool efficiency telemetry | none | L4 | Redundant reads/searches invisible | Data to find redundancy | LOW (plugin hook) | MED (runtime risk) | NDJSON produced, tested | **IMPLEMENT** (measure only; no enforcement yet) |
| 8 | Continuous evaluation | none | L3/L4 | No before/after | Show improvement/regression | LOW-MED | LOW | Golden-task records | **IMPLEMENT** (minimum: golden set + records) |
| 9 | Golden task set | none | L3 | No repeatable probe | Honest task-level baseline | LOW | LOW | Tasks runnable | **IMPLEMENT** |
| 10 | Failure classification | none | L3 | Failures not categorized | Feedback loop entry | LOW | LOW | Taxonomy used in records | **ADAPT** (schema in candidate 6) |
| 11 | Human control / autonomy | L1 rule only | L4 | Destructive ops not gated mechanically | Approval enforced at runtime | LOW | MED | Permission rules active | **IMPLEMENT** (permission config + documented levels) |
| 12 | Model routing | none | L4 | Single model | — | HIGH | HIGH | Multi-model infra | **REJECT** (no multi-model infra; not justified on this host) |
| 13 | Memory mechanism | L1 single file | — | Manual notes only | — | — | — | — | **CONFIGURE** (keep sara.md; add records + telemetry as durable state; no new memory service) |
| 14 | RAG | none | — | No retrieval need proven | — | HIGH | HIGH | — | **REJECT** (documented decision: grep/glob/webfetch/tool-search suffice) |
| 15 | Whole-repo audit | none | L3 | Repo-wide complexity invisible | Ranked findings | LOW | LOW | Audit runnable | **ADAPT** (via auditor agent + `/sara-audit`) |
| 16 | Benchmark infrastructure | none | L5 | — | — | HIGH | HIGH | — | **REJECT** (golden set + records instead of LLM-judge infra) |

## Principle applied

No new intelligence where a deterministic mechanism suffices (commands,
agents, permissions). No agent where a workflow suffices (review tiers).
No workflow where a function suffices (decision schema). No RAG/big-memory/
benchmark infra — evidence lives in flat records + telemetry.