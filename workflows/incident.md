# Workflow — Incident

For something broken now: a failed deploy, a dead service, corrupted data, a
security event. Gates are defined in
[../architecture/OPERATING-MODEL.md](../architecture/OPERATING-MODEL.md).

Order matters and is counter-intuitive: **stop the damage before understanding it.**
Diagnosis is stage 2. A root cause found after irreversible damage is a worse
outcome than a service restarted without explanation.

---

## Stages

### 1. Stabilize — before anything else

- Is the damage still accumulating? Stop it: roll back, disable the feature,
  route around it, stop the writer.
- Preserve evidence **before** restarting or deleting anything: copy the log, dump
  the failing rows, save the config in force.
- State the blast radius as observed: what is broken, for whom, since when.

Any stabilization step that is destructive is L4: propose it, get approval, unless
the alternative is ongoing data loss — in which case act and disclose immediately.

**Gate:** damage stopped or bounded; evidence preserved.

### 2. Establish the timeline

Reconstruct from evidence, not memory: last known good point, first failed
observation, what changed in between (deploy, config, migration, traffic, external
dependency). Timestamps from logs, not from recall.

The single most useful question: **what changed immediately before?**

### 3. Diagnose

- Read the actual error, in full, including the part that scrolls past.
- Form one hypothesis, test it. Repeat. Keep the ones you eliminated.
- Distinguish the triggering change from the latent defect it exposed — most
  incidents are a small trigger hitting a pre-existing weakness.

Dispatch [`recovery`](../roster/README.md) when the failure class is unclear
(transient vs. permanent vs. data corruption vs. resource exhaustion).

**Gate:** a stated cause, with the evidence that distinguishes it from the
alternatives considered.

### 4. Restore

- Prefer the smallest, most reversible restoration: rollback over hotfix, config
  revert over code change, restart over redeploy.
- Verify restoration against the original symptom, not against "it looks fine".
- If a hotfix is unavoidable, it goes through [bugfix.md](bugfix.md) and gets its
  real fix later, tracked.

**Gate:** original symptom re-tested and absent.

### 5. Harden

- Fix the latent defect, not just the trigger.
- Add the detection that would have caught it sooner: which signal, at what
  threshold, alerting whom.
- Add the guard that prevents recurrence: test, constraint, permission, limit.

### 6. Record — mandatory

Write it the same day, while the evidence still exists:

- timeline with timestamps
- cause (stated plainly, without blame language)
- what was done, in order
- what made it worse or wasted time
- what is now different
- follow-up items with owners

## Definition of done

- [ ] damage stopped; evidence preserved before recovery
- [ ] timeline reconstructed from logs
- [ ] cause stated with distinguishing evidence
- [ ] original symptom re-tested after restoration
- [ ] latent defect fixed, not only the trigger
- [ ] detection added for earlier warning
- [ ] written record with follow-ups and owners

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| Diagnosing while data keeps corrupting | the cause becomes secondary to the loss |
| Restarting before capturing logs | destroys the only evidence of the cause |
| Rolling forward a hotfix under pressure | compounding an unverified change onto a broken system |
| Stopping at "it works now" | the latent defect fires again with a different trigger |
| Blameless treated as evidence-free | no blame is not the same as no analysis |
