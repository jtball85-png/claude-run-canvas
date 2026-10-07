---
name: dev-team
description: Run a task through the architect → coder → tester → manager pipeline instead of handling it in this session directly. Best for multi-step feature work; skip it for small, well-defined edits.
---

# Dev Team — Plan, Implement, Verify, Review

Task: $ARGUMENTS

If no task was given, ask for one and wait. Otherwise execute these steps in order.

---

## 1. Architect

Delegate the task to the `architect` subagent. Show the resulting plan to the user in a few lines before continuing — don't wait for approval, just surface it.

## 2. Coder

Delegate the plan to the `coder` subagent.

## 3. Tester

Delegate to the `tester` subagent to verify the coder's change.

## 4. Manager

Delegate the original task, the plan, the coder's diff, and the tester's report to the `manager` subagent for review.

## 5. Fix loop (capped at one round)

- If the manager reports the work is done: tell the user it's done, in a couple of sentences, and stop.
- If the manager leaves fix notes and this is the **first** time through: delegate the notes back to the `coder` subagent, then repeat steps 3–4 once.
- If the manager still has notes after that one fix round: stop. Show the user the unresolved notes directly — do not send a third round.

---

Do not skip the tester or manager steps even if the change looks obviously correct — that judgment call is exactly what this workflow exists to check.
