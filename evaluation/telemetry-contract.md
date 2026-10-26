# Telemetry contract

Verified: 2026-10-25

The interface between **producers** (runtime hooks that observe what Sara does)
and **consumers** (evaluation, cost review, audit).

**Status: SPECIFIED BUT NOT IMPLEMENTED.** Verified 2026-10-25: no `state/`
directory and no producing plugin exist on this host. Every evaluation run today
must therefore label tool-call counts OBSERVED, not MEASURED. Tracked as OQ-002.

---

## Event shape

One JSON object per line (NDJSON), append-only, one file per day:

```
<config>/state/tool-events.ndjson
```

```json
{
  "ts": "2026-10-25T09:14:03.120Z",
  "session": "ses_abc123",
  "task": "G5",
  "event": "tool.execute.after",
  "tool": "bash",
  "args_digest": "sha256:1f2e...",
  "duration_ms": 412,
  "outcome": "ok"
}
```

| Field | Required | Notes |
|---|---|---|
| `ts` | yes | ISO-8601 UTC, millisecond precision |
| `session` | yes | opencode session id — the join key |
| `task` | no | evaluation task tag (G1…G10) when the run is a probe |
| `event` | yes | `tool.execute.before` · `tool.execute.after` · `agent.start` · `agent.end` |
| `tool` | after | tool name |
| `args_digest` | after | hash only — **never raw arguments** |
| `duration_ms` | after | measured wall time |
| `outcome` | after | `ok` · `error` · `denied` |

## Producer obligations

1. **Never record content.** No file contents, no prompt text, no command output,
   no arguments in clear. Hashes and counts only. The telemetry file must be safe
   to read aloud.
2. **Never record secrets.** If an argument could carry one, it is digested, not
   logged.
3. **Append only.** No rewriting or truncating; a corrupt line is skipped by the
   consumer, not repaired in place.
4. **Never block the tool call.** A telemetry failure is logged to stderr and
   swallowed. Observability must not break the thing it observes.
5. **One line per event**, written after the operation completes.

## Consumer obligations

1. Treat a missing field as absent, never as zero.
2. A gap in the file is a fact about the producer, not about the run — say so
   rather than inferring "no calls happened".
3. Correlate by `session` + `task` window; never by wall-clock guesswork.
4. Report counts as MEASURED only when read from this file.

## What this enables

| Question | Computed from |
|---|---|
| How many tool calls did this task cost? | count by `session` + `task` |
| Which tools dominate? | group by `tool` |
| How often are actions denied? | `outcome = denied` |
| Is a task class getting cheaper over time? | calls per successful task, across runs |
| Where does time go? | sum `duration_ms` by `tool` |

## Out of scope

Cost in currency, token accounting, and model routing decisions. Those need
provider-level data this contract does not capture. Adding them is a new ADR, not
an extension here.
