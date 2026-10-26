# Hamtayar — Phased Implementation Plan (Complete)

## 1. Assumptions and Open Decisions

### 1.1 Assumptions (explicitly flagged)
- **A1:** Hamtayar has **no authority over final answer generation**; outputs are cited context only.
- **A2:** Padin remains the Policy Decision Point (PDP); Hamtayar is the Policy Enforcement Point (PEP).
- **A3:** Every consumer request carries an actor identity, with optional agent identity.
- **A4:** All security defaults are **fail-closed**.
- **A5:** Scale figures, benchmark claims, and latency targets are **not invented**; see the open-questions list.
- **A6:** ACL granularity is **document-level** unless a later decision explicitly justifies section-level ACL as a separate scoped decision.

### 1.2 Open Decisions Table

| ID | Decision | Options | Recommended Default | If Wrong |
|---|---|---|---|---|
| OD-1 | Agent identity | on-behalf-of intersection / delegated only / agent standalone | **on-behalf-of intersection** | delegated only causes cross-user leakage |
| OD-2 | External metadata contract | push only / pull only / push + pull sync / event + backfill | **push events + pull fallback sync** | a single point of failure or missing deltas compromise consistency |
| OD-3 | Missing metadata behavior | not retrievable / broad visibility / default reader | **not retrievable (fail-closed)** | anything else creates an exposure path |
| OD-4 | Embeddings/models location | inside organization / managed cloud / hybrid | **inside organization unless approved** | unapproved egress of enterprise content |
| OD-5 | Code languages in release one | Java / Java + TS/JS / N languages via plugin | **Java only** | broader parser support weakens early edge quality |
| OD-6 | LLM answer generation/memory | out of scope / in scope | **out of scope** | scope creep and governance ambiguity |
| OD-7 | ACL granularity | document-level / section-level | **document-level** | section-level requires an explicit, justified decision |
| OD-8 | Padin revoke latency | near-real-time / bounded window / batch | **state the Padin requirement explicitly** | query-time enforcement can only inherit Padin timing |

## 2. Architecture

### 2.1 Components
- **Intake API** — receives ingestion requests and external metadata events.
- **Padin Adapter** — the single boundary to PDP batch permission checks.
- **Normalization & Chunking Engine** — deterministic parsing and chunk creation.
- **Code Analysis Worker** — static analysis only; no code execution.
- **Shadow Version Publisher** — writes versioned candidate data.
- **Index Projector** — exposes only committed current versions.
- **Retrieval Service** — generates candidate sets and ranks them.
- **Authorization Enforcer** — coarse pre-filter plus authoritative post-retrieval permission check.
- **Invalidation Controller** — applies tombstones and cleanup.
- **Audit Service** — immutable audit records, no content snippets.
- **Evaluation Harness** — golden queries, retrieval metrics, negative leak tests.

### 2.2 Conceptual Data Model
- `document`: logical identity, source system, repository, creation metadata.
- `document_version`: content hash, source revision, ingestion attempt id, status, create timestamp.
- `current_version_pointer`: one logical document points to exactly one committed current version; this is the atomic switch.
- `chunk`: belongs to one document_version; has offsets or AST spans; hash; citation locator.
- `symbol`: repository-scoped qualified name, definition span, language.
- `edge`: source symbol, target symbol, edge kind, certainty flag, evidence.
- `metadata`: provider record, ACL scope, classification, owner, timestamps.
- `acl_scope`: defines document-level effective permission scope relative to Padin.
- `tombstone`: marks document, version, or chunk as excluded from query; fail-closed.
- `audit_record`: actor, agent subject, operation, query hash, policy outcome, output cardinality, timestamps; no content snippet.

### 2.3 Consumer API Contract (draft)

All requests include:
- actor
- optional agent subject with explicit scope
- operation parameters

Endpoints:
- `Search(query, scope, filters, topK, pagination)`
- `GetContext(query, budget, consumerType)`
- `GetDocument(documentId)`
- `ResolveSymbol(qualifiedName, repository)`
- `FindReferences(symbolId | qualifiedName, direction, options)`

#### Error Semantics
- Policy service unavailable: `503` with **no results**.
- Not allowed and not found: identical `404` at document level.
- No count, snippet, existence signal, or timing-based inference may reveal inaccessible data.
- A caller-supplied scope narrows effective permissions; it can never widen them.

#### Agent Safety in Contract
- Effective access = intersection of user access and agent scope.
- Agent subject is mandatory in the API and audit contract from **Phase 0**.

## 3. Pipeline Specs

### 3.1 Ingestion
- **Inputs:** content reference + metadata event + caller provenance
- **Stages:** contract validation → metadata join → normalize → parse code (if applicable) → AST-based chunking → create shadow version → version validation (completeness, counts, sample checks) → authorization projection validation → atomic promotion via current_version pointer → audit
- **Failure semantics:** failed ingestion leaves query results unchanged; shadow/promoted versions are isolated; idempotency key prevents duplicate commits; no failed ingestion alters query output

