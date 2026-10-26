# Evaluation results

One file per run: `YYYY-MM-DD-<task-id>.md`. Never edit a past result to improve
it — a correction is a new file that supersedes the old one.

## Template

```markdown
# <G-id> — <task name>

**Date:** YYYY-MM-DD · **Model:** <provider/model> · **Run:** live | sandbox
**Runtime:** opencode <version> · **Host:** <user>@<machine>

## Decision block (emitted before implementation)

- Task Class: … | AI Needed: … | Agent Needed: …
- Complexity: … | Review Tier: …
- Reason: one line
- Evidence: n/a (decision stage)

## Metrics

| Metric | Value | Evidence label |
|---|---|---|
| tool calls | … | MEASURED / OBSERVED |
| iterations / repairs | … | |
| files created | … | |
| LOC added / removed | … | |
| dependencies added | … | |
| correctness | … | |

## Conclusion

What was done, and what it establishes. One paragraph.

## Limitations

What this run does **not** prove. Required — a result with no stated limits is
overclaimed by default.
```

## Rules

- **No fabricated numbers.** A number you did not measure is labelled OBSERVED at
  best, or omitted.
- **Limitations are mandatory.** If the telemetry file did not exist, say the
  counts are observed from the transcript.
- **Compare like with like.** A result from a different host or runtime version is
  not a baseline for this one; state the difference.

## Existing records

- [2026-10-26-G1.md](2026-10-26-G1.md) — first record produced on this host;
  AFTER-only, no baseline, so it proves behaviour, not improvement.

The only historical record is
`archive/SARA-GOLDEN-RESULTS.md` (G5), produced on a different machine and runtime
(host `98903`, opencode 1.18.25) — it is context, not a current baseline.
