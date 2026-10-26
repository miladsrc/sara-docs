# Workflow — Bugfix

For behaviour that is wrong relative to intent. Gates are defined in
[../architecture/OPERATING-MODEL.md](../architecture/OPERATING-MODEL.md).

The defining discipline: **reproduce before you change anything.** A fix without
a reproduction is a guess that happened to compile.

---

## Stages

### 1. Symptom — G0

- State what is observed versus what was expected, with the exact input.
- Name where it was observed: which command, endpoint, screen, or test.
- One sentence the owner would agree with.

### 2. Reproduce — G1 (mandatory, do not skip)

- Produce the failure on demand: command, minimal input, output.
- If it cannot be reproduced: **stop and say so.** You now have an investigation,
  not a bugfix. Report what you tried; ask for the missing condition.
- Record the reproduction as evidence — it becomes the regression test.

**Gate:** a command whose output is the bug.

### 3. Localize — G1

- Find the failing line by evidence, not by plausibility: add output, read the
  stack trace, check the actual value.
- Distinguish the **root cause** from the **surfacing point**. The place the error
  appears is usually not where it started.
- Check whether the same defect exists elsewhere (grep the pattern). Report
  siblings; fix only what the scope covers.

**Gate:** the specific line/condition responsible, with evidence.

### 4. Hypothesize

Write the claim before testing it:

> "The failure occurs because `<X>`, which would be proven by `<observation>`."

Then make the observation. If the hypothesis was wrong, discard it publicly and
form another — do not retro-fit the original explanation.

### 5. Fix — G4

- Smallest change that addresses the root cause.
- Do **not** fix the symptom at the call site if the defect is in the callee.
- Do not bundle unrelated cleanups.
- Add the regression test **from the reproduction** and confirm it fails before
  the fix, passes after. A test written after the fix that was never seen failing
  proves less than it appears to.

### 6. Verify — G5

- Regression test: red before, green after (state which you actually observed).
- Full relevant suite: green, with the command and output.
- Re-run the original reproduction from stage 2 verbatim.

### 7. Record

- Root cause in one paragraph and the fix in one line, in the daily record.
- If the bug revealed a gap in tests, convention, or a doc, record that as an open
  question rather than silently improving it.

## Definition of done

- [ ] reproduction command, recorded before the fix
- [ ] root cause identified with evidence, not assumption
- [ ] regression test added and observed failing pre-fix
- [ ] full suite run, output recorded
- [ ] original reproduction re-run and now correct
- [ ] no unrelated changes in the diff

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| "Fixed" without reproduction | cannot distinguish the fix from coincidence |
| Defensive null-check at the symptom site | hides the defect, preserves the cause |
| Asserting the cause from the error message alone | error text is generated where it is reported, not where it originated |
| Skipping the suite because the change is small | the small changes are the ones that break neighbours |
| Adding a test after the fix and never seeing it fail | it may not test the thing you think |
