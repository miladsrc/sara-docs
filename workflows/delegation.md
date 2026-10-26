# Workflow — Delegation

How Sara dispatches a subagent. Agent contracts and routing live in
[../roster/README.md](../roster/README.md); this file owns the **handoff**.

A subagent starts with **fresh context**. It cannot see this conversation, your
reasoning, or the files you already read. Everything it needs, you must write.

---

## The handoff contract

Every dispatch contains all six sections. Missing any one of them is the usual
cause of a useless result.

```
1. ROLE      Which agent, and why that one.
2. GOAL      One sentence: the outcome, not the activity.
3. CONTEXT   Facts already established — paths, versions, constraints,
             decisions already made. State them; do not allude to them.
4. SCOPE     What to look at / change, and explicitly what NOT to touch.
5. OUTPUT    The exact shape wanted: findings table, patch, verdict, file.
6. DONE      How it knows it is finished and how correctness is judged.
```

## Dispatcher's obligations

- **Do not send it to find what you already know.** Restate known facts; spend
  the subagent's budget on what is unknown.
- **One question per dispatch.** Two questions produce one answered and one
  half-answered.
- **Read-only unless stated.** If it may write, say where; otherwise scope it to
  read-only and treat its output as a proposal.
- **Ask for evidence, not prose.** "Cite path:line for each claim" beats
  "summarize". Require the agent to distinguish verified from inferred.
- **Never delegate the decision.** Delegation gathers or produces; the judgment
  that commits stays with the dispatcher.

## Choosing the agent

The routing table (signal → agent) is owned by
[../roster/README.md](../roster/README.md). Consult it there; this workflow owns
only the handoff mechanics. Per-agent inputs, outputs, and failure modes are in
the same file.

## Receiving the result

1. **Check the shape.** Did it return what was asked, or what it found easier to
   return?
2. **Check the evidence.** Every claim should carry a path, command, or citation.
   Uncited claims are opinions — treat them as INFERRED.
3. **Check the scope.** Anything it did outside the stated scope is reverted or
   explicitly accepted, not ignored.
4. **Verify the critical claim yourself** when it is load-bearing for a
   decision. Trusted delegation still ends in a verification by the dispatcher.

Then record: which agent, what it was asked, what came back, what you accepted.
The dispatcher owns the outcome — a subagent's error is the brief's error.

## When not to delegate

- The task is one step with a known answer: just do it (see the decision ladder in
  the operating model).
- The task requires the conversation history to make sense and writing that
  history down would cost more than the work itself.
- The work is a decision the owner must make.
- You cannot state the six sections. That is a sign the task is not yet understood
  — clarify first, delegate second.

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| "Look into the auth code and fix whatever's wrong" | no scope, no output shape, no way to judge done |
| Delegating and accepting the answer unread | accountability still sits with the dispatcher |
| Parallel agents editing the same files | conflicting writes, no merge owner |
| Using a subagent for a one-line lookup | latency and context cost with no independence benefit |
| Relaying subagent claims as fact | it reasons from a partial brief; label what it returns |
