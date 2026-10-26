# Workflow — Feature

For adding new behaviour to an existing project. Classification and gates are
defined in [../architecture/OPERATING-MODEL.md](../architecture/OPERATING-MODEL.md);
this file owns the **sequence**.

Not this workflow: changing existing behaviour to something explicitly different
(treat as feature + its own review), schema changes
([db-migration.md](db-migration.md)), behaviour-preserving cleanup
([refactor.md](refactor.md)).

---

## Stages

### 1. Frame — G0 Requirement

- Restate the goal in one sentence, in your own words.
- List **non-goals**: what this deliberately does not do.
- Name the acceptance signal: the observable fact that proves it works.
- If the goal is ambiguous, ask one specific question instead of guessing. One
  question, not a questionnaire.

**Gate:** goal + non-goals + acceptance signal written down.

### 2. Ground — G1 Grounding

Never design against an assumed codebase.

- Locate the real files: entry point, the module that will change, the tests that
  cover it.
- Read the surrounding convention: naming, error handling, layering, test style.
- Check for an existing partial implementation of the same thing.
- Record paths and line references as evidence.

Dispatch [`discovery`](../roster/README.md) for anything spanning more than two
files or an unfamiliar module.

**Gate:** file paths + line refs + the convention to follow.

### 3. Plan — G2 Plan

The plan must state, in order:

1. files to create/modify and why each one
2. the failure points (what is most likely to break, and how you would notice)
3. the verification command(s) that will prove it
4. the rollback: how to undo if it goes wrong

L3 features get an independent plan review before implementation. A plan with no
failure points listed is not a plan.

**Gate:** ordered steps + verification commands + rollback.

### 4. Approve — G3 Approval

Required when: schema/contract change, auth/permission change, destructive step,
new dependency, or a change to Sara's own runtime. Quote the approval.
Otherwise record "G3 not required: L2, no contract impact".

### 5. Implement — G4

- Smallest change that satisfies the plan. No drive-by refactoring.
- Match the project's existing style, even where you would choose differently.
- New behaviour ships with its tests in the same change.
- Commit-sized: one logical change; do not mix formatting with behaviour.

**Gate:** diff matches the plan. If the plan was wrong, return to stage 3 and say
why — do not silently redesign.

### 6. Verify — G5

- Run the project's real command (its own test runner, not a proxy).
- Run the specific new tests **and** the surrounding suite.
- If a test cannot run in this environment, say exactly that. Never imply green.
- Paste the command and the result. MEASURED, not OBSERVED, when the run happened
  in this session.

**Gate:** command + output recorded; all suite results stated honestly.

### 7. Review — G6

Tier from the operating model. Tier 2+ means an independent reviewer that did not
write the code ([code-review.md](code-review.md)). Authors do not approve their
own L3 work.

### 8. Record — G7

- Update [../memory/current-state.md](../memory/current-state.md) if state changed.
- Daily record: what was built, how it was verified, what stayed open.
- ADR if the feature made a decision someone will later ask "why?" about.

## Definition of done

- [ ] goal, non-goals and acceptance signal stated
- [ ] code follows existing convention, tests included in the same change
- [ ] test command run with output recorded (or the inability stated plainly)
- [ ] diff limited to the planned scope
- [ ] review gate satisfied for the tier
- [ ] state/daily record written
- [ ] no secrets, no debug leftovers, no commented-out code

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| Coding before locating the real entry point | builds a parallel implementation next to the real one |
| "Tests pass" without a command | the most common false claim in this repo's history |
| Redesigning while implementing | diff exceeds the plan; review cannot isolate risk |
| Adding a dependency for a 20-line problem | permanent cost for temporary convenience |
| Widening scope because it was "nearby" | unreviewable change; unrelated breakage |
