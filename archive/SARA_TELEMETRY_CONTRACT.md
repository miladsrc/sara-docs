# SARA Telemetry Contract

Producer: `~/.config/opencode/plugin/sara.js` (opencode plugin, `tool.execute.*` hooks).
Interface: this document. Consumer: evaluation (`/sara-eval`, golden-task runs).

This is an interface description only. It does not duplicate plugin implementation
logic; the plugin remains the single producer.

## State location

Default: `~/.config/opencode/state/tool-events.ndjson`
Override: env `SARA_STATE_DIR` (points at a directory containing `tool-events.ndjson`).

## Record shape (one JSON object per line, NDJSON)

| Field       | Type    | Meaning                                             |
| ----------- | ------- | --------------------------------------------------- |
| `ts`        | string  | ISO-8601 timestamp of `tool.execute.after`          |
| `tool`      | string  | tool name (read, grep, bash, ...)                   |
| `sessionID` | string  | opencode session id                                 |
| `callID`    | string  | per-call id used to pair before/after               |
| `elapsedMs` | number  | latency of the call (ms); absent if no matching start |
| `outputLen` | number  | length of tool output (chars); absent if no string  |
| `title`     | string  | output title (truncated 120); absent if none        |
| `args`      | object  | summarized args: selected scalar fields + `fieldCount` |

`args` keeps only a fixed allowlist of scalar fields (`filePath`, `path`,
`pattern`, `include`, `query`, `tool`, `command`, `input`); values are
truncated to 160 chars. `args.fieldCount` = total arg keys (never full payloads).

## Truncation behavior

- args strings > 160 chars: truncated to 160 + `…`.
- title > 120 chars: truncated.
- output payloads are NOT stored — only `outputLen`.

## Reliability / compatibility

- Telemetry is **best-effort**: any write failure is swallowed so the session
  never breaks (a malformed state path or locked file cannot crash a tool call).
- The plugin reads `SARA_STATE_DIR`/`homedir()` at call time, so tests can point
  it at a temp dir.
- No PII beyond tool intent is captured. No secrets are recorded (args are the
  allowlist only).
- Schema is append-only NDJSON; new fields may be added, existing fields are
  not removed, so consumers remain compatible.

## Consumers

`/sara-eval` reads this file for per-call measurements (tool count, latency,
redundancy). Treat the file as evidence, not a score.
