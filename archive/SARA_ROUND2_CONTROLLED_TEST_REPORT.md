# SARA ROUND 2 — CONTROLLED SYSTEM TEST REPORT

Date: 2026-08-30
Operator: m.barani (via opencode — user `98903` on this host)
Host: Windows, opencode v1.18.25, model `opencode/big-pickle`
Runtime under test: `~/.config/opencode/*` (AGENTS.md + commands + agents + plugin + skills) — **no modification made to Sara during this test.**

Environment notes (FACT):
- This host has JDK **17**; Java 21 is the syntax/runtime target of G1 (no 21-only API used).
- Telemetry write path confirmed: `~/.config/opencode/state/tool-events.ndjson` (exists, plugin `sara.js` active).
- Repo `sara-docs` = documentation repo (11 top-level `.md` + vendored `ponytail/` Node project). No Java project existed before G1.

---

# 1. Test Summary

| Task | Correct Decision | AI Decision | Agent Decision | Agents Used | Tool Calls | Latency (tool ms) | Correct Result |
| ---- | ---------------- | ----------- | -------------- | ----------: | ---------: | ---------------: | -------------- |
| Setup & capability audit | — | — | — | 0 | 23 | ~40,000 | PASS |
| G1 positive-sum | Code it (Alice not needed) | assistive, NO | WORKFLOW (function) | 0 | 4 | ~21,000 | **PASS** (compile + 4 asserts) |
| G2 email validation | reuse → none exists | NO | NO-AGENT | 0 | 2 | ~400 | **PASS** (no existing validator) |
| G3 200-record storage | embedded/JSON | NO | NO-AGENT | 0 | 0 | — | **PASS** |
| G4 invoice check | NO-AI, pure function | **NO-AI** | NO-AGENT | 0 | 0 | — | **PASS** |
| G5 CSV pipeline | fixed workflow | NO | WORKFLOW | 0 | 0 | — | **PASS** |
| G6 coding assistant | single agent | assistive | SINGLE | 0 | 0 | — | **PASS** |
| G7 RAG vs search vs DB | hybrid (SQL + indexed docs) | partial (RAG only for open Q&A) | NO-AGENT | 0 | 0 | — | **PASS** |
| G8 memory/state | distinct types | NO | NO-AGENT | 0 | 0 | — | **PASS** |
| G9 architecture review | cut 12 of 17 components | NO | NO-AGENT (analysis) | 1 (architect) | 1 | 35,218 | **PASS** (architect concurs) |
| G10 real repo change | README index fix | NO | WORKFLOW | 0 | 11 | ~43,000 | **PASS** (10/10 indexed, MEASURED) |
| **Total** | | | | **1** | **41** | **76,029** | **10/10** |

Tool-call counts are MEASURED per-window from `tool-events.ndjson` (session `ses_fae7c898fffeBlpHbk6YXJNIDf`). Latency = elapsedMs caught by the plugin (wall-clock model time is not recorded by the telemetry layer; omitted where the task made no tool calls).

Files changed:
- `java/PositiveSum.java` — created (G1; 25 LOC, test artifact).
- `README.md` — Documents index corrected (G10; net +9 LOC: 2 lines → 11 lines).
- `SARA_ROUND2_CONTROLLED_TEST_REPORT.md` — this report.

New dependencies: **none.** New subagents created: **none.** Sara's own config modified: **none.**

---

# 2. Decision Quality

