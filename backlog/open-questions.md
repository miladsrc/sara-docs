# Open questions

Things that are unknown, unapproved, or blocked. Each has an owner and a
severity. An open question is never resolved by assumption — it is resolved by
an answer, recorded here and then promoted into a living doc.

Severity: **blocks** work cannot proceed · **shapes** work proceeds but may need
redoing · **minor** cosmetic or deferrable.

---

## OQ-001 — Should the live runtime config be git-tracked again?

**Severity:** shapes · **Owner:** m.barani · **Raised:** 2026-10-25

`archive/SARA-DECISIONS.md` DECISION 001 decided to version
`C:\Users\m.barani\.config\opencode` in place. Verified 2026-10-25: it is **not
a git repository**, so that decision is currently unenforced — there is no
history and no rollback for agent, skill, or config changes.

Options: (a) re-initialize a local-only repo with a curated `.gitignore`
(`state/`, `node_modules/`, `postman-plugin/`, backups); (b) keep manual backups;
(c) track only the text surface (`agent/`, `skills/`, `AGENTS.md`,
`opencode.jsonc`, `memory/`) and leave plugins untracked.

Note: the config directory holds memory files containing internal hostnames and
infrastructure prose. A remote would raise this to a credential-exposure decision.

## OQ-002 — Is there any telemetry at all?

**Severity:** shapes · **Owner:** m.barani · **Raised:** 2026-10-25

`archive/SARA_TELEMETRY_CONTRACT.md` specifies an event interface produced by a
plugin into `state/tool-events.ndjson`. Verified: no `state/` directory and no
producing plugin exist on this host. Evaluation currently cannot measure tool
calls, iterations, or cost.

Options: (a) build a minimal telemetry plugin; (b) evaluate from transcripts
manually and label results OBSERVED instead of MEASURED; (c) declare evaluation
out of scope and delete the contract to stop it from implying capability.

## OQ-003 — Do we want slash-command gates?

**Severity:** minor · **Owner:** m.barani · **Raised:** 2026-10-25

The archived design relies on `/sara-decide`, `/sara-review`, `/sara-audit`,
`/sara-eval` living in `command/`. That directory does not exist, so no gate is
invokable — the rules live only in prose that an agent may or may not follow.

Options: (a) create `command/` with 2-3 gates that matter (decide, review,
eval); (b) rely on the workflow playbooks and skip commands; (c) both, with
commands as shortcuts into the playbooks.

## OQ-004 — Why does `hmyar` have no memory file?

**Severity:** minor · **Owner:** m.barani · **Raised:** 2026-10-25

There are 14 agent definitions but 13 memory files; `hmyar` is the odd one out,
even though its own definition mandates loading state from the `hmyar` repo. Is
the missing file intentional (state lives in the project repo) or an oversight?

## OQ-005 — Where does the Hamtayar implementation plan belong?

**Severity:** minor · **Owner:** m.barani · **Raised:** 2026-10-25

`archive/HAMTYAR_PHASED_IMPLEMENTATION_PLAN.md` is a 16 KB plan for the Hamtayar
project, not for Sara. It was frozen into `archive/` per the freeze-everything
decision, but it arguably belongs in the `hmyar` repository where the project's
memory and workflows already live.

Options: (a) move it to `C:\Users\m.barani\IdeaProjects\hmyar` as a project
deliverable; (b) keep a copy here as an external-project reference; (c) leave in
`archive/`.

## OQ-006 — What is the actual acceptance bar for Sara's output?

**Severity:** shapes · **Owner:** m.barani · **Raised:** 2026-10-25

`evaluation/GOLDEN-TASKS.md` defines probe tasks but no pass threshold. Without a
threshold, "better" is unfalsifiable and every self-assessment is opinion.

Options: (a) define per-class minimums (e.g. deterministic tasks must be correct
and add zero dependencies); (b) compare against a human baseline on the same
task; (c) treat any regression against a recorded prior run as failure.

---

## Resolved

(none yet — resolved questions are moved here with the answer and the doc that
now owns them)