### 3.2 Query
- **Inputs:** actor, optional agent, query, scope, filters, budget
- **Stages:** principal resolution → effective permission scope → coarse ACL pre-filter on current versions only → candidate retrieval → authoritative batch Padin permission check on candidate set → ranking → citation assembly → audit
- **Failure semantics:** policy service failure yields `503` and no partial result; empty result remains a valid response

### 3.3 Invalidation
- **Inputs:** delete, revoke, supersession, metadata correction
- **Stages:** create tombstone → immediate query exclusion → background cleanup → failure or success verification
- **Failure semantics:**
  - **Delete/revoke:** tombstoned items remain excluded even if cleanup partially fails.
  - **Version supersession:** version replacement allows only bounded staleness.
  - Tombstone remains authoritative until cleanup succeeds and is re-verified.

### 3.4 Code Analysis (static only)
- **Inputs:** repository snapshot, parser config
- **Stages:** syntax/AST parse → symbol extraction → edge extraction → certainty tagging → graph write → chunk correlation
- **Failure semantics:** malformed input yields partial graph plus diagnostics; code analysis failure does not block unrelated document ingestion; edge certainty is always serialized, never omitted

## 4. Reuse Before Build

| Component | Reuse Option | Decision Direction | License/Maintenance Risk | Gap vs Four Hard Problems |
|---|---|---|---|---|
| Document ingestion connectors | Onyx community edition | reuse/adapt | Verify which permission features require enterprise edition | Not guaranteed to meet Padin-as-PDP enforcement |
| Hybrid retrieval | Candidate vector store based on stack | adapt | Validate maintenance activity and operational fit | Must implement authorization and atomic publish |
| Permission modeling | OpenFGA / SpiceDB | adapt for pattern | Widely maintained but demands modeling work | PDP boundary stays Padin, not the graph itself |
| Code parsing / symbol graph | tree-sitter based tools; SCIP indexer | adapt | Check support and maturity for target languages | Must add certainty-tagged edges and provenance |
| Identifier search | Zoekt / OpenGrok | reuse / adapt | Verify deployment and licensing constraints | Must align result scopes with ACL scope |
| Graph edge semantics | None directly | build | New internal component | Unique requirement for certainty-tagged edges |

**Reality statement:** no single existing project is known to simultaneously cover Padin-as-PDP enforcement, atomic versioned publish, and certainty-tagged code graphs. Therefore, Hamtayar must build its authorization and versioning boundary, and may adapt retrieval and code-analysis components.

## 5. Phase Spikes (each with pass/fail)

### S1 Baseline permission behavior
- **Task:** Ingest a small real corpus into a candidate retrieval solution, mirror Padin-like ACLs, run negative permission-leak suite and revoke-latency test.
- **Pass:** no leak; the candidate supports the required authorization test pattern.
- **Fail:** authorization result must be treated as an explicit hard risk.

### S2 Padin batch permission feasibility
- **Task:** measure batch permission checks on representative candidate sets.
- **Pass:** latency and result size are acceptable for production candidate sizes; contract approved.
- **Fail:** if unsuitable, propose the documented fallback design and state its security trade-off explicitly.

### S3 Retrieval store behavior
- **Task:** test filtered vector search with restrictive ACL filters and identifier search for camelCase and qualified identifiers.
- **Pass:** acceptable filter behavior and identifier recall.
- **Fail:** accept fewer retrieval-store options or require design adjustment with named consequences.

## 6. Phased Plan

### Phase 0 — Decisions, Contracts, Evaluation Harness
- **Goal:** establish contract-first foundation and executable evaluation tooling.
- **In scope:** decisions, API contract, metadata contract, spikes S1-S3, golden query corpus, leak cases, audit baseline
- **Out of scope:** production ingestion, advanced code graph, answer generation
- **Deliverables:** approved ADRs, API and metadata schemas, spike reports, evaluation harness
- **Dependencies:** stakeholder decisions, Padin integration lead
- **Acceptance criteria:** contracts signed; harness runnable; agent subject present in contract and audit model
- **Risks:** unresolved decision ambiguity
- **Effort:** M

### Phase 1 — Trust Core on Documents
- **Goal:** an end-to-end authorization-aware document retrieval slice.
- **In scope:** ingestion, ACL projection, `Search`, `GetContext`, `GetDocument`, audit trail, adversarial intersection tests for agent subjects
- **Out of scope:** code graph, version history, answer generation
- **Deliverables:** production document ingestion path and query service
- **Dependencies:** Phase 0 contracts and Padin sandbox
- **Acceptance criteria:** no unauthorized bytes, counts, or error observations; forced unauthorized access results do not exist
- **Risks:** policy mapping defects; authorization bypass
- **Effort:** L

