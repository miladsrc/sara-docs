# SARA ARCHITECTURE — AFTER ROUND 2

Version: 2026-08-30

## Diagram (as implemented on the opencode runtime)

```text
                              SARA
        (opencode v1.18.25 + ~/.config/opencode/*  |  sara-docs repo)
                                │
                 ┌──────────────┴──────────────┐
                 │                              │
            DECISION LAYER                 EXECUTION LAYER
        /sara-decide command             opencode primary loop
        ├── Task classification          (single primary agent)
        ├── AI suitability    ──────┐
        ├── Agent suitability  ──────┤        TOOLS (built-in)
        └── Review tier        ──────┼─►      read/edit/write/bash/
                 │                   │        glob/grep/task/webfetch
              RECORDS                │        websearch/question/todowrite
        SARA-DECISIONS.md ───────────┼──►        │
                                     │          plugin sara.js
        SUITABILITY/REVIEW GATES      │    tool.execute.before/after
        architect agent ─────────────┼──►   → state/tool-events.ndjson
        reviewer agent ──────────────┘          (telemetry, L4)
        auditor agent ─── /sara-audit
                 │
             ROUTING
        /sara-review  →  tier → skill or subagent
                 │
          VERIFICATION
        self-review checklist + counterparty agents + bash tests
                 │
            EVALUATION
        /sara-eval → golden tasks (SARA_GOLDEN_TASKS.md)
        → SARA-GOLDEN-RESULTS.md (before/after, evidence-labeled)
                 │
             FEEDBACK
        failure taxonomy → decision records → revisit triggers
                 │
        CONTINUOUS IMPROVEMENT
        telemetry + records → candidate reassessment
```

## Autonomy control (permission layer, enforced by opencode)

- `ask` gates in `opencode.jsonc`: `git push*`, `git reset --hard *`,
  `git clean -fd *`, `rm -rf *`, `docker compose down -v *`, `dropdb *`.
- Behavioral tiers documented in AGENTS.md: autonomous / review / human-approval.

## Layer classification of the Round-2 additions

| Component | Layer | Mechanism |
|-----------|-------|-----------|
| `plugin/sara.js` | L4 | Runtime hook (telemetry) |
| role agents (`architect`, `reviewer`, `auditor`) | L3/L4 | Routed subagents with deny-edit |
| commands (`sara-decide`, `sara-review`, `sara-audit`, `sara-eval`) | L3 | Invokable workflows |
| `permission` rules | L4 | Runtime enforcement |
| AGENTS.md "Operational Gates" | L1 | Instructions referencing the above |
| golden set + decision records + eval results | L3 | Operational evidence loop |

## Key architectural fact

Sara has no process of her own; "runtime modifies" == opencode config surface.
The plugin is the only executable code Sara owns. Everything else routes
through opencode's native mechanisms (commands, agents, permissions) — no
framework was built, no new service, no new database.