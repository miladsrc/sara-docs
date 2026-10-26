# Workflow — Refactor

Changing structure without changing behaviour. Gates are defined in
[../architecture/OPERATING-MODEL.md](../architecture/OPERATING-MODEL.md).

The invariant is the point: **behaviour must be identical, and that must be
provable by tests that were green before and after.**

---

## Stages

### 1. Justify

A refactor needs a reason stronger than preference. Acceptable:

- a specific defect class the current structure invites
- duplicated logic with evidence of divergence risk
- a change the current structure makes hazardous (the next feature cannot land
  safely)
- measured cost (performance, build time) with the measurement

Not acceptable: "cleaner", "more idiomatic", "modern", "feels better". If the
reason is taste, it is a proposal to the owner, not a task.

### 2. Establish the safety net — G1

- Identify the tests that cover the target code. Run them. Record the result.
- **If coverage is inadequate, write characterization tests first**, capturing
  current behaviour — including behaviour that looks wrong. A refactor preserves
  what the code does, not what it should do.
- No net, no refactor. Structural change under weak tests is a rewrite with
  unknown consequences.

**Gate:** green suite covering the target, or characterization tests added.

### 3. Bound the change

- Name the exact symbols/files in scope. Everything else is out of scope.
- Pick one mechanical transformation. Multi-pattern refactors are unreviewable.
- State what must **not** change: public signatures, wire formats, schema,
  ordering, error messages that clients match on.

### 4. Transform in steps

- Each step compiles and passes the suite on its own.
- Commit-sized steps; no step mixes behaviour with structure.
- If a step requires a behaviour change to proceed, you have left refactoring.
  Stop, and report the choice: refactor first, then a separate feature change.

### 5. Verify — G5

- Suite green, command and output recorded.
- Diff review: confirm nothing but structure moved. Look specifically at
  conditionals, default values, error paths, and ordering.
- For anything perf-sensitive, measure before and after. An unmeasured "faster"
  is a claim, not a fact.

### 6. Review — G6

Tier 2+ always: a refactor is judged by whether behaviour is preserved, which the
author is the worst person to confirm.

## Definition of done

- [ ] reason stated and stronger than preference
- [ ] test coverage established before touching code
- [ ] one transformation pattern, bounded scope
- [ ] suite green before and after, both recorded
- [ ] public surface unchanged (or the change is explicit and reviewed)
- [ ] independent review of the structural diff
- [ ] no unrelated files touched (formatting noise included)

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| Refactor + feature in one change | impossible to tell which broke behaviour |
| "Tests are green" after silently updating test expectations | the net was rewritten to fit the fall |
| Reformatting files you happened to open | obscures the real diff; review cost without benefit |
| Refactoring toward an architecture nobody approved | redesign by increment, no decision on record |
| Characterizing behaviour as "obviously a bug, I fixed it" | that is a behaviour change; it needs its own workflow |
