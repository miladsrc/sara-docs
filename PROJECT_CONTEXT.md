# Sara Project Context

## Projects Sara Has Worked On

### 1. ai-swe-engine

**Status:** Phase 2 SoD Design COMPLETE, Increment 1 Implemented (2026-08-26)
**Version:** 0.2.0+
**Tests:** 113+ passing
**Repository:** https://github.com/miladsrc/ai-swe-engine
**Latest commit:** 69c93b9

#### What It Is
An autonomous software engineering engine that:
- Runs fully offline with local LLMs (Ollama/Qwen)
- Implements deterministic governance (gates, audit, identity)
- Requires human approval at critical decision points
- Never depends on Sara at runtime

#### Architecture
- FastAPI + PostgreSQL
- PRD -> US -> AC -> Spec -> AgentRun -> CRP -> MRP -> VCR chain
- Hard gates at each stage
- Deterministic governance, LLM generates content only

#### Phases (Master Plan)
- Phase 0: Foundational agent loop (COMPLETE)
- Phase 1: Governance integrity hardening (COMPLETE)
- Phase 2: Separation of duties (DESIGN COMPLETE, increment 1 done, SASE_SOD_MODE=legacy)
- Phase 3: Semantic memory/Qdrant
- Phase 4: Bounded self-repair/L1 autonomy
- Phase 5: Redis (conditional)
- Phase 6: L2 automation
- Phase 7: L3 delegated engineering
- Phase 8: L4 platform maturity
- Phase 9: Platform UI / Human Operations Layer (DEFERRED)

#### Key Components
- **Verification Module** (agents/verification.py): Tree-hash binding, clean-checkout, orchestrator-owned test/scan/lint
- **Governance Dashboard** (static/ui/, api/routers/dashboard.py): Zero-build vanilla JS, bearer auth
- **Coder Agents**: Python + SpringBoot, propose_only mode for SoD strict
- **Agent Layer**: 8 roles (product, spec, coder, reviewer, reflection, test_runner, springboot_coder, designer)
- **Auth** (api/authn.py, api/routers/auth.py): Token-based login, PBKDF2 200k, /auth/login + /auth/me

#### Key Files
- `agents/orchestrator.py` - Pipeline orchestration (legacy + strict SoD modes)
- `agents/verification.py` - SoD verification steps (tree-hash, test, scan, lint)
- `agents/coder_agent.py` - Python coder (propose_only support)
- `agents/coder_springboot.py` - SpringBoot coder (propose_only support)
- `api/gates.py` - Governance gates
- `api/routers/dashboard.py` - Dashboard API
- `api/security.py` - Auth (require_human_actor, require_authenticated_actor)
- `api/authn.py` - Token authentication (PBKDF2)
- `static/ui/` - Dashboard UI (app.js, index.html, styles.css)
- `docs/MASTER_PLAN.md` - Source of Truth
- `docs/PHASES/PHASE-2.md` - SoD design doc

#### Known Issues
- CRP endpoint can set run.status='blocked' bypassing assert_run_patchable (engine bug)
- MRP open_crp_ids snapshot misses CRPs raised AFTER MRP creation (display stale, safety holds)
- Blueprint table has no API endpoint — must INSERT directly into Postgres

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
