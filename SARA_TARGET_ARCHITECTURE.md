# SARA Target Architecture

Adapted to actual OpenCode discovery semantics (only `command/`, `agent/`,
`skills/*/SKILL.md`, and global `AGENTS.md` are auto-loaded).

```
                        SARA
                          |
           +--------------+----------------+
           |                               |
        POLICY (AGENTS.md)             EXECUTION (~/.config/opencode)
           |                               |
   +-------+-------+              +--------+---------+
   |       |       |              |        |         |
Decision  Tier  Taxonomy        Commands  Agents   Skills
(sara-   (AGENTS (sara-          (/sara-  (architect,
 decide) .md)    review)         decide,  reviewer,
   |       |       |              /sara-   auditor)
   +-------+-------+              review, |
                                  /sara-   |
                                  audit,   |
                                  /sara-   |
                                  eval)    |
                                     |     |
                                   Runtime (plugin/sara.js)
                                     |
                                   Telemetry (state/tool-events.ndjson)
                                     |
                                   Evaluation (/sara-eval, golden tasks)
```

## Owners (one per concept)

| Concept            | Canonical Owner               | Consumers (reference, not copy) |
| ------------------ | ----------------------------- | ------------------------------- |
| Decision schema    | `command/sara-decide.md`      | `agent/architect.md`            |
| Classification     | `command/sara-decide.md`      | `agent/architect.md`            |
| Review tiers       | `AGENTS.md` (Review routing)  | `sara-decide`, `sara-review`    |
| Complexity taxonomy| `skills/sara-review/SKILL.md` | `reviewer`, `auditor`, commands |
| Debt semantics     | `skills/sara-debt/SKILL.md`   | `agent/auditor.md`              |
| Safety mechanism   | `opencode.jsonc` (permission) | policy text in `AGENTS.md`      |
| Telemetry contract | `SARA_TELEMETRY_CONTRACT.md`  | `/sara-eval`                    |

## Boundaries

- Commands are thin workflow surfaces that route.
- Agents are specialized read-only reviewers (architect, reviewer, auditor).
- Runtime (plugin) is separate from policy (AGENTS.md).
- Generated state (`state/tool-events.ndjson`) is separate from source/config.
- Evaluation (`/sara-eval`, golden tasks) is separate from runtime.
- No circular dependencies: policy owns doctrine; execution owns behavior;
  runtime produces telemetry; evaluation consumes it.
