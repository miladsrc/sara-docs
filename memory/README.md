# Memory index

Durable, reviewed knowledge about Sara's operating state. Session transcripts are
temporary; only what is written here and committed is durable.

## Files

- [current-state.md](current-state.md) — verified live state, active work,
  recent changes, blockers, proposed next step. Start every session here.
- `decisions/` — one ADR per non-trivial decision. Append-only; never rewrite
  history, supersede it. Template: [decisions/ADR-TEMPLATE.md](decisions/ADR-TEMPLATE.md).
- `daily/YYYY-MM-DD.md` — dated session records: what changed, what was verified,
  what stayed open.
- [lessons-learned.md](lessons-learned.md) — reusable lessons that should change
  future behavior. Not a changelog.

## What belongs here vs. elsewhere

| Content | Home |
|---|---|
| How Sara works, what is verified about her environment | this directory |
| How a kind of task is performed | [../workflows/](../workflows/) |
| Who does what, and what they return | [../roster/](../roster/) |
| Whether output was good | [../evaluation/](../evaluation/) |
| What is unknown, unapproved, or blocked | [../backlog/open-questions.md](../backlog/open-questions.md) |
| History of what was believed at a point in time | [../archive/](../archive/) |

## Conventions

- Label statements FACT / MEASURED / OBSERVED / INFERRED / ASSUMPTION / PROPOSAL /
  OPEN QUESTION — see [../AGENTS.md](../AGENTS.md).
- Never promote a guess into a fact.
- Keep files small and cross-linked; one owner per concept.
