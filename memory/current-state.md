# Current state

Verified: 2026-10-26 · host `m.barani` · opencode `v2.1.4`

## Active work

The restructure is **complete and green**: validated structure, 8 SDLC playbooks,
agent contracts, evaluation loop, and the live pointer applied with owner
approval. Old reports are frozen in `archive/`.

**2026-10-26:** the Ponytail integration was upgraded to upstream **v5.3.2**
(`16352ac2`) through the owners that exist on this host — two new skills
(`sara-review`, `sara-debt`) plus an always-on policy section in `AGENTS.md`.
Decision: [decisions/ADR-002-ponytail-v5-integration.md](decisions/ADR-002-ponytail-v5-integration.md);
evidence: [daily/2026-10-26.md](daily/2026-10-26.md).

Open: the owner's restart into a fresh session; nine golden probes still unrun
(G1 now has an AFTER-only record); OQ-001…OQ-006 awaiting owner decisions.


## Verified facts about the environment

Each line below was checked by command during the 2026-10-25 session. **FACT**
unless marked otherwise.

### Live runtime surface

Path: `C:\Users\m.barani\.config\opencode` — exists.

| Element | Verified state |
|---|---|
| git tracking | **not a git repository** (no history, no rollback) |
| `opencode.jsonc` | 5 lines: `$schema`, `default_agent: sara`, `instructions: [AGENTS.md]` |
| `AGENTS.md` | 109 lines / 5536 B; carries the Sara-v2 bridge, the sara-docs pointer, the smallest-complete-change policy, and the repo/CI fact |
| `agent/` | 14 files: `sara`, `hmyar` (both primary) + 12 subagents |
| subagents | `orchestrator`, `router`, `planner`, `discovery`, `coding`, `database`, `testing`, `security`, `review`, `research`, `evaluation`, `recovery` |
| `skills/` | 11 skills — `read-terminals`, `sara-review`, `sara-debt` plus `backend-dev`, `ci-cd`, `docker-stack-op`, `frontend-dev`, `git-hygiene`, `report-builder`, `test-verify`, `ui-ux` |
| `plugins/` | 1 file — `plugins/postman.ts`; plus a `postman-plugin/` directory |
| `memory/` | 13 agent memory files (all agents except `hmyar`) |
| `command/` | **absent** — no slash-command gates exist |
| `state/` | **absent** — no telemetry is being recorded |
| `test/` | **absent** — no plugin test suite exists |
| `tui.json` | **absent**; `cli.json` and `service.json` exist instead |

### Sara v2 governed runtime

- Path `C:\Users\m.barani\IdeaProjects\sara` exists.
- Port `8800` is **closed** → the v2 Gateway is down. Per the bridge rule,
  Level 1+ actions run directly and must disclose the bypass.
  **OBSERVED** (single port probe, not a startup attempt).

### Other verified facts

- **FACT**: this repo's git tip before this work was `2c6b77a` (6 commits,
  clean tree).
- **FACT**: four evaluator working directories exist under the live config
  (`challenge-eval-2026-09-21`, `dotin-10day-evaluator-2026`,
  `dotin-exam-02-evaluator-2026`, `dotin-combined-03-04-evaluator-2026`). Their
  contents were not inspected in this session.
- **FACT**: `C:\Users\m.barani\IdeaProjects\hmyar` implements the mature pattern
  this repository now adopts (memory/, workflows/, backlog/, validating scripts,
  CI). It is the reference implementation for this structure.
- **FACT**: host user is `m.barani`; user profile `98903` does not exist on this
  machine.
- **OBSERVED (mid-session drift)**: the skill set grew from 1 to 9 while this
  session was running — 8 domain skills (`backend-dev`, `ci-cd`,
  `docker-stack-op`, `frontend-dev`, `git-hygiene`, `report-builder`,
  `test-verify`, `ui-ux`) appeared between the first inventory check and the
  pointer edit. Cause not investigated; either the owner or another session added
  them. **Lesson for the rule set:** a single inventory at session start is not
  enough — re-verify the live surface before reporting facts about it.
- **FACT**: live `AGENTS.md` now carries the sara-docs operating-manual pointer
  (applied 2026-10-25 with owner approval; backup `AGENTS.md.bak-2026-10-25`,
  original 2883 bytes preserved, +816 bytes appended).

## Corrections to previously documented claims

The frozen docs in `archive/` assert the following. They were written on a
different machine and are **not true here**. This table is the single owner of
those corrections.

| Archived claim | Verified reality (2026-10-25) |
|---|---|
| Host user `98903`, opencode `1.18.25` | user `m.barani`, opencode `v2.1.4` |
| Live config is git repo `82c89c4` (DECISION 001) | not a git repository at all — that guarantee is unenforced |
| `command/` holds `/sara-decide`, `/sara-review`, `/sara-audit`, `/sara-eval` | no `command/` directory exists |
| `plugin/sara.js` + `test/` with 4/4 passing tests | neither exists; only `plugins/postman.ts` |
| 3 skills: read-terminals, sara-review, sara-debt | 9 skills on 2026-10-25 (none of the three named beyond `read-terminals`). **2026-10-26:** `sara-review` and `sara-debt` now exist — added deliberately, in a different form, and recorded in ADR-002; the archive claim was still false when it was read |
| Agents `architect`, `reviewer`, `auditor` | absent; the 14 agents listed above exist instead |
| AGENTS.md is 117 lines after cleanup | 55 lines on 2026-10-25; 105 lines after the 2026-10-26 policy addition, 109 after the same-day config sync |
| Telemetry recorded to `state/tool-events.ndjson` | no `state/` directory; nothing records |
| Golden evaluation is an active loop | one G5 result exists, from another host; not re-run here |

## Blockers

None blocking this build. See
[../backlog/open-questions.md](../backlog/open-questions.md) for open questions
that need owner decisions (live git tracking, telemetry, command gates, the
`hmyar` memory file gap, and where the Hamtayar plan belongs).

## Proposed next step

1. ~~Owner review of the live-pointer edit~~ — **approved and applied** 2026-10-25;
   revert is deletion of the appended block or restore of
   `AGENTS.md.bak-2026-10-25`. Effect begins at the next opencode restart.
2. **Restart opencode** to load the 2026-10-26 policy and the two new skills in a
   fresh interactive session. Rollback hashes are in [daily/2026-10-26.md](daily/2026-10-26.md).
3. Decide open questions OQ-001 through OQ-006.
4. Run the remaining golden probes. G1 has an AFTER-only record here
   ([../evaluation/results/2026-10-26-G1.md](../evaluation/results/2026-10-26-G1.md));
   G5 exists only from another host ([../evaluation/results/2026-10-25-G5.md](../evaluation/results/2026-10-25-G5.md));
   G2–G4 and G6–G10 are unrun (8 of 10). With no acceptance threshold (OQ-006),
   none of this supports an improvement claim.
5. Re-run the live-surface inventory before reporting environment facts — it
   changed from 9 to 11 skills inside the 2026-10-26 session.
