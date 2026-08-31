# Sara Portable Knowledge Base

> **Version:** 2.0
> **Date:** 2026-08-26
> **Purpose:** Make Sara's knowledge portable across environments

---

## What This Is

This is a complete export of Sara's knowledge, identity, memory, and capabilities. It can be used to:

1. **Load Sara into a new environment** (new machine, new opencode instance)
2. **Restore Sara's context** after a system failure
3. **Transfer Sara's knowledge** to another operator
4. **Document Sara's state** at a point in time

---

## How to Use This Package

### Option 1: Load into opencode

1. Copy `memory/sara.md` to `~/.config/opencode/memory/sara.md`
2. Copy `config/AGENTS.md` to `~/.config/opencode/AGENTS.md`
3. Copy `skills/` to `~/.config/opencode/skills/`
4. Restart opencode

### Option 2: Load into SARA v2

1. Use `scripts/seed_memory.py` to load memory into pgvector
2. Copy `config/` to SARA v2 config directory
3. Restart SARA v2 stack

### Option 3: Manual Reference

Read the files in this package to understand Sara's context and continue her work.

---

## Package Contents

```
sara-portable/
├── README.md                    # This file
├── IDENTITY.md                  # Sara's identity and persona
├── MEMORY.md                    # Complete session history (77 lines, 2026-08-26)
├── CAPABILITIES.md              # Skills and agent roster
├── WORKING_RULES.md             # How Sara operates
├── PROJECT_CONTEXT.md           # Projects Sara has worked on
├── ARCHITECTURE_DECISIONS.md    # 10 ADRs
├── ARCHITECTURE.md              # Trust boundaries diagram
├── CHANGELOG.md                 # Documentation changelog
├── PORTABLE_KNOWLEDGE_BASE.md   # This file
├── config/
│   └── AGENTS.md               # opencode agent configuration
├── memory/
│   └── sara.md                 # Sara's persistent memory file (77 lines)
├── skills/
│   └── read-terminals/         # Terminal monitoring skill
│       ├── SKILL.md
│       └── read_terminals.py
└── scripts/
    └── load_sara.py            # Script to load Sara into new environment
```

---

## Quick Start

```bash
# 1. Clone this repo
git clone https://github.com/miladsrc/sara-docs.git

# 2. Load Sara's memory
cp sara-docs/memory/sara.md ~/.config/opencode/memory/sara.md

# 3. Load Sara's config
cp sara-docs/config/AGENTS.md ~/.config/opencode/AGENTS.md

# 4. Load Sara's skills
cp -r sara-docs/skills/* ~/.config/opencode/skills/

# 5. Restart opencode
# Sara is now loaded with full context
```

---

## What Sara Knows (As of 2026-08-26)

### Identity
- Sara is a supervisor meta-agent ("god agent")
- External to managed systems, never a runtime dependency
- Plans, delegates, monitors, verifies — never executes destructive actions
- SARA v2 is the default runtime for Level 1+ actions

### Projects Managed
- **ai-swe-engine**: Phase 0+1+Identity COMPLETE, Phase 2 SoD design COMPLETE + increment 1 done. 113+ tests passing. Version 0.2.0+
- **SARA v2**: MCP-based human-in-the-loop agent, Docker stack running at 127.0.0.1:8800
- **todo-cli**: Example project built by ai-swe-engine agents
- **todo-springboot**: Spring Boot example, 16 tests pass
- **demo-map-backend/frontend**: Map demo projects, MRPs green
- **game-agent**: Chrome Dino agent, score ~2400

### Key Decisions Made
- ADR-001: Sara is external to ai-swe-engine
- ADR-002: Master Development Plan is Source of Truth
- ADR-003: LLMs generate; deterministic software governs
- ADR-004: Human is final authority on all irreversible decisions
- ADR-005: Token auth now, OIDC deferred
- ADR-006: Sara v2 is default runtime
- ADR-007: Phase 1 bugs fixed
- ADR-008: Separation of Duties (Phase 2 SoD)
- ADR-009: Governance Dashboard as Client Layer
- ADR-010: Human Operating Layer deferred to Phase 9

### Current State
- ai-swe-engine: Phase 0+1+Identity COMPLETE, Phase 2 SoD design COMPLETE + increment 1
- SARA v2: Default runtime, Gateway pipeline active
- Memory: 77 lines of session history
- Tests: 113+ passing
- Version: 0.2.0+
- Latest commit: 69c93b9 (pushed to github miladsrc/ai-swe-engine)
- Dashboard: Live at /ui, zero-build vanilla JS
- SoD: SASE_SOD_MODE=legacy default, strict behind flag, E2E validated
- Phase 9: DEFERRED (Human Operating Layer)
- LLM: 100% local — qwen2.5-coder:7b via Ollama, no cloud dependencies

### Known Issues
- CRP endpoint can set run.status='blocked' bypassing assert_run_patchable (engine bug)
- MRP open_crp_ids snapshot misses post-MRP CRPs (display stale, safety holds)
- Blueprint table has no API endpoint — must INSERT directly into Postgres
- DNS poisoning risk: OpenVPN TAP adapter may re-assert on reconnect
- SMB client registry changes PENDING REVERT
