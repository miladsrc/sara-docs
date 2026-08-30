# SARA ARCHITECTURE CLEANUP REPORT

Date: 2026-08-30
Type: READ-ONLY architecture inventory and diagnosis — nothing was modified, moved, renamed, or deleted during this pass.
Runtime under inspection: opencode v1.18.25 (model `opencode/big-pickle`) + `C:\Users\98903\.config\opencode\*` (user `98903` on this host), plus the `sara-docs` repository.
Evidence basis: filesystem inspection of both surfaces; telemetry `state/tool-events.ndjson` for live tool usage; observed session behavior. Prior reports were **not** used as ground truth — only as documents to be cross-checked for drift.

---

# 1. Executive Summary

Sara is not a process. Sara = the opencode runtime + a configuration layer (`~/.config/opencode/`) + a documentation repo (`sara-docs/`). The Round 1→Round 2 upgrade added a plugin, 3 agents, 4 commands, 3 skills, autonomy gates, and 10+ documentation files.

**Is Sara over-engineered?** Not catastrophically — the runtime surface is small (one 52-line plugin, one 110-line policy file, 7 command/agent files, 3 skills). The clutter is concentrated in **four** spots:

1. **Duplicated decision/review doctrine** — the same decision-block schema, task-classification, least-mechanism ladder, and 5-tag complexity taxonomy are copied across `AGENTS.md`, `command/sara-decide.md`, `command/sara-review.md`, `agent/architect.md`, `agent/reviewer.md`, `agent/auditor.md`, and `skills/sara-review/SKILL.md`. Seven files, roughly three source-of-truth candidates.
2. **Overlapping audit/debt tooling** — `agent/auditor.md` (whole-repo, 5-tag + `sara:` debt ledger) and `skills/sara-debt/SKILL.md` (only the `sara:` debt ledger) implement the same concept at different sizes. `sara-debt` is a strict subset of `auditor`.
3. **Broken/vestigial files** — `skills/read-terminals/*` hardcodes the other user's path (`C:/Users/m.barani/...`) and **cannot function on this host** (verified: that path does not exist); `.gitignore` exists with no git repository; `AGENTS.md.bak-20260830` and `opencode.jsonc.bak-20260830` are rollback snapshots that nothing automated consumes.
4. **Documentation sprawl** — 12 top-level documents in `sara-docs` overlap heavily (SYSTEM_MAP vs ARCHITECTURE_AFTER_ROUND2 vs FINAL_REPORT describe the same layers; BASELINE/CANDIDATES/BOUNDARY are one-off snapshots; README duplicates a Task Log). Three "persistence" mechanisms (`SARA-DECISIONS.md`, `SARA-AUDIT.md`, `SARA-DEBT.md`) are defined by commands/skills but have **never written a single file** (verified absent).

The always-loaded policy file (`AGENTS.md`, 7.3 KB) also carries **machine-specific content** referring to user `m.barani` and a v2 Gateway that is not present on this host — real, if small, context bloat and drift.

Round 2 is behaviorally real (plugin fires per tool call; a subagent was used in the controlled test; `sara-review` skill ran). The clean-up is a **consolidation and housekeeping** job, not a rebuild: no capability needs to be invented, and no core mechanism should move.

---

# 2. Current System Map

```
opencode runtime (v1.18.25)                    ← supporting infra, NOT Sara
 ├─ opencode.db (49 MB SQLite + WAL)            ← session/message/todo persistence (runtime)
 ├─ ~/.local/share/opencode/{log,repos,snapshot,tool-output}
 └─ TUI (tui.json: mouse=false)

Sara config layer  C:\Users\98903\.config\opencode\
 ├─ AGENTS.md                      policy + persona + Round-2 operational gates
 ├─ AGENTS.md.bak-20260830         pre-Round-2 snapshot (rollback)
 ├─ opencode.jsonc                 plugin registration + permission(ask) gates
 ├─ opencode.jsonc.bak-20260830    pre-Round-2 snapshot
 ├─ tui.json                       TUI settings
 ├─ package.json / package-lock / node_modules/    plugin project scaffolding (GENERATED)
 ├─ .gitignore                     orphaned (no git repo)
 ├─ plugin/sara.js                 telemetry hook (tool.execute.before/after)
 ├─ test/sara-plugin.test.mjs      plugin tests (node:test, 4 tests)
 ├─ command/  sara-decide · sara-review · sara-audit · sara-eval
 ├─ agent/    architect · reviewer · auditor
 ├─ skills/   sara-review · sara-debt · read-terminals(+read_terminals.py)
 ├─ memory/sara.md                 persistent cross-session log (manual append)
 └─ state/tool-events.ndjson       telemetry stream (GENERATED)

Docs repo  C:\Users\98903\IdeaProjects\sara-docs\  (git, 1 commit daf7c71)
 ├─ README + 11 top-level .md  (Round-2 docs: SYSTEM_MAP, SELF_BOUNDARY, BASELINE,
 │   CANDIDATES, ARCHITECTURE_AFTER_ROUND2, FINAL_REPORT, GOLDEN_TASKS,
 │   GOLDEN-RESULTS, PONYTAIL_SELF_UPGRADE_REPORT, ROUND2_CONTROLLED_TEST_REPORT)
 ├─ PROGRESS-PHASE-2.md        untracked (ai-swe-engine artifact, per owner decision)
 ├─ ponytail/                   vendored third-party git clone (own .git, untracked)
 ├─ java/                       G1 test scaffold (untracked)
 └─ .idea/                       IDE state (untracked)
```

---

# 3. File Inventory

Status legend: ACTIVE / INDIRECTLY USED / LEGACY / UNUSED / GENERATED / TEMPORARY / DUPLICATE / UNKNOWN.
(Usage judgments from config references + live session observation; telemetry only records tool calls, not skill/command evocations, so skill/command status includes inference.)

## 3.1 Config layer — `~/.config/opencode/`

