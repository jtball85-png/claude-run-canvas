---
name: end-of-day
description: End of session wrap-up — capture session memory, update project-context.md, commit both files, and push to GitHub. Facts and decisions only.
---

# End of Day — Session Wrap-Up

Execute these steps in exact order.
Do NOT skip steps.
Do NOT interpret or editorialize — record facts and decisions only.

---

## 1. Collect the facts

Run these commands and hold the output for the steps below.

```bash
# What changed today
git log --oneline --since="1 day ago"

# What files were touched
git diff --stat HEAD~1

# Current branch
git rev-parse --abbrev-ref HEAD

# Last commit hash and message
git log -1 --format="%h %s"

# Anything not yet committed
git status --porcelain
```

---

## 2. Update project-memory.md

Open project-memory.md and append a new session entry at the TOP of the Sessions section.

Format exactly:
```
## Session — [YYYY-MM-DD]

**Focus:** [What the user said we were working on at start of day]

**Decisions made:**
- [Decision 1 and the reasoning behind it]
- [Decision 2 and the reasoning behind it]

**Problems solved:**
- [Problem and how it was resolved]

**Approaches discussed:**
- [Any approaches, patterns, or methods talked through — even if not implemented]

**Left unresolved:**
- [Anything discussed but not concluded]

**Files changed this session:**
[paste git diff --stat output here]
```

Rules:
- Only include sections that have content — skip empty ones
- Facts and decisions only — no summaries of what Claude did
- This file is Claude's memory for next session — write it for that purpose

---

## 3. Update project-context.md

Update ONLY these three fields. Do not touch any other section.

### a. Last updated
Replace with today's date:
- Format: `Last updated: [YYYY-MM-DD] by Claude Code`

### b. Where we left off
Replace the entire contents with:
```
Last commit: [hash] — [message]
In progress: [any uncommitted work from git status, or "none"]
Branch: [current branch]
```

### c. What's next
- Remove any tasks completed during this session
- Do not add new tasks unless the user explicitly states them
- Leave all remaining tasks exactly as written

### d. Change log
Append one new entry at the TOP. Do not remove existing entries.
```
- [YYYY-MM-DD] — [one line per commit from git log] — Source: Claude Code
```

---

## 4. Consistency check

Before committing, verify:
- [ ] project-memory.md has a new session entry at the top
- [ ] Last updated date in project-context.md is today
- [ ] Where we left off matches the actual last commit
- [ ] Completed tasks removed from What's next
- [ ] Change log has a new entry at the top
- [ ] No other sections were modified

---

## 5. Commit both files

```bash
git add project-context.md project-memory.md
git commit -m "End of day [YYYY-MM-DD] — context and memory updated"
```

Verify clean state:
```bash
git status
```

---

## 6. Push to GitHub

Check whether this project has a remote:

```bash
git remote -v
```

If there's no remote, tell the user this project isn't connected to GitHub yet — today's work is only saved locally on this machine — and skip to Step 7.

If there is a remote, push:

```bash
git push
```

Handle the result:

- **Push succeeds:** continue to Step 7.
- **Push is rejected because the remote has commits this machine doesn't have** (most likely: work was done from a different computer without pulling here first): STOP. Do not force push. Tell the user the commit succeeded locally but push was rejected, and offer to pull (merge) and push again — don't do it silently, confirm first, since it may touch `project-memory.md`'s Sessions section on both sides.
- **Push fails because GitHub is unreachable (network/auth):** tell the user the commit succeeded locally but couldn't be pushed — their work is safe on this machine but not backed up yet. Continue to Step 7.

---

## 7. Done

Tell the user:

"Session captured. Both files committed[, and pushed to GitHub / — not pushed, see above]."

Fill in the bracketed part based on what actually happened in Step 6; drop the brackets.

"Tomorrow: type /start-of-day to pick up where we left off."
