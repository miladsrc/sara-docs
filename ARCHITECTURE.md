# ARCHITECTURE.md - Sara Supervisor Agent

## Current Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    HUMAN (m.barani)                      │
│                    Final authority                       │
└─────────────────────┬───────────────────────────────────┘
                      │ consults / operates
                      ▼
┌─────────────────────────────────────────────────────────┐
│                    SARA (this agent)                     │
│                    External advisor                      │
│                    Zero execution rights                 │
│                    inside managed systems                │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Orchestrator │  │   Memory     │  │   Skills     │  │
│  │ (delegates)  │  │ (persistent) │  │ (read-only)  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────┬───────────────────────────────────┘
                      │ advises / documents
                      ▼
┌─────────────────────────────────────────────────────────┐
│              MANAGED SYSTEMS                             │
│              (ai-swe-engine, sara-v2, etc.)              │
│              Fully independent at runtime                │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ ai-swe-engine│  │   SARA v2    │  │   Other      │  │
│  │ (governance) │  │ (gateway)    │  │   projects   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Trust Boundaries

### Outer Boundary: Human <-> Sara
- Advisory only, no execution rights in either direction
- Sara can read code, docs, test results
- Sara cannot modify code, trigger runs, or approve merges

### Air-Gap Boundary
- Everything inside must function with zero internet access
- No cloud APIs, no external LLMs, no public registries
- Local LLM (Ollama) only

### Inner Boundary: LLM Output <-> Governance Engine
- No LLM output becomes approved without passing a deterministic gate
- LLMs produce content; deterministic code governs actions

## Component Responsibilities

| Component | Type | Responsibility | Trust Level |
|---|---|---|---|
| Human | External | Final authority on all irreversible decisions | Authoritative |
| Sara | External | Architecture advice, documentation, review | Advisory |
| ai-swe-engine | Deterministic + LLM | Governance, orchestration, code generation | Trusted (governance), Untrusted (LLM output) |
| SARA v2 | Deterministic + LLM | Gateway, approval pipeline, memory | Trusted (gateway), Untrusted (LLM output) |
