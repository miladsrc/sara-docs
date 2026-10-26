# Lessons learned

Reusable lessons that should change future behavior. Not a changelog — if a
lesson does not alter what Sara does next time, it belongs in `daily/` instead.

---

## L1 — Documentation without a checker rots silently

**Date:** 2026-10-25 · **Source:** restructure of this repo

Sixteen reports claimed a host user, an opencode version, a git-tracked config,
four slash commands, a plugin, a test suite, and three skills. Verified on the
current host: none of those were true. Nothing failed loudly, because nothing
checked.

**Rule:** a factual claim in a doc must be machine-checkable or dated. Absolute
paths in backticks must exist; links must resolve; no foreign host names.
Enforced by `scripts/validate_docs.py`.

## L2 — Reports describe the past; playbooks govern the future

**Date:** 2026-10-25 · **Source:** same

A repo full of analysis reports reads as maturity while providing no procedure.
The highest-value doc is one an agent can execute step by step with a pass/fail
gate at each stage.

**Rule:** when documenting a capability, write the procedure and the gate, not
the narrative of having done it once.

## L3 — "Never claim a test passed if not run" needs to be structural

**Date:** 2026-10-25 · **Source:** archive review

Prose rules against overclaiming did not prevent eight stale claims. Structural
rules (validators, dated verification lines, MEASURED vs OBSERVED labels) do.

**Rule:** prefer enforcement over exhortation. If a rule matters, find the check
that fails when it is broken.

## L4 — Adopt a proven pattern instead of inventing a structure
**Date:** 2026-10-25 · **Source:** `IdeaProjects\hmyar`

The `hmyar` repository already implemented memory/, workflows/, backlog/,
validating scripts, and CI. Designing a bespoke structure for Sara would have
produced a second, differently-shaped convention for the same problem.

**Rule:** before designing an information architecture, check whether one already
exists in the owner's projects and reuse its shape.

## L5 — A session-start inventory goes stale within the hour

**Date:** 2026-10-25 · **Source:** live surface changed mid-session

The runtime skill set went from 1 to 9 skills while this session was running. The
inventory written at session start became a false statement before the session
ended — through no fault of the inventory.

**Rule:** re-verify the live surface before *reporting* facts about it, not only
before acting on it. When a fact is load-bearing, its verification timestamp is
part of the fact.

## L6 — A rule that forbids naming a problem blocks its own correction

**Date:** 2026-10-25 · **Source:** two rounds of validator findings on this repo

A rule against foreign host references rejected the correction table whose purpose
was to name the foreign host. A rule against credential-shaped strings rejected
test fixtures for the credential scanner. Both times the tempting fix was to
delete the evidence.

**Rule:** every prohibition needs a declared, reviewable escape for the case that
documents the prohibition itself. Make the escape explicit (a named file list, a
per-line marker) so using it is a visible act, and test that it is not a wildcard.

## L7 — Short paths break directory changes on this host

**Date:** 2026-10-25 · **Source:** G5 run

`$env:TEMP` expands to `C:\Users\M4436~1.BAR\...`; `Set-Location` rejects it, so a
script that "changes into the sandbox" silently keeps the previous working
directory and writes there. In this case, four files landed in a git repository
root.

**Rule:** never `Set-Location` into a path derived from an environment variable.
Pass an explicit working directory to the command instead, and verify the target
after writing.

