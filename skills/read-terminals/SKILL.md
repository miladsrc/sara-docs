---
name: read-terminals
description: Show live progress of other opencode terminals/sessions by querying the shared opencode SQLite database. Use when the user asks "what are the other terminals doing", "see other terminal progress", "read other sessions", or wants to know what another opencode instance is working on right now.
---

# Read other opencode terminals

All opencode sessions on this machine share one SQLite database:
`C:/Users/m.barani/.local/share/opencode/opencode.db` (WAL mode).

**Read-only rule:** run ONLY `SELECT` / `PRAGMA` statements against this DB. Never
INSERT/UPDATE/DELETE/ATTACH. Open with a read-only URI if convenient
(`file:...?mode=ro`), and always copy the DB or use `mode=ro` to avoid lock contention.

Use the helper script that ships with this skill (same folder as this file):

```
python "<skill-dir>/read_terminals.py" list [MINUTES]         # active sessions (default: last 30 min)
python "<skill-dir>/read_terminals.py" show <session_id> [N] # last N messages of a session (default 6)
python "<skill-dir>/read_terminals.py" todos <session_id>    # todo progress of a session
```

The script connects read-only (`mode=ro`) and issues only SELECTs — never edit the DB.

Timestamps are epoch milliseconds internally. Report each session's title,
working directory, and minutes since last activity.

## Notes

- Exclude THIS session from results (match its own session id/title) so you
  report only *other* terminals.
- If no sessions appear, widen the cutoff window before concluding "nothing running".
- This only covers opencode sessions — plain cmd/PowerShell windows are invisible.
