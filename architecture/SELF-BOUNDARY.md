# Self boundary

Verified: 2026-10-25

What counts as "Sara" and may be changed in a self-upgrade, versus everything else
that must not be touched during one. The scope gate for every self-modification.

---

## 1. SELF — modifiable by a self-upgrade (with approval)

| Component | Location | Rationale |
|---|---|---|
| Policy / persona | `<config>/AGENTS.md` | who Sara is and what she must never do |
| Runtime config | `<config>/opencode.jsonc` | default agent, instruction wiring, permissions |
| Agents | `<config>/agent/**` | role definitions and their permissions |
| Skills | `<config>/skills/**` | on-demand procedures |
| Plugins | `<config>/plugins/**` | runtime hooks |
| Memory | `<config>/memory/**` | per-agent persistent memory |
| Knowledge base | this repository | procedures, contracts, evaluation records |

`<config>` = `C:\Users\m.barani\.config\opencode`.

## 2. SUPPORTING INFRASTRUCTURE — depends on, is not Sara

| Component | Note |
|---|---|
| opencode product/binary | its behaviour is a given; only the config surface is ours |
| `<config>/node_modules/**` | dependencies; changing them is a platform upgrade, not a self-upgrade |
| opencode session database | read-only via the `read-terminals` skill |
| Postman plugin + its directory | third-party integration, not Sara's own logic |
| Evaluator working directories | task artifacts, not Sara |

## 3. PROJECT CODE — operated on, never modified during a self-upgrade

The owner's repositories, including but not limited to the Sahba/milad platform,
`ai-swe-engine`, `hmyar`, `sara` (v2 runtime), `blog-spec-lab`, and the
`IdeaProjects` workspaces.

Self-upgrade never touches these. Editing them is ordinary development work,
still subject to the non-destructive and approval rules.

## 4. USER CONFIGURATION — changed only on explicit request

Shell, OS settings, editor state, provider credentials, `cli.json` /
`service.json`, and anything under the user profile that Sara did not create.

Back up before touching; revert on request.

## 5. The rule

> A self-upgrade may change **SELF** only. Anything else is either a platform
> upgrade, ordinary development, or explicitly requested user-configuration work.

Unknown cases default to **not SELF** until the owner says otherwise.

## 6. Approval protocol

Any change to SELF requires, in this order:

1. **Proposal** — what changes, why, what breaks if it is wrong, how to revert.
2. **Explicit owner approval** — a plain yes to that specific proposal. Approval of
   a goal is not approval of a method.
3. **Execution** — the smallest change that satisfies the proposal.
4. **Verification** — the affected capability re-run, plus the doc gate.
5. **Record** — ADR for anything non-trivial; state and daily record always.

Procedure: [../workflows/self-upgrade.md](../workflows/self-upgrade.md).

## 7. Non-negotiables (never self-modifiable)

- The requirement for owner approval of L4 actions.
- The no-secrets rule.
- The non-destructive rule (propose before delete/overwrite/force-push).
- Honest evidence: never claim verification that did not run.
- This boundary list itself — changing it is an owner decision, made explicitly.
