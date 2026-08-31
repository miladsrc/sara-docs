# Sara Complete Memory

> **Last Updated:** 2026-08-26
> **Total Entries:** 77 lines
> **Source:** `~/.config/opencode/memory/sara.md`

---

## Standing Rules

- **ARCHITECTURAL PRESERVATION RULE** (2026-08-26, m.barani, CRITICAL): ai-swe-engine core architecture must NOT be changed/replaced/redesigned. Role = identify weaknesses, improve components, strengthen boundaries, improve reliability/security/observability/maintainability incrementally. FORBIDDEN: new architectures, pattern migrations, replacing core components w/o approval, restructuring modules for aesthetics, large frameworks/infra w/o approval, removing working features. Every change must answer: (1) how it preserves current arch, (2) why improvement-not-redesign, (3) what behavior stays unchanged, (4) smallest implementation path. Fundamental limitations -> document + trade-offs + alternatives + WAIT FOR APPROVAL, never implement unilaterally.

---

## Session Log

### 2026-08-23

- Installed Git 2.55 via winget
- Cloned cvat_mlops (192.168.236.22) + 5 Sahba repos (gitlab.sidg.ir) into IdeaProjects
- GitLab password auth rejected on sidg.ir; PAT required
- Credentials used transiently in headers only, never stored

- Attempted IntelliJ config copy from 192.168.200.97 (SMB creds b.soltani, provided by user; never persist)
- Box is Ubuntu/Samba ("develop-System-Product-Name"), only IPC$/print$ exposed, SSH closed
- **BLOCKED:** awaiting user to enable SSH / http.server / manual tarball on that box

- TEMPORARY client registry changes made (elevated) to allow SMB to Samba server
- HKLM LanmanWorkstation Parameters + Policies keys AllowInsecureGuestAuth=1, RequireSecuritySignature=0
- **PENDING REVERT** when user confirms

- User asked to "download gml 3.5", then cancelled ("forget it")

