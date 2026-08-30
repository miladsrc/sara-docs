# SARA SELF-UPGRADE ROUND 2 — FINAL REPORT

Version: 2026-08-30 | Agent: Sara | Runtime: opencode 1.18.25, config at `~/.config/opencode`

---

# 1. Executive Summary

Round 2 was an **operational upgrade**, not an instruction dump. Discovery
showed Sara has no process of her own — she is the persona loaded on the
**opencode runtime**, so "runtime changes" means changes to opencode's config
surface: commands, agents, plugin hooks, permissions.

Implemented, as real mechanisms:

- **L4 runtime:** `plugin/sara.js` — `tool.execute.before/after` hooks writing
  per-call telemetry (`~/.config/opencode/state/tool-events.ndjson`).
  Unit-tested (4 tests, node:test).
- **L3 gates:** `/sara-decide` (architecture + AI/agent suitability + review
  tier, persists `SARA-DECISIONS.md`), `/sara-review`, `/sara-audit`, `/sara-eval`.
- **L3/L4 routing:** three role subagents — `architect`, `reviewer`, `auditor`
  (all deny-edit/deny-bash).
- **L4 autonomy:** `permission` rules gate destructive bash in `opencode.jsonc`.
- **L3 evaluation loop:** `SARA_GOLDEN_TASKS.md` (10 tasks), `SARA-GOLDEN-RESULTS.md`
  (first honest record: G5 demo, deterministic route, 0 AI, 0 agents, 3 tool calls).
- **L1 wiring:** AGENTS.md gained an "Operational Gates" section that binds the
  above into Sara's intake/review/autonomy behavior.

Deliberately **not** built: model routing, RAG, memory service, benchmark
infrastructure, LLM judges, mode system, subagent propagation. Rejected or
deferred with reasons (§26, §27). No framework, service, or database was added.

# 2. What Sara Actually Was Before Round 2

- One persona file (`AGENTS.md`, 96 lines), 3 skills, 1 manual memory file, a
  minimal `opencode.jsonc` ($schema only).
- No operational gates, no task classification, no routing, no review tiers, no
  evidence records, no telemetry, no evaluation, no failure taxonomy.
- Subagents were only opencode built-ins (`build/plan/general/explore`).
- v2 governed runtime was not present on this host (verified: paths absent,
  port 8800 down) — the Gateway was therefore **bypassed** for this upgrade,
  disclosed per AGENTS.md fallback rule.

# 3. Self Boundary

Documented in `SARA_SELF_BOUNDARY.md`. Sara-mutable = `~/.config/opencode/**`
(own config/skills/agents/commands/plugin/state/memory) + the `sara-docs` repo.
Protected: project code, user configuration, supporting infrastructure (opencode
itself), nested `ponytail/` reference repo.

# 4. Round 1 Limitations

Round 1 (Ponytail adoption) was classified through the change taxonomy:

| Change | Instruction? | Skill? | Workflow? | Runtime? | Measured? |
|--------|:---:|:---:|:---:|:---:|:---:|
| Decision Ladder (AGENTS.md) | YES | — | — | — | — |
| Self-review checklist (AGENTS.md) | YES | — | — | — | — |
| `sara:` convention (AGENTS.md) | YES | — | — | — | — |
| `sara-review` skill | — | YES | — | — | — |
| `sara-debt` skill | — | YES | — | — | — |

