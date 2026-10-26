# SARA SYSTEM MAP

Version: 2026-08-30 | Round 2 discovery output (Phase 0)

## What Sara actually is (evidence, not assumption)

Sara is **not a standalone runtime binary**. On this machine (user `98903`,
opencode v1.18.25) Sara is the person loaded on top of the **opencode** agent
runtime:

```
opencode (the product/runtime)   ← supporting infrastructure, NOT Sara
  + ~/.config/opencode/AGENTS.md ← the persona + rules (Sara's instructions)
  + ~/.config/opencode/opencode.jsonc
  + ~/.config/opencode/skills/**
  + ~/.config/opencode/memory/**

= "Sara"
```

Memory in AGENTS.md references a **Sara v2 governed runtime** at
`C:\Users\m.barani\IdeaProjects\sara` (FastAPI :8800). Verified: not present on
this host (`Test-Path` = False everywhere, port 8800 down). Therefore the
operational system under inspection **is the opencode runtime + Sara's
config layer**. Changes to Sara's *runtime* = changes to opencode's config
surface (agents, commands, hooks/plugins, permissions).

---

## System tree

```text
Sara
│
├── Interface                 opencode TUI + CLI (v1.18.25), model opencode/big-pickle
│
├── Prompt / Instruction      ~/.config/opencode/AGENTS.md (96 lines)
│
├── Skill Layer               ~/.config/opencode/skills/ (3 skills)
│
├── Decision Layer            instruction-level only (Decision Ladder in AGENTS.md)
│
├── Task Classification       none (manual, per-call)
│
├── Orchestration             manual; ad-hoc delegation to Task tool
│
├── Subagents                 opencode built-ins (build / plan / general / explore)
│
├── Tool Layer                opencode built-ins (bash, read, edit, write, glob,
│                             grep, task, todowrite, question, webfetch, websearch)
│
├── Memory / State            ~/.config/opencode/memory/sara.md (manual append)
│
├── Model Layer               single model, no routing, no small_model
│
├── Execution                 opencode agent loop (single primary agent)
│
├── Verification              manual: self-review checklist + bash test/lint
│
├── Evaluation                none
│
└── Persistence / Feedback    memory/sara.md only; no feedback loop
```

---

## Component inventory

### Interface
- Location: opencode product (installed binary)
- Responsibility: user ↔ Sara conversation, tool I/O, sub-agent results
- Input: user messages; Output: agent responses
- Dependencies: opencode runtime
- Limitations: config not hot-reloaded (restart required after config edits)
- Extension points: TUI is a product feature, not extensible here

### Prompt / Instruction Layer
- Location: `~/.config/opencode/AGENTS.md` (96 lines)
- Responsibility: identity, persona, working rules, round-1 heuristics
- Input: loaded at session start; Output: behavioral context
- Dependencies: opencode auto-imports AGENTS.md
- Limitations: static instructions; no operational gating; grows context
- Extension points: `opencode.jsonc` `instructions[]`, additional AGENTS files

### Skill Layer
- Location: `~/.config/opencode/skills/`
- Inventory: `read-terminals`, `sara-review`, `sara-debt`
- Responsibility: reusable procedures injected on demand (L2 capabilities)
- Input: trigger phrases in user intent; Output: procedure guidance
- Dependencies: opencode skill registry
- Limitations: advisory; nothing enforces their use; no invocation metrics
- Extension points: new skill folders; `skills.paths` in config

### Decision Layer
- Location: AGENTS.md "Decision Ladder" (lines 27–54) — **instructions only**
- Responsibility: anti-overengineering reasoning heuristic
- Actual capability: none operational; Sara may or may not climb it per task
- Limitations: cannot force execution, cannot persist decisions, no routing
- Extension points: commands (invokable gates), plugins (enforcement)

### Task Classification
- Current: none. Every task handled identically by the same primary loop.
- Limitation: no structured class → no routing → no tiered review → no evidence

### Orchestration
- Current: manual, implicit. Sara decides at each message whether to act,
  delegate to Task tool, or ask the user.
- Limitation: no state machine, no mandated pipeline, no retry policy,
  no failure classification on the orchestration path

### Subagents
- Location: opencode built-ins `build` / `plan` / `general` / `explore`
- Responsibility: plan-mode (read-only), exploration, generic delegation
- Limitation: no architect / reviewer / auditor roles; no per-role permissions
- Extension points: `~/.config/opencode/agent/<name>.md` (mode, model,
  permission, prompt) — full documented surface

### Tool Layer
- Location: opencode built-ins: bash, read, edit, write, glob, grep, task,
  todowrite, question, webfetch, websearch
- Responsibility: all file, shell, search, web, and orchestration actions
- Limitation: no visibility into tool usage; e.g. redundant reads cannot be
  detected today
- Extension points: `permission.*` rules (autonomy gates), plugin hooks
  (`tool.execute.before/after` telemetry)

### Memory / State
- Location: `~/.config/opencode/memory/sara.md` (manual notes)
- Responsibility: cross-session continuity
- Limitation: manual append only, no structure, no per-task state, no telemetry
- Extension points: plugin state dir; opencode message/session persistence

### Model Layer
- Current: single model `opencode/big-pickle`; `small_model` not configured
- Limitation: no routing by task class (coding/reasoning/summarization)
- Extension points: `model` / `small_model`, per-agent `model`

### Execution
- Current: opencode primary agent loop
- Limitation: no decision gate before execution; executes whatever Sara decides

### Verification
- Current: manual — bash test/lint commands + AGENTS.md self-review checklist
- Limitation: no counterparty review for high-risk changes

### Evaluation
- Current: **none**. No task records, no before/after, no metrics.
- Limitation: cannot demonstrate improvement or regression

### Persistence / Feedback
- Current: memory/sara.md only
- Limitation: no decision records, no failure classification, no improvement loop

---

## Key boundary finding

Everything Sara "owns" is configuration loaded by opencode. There is no Sara
process to patch. The highest-value operational (L3/L4) changes available on
this runtime are:

1. **Commands** (`~/.config/opencode/command/`) — invokable operational gates
2. **Agents** (`~/.config/opencode/agent/`) — real routed roles with permissions
3. **Plugin hooks** (`opencode.jsonc` `plugin`) — runtime-side telemetry/enforcement
4. **Permissions** (`opencode.jsonc` `permission`) — autonomy / human control