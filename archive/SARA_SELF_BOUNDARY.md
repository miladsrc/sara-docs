# SARA SELF BOUNDARY

Version: 2026-08-30 | Round 2 discovery output (Phase 1)

Defines what is "Sara" (modifiable as part of a self-upgrade) vs. everything
else (must not be touched by a self-upgrade).

## 1. SELF — components Sara may modify during a self-upgrade

| Component | Path | Rationale |
|-----------|------|-----------|
| Sara instructions | `~/.config/opencode/AGENTS.md` | Persona + working rules |
| Sara runtime config | `~/.config/opencode/opencode.jsonc` | opencode config that defines Sara's runtime surface |
| Sara skills | `~/.config/opencode/skills/**` | Reusable capabilities |
| Sara agents | `~/.config/opencode/agent/**` | Routed subagent roles (new) |
| Sara commands | `~/.config/opencode/command/**` | Invokable operational gates (new) |
| Sara plugin | `~/.config/opencode/plugin/**` | Runtime hooks (new) |
| Sara state/telemetry | `~/.config/opencode/state/**` | Evaluation + decision records (new) |
| Sara session memory | `~/.config/opencode/memory/sara.md` | Cross-session continuity |
| Sara self-docs repo | `C:\Users\98903\IdeaProjects\sara-docs\**` | Home of system map, reports, golden set |

## 2. SUPPORTING INFRASTRUCTURE — depends on, but not Sara

| Component | Path | Note |
|-----------|------|------|
| opencode product | installed binary | Its behavior is a given; only config surface is ours |
| opencode SDK/types | `~/.config/opencode/node_modules/**` | Used by the plugin; not Sara's own code |
| opencode session DB | `~/.local/share/opencode/**` | Read-only (read-terminals) |
| opencode itself's defaults | built-in agents/skills/config | Treat as platform capability |
| sara-docs/ponytail | nested git repo | Reference material only; not to be modified |

## 3. PROJECT CODE — Sara operates on, must NOT modify during self-upgrade

| Project | Purpose |
|---------|---------|
| milad platform | `C:\Users\m.barani\Downloads\milad\PROJECT_DOCUMENTATION\` (docs) |
| ai-swe-engine | IdeaProjects product (traceability engine) |
| todo-cli | ideaProjects agent workspace |
| first-test | Spring Boot experiments |
| game-agent | dino agent experiments |
| cvat_mlops + 5 Sahba repos | irrelevant to self-upgrade |

Self-upgrade never touches these. Deletion/addition there is normal dev work
(separate from self-modification), still subject to Sara's non-destructive rule.

## 4. USER CONFIGURATION — affects Sara, not Sara's implementation

| Component | Path |
|-----------|------|
| opencode global extras | `~/.config/opencode/tui.json` |
| auth provider config | opencode-managed credentials |
| user shell/OS settings | user-managed |

Do not change without explicit request. Back up before touching.

## Operational rule

Self-upgrade changes are limited to **SELF**. Any change to **Supporting
Infrastructure** is a platform build/upgrade (e.g. `npm install`), not a
self-upgrade. Any change to **Project Code** is normal engineering work.
**User Configuration** changes only on explicit request.

## Autonomy note

AGENTS.md rule: "any change to Sara's own configs/code requires a proposal +
explicit user approval first." Round 2 mission text approved performing the
upgrade, and explicit user confirmation ("do it" / "sara") followed. This
boundary doc is the scope gate for those approvals.