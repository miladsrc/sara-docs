# Agent roster and contracts

Verified: 2026-10-26 · source of the roster: `<config>/agent/**`

Whom Sara delegates to, when, and what each one returns.

**Ownership note.** The live agent definitions in `<config>/agent/**` own *how each
agent behaves* (its prompt and rules). This file owns *when to route to it* and
*what contract it must satisfy*. It deliberately does not restate the prompts —
duplicating them is how the previous doc set drifted out of truth.

---

## Routing table

| Signal from the task | Agent | Read-only |
|---|---|---|
| "which files / where is / how does this work" | `discovery` | yes |
| "should we / design this / what is the plan" | `planner` | yes |
| "break this down into ordered steps with dependencies" | `orchestrator` | yes |
| "which path does this task take / does it need approval" | `router` | yes |
| "implement / patch / fix this code" | `coding` | no |
| "schema / migration / query / data repair" | `database` | no (proposes first) |
| "write tests / run the suite / why does this test fail" | `testing` | no |
| "review this with fresh eyes" | `review` | yes |
| "is this safe / authz / secrets / permissions" | `security` | yes |
| "check docs, versions, compatibility, prior art" | `research` | yes |
| "grade this against the criteria" | `evaluation` | yes |
| "it broke, and the cause is unclear" | `recovery` | no (diagnoses, then proposes) |

Primary agents (not delegated to — they *are* the session): `sara` (supervisor,
default) and `hmyar` (Hamtayar project teammate, loads state from the `hmyar`
repository).

## Contracts

Format — **In**: what the brief must supply · **Out**: what it must return ·
**Fails when**: its characteristic failure modes.

### `discovery`

- **In**: the question, the search scope (paths/repos), and any facts already known.
- **Out**: an artifact map — file paths with line references, what each thing
  does, and what it could *not* find.
- **Fails when**: asked a design question instead of a location question; or when
  the scope is "the codebase" and it returns a plausible summary with no paths.

### `planner`

- **In**: the goal, constraints, non-goals, and grounded facts (from discovery).
- **Out**: ordered steps, per-step risk, budgets, validation criteria, and the
  failure points.
- **Fails when**: input is ungrounded — it will produce a confident plan for a
  codebase it has not read.

### `orchestrator`

- **In**: a multi-step goal and the available agents.
- **Out**: a dependency-aware DAG with owners per step, checkpoints, and state
  transitions.
- **Fails when**: the task is actually linear; the DAG adds ceremony without
  removing risk.

### `router`

- **In**: the raw goal.
- **Out**: classification, required agents, order, and whether approval is needed.
- **Fails when**: it classifies from the wording rather than the actual risk.

### `coding`

- **In**: the plan, the files in scope, the convention to follow, and the
  verification command.
- **Out**: a focused patch plus the tests and the command output that prove it.
- **Fails when**: scope is vague — it will refactor the neighbourhood; or when the
  verification command is omitted, in which case completion is unproven.

### `database`

- **In**: the schema intent, the migration tool, the target environment, and the
  data-loss tolerance.
- **Out**: a reversible changeset, the forward and rollback commands, and the
  measured risk.
- **Fails when**: asked to "just fix the data" — it must classify and propose
  before writing anything.

### `testing`

- **In**: the behaviour under test and the project's test runner.
- **Out**: tests, a run, and a diagnosis classified as real bug / test defect /
  environment problem.
- **Fails when**: the failure classification is skipped and every red is treated
  as a code bug.

### `review`

- **In**: the diff, the requirement, and the review tier.
- **Out**: a verdict (APPROVE / APPROVE WITH COMMENTS / REQUEST CHANGES / BLOCK),
  findings with severity and location, and a "not verified" section.
- **Procedure**: `<config>/skills/sara-review/SKILL.md` — it owns the method and
  the lean taxonomy, and covers both a change and a whole repo. Tiers are
  referenced from `../architecture/OPERATING-MODEL.md`, never restated.
- **Fails when**: given the author's narrative instead of the diff — it reviews
  intentions rather than code.

### `security`

- **In**: the change plus the trust boundary it sits on.
- **Out**: findings with exploitability and severity, each with a location.
- **Fails when**: scoped to "review everything" — generic checklist output with no
  exploitability assessment.

### `research`

- **In**: a specific question and the version/context constraints.
- **Out**: cited findings, explicitly dated, with conflicting sources surfaced.
- **Fails when**: asked to decide. It returns options, not verdicts.

### `evaluation`

- **In**: the artifact and the acceptance criteria (or KPIs).
- **Out**: per-criterion score with evidence, plus a regression note against prior
  runs.
- **Fails when**: the criteria are unstated — it will invent them, and the score
  becomes opinion.

### `recovery`

- **In**: the failure (symptom, logs, what changed) and the constraint (may it be
  restarted? is data at risk?).
- **Out**: failure class, most likely cause with distinguishing evidence, and a
  recovery strategy ordered by reversibility.
- **Fails when**: asked to act before diagnosing — it will restart things.

## Dispatch rules

- Handoffs follow [../workflows/delegation.md](../workflows/delegation.md) — six
  sections, one question, evidence required.
- Never dispatch two agents to write to the same files in parallel.
- The dispatcher verifies load-bearing claims; a subagent's confidence is not
  evidence.
- An agent's error is the brief's error. Fix the handoff, not just the output.

## Known gaps

- `hmyar` has no memory file under `<config>/memory/` while every other agent
  does — tracked as OQ-004.
- No agent currently owns **accessibility** review; that falls to `coding` or
  `review` with an explicit note that the specialty is missing. Performance/load
  analysis is now inside `sara-review` (#3 and #5 of its check list), not a
  separate role.
