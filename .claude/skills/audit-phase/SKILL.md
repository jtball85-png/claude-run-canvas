---
name: audit-phase
description: Audit a completed build phase against its spec requirements and its own status-doc claims — catches implementation gaps, deferred work masquerading as done, and project-context.md/project-memory.md drift. Use when the user asks to audit, review, or verify a phase, or before marking a phase complete.
---

# Audit a Phase

Verifies that a phase project-context.md claims is "done" actually is — against the
spec it was built from, the tests that are supposed to prove it, and any output
artifacts it produced (not just the status docs' word for it). Read-only: produces a
findings report, does not edit code, tests, or docs.

Phase to audit: $ARGUMENTS

If no phase was given, ask which one — offer the most recent phase
project-context.md's change log claims is complete as the default. Otherwise execute
these steps in order.

---

## 1. Establish what this phase claims to be

- Read project-context.md's "Current status", "What's next" (checked/unchecked boxes),
  and every "Change log" entry mentioning this phase.
- Read project-memory.md's "Key decisions" and "Sessions" entries for the same phase.
- Note every concrete claim: what was built, what tests exist, what's explicitly
  deferred, and whether the phase's own checkbox is checked.
- **Flag immediately if the "Current status" prose and the "What's next" checkbox
  disagree about whether this phase is done** — that contradiction alone is worth
  surfacing before anything else, and is exactly the kind of drift this skill exists
  to catch.

## 2. Find the spec ground truth

- Read the project's spec doc in full (or re-skim if already familiar) and identify
  every section that governs this phase's claimed scope. Don't rely solely on
  project-context.md's own section citations — search the spec directly using terms
  tied to this phase's claimed scope, plus the spec's own build-order section (if it
  has one) for what this phase is explicitly allowed to exclude.
- Note requirements that are typically under-covered relative to the happy path:
  safety/guardrail mechanisms, event/notification triggers, edge-case handling
  (ambiguous or unparseable output, budget/resource exhaustion, retry/backoff limits).

## 3. Verify against the actual code, not the docs' description of it

For each spec requirement identified in step 2:

- Locate the implementing code. If this codebase cites spec section numbers in
  comments/docstrings (as this one does), grepping for the section number is usually
  the fastest way in.
- Read it well enough to confirm it actually does what's claimed — don't stop at
  confirming a function with the right name exists.
- Grep the whole phase's code for `TODO`, `PENDING`, `not implemented`, `future work`,
  `deferred`, `placeholder` — anything self-flagged as incomplete. These are usually
  honest and worth trusting at face value; the thing to check is whether a status doc
  elsewhere contradicts them by claiming that same area is done.
- If the phase produced any output artifacts (a manual run log, a generated report, a
  saved transcript) — **read the artifact itself**, don't trust a summary of it. This
  is where drift hides: a status doc can call a run "verified" when the run's own
  output marks it incomplete.

## 4. Run the tests

- Run the phase's test suite and record the actual pass count.
- Skim test names (not full bodies) for coverage shape: does every
  kill/branch/edge-case path the spec calls out have a test, or only the happy path?
  A large passing count is not proof of coverage on its own — check what's actually
  being exercised.

## 5. Report

Structure findings into three buckets, most important first:

1. **Status-doc drift** — anywhere project-context.md or project-memory.md claims
   something the code, tests, or a referenced artifact don't actually support. This is
   the highest-value category: it's the gap between what the user believes is true and
   what's real.
2. **Real gaps** — spec requirements in this phase's scope that aren't implemented,
   aren't tested, or behave differently than documented, and aren't already
   self-flagged as an intentional deferral.
3. **Confirmed solid** — a short list of what checked out, so the report isn't just a
   list of problems.

Do not edit code, tests, or docs during this skill — audit only. If drift or gaps are
found, ask the user whether to (a) fix the code, (b) correct the status docs to match
reality, or (c) leave it as known debt — don't assume which.
