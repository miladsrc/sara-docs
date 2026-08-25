#!/usr/bin/env python
"""Read-only viewer for other opencode sessions (shared opencode.db).

Usage:
  python read_terminals.py list [MINUTES]        # active sessions, default 30 min window
  python read_terminals.py show <session_id> [N] # last N messages of a session (default 6)
  python read_terminals.py todos <session_id>    # todo progress of a session

STRICTLY READ-ONLY: connects with mode=ro; only SELECT/PRAGMA issued.
"""
import json
import sqlite3
import sys
import time

DB = r"file:C:/Users/m.barani/.local/share/opencode/opencode.db?mode=ro"


def connect():
    return sqlite3.connect(DB, uri=True)


def cmd_list(minutes=30):
    c = connect()
    now = int(time.time() * 1000)
    cutoff = now - minutes * 60 * 1000
    rows = c.execute(
        "SELECT id, title, directory, time_updated "
        "FROM session WHERE time_updated > ? AND time_archived IS NULL "
        "ORDER BY time_updated DESC LIMIT 20",
        (cutoff,),
    ).fetchall()
    if not rows:
        print(f"No sessions active in the last {minutes} min.")
        return
    for sid, title, directory, updated in rows:
        age = (now - updated) / 60000.0
        print(f"{sid} | {age:6.1f} min ago | {title}")
        print(f"{'':38}| dir: {directory}")


def _print_messages(session_id, limit):
    c = connect()
    q = (
        "SELECT m.data, p.data FROM message m "
        "LEFT JOIN part p ON p.message_id = m.id "
        "AND json_extract(p.data,'$.type')='text' "
        "WHERE m.session_id = ? ORDER BY m.id DESC LIMIT ?"
    )
    for mdata, pdata in c.execute(q, (session_id, limit)).fetchall():
        role = json.loads(mdata).get("role", "?")
        txt = json.loads(pdata).get("text", "") if pdata else ""
        print(f"--- {role} ---")
        print(txt[:600].replace("\n", " "))
        print()


def cmd_show(session_id, limit=6):
    _print_messages(session_id, limit)


def cmd_todos(session_id):
    c = connect()
    row = c.execute("SELECT data FROM todo WHERE session_id = ?", (session_id,)).fetchone()
    if not row:
        print("No todos recorded for this session.")
        return
    for t in json.loads(row[0]):
        print(f"[{t.get('status', '?'):>10}] {t.get('content', '')}")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    cmd, rest = args[0], args[1:]
    if cmd == "list":
        cmd_list(float(rest[0]) if rest else 30)
    elif cmd == "show":
        cmd_show(rest[0], int(rest[1]) if len(rest) > 1 else 6)
    elif cmd == "todos":
        cmd_todos(rest[0])
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
