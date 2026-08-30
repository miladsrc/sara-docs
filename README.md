# sara-docs

## Documents

- **PROGRESS-PHASE-2.md**: AI-SWE-Engine Phase 2 progress manifest (SoD, token auth, governance, tests, next steps)
- **PONYTAIL_SELF_UPGRADE_REPORT.md**: Audit of the vendored `ponytail/` plugin self-upgrade
- **SARA_ARCHITECTURE_AFTER_ROUND2.md**: Round 2 architecture as implemented on the opencode runtime
- **SARA-GOLDEN-RESULTS.md**: Evidence records from golden-task runs
- **SARA_GOLDEN_TASKS.md**: Golden probe set used to compare Sara before/after an upgrade
- **SARA_SELF_BOUNDARY.md**: Rules for when Sara may modify herself
- **SARA_SELF_UPGRADE_ROUND2_BASELINE.md**: Pre-upgrade baseline measurements
- **SARA_SELF_UPGRADE_ROUND2_FINAL_REPORT.md**: Round 2 self-upgrade final report
- **SARA_SYSTEM_MAP.md**: Phase-0 discovery — component inventory of Sara on this host
- **SARA_UPGRADE_CANDIDATES.md**: Candidate upgrade items considered for Round 2
- **ponytail/**: Vendored `@dietrichgebert/ponytail` plugin project (lazy-senior-dev mode)

## Task Log

### 2026-08-26 - Phase 2 SoD COMPLETE (ai-swe-engine)
- Built agents/verification.py: tree-hash binding, clean-checkout test/scan/lint steps
- CoderAgent.implement_spec(propose_only=True): proposal stops after commit
- Orchestrator _run_code_phase: SASE_SOD_MODE=strict branch runs steps A-H
- tests/test_sod_unit.py: 9 tests incl. fail-closed drift
- Suite: 113 unit green
- Map demo E0-E3 done (both SoD tracks GREEN, approvals pending)
- SpringBoot + Angular tracks validated
- Honest repair history preserved (failed runs kept as provenance)

### 2026-08-26 - Token Migration COMPLETE
- Token-first auth implemented (SASE_LIVE_USERNAME/SASE_LIVE_PASSWORD)
- Legacy X-Acting-As fallback only when credential-less
- Gate proof trio verified LIVE: valid token, invalid token 401, spoofed header rejected
- 101 unit + live E2E green in both modes
- SASE_REQUIRE_HUMAN_TOKEN=1 ready (flag OFF per owner)

### 2026-08-26 - Human Identity System
- users + api_tokens tables (migrations/003_users.sql)
- PBKDF2 + token crypto (api/authn.py)
- /auth/login + /auth/me endpoints
- Bearer token in require_human_actor
- Bootstrap script: scripts/create_user.py
- 21 DB-free auth tests
- User m.barani created and verified

### 2026-08-26 - Hardening Batch (P1-P8)
- P1: Env-configurable Ollama + bounded transient retry
- P2: Provenance columns populated (model_version, prompt id/ver/hash)
- P3: CI token fail-closed (503), constant-time compares
- P4: Orphan-run reaper on startup
- P5: Surgical git staging + language-aware security scan
- P7: Full test/scan/lint output persisted into audit context
- P8: Blueprint create/update audited

### 2026-08-26 - Governance Dashboard
- static/ui/: login → dashboard → approvals → runs → evidence → audit
- Backend: dashboard.py read-only router + require_authenticated_actor
- Dockerfile ships static/ui; live at http://localhost:8000/ui/
- 5 dashboard tests + 103 unit + 8 live green

### 2026-08-25 - Phase 1 Complete (ai-swe-engine)
- Fixed Bug 1: CRP endpoint now calls assert_run_patchable before setting run.status=blocked
- Fixed Bug 2: mrp_ready_for_merge now queries live CRP data instead of stale open_crp_ids snapshot
- Added provenance tagging to evidence records (human|tool|llm)
- Built read-only evidence export endpoint: GET /evidence/run/{run_id}
- Added 3 regression tests for the two bugs
- All 61 tests passing
- Version bumped to 0.2.0

### 2026-08-24 - Coder Agent Live (ai-swe-engine)
- Built agents/coder_agent.py + coder_prompts.py
- Full offline dev flow achieved with local LLM (qwen2.5-coder:7b)
- Live demo: spec -> agent run -> MRP -> CI evidence -> working CLI
- Prompt engineering round for better spec quality
- Documentation fully rewritten for v0.2.0

### 2026-08-24 - SARA v2 Setup
- Built MCP-based human-in-the-loop agent platform
- Stack: Python 3.12, LangGraph, FastAPI, Postgres+pgvector
- Gateway pipeline: classify->policy->approval->execute->audit
- E2E approval demo passed live
- All 4 MCP servers enabled

### 2026-08-23 - Initial Setup
- Installed Git 2.55 via winget
- Cloned repos into IdeaProjects
- Built game-agent project with direct state mode