| File/Dir | Layer | Purpose | Used By | Status | Keep/Move/Merge/Delete Candidate |
| -------- | ----- | ------- | ------- | ------ | -------------------------------- |
| `AGENTS.md` (7.3 KB, 110 ln) | Instructions | persona + rules + decision ladder + round-2 operational gates | opencode loads at every session start | ACTIVE | Keep — but strip machine-specific references; move gate doctrine out (see §20) |
| `AGENTS.md.bak-20260830` | Persistence | pre-Round-2 rollback snapshot | rollback only (referenced by memory/sara.md) | LEGACY | Archive (not part of any active config) |
| `opencode.jsonc` | Configuration | plugin registration; permission ask-gates | opencode runtime | ACTIVE | Keep — canonical safety mechanism |
| `opencode.jsonc.bak-20260830` | Persistence | pre-Round-2 snapshot | rollback only | LEGACY | Archive |
| `tui.json` | Interface | TUI settings (mouse off) | opencode TUI | ACTIVE | Keep |
| `package.json` | Config/Scaffolding | declares `@opencode-ai/plugin` | tooling (not imported by sara.js) | UNUSED at runtime | Keep (plugin dev-header) |
| `package-lock.json` | Config | lockfile | npm | GENERATED | Keep alongside manifest |
| `node_modules/` | Runtime | dependency tree (zod, msgpackr, yaml, …) | plugin toolchain | GENERATED | Orphans from version control; never commit |
| `.gitignore` | Config | ignores node_modules/package files | (no repo exists here) | UNUSED | Delete or create the git repo it implies |
| `plugin/sara.js` (52 ln) | Runtime/Observability | telemetry hook: every tool call → NDJSON | opencode hook bus; consumers: evaluation/docs/this report | ACTIVE | Keep (canonical telemetry) |
| `test/sara-plugin.test.mjs` (68 ln) | Evaluation | 4 node:test cases for the plugin | `node --test` | ACTIVE (dev-time) | Keep — the only automated test Sara owns |
| `command/sara-decide.md` | Decision | architecture decision gate (task class, AI/agent, tier, persist) | invoked by human/Sara; output → `SARA-DECISIONS.md` | ACTIVE (invoked-inline; sink never written) | Merge into a single decision artifact (duplicates architect.md) |
| `command/sara-review.md` | Routing/Review | routes review to skill vs reviewer agent | invoked by human/Sara | ACTIVE (used in controlled test) | Consolidate routing table with AGENTS.md |
| `command/sara-audit.md` | Routing/Review | delegrates whole-repo debt scan to auditor | invoked by human/Sara; sink `SARA-AUDIT.md` | INDIRECTLY USED (never invoked; sink absent) | Keep as wrapper, or fold into one review command |
| `command/sara-eval.md` | Evaluation | golden-task execution + evidence capture | `/sara-eval`; output caption → `SARA-GOLDEN-RESULTS.md` | INDIRECTLY USED (this test superseded it; results file exists from Round 2) | Keep; decouple from hardcoded temp path |
| `agent/architect.md` | Agents/Decision | read-only architecture decision reviewer; decision block | Sara (Tier-2 review) | ACTIVE (used once in controlled test) | Keep as agent (safe read-only isolation) — but de-duplicate its block vs sara-decide |
| `agent/reviewer.md` | Agents/Review | correctness+security+complexity reviewer | Sara (Tier-2/3 review) | INDIRECTLY USED (defined, not yet invoked) | Keep |
| `agent/auditor.md` | Agents/Audit | whole-repo complexity/debt scanner | `/sara-audit` | INDIRECTLY USED (defined, not yet invoked) | Keep; absorb sara-debt skill |
| `skills/sara-review/SKILL.md` | Skills | complexity-only review (5 tags) | AGENTS.md, reviewer.md, auditor.md, sara-review.md | ACTIVE (used in controlled test) | Keep as **canonical** taxonomy owner |
| `skills/sara-debt/SKILL.md` | Skills | harvests `sara:` markers → debt ledger | user phrases only; not referenced by commands/agents | INDIRECTLY USED | Merge into auditor (subset) |
| `skills/read-terminals/SKILL.md` + `read_terminals.py` | Skills | read other opencode sessions from shared DB | user phrases; `read_terminals.py` | INDIRECTLY USED but **BROKEN on this host** (hardcoded `C:/Users/m.barani/...`; DB is under `98903`) | Fix path (parameterize via home discovery) or mark dormant |
| `memory/sara.md` (21 KB) | State/Memory | cross-session journal (manual append) | Sara, for continuity | ACTIVE | Keep; consider trimming finished ai-swe-engine detail (historical) |
| `state/tool-events.ndjson` (24 KB, 73 ln) | State (GENERATED) | telemetry event stream | eval, reports | GENERATED | Exclude from versioning; rotate/archive |

## 3.2 Runtime data — `~/.local/share/opencode/` (opencode-owned, not Sara)

| Path | Purpose | Status |
| ---- | ------- | ------ |
| `opencode.db` (+`-wal`,`-shm`) | sessions/messages/todos (49 MB) | GENERATED — runtime state, not Sara's |
| `log/`, `repos/`, `snapshot/`, `tool-output/` | runtime aux data | GENERATED |

## 3.3 Docs repo — `sara-docs/`

| File | Layer | Purpose | Status | Candidate |
| ---- | ----- | ------- | ------ | --------- |
| `README.md` | Docs | index + task log | ACTIVE | Keep — index should become the single entry |
| `SARA_SYSTEM_MAP.md` | Docs | Phase-0 discovery inventory | LEGACY (describes pre-implementation state; "Evaluation: none", "no commands") | Merge into ARCHITECTURE_AFTER_ROUND2 |
| `SARA_ARCHITECTURE_AFTER_ROUND2.md` | Docs | as-built architecture | ACTIVE | Keep as the single architecture doc |
| `SARA_SELF_BOUNDARY.md` | Docs | self-modification boundary | ACTIVE | Keep (short) |
| `SARA_SELF_UPGRADE_ROUND2_BASELINE.md` | Docs | pre-upgrade measurements | LEGACY (snapshot) | Archive |
| `SARA_SELF_UPGRADE_ROUND2_FINAL_REPORT.md` | Docs | full upgrade report (439 ln) | LEGACY (event record) | Archive |
| `SARA_UPGRADE_CANDIDATES.md` | Docs | candidate list (superseded) | LEGACY | Archive |
| `SARA_GOLDEN_TASKS.md` | Evaluation | golden task definitions | ACTIVE | Keep (do NOT modify) |
| `SARA-GOLDEN-RESULTS.md` | Evaluation | golden result records | ACTIVE | Keep — the eval sink |
| `PONYTAIL_SELF_UPGRADE_REPORT.md` | Docs | vendored-ponytail audit | LEGACY (one-off) | Archive |
| `SARA_ROUND2_CONTROLLED_TEST_REPORT.md` | Evaluation | controlled test evidence | ACTIVE | Keep |
| `PROGRESS-PHASE-2.md` | Docs | ai-swe-engine manifest (unrelated) | UNUSED here (owner excluded from commit) | Move to ai-swe-engine or archive |
| `ponytail/` | Vendored third-party | embedded git clone for self-upgrade study | UNUSED (worked-from copy) | Exclude from repo; reference by URL |
| `java/`, `.idea/` | TEMPORARY / editor | G1 scaffold, IDE state | TEMPORARY / UNUSED | Delete scaffold; ignore IDE |