**Where it stopped:** Round 1 never left L1/L2. Nothing was invokable, nothing
routed, nothing recorded, nothing measured. A "prompt change" was honestly
reported (Round 1 report's own "Evaluation: NOT MEASURED" and "Runtime: no
changes" confirm this).

# 5. Architecture Gaps

1. No task classification → every task on the same path.
2. No decision gate → architecture choices made implicitly and forgotten.
3. No review routing → no risk-proportional verification.
4. No role separation in subagents → single generic delegation.
5. No evidence/decision persistence → facts and assumptions blur.
6. No tool telemetry → redundant reads/searches invisible.
7. No evaluation → improvement can't be shown or regressions caught.
8. No mechanical autonomy control → destructive ops rely on behavior alone.

# 6. Upgrade Candidates

Full matrix in `SARA_UPGRADE_CANDIDATES.md`.
Decisions: 6 IMPLEMENT, 4 ADAPT, 1 CONFIGURE, 4 REJECT, 1 DEFER-implied. The
three "engines" (architecture / AI suitability / agent suitability) were merged
into **one** decision gate to honor the simplicity principle.

# 7. Changes Actually Implemented

| # | Change | Layer | Purpose | Location | Validation |
|---|--------|-------|---------|----------|------------|
| 1 | `sara.js` plugin | L4 | tool telemetry (call, latency, output size, args) → NDJSON | `~/.config/opencode/plugin/sara.js` | 4 passing node:test tests |
| 2 | `architect` agent | L3/L4 | architecture + AI/agent suitability decision pass, deny-edit | `~/.config/opencode/agent/architect.md` | file present, frontmatter valid |
| 3 | `reviewer` agent | L3/L4 | correctness+security+complexity counterparty review, deny-edit | `~/.config/opencode/agent/reviewer.md` | file present |
| 4 | `auditor` agent | L3/L4 | whole-repo complexity/debt scan, deny-edit | `~/.config/opencode/agent/auditor.md` | file present |
| 5 | `/sara-decide` | L3 | decision gate; persists `SARA-DECISIONS.md` | `~/.config/opencode/command/sara-decide.md` | command loads (restart) |
| 6 | `/sara-review` | L3 | tier-based review routing | `~/.config/opencode/command/sara-review.md` | command loads (restart) |
| 7 | `/sara-audit` | L3 | whole-repo audit → `SARA-AUDIT.md` | `~/.config/opencode/command/sara-audit.md` | command loads (restart) |
| 8 | `/sara-eval` | L3 | golden-task harness → `SARA-GOLDEN-RESULTS.md` | `~/.config/opencode/command/sara-eval.md` | command loads (restart) |
| 9 | `permission` rules | L4 | human-approval gates on destructive bash | `opencode.jsonc` | schema-valid fields |
| 10 | AGENTS.md "Operational Gates" | L1 | binds 1–9 into behavior | `~/.config/opencode/AGENTS.md` | read-back |
| 11 | Golden set + results | L3 | evaluation substrate | `sara-docs/SARA_GOLDEN_TASKS.md`, `SARA-GOLDEN-RESULTS.md` | G5 demo run |

**Trigger / input / output** per change: commands trigger on user invocation
(`$ARGUMENTS` in); agents trigger via `task` delegation (decision block / review
findings / audit report out); plugin triggers on every tool execution (NDJSON
records out); permission rules trigger on matching bash commands (ask dialog
out). Trade-offs and risks are in each section below.

# 8. Runtime Changes

Mandatory section.

**Actual runtime files added:**
- `~/.config/opencode/plugin/sara.js` — executable hook code (L4).
- `~/.config/opencode/command/*.md` (4) — invokable workflow prompts (L3).
- `~/.config/opencode/agent/*.md` (3) — routed subagent roles (L3/L4).

**Runtime files modified:**
- `~/.config/opencode/opencode.jsonc` — `"plugin"` registration + `permission`.
- `~/.config/opencode/package.json` — added `"type": "module"` (so the plugin
  module-portability is unambiguous).
- `~/.config/opencode/AGENTS.md` — instruction-layer wiring (L1, not runtime).

**Workflow changes:** task intake now passes through `/sara-decide` for
non-trivial work; review happens by tier (skill/self/subagent/human);
whole-repo and eval are first-class invokable workflows.

**Orchestration changes:** delegation is now role-based (`architect`,
`reviewer`, `auditor`) instead of only generic `explore`/`general`.

**These are real L3/L4 changes** — not a prompt claim. The plugin is tested
executable code; permissions and routing are runtime-enforced mechanisms.

# 9. Skill / Instruction Changes

Separated from runtime:
- Skills: **unchanged**. `sara-review` and `sara-debt` are now *consumed* by the
  reviewer/auditor agents and the `/sara-review` router — reuse, no new skills.
- Instructions: AGENTS.md grew +~30 lines ("Operational Gates"). No new
  speculative instructions; this section only points at real mechanisms.

# 10. Architecture Decision Engine

Implemented as `/sara-decide`: a required classification pass before non-trivial
implementation. Produces and **persists** a structured decision record:
Context / Facts / Assumptions / Options / Chosen / Rejected / Reason / Risks /
Class (Task/AI/Agent/Complexity/Tier) / Confidence / Revisit Trigger / Evidence.
Tier 2+ routes a second opinion to the `architect` agent. Capability report:
L1 YES · L2 YES · L3 YES (default for non-trivial tasks) · L4 NOT-MEASURED.

# 11. AI Suitability Engine

**No AI where a deterministic mechanism suffices.** Folded into `/sara-decide`
as the `AI Needed` decision. Decision inputs (documented): determinism,
ambiguity, error cost, latency, privacy, explainability, frequency. Demonstrated
live on G5 (deterministic CSV compare → AI Needed: NO). L1–L3 YES, L4 NOT-MEASURED.

# 12. Agent Suitability Engine

**No agent where a workflow or function suffices.** `Agent Needed` decision in
`/sara-decide` with inputs: multi-step, dynamic planning, tool interaction,
iterative correction, environment interaction, state, uncertainty. Demonstrated
on G5 (Agent Needed: NO). L1–L3 YES, L4 NOT-MEASURED.

# 13. Multi-Agent Routing

Three roles added — `architect`, `reviewer`, `auditor`. Each has a defined
responsibility, input, output, trigger, authority (read-only, deny edit/bash),
and failure condition (weak/un-anchored findings are dropped by Sara). These
were the only roles with real separation of responsibility; researcher =
existing `explore`, implementer/planner = existing primary agent. No role added
for theater. L1–L3 YES, L4 NOT-MEASURED.

# 14. Review Routing

Tiers 0–3 operationalized: 0 no pass · 1 self-review checklist · 2 +`architect`
second opinion · 3 +`reviewer` and human approval. `/sara-review` routes by
risk: complexity→`sara-review` skill; correctness/security→`reviewer` agent;
repo-wide→`/sara-audit`. L1–L3 YES, L4 NOT-MEASURED.

# 15. Evaluation

Minimum useful loop, no benchmark infra: fix telemetry culprit behind
measurement (`tool-events.ndjson`), golden tasks (`SARA_GOLDEN_TASKS.md`,
10 tasks across the required classes), results file with evidence labels,
failure taxonomy. Metrics captured only if actually measurable (tool calls,
iterations, files, LOC, deps, correctness). L1–L3 YES, L4 starts with the G5
entry (measurement methodology live from next restart).

# 16. Golden Tasks

10 tasks (G1–G10) covering: trivial coding, existing-code reuse,
over-engineering temptation, architecture choice, AI-vs-non-AI,
agent-vs-workflow, single-vs-multi-agent, RAG-vs-no-RAG, debugging, repo
modification. Anti-gaming: no expected outputs hard-coded; tasks run in throwaway
temp dirs.

# 17. Failure Classification

Taxonomy (requirement-misunderstanding / planning / architecture / model / tool /
context / orchestration / subagent / verification / evaluation) is bound into
`/sara-eval` output and the AGENTS.md evaluation rule — every failed golden run
must be classified, feeding the revisit triggers in decision records.

# 18. Tool Efficiency

L4 telemetry added (the measurement precondition): per-call `tool`, `sessionID`,
`elapsedMs`, `outputLen`, args summary (paths/patterns) → NDJSON.
This makes redundant reads/searches and unnecessary tool calls detectable.
**Enforcement heuristics were deliberately deferred** — optimize for minimum
sufficient work, not raw count, and that judgment needs data first.

# 19. Model Routing

**REJECTED for this host.** One provider, one model, no small_model, no task
classes varied enough to justify routing. Adding `small_model` or per-agent
models now would be config theater. Revisit trigger: a second model/provider
becomes available or summarization/classification cost becomes material.

# 20. Memory Decisions

Per-level conclusion:
- Conversation/session — handled by opencode's message store (not ours).
- Task state — decision records + telemetry (`SARA-DECISIONS.md`,
  `tool-events.ndjson`).
- Persistent preferences — `memory/sara.md` stays (lean, manual).
- Semantic/episodic memory, vector store — **REJECTED**. No problem was shown
  that grep + records + flat files cannot solve more reliably.

# 21. RAG Decisions

**REJECTED.** Retrieval needs today are satisfied by `grep`/`glob`/file reads /
`webfetch`/`websearch` — all already in the tool set. A RAG layer would serve
zero demonstrated queries. Documented in the decision schema under
`Revisit Trigger`: "large on-disk corpus queried ad hoc at scale."

# 22. Human Control

Two layers:
- Mechanical: `permission` `ask` gates on `git push*`, `git reset --hard *`,
  `git clean -fd *`, `rm -rf *`, `docker compose down -v *`, `dropdb *`.
- Behavioral: documented tiers — autonomous (reads/analysis/normal edits),
  review required (tier 2+), approval required (destructive, credentials,
  irreversible, deploy, production). A `deny` is always honored.

# 23. Before vs After

Actual evidence this session:

| Area | Before | After | Evidence |
|------|--------|-------|----------|
| Tool telemetry | none | L4 hook, NDJSON | 4 tests pass; fires on every tool execution (from restart) |
| Decision gate | none | `/sara-decide` + persisted records | command exists; schema in AGENTS.md |
| Subagent roles | 2 generic | 3 specialized + 2 generic | agent files present |
| Eval | none | golden set + result record | G5 demo: deterministic, 0 AI/agent, IDENTICAL+DIFFERENT correct |
| Autonomy | behavior-only | `permission` asks | opencode.jsonc rules |

Do not fabricate: L5-style *before/after* numbers for arbitrary tasks are
**NOT-MEASURED** — telemetry starts recording at next restart, so the first
real before/after comparison is the next `/sara-eval` run after restart.

# 24. Regression Analysis

Checked for the classic regressions:
- Latency: plugin adds one sync file append per tool call — sub-ms, wrapped in
  try/catch; no session breakage (test proves invalid-path never throws).
- Context: AGENTS.md +~30 lines; commands/agents are on-demand, not permanent.
- Tool calls: no new forced calls; the decision gate can add one command before
  heavy work, and saves calls by avoiding wrong-route work.
- Trivial tasks: tier 0 exempts them from review; `/sara-decide` is for
  non-trivial intake only, not every keystroke.
- Over-minimization / refusals: no new refusal logic.
- Risk: **permission `ask`** is the main behavior change — it can add prompts on
  destructive commands. Mitigation: patterns are narrowly destructive-scoped.

# 25. Complexity Cost

| Cost | Value |
|------|-------|
| Context increase (AGENTS.md) | +~30 lines (L1 entry points only) |
| Runtime overhead | sub-ms append per tool call |
| New dependencies | 0 (uses existing `@opencode-ai/plugin`, node stdlib) |
| New components | 1 plugin + 4 commands + 3 agents = 8 small files |
| New code (executable) | ~90 lines plugin + ~45 lines test |
| New operational burden | restart to activate; self-review gates on bigger tasks |

# 26. Rejected Improvements

Model routing · RAG · semantic/vector memory · benchmark/LLM-judge infra ·
mode intensity system · subagent propagation hooks · 20-platform adapters ·
uninstall system · custom task-tracking service. Each rejected in the section
that covers it or in `SARA_UPGRADE_CANDIDATES.md` — no framework where a
command/agent/permission suffices.

# 27. Deferred Improvements

- Tool-efficiency **enforcement** (after ≥1 full session of telemetry data).
- Whole-repo audit record for sara's own repo (needs `/sara-audit` after restart).
- Model routing (only if a second model/provider appears).
- Counterparty review for everyday tier-1 changes (currently self-review only).

# 28. Known Limitations

- Config not hot-reloaded → everything activates on next opencode restart.
- `permission` pattern-match semantics are best-effort (specific patterns; no
  catch-all) — verified to be schema-valid, behavioral verification pending.
- Plugin telemetry only knows tool calls, not decision *quality*.
- v2 Gateway is not present on this host; the D4 fallback disclosure applies to
  all Level 1+ actions performed here.
- No L4 measurement yet — honest floor for §30 scores.

# 29. Evidence Quality

| Claim | Quality |
|-------|---------|
| opencode v1.18.25; runtime surface | MEASURED |
| v2 host absent, port 8800 down | MEASURED |
| plugin passes 4 unit tests | MEASURED |
| G5 deterministic + correct on both cases | MEASURED |
| G5 tool calls = 3, 0 deps | OBSERVED (transcript count; telemetry from restart) |
| Runtime changes above work end-to-end | INFERRED (config valid; hooks tested; full run pending restart) |
| L5 improvement vs Round 1 | NOT-MEASURED (first real comparison after restart) |

# 30. Final Score

| Dimension | Score /10 | Why |
|-----------|:---:|-----|
| Requirement Analysis | 8 | Baseline/gap work was evidence-driven, not speculative |
| Architecture Reasoning | 8 | Right sized to a config-surface runtime; merged 3 engines into 1 |
| AI Suitability | 7 | Operationalized as a gated decision; demonstrated on G5 |
| Agent Suitability | 7 | Same gate; does not spawn agents for workflows |
| Multi-Agent Decisions | 7 | 3 justified roles; refused role theater |
| RAG Decisions | 8 | Correctly rejected with a documented trigger |
| Memory Decisions | 8 | Kept flat files; refused a memory service |
| Model Selection | 6 | Single-model honesty; routing refused as theater |
| Task Routing | 6 | `/sara-decide` gate; not yet observed in long-run use |
| Orchestration | 6 | Role-based delegation added; process maturity pending |
| Self-Review | 8 | Checklist + tier 0 exemption; low overhead design |
| Architecture Review | 7 | `architect` second opinion for tier 2+ |
| Technical Debt | 7 | `sara:` + ledger + auditor agent now mechanical paths |
| Evaluation | 6 | Loop exists and recorded G5; measurement needs a compiled session |
| Failure Analysis | 6 | Taxonomy bound into eval records; no failures occurred to classify |
| Tool Efficiency | 6 | Telemetry L4 in place; enforcement correctly deferred for data |
| Autonomy Control | 8 | Mechanical `permission` gates + documented approval tiers |
| **Overall** | **7/10** | Round 1 → instructions; Round 2 → working gates, routing, telemetry, eval. Ceiling set by unmeasured long-run behavior. |

---

# WHAT ACTUALLY CHANGED IN SARA

## 1. INSTRUCTIONS
- AGENTS.md "Operational Gates": intake must classify, review by tier,
  autonomy levels, eval/failure rules. Why: bind the new mechanisms into
  behavior. Where: `~/.config/opencode/AGENTS.md`. Evidence: read-back.
  Validation: L1 (needs restarted session to be behaviorally active).

## 2. SKILLS
- None added. `sara-review` / `sara-debt` now consumed by the routers.
  Why: reuse over creation (Round 1 already built them).

## 3. WORKFLOWS
- `/sara-decide` (decision gate, persists records) · `/sara-review`
  (tier routing) · `/sara-audit` (repo scan) · `/sara-eval` (golden harness).
  Why: convert instructions into invokable operational steps.
  Where: `~/.config/opencode/command/*.md`. Evidence: files present; behavior
  active next restart. Validation: L3 installed (invokable), active pending restart.

## 4. RUNTIME
- `plugin/sara.js` — real hook code logging every tool execution to
  `state/tool-events.ndjson` (tool, latency, output size, args). Why: telemetry
  is the precondition for tool-efficiency and evaluation.
  Evidence: 4 unit tests pass (node:test). Validation: L4, tested; live from restart.
- `permission` gates in `opencode.jsonc` for destructive bash (`git push*`,
  `rm -rf *`, `docker compose down -v *`, …). Why: mechanical human control.
  Evidence: schema-valid. Validation: L4 installed; behavior verified on restart.
- 3 subagent roles (`architect` / `reviewer` / `auditor`), deny-edit/deny-bash.
  Evidence: agent files present. Validation: L3 installed.

## 5. MEASURED
- Plugin: 4/4 tests pass. G5 demo: deterministic route chosen, 0 AI, 0 agents,
  0 deps, 3 tool calls, correct on both cases. Evidence: test output + results file.
  Validation: L4 measured for the plugin; L5 for G5 is OBSERVED (telemetry
  consistency from next restart).

---

# FINAL TRUTH CHECK

### Q1. Did I only change prompts?
**No.** Commands/agents are more than prompts (routing + permission surface),
and `plugin/sara.js` is executable runtime code.

### Q2. Did I only create skills?
**No.** No skills added; added commands, agents, a plugin, and permissions.

### Q3. Did I modify workflow/orchestration?
**Yes.** Tiered review routing, role-based delegation, intake decision gate,
eval/audit/decision workflows.

### Q4. Did I modify actual Sara runtime code?
**Yes (bounded).** The plugin is runtime hook code; `opencode.jsonc` runtime
settings (plugin registration + permissions) changed; 8 runtime surface files
added; AGENTS.md/package.json touched for wiring/module-type.

### Q5. Did I run an experiment?
**Yes.** G5 golden run (live) and 4 plugin unit tests.

### Q6. Did behavior actually change?
**Not yet observable in the long run** — opencode loads config at start; the
behavioral changes activate on the next restart. The plugin's hook invocation is
the only immediately-live piece, and it was verified in isolation.

### Q7. Did outcomes improve?
**OBSERVED on G5**, generalizable answer pending compiled sessions.

### Q8. What evidence proves the improvement?
Test results (MEASURED), G5 results record (MEASURED/OBSERVED), config
validation, baseline vs after documents. Telemetry NDJSON starts providing
continuous evidence at next restart.

### Q9. What became worse?
- +~30 lines permanent context in AGENTS.md.
- Possible extra user prompts on destructive commands (permission `ask`).
- One extra step (decision gate) for non-trivial intake.
- Restart required to activate.

### Q10. What would be the next highest-value upgrade?
After a restart, run `/sara-eval` on G1–G10 to produce the first **telemetry**-
backed baseline; then use that data to enable **tool-efficiency enforcement**
(flag redundant reads/searches) and, if a second model appears, model routing.
That targets the current ceiling: L5 measurement of real behavior.

---

## Activation

Quit and restart opencode for the config (plugin, permissions, commands,
agents) to load. Backups: `opencode.jsonc.bak-20260830`, `AGENTS.md.bak-20260830`.
Rollback = restore those two files and delete the added `plugin/`, `command/`,
`agent/`, `test/` folders plus the sara-docs Round 2 docs if unwanted.