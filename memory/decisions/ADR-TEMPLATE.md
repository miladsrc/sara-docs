# ADR-NNN — <short title, imperative>

**Status:** proposed | accepted | superseded by ADR-NNN | rejected
**Date:** YYYY-MM-DD
**Owner:** m.barani
**Supersedes:** — / ADR-NNN

## Context

What situation forces a decision. Verified facts only, each with its evidence
(path, command output, or measurement). State the constraint, not the conclusion.

## Decision

The decision, in one sentence, then the specifics.

## Rejected alternatives

For each: what it was, and the concrete reason it lost. "More complex" is not a
reason unless the complexity is named.

## Consequences

- **Behavior change:** what users/agents will observe differently.
- **Cost:** new mechanisms, dependencies, or maintenance burden — say zero
  explicitly if zero.
- **Unchanged:** what deliberately stays the same.
- **Reversibility:** cost of undoing this later.

## Verification

How compliance is proven, as a checklist an agent can run. Prefer
`python scripts/validate_docs.py` and observable command output over prose.

## Evidence

- FACT: …
- MEASURED: …
- ASSUMPTION: … (with impact if wrong)
