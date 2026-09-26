# SARA_EXAMS.md — Exam series: examiner records, grading, and candidate coaching

Scope: Sara's role as **examiner / evaluator / mentor** for the `dotin-10day-challenges`
series on this host, and the durable lessons from it. This is the knowledge-layer
record; the *live* runtime self and its memory remain at
`C:\Users\m.barani\.config\opencode` (`memory/sara.md`).

Sara is the **examiner, never the implementer**. In an exam workspace Sara grades
as-is and does not fix the candidate's code — see `SARA_SELF_BOUNDARY.md` and each
exam's `RULES.md`, which forbids AI assistance. Coaching is offered only as a
separate, explicitly requested mode.

---

## 1. Exam series map

Location: `C:\Users\m.barani\IdeaProjects\dotin-10day-challenges\`

| # | Directory | Topic | State (as of 2026-09-26) |
|---|---|---|---|
| 01 | `dotin-sim-01-core-payment-rules` | Fee-rules engine rescue (pure Java, no Spring) | **graded 25/100** — see §2 |
| 02 | `dotin-sim-02-wallet-transfer-api` | JPA transfer + concurrency | evaluator kit built; publish blocked (`gh` absent) |
| 03 | `dotin-sim-03-jpa-transfer-history` | — | starter only |
| 04 | `dotin-sim-04-idempotent-payment` | — | starter only |
| 05 | `dotin-sim-05-legacy-transaction-incident` | — | starter only |
| 06 | `dotin-sim-06-postgres-query-rescue` | — | starter only |
| 07 | `dotin-sim-07-transactional-outbox` | — | starter only |
| 08 | `dotin-sim-08-psp-resilience` | — | starter only |
| 09 | `dotin-sim-09-production-readiness` | — | starter only |
| 10 | `dotin-sim-10-payment-refund-final` | — | starter only |

`_superseded-exam02-peer-20260926T0814/` — a non-compliant parallel build of exam 02
(wrong package root `ir.dotin.exam02`, wrong seed data). **Relocated, not deleted**;
operator may remove it.

---

## 2. EXAM-01 grading record — `dotin-sim-01-core-payment-rules`

**Verdict: 25/100 technical, mid-flight checkpoint. Official grade 0 (no valid submission).**

- Package root: `ir.dotin.exam01` (contract — must not be renamed)
- Baseline: commit `a35ee0c` "chore: create exam starter baseline", tag `exam-01-baseline`
- Branches: `main` (baseline) + `candidate` (answer). **No remote configured.**
- Graded: 2026-09-26, JDK 17 + project Maven Wrapper only.

### 2.1 Exam contract (from README.md / RULES.md — the grading surface)

- Section 3 freezes the public API: `PaymentChannel`, `CustomerType`, `PaymentRequest`,
  `FeeQuote`, `FeePolicy`, `AtmFeePolicy`/`MobileFeePolicy`/`WebFeePolicy`,
  `FeeCalculator` (incl. **both** `quoteAll(List)` and `quoteAll(Set)`), and the two
  exceptions in `ir.dotin.exam01.error`. **Signatures are a contract; changing them is
  forbidden.** `quoteAll(null)` must be made *unambiguous*, not deleted.
- Section 4 fixes the rate table and the rounding pipeline: `amount * rate / 100`, then
  `setScale(2, HALF_UP)`; for VIP, halve the **already-rounded** fee and round again.
- Section 5 lists the 9 mandatory behavioural rules (extensibility, dedupe-first-wins,
  first-seen ordering, no input mutation, determinism, `BigDecimal`-only money,
  meaningful exceptions, input boundaries, `equals`/`hashCode` contract).
- Section 8 deliverables: green build, **`FIX_NOTES.md` (graded)**, **≥6 unit tests
  (graded)**, root-cause notes for any moved/redesigned file. No deleting or disabling
  tests; no CI tampering.
- RULES.md: 120-minute exam; answer only on branch `candidate`; **uncommitted or unpushed
  work scores nothing**; no web search, no AI assistant, no copying.

### 2.2 Build evidence

```
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-17.0.20.8-hotspot"
.\mvnw.cmd -B clean test     ->  BUILD SUCCESS (1.739 s)
```

Compiles — but surefire executed **zero tests** because `src/test/java` does not exist.

### 2.3 The 5 seeded compile errors — candidate's handling

| # | Error | What the candidate did | Examiner verdict |
|---|---|---|---|
| 1 | generic mismatch, channel→policy map | `new HashMap<>()` in `FeePolicyRegistry:14` | correct, minimal |
| 2 | local reassigned then captured in lambda | wrapped it: `var ref = new Object(){ BigDecimal factor = … }` then `ref.factor = ref.factor.setScale(…)` | **hack** — defeats the *effectively-final* check instead of fixing the cause. Correct fix is a single-assignment local; `MobileFeePolicy:22-25` already shows the right shape |
| 3 | incomplete `return` in a fee policy | added `return feeFor(amount, STANDARD)` (`AtmFeePolicy:24`) | correct |
| 4 | `amount()` called on a `getAmount()` class | `quote.amount()` → `quote.getAmount()` | correct |
| 5 | ambiguous overload invocation | **commented out the whole `quoteAll(Set<PaymentRequest>)` method** (`FeeCalculator:92-97`) | **not fixed — destroyed a frozen public API to silence the compiler** |

### 2.4 Behavioural audit — all 6 seeded behaviour bugs still present (probe-verified)

| Contract | Result | Evidence |
|---|---|---|
| Rate table (11 reference cases) | 8 pass / 3 fail | `ATM 0.50→0.00` (want `0.01`), `ATM 1234.56→12.34` (want `12.35`), `ATM 0.50 VIP→0.00` |
| R1 extensible, no per-channel `if/else` | intact | registry-map design was already correct |
| R2 duplicate `clientReference` counted **once**, first wins | **FAIL** | `REF-1001 = 2.00`, want `1.00` — `FeeCalculator:80` *adds* the later fee |
| R3 output order = first-occurrence order | **FAIL** | input `Z-9, A-1` came back `A-1, Z-9` — `FeeCalculator:67` sorts by reference |
| R4 never mutate the caller's list | **FAIL** | same in-place `requests.sort(...)` |
| R5 determinism | pass | |
| R6 no `double`/`float` for money | **FAIL** | `AtmFeePolicy:30-32` still `double` + `Math.floor` (truncates instead of HALF_UP). `MobileFeePolicy` / `WebFeePolicy` are the correct `BigDecimal` reference |
| R7 throw instead of returning `null` | **FAIL** | all four invalid-input paths return `null`; `InvalidAmountException` and `UnsupportedChannelException` are **still never used anywhere** |
| R8 input boundaries | 1/3 | `null` list → empty ok; **empty list throws `UnsupportedOperationException`** (sorting an immutable `List.of()`); `null` member silently filtered instead of throwing |
| R9 `equals`/`hashCode` contract | **FAIL** | `hashCode` is `System.identityHashCode(this)` (`PaymentRequest:58`) → two field-equal requests form a `Set` of size 2 |

### 2.5 Score card (100)

| Section | Weight | Score |
|---|---:|---:|
| Compile recovery | 15 | 12 |
| Behavioural correctness (§4 + §5) | 35 | 12 |
| Unit tests (≥6 required) | 25 | 0 |
| `FIX_NOTES.md` (graded deliverable) | 15 | 0 |
| Discipline / contract compliance | 10 | 1 |
| **Total** | **100** | **25** |

Discipline earned 1 point only for: CI file, `pom.xml` versions, and `mvnw` untouched;
no secrets committed. It lost the rest for deleting a contract API, using `double` for
money, leaving everything uncommitted, and having no remote to push to.

**Submission validity:** all 3 fixes are working-tree only, nothing committed on
`candidate`, and `git remote -v` is empty — so per RULES.md the official result is
**0, no valid submission**. The 25/100 is the technical score of work in progress.

### 2.6 Examiner method that worked (reusable)

The candidate ships a deliberately broken baseline. A fast, non-invasive way to grade it
without touching the workspace:

1. Build with the exam's own command to get the real compile signal.
2. Write a **throwaway probe outside the exam workspace** and run it on the compiled
   classes with the JDK 17 single-file source launcher:
   `java -cp "<repo>\target\classes;." Probe.java`
3. Encode the README's reference table and §5 rules as assertions; count failures.

Gotchas that cost time and are worth remembering:

- The probe must `import ir.dotin.exam01.error.*` **explicitly** — a wildcard
  `ir.dotin.exam01.*` does not reach a sub-package.
- `java -cp X Probe.java` needs the file to resolve from the **current directory**; run
  the command with the workdir set to the probe directory, otherwise Java treats
  `Probe.java` as a class name (`ClassNotFoundException`).
- Assertions that *crash* the engine (the empty-list `UnsupportedOperationException`)
  must be wrapped in `try/catch` or the rest of the probe never runs.
- A "did it mutate the list?" check is only meaningful when the input is **not already
  in sorted order** — otherwise the reordering is invisible. Probe with unsorted keys.
- Probing from outside the workspace also keeps the submission clean, which matters
  because RULES.md forbids moving evaluator material into the candidate's tree.

---

## 3. Candidate development plan (learner = the operator)

History: the operator scored **41/100** on the earlier payments challenge. Recurring
root causes, in the order they keep costing points:

1. **Verify the money actually moves.** The 41/100 failure was a no-op
   `setBalance(BigDecimal b){ this.balance = b; }` — balances never changed and every
   business-rule test still "passed". Assert DB truth after each rule, not just the
   HTTP response.
2. **Fix the cause, not the compiler.** Exam-01 added an anonymous-class wrapper to
   defeat a lambda check, and deleted a public method to silence an overload error.
   Both make the symptom disappear while leaving the defect (and the contract) broken.
3. **Read the frozen contract before editing.** Section 3 said the signatures cannot
   change; the ambiguity note even said *how* to disambiguate. Both were on the page.
4. **Concurrency and `BigDecimal` discipline.** Money as `double` with `Math.floor`
   truncates instead of HALF_UP — the exact class of bug a single assertion catches.
5. **Ship the graded artefacts.** 40 of 100 points were `FIX_NOTES.md` + tests, and a
   perfect fix with no tests and no notes still fails the exam.
6. **Finish the submission workflow.** Commit on `candidate`, push, then report the SHA.
   Work that is never pushed scores nothing.

Drills: a failing test first, then the implementation; design entity/API shape before
coding; re-run the full suite green at the end; simulate the nasty cases (duplicates,
unsorted keys, immutable inputs, empty inputs, `null` members) *before* declaring done.

---

## 4. Environment facts (durable, this host)

- Ambient `java` / `JAVA_HOME` is **JDK 26** (`C:\Users\m.barani\.jdks\openjdk-26.0.2.1`).
  Java 17 = `C:\Program Files\Eclipse Adoptium\jdk-17.0.20.8-hotspot`. Select per-process:
  `$env:JAVA_HOME="C:\Program Files\Eclipse Adoptium\jdk-17.0.20.8-hotspot"` then prepend
  `$env:JAVA_HOME\bin` to PATH. Global settings are never changed.
- Maven 3.9.6 at `C:\Users\m.barani\Tools\maven`. The exam projects use the **Maven
  Wrapper only** (`.\mvnw.cmd`); wrapper `only-script` needs an explicit
  `distributionUrl` for `apache-maven-3.9.6-bin.zip` (`-Dmaven=3.9.6` gets mangled by
  PowerShell into a versionless URL that 404s).
- `gh` CLI is **not installed** on this machine. `gitlab.sidg.ir` is the working remote
  for pushes; GitHub is reachable but slow/occasional DNS trouble on this network.
- Exam-01 environment per RULES.md: JDK 17, app port `18101` (declared but unused — the
  project has no server), PostgreSQL `15431`, container prefix `dotin01`. Only
  dependency: `spring-boot-starter-test` (test scope) → JUnit 5 + AssertJ.
- `read-terminals` helper: `todos` subcommand fails with `no such column: data`; needs
  `PYTHONIOENCODING=utf-8`; `-Dtest=ir.dotin...*` patterns do not match — use `-Dtest=Hidden*`.

---

## 5. Open items

- **EXAM-01:** candidate work is unfinished — 6 behaviour bugs open, 0 tests,
  no `FIX_NOTES.md`, nothing committed, no remote. Next session: mentor mode
  (Problem → Solution → Correction → Retest, Persian, no code handed over).
- **EXAM-01 publishing:** the repo has no remote. Decide GitHub vs `gitlab.sidg.ir`
  before the final submission, then push `candidate`.
- **EXAM-02:** evaluator kit at
  `C:\Users\m.barani\.config\opencode\dotin-exam-02-evaluator-2026`
  (7 hidden classes / 49 methods, rubric exactly 100, reference solution 55/55 green,
  starter fails 26 + 4 errors). Publishing still blocked on the missing `gh` CLI.
- `_superseded-exam02-peer-20260926T0814/` — awaiting the operator's delete/keep decision.
- Stale java pids `25032` / `26004` from the peer run still hold port `18102`; not killed,
  per the no-kill rule.
