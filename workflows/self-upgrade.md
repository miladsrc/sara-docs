# Workflow — Self-upgrade

Changing Sara herself: policy, agents, skills, plugins, permissions, memory
structure. Scope rules live in
[../architecture/SELF-BOUNDARY.md](../architecture/SELF-BOUNDARY.md); this file
owns the **procedure**.

The governing asymmetry: a wrong project change is reverted; a wrong change to the
agent making changes propagates into everything it touches afterwards.

---

## Stages

### 1. Proposal — before any edit

Written, not spoken. Contains:

- **What** changes: exact files, exact intent.
- **Why** the current state is inadequate, with evidence (a failure, a gap, a
  measured cost) — not preference.
- **Blast radius**: what behaviour could change, for which tasks.
- **Reversibility**: the exact revert steps.
- **Cost**: new files, new mechanisms, maintenance burden. Say "zero" explicitly
  when it is zero.
- **What stays unchanged**: the non-goals.

Present it and **stop**. Do not begin implementation while proposing.

**Gate:** proposal delivered and owner has responded.

### 2. Approval — G3

The owner must approve **this proposal**, explicitly. Ambiguous enthusiasm is not
approval. Approval of a goal ("improve yourself") does not authorize a specific
restructure — ask for the method.

Record the approval verbatim in the ADR.

### 3. Back up

- Copy the affected files first. Without live-config git tracking (OQ-001), the
  backup *is* the rollback.
- Record the backup location in the ADR.

### 4. Implement the smallest version

- Smallest change that satisfies the proposal.
- One concern per change. A policy rewrite plus a new skill is two changes.
- Do not improve adjacent things because you are already in the file.
- Preserve every non-negotiable listed in the boundary doc.

### 5. Verify

| Check | How |
|---|---|
| Files parse | JSON/JSONC parse; markdown links resolve |
| Capability still works | run the affected skill/agent once, live |
| Behavior unchanged where claimed | re-run the probe set (below) |
| Permissions not weakened | diff `opencode.jsonc` — an `ask` gate must not become `allow` silently |
| Docs consistent | `python scripts/validate_docs.py` in this repo |

### 6. Restart requirement

Config is loaded at session start and is **not hot-reloaded**. State clearly:
which changes take effect only after an opencode restart. Never claim a config
change is live when the running process still holds the old config.

### 7. Record

- ADR: proposal, approval, change, verification, revert steps.
- Update [../memory/current-state.md](../memory/current-state.md) and refresh its
  `Verified:` date.
- If the change was made because of a failure, add the lesson to
  [../memory/lessons-learned.md](../memory/lessons-learned.md).

## Probe set before/after

A self-upgrade without a before/after comparison cannot demonstrate improvement.
Minimum: one task per class it touches — a code task, a delegation task, and a
gate-retention check. Reuse [../evaluation/GOLDEN-TASKS.md](../evaluation/GOLDEN-TASKS.md)
and record results under `evaluation/results/`.

If no probe was run, the report must say **"improvement not measured"** in those
words.

## Definition of done

- [ ] written proposal with blast radius and revert steps
- [ ] explicit approval of that proposal, quoted in the ADR
- [ ] backup taken and its location recorded
- [ ] change limited to the proposal's scope
- [ ] non-negotiables intact (approval duty, no-secrets, non-destructive, honest evidence)
- [ ] permission gates not weakened
- [ ] probes run before/after, or "not measured" stated
- [ ] restart requirement stated
- [ ] ADR + current-state + daily record written

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| "Improving yourself" interpreted as license to restructure | the agent picks its own constraints |
| Editing the boundary doc to permit the change | the gate redefines itself |
| Weakening a permission gate to remove friction | safety removed silently, no user-visible event |
| Shipping without a probe run | no evidence of improvement, only of activity |
| Config change reported as live before restart | false claim about the running system |