---

# 4. Layer Map

| Layer | Components |
| ----- | ---------- |
| 1. Interface | opencode TUI + `tui.json`, CLI, model `big-pickle` |
| 2. Configuration | `opencode.jsonc` (+`.bak`), `package.json`/lock, `.gitignore` |
| 3. Instructions / Policy | `AGENTS.md` (persona, Decision Ladder, gates, v2-bridge) |
| 4. Skills | `sara-review`, `sara-debt`, `read-terminals` (+ helper py) |
| 5. Decision | `command/sara-decide.md`, `agent/architect.md` (schemas duplicated) |
| 6. Routing | `command/sara-review.md` (tier→skill/agent), `command/sara-audit.md` (→auditor) |
| 7. Orchestration | none as files — opencode primary loop (Sarah manual; no state machine) |
| 8. Agents / Subagents | `architect`, `reviewer`, `auditor` (custom) + built-ins (`explore`, `general`) |
| 9. Tools | opencode built-ins (read/edit/write/bash/glob/grep/task/webfetch/websearch/question/todowrite/skill) |
| 10. Runtime | `plugin/sara.js`, opencode hook bus |
| 11. State / Memory | `memory/sara.md`, `state/tool-events.ndjson`, opencode.db |
| 12. Observability | `plugin/sara.js` → `state/tool-events.ndjson` |
| 13. Evaluation | `SARA_GOLDEN_TASKS.md`, `SARA-GOLDEN-RESULTS.md`, `test/sara-plugin.test.mjs`, `command/sara-eval.md`, controlled-test report |
| 14. Persistence | `memory/sara.md`, `.bak-20260830` files, state dir (unversioned), docs repo commit history |
| 15. Documentation | `sara-docs/*.md` (12 files) |

(No component required a new layer — the 15-layer taxonomy fits.)

---

# 5. Dependency Graph

```
WHO CALLS WHOM / DEPENDS / READS / WRITES / TRIGGERS
(text edge weights: calls →, depends ⇒, reads ⇠, writes ⇢, triggers ⤷)

User
 ⤷ opencode TUI/CLI  ⇒ opencode.jsonc (plugin, permission) · AGENTS.md (loaded every session)
User/Sara ⤷ commands:
  sara-decide  ⇒ architect.md (schema)         ⇢ SARA-DECISIONS.md   (NEVER written)
  sara-review  ⇒ sara-review skill | reviewer   ⇒ AGENTS.md (tiers)   ⇢ verdict
  sara-audit   ⇒ auditor.md                    ⇢ SARA-AUDIT.md       (NEVER written)
  sara-eval    ⇒ GOLDEN_TASKS ⇠ telemetry file ⇢ SARA-GOLDEN-RESULTS.md
Sara (primary) ⤷
  tools (built-in) ⇒ opencode hook bus → plugin/sara.js → state/tool-events.ndjson
  ├─ read/write/edit/bash/glob/grep (file I/O) ⇠ repo
  ├─ task ⇒ agents: architect / reviewer / auditor / explore / general   (deny edit, deny bash)
  └─ skill ⇒ sara-review / sara-debt (user-phrase trigger) / read-terminals (helper py)
Skills:
  sara-review ⇒ AGENTS.md ladder (taxonomy owned here; copied into reviewer.md & auditor.md)
  sara-debt   ⇒ grep sara: markers         (subset of auditor's job)
  read-terminals ⇒ read_terminals.py ⇒ C:/Users/m.barani/...opencode.db   [MISMATCH → broken]
Evaluations: sara-eval ⇠ tool-events.ndjson (hardcoded path); GOLDEN tasks ⇒ results file.
Docs:      sara-docs/* ⇠ describes config+repo; SYSTEM_MAP/MISC describe stale state (drift).
Runtime:   opencode.db ⇢ sessions/messages/todos (opencode-owned, Sara only reads via read-terminals).
```

---

# 6. Duplication

| Concept | Location A | Location B | Type | Recommended Source of Truth |
| ------- | ---------- | ---------- | ---- | --------------------------- |
| Least-mechanism ladder | `AGENTS.md` (Decision Ladder) | `architect.md` "Prefer the least mechanism…" | 2nd copy of policy | `AGENTS.md` (architect references the rule, does not re-state it) |
| Decision-block schema (13 fields) | `command/sara-decide.md` | `agent/architect.md` | identical schema, two hosts | ONE block schema doc that both invoke |
| Task classification schema | `command/sara-decide.md` | `agent/architect.md` | identical | Same as above |
| Review tier ladder (0–3) | `AGENTS.md` | `sara-decide.md` | `sara-review.md` | same text 3× | `AGENTS.md` single table |
| 5-tag complexity taxonomy | `skills/sara-review/SKILL.md` | `reviewer.md` | `auditor.md` | copied 3× | `skills/sara-review/SKILL.md` (others say "use sara-review tags") |
| `sara:` debt-ledger format (`no-trigger`) | `auditor.md` | `sara-debt/SKILL.md` | exact replica format | `auditor.md`; sara-debt folded in |
| Salvage autonomy (ask-list) | `AGENTS.md` (list of 6) | `opencode.jsonc` (same 6 patterns) | policy ↔ mechanism (must stay in sync; currently consistent) | `opencode.jsonc` is mechanism; AGENTS.md lists policy only (drop the inventory) |
| Architecture description | `SARA_SYSTEM_MAP.md` | `SARA_ARCHITECTURE_AFTER_ROUND2.md` | overlapping layer inventories | ARCHITECTURE_AFTER_ROUND2 |
| Round-2 event record | `FINAL_REPORT.md` ↔ `memory/sara.md` 2026-08-30 entry | near-identical summary | memory (short), report (long) | Keep memory as the log; report archived |
| Task log | `README.md` Task Log | `PROGRESS-PHASE-2.md` | 28-line duplicate of a manifest | README links the manifest; does not paste it |
| Plugin test | `test/sara-plugin.test.mjs` | memory/sara.md ("4 tests pass") | unreferenced elsewhere | Keep test file; docs don't need to restate |

