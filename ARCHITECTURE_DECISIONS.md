# Sara Architecture Decisions

## ADR-001: Sara is External

**Date:** 2026-08-24
**Status:** Accepted
**Context:** Architectural self-assessment of Sara vs ai-swe-engine

### Decision

Sara is NOT part of the engine. Sara is a development-time assistant.

### Rationale

1. The engine must be fully air-gapped and autonomous
2. No Python file in the engine imports Sara
3. No runtime component depends on Sara
4. Engine runs with `docker compose up` + Ollama, no Sara needed

### Consequences

- Trust boundary formalized: outside (human, Sara, dev tools) vs inside air-gapped (engine, agents, LLM, Postgres)
- All deterministic governance (gates, security, audit, IDs) must NEVER depend on LLM
- LLM produces content only

---

## ADR-002: Master Plan is Source of Truth

**Date:** 2026-08-25
**Status:** Accepted
**Context:** m.barani provided complete AI-SWE-ENGINE MASTER DEVELOPMENT PLAN

### Decision

The Master Development Plan is the official Source of Truth for ai-swe-engine development.

### Rationale

1. Defines 8 phases with clear deliverables
2. Establishes autonomy model (L0-L4)
3. Sets governance rules
4. Clarifies component responsibilities

### Consequences

- All development follows the plan
- Phase transitions require verification
- Sara is external, advisory-only
- Human is final authority on all irreversible decisions

---

## ADR-003: LLMs Generate, Deterministic Software Governs

**Date:** 2026-08-24
**Status:** Accepted
**Context:** Architectural principle for ai-swe-engine

### Decision

LLMs generate content; deterministic software governs actions.

### Rationale

1. LLMs are probabilistic and can hallucinate
2. Governance must be deterministic and predictable
3. Human approval at critical decision points

### Consequences

- All gates are deterministic code
- LLM output is treated as draft content
- Human reviews and approves before execution

---

## ADR-004: Human is Final Authority

**Date:** 2026-08-24
**Status:** Accepted
**Context:** Trust boundary between Sara and managed systems

### Decision

The human (m.barani) is the final authority on all irreversible decisions.

### Rationale

1. Sara is external and advisory-only
2. Managed systems must be independent
3. Human oversight prevents autonomous mistakes

### Consequences

- Sara proposes, human approves
- Destructive actions require confirmation
- No autonomous execution of irreversible changes

---

## ADR-005: Token Auth Now, OIDC Deferred

**Date:** 2026-08-24
**Status:** Accepted
**Context:** Authentication decision for ai-swe-engine

### Decision

Use token-based authentication now; defer OIDC until second human/deploy-off-localhost/corporate IdP.

### Rationale

1. Token auth is simpler to implement
2. Sufficient for single-developer use
3. OIDC adds complexity not needed yet

### Consequences

- users table + /auth/login endpoint
- X-Acting-As header for human-only endpoints
- OIDC can be added later when needed

---

## ADR-006: Sara v2 is Default Runtime

**Date:** 2026-08-24
**Status:** Accepted
**Context:** Bridge between opencode Sara (v1) and SARA v2

### Decision

Sara v2 (MCP-based human-in-the-loop agent) is the default runtime for Level 1+ actions.

### Rationale

1. Provides governance pipeline (classify -> policy -> approval -> execute -> audit)
2. Human approval at critical decision points
3. Audit trail for all actions

### Consequences

- v1 routes Level 1+ actions through v2 Gateway
- Approver prefix "gateway-controller:" mandatory
- Fallback to direct execution only if stack down + must disclose

---

## ADR-007: Phase 1 Bugs Fixed

**Date:** 2026-08-25
**Status:** Accepted
**Context:** Phase 1 (Governance Integrity Hardening) implementation

### Decision

Fix two known bugs and add provenance tagging + evidence export.

### Rationale

1. Bug 1: CRP endpoint bypassed assert_run_patchable (could flip terminal runs)
2. Bug 2: MRP open_crp_ids snapshot missed CRPs raised after MRP creation
3. No provenance tagging existed
4. No evidence export endpoint existed

### Consequences

- CRP endpoint now calls assert_run_patchable before setting run.status=blocked
- mrp_ready_for_merge now queries live CRP data
- MRPEvidenceUpdate schema accepts provenance field (human|tool|llm)
- GET /evidence/run/{run_id} returns run details, MRP evidence, and audit trail
- 3 regression tests added

---

## ADR-008: Separation of Duties (Phase 2 SoD)

**Date:** 2026-08-26
**Status:** Design Complete, Increment 1 Implemented
**Context:** Phase 2 SoD - coder self-attestation risk

### Decision

Implement Separation of Duties behind SASE_SOD_MODE flag (legacy default). Coder becomes PROPOSAL-ONLY in strict mode; orchestrator owns verification via agents/verification.py with tree-hash content binding.

### Rationale

1. Self-certification risk: coder runs its own tests and certifies its own output
2. No content binding between tested bytes and committed bytes
3. Provenance misleading (ci:test-runner identity but agent-produced data)
4. Self-authored tests can be gamed
5. Reviewer agent absent (ai_review_status always null)

### Design

- Orchestrator-owned verification steps A-H (generate -> snapshot commit+tree hash -> independent test step in clean checkout -> scan same tree -> lint -> evidence PATCH w/ runner=orchestrator -> MRP -> CRP -> terminal)
- Tree-hash content binding: HEAD^{tree} hash bound to evidence, test step FAILS CLOSED on drift
- New gates: G7 (runner=orchestrator + tree_hash match required), G8 (ai_review presence)
- Migration 004: MRP.verified_tree_hash column
- Rollout: SASE_SOD_MODE=legacy default, strict flip after E2E validation

### Consequences

- Legacy path unchanged when flag unset
- CoderAgent.implement_spec(propose_only=True) returns verification_pending=True
- Orchestrator _sod_verify_and_package shared by CLI and demo scripts
- AgentRunUpdate.status now Optional (proposal patches are non-terminal metadata)
- 9 unit tests (drift fail-closed, checkout isolation, proposal-only never verifies)

---

## ADR-009: Governance Dashboard as Client Layer

**Date:** 2026-08-26
**Status:** Accepted, Implemented
**Context:** Need for human-facing UI to manage governance workflow

### Decision

Build a pure client-layer dashboard served at /ui (zero-build vanilla JS, air-gap safe). No new trust boundary, no second auth system.

### Rationale

1. Need human-facing UI for approvals, audit, evidence chain
2. Must not introduce new authorization system
3. Must work air-gapped (no build tooling, no CDN)
4. Bearer-first auth via require_authenticated_actor

### Consequences

- Backend: dashboard.py read-only router, require_authenticated_actor (bearer preferred)
- UI: login, dashboard, Approval Center, Agent Runs, Evidence Chain, Audit, Projects, Console, Settings
- Console records instructions to audit_log only; does NOT spawn agents
- Dockerfile copies static/ui into image
- Designer agent (agents/designer_agent.py) generates DESIGN.md contract

---

## ADR-010: Human Operating Layer Deferred to Phase 9

**Date:** 2026-08-26
**Status:** Accepted (DEFERRED)
**Context:** Full human workspace/dashboard effort vs backend governance milestones

### Decision

Defer the complete Human Operating Layer (roles, assignments, My Tasks, notifications, team management) to Phase 9 — Platform UI / Human Operations Layer.

### Rationale

1. Auth and interim dashboard exist but full human workspace is a major frontend product effort
2. Must not dilute backend governance milestones (Phases 0-8)
3. Phase 9 gives it a formal home without disturbing existing phases

### Consequences

- Architectural concepts preserved in docs/HUMAN_OPERATING_LAYER_PROPOSAL.md
- No migrations/endpoints/UI built from it until Phase 9
- Prerequisites: Phases 1-4 stable, SoD complete, strict token mode ON
- Pipeline-start API deliberately withheld until Phase 2 SoD restructures execution ownership

---

## ADR-011: Genuine SoD Isolation (Real Agent/Process Separation)

**Date:** 2026-08-31
**Status:** Accepted (incremental implementation; remote boundary BLOCKED)
**Context:** Owner decision — Phase 2 SoD must be genuine separation, not logical classes/prompts in one process (ADR-011 supersedes ADR-008's orchestrator-owned verification design; ADR-008 history preserved)

### Decision

Move to REAL agent/process isolation: `User → Orchestrator → Coder → Independent Verifier subprocess → G7 → Independent Reviewer subprocess → G8 → Human → Merge`. Rule: `Coder ≠ Verifier ≠ Reviewer ≠ Human`. Full record in ai-swe-engine `docs/ADR/ADR-002-genuine-sod-isolation.md` (+ addendum).

### Rationale

1. Orchestrator-owned verification was still self-attestation in one process
2. Evidence provenance must be owned by a distinct credentialed identity
3. Orchestrator must NOT hold verifier credentials (no god-process)

### Consequences

- Verifier + Reviewer run as separate subprocesses with own identity + credentials (`ci:verifier` / `agent:reviewer`, SASE_VERIFIER_TOKEN / SASE_REVIEWER_TOKEN)
- Orchestrator coordinates via immutable verification requests; never reads verifier token; never writes verifier evidence
- G7 trusts verifier-owned evidence tree hash == MRP.verified_tree_hash; G8 requires reviewer-owned completed review
- Security scanner extracted to neutral agents/scanner.py
- GENUINE REMOTE BOUNDARY VERDICT BLOCKED (2026-08-31): same-local-admin user + Docker daemon control make all local credentials forgeable; remote GitLab runner requires infra/authority outside m.barani (repo not on gitlab.sidg.ir; m.barani = Developer)
- Local harness (migration 006 verification_requests + claim/complete endpoints + verifier --claim) proves protocol mechanics only
- Live comms evidence of the real chain: scripts/trace_coder_verifier.py (2026-09-05), SASE_ENGINE_TRACE=1