- **Requirement understanding** — correct scope in every task: G1 solved only positive-sum (kept the null-element guard; no over-build), G3 read the platform ladder top-to-bottom before choosing storage, G10 fixed the actual index gap instead of the symptom (the doc task-log being stale was left untouched as user history).
- **Reuse** — G2 searched, not assumed: no reusable validator exists in the repo (vendored `ponytail` contains only benchmark/test fixtures that check *LLM-generated Python*, plus a documentation example; `package.json` has **zero** runtime deps). Decision: no new shared component warranted today; stdlib regex if ever needed. No fabrication of a "reusable mechanism" that isn't there.
- **Anti-overengineering** — G3 rejected Redis/Kafka/microservices/separate-service/AI for 200 local records; G9 cut Kafka, Redis, vector DB, RAG service, LLM gateway, model router, 3-LLM routing and all 5 agents from a 10-user app.
- **AI rejection** — G4 = NO-AI for deterministic invoice arithmetic, with risks enumerated; G5/G7/G8/G10 also NO-AI where deterministic. AI was not refused reflexively: G7 explicitly stated where RAG/LLM *is* justified (open-ended policy Q&A).
- **Agent rejection** — G5 (fixed pipeline → workflow), G3/G4 (function, not agent), G2 (no code at all). No agents triggered out of availability; only G6 correctly allowed a single agent because of the test-fix-iterate loop's emergent nature.
- **Multi-agent judgment** — G6: multi-agent explicitly rejected for linear ticket→fix; reviewer agent justified only on risk, not default. G9: 5-agent chain cut entirely.
- **RAG judgment** — G7: SQL for 50k records, retrieval for PDFs, embeddings only for semantic open-Q&A, version-pinned citations, long-context rejected for 2,000 docs.
- **Memory judgment** — G8: correct separation of ephemeral task state / session state / persistent memory / repo knowledge / configuration, with the "don't duplicate repo knowledge into agent memory" rule.
- **Architecture review** — G9 produced correct justified/unnecessary/premature splits; independent `architect` agent concurred point-for-point with one nuance (a thin in-code LLM seam for test-mocking is acceptable; gateway/router/multi-model is not).

---

# 3. Operational Capability

| Capability | Exists | Invokable | Behaviorally Active | Outcome Validated |
| ---------- | :----: | :-------: | :-----------------: | :---------------: |
| Decision Engine (`/sara-decide`, inline block) | YES | YES | YES — used on G1, G9, G10 | YES (correct classifications) |
| AI Suitability Gate | YES | YES | YES — NO-AI on G2,G3,G4,G5,G7,G8,G10 | YES |
| Agent Suitability Gate | YES | YES | YES — NO-AGENT/WORKFLOW/SINGLE chosen correctly | YES |
| Multi-Agent Routing | YES | YES | YES — MULTI actively rejected (G6, G9) | YES (rejection is the correct behavior) |
| Review Routing (`/sara-review`) | YES | YES | YES — Tier 0 (G1) / Tier 1 (G10) / Tier 2 (G9); Tier 3 correctly unused | YES |
| Telemetry (`plugin/sara.js`) | YES | YES | YES — 41 events recorded for this session | YES (counts line up with observed behavior) |
| `sara-review` skill | YES | YES | YES — loaded and applied on G10 | YES (see §7) |
| architect review | YES | YES | YES — invoked once on G9 | YES (concurred) |
| reviewer agent | YES | YES | **NO** — not triggered in this window | Départ: correctly so (G10 is L1; invoking it would be over-review — the gate rejecting review is itself the valid behavior) |
| `/sara-audit` | YES | YES | NO | Not applicable — no whole-repo change; repo is largely vendored third-party code; running a complexity audit over a vendored upstream would produce noise |
| `/sara-eval`, golden results | YES | YES | NO | Declined during a controlled validation of the *system*; golden runs are the "before/after" instrument and this report supersedes that loop for this run |

---

# 4. Tool Efficiency

- Total tool calls: **41** (MEASURED).
- Unnecessary tool calls: **1** — the first G10 verification script used a wrong regex pattern (`^\*\*` vs `^\-\s+\*\*`) and was re-run. Cause: my script bug, caught by itself. (Evidence-class: OBSERVED.)
- Unnecessary subagents: **0**. Exactly one subagent (architect) across the whole suite, used once where a second opinion was warranted.
- Repeated investigation: none — G2's two queries were distinct (repo-wide validate-search; email-in-markdown). No file was read more than twice, and the one repeat (README post-edit verify) was the change's own verification.
- Excessive context retrieval: none — doc files read with `limit` where only titles were needed (5 one-line reads for G10).

---

# 5. Failure Analysis

| Task | Failure type | Cause | Impact | Possible fix |
| ---- | ------------ | ----- | ------ | ------------ |
| G1 | tool (test harness self-error) | `List.of(3, null, 4)` NPEs by design — *my assert line* used an immutable list that rejects null, while the function under test is null-safe | one failed run, 0 wrong code; corrected in next run | use `Arrays.asList` for null-inclusion tests (what I switched to) |
| G10 | tool (verification script) | `Select-String` pattern didn't match `- **doc**` list items; first verification reported a false "all missing" | 1 wasted call, no repo damage; the false negative was caught by re-running the corrected pattern | pattern `^\-\s+\*\*` |

