# Sara Documentation Changelog

---

## 2026-08-26

### Major Updates
- Phase 2 SoD design and implementation increment 1 committed and pushed
- Governance Dashboard built and live at /ui
- SoD validation demo completed end-to-end (Internal Task Manager)
- Map demo E0-E3 completed (SpringBoot + Angular)
- Human Operating Layer deferred to Phase 9
- 4 reasoned commits pushed to origin (tip 69c93b9)
- Hardening batch DONE (P1-P8) — 79 unit total + live E2E green
- Phase 2 token migration COMMITTED and COMPLETE — gate proof trio verified LIVE
- Docs audit + PUSHED (e0e2c22)
- E2 gate confirmed: LLM runtime 100% local (qwen2.5-coder:7b)
- UI human access flow FIXED (login page, SPA routing, bearer auth)
- 113+ tests passing

### Added
- docs/PHASES/PHASE-2.md: SoD design doc (risk register R1-R7, steps A-H, gates G7/G8)
- agents/verification.py: tree-hash binding, clean-checkout, orchestrator-owned test/scan/lint
- CoderAgent.propose_only mode (SoD strict: proposal stops after commit)
- Orchestrator _sod_verify_and_package shared by CLI and demo
- Dashboard UI (static/ui/): vanilla JS, black/gold + blue/white theme
- api/routers/dashboard.py: read-only dashboard endpoints
- require_authenticated_actor dependency (bearer-first)
- Designer agent (agents/designer_agent.py, agents/config.py designer role)
- migrations/004_prompt_registry.sql
- tests/test_sod_unit.py (9 tests), tests/test_dashboard_live.py (5 tests)
- scripts/: demo validation, map demo, seed scripts, evidence viewer
- docs/DEMO_VALIDATION_SOD.md, docs/design/DASHBOARD_DESIGN.md
- docs/HUMAN_OPERATING_LAYER_PROPOSAL.md (architectural preparation)
- Phase 9 in MASTER_PLAN.md (DEFERRED)
- api/authn.py: Token authentication (PBKDF2 200k, sha256-stored tokens)
- api/routers/auth.py: /auth/login + /auth/me endpoints
- migration 003_users.sql: users + api_tokens tables
- scripts/create_user.py: User creation script
- tests/test_auth_unit.py: 21 DB-free auth tests

### Changed
- api/schemas.py: AgentRunUpdate.status now Optional
- api/routers/agent_runs.py: optional status guard
- CoderAgent._commit: staged-only check (git diff --cached)
- README: Dashboard section, Phase 9 roadmap note
- ARCHITECTURE: UI Boundary subsection
- CHANGELOG: Multiple entries for 2026-08-26
- FULL_DOCUMENTATION: Dashboard API table, Phase 9 deferral note
- MASTER_PLAN: Phase 2 status -> DESIGN COMPLETE, new Phase 9
- PROGRESS/2026-08-26.md: Complete session timeline
- Dockerfile: COPY static/ui

---

## 2026-08-25

### Added
- Sara documentation repository (this repo) — portable knowledge base
- README.md with complete Sara overview
- ARCHITECTURE.md with trust boundaries and component responsibilities
- CHANGELOG.md for tracking changes
- ARCHITECTURE_DECISIONS.md (10 ADRs total)
- IDENTITY.md, CAPABILITIES.md, WORKING_RULES.md
- PROJECT_CONTEXT.md, MEMORY.md, PORTABLE_KNOWLEDGE_BASE.md
- config/AGENTS.md (opencode agent configuration)
- memory/sara.md (persistent memory export)
- skills/read-terminals/ (terminal monitoring skill)
- scripts/load_sara.py (loader script)

### Key Documentation
- Sara's role as external supervisor
- Agent roster (13 specialized subagents including designer)
- Memory protocol (persistent cross-session, append-only)
- Projects managed (ai-swe-engine, SARA v2, todo-cli, todo-springboot, demo-map, game-agent)
- Working rules and principles
- 10 Architecture Decision Records

### ai-swe-engine
- Phase 1 completed (Governance Integrity Hardening)
- 2 bugs fixed, provenance tagging, evidence export
- 61 tests passing, version 0.2.0
- Documentation fully rewritten for v0.2.0
- Master plan provided, 8 phases defined

---

## 2026-08-24

### Sara Activities
- Built SARA v2 (MCP-based human-in-the-loop agent)
- Built ai-swe-engine agent layer (6 RolePolicies)
- Achieved full offline dev flow with Qwen 7B
- Pushed ai-swe-engine to GitHub (miladsrc)
- Completed architectural self-assessment
- Installed Docker Desktop 4.87
- E2E approval demo passed live
- SARA v2 became default runtime
- read-terminals skill added
- Phase 4 knowledge investigation
- Prompt-engineering round
- Documentation fully rewritten for v0.2.0

---

## 2026-08-23

### Sara Activities
- Installed Git 2.55 via winget
- Cloned multiple repositories (cvat_mlops, 5 Sahba repos)
- Fixed DNS poisoning issue with OpenVPN
- Game-agent dino agent upgraded to perfect-information mode
