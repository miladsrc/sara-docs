# Operating model

Verified: 2026-10-25

The single owner of **task classification, complexity, review tier, and gate
definitions**. Workflows reference these; they never restate them.

Purpose: make the depth of process proportional to the risk, and make "done"
falsifiable.

---

## 1. Classify before acting

Every non-trivial request is classified before the first tool call. The
classification is stated in one line:

```
Task Class: CODE | Complexity: L2 | Review: 2 | Workflow: workflows/feature.md
```

| Class | Meaning | Typical first agent |
|---|---|---|
| `QUESTION` | Answer from known context; nothing changes | none — answer directly |
| `ANALYSIS` | Read-only investigation producing a finding | `discovery` |
| `CODE` | Change application source or tests | `coding` |
| `DB` | Schema, migration, data repair | `database` |
| `CONFIG` | Runtime/config files, CI, tooling | `coding` |
| `DOCS` | Knowledge base, specs, reports | none — write directly |
| `SECURITY` | Authz/authn, secrets, permissions, threat review | `security` |
| `RESEARCH` | External facts needed before a decision | `research` |
| `EVAL` | Score output against criteria | `evaluation` |

## 2. Complexity

| Level | Definition | Who acts | Evidence required |
|---|---|---|---|
| **L0** | Read-only, reversible, no side effects | Sara directly | the finding itself |
| **L1** | Single file, obvious change, trivially reversible | Sara directly | diff + what was run |
| **L2** | Multi-file or single-concern change; tests exist | one specialist agent | diff + test output |
| **L3** | Cross-cutting, schema/contract impact, or hard to undo | plan + specialist + independent review | plan, diff, tests, review verdict |
| **L4** | Destructive, irreversible, credential-touching, or affects Sara's own runtime | **owner approval required before execution** | proposal, approval record, verification |

**Escalate on doubt.** Being wrong upward costs a message; being wrong downward
costs a rollback or a data loss.

## 3. Review tiers

| Tier | When | Reviewer |
|---|---|---|
| **0** | L0/L1 work, docs, local scratch | none — self-check |
| **1** | L1/L2 code with existing passing tests | author self-review against the checklist |
| **2** | L2/L3: production paths, shared modules | independent `review` agent (fresh eyes, no author context) |
| **3** | L3/L4: security, schema, money, auth, irreversible ops | `review` **and** `security`, plus human sign-off |

Independence is the point of tier 2+. The author may not be the reviewer.

## 4. Gates

Referenced by name from workflows. A gate that is not evidenced did not happen.

| Gate | Question | Evidence |
|---|---|---|
| **G0 Requirement** | Is the goal unambiguous and are its edges stated? | restated goal + explicit non-goals |
| **G1 Grounding** | Do we know the real current state of the code/config? | file paths, line refs, command output |
| **G2 Plan** | Is there an ordered plan with failure points? | plan with steps, risks, rollback |
| **G3 Approval** | Has the owner authorized this, if L4? | explicit approval, quoted |
| **G4 Implementation** | Does the change do exactly what was planned? | diff |
| **G5 Verification** | Was it actually run, and did it pass? | command + output, tests |
| **G6 Review** | Did someone other than the author accept it? | review verdict |
| **G7 Record** | Can the next session reconstruct what happened? | state, daily record, ADR if needed |

Skipping a gate is allowed only when it is named as skipped, with a reason, in the
session record. Silent skipping is a defect.

## 5. Decision ladder

Try the cheapest sufficient rung; climb only when it fails.

1. **Answer** — is this already known? (docs, code, prior decision)
2. **Direct action** — one obvious change; no plan needed
3. **Deterministic tool** — a command, script, or query beats prose and beats AI
4. **Single agent** — one specialist, clear contract
5. **Multi-agent** — parallel independent work, or a review of the work
6. **Human** — irreversible, ambiguous, or values-laden

Two standing heuristics:

- **Is AI needed?** No, when the operation is deterministic (compare, count,
  move, rename, sort). AI adds variance to work that has none.
- **Is an agent needed?** No, when the task is a single step with a known answer.
  A subagent costs latency and context; it buys independence and parallelism.

## 6. Stop rules

Stop and escalate instead of improvising when:

- a required fact cannot be verified (say so; do not guess)
- two docs, or a doc and the code, contradict each other (report both)
- the requested change reaches into a path outside the declared scope
- verification is impossible in this environment
- the action is L4 and approval is not on record

## 7. Evidence labels

Defined in [../AGENTS.md](../AGENTS.md) — FACT / MEASURED / OBSERVED / INFERRED /
ASSUMPTION / PROPOSAL / OPEN QUESTION. This model depends on them: an L3 claim
supported by an INFERRED label is not verified, it is assumed.
