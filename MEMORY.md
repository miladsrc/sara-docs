# Sara Complete Memory

> **Last Updated:** 2026-08-25
> **Total Entries:** 47 lines
> **Source:** `~/.config/opencode/memory/sara.md`

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
- Meaning of gml unclear, no action taken

- game-agent project (IdeaProjects\game-agent):
  - Upgraded dino agent from vision-only to perfect-information "direct" mode
  - agent/direct_state.py reads game vars via page.evaluate
  - Exact-physics jump window in decision.py decide_exact
  - Score 867 -> ~2400 consistent
  - Deterministic ceiling at score ~2377 remains (input latency vs difficulty ramp)
  - User declined further tuning ("merge them, it won't get better")
  - Bugs fixed: obstacles-behind-player causing jump spam
  - Blocking duck removed in direct mode (birds can't hit grounded player in this game)
  - NOTE: concurrent edits/launches happened on this repo during the session

---

### 2026-08-24

- **Built SARA v2** (IdeaProjects\sara):
  - MCP-based human-in-the-loop agent per user mission
  - Stack: Python 3.12, LangGraph, mcp SDK, FastAPI (:8800), Postgres+pgvector (user-approved), FileApprovalStore fallback
  - Gateway pipeline classify->policy(L0-L3)->approval->execute->audit
  - L3 needs SARA_ARM_LEVEL3 + "gateway-controller:" approver
  - SECURITY FIXES during build:
    1. Approval forgery at L1/L2 - approver must now start with "human:"/"gateway-controller:"
    2. Unicode homoglyph evasion - PolicyEngine NFKC+zero-width-strips args before regex
  - 31 tests pass (.venv in repo)
  - Existing opencode Sara untouched; persona derived from AGENTS.md in sara/agent_core/prompts/sara.md
  - Open: docker compose not yet run end-to-end; MCP servers disabled by default except filesystem

- **ai-swe-engine project** (IdeaProjects\ai-swe-engine):
  - SASE traceability backbone, FastAPI+Postgres
  - PRD->US->AC->Spec->AgentRun->CRP->MRP->VCR chain with hard gates
  - Fixed 4 gaps:
    1. ids.py _next_seq race -> single UPSERT..RETURNING
    2. NEW api/security.py require_human_actor dependency
    3. CRP list ordering was alphabetical -> CASE priority order
    4. Removed unused param from crp merge gate
  - Added tests/test_gates_unit.py (14 DB-free tests, all pass)
  - README curl walkthrough updated for the header
  - Not committed (no repo init)
  - Remaining known gap: X-Acting-As is a seam, not real authn - OIDC/mTLS later

- Ran review agent over ai-swe-engine -> 18 findings (4 HIGH blocking, 7 MED, 7 LOW)
- Compiled docs/FULL_DOCUMENTATION.md in the project
- Findings NOT yet fixed - user hasn't asked

- ai-swe-engine now a git repo (baseline commit 7011274)
- Coding agent fixed the 4 HIGH findings UNCOMMITTED for user review:
  - B1: require_ci_actor on /mrps/{id}/evidence + SASE_CI_TOKEN env
  - B2: optional SASE_API_TOKEN perimeter middleware in main.py
  - B3: assert_run_patchable in gates.py - terminal agent runs immutable 409
  - B4: migrations/002_audit_lockdown.sql + require_any_actor guards
- 36 unit tests pass
- Stray empty git/ dir inside project left on disk, gitignored

- User approved deletion of git/ dir (done)
- Docker stack UP: ai-swe-engine-postgres-1 on host 5433, ai-swe-engine-api-1 on 8000
- Migrations 001+002 auto-applied on first boot
- Found+fixed TWO latent product bugs while getting E2E green:
  1. VCR resolving a CRP never cleared it from MRPs' open_crp_ids snapshot
  2. E2E test lacked blueprint_version on MRP
- Suite now 37 passed x2 consecutive runs incl. live E2E chain
- Seeded demo project: demo-springboot, PRD-AUTH-001, US-AUTH-001, AC-AUTH-001-01

- All pending changes committed as 7 reasoned commits on master
- Branches: master=stable, develop (checked out, active dev), hotfix/stale-crp-snapshot-repair
- Auth decision: token login now, OIDC deferred

- Enabled all 4 MCP servers in sara/mcp_layer/servers.yaml
- Installed Docker Desktop 4.87 via winget
- docker compose stack UP: sara-db-1 + sara-app-1, health ok

- E2E approval demo PASSED live
- FIXES during demo: graph.run was sync .invoke() on async nodes -> now async ainvoke
- Wired real sandbox-confined fs executors into api/main.py
- 37/37 tests pass

- **SARA V2 IS NOW THE DEFAULT RUNTIME**
- Bridge added to ~/.config/opencode/AGENTS.md
- All 13 v1 memory files seeded into v2 pgvector via scripts/seed_memory.py

- User approved sara.md quarantine release
- All 13 v1 memory files fully live in v2

- **read-terminals skill added** (user approved)
- Built `~/.config/opencode/skills/read-terminals/`
- Reads other opencode sessions via shared DB

- Started REAL project (todo-cli) on ai-swe-engine with separate-agent layer
- Built agents/ package with 6 RolePolicies
- 8 new unit tests, suite 44 pass
- Seeded live chain: project todo-cli, PRD-TODO-002, US-TODO-002, AC-TODO-CORE
- Gate 1 verified live: agent-run vs unvalidated spec -> 409

- ai-swe-engine pushed to origin = https://github.com/miladsrc/ai-swe-engine
- Root cause of "git terminal problem": missing user.name/email + DNS poisoning
- FIXED durably via elevated netsh setting

- **QWEN IS LIVE**
- Ollama 0.32.15 installed, qwen2.5-coder:7b imported via Modelfile
- Pipeline --online run GREEN end-to-end
- Spec quality mediocre (tutorial-style, ignores template format) - expected for v0 prompts

- **FULL OFFLINE DEV FLOW ACHIEVED** on ai-swe-engine
- New: IdeaProjects\todo-cli = agents' local git workspace
- Flow proven live: validated SPEC-TODO-CORE-R4 -> RUN-QW-2026-00009 -> todo.py+test_todo.py written
- CLI actually works (add/list/--priority/TODO_STORE)
- LESSONS: qwen 7b oscillates architectures between repairs

- Prompt-engineering round done on ai-swe-engine agents/
- KEY LESSON: qwen 7b ignores negative prompting re fabricated AC ids
- Suite 48 pass incl live e2e

- ai-swe-engine documentation fully rewritten for v0.2.0
- 58 tests pass

- **Phase 4 knowledge investigation**
- FINDINGS: No Phase 4 design doc exists anywhere in repo
- Redis: ZERO code support
- LangGraph: explicitly deferred
- Report saved as docs/PHASE_4_KNOWLEDGE_REPORT.md

- **Architectural self-assessment** of Sara vs ai-swe-engine
- KEY DECISION: Sara is NOT part of the engine
- Trust boundary formalized

---

### 2026-08-25

- **Master plan provided** by m.barani
- Key decisions: Sara is external, engine is the product, LLMs generate, human is authority
- 8 phases defined, Phase 1 is NEXT
- Saved MASTER_PLAN.md as Source of Truth

- **Documentation structure created**
- docs/MASTER_PLAN.md, docs/ARCHITECTURE.md, docs/PHASES/PHASE-0.md, docs/PHASES/PHASE-1.md
- docs/ADR/ADR-001-sara-is-external.md, docs/CHANGELOG/CHANGELOG.md
- docs/PROGRESS/2026-08-25.md, docs/GAP_ANALYSIS.md

- **Gap analysis performed**
- Phase 0 COMPLETE, Phase 1 NOT STARTED
- Two known bugs, no provenance tagging, no evidence export endpoint
- 58 tests passing

- **Phase 1 completed** (Governance Integrity Hardening)
- Fixed Bug 1: CRP endpoint now calls assert_run_patchable
- Fixed Bug 2: mrp_ready_for_merge now queries live CRP data
- Added provenance tagging to evidence records
- Built read-only evidence export endpoint
- Added 3 regression tests
- All 61 tests passing
- Version bumped to 0.2.0

---

## Key Facts

### Projects
- **ai-swe-engine**: Phase 1 complete, 61 tests passing, version 0.2.0
- **SARA v2**: MCP-based human-in-the-loop agent, Docker stack running
- **todo-cli**: Example project built by ai-swe-engine agents

### Architecture Decisions
- Sara is external to ai-swe-engine (ADR-001)
- Master Development Plan is Source of Truth
- 8 phases defined
- LLMs generate; deterministic software governs
- Human is final authority on all irreversible decisions

### Current State
- ai-swe-engine: Phase 1 complete, Phase 2 next
- Memory: 47 lines of session history
- Tests: 61 passing
- Version: 0.2.0
