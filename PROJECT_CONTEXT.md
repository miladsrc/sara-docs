# Sara Project Context

## Projects Sara Has Worked On

### 1. ai-swe-engine

**Status:** Phase 2 SoD largely implemented and pushed (2026-09-05)
**Version:** 0.2.0+
**Tests:** 158 passing (non-live), 3 skipped, 6 deselected
**Repository:** https://github.com/miladsrc/ai-swe-engine
**Latest commit:** d2f6703
**Mode:** SASE_SOD_MODE=strict (live + docker-compose)

#### What It Is
An autonomous software engineering engine that:
- Runs fully offline with local LLMs (Ollama/Qwen)
- Implements deterministic governance (gates, audit, identity)
- Requires human approval at critical decision points
- Never depends on Sara at runtime
- Enforces Separation of Duties via independent subprocesses (Coder ≠ Verifier ≠ Reviewer ≠ Human)

#### Architecture
- FastAPI + PostgreSQL
- PRD -> US -> AC -> Spec -> AgentRun -> CRP -> MRP -> VCR chain
- Hard gates at each stage (incl. SoD gates G7 verifier tree-hash binding, G8 reviewer ownership)
- Deterministic governance, LLM generates content only
- Agents communicate ONLY through the engine API + git (never point-to-point) — proven live by scripts/trace_coder_verifier.py

#### Phases (Master Plan)
- Phase 0: Foundational agent loop (COMPLETE)
- Phase 1: Governance integrity hardening (COMPLETE)
- Phase 2: Separation of duties (mostly IMPLEMENTED: verification module, verifier subprocess, reviewer G8, G7 gate, offline workflow; genuine remote boundary BLOCKED)
- Phase 3: Semantic memory/Qdrant
- Phase 4: Bounded self-repair/L1 autonomy
- Phase 5: Redis (conditional)
- Phase 6: L2 automation
- Phase 7: L3 delegated engineering
- Phase 8: L4 platform maturity
- Phase 9: Platform UI / Human Operations Layer (DEFERRED)

#### Key Components
- **Independent Verifier subprocess** (agents/verifier.py): role ci:verifier, own token (SASE_VERIFIER_TOKEN), claims verification requests, clean-checkout verification, authoritative tree hash — orchestrator never holds verifier credentials
- **Independent Reviewer agent** (agents/reviewer.py, agents/critic.py): role agent:reviewer, PATCH /mrps/{id}/review, drives gate G8
- **Verification requests** (api/routers/verification_requests.py): immutable envelopes (run/mrp/commit/worktree), atomic claim, fail-closed TTL
- **SoD gates** (api/gates.py): G7 (verifier-owned evidence tree hash == MRP.verified_tree_hash), G8 (reviewer-owned completed review)
- **Offline workflow runner** (scripts/offline_runner.py): host FastAPI on :8899, Blueprint -> PRD->…->artifact, artifact download
- **Verification Module** (agents/verification.py): tree-hash binding, clean-checkout, test/scan/lint steps
- **Governance Dashboard** (static/ui/, api/routers/dashboard.py): zero-build vanilla JS, bearer auth, SoD validation view
- **Coder Agents**: Python + SpringBoot, propose_only mode in strict SoD
- **Agent Layer**: product, spec, coder, reviewer, critic, verifier, test_runner, springboot_coder, designer, orchestrator
- **Auth** (api/authn.py, api/routers/auth.py): token-based login, PBKDF2 200k; strict CI/verifier/reviewer actor checks
- **Comms trace**: SASE_ENGINE_TRACE=1 opt-in [comms] tracing in EngineClient (never logs headers/tokens)

#### Key Files
- `agents/orchestrator.py` - Pipeline orchestrator + `_sod_verify_and_package` (SoD coordinator)
- `agents/verifier.py` - Independent verifier subprocess (--claim runner mode + stdin mode)
- `agents/reviewer.py` / `agents/critic.py` - G8 reviewer + reflection/critic boundaries
- `agents/verification.py` - verification steps (tree-hash, clean-checkout, test, scan, lint)
- `agents/scanner.py` - neutral security scanner
- `agents/coder_agent.py` - Python coder (propose_only, deterministic PR numbers)
- `agents/coder_springboot.py` - SpringBoot coder
- `agents/engine_client.py` - API client (role allowlists w/ wildcard policy, comms trace)
- `api/gates.py` - Governance gates (incl. G7/G8)
- `api/routers/verification_requests.py` - verification request lifecycle
- `api/routers/review.py` - reviewer PATCH endpoint
- `api/security.py` - actor auth (human/CI/verifier/reviewer)
- `scripts/trace_coder_verifier.py` - LIVE Coder↔Verifier communication demo
- `scripts/offline_runner.py` - host offline workflow runner
- `static/ui/` - Dashboard UI
- `docs/MASTER_PLAN.md` - Source of Truth
- `docs/ADR/ADR-002-genuine-sod-isolation.md` - real SoD boundary decision + addendum