---

# 7. Responsibility Collisions

| Component A | Component B | Overlap | Problem | Recommended Boundary |
| ----------- | ----------- | ------- | ------- | -------------------- |
| `sara-decide` command | `architect` agent | both run "the decision gate" with the same schema | two decision engines; which is authoritative? | Command = user-facing ceremony (persists); agent = delegated second opinion. Same schema, invoke both — don't maintain two copies |
| `reviewer` agent | `sara-review` skill | both review *complexity* | reviewer is a superset (adds correctness/security) | Skill = complexity canonical; agent references it and adds C/S |
| `auditor` agent | `sara-debt` skill | both produce the `sara:` debt ledger | two debt tools | Debt ledger owned by auditor; skill becomes a thin user wrapper or disappears |
| `auditor` agent | `sara-review` skill | auditor *is* a whole-repo sara-review | whole-repo vs diff-level variant of same taxonomy | Same taxonomy source; scope differs (repo vs diff) — legit, document it |
| `sara-review` command | `AGENTS.md` review-tier table | routing rules duplicated | command must re-implement policy | Command references the table by name |
| `sara-eval` | plugin telemetry | eval reads the telemetry file | correct coupling, but via hardcoded path+format | Telemetry = interface; document the schema, not the path |
| `memory/sara.md` | AGENTS.md | both carry project-path memory | duplication of standing context | AGENTS.md: current-only; memory: history |
| Docs set | docs set | SYSTEM_MAP/FINAL_REPORT/ARCHITECTURE overlap | reader can't tell which is current | 1 live architecture doc + archive the rest |

---

# 8. Orphaned Components

Verified (no active consumer found in config or repo):

| Item | Why it looks orphaned |
| ---- | --------------------- |
| `.gitignore` (config root) | no git repository exists at `~/.config/opencode` (verified `Test-Path .git = False`) |
| `AGENTS.md.bak-20260830`, `opencode.jsonc.bak-20260830` | no automated rollback reads them; referenced only by memory/sara.md prose |
| `skills/sara-debt/SKILL.md` | referenced by no command, agent, or AGENTS.md entry; trigger is user phrase only; its output file `SARA-DEBT.md` never created |
| `command/sara-audit.md` output sink `SARA-AUDIT.md` | the file the command is specified to write has never been created |
| `command/sara-decide.md` output sink `SARA-DECISIONS.md` | ditto — never created (this session recorded decisions inside the test report instead) |
| `command/sara-eval.md` + golden tasks | defined; controlled test ran instead this session; results file exists only from Round-2 setup |
| `agent/reviewer.md`, `agent/auditor.md` | both defined; telemetry shows zero `task` invocations of reviews/audits so far (architect used once) |
| `package.json` `@opencode-ai/plugin` dep | `sara.js` imports only `node:*`; the dep is dev/type-only — likely never loaded at runtime |
| `read-terminals` skill | functional orphan on THIS host: its stated capability cannot run (path mismatch) |
| `sara-docs/PROGRESS-PHASE-2.md` | ai-swe-engine artifact, owner-excluded from this repo's history |
| `sara-docs/ponytail/` | a full third-party clone whose only interplay is PONYTAIL report (also not referencing the copy anymore) |

---

# 9. Wrong-Layer Responsibilities

