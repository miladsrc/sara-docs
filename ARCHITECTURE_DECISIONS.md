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
- All 61 tests passing
- Version bumped to 0.2.0
