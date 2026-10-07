---
name: checkpoint
description: A stripped-down /end-of-day for use mid-session, any time you're about to /clear — same memory capture, none of the ceremony.
---

# Checkpoint

A stripped-down `/end-of-day`, for use **mid-session, any time you're about
to `/clear`** — not just at the actual end of the day. Same memory capture,
none of the ceremony. Facts and decisions only, no interpretation.

Claude cannot trigger `/clear` itself — that's a client-side command outside
any tool's reach. This command ends by telling you to run it yourself.

---

## 1. Collect the facts

```bash
git log --oneline --since="4 hours ago"
git diff --stat HEAD~1
git rev-parse --abbrev-ref HEAD
git log -1 --format="%h %s"
git status --porcelain
date +%Y-%m-%d
```

## 2. Append a session entry to project-memory.md

Same entry shape `/end-of-day` uses — top of the `## Sessions` section:

```
## Session — [YYYY-MM-DD] (checkpoint)

**Focus:** [what this stretch of conversation was actually about]

**Decisions made:**
- [decision + reasoning, if any]

**Problems solved:**
- [problem + resolution, if any]

**Left unresolved:**
- [anything mid-flight — this is the part a fresh session most needs]

**Files changed this session:**
[paste git diff --stat output]
```

Only include sections with real content. If this is the second (or third)
checkpoint today, append as its own entry — don't merge with an earlier one.

## 3. Update project-context.md

Same three fields `/end-of-day` touches, nothing else:

- **Last updated** → today's date, "by Claude Code"
- **Where we left off** → last commit hash/message, in-progress work from
  `git status`, current branch
- **Change log** → one new line at the top: `- [YYYY-MM-DD] — [summary] — Source: Claude Code`

Leave **What's next** alone unless something on it was just finished.

## 4. Commit and push

```bash
git add project-context.md project-memory.md
git commit -m "Checkpoint [YYYY-MM-DD] — mid-session save"
```

Then check for a remote before pushing:

```bash
git remote -v
```

- **No remote:** say so — checkpoint is committed locally only, nothing to push.
- **Remote exists:** `git push`. If it's rejected because the remote has
  commits this machine doesn't have, STOP — don't force push. Say the
  commit succeeded locally but push was rejected, and offer to pull and
  push again rather than doing it silently. If push fails for network/auth
  reasons, say the commit succeeded but wasn't backed up yet — don't report
  plain success.

## 5. Tell the user

"Checkpoint saved[, and pushed / — not pushed, see above]. Safe to `/clear`
now — run it yourself whenever you're ready; I can't trigger it from here.
Next session, run `/start-of-day` to pick back up."

Fill in the bracketed part based on what actually happened in Step 4; drop the brackets.
