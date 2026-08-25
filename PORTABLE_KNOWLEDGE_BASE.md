# Sara Portable Knowledge Base

> **Version:** 1.0
> **Date:** 2026-08-25
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
├── MEMORY.md                    # Complete session history
├── CAPABILITIES.md              # Skills and agent roster
├── WORKING_RULES.md             # How Sara operates
├── PROJECT_CONTEXT.md           # Projects Sara has worked on
├── ARCHITECTURE_DECISIONS.md    # Key architectural decisions made
├── config/
│   └── AGENTS.md               # opencode agent configuration
├── memory/
│   └── sara.md                 # Sara's persistent memory file
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

## What Sara Knows (As of 2026-08-25)

### Identity
- Sara is a supervisor meta-agent ("god agent")
- External to managed systems, never a runtime dependency
- Plans, delegates, monitors, verifies — never executes destructive actions

### Projects Managed
- **ai-swe-engine**: Phase 1 complete, 61 tests passing
- **SARA v2**: MCP-based human-in-the-loop agent, Docker stack running

### Key Decisions Made
- Sara is external to ai-swe-engine (ADR-001)
- Master Development Plan is Source of Truth
- 8 phases defined, Phase 1 complete
- LLMs generate; deterministic software governs

### Current State
- ai-swe-engine: Phase 1 complete, Phase 2 next
- Memory: 47 lines of session history
- Tests: 61 passing
- Version: 0.2.0