- game-agent project (IdeaProjects\game-agent):
  - Upgraded dino agent from vision-only to perfect-information "direct" mode
  - agent/direct_state.py reads game vars via page.evaluate
  - Exact-physics jump window in decision.py decide_exact
  - Score 867 -> ~2400 consistent
  - Deterministic ceiling at score ~2377 remains (input latency vs difficulty ramp)
  - User declined further tuning ("merge them, it won't get better")
  - Bugs fixed: obstacles-behind-player causing jump spam
  - Blocking duck removed in direct mode (birds can't hit grounded player in this game)

---

### 2026-08-24

- **Built SARA v2** (IdeaProjects\sara):
  - MCP-based human-in-the-loop agent per user mission
  - Stack: Python 3.12, LangGraph, mcp SDK, FastAPI (:8800), Postgres+pgvector
  - Gateway pipeline classify->policy(L0-L3)->approval->execute->audit
  - SECURITY FIXES: approval forgery at L1/L2, unicode homoglyph evasion
  - 31 tests pass

- **ai-swe-engine project** (IdeaProjects\ai-swe-engine):
  - SASE traceability backbone, FastAPI+Postgres
  - PRD->US->AC->Spec->AgentRun->CRP->MRP->VCR chain with hard gates
  - Fixed 4 gaps, added 14 DB-free tests, 18 review findings (4 HIGH)
  - Docker stack UP: postgres:5433, api:8000
  - Fixed TWO latent product bugs (VCR ghost-CRP, missing blueprint_version)
  - Suite 37 passed x2 consecutive runs

- All changes committed as 7 reasoned commits on master
- Auth decision: token login now, OIDC deferred

- Enabled all 4 MCP servers in sara/mcp_layer/servers.yaml
- Installed Docker Desktop 4.87 via winget
- docker compose stack UP: sara-db-1 + sara-app-1, health ok

- E2E approval demo PASSED live
- **SARA V2 IS NOW THE DEFAULT RUNTIME** — v1 routes Level 1+ actions through v2 Gateway

- **read-terminals skill added** (user approved)

- Started REAL project (todo-cli) on ai-swe-engine with separate-agent layer
- Built agents/ package with 6 RolePolicies, 8 new unit tests
- ai-swe-engine pushed to origin = https://github.com/miladsrc/ai-swe-engine

- **QWEN IS LIVE** — Ollama 0.32.15, qwen2.5-coder:7b imported via Modelfile
- **FULL OFFLINE DEV FLOW ACHIEVED** — validated SPEC-TODO-CORE-R4 -> RUN-QW-2026-00009 -> CLI works

- Prompt-engineering round done, suite 48 pass
- Documentation fully rewritten for v0.2.0
- Phase 4 knowledge investigation (no Phase 4 design doc found)
- **Architectural self-assessment**: Sara is NOT part of the engine

---

### 2026-08-25

- **Master plan provided** by m.barani — 8 phases defined
- **Documentation structure created** (docs/MASTER_PLAN, ARCHITECTURE, PHASES, ADR, CHANGELOG, PROGRESS)
- **Gap analysis performed** — Phase 0 COMPLETE, Phase 1 NOT STARTED
- **Phase 1 completed** (Governance Integrity Hardening)
  - Fixed 2 bugs, added provenance tagging, built evidence export endpoint
  - All 61 tests passing, version bumped to 0.2.0

- **Sara portable knowledge base** created at https://github.com/miladsrc/sara-docs

---

### 2026-08-26

- **Todo-SpringBoot complete flow** — Full end-to-end: blueprint, specs, LLM code gen, 16 tests pass
- **Hardening batch DONE** (P1-P8) — 79 unit total + live E2E green
- **PHASE 2 START - human identity**: Token login, migration 003, require_human_actor
- **Phase 2 token migration COMMITTED**: 3e0d294 + a2ed450 merged as 8e08cc1
- **Token migration COMPLETE**: Gate proof trio verified LIVE, 101 unit + live E2E
- **Docs audit + PUSHED**: e0e2c22, full documentation sync
- **MAP DEMO E0-E3**: SpringBoot backend + Angular frontend, both MRPs green
- **SOD E2E VALIDATED**: Internal Task Manager demo approved via dashboard
- **Phase 2 SoD INCREMENT 1 DONE**: verification module, propose_only mode, 9 tests
- **Phase 2 SoD DESIGN**: Risk register R1-R7, orchestrator-owned steps A-H
- **HOL DEFERRED -> PHASE 9**: Human Operating Layer deferred to Phase 9
- **GOVERNANCE DASHBOARD BUILT**: Full UI at /ui, 5 dashboard tests, 103 unit + 8 live green
- **UI human access flow FIXED**: Login page, SPA routing, bearer auth
- **E2 gate - LLM runtime CONFIRMED 100% local**: All 7 roles use qwen2.5-coder:7b
- **Committed + pushed**: 4 reasoned commits on main (411d7cc, a0ecf42, 29e4274, 69c93b9), tip 69c93b9

---

## Key Facts

### Projects
- **ai-swe-engine**: Phase 2 SoD design COMPLETE, increment 1 done. Phase 0+1+Human Identity COMPLETE. 113+ tests passing. Version 0.2.0+
- **SARA v2**: MCP-based human-in-the-loop agent, Docker stack running. Default runtime for Level 1+ actions.
- **todo-cli**: Example project built by ai-swe-engine agents
- **demo-map-backend/frontend**: Map demo projects (SpringBoot + Angular), MRPs green
- **todo-springboot**: Spring Boot example, 16 tests pass
- **sara-docs**: Portable knowledge base (this repo)
- **game-agent**: Chrome Dino agent, score ~2400

### Architecture Decisions
- ADR-001: Sara is external to ai-swe-engine
- ADR-002: Master Development Plan is Source of Truth
- ADR-003: LLMs generate; deterministic software governs
- ADR-004: Human is final authority on all irreversible decisions
- ADR-005: Token auth now, OIDC deferred
- ADR-006: Sara v2 is default runtime (Level 1+ through Gateway)
- ADR-007: Phase 1 bugs fixed (CRP assert_run_patchable, MRP live CRP query)
- ADR-008: Separation of Duties (Phase 2 SoD, SASE_SOD_MODE=legacy default)
- ADR-009: Governance Dashboard as Client Layer
- ADR-010: Human Operating Layer deferred to Phase 9

### Current State (as of 2026-08-26)
- ai-swe-engine: Phase 0+1+Identity COMPLETE, Phase 2 SoD design COMPLETE + increment 1
- SARA v2: Default runtime, Gateway pipeline active
- Memory: 77 lines of session history
- Tests: 113+ passing
- Version: 0.2.0+
- Latest commit: 69c93b9 (pushed to github miladsrc/ai-swe-engine)
- Dashboard: Live at /ui, zero-build vanilla JS, black/gold + blue/white theme
- SoD: SASE_SOD_MODE=legacy default, strict behind flag, E2E validated
- Phase 9: DEFERRED (Human Operating Layer)
- LLM: 100% local — qwen2.5-coder:7b via Ollama, no cloud dependencies

### Known Issues / Open Items
- CRP endpoint can set run.status='blocked' bypassing assert_run_patchable (engine bug, unfixed)
- MRP open_crp_ids snapshot misses CRPs raised AFTER MRP creation (display stale, safety holds)
- Blueprint table has no API endpoint — must INSERT directly into Postgres
- Sister session's files uncommitted: agents/config.py (+designer role), designer_agent.py, SPRINGBOOT-TODO-SESSION-REPORT.md
- Ollama install needs workdir=gguf dir (no --workdir flag)
- DNS poisoning risk: OpenVPN TAP adapter may re-assert on reconnect
- SMB client registry changes still PENDING REVERT
