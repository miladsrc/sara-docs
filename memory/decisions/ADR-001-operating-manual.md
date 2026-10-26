# ADR-001 — Rebuild sara-docs as a validated operating manual

**Status:** accepted
**Date:** 2026-10-25
**Owner:** m.barani
**Supersedes:** DECISION 001 in `archive/SARA-DECISIONS.md` (see Consequences)

## Context

The repository held 16 standalone markdown reports describing Sara's architecture
and history. Verified during this session:

- **FACT** — the reports described host user `98903` and opencode `1.18.25`; the
  actual host is `m.barani` on opencode `v2.1.4`.
- **FACT** — `archive/SARA-DECISIONS.md` DECISION 001 claims the live config is a
  git repository (`82c89c4`); `C:\Users\m.barani\.config\opencode` is **not** a git
  repository.
- **FACT** — the reports reference `command/`, `plugin/sara.js`, `test/`,
  `state/`, three skills, and three agents that do not exist on this host.
- **FACT** — eight stale claims across three files, none of which anything checked.
- **FACT** — there was no workflow documentation of any kind: no feature path, no
  bugfix path, no migration path, no definition of done, no review method.
- **OBSERVED** — `C:\Users\m.barani\IdeaProjects\hmyar` implements the mature
  pattern: `memory/`, `workflows/`, `backlog/`, validating scripts, CI.

Owner instruction: improve the docs so they help deliver software, not just
describe Sara.

## Decision

Restructure this repository on the pattern already proven in the `hmyar`
repository: a validated operating manual with durable memory, SDLC playbooks,
agent contracts, an evaluation loop, and scripts that fail when the docs drift.
Freeze the previous reports into `archive/` unmodified.

Structure: `README.md` (entry) · `AGENTS.md` (operating contract) · `memory/` ·
`architecture/` · `workflows/` · `roster/` · `evaluation/` · `backlog/` ·
`scripts/` + `tests/` · `archive/` (frozen).

## Rejected alternatives

- **Rewrite the 16 reports in place.** Keeps 16 competing documents, no entry
  point, and no enforcement. The reports are evidence of history; editing them
  destroys the record while keeping the sprawl.
- **Docs only, no live pointer.** The playbooks would be reference material Sara
  never loads — documentation that cannot change behavior. Rejected by the owner.
- **Full wiring (commands + telemetry plugin + re-init git) in one step.** Largest
  blast radius on the live runtime, several irreversible-ish steps, and all three
  items are open questions (OQ-001, OQ-002, OQ-003) the owner has not decided.
  Deferred, not dropped.
- **Bespoke information architecture.** A second, differently shaped convention for
  the same problem the owner had already solved in `hmyar`.

## Consequences

- **Behavior change:** Sara now has procedures with gates instead of narrative
  reports. None of it is enforced until the live runtime points at `workflows/` —
  that edit is proposed separately and requires approval.
- **Cost:** three validators and a test suite (~25 tests) to maintain; the gate
  must keep passing. Dependencies added: **zero** (stdlib Python + pytest already
  present).
- **Unchanged:** no application code touched; no live runtime file modified in this
  change; `archive/` preserved byte-for-byte.
- **Reversibility:** high — the change is additive plus `git mv`; reverting is a
  checkout of the previous commit.
- **INHERITED OBLIGATION:** DECISION 001's goal (versioning the live runtime) is
  **not** delivered by this ADR. It remains open as OQ-001. This ADR removes the
  false claim from the living docs; it does not create the guarantee.

## Verification (accepted)

- [x] `python -m pytest tests -q` → 29 passed
- [x] `python scripts/validate_docs.py` → OK (22 required files, 0 warnings)
- [x] all 16 previous reports present under `archive/`, renamed only, content unmodified
- [x] no live runtime file modified (`git status` on the config directory: n/a, not a repo)
- [ ] owner review of the proposed live-pointer edit (pending)
- [ ] one golden task run and recorded under `evaluation/results/` (pending — OQ-006)

## Evidence

- FACT: 25/25 validator tests pass (this session).
- FACT: validators detect the exact failure class that motivated this ADR — see
  `tests/test_validate_docs.py::test_host_refs_flag_foreign_literal`.
- ASSUMPTION: the owner will keep maintaining the docs through the validators; if
  the gate is bypassed, drift returns. Impact if wrong: this ADR's main benefit is
  lost, no runtime harm.