#### Known Issues
- Genuine remote verifier SoD boundary BLOCKED (needs separately-administered infra outside m.barani control; local harness mechanics proven only — ADR-002 addendum)
- offline_runner invokes reviewer with --offline -> TemplateLLM no review output -> no review PATCH -> G8 never completes (LIVE-blocker for full pipeline demo)
- deepseek-r1:8b times out on CPU-only machine; working models = qwen2.5-coder:7b and qwen2.5:7b
- Codegen quality is the current bottleneck (7b consistently fails its own tests in demo runs — the verifier correctly rejects; proven by comms-trace demo)
- MRP open_crp_ids snapshot misses CRPs raised AFTER MRP creation (display stale, safety holds)
- Blueprint table has no API endpoint — must INSERT directly into Postgres
- Scratch files untracked in workdir: examine_db.py, query_todos*.py, search_*.py, sessions_with_todos.py, offline_runs/, tests/my-blueprint.txt

---

### 2. SARA v2

**Status:** Active (2026-08-24)
**Stack:** Python 3.12, LangGraph, FastAPI, PostgreSQL+pgvector
**API:** http://127.0.0.1:8800
**Repository:** IdeaProjects\sara

#### What It Is
A human-in-the-loop agent with:
- MCP-based tool integration
- Gateway pipeline (classify -> policy -> approval -> execute -> audit)
- Approval levels (L0-L3) with escalation
- PostgreSQL + pgvector for memory

#### Architecture
- Gateway controller handles all requests
- Policy engine classifies actions (L0-L3)
- Approval store tracks pending decisions
- Audit trail logs all actions
- Memory manager handles pgvector storage

#### Trust Boundary
- Sara v1 = interactive front-end (opencode agent)
- Sara v2 = default runtime for Level 1+ actions
- Approver prefix "gateway-controller:" mandatory
- Fallback to direct execution only if stack down + must disclose

---

### 3. todo-cli

**Status:** Example project (2026-08-24)
**Built by:** ai-swe-engine agents
**Repository:** IdeaProjects\todo-cli

An example project built by the ai-swe-engine agent layer to demonstrate the full offline dev flow. Built by agent:coder using qwen2.5-coder:7b, 4 reflection iterations, real pytest tests, CLI actually works.

---

### 4. todo-springboot

**Status:** Example project (2026-08-26)
**Built by:** ai-swe-engine SpringBoot coder agent
**Repository:** IdeaProjects\todo-springboot

Full end-to-end Spring Boot example: auth, chat, calendar/reminders, SPA frontend. 16 tests pass (6 controller + 10 service). Fixed H2 'USER' reserve word bug with @Table(name='users').

---

### 5. demo-map-backend/frontend

**Status:** Map demo (2026-08-26)
**Built by:** ai-swe-engine with SoD strict mode

SpringBoot backend + Angular 17 frontend for location CRUD. Both MRPs green, awaiting human approval.

---

### 6. game-agent

**Status:** Completed (2026-08-23)
**Repository:** IdeaProjects\game-agent

Chrome Dino game agent upgraded from vision-only to perfect-information "direct" mode. Score 867 -> ~2400 consistent.

---

### 7. sara-docs (this repo)

**Status:** Active (2026-08-25)
**Repository:** https://github.com/miladsrc/sara-docs
**Purpose:** Portable knowledge base for Sara

Complete export of Sara's knowledge, identity, memory, and capabilities. Used to load Sara into new environments or restore context after failures.

---

## Projects Sara Has Referenced

### Sahba Repos
- gitlab.sidg.ir/msg/sahba/sahba-backend/...
- Java microservices platform for organizational access management
- OBS/CBAC, Spring Boot 2.5.6, PostgreSQL, Eureka, Hazelcast, RabbitMQ

### cvat_mlops
- 192.168.236.22
- MLOps related project
