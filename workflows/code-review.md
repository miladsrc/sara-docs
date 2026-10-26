# Workflow — Code review

Reviewing a diff, plan, or design. Review tiers and gates are defined in
[../architecture/OPERATING-MODEL.md](../architecture/OPERATING-MODEL.md); this
file owns the **method**.

The reviewer's job is not to approve. It is to find what the author could not see,
and to say plainly what was and was not verified.

---

## Rules of the role

1. **Independence.** The author may not perform a tier 2+ review of their own
   work. If asked to, say so and decline.
2. **Fresh eyes, no narrative.** Review the diff and the requirement — not the
   author's explanation of what it does. If the diff needs the explanation to be
   correct, that is a finding.
3. **Verdict required.** One of: **APPROVE**, **APPROVE WITH COMMENTS**,
   **REQUEST CHANGES**, **BLOCK**. No verdict is not a review.
4. **Verify before asserting.** If you claim a test would fail, run it. If you
   claim a convention is violated, quote the convention and its location.
5. **Severity on every finding.** Blocking / should-fix / nit. Nits never block.

## What to check, in this order

### 1. Does it do what was asked?

- Compare against the stated requirement and non-goals.
- Anything extra in the diff is a finding (scope creep), regardless of quality.
- Anything missing from the requirement is a blocking finding.

### 2. Does it handle the edges?

Failing case first: empty input, null/absent, single element, huge input,
concurrent access, unicode, timezone, zero and negative numbers, partial failure,
retry after partial success.

### 3. Is the failure behaviour safe?

- Does an error path leave state consistent, or half-written?
- Does it fail closed for anything security-relevant?
- Are resources closed on the error path?
- Are exceptions swallowed where the caller needed to know?

### 4. Security

- Any secret, token, or credential in the diff: **BLOCK**.
- Authorization checked at the authoritative point, not the UI?
- Every user-controlled value reaching a query, path, shell, or template?
- Injection, traversal, deserialization, SSRF surfaces touched?
- For anything access-control related, dispatch
  [`security`](../roster/README.md) — do not self-assess.

### 5. Tests

- Do the tests test the requirement, or the implementation's current shape?
- Is the happy path the only path covered?
- Was the regression test actually observed failing (bugfixes)?
- Are assertions specific enough to fail when the code is wrong?

### 6. Convention

- Consistent with surrounding code: naming, error handling, layering, logging.
- New dependency: justified, maintained, and necessary? Any dependency added for
  convenience is a should-fix.
- Dead code, commented-out code, debug output, TODOs without an owner.

### 7. Understandability

- Can a newcomer follow the control flow without the author present?
- Are the non-obvious decisions explained at the point they occur?
- Is anything clever where plain would do?

## How to report

```
VERDICT: REQUEST CHANGES

BLOCKING
- path/file.ext:42 — <what is wrong> — <why it matters> — <what to do>

SHOULD FIX
- ...

NITS
- ...

NOT VERIFIED BY ME
- <what you did not run/check, stated plainly>
```

Always include the "not verified" section. Silence about coverage reads as
verification.

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| Reviewing the author's description instead of the diff | approves intent, not code |
| "LGTM" with no verdict or findings | indistinguishable from not reviewing |
| Blocking on style preferences | buries the real findings; author tunes out |
| Claiming a test passes without running it | the exact falsehood this repo exists to prevent |
| Reviewing a 900-line diff in one pass | attention is a resource; require it be split |
| Fixing the code during review | reviewer becomes author; independence is lost |
