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
- Initial Sara documentation repository
- README.md with complete Sara overview
- ARCHITECTURE.md with trust boundaries and component responsibilities
- CHANGELOG.md for tracking changes
- ARCHITECTURE_DECISIONS.md (7 ADRs)

### Key Documentation
- Sara's role as external supervisor
- Agent roster (12 specialized subagents)
- Memory protocol (persistent cross-session)
- Projects managed (ai-swe-engine, SARA v2)
- Working rules and principles

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

---

## 2026-08-23

### Sara Activities
- Installed Git 2.55 via winget
- Cloned multiple repositories (cvat_mlops, 5 Sahba repos)
- Fixed DNS poisoning issue with OpenVPN
- Game-agent dino agent upgraded to perfect-information mode
