# System map

Verified: 2026-10-26 · host `m.barani` · opencode `v2.1.4`

Component inventory of Sara. The **current** verified values (counts, git state,
what is missing) live in [../memory/current-state.md](../memory/current-state.md)
— this file owns the *shape*, that file owns the *state*.

---

## What Sara is

Sara is not a standalone binary. She is a persona and a configuration surface
loaded by the **opencode** runtime:

```
opencode (product/runtime — infrastructure, not Sara)
  + <config>/AGENTS.md          persona + policy, auto-loaded every session
  + <config>/opencode.jsonc     default agent, instruction wiring
  + <config>/agent/**           role definitions (primary + subagents)
  + <config>/skills/**          procedures injected on demand
  + <config>/plugins/**         runtime hooks
  + <config>/memory/**          per-agent persistent memory
  = "Sara"
```

`<config>` = `C:\Users\m.barani\.config\opencode`.

Consequence: there is no Sara process to patch. Changing Sara means changing
config files, and config is loaded at session start — **not hot-reloaded**.

## Layers

| Layer | Owned by | Notes |
|---|---|---|
| Interface | opencode TUI/CLI | product feature, not extensible here |
| Prompt / policy | `<config>/AGENTS.md` | always loaded; size is a real cost |
| Agent roster | `<config>/agent/**` | 1 primary supervisor + 1 project agent + 12 specialists |
| Procedures | `<config>/skills/**` | loaded on demand by description match |
| Runtime hooks | `<config>/plugins/**` | tool interception, telemetry |
| Memory | `<config>/memory/**` | one file per agent, appended by that agent |
| Gating | `opencode.jsonc` `permission` | mechanical allow/ask/deny; **absent on this host** — the only denial in force is `edit: deny` in the `review` and `security` agent frontmatter |
| Documentation | this repository | procedures, contracts, evaluation |

## Procedure owners

One owner per reusable procedure. A skill that references another owner's
concept must not restate it.

| Procedure | Owner | Used by |
|---|---|---|
| Review a change or a repo (correctness, safety, load, tests, speed, lean) | `<config>/skills/sara-review/SKILL.md` | `review` agent, `code-review.md` workflow |
| Lean/complexity taxonomy (`delete`/`reuse`/`stdlib`/`native`/`yagni`/`merge`/`split`) | same file — it is the taxonomy's only home | `review`, `security` |
| Debt ledger + marker forms (`sara:`, `shortcut:`, `ponytail:`) | `<config>/skills/sara-debt/SKILL.md` | `review`, any audit |
| Task class, L0–L4, review tiers, gates | `architecture/OPERATING-MODEL.md` | everything above — referenced, never copied |
| Smallest-complete-change policy + `sara:` convention | `<config>/AGENTS.md` | every session |

## Two-surface rule

| Surface | Location | Change requires |
|---|---|---|
| **Live runtime** | `<config>/**` | [../workflows/self-upgrade.md](../workflows/self-upgrade.md) — proposal + owner approval |
| **Knowledge base** | this repository | normal doc workflow; validators must pass |

Confusing the two is the most common self-modification error: editing this repo
changes nothing about how Sara behaves until the live surface points at it.

## Agent roster shape

```
sara        primary   supervisor — plans, delegates, verifies, reports
hmyar       primary   project teammate for Hamtayar (separate repo memory)

specialists (subagents)
  intake      router, planner, orchestrator
  knowledge   discovery, research
  execution   coding, database, testing
  assurance   review, security, evaluation, recovery
```

Contracts for each — inputs, outputs, permissions, failure modes — live in
[../roster/README.md](../roster/README.md).

## Delegation capability

The runtime exposes subagents through the task tool. Delegation is only as good
as the brief: see [../workflows/delegation.md](../workflows/delegation.md) for the
handoff contract. A subagent starts with fresh context and cannot see this
conversation.

## Known structural limits

| Limit | Consequence | Tracked as |
|---|---|---|
| No `command/` directory | no invokable slash gates; rules live in prose | OQ-003 |
| No `state/` directory | no telemetry; evaluation cannot MEASURE tool cost | OQ-002 |
| No plugin test suite | plugin behaviour is unverified | OQ-002 |
| Live config not git-tracked | no history or rollback for Sara's own changes | OQ-001 |
| Config not hot-reloaded | every config edit needs an opencode restart | — |
| Memory is manual append | agents may forget to write; no validation | — |

These are recorded, not hidden. A limit that is written down can be decided
about; a limit that is omitted becomes a false claim of capability.
