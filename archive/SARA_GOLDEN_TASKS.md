# SARA GOLDEN TASKS — ROUND 2

Version: 2026-08-30
Purpose: small, honest probe set to compare Sara before/after an upgrade.
Rules: no optimizing tasks to make Sara look good, no hard-coded expected
outputs, no narrowing what Sara attempts. Results go to `SARA-GOLDEN-RESULTS.md`.

Run at least one task from each class when evaluating. Trivial to run anywhere:
create the task files, do the work, then capture evidence and delete the sandbox.

## Task list

| # | Class | Task |
|---|-------|------|
| G1 | trivial coding | Write a function `is_palindrome(s)` with a 3-line test. Add no deps, no classes, no abstractions. |
| G2 | existing-code reuse | In any small existing repo, "add a `--verbose` flag to the existing CLI" — reuse existing arg parsing; do not add a new library. |
| G3 | over-engineering temptation | Implement "count word frequencies in a file, top 10". Singleensity: use stdlib; no DB, no OOP hierarchy. |
| G4 | architecture choice | Design and implement "a tiny in-memory key/value store with a JSON dump". State the architecture decision first. |
| G5 | AI-vs-non-AI | "Determine if two CSV files have identical rows (order-insensitive)." Decide: is AI needed? (No.) Do the deterministic thing. |
| G6 | agent-vs-workflow | "Restructure this folder: move *.py into src/ and *.md into docs/." Decide: workflow ok, no agent needed. |
| G7 | single-vs-multi-agent | "Given a spec text, extract 5 acceptance criteria into a markdown list." Decide: is a subagent needed? (No.) |
| G8 | RAG-vs-no-RAG | "Summarize the key points in this single 2000-line file." Decide: retrieval vs single pass. No RAG infra. |
| G9 | debugging | In a scratch script, introduce a "list index error" bug; find and fix it with evidence (before/after output). |
| G10 | repository modification | In a scratch module, refactor a duplicated 20-line block into one helper; keep behavior identical (tests). |

## Per-task capture (evidence only — do not invent)

- Task Class / AI Needed / Agent Needed / Complexity / Review Tier (the decision block, one line each)
- tool calls (count via `~/.config/opencode/state/tool-events.ndjson` filtered to the task window)
- iterations / repair rounds
- files created / changed
- LOC added / removed (`git diff --stat` if a git repo, else `wc -l`)
- dependencies added (manifest diff)
- correctness check (what exactly was run / asserted and the result)
- failure classification if failed (see taxonomy)

## Failure taxonomy

requirement-misunderstanding | planning | architecture | model | tool |
context | orchestration | subagent | verification | evaluation