---
name: new-project
description: New project setup — interview the user, fill out project-context.md, create project-memory.md, and prepare for first session.
---

# New Project Setup

You are setting up a new project from scratch.
Your job is to interview the user and use their answers to fill out project-context.md completely.

Do NOT rush. Do NOT move to the next question until the current one is answered clearly.
Do NOT fill in placeholders — every section must have real content before you finish.

---

## 1. Open the kickoff

Say exactly this:

"Let's set up your new project. I'm going to ask you questions one at a time — take your time with each answer, and I'll ask for more detail if I need it.

What's the idea? Describe it however feels natural."

Wait for their answer.
If the answer is vague, ask a follow-up before moving on:
- "Who is this for?"
- "What problem does it solve?"
- "What does done look like?"

Do not move to Step 2 until you can write a clear 2–3 sentence project description.

---

## 2. Interview — one question at a time

Ask each question below in order.
Wait for a clear answer before asking the next one.
If an answer is unclear, ask one follow-up question before moving on.

**Q1 — Current status**
"Where does this project stand right now? Is this brand new, already started, or picking up something stalled?"

**Q2 — What's built or decided already**
"What exists already — files, decisions, research, anything? Or are we starting from zero?"

**Q3 — What's next**
"What are the first 3 things that need to happen to move this forward?"

**Q4 — Tools**
"For each of those tasks — is it thinking and planning (Chat), building and editing files (Claude Code), or browser and desktop work (Cowork)?"

**Q5 — Key terms and structure**
"Are there specific terms, naming conventions, or a folder structure I should know about for this project?"

**Q6 — Key files**
"What are the most important files in this project? Just the ones that matter most."

**Q7 — Known issues**
"Anything already broken, blocked, or uncertain that I should know going in?"

---

## 3. Fill out project-context.md

Using the answers from Step 2, write a complete project-context.md file.
Use this exact template — no placeholders, no empty sections:

```markdown
# Project: [Project Name]
Last updated: [YYYY-MM-DD] by Claude Code

## What this project is
[2–3 sentences — what it is, who it's for, what problem it solves]

## Current status
[One paragraph — what stage, what exists, what's not built yet]

## Where we left off
Last commit: N/A
In progress: Project setup — first session
Branch: main

## What's next
- [ ] [Task 1 — Tool]
- [ ] [Task 2 — Tool]
- [ ] [Task 3 — Tool]

## Project structure / terminology
[Key terms and naming conventions from Q5]

## File map (key files)
| File | Purpose |
|---|---|
| `project-context.md` | Project status and orientation |
| `project-memory.md` | Session decisions and reasoning |
| `[other files from Q6]` | [purpose] |

## Key decisions made
- [YYYY-MM-DD] — Project initialized

## Known issues
[From Q7, or "None at this time"]

## Context for each tool

### Chat
Thinking, planning, decisions, and fuzzy problems.
Flag anything that requires a major direction change before acting.

### Claude Code
Building and editing files.
Run /start-of-day at the start of every session.
Run /end-of-day at the end of every session.

### Cowork
Browser tasks, desktop automation, file management.
Use project-context-updater.html on Cowork-heavy days.

## Change log
- [YYYY-MM-DD] — Project initialized — Source: Claude Code
```

Show the completed file to the user and say:
"Here's your project-context.md — does this look right? Anything to change before I save it?"

Wait for confirmation. Make any changes requested before saving.

---

## 4. Create project-memory.md

Write the following file to the project root:

```markdown
# Project Memory
Last updated: [YYYY-MM-DD]

This file captures decisions, reasoning, and session context that
project-context.md doesn't hold. It is Claude's memory between sessions.

---

## Key decisions (permanent record)

- [YYYY-MM-DD] — Project initialized

---

## Sessions

<!-- end-of-day skill appends new sessions here -->
```

---

## 5. Save both files

```bash
git add project-context.md project-memory.md
git commit -m "New project initialized — [Project Name]"
```

---

## 6. Done

Tell the user:

"Your project is set up and committed.

From here:
- Start every session with /start-of-day
- End every session with /end-of-day
- Use Chat for planning and decisions

What are we working on in this first session?"
