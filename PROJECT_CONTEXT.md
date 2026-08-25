# Sara Project Context

## Projects Sara Has Worked On

### 1. ai-swe-engine

**Status:** Phase 1 Complete (2026-08-25)
**Version:** 0.2.0
**Tests:** 61 passing
**Repository:** https://github.com/miladsrc/ai-swe-engine

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
- Phase 2: Separation of duties (NEXT)
- Phase 3: Semantic memory/Qdrant
- Phase 4: Bounded self-repair/L1 autonomy
- Phase 5: Redis (conditional)
- Phase 6: L2 automation
- Phase 7: L3 delegated engineering
- Phase 8: L4 platform maturity

#### Key Files
- `api/gates.py` - Governance gates
- `api/routers/crp.py` - CRP endpoint (Bug 1 fixed)
- `api/routers/evidence.py` - Evidence export endpoint
- `api/schemas.py` - Pydantic schemas
- `tests/test_gates_unit.py` - Gate tests
- `docs/MASTER_PLAN.md` - Source of Truth

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

#### Key Components
- `api/main.py` - FastAPI application
- `api/graph.py` - LangGraph workflow
- `api/gateway.py` - Gateway controller
- `api/policy.py` - Policy engine
- `api/approval.py` - Approval store
- `api/audit.py` - Audit trail
- `api/memory.py` - Memory manager

---

### 3. todo-cli

**Status:** Example project (2026-08-24)
**Built by:** ai-swe-engine agents
**Repository:** IdeaProjects\todo-cli

#### What It Is
An example project built by the ai-swe-engine agent layer to demonstrate the full offline dev flow.

#### Key Features
- Built by agent:coder using qwen2.5-coder:7b
- 4 reflection iterations
- Real pytest tests
- CLI actually works (add/list/--priority/TODO_STORE)

---

### 4. game-agent

**Status:** Completed (2026-08-23)
**Repository:** IdeaProjects\game-agent

#### What It Is
A Chrome Dino game agent upgraded from vision-only to perfect-information "direct" mode.

#### Key Achievements
- Score 867 -> ~2400 consistent
- Deterministic ceiling at score ~2377
- User declined further tuning ("merge them, it won't get better")

---

## Projects Sara Has Referenced

### Sahba Repos
- gitlab.sidg.ir/msg/sahba/sahba-backend/...
- Java microservices platform for organizational access management
- OBS/CBAC, Spring Boot 2.5.6, PostgreSQL, Eureka, Hazelcast, RabbitMQ

### cvat_mlops
- 192.168.236.22
- MLOps related project
