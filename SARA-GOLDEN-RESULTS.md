# SARA-GOLDEN-RESULTS

Round 2 evaluation records. One entry per `/sara-eval` run. Evidence-labeled:
MEASURED / OBSERVED / INFERRED / NOT-MEASURED. Never fabricate numbers.

---

## G5 — AI-vs-non-AI (CSV row-set equality)

**Date:** 2026-08-30 | **Model:** opencode/big-pickle | **Run:** demo (post-Round-2)

### Decision block (emitted before implementation)
- Task Class: CODE | AI Needed: **NO** | Agent Needed: **NO**
- Complexity: L1 | Review Tier: 1 (self-review)
- Reason: deterministic row-compare is plain code; no ambiguity, no cost/privacy risk. AI would be strictly worse.
- Evidence: n/a (decision stage)

### Metrics (captured during the demo run)
| Metric | Value | Evidence |
|--------|-------|----------|
| tool calls | 3 (write script, generate CSVs, run checks) | OBSERVED (counted in run) |
| iterations / repairs | 0 | OBSERVED |
| files created | 4 (script + 3 CSVs) | MEASURED |
| LOC added | 7 (script) + 3 data files | MEASURED |
| dependencies added | 0 | MEASURED |
| correctness | IDENTICAL (shuffled order) + DIFFERENT (extra row), both expected | MEASURED (python exit checks) |

### Conclusion
Deterministic route chosen; correct on both cases; no AI/agent spawned. Minimal
tool surface (3 calls). This is the "after" baseline for G5.

### Limitations
Tool-call count is from the live run, not yet the plugin telemetry file —
`tool-events.ndjson` recording starts on the next opencode restart. Future G5
runs must read the count from telemetry (MEASURED), not from the run transcript.

*Superseded 2026-08-30: telemetry is now recording (see live re-run below).*

---

## G5 — AI-vs-non-AI (CSV row-set equality) — LIVE RE-RUN

**Date:** 2026-08-30 | **Model:** opencode/big-pickle | **Run:** live, post-versioning

### Decision block (emitted before implementation)
- Task Class: CODE | AI Needed: **NO** | Agent Needed: **NO**
- Complexity: L1 | Review Tier: 1 (self-review)
- Reason: deterministic; AI strictly worse.
- Evidence: n/a (decision stage)

### Metrics
| Metric | Value | Evidence |
|--------|-------|----------|
| tool calls | 2 bash calls in task window | OBSERVED (transcript) |
| telemetry | `tool-events.ndjson` grew 233 → 236 lines (+3) over window | MEASURED (plugin) |
| iterations / repairs | 0 | OBSERVED |
| files created | 3 (a.csv, b.csv, c.csv) | MEASURED |
| LOC added | 13 lines data (no code written; compare = one-liner) | MEASURED |
| dependencies added | 0 | MEASURED |
| correctness | a↔b IDENTICAL (order-insensitive); a↔c and b↔c DIFFERENT (extra row) — both as expected | MEASURED |

### Conclusion
Live run confirms the plugin telemetry pipeline works end-to-end (decision is
traceable in the eval `state/`), replacing the earlier "post-restart" limitation.
Deterministic compare returns correct results on both cases with no AI/agent.