### Phase 2 — Versioning and Invalidation
- **Goal:** make changes safe and deterministic.
- **In scope:** shadow version and current pointer; version validation; invalidation via tombstones; revoke/delete bounded consistency
- **Out of scope:** new retrieval interfaces
- **Deliverables:** versioned publish and invalidation services
- **Dependencies:** Phase 1 document core
- **Acceptance criteria:** failed ingestion does not change query results; revoked items disappear or return identical not-found behavior within the explicit contract
- **Risks:** deployable complexity in version state
- **Effort:** M

### Phase 3 — Code Pipeline
- **Goal:** make code graph-aware and permissioned.
- **In scope:** `ResolveSymbol`, `FindReferences`, parser integration, certainty flags, citation links
- **Out of scope:** graph query APIs outside the required contract; broad language coverage
- **Deliverables:** code-side search and reference resolution
- **Dependencies:** Phase 1/2 infrastructure and metadata contract
- **Acceptance criteria:** edges and symbols both honor ACL boundaries and include certainty flags
- **Risks:** language coverage precision drift
- **Effort:** L

### Phase 4 — Agent Interface
- **Goal:** expose a safe agent contract with on-behalf-of semantics.
- **In scope:** agent subject enforcement, intersection permission engine, citations for agents, injection-defense metadata
- **Out of scope:** an agent runtime inside Hamtayar
- **Deliverables:** agent-facing operations and test vectors
- **Dependencies:** stable document/code contracts
- **Acceptance criteria:** agent permission tests remain green under adversarial inputs
- **Risks:** scope mismatch between human and agent identities
- **Effort:** M

### Phase 5 — Quality and Scale
- **Goal:** polish quality and operational evidence.
- **In scope:** ranking evaluation, benchmarking, observability hardening, partitioning guidance supported by real results
- **Out of scope:** untested product expansion
- **Deliverables:** quality report, runbooks, operations guide
- **Dependencies:** measured real workloads from prior phases
- **Acceptance criteria:** agreed baselines pass and rollback path is documented
- **Risks:** performance surprises under real data
- **Effort:** M/L

### Challenge to Candidate Order
The candidate sequence is accepted because authorization and testability precede features, but one correction is required: **adversarial agent-permission tests must start in Phase 1**, even before full agent APIs arrive, so the core data path is proven safe first.

## 7. Cross-Cutting Requirements

### Security
- default deny across intake, retrieval, document access, and graph access
- only coarse pre-filter plus authoritative post-retrieval check
- document-level ACL unless explicitly changed
- no exact count, timing, or error variance for inaccessible content
- no content snippets in logs, telemetry, or error messages

### Evaluation
- golden queries before feature implementation
- metrics: relevance metrics and exact behavior checks
- negative permission-leak tests are release blockers
- each ACL bug becomes a regression test

### Observability and Audit
- no snippets in logs or audit records
- decision-bearing state changes captured
- failed ingestions and invalidations visible as distinct events
- consume audit data without exposing raw content text

### Prompt-Injection Defenses
- all context content marked as untrusted source material
- response contract includes citation boundaries
- consumers are instructed not to treat context as commands
- no execution or extension derived from retrieved text

## 8. Traceability Matrix

| Requirement | Phase | Acceptance Test |
|---|---:|---|
| Authorization-aware retrieval | 1 | unauthorized content/secrecy/leak suite must fail |
| Consistent delete/revoke behavior | 2 | revoke-latency test and tombstone checks |
| Failed ingestion never changes query results | 2 | fault-injection ingestion tests |
| Code graph with certainty labels | 3 | edge certainty and resolution test suite |
| On-behalf-of safety | 1 + 4 | adversarial intersection tests |
| Fail-closed policy behavior | 1 | PDP unavailable returns 503 with no results |
| Identical not-found/not-allowed errors | 1 | 404 equivalence test |
| No leaks through counts or errors | 1 | leak suite |
| No deferred feature creep | all phases | scope review against requirements |

## 9. Consolidated Open Questions

1. What are current and peak query rates and customer-facing latency commitments?
2. What are expected document repository sizes in Year 1 and Year 3?
3. What are expected code repositories per language and total symbol counts?
4. What is Padin's required revoke propagation latency at query time?
5. Are agent subjects required at the gateway contract, or only downstream?
6. Are section-level ACL semantics needed for any regulated class of content?
7. Which code languages must be supported in release one?
8. Are embeddings and models required to remain fully inside the organization?
9. What is acceptable bounded staleness for content updates?
10. Which consumers require `GetDocument` versus only cited context?

**Proceed rule:** unanswered questions continue with the stated defaults and each affected deliverable is flagged as assumption-dependent. No numbers, benchmarks, or performance claims are presented as confirmed.