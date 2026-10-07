---
name: start-of-day
description: Start of session orientation — pull the latest from GitHub, read project-context.md and project-memory.md, confirm understanding, and ask what we're working on today.
---

# Start of Day — Session Orientation

Execute these steps in exact order.
Do NOT skip steps.
Do NOT begin working until all steps are complete.

---

## 1. Sync with GitHub

Check whether this project has a remote:

```bash
git remote -v
```

If there's no remote, skip straight to Step 2 — this project isn't connected to GitHub yet.

If there is a remote, pull:

```bash
git pull
```

Handle the result:

- **Up to date, or pulled cleanly (fast-forward):** continue to Step 2.
- **Pull refuses because of local uncommitted changes that would be overwritten:** STOP. Do not stash, discard, or force anything. Tell the user exactly what's uncommitted and that you stopped before touching it — let them decide how to proceed.
- **Pull results in a merge conflict:** STOP. Do not resolve `project-context.md` or `project-memory.md` conflicts silently. Show the user which files conflict and ask how they want to resolve it — usually this means keeping both sides' `Sessions` / change-log entries rather than picking one.
- **Pull fails because GitHub is unreachable (network/auth):** warn the user you couldn't check for updates and are proceeding with the local copy, which may be behind. Continue to Step 2 — don't block the session over a network hiccup.

---

## 2. Read both context files

Read the following files from the project root:

```bash
cat project-context.md
cat project-memory.md
```

If either file is missing, stop and tell the user:
- "project-context.md not found — please paste it directly into the chat."
- "project-memory.md not found — this may be a new project. Run /new-project to initialize."

---

## 3. Confirm orientation

After reading both files, give the user a short orientation summary in this exact format:

---
**Project:** [project name from project-context.md]
**Last updated:** [date from project-context.md]
**Architecture:** [only if project-context.md has an Architecture decision section — Static frontend / Full stack]
**Tech stack:** [only if project-context.md has a Tech stack table — one line summary]
**Where we left off:** [1–2 sentences from the "Where we left off" section]
**What's next:** [list the open tasks from "What's next"]
**Last session memory:** [1–2 sentences summarizing the most recent entry in project-memory.md]
---

Omit the Architecture and Tech stack lines entirely for projects that don't have those sections — don't show them as empty.

Keep it short. Facts only. No interpretation.

---

## 4. Ask what we're working on today

After the summary, ask exactly this:

"What are we working on today — sticking with What's Next, or something different?"

Wait for the user's answer before doing anything else.

---

## 5. Begin

Once the user confirms the focus for today, acknowledge it in one sentence and begin.

Do not re-summarize. Do not ask follow-up questions. Just start.