| Current Location | Responsibility | Better Layer | Reason |
| ---------------- | -------------- | ------------ | ------ |
| `AGENTS.md` | machine-specific references (`C:\Users\m.barani\…`, downloads path, "SQLite DB at C:/Users/m.barani/…") | removed/parameterized | policy file must be host-neutral (this host's user is `98903`) |
| `AGENTS.md` | the Sara v2 Gateway bridge (8800) | removed on this host | v2 is documented absent here; always-loaded text describes a dead gateway |
| `AGENTS.md` | full inventory of `ask` permissions | `opencode.jsonc` (mechanism) only | two lists to keep in sync = drift risk |
| `AGENTS.md` | review-tier ladder | a single tier table (in AGENTS.md) referenced by others | currently restated inside two commands |
| `agent/reviewer.md` + `agent/auditor.md` | the 5-tag taxonomy text | `skills/sara-review/SKILL.md` | one owner, two references |
| `read-terminals/read_terminals.py` | hardcoded absolute DB path | discovery via `~` (homedir) / env | baked machine identity into a skill |
| `command/sara-eval.md` | hardcoded temp dir + telemetry path | constants/params | evaluating on this host only |
| `plugin/sara.js` | schema of `args` summarized inline | documented interface | consumers (eval/reports) re-derive the format by reading the plugin |
| `memory/sara.md` | 21 KB of finished ai-swe-engine project log | `ai-swe-engine` repo | Sara's memory should be Sara's decisions, not another repo's changelog |

---

# 10. Coupling Problems

| Finding | Type | Rating |
| ------- | ---- | ------ |
| `read-terminals` → `C:/Users/m.barani/...` | hardcoded path (broken on host) | **HIGH** — capability dead until fixed |
| `sara-eval` → `~/.config/opencode/state/tool-events.ndjson` + temp dir | hardcoded paths | **MEDIUM** |
| `AGENTS.md` ↔ `opencode.jsonc` permission inventory | two lists = sync debt | **MEDIUM** |
| `Sara's` commands/agents ↔ AGENTS.md doctrine | implicit convention (no reference-links enforced) | **MEDIUM** |
| `sara-review` skill taxonomy copies (reviewer/auditor) | duplicated data, not code | **MEDIUM** (drift risk) |
| `architect.md` ↔ `sara-decide.md` schema | duplicated decision format | **MEDIUM** |
| Docs ↔ runtime (SYSTEM_MAP, BASELINE, FINAL_REPORT) | stale descriptions | **HIGH** for navigation, LOW for runtime (docs don't execute) |
| `reviewer.md` → `sara-review` skill (taxonomy) | dependency declared but not enforced (grep-able) | **LOW** |
| `plugin/sara.js` → `state/` file | state dir coupled to config dir | **LOW** (portable override `SARA_STATE_DIR` exists) |
| Evaluation ↔ telemetry | format dependency | **LOW** — but schema undocumented |
| `sara-docs` ↔ ponytail vendored clone | embedded repo | **MEDIUM** (bloat + orphan risk) |
| opencode.db (`read-terminals`) | schema knowledge (empty `session_message` table, etc.) lives in memory, not in skill | **MEDIUM** |

No circular dependency found. The only CRITICAL-adjoining risk is the broken `read-terminals` path (HIGH) — not architecture, a one-line fix.

---

# 11. Context Bloat

Always-loaded (measured): `AGENTS.md` 7.3 KB / 110 lines.

| Source | Approx Size | Always Loaded? | Necessary? | Recommendation |
| ------ | ----------: | -------------- | ---------- | -------------- |
| `AGENTS.md` persona+identity | ~1.5 KB | YES | YES | Keep |
| `AGENTS.md` Decision Ladder | ~1 KB | YES | YES | Keep |
| `AGENTS.md` Operational Gates (Round 2) | ~2.5 KB | YES | Mostly — needs the tiers & sinks | Keep; drop re-listed content |
| `AGENTS.md` Standing context (m.barani paths, downloads, gitlab) | ~0.8 KB | YES | **NO on this host** | Remove machine/other-user specifics |
| `AGENTS.md` Sara v2 bridge (default executor, 8800, approval calls) | ~1.5 KB | YES | **NO on this host** | Remove or mark inactive; v2 absent (verified) |
| Skill inventory (3 descriptions) | ~1.5 KB | YES (descriptions) | YES | Keep |
| `memory/sara.md` | 21 KB | NO (referenced) | Partial | Not in context; fine — but trim stale ai-swe-engine section when next appended |
| Command/agent/skill bodies | ~12 KB total | NO (on invocation) | YES | Keep |
| Docs (sara-docs) | ~100 KB | NO | YES | Consolidate (§20) |

Net: the **always-loaded** waste is ~2.3 KB of this-host-irrelevant policy text (≈25% of AGENTS.md). Modest, but it is permanent per-session overhead and the most visible wrong-layer content.

---

# 12. Operational Flow

Actual current flow (compiled from config + observed session):

**Trivial coding task** (e.g., G1):
```
INPUT → primary loop → [AGENTS.md ladder rung 2/3: stdlib] → direct tools → plugin telemetry append → OUTPUT
Steps: 0 gate steps (Tier 0). Correct: no added ceremony.
```

**Normal coding task** (e.g., G10):
```
INPUT → CLASSIFICATION (inline decision block: class=CODE, AI=NO, agent=WORKFLOW, L1, tier 1)
  → TOOLS (search/read) → self-review checklist (AGENTS.md) → sara-review skill (complexity)
  → verification (bash assert) → TELEMETRY (auto) → OUTPUT
Steps worth noting: the decision block is emitted but NOT persisted to SARA-DECISIONS.md (sink never materialized) — the ceremony's persistence step is currently dead code in the workflow.
```

**Architecture task** (G9):
```
INPUT → CLASSIFICATION + DECISION block → ROUTING (tier 2) → SUBAGENT architect (deny-edit/bash)
  → inline verdict cross-checked → TELEMETRY → OUTPUT
```

**High-risk task** (not observed this session; per config):
```
INPUT → CLASSIFICATION (tier 3) → architect + reviewer → human “ask” gate
  (jsonc permission patterns: git push*/reset --hard*/clean -fd*/rm -rf*/dropdb*/docker compose down -v*) → execute → telemetry → OUTPUT
Note: AGENTS.md also lists deploy/production as human-approval, but those have NO mechanical gate (no matching permission pattern) — enforced only by discipline.
```

**Evaluation task** (`/sara-eval`):
```
INPUT (golden task) → DECISION block → execute in temp sandbox → CAPTURE (telemetry reads tool-events.ndjson, git diff stats, LOC) → append SARA-GOLDEN-RESULTS.md → OUTPUT
```

Unnecessary steps identified: (a) decision-block **persistence** is spec'd but inert; (b) two review paths (`sara-review` command routing table duplicated in AGENTS.md) force reconciliation; (c) hardcoded paths in eval make the "run anywhere" promise false on other hosts.

---

# 13. Agent Analysis (architect / reviewer / auditor)

| | architect | reviewer | auditor |
| -- | --------- | -------- | ------- |
| Responsibility | pre-code architecture decision review + decision block | correctness/security/complexity on a specific change | whole-repo complexity/debt scan |
| Trigger | Tier-2 routing; human | Tier-2/3 routing; human | `/sara-audit`; human |
| Inputs | problem statement / plan | change/diff under review | repo root |
| Outputs | decision block + one-line recommendation | ordered SEVERITY findings + verdict | ranked findings + `sara:` debt ledger + summary |
| Tools | read-only (edit: deny, bash: deny) | read-only | read-only |
| Permissions | deny edit/bash (subagent mode) | deny edit/bash | deny edit/bash |
| Relationship to Sara | delegated second opinion | counterparty review | delegated scan |
| Overlap | **with `sara-decide`** (schema clone) | **with `sara-review` skill** (taxonomy clone) | **with `sara-debt` skill** (format clone) |
| Remain an agent? | YES — isolation (deny edit/bash) is the point; safer than a workflow the primary runs | YES | YES |
| Could it be a skill/workflow instead? | Schema could be a shared skill, but role-as-agent gives permission isolation | Same | Same — and it should *absorb* sara-debt |

Verdict: all three **should remain agents** (read-only isolation is a genuine safety feature), but all three should stop *copying* doctrine and instead reference shared policy artifacts.

---

# 14. Command / Workflow Analysis

| | sara-decide | sara-review | sara-audit | sara-eval |
| -- | ----------- | ----------- | ---------- | --------- |
| Owns | decision gate ceremony + persistence | review routing (skill vs reviewer) | audit delegation | golden-task harness + evidence capture |
| Invoked by | human `/…`; Sara (inline in this session) | human/Sara | human/Sara | human `/…` |
| Duplicates | decision schema also in architect.md | tier ladder also in AGENTS.md | whole concept duplicated by sara-debt | telemetry path/format re-derived by hand |
| Remain a command? | YES (flow + persist) — but share the schema | YES (router) — but reference AGENTS.md tiers | YES or fold into sara-review | YES |
| Better as workflow? | No — commands ARE the workflow surface for opencode | No | No | No |
| Primary fix | single decision-block artifact referenced by both | single tier table | absorb sara-debt | parameterize paths; document telemetry schema |

Two commands (`sara-decide`, `sara-eval`) have spec'd outputs that have never been produced; the commands themselves remain valid.

---

# 15. Telemetry Analysis

- **What/where**: `plugin/sara.js` hooks `tool.execute.before/after`; per call it captures `ts, tool, sessionID, callID, elapsedMs, outputLen, title, args{filePath,path,pattern,include,query,tool,command,input}+fieldCount` (values truncated: args 160, title 120).
- **Persisted to**: `~/.config/opencode/state/tool-events.ndjson` (append, best-effort, never throws; `started` map capped at 2000; env override `SARA_STATE_DIR`).
- **Consumed by**: evaluation (`sara-eval` references it), reports/audits (this session used it), humans.
- **Coupled to execution?** No — hooks are passive; failure is swallowed. Good separation.
- **Separation of telemetry vs state**: plugin output is the only writer into `state/`; opencode's own DB lives elsewhere. Already cleanly separated from source/config.
- **Generated files mixed with source?** `state/tool-events.ndjson` sits inside the config dir (not a git repo, so no accidental commit risk here); the docs repo's `.gitignore`/commit discipline excludes it. The `SARA_STATE_DIR` override exists but is undocumented anywhere — minor.
- **Gap**: no schema document for record fields; `sara-eval` and this report re-derive the format by reading the plugin.

Verdict: telemetry is the cleanest component in the system. Leave it alone; doc its schema.

---

# 16. Safety / Permissions Analysis

- **Where gates live**: `opencode.jsonc` `permission.bash` (6 patterns, all `ask`); policy text in `AGENTS.md` (autonomy tiers + human-approval list); actual approval UI = interactive opencode runtime.
- **Who enforces**: opencode runtime (mechanical, on bash tool calls). Not the plugin.
- **Centralized?** Yes, mechanically one place — but **doctrinally two** (AGENTS.md list mirrors jsonc patterns, and AGENTS.md includes doctrine with no mechanical backstop: deploy/production/credential expose are "human approval" only by discipline).
- **Duplicated rules**: the 6 patterns exist twice (AGENTS.md + jsonc). Currently consistent.
- **Bypass paths**: none found. `bash` is gated by pattern; `edit/write` are not restricted by permission config (Sara's own autonomy governs edits — matches design). `task` (subagents) carry their own deny-edit/bash.
- **Do permissions belong in plugin/config/workflow/policy?** Mechanics: `opencode.jsonc` (correct). Doctrine: `AGENTS.md` (correct). The two must be reconciled so the policy list never drifts from the enforced list — the single highest-risk drift point if someone edits only one file.

---

# 17. Evaluation Analysis

- **Golden tasks**: `sara-docs/SARA_GOLDEN_TASKS.md` (10 tasks) — untouched by all Round-2 work (verified content; owned definitions).
- **Logic**: `command/sara-eval.md` procedure (decide → temp sandbox → capture → append results).
- **Reports**: `SARA-GOLDEN-RESULTS.md` (from Round 2) + this session's `SARA_ROUND2_CONTROLLED_TEST_REPORT.md`.
- **Telemetry**: consumed via file path at capture time.
- **Storage**: results in docs repo (versioned); task scratch in `%TEMP%\opencode` (throwaway — good).
- **Coupling**: evaluation depends on the telemetry file *path + field names* (assumed, not documented) → MEDIUM coupling, LOW blast radius (telemetry is stable).
- **Duplication/contamination**: none — golden definitions separate from runtime; no generated artifact lives in source; the controlled test superseded, not corrupted, the golden loop.
- **Recommendation**: document the telemetry schema; keep eval as a command; leave golden tasks frozen.

---

# 18. Documentation Drift

| Documentation | Reality | Drift | Severity |
| ------------- | ------- | ----- | -------- |
| SYSTEM_MAP "3 skills; no commands; Evaluation none; Task classification none" | 3 skills, but 4 commands + 3 agents + eval now exist | obsolete (Phase-0 snapshot) | HIGH (navigation) |
| SYSTEM_MAP "user `98903`, opencode v1.18.25" | correct | none | — |
| AGENTS.md "user m.barani" / downloads path | host is `98903` | wrong host refs in live policy | MEDIUM |
| AGENTS.md "Sara v2 default executor (8800)" | v2 absent on this host | dead gateway described as default | MEDIUM |
| ARCHITECTURE_AFTER_ROUND2 (commands/agents/plugin/permissions) | matches disk exactly | none | — |
| memory/sara.md "SARA V2 IS NOW THE DEFAULT RUNTIME" | not true on this host | stale | MEDIUM |
| read-terminals SKILL "DB at C:/Users/m.barani/..." | real DB is `98903`, and m.barani path missing | **broken pointer** | HIGH |
| `sara-eval` path `C:\Users\98903\AppData\Local\Temp\opencode` | correct on this host | machine-specific (fine here, breaks elsewhere) | LOW |
| README "Documents" index lists PROGRESS-PHASE-2 + ponytail/ | both untracked/uncommitted on disk | index vs version-control mismatch | LOW |
| FINAL_REPORT/BASELINE/CANDIDATES (Round-2 event records) | historical, do not describe "now" | intentionally snapshot | LOW (archive) |
| GOLDEN_TASKS | unmodified | none | — |

---

# 19. Current Architecture Diagram (as-built)

```
┌────────────────────────────────────────────────────────────┐
│ INTERFACE   opencode TUI (tui.json) · CLI · big-pickle       │
├────────────────────────────────────────────────────────────┤
│ POLICY      AGENTS.md  [persona · Decision Ladder · gates]   │  ← machine-specific + v2-bridge noise
├────────────────────────────────────────────────────────────┤
│ SKILLS      sara-review (Taxonomy◄─canonical) · sara-debt    │
│             read-terminals ▶(BROKEN hardcoded path)          │
│ COMMANDS    sara-decide ◄─┐ sara-review · sara-audit · sara-eval│
├────────────────────────────────────────────────────────────┤
│ DECISION/ROUTING   tier table (AGENTS.md) · architect schema│  ← schema duplicated command/agent
├────────────────────────────────────────────────────────────┤
│ AGENTS      architect ● reviewer ○ auditor ○  (read-only)   │  ●=used · ○=defined, unused
├────────────────────────────────────────────────────────────┤
│ RUNTIME/TOOLS  opencode hooks ⇒ plugin/sara.js              │
├────────────────────────────────────────────────────────────┤
│ STATE/OBS   state/tool-events.ndjson · memory/sara.md       │
│ EVAL        golden tasks + results + plugin tests           │
│ PERSISTENCE opencode.db · .bak-20260830 · docs-repo (git)   │
│ DOCS        sara-docs (12 md) ◄── some stale                 │
└────────────────────────────────────────────────────────────┘
```

---

# 20. Proposed Clean Architecture

Principles: one source of truth per concept, minimal always-loaded text, policy-doctrine split, generated-state exclusion, single doc home.

### CURRENT
- Decision-block schema: **2** copies (command + agent)
- Tier ladder: **3** copies (AGENTS.md + 2 commands)
- Complexity taxonomy: **3** copies (skill + 2 agents)
- Debt ledger: **2** producers (auditor + sara-debt)
- Architecture doc: **3** overlapping (SYSTEM_MAP/ARCHITECTURE/FINAL_REPORT)
- Permissions inventory: **2** lists (policy + mechanism)
- Broken skill: 1 (read-terminals path)
- Persistence sinks: 3 never-written (DECISIONS/AUDIT/DEBT)

### PROPOSED
- Decision-block schema: **1** artifact (`policy/decision-block.md`) referenced by command + architect
- Tier ladder: **1** table in AGENTS.md; commands reference it
- Complexity taxonomy: **1** (sara-review skill); reviewer/auditor cite it
- Debt ledger: **1** producer (auditor); sara-debt wrapper removed or made a 3-line alias
- Architecture doc: **1** live (`ARCHITECTURE_AFTER_ROUND2.md`) + an `archive/` folder
- Permissions: **1** mechanical source (`opencode.jsonc`); AGENTS.md states doctrine only (no inventory)
- `read-terminals`: path discovery fixed (`~` expansion); helper works on any host
- Evaluation/temp/state paths: parameters or env, documented telemetry schema
- State stays outside source; `sara-docs` gains `archive/` + `eval/` subfolders

Result: fewer moving pieces, same capabilities — zero agents removed, zero commands removed, safety surface enlarged (doctrine now can't silently drift from mechanism).

---

# 21. Current vs Proposed (surface delta)

| Metric | Current | Proposed | Delta |
| ------ | ------- | -------- | ----- |
| Decision-block copies | 2 | 1 | −1 |
| Tier-ladder copies | 3 | 1 | −2 |
| Taxonomy copies | 3 | 1 | −2 |
| Debt-ledger producers | 2 | 1 | −1 |
| Live architecture docs | 3 | 1 | −2 |
| Broken/vestigial files | 4–5 (read-terminals, .gitignore, 2 .bak, sara-debt) | 0–2 | −3 |
| Written-but-undeclared sinks | 3 | 3 (now actually used) | 0 |
| Agents | 3 (custom) + 2 built-in | 3 | 0 |
| Commands | 4 | 4 | 0 |
| Skills | 3 | 2–3 | −0/1 |
| Always-loaded waste | ~2.3 KB | ~0.3 KB | −2 KB |

---

# 22. Target Directory Structure (based on ACTUAL files)

```
~/.config/opencode/
├── opencode.jsonc                   # plugin + permission gates (sole mechanical safety)
├── policy/
│   ├── AGENTS.md                    # persona + ladder + tier table (host-neutral)
│   └── decision-block.md            # SINGLE schema used by command + architect
├── skills/
│   ├── sara-review/                 # canonical taxonomy (unchanged)
│   ├── read-terminals/              # path fix only
│   └── (sara-debt → fold into auditor, or 3-line wrapper)
├── agents/        architect.md · reviewer.md · auditor.md    (reference, don't copy, policy)
├── commands/      sara-decide.md · sara-review.md · sara-audit.md · sara-eval.md
├── plugin/        sara.js
├── test/          sara-plugin.test.mjs
└── state/         tool-events.ndjson        # GENERATED — never versioned
    (backups: move .bak → archive/ or retire)

sara-docs/
├── SARA_ARCHITECTURE_AFTER_ROUND2.md   # single live architecture doc
├── SARA_SELF_BOUNDARY.md · SARA_GOLDEN_TASKS.md · SARA-GOLDEN-RESULTS.md
├── archive/   FINAL_REPORT · SYSTEM_MAP · BASELINE · CANDIDATES · PONYTAIL_REPORT
└── README.md  (points at the above + archive)
```

No new runtime component introduced; the structure mirrors what exists minus the duplication.

---

# 23. Refactoring Plan (ranked — DO NOT EXECUTE)

### P0 — Critical (none strictly destructive; highest drift risk first)
1. **Fix `read-terminals` hardcoded path.** Problem: skill unusable on this host; helpers point at a nonexistent `C:/Users/m.barani/...` DB. Change: resolve `~/.local/share/opencode/opencode.db` at runtime (Python `Path.home()`, skill text says `~`); files: `skills/read-terminals/{SKILL.md,read_terminals.py}`. Dependencies: none. Risk: none (read-only). Rollback: 2-line revert. Benefit: working multi-terminal visibility. Behavior change: YES (capability becomes functional).

### P1 — High value
2. **Single source for the decision-block schema.** Problem: `sara-decide` and `architect` maintain identical 13-field block + classification + ladder text. Change: `policy/decision-block.md`; both files reference it ({command, agent} keep only mission-specific prose). Files: `command/sara-decide.md`, `agent/architect.md`, new `policy/decision-block.md`. Risk: LOW (text-only); rollback trivial; benefit: one edit updates both; behavior: NO change to decisions themselves.
3. **Single tier table.** Problem: 0–3 ladder text in AGENTS.md + sara-decide + sara-review. Change: keep in AGENTS.md; commands reference. Same class as #2.
4. **Make `sara-debt` a thin wrapper or fold into auditor.** Problem: format duplicate. Change: auditor owns debt ledger; `sara-debt` becomes a 3-line alias (grep → ledger) or is removed. Risk: no capability lost (auditor superset). Behavior: NO change for users who say "sara debt" (alias still answers); YES if skill deleted without alias.

### P2 — Nice to have
5. **Archive Round-2 event docs** (SYSTEM_MAP, FINAL_REPORT, BASELINE, CANDIDATES, PONYTAIL_REPORT → `sara-docs/archive/`) and slim README Task Log to a link. Behavior: NO runtime change.
6. **Strip machine-specific/v2 content from AGENTS.md** (~2.3 KB). Risk: LOW; behavior: NO for this host (v2 dead); big context win on other hosts.
7. **Parameterize `sara-eval` paths** (temp + telemetry) and **document the telemetry schema** in the plugin or a `policy/telemetry.md`. Behavior: NO.
8. **Reconcile permissions**: AGENTS.md stops listing the 6 patterns (references jsonc instead); optionally add mechanical gates for "deploy/production" if that doctrine is to be real. Behavior: NO unless new gates added (then protection increases).

### P3 — Do not touch
- Plugin `sara.js` + `state/tool-events.ndjson` schema/collection.
- `SARA_GOLDEN_TASKS.md` definitions and the eval result pipeline.
- The three agents' deny-edit/deny-bash permissions.
- committed `sara-docs` history and the golden results.
- `ponytail/`, `PROGRESS-PHASE-2.md`, `java/` (keep out of version control; do not modify).

---

# 24. Risk Analysis (of pursuing delene cleanup)

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| Consolidating decision schema mislinks (command reads missing artifact) | LOW | MED | Keep both files working during the change; verify by re-invoking a decision |
| Archiving docs removes the canonical Round-2 narrative | LOW | LOW | Archive folder is still in the repo; nothing deleted |
| `sara-debt` removal surprises a user who typed "sara debt" | LOW | LOW | Ship alias first, remove later |
| Editing AGENTS.md by stripping v2 bridge changes behavior unexpectedly | MED (bridge text still referenced in memory) | LOW | Re-run a trivial + Tier-2 task after edit |
| read-terminals path fix reads the wrong new DB | MED | LOW | Verify against `~/.local/share/opencode/opencode.db` existence check |
| Any change to plugin/permissions | HIGH-risk, so **excluded** | — | P3 list — do not touch |

---

# 25. Minimality Check

Smallest architecture preserving all valuable capabilities:

- **Keep:** plugin + telemetry file; agent trio (read-only isolation); 4 commands (the workflow surface); sara-review skill; AGENTS.md ladder; jsonc gates; golden tasks; memory; README-as-index. → the full capability set survives with **2–3 files deleted** (`.gitignore`, `sara-debt`, eventually the 5 archived docs) and **~4 files edited for dedup** — no new abstractions, no new agents, no new persistence.
- **Removed without loss:** `sara-debt` (subset of auditor); `.gitignore` (or the repo it implies); README Task-Log duplication; read-terminals broken copy→fixed.
- **Preserved:** safety (permissions mechanical), observability (plugin untouched), evaluation (golden set frozen), decision quality (schema single copy but same decisions), rollback (git history + .bak archives), testability (plugin tests untouched), specialization (three roles).

Delta: **~0 lines of complex logic added; ~–40 lines of duplicated text; 1 capability repaired.**

---

# 26. What MUST NOT Be Changed

1. `plugin/sara.js` and the `tool-events.ndjson` record schema — telemetry is the system's cleanest component and others (eval, reports) consume it.
2. `opencode.jsonc` permission gates — the only mechanical safety surface. Loosening = integrity loss.
3. The three agents' `permission: deny edit/bash` — the read-only-isolation property is the reason they exist.
4. `SARA_GOLDEN_TASKS.md` and the golden-result storage pipeline — evaluation ground truth.
5. The Decision Ladder and autonomous/review/approval doctrine in AGENTS.md.
6. `memory/sara.md` — continuity source (edit/append, never simplify away content).
7. The committed `sara-docs` history (daf7c71) — no history rewrite.
8. `test/sara-plugin.test.mjs` — the only automated regression net Sara owns.

---

# 27. Final Recommendation

1. **Is Sara actually over-engineered?** **No**, not in the runtime — the live mechanism is small (52-line plugin + policy + 3 agents + 4 commands). It is **under-organized**: doctrine duplicated across 7 files, one broken skill, 3 inert persistence sinks, and a sprawling docs set.
2. **Where is the biggest architectural mess?** The **duplicated decision/review doctrine** (schema + tier ladder + taxonomy living in multiple files) — highest drift potential because no single file is authoritative. Second: the broken `read-terminals` path.
3. **What should be merged?** `sara-debt` → `auditor`; SYSTEM_MAP/FINAL_REPORT/BASELINE/CANDIDATES → one live architecture doc + archive; decision-block (command/agent) → one artifact; tier ladder → AGENTS.md table.
4. **What should be separated?** Generated state (`state/`) from config (already true) and *policy* (decision-block, taxonomy, tiers) from *prompts* (command/agent mission prose); docs into `live/` vs `archive/`.
5. **What should be moved?** `.bak` rollback files → an `archive/` (or git history once the config dir gets a repo); `PROGRESS-PHASE-2.md` → ai-swe-engine; machine-specific references out of AGENTS.md and the read-terminals helper → host-neutral resolution.
6. **What should be deleted eventually?** `.gitignore` (or create its implied git repo); `sara-debt` (post-alias); the archived event docs may be deleted after one more round; `java/` test scaffold; `.idea/` via ignore.
7. **What should remain exactly as-is?** §26 list: plugin, permissions, agent read-only modes, golden tasks, decision ladder doctrine, memory, history, plugin tests.
8. **Single highest-value cleanup:** Make `sara-review`'s taxonomy + an extracted decision-block + tier table the three **single sources of truth**, and point every command/agent at them — with conflicts resolved, most other items (audit merge, doc archive, sara-debt removal) become mechanical.
9. **What cleanup should NOT be done?** Removing any of the three agents, merging plugin into commands, rewriting AGENTS.md from scratch, deleting golden/result history, "touching up" the vendored ponytail tree, or version-controlling `state/`.

Bottom line: **capability set is right; organization is the debt.** All valuable Round-1/2 behavior is preserved by a consolidation pass that deletes almost nothing structural and repairs exactly one broken component.