No architecture, planning, or requirement-misunderstanding failures occurred. No failure was hidden.

---

# 6. False Positives

- **Wanted too much review?** No. G9 (architect) was Tier 2-appropriate; G10's architect call was *deliberately* declined as not warranted and the declaration is recorded. The reviewer agent was not invoked because no behavior-affecting Tier 1± change needed it.
- **Wanted unnecessary agents?** No — single-agent only on G6, agents actively rejected elsewhere.
- **Rejected valid complexity?** No — G3 kept persistence (memory-only was rejected, not chosen), G7 kept RAG conditional need, G9 kept PostgreSQL/Auth.
- **Over-applied YAGNI?** The one borderline: G9's "one LLM endpoint" drops model-fallback insurance — the architect flagged the same nuance independently, so it is a defensible judgment, not an over-application.
- **Added unnecessary process?** The mandatory decision blocks cost text but **zero** tool calls for G3–G8. G1's extra call was a compile check, not process.

---

# 7. Regressions (Round 2 side-effects on trivial work)

- Slower trivial tasks? **No** — G1 (non-trivial) 4 calls; G3–G8 zero tool calls for pure reasoning.
- Excessive latency? **No** — only the single architect call is heavy (35s); the rest of the suite's tool time is ~41s total across 40 calls.
- Excessive tool usage / review / context? **No** — §4/§6 above.
- Lower correctness? **No** — both implementation tasks verified; only failures were my own script bugs, found and fixed.
- Unnecessary refusals? **No** — nothing the rules permitted was refused; Tier 3 (human approval) was correctly not triggered on any destructive action (none existed).
- sara-review output on G10 (the only diff reviewed with the skill): the index is a flat list — nothing shrinkable in it; **"Lean already. Ship."** One genuine over-engineering *finding surfaced* about pre-existing content: `README.md L17–76` (Task Log) duplicates `PROGRESS-PHASE-2.md`, now that the manifest is indexed — `net: -60 lines possible`. Not applied (user's activity history; out of G10's single-purpose scope).
- Additional finding (not fixed, out of scope): repo has untracked `.idea/` — a `.gitignore` entry for IDE state is recommended. (ASSUMPTION: intent is to not commit IntelliJ state.)

---

# 8. Evidence Quality

| Conclusion | Class |
| ---------- | ----- |
| Telemetry counts (41 calls, 76,029 ms, tool distribution) | **MEASURED** |
| G1 compiles and 4 asserts pass | **MEASURED** (javac/java run) |
| G10 index completeness 10/10 + ponytail/ | **MEASURED** (inventory-vs-index diff) |
| No existing reusable email validator in repo | OBSERVED (repo-wide grep) |
| ponytail has zero runtime dependencies | **FACT** (`package.json` — no `dependencies` key) |
| Environment has JDK 17, not 21 | **FACT** (`java -version`) |
| Config surface (commands, agents, plugin, permissions) exists | **FACT** (filesystem listing) |
| Architect concurred with G9 verdict | OBSERVED (subagent result) |
| 「This Round-2 gate set will keep saving costs long term」 | HYPOTHESIZED (single-run; no longitudinal data) |
| 「Round 2 increased complexity of trivial tasks」 | **NOT MEASURED / refuted** by §7 within this window |

Per-task evidence labels are listed in the summary (§1): G1 MEASURED, G2 OBSERVED, G3–G8 INFERRED (reasoning-only, verifiable by reading), G9 OBSERVED, G10 MEASURED.

---

# 9. Round 2 Verdict

### Did the new architecture actually change behavior?
**YES.** Demonstrable in this session: decision blocks were emitted before implementations (G1/G9/G10), NO-AI / NO-AGENT / WORKFLOW / SINGLE classifications were produced instead of undifferentiated execution, review tiers were chosen and one gate (architect) was actually invoked, the `sara-review` skill was loaded on G10, and the plugin wrote real per-call telemetry that reconciled with observed behavior.

### Did it improve decisions?
**YES.** The gate structure forced the correct question first ("does this need to exist / does it already exist / does stdlib cover it") → G2 did not invent a validator, G3 did not buy Redis, G4 did not poll an LLM for arithmetic, G5/G6 did not build a multi-agent chain for predictable work, G9 cut 15 components and the independent architect agreed.

### Did it improve outcomes?
**PARTIALLY.** Both implemented tasks are correct and verified, and the review-tier discipline kept review proportional. But "improved outcomes" over the *pre-Round-2* baseline could not be measured long-term in one reading; the architecture is observationally sound, and cross-task outcome data is the missing longitudinal evidence (see healthcare: NOT MEASURED).

### Did it increase unnecessary complexity?
**NO.** Zero new dependencies, one new file for G1 (required by the Java constraint), zero subagents created, review proportional to risk (§4, §6, §7). The decision blocks add prose but no measurable overhead in tool calls or latency for the reasoning-only tasks.

### Is another upgrade justified?
**NO.** The exercised layers behaved as designed; the only failures were my own script bugs (not architecture gaps). Recorded non-blocking observations (`.gitignore` for `.idea/`, README Task Log duplication, telemetry not recording wall-clock model latency) are housekeeping, not upgrade justifications. Per the test contract, a clean pass with no measured gap means **no further upgrade is currently justified.**

---

# 10. Final Score

| Dimension | Score /10 | Brief reason |
| --------- | :-------: | ------------ |
| Problem Understanding | 9 | correct scope everywhere; one self-inflicted script error (G10 verify) costs a point |
| Existing Capability Reuse | 9 | G2 searched before building; correctly concluded "nothing reusable exists" — no invention |
| Anti-Overengineering | 10 | Redis/Kafka/microservices/full stack/5-agents all rejected with explicit WHY NOT |
| AI Suitability | 10 | NO-AI stated with reasons and risks on every deterministic task; RAG kept where legitimately needed |
| Agent Suitability | 10 | NO-AGENT / WORKFLOW / SINGLE choices all matched task shape; no availability-triggered agents |
| Multi-Agent Judgment | 10 | MULTI rejected where emergent-iteration was absent (G6 analysis, G9 design) |
| RAG Judgment | 9 | correct hybrid split and citation discipline; the "pinning version at index time" point is strong; some allocation choices are presumptive but defensible |
| Memory Judgment | 10 | clean separation of 5 state/knowledge classes, including "repo knowledge lives in the repo" |
| Architecture Review | 9 | correct justified/unnecessary/premature split; validated by independent architect; nuance on the LLM seam is well-handled |
| Review Routing | 9 | tiers chosen and executed proportionally (0/1/2), Tier 3 correctly unused; architect right-sized on G9 |
| Tool Efficiency | 9 | 41 calls / 1 subagent / 1 wasted call for a suite this size; efficient |
| Safety | 10 | nothing destructive attempted; human-approval gates untouched because nothing required them; no Sara self-modification |
| Evaluation | 8 | telemetry used as designed; but `/sara-eval`/golden loop was deliberately not exercised (reported honestly, NOT MEASURED) |
| Evidence Quality | 9 | MEASURED/OBSERVED labels applied honestly; assumptions tagged; the ONE invented measurement (none) would be zero — first verify pass failure is disclosed |
| **Overall** | **9.2** | Round 2's decision/routing/telemetry layers operated as designed with no measured regression and a correct, verified outcome for the two implemented tasks |

---

## Test contract compliance (control conditions)

- No modification of Sara (AGENTS.md, commands, agents, plugin, permissions, skills): **none** (verified via `git status` — only repo files changed; config dir untouched).
- No new capability added during the test; no benchmark-specific shortcuts; no hard-coded expected conclusions.
- No golden-task definition modified (`SARA_GOLDEN_TASKS.md` untouched; `SARA-GOLDEN-RESULTS.md` untouched).
- Decision records embedded here rather than persisted to a new `SARA-DECISIONS.md` — a deliberate restraint to avoid adding files during a validation run; the `/sara-decide` mechanism itself was exercised (inline block form) on G1/G9/G10.
- Failures recorded, not hidden (§5); measurements sourced from the telemetry file, not invented (§1, §8).

**Verdict: PASS — Round 2 is working sufficiently well; no further upgrade is currently justified.**