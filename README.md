# sara-docs — Sara's operating manual

The knowledge base that governs **how Sara does software development**: which
workflow a task follows, which agent handles which stage, what evidence counts
as proof, and when work may not proceed.

This is not a report archive. Reports describe what already happened; these
files decide what happens next.

**Verified: 2026-10-25** · host `m.barani` · opencode `v2.1.4`

## Start here

| You want to… | Read | Then |
|---|---|---|
| understand what Sara is and may touch | [architecture/SELF-BOUNDARY.md](architecture/SELF-BOUNDARY.md) | [architecture/SYSTEM-MAP.md](architecture/SYSTEM-MAP.md) |
| know how a task gets classified and gated | [architecture/OPERATING-MODEL.md](architecture/OPERATING-MODEL.md) | [workflows/delegation.md](workflows/delegation.md) |
| build a feature | [workflows/feature.md](workflows/feature.md) | dispatch from [roster/README.md](roster/README.md) |
| fix a bug | [workflows/bugfix.md](workflows/bugfix.md) | — |
| change a schema or migration | [workflows/db-migration.md](workflows/db-migration.md) | — |
| clean up code without changing behavior | [workflows/refactor.md](workflows/refactor.md) | — |
| review someone's work | [workflows/code-review.md](workflows/code-review.md) | — |
| respond to something broken in production | [workflows/incident.md](workflows/incident.md) | — |
| change Sara herself | [workflows/self-upgrade.md](workflows/self-upgrade.md) | — |
| decide which agent to use | [roster/README.md](roster/README.md) | [workflows/delegation.md](workflows/delegation.md) |
| measure whether Sara is getting better | [evaluation/GOLDEN-TASKS.md](evaluation/GOLDEN-TASKS.md) | [evaluation/results/](evaluation/results/) |
| know what is still unknown | [backlog/open-questions.md](backlog/open-questions.md) | — |

## Repository map

```
sara-docs/
├── AGENTS.md              operating contract: session protocol, knowledge
│                          classification, evidence rules, doc rules
├── memory/                durable state — current-state, decisions (ADR),
│                          daily session records, lessons learned
├── architecture/          SYSTEM-MAP (verified inventory) · OPERATING-MODEL
│                          (classification → gating) · SELF-BOUNDARY (scope)
├── workflows/             the SDLC playbooks — one per recurring job
├── roster/                routing table + per-agent contracts
├── evaluation/            golden tasks, dated results, telemetry contract
├── backlog/               open questions with owners and blocking severity
├── scripts/               validators: structure, host drift, links, secrets
├── tests/                 tests for the validators
└── archive/               frozen history — old reports, kept as evidence only
```

## How to keep this honest

```powershell
python scripts/validate_docs.py     # the gate: structure, drift, links, secrets
python -m pytest tests -q           # proof that the gate itself works
```

`archive/` is exempt from freshness rules on purpose: it is history and must not
be edited to look current. If an archived claim is wrong today, the fix belongs
in a living doc, with the archive left as the record of what was believed then.

## Status

Foundation (structure, validators, entry point, memory, backlog) is in place.
Workflows, roster contracts, and the architecture docs are being written in this
same build. Anything not yet migrated is tracked in
[backlog/open-questions.md](backlog/open-questions.md).

## What this repo is not

- Not Sara's runtime. The live runtime is the opencode config surface at
  `C:\Users\m.barani\.config\opencode` — see
  [architecture/SYSTEM-MAP.md](architecture/SYSTEM-MAP.md) for the verified
  boundary between the two.
- Not project source code. It never contains application code, only how Sara
  approaches it.
