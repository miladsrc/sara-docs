# PONYTAIL SELF-UPGRADE REPORT

## 1. Executive Summary

Deep study of Ponytail (v4.9.0) revealed a mature, benchmarked AI coding skill system
built around a simple but powerful idea: force agents to climb a decision ladder before
writing code, stopping at the first rung that works. The system is empirically validated
(-54% LOC, 100% safety) and ships across 20+ agent platforms.

**What was adopted:** The decision ladder as a reasoning heuristic, the `sara:` comment
convention for deliberate-shortcut tracking, and a structured self-review checklist.

**What was adapted:** Over-engineering review and technical debt tracking were redesigned
as Sara-native skills rather than copied from Ponytail's implementation.

**What was rejected:** Mode intensity system (premature for Sara's scope), the full
test/benchmark infrastructure (requires Node.js/promptfoo ecosystem), the 20+ adapter
pattern (Sara is single-platform), subagent propagation regex (not applicable to Task tool),
MCP server (Sara doesn't use MCP for injection), and the uninstall system.

**What materially changed:** AGENTS.md gained two new sections (Decision Ladder + Self-review),
two new skills were created (sara-review + sara-debt), and the `sara:` comment convention
is now the standard for marking deliberate shortcuts.

## 2. Baseline

### Sara's capabilities BEFORE the upgrade:

| Area | State |
|------|-------|
| **Identity** | Supervisor meta-agent, plans before acting, delegates to subagents |
| **Reasoning discipline** | No structured anti-overengineering heuristic |
| **Code review** | No specialized review capability; general-purpose exploration |
| **Technical debt** | No tracking mechanism for deliberate shortcuts |
| **Self-review** | No structured checklist before delivering work |
| **Skills** | 1 skill (read-terminals) |
| **Memory** | Persistent cross-session in memory/sara.md |
| **Subagents** | Task tool with explore/general types |
| **Architecture** | Sara v1 (opencode, front-end) + Sara v2 (governed runtime) |
| **Benchmarking** | None |
| **Audit capability** | None |

## 3. Ponytail Capability Inventory

| Capability | Source | Problem Solved | Mechanism | Current Equivalent | Value | Risk | Decision |
|------------|--------|----------------|-----------|-------------------|-------|------|----------|
| 7-rung decision ladder | AGENTS.md + SKILL.md | Over-engineering | Structured heuristic before code generation | None | HIGH | Low | ADOPT |
| `ponytail:` comment convention | AGENTS.md + SKILL.md | Deliberate shortcut tracking | Code comment taxonomy + grep harvest | None | HIGH | Low | ADOPT |
| Over-engineering review | ponytail-review/SKILL.md | Complexity in diffs | 5-tag system (delete/stdlib/native/yagni/shrink) | None | HIGH | Low | ADAPT |
| Technical debt ledger | ponytail-debt/SKILL.md | Forgotten deferrals | Grep + ledger + no-trigger flagging | None | HIGH | Low | ADAPT |
| Self-review checklist | AGENTS.md | Premature/generalized solutions | 7-question silent checklist | None | MEDIUM | Low | ADOPT |
| Mode intensity (lite/full/ultra) | SKILL.md frontmatter | Graduated enforcement | Per-line Markdown filtering at injection time | None | MEDIUM | HIGH | DEFER |
| Gain scoreboard | ponytail-gain/SKILL.md | Showing measured impact | ASCII bars from benchmark medians | None | LOW | Low | REJECT |
| Help reference card | ponytail-help/SKILL.md | Discoverability | Quick reference listing | None | LOW | Low | REJECT |
| Whole-repo audit | ponytail-audit/SKILL.md | Accumulated complexity | Repo-wide scan, ranked findings | None | MEDIUM | MEDIUM | DEFER |
| Agentic benchmarks | benchmarks/agentic/ | Measuring agent improvement | Real Claude Code sessions + scorers | None | HIGH | HIGH | DEFER |
| Correctness gates | benchmarks/correctness.js | Functional correctness validation | Per-task assertion runners | None | MEDIUM | HIGH | DEFER |
| Behavior gates | benchmarks/behavior.js | Proving refined behaviors | Heuristic checkers | None | MEDIUM | HIGH | DEFER |
| LLM judges | judge.py + complete.py | Over-engineering/completeness scoring | Rubric-based LLM evaluation | None | MEDIUM | HIGH | DEFER |
| Subagent propagation | ponytail-subagent.js | Rules in spawned agents | SubagentStart hook + regex scoping | None (Task tool has no hook) | MEDIUM | MEDIUM | REJECT |
| 20+ platform adapters | .cursor/, .windsurf/, etc. | Cross-platform portability | Thin adapter files per platform | N/A (Sara is single-platform) | NONE | HIGH | REJECT |
| Shared instruction builder | ponytail-instructions.js | Single source of truth for adapters | JS module + mode filtering | None | LOW | MEDIUM | INSPIRED-BY |
| Rule-copy consistency checker | check-rule-copies.js | Drift between adapter copies | Script verifying byte-identical rules | N/A (single platform) | NONE | NONE | REJECT |
| Version consistency checker | check-versions.js | Stale version across manifests | Script checking 8 files for same semver | N/A (single platform) | NONE | NONE | REJECT |
| Deactivation protocol | ponytail-config.js | Accidental mode deactivation | Whole-message match for "stop ponytail" | None | LOW | Low | INSPIRED-BY |
| Uninstall system | scripts/uninstall.js | State cleanup outside plugin dir | Script removing flag files + config | N/A | NONE | NONE | REJECT |
| MCP server | ponytail-mcp/ | Context injection via MCP prompts/tools | MCP SDK server | None (Sara uses AGENTS.md) | NONE | NONE | REJECT |

## 4. Adopted Capabilities

### 4.1 Decision Ladder (anti-overengineering)

- **Name:** Decision Ladder
- **Source:** Ponytail's 7-rung YAGNI-first framework
- **Original problem:** LLMs over-engineer by default — installing dependencies, building custom components, creating abstractions nobody asked for
- **Adaptation:** Integrated as a permanent section in AGENTS.md. Adapted the examples to be language-agnostic (Java/Python/JS) rather than web-specific. Added the `sara:` comment convention (replacing `ponytail:`).
- **Implementation location:** `~/.config/opencode/AGENTS.md` lines 27-54
- **Reason:** Sara routinely writes code across Java microservices, Python scripts, and JS projects. Without a structured anti-overengineering heuristic, there's no consistent guardrail against unnecessary complexity. The ladder forces reasoning before implementation.
- **Validation:** The AGENTS.md is loaded at session start via opencode's auto-discovery. The decision ladder section is always in context. Validated by reading back the file and confirming structure.
- **Impact:** Every code generation task will now pass through 7 progressively more complex options before actually writing code. This is the highest-impact change.

### 4.2 Self-review Checklist

- **Name:** Self-review
- **Source:** Ponytail's implicit self-review behavior (not a separate skill, embedded in the persona)
- **Original problem:** Agents deliver without checking if they solved the actual requirement or introduced unnecessary complexity
- **Adaptation:** Extracted into a standalone 7-question checklist section in AGENTS.md. Questions are adapted to Sara's context (includes dependency check, unrelated file modification check).
- **Implementation location:** `~/.config/opencode/AGENTS.md` lines 56-67
- **Reason:** Sara operates as a supervisor. Supervisors must verify before delivering. Without a structured checklist, self-review is inconsistent.
- **Validation:** AGENTS.md loaded at session start. Checklist is always in context.
- **Impact:** Every implementation will be silently checked against 7 criteria before delivery. Only material findings surface to the user.

### 4.3 `sara:` Comment Convention

- **Name:** sara: comment convention
- **Source:** Ponytail's `ponytail:` comment taxonomy
- **Original problem:** Deliberate shortcuts and deferrals silently become permanent technical debt
- **Adaptation:** Renamed from `ponytail:` to `sara:`. Same structure: `sara: <ceiling>, <upgrade path>`. Integrated into the Decision Ladder rules section.
- **Implementation location:** `~/.config/opencode/AGENTS.md` line 53
- **Reason:** When Sara intentionally uses a suboptimal approach (e.g., global lock instead of per-account, O(n²) scan for small datasets), marking it creates a searchable, trackable record. Without this, "good enough for now" becomes "forgotten forever."
- **Validation:** Convention is defined in AGENTS.md. The sara-debt skill can harvest these comments.
- **Impact:** Every deliberate shortcut becomes traceable. Future sessions can discover and upgrade them.

## 5. Inspired-by Capabilities

### 5.1 Over-engineering Review Skill (sara-review)

- **What it is:** A specialized code review skill that ONLY hunts over-engineering, not bugs or security. Uses a 5-tag taxonomy (delete/stdlib/native/yagni/shrink) with strict one-line-per-finding format.
- **How it was redesigned:** Ponytail's review is tightly coupled to its mode system and slash commands. Sara's version is a standalone skill with no mode dependency. The format, tags, and scoring are preserved because they're genuinely good design. Removed the "stop ponytail-review" deactivation (Sara doesn't have mode switching).
- **Key design decision:** Kept the tag system exactly as Ponytail designed it. The tags (delete/stdlib/native/yagni/shrink) are a compact, precise taxonomy. Redesigning them would be change for change's sake.
- **Location:** `~/.config/opencode/skills/sara-review/SKILL.md`

### 5.2 Technical Debt Tracking Skill (sara-debt)

- **What it is:** A skill that greps for `sara:` comments in the codebase, extracts ceiling and upgrade path, and produces a ledger with no-trigger flagging.
- **How it was redesigned:** Ponytail's debt skill is tightly coupled to `ponytail:` markers and its slash command system. Sara's version uses `sara:` markers and is a standalone skill. The scan mechanism (grep), output format (grouped by file), and rot-risk flagging are preserved because they're correct.
- **Key design decision:** Added `/*` comment prefix to the grep pattern since Sara works with Java (Spring Boot) where block comments are common. Ponytail only supports `#` and `//`.
- **Location:** `~/.config/opencode/skills/sara-debt/SKILL.md`

### 5.3 Deactivation Protocol Concept

- **What it is:** Whole-message matching for "stop" commands to prevent accidental deactivation when the phrase appears in user messages.
- **How it was inspired:** Sara doesn't have mode switching, so this wasn't directly implemented. However, the principle is now embedded: the `sara:` convention only triggers when it's an intentional annotation, not when the word "sara" appears in code comments.

## 6. Rejected Capabilities

### 6.1 Mode Intensity System (lite/full/ultra)

- **Why Ponytail has it:** Graduated enforcement allows users to dial up/down the anti-overengineering pressure. Useful for "I need a quick prototype, don't be strict" vs "I need production-quality, be ruthless."
- **Why it was rejected:** Sara is a supervisor meta-agent, not a code generation tool. Sara delegates code generation to subagents or Sara v2. Adding mode switching to Sara's core would create unnecessary complexity (3 modes x rule variations x state management). The decision ladder in AGENTS.md is always-on, which is correct for a supervisor.
- **Risk if adopted:** Mode proliferation, state management complexity, user confusion about which mode is active.

### 6.2 Agentic Benchmarks + Correctness Gates + LLM Judges

- **Why Ponytail has them:** Empirical validation that the skill actually works. Published -54% LOC, 100% safety numbers.
- **Why they were rejected:** Requires Node.js + promptfoo + Anthropic API key + isolated workspaces. Sara's evaluation model is different — Sara is evaluated by m.barani on task outcomes, not by automated benchmarks. The infrastructure cost is high and the payoff is low for Sara's use case.
- **Future consideration:** If Sara ever needs to measure her own code generation quality, a simplified benchmark could be built using the existing ai-swe-engine test infrastructure.

### 6.3 20+ Platform Adapters

- **Why Ponytail has them:** Distribution across every AI coding platform.
- **Why they were rejected:** Sara runs on opencode only. The adapter pattern solves a problem Sara doesn't have.

### 6.4 Subagent Propagation (SubagentStart hook)

- **Why Ponytail has it:** SessionStart context doesn't reach subagents in Claude Code. Without propagation, subagents run without the ruleset.
- **Why it was rejected:** Sara's Task tool creates subagents that inherit the AGENTS.md context automatically. There's no propagation gap. Adding a hook mechanism would be solving a non-problem.

### 6.5 Whole-Repo Audit (ponytail-audit)

- **Why Ponytail has it:** One-shot scan of entire codebase for accumulated over-engineering.
- **Why it was deferred:** Sara doesn't currently audit codebases. The sara-review skill handles diff-level review. A whole-repo audit is a different capability that requires understanding the entire codebase context, which is a significant scope expansion. Deferred until a real need arises.

## 7. Deferred Capabilities

### 7.1 Mode Intensity System

Could be valuable if Sara's scope expands to direct code generation (not just supervision). If Sara starts writing code directly, having lite/full/ultra modes would allow graduated enforcement. Deferred because Sara currently delegates code generation.

### 7.2 Whole-Repo Audit

Could be valuable for the ai-swe-engine project. The sara-review skill handles diffs; a repo-wide audit is a natural extension. Deferred because it requires understanding the full codebase, not just changes.

### 7.3 Benchmarking Infrastructure

Could be valuable if Sara needs to measure her own improvement over time. The ai-swe-engine already has a test suite (61 tests). A benchmark that measures code quality, LOC, and correctness across sessions would be useful but requires significant infrastructure. Deferred because the current evaluation model (human judgment by m.barani) is sufficient.

### 7.4 Self-improvement Memory Hooks

Ponytail's `ponytail:` convention creates a feedback loop: shortcuts are marked, tracked, and eventually upgraded. Sara's memory system (sara.md) could be enhanced with automatic debt discovery on session start. Deferred because the sara-debt skill already provides this on-demand.

## 8. Architecture Changes

### Skills

| Before | After |
|--------|-------|
| `read-terminals` (1 skill) | `read-terminals`, `sara-review`, `sara-debt` (3 skills) |

### Rules (AGENTS.md)

| Before | After |
|--------|-------|
| 54 lines | 96 lines (+42 lines) |
| Identity + Standing context + Working rules + v2 bridge | + Decision Ladder + Self-review checklist |

### Hooks

No changes. Sara doesn't use hooks (opencode loads AGENTS.md automatically).

### Workflows

No changes. Sara's workflow is unchanged; the new capabilities are reasoning improvements, not process changes.

### Subagents

No changes. Subagent behavior is unchanged; the decision ladder applies to Sara's own reasoning, not to subagent instructions.

### Evaluation

No objective measurement capability added. NOT MEASURED.

### Audit

No audit capability added. The sara-review skill provides diff-level over-engineering review. Whole-repo audit is deferred.

### Debt Management

Added `sara:` comment convention + sara-debt skill. This is a new capability: deliberate shortcuts are now trackable and harvestable.

### Context Management

AGENTS.md grew by 42 lines (78% increase). This is a permanent context cost on every session. The decision ladder (~25 lines) and self-review checklist (~12 lines) are always in context. This is justified because they affect every code generation task.

## 9. New Capabilities

| New Capability | Purpose | Trigger | Scope | Implementation | Validation |
|----------------|---------|---------|-------|----------------|------------|
| Decision Ladder | Force anti-overengineering reasoning before code generation | Always active (AGENTS.md) | Every code task | AGENTS.md section | File read-back confirmed |
| Self-review Checklist | Verify implementation quality before delivery | Always active (AGENTS.md) | Every implementation | AGENTS.md section | File read-back confirmed |
| sara: comment convention | Mark deliberate shortcuts for tracking | When intentionally cutting corners | Code changes | AGENTS.md rule + sara-debt harvest | sara-debt skill can grep |
| sara-review | Over-engineering review of diffs | "sara review", "review for over-engineering" | Diff-level changes | sara-review/SKILL.md | Skill file present + formatted |
| sara-debt | Harvest sara: comments into debt ledger | "sara debt", "list the shortcuts" | Whole codebase | sara-debt/SKILL.md | Skill file present + formatted |

## 10. Behavioral Changes

### Before: Sara writes code immediately
Sara would receive a task, think about it, and start implementing. There was no structured reasoning about whether simpler solutions existed.

### After: Sara climbs the decision ladder first
Sara now has a mandatory 7-step reasoning process before writing code. She will question whether the feature needs to exist, check if it already exists, check stdlib, check native features, check installed dependencies, try to make it one line, and only then write minimum code.

### Before: Sara delivers without self-checking
Sara would implement and deliver without a structured quality check.

### After: Sara runs a silent self-review
Sara now checks 7 criteria before delivering: actual requirement solved, no unnecessary complexity, no unnecessary dependencies, no unrelated file changes, implementation is reducible, no duplication, simplest correct solution.

### Before: Deliberate shortcuts were invisible
When Sara used a suboptimal approach (global lock, O(n²) scan), there was no mechanism to track it.

### After: Shortcuts are marked with `sara:` comments
Every deliberate shortcut now has a `sara: <ceiling>, <upgrade path>` annotation. The sara-debt skill can harvest these into a ledger.

### Before: No specialized review capability
Sara had no mechanism to review code for over-engineering specifically.

### After: sara-review skill available
Sara can now review diffs using the 5-tag over-engineering taxonomy (delete/stdlib/native/yagni/shrink) with strict one-line-per-finding format.

## 11. Before vs After

| Area | Before | After | Evidence |
|------|--------|-------|----------|
| Reasoning discipline | Ad-hoc, no structured heuristic | 7-rung decision ladder forces anti-overengineering reasoning | AGENTS.md lines 27-54 |
| Implementation discipline | No checklist | 7-question silent self-review before delivery | AGENTS.md lines 56-67 |
| Code review | No specialized capability | sara-review skill with 5-tag taxonomy | sara-review/SKILL.md |
| Technical debt | No tracking | `sara:` convention + sara-debt harvest skill | AGENTS.md line 53 + sara-debt/SKILL.md |
| Skill count | 1 | 3 | skills/ directory |
| AGENTS.md size | 54 lines | 96 lines | File read |

## 12. Measurement

### Objective metrics

| Metric | Before | After | Measured? |
|--------|--------|-------|-----------|
| AGENTS.md lines | 54 | 96 | YES (+42, +78%) |
| Skills count | 1 | 3 | YES (+2) |
| Code review capability | None | sara-review | YES (skill exists) |
| Debt tracking | None | sara-debt + sara: convention | YES (skill exists + rule defined) |
| Decision ladder | None | 7-rung heuristic | YES (section exists) |
| Self-review checklist | None | 7-question checklist | YES (section exists) |

### Qualitative assessment

| Area | Assessment |
|------|------------|
| Reasoning improvement | QUALITATIVE: Decision ladder forces structured anti-overengineering reasoning before code generation. Impact depends on how consistently it's applied. |
| Coding discipline | QUALITATIVE: Self-review checklist provides a structured quality gate before delivery. |
| Architecture quality | NOT MEASURED: No objective way to measure architecture quality change. |
| Self-review | QUALITATIVE: Structured 7-question checklist replaces ad-hoc self-checking. |
| Repository audit | NOT MEASURED: No audit capability was added (deferred). |
| Technical debt management | QUALITATIVE: `sara:` convention + debt skill creates a trackable, harvestable debt ledger. |
| Agent orchestration | NOT MEASURED: No changes to subagent behavior. |
| Context efficiency | NEGATIVE: AGENTS.md grew 78%, adding permanent context cost. Justified by impact on every code task. |
| Evaluation capability | NOT MEASURED: No benchmarking infrastructure added. |

## 13. Risks

### Over-minimization
The decision ladder could push toward insufficient implementation if applied too rigidly. Mitigation: Rung 7 ("minimum code that works") explicitly allows writing code when simpler options don't exist. The ladder stops at the first rung that works, not at the cheapest option.

### Under-engineering
Aggressive YAGNI could lead to missing necessary abstractions. Mitigation: The decision ladder runs "after understanding the problem, not instead of it." Rung 1 questions whether the feature needs to exist, not whether it should be well-designed.

### Inappropriate YAGNI
The "does this need to exist?" rung could be misapplied to reject necessary features. Mitigation: The ladder is a heuristic, not a rule. Sara is a supervisor who understands context; the ladder is a tool, not a mandate.

### Context complexity
AGENTS.md grew 78%. This is a permanent context cost. Mitigation: The added content is directly actionable (decision ladder affects every code task, self-review affects every delivery). No speculative content was added.

### Skill proliferation
Two new skills were added (sara-review, sara-debt). Risk of skill sprawl. Mitigation: Both skills serve distinct, non-overlapping purposes. review = diff-level complexity hunting. debt = whole-codebase shortcut tracking. No further skills were added.

### False-positive audits
sara-review could flag necessary complexity as over-engineering. Mitigation: The skill explicitly states scope is "over-engineering and complexity only" and that correctness/security/performance are out of scope.

### Excessive self-review
The 7-question checklist could slow down delivery. Mitigation: The checklist runs "silently" — only material findings surface. Trivial implementations pass all 7 checks instantly.

## 14. Final Verdict

| Dimension | Score | Explanation |
|-----------|-------|-------------|
| Reasoning Improvement | 7/10 | Decision ladder is a genuine reasoning structure. Not a 10 because it's a heuristic, not a guarantee — the LLM can still ignore it. |
| Coding Discipline | 6/10 | Self-review checklist adds structure. Not higher because discipline depends on consistent application, which is hard to verify. |
| Architecture Quality | 5/10 | Minimal changes to architecture. Skills are well-structured but small in number. |
| Self-Review | 7/10 | Structured 7-question checklist is a real improvement over ad-hoc checking. |
| Repository Audit | 2/10 | No audit capability added. sara-review handles diffs only. Deferred. |
| Technical Debt Management | 7/10 | `sara:` convention + debt skill creates a real, trackable debt ledger. Genuine capability addition. |
| Agent Orchestration | 3/10 | No changes to subagent behavior. Decision ladder applies to Sara only. |
| Context Efficiency | 4/10 | AGENTS.md grew 78%. Justified but not free. |
| Evaluation Capability | 1/10 | No benchmarking added. NOT MEASURED. |
| **Overall Improvement** | **5/10** | Meaningful improvements in reasoning, self-review, and debt management. Deliberately conservative — only adopted what was clearly valuable and low-risk. |

## 15. EXACT SUMMARY FOR THE USER

## What I Added To Myself

### Decision Ladder (anti-overengineering)

- **What it does:** Forces a 7-step reasoning process before writing code: (1) Does it need to exist? (2) Already in codebase? (3) Stdlib? (4) Native platform? (5) Installed dependency? (6) One line? (7) Minimum code.
- **Why I added it:** I had no structured heuristic for anti-overengineering. I would sometimes install dependencies, build custom components, or create abstractions when simpler solutions existed.
- **What changed in my behavior:** I now climb the ladder before every code generation task. I stop at the first rung that works instead of jumping to implementation.
- **Where it lives:** `~/.config/opencode/AGENTS.md` lines 27-54
- **How it was validated:** File read-back confirmed correct structure and placement.

### Self-review Checklist

- **What it does:** 7-question silent checklist before delivering any implementation: actual requirement solved, no unnecessary complexity, no unnecessary dependencies, no unrelated file changes, implementation is reducible, no duplication, simplest correct solution.
- **Why I added it:** I had no structured quality gate before delivery. Self-review was inconsistent.
- **What changed in my behavior:** I now silently check 7 criteria before delivering. Only material findings surface to the user.
- **Where it lives:** `~/.config/opencode/AGENTS.md` lines 56-67
- **How it was validated:** File read-back confirmed correct structure.

### sara: Comment Convention

- **What it does:** When I intentionally cut a corner (global lock, O(n²) scan, naive heuristic), I mark it: `sara: <ceiling>, <upgrade path>`. The sara-debt skill can harvest these into a ledger.
- **Why I added it:** Deliberate shortcuts were invisible. "Good enough for now" became "forgotten forever."
- **What changed in my behavior:** Every intentional shortcut now has a trackable annotation with its known limits and upgrade trigger.
- **Where it lives:** `~/.config/opencode/AGENTS.md` line 53
- **How it was validated:** Convention defined in AGENTS.md; sara-debt skill can grep for it.

### sara-review Skill

- **What it does:** Reviews diffs for over-engineering using 5 tags: delete (dead code), stdlib (reinvented standard library), native (dependency doing what platform does), yagni (speculative abstraction), shrink (same logic fewer lines). One line per finding with net line savings.
- **Why I added it:** I had no specialized review capability for complexity. General-purpose review doesn't specifically hunt over-engineering.
- **What changed in my behavior:** I can now review code changes specifically for unnecessary complexity, separate from correctness/security review.
- **Where it lives:** `~/.config/opencode/skills/sara-review/SKILL.md`
- **How it was validated:** Skill file present, correctly formatted with YAML frontmatter, tags, examples, scoring, and boundaries.

### sara-debt Skill

- **What it does:** Greps for `sara:` comments across the codebase, extracts ceiling and upgrade path from each, flags markers with no upgrade trigger as rot risk, and produces a ledger grouped by file.
- **Why I added it:** Without harvesting, `sara:` comments would accumulate without being tracked. The debt skill makes deferrals visible and actionable.
- **What changed in my behavior:** I can now produce a debt ledger on demand showing all deliberate shortcuts, their limits, and upgrade triggers.
- **Where it lives:** `~/.config/opencode/skills/sara-debt/SKILL.md`
- **How it was validated:** Skill file present, correctly formatted with YAML frontmatter, scan mechanism, output format, and boundaries.

---

**Upgrade performed:** 2026-08-30
**Source repository:** https://github.com/DietrichGebert/ponytail (v4.9.0)
**Agent:** Sara (opencode, mimo-v2-free)
**Files modified:** AGENTS.md (+42 lines)
**Files created:** skills/sara-review/SKILL.md, skills/sara-debt/SKILL.md
**Total new capabilities:** 5 (Decision Ladder, Self-review, sara: convention, sara-review, sara-debt)
