# Golden tasks

Frozen probe set for comparing Sara before and after a change. Owner of the
**task definitions**; [results/](results/) owns the records.

Rules that keep this honest:

- No task is tuned to make Sara look good.
- No expected output is hard-coded.
- No task is narrowed to what Sara happens to be good at.
- A run that was not performed is recorded as not performed.

---

## Why these ten

Each probes a distinct failure mode, not just "can it code". Four of them test
whether Sara **declines** the elaborate answer — that is the capability most often
missing in agent systems.

| # | Class | Task | What it actually probes |
|---|---|---|---|
| G1 | trivial coding | `is_palindrome(s)` plus a 3-line test. No deps, no classes, no abstraction. | Baseline correctness without over-engineering |
| G2 | existing-code reuse | Add a `--verbose` flag to an existing CLI, reusing its arg parsing. | Reading before writing; not adding a library |
| G3 | over-engineering temptation | Count word frequencies in a file, top 10. Stdlib only. | Resistance to inventing architecture |
| G4 | architecture choice | Tiny in-memory KV store with JSON dump. State the decision first. | Explicit decision before code |
| G5 | AI-vs-non-AI | Do two CSVs have identical rows, order-insensitive? | Recognizing a deterministic problem |
| G6 | agent-vs-workflow | Move `*.py` to `src/`, `*.md` to `docs/`. | Recognizing a script beats an agent |
| G7 | single-vs-multi-agent | Extract 5 acceptance criteria from spec text. | Recognizing delegation is overhead |
| G8 | RAG-vs-no-RAG | Summarize one 2000-line file. | Not standing up retrieval for one document |
| G9 | debugging | Insert a list-index bug in a scratch script; find and fix with before/after evidence. | Reproduction-first discipline |
| G10 | repository modification | Refactor a duplicated 20-line block into one helper; behaviour identical. | Behaviour preservation |

## Procedure

1. Create a scratch sandbox outside any real project.
2. Emit the decision block **before** implementing:
   `Task Class / AI Needed / Agent Needed / Complexity / Review Tier`.
3. Do the work.
4. Capture the evidence below.
5. Write the result to [results/](results/) using the template there.
6. Delete the sandbox.

## Per-task evidence

| Field | How to obtain |
|---|---|
| Decision block | stated by Sara before implementation |
| Tool calls | telemetry when available; otherwise OBSERVED transcript count |
| Iterations / repair rounds | counted |
| Files created / changed | `git status` or directory listing |
| LOC added / removed | `git diff --stat`, else line count |
| Dependencies added | manifest diff |
| Correctness | the exact command run and its result |
| Failure class | from the taxonomy below, when it failed |

## Failure taxonomy

`requirement-misunderstanding` · `planning` · `architecture` · `model` · `tool` ·
`context` · `orchestration` · `subagent` · `verification` · `evaluation`

## Evidence labels

MEASURED (a number from a real run), OBSERVED (seen in the session), INFERRED
(derived), NOT-MEASURED (explicitly absent). Never fabricate a number.

## Pass bar

**OPEN — OQ-006.** Until the owner defines a threshold, results are descriptive
and must not be used to claim improvement. A comparison against a recorded prior
run is the minimum bar; an absolute threshold is stronger.
