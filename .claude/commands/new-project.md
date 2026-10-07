---
name: new-project
description: New project setup — determine whether this is an app/browser-based project or something else, interview the user accordingly, fill out project-context.md, create project-memory.md, and commit both.
---

# New Project Setup

You are setting up a new project from scratch.
Your job is to interview the user and use their answers to fill out project-context.md completely.

Do NOT rush. Do NOT move to the next question until the current one is answered clearly.
Do NOT fill in placeholders — every section must have real content before you finish.

---

## 1. Determine project type

Before anything else, ask:

"One thing before we start — is this an app or something that runs in a browser (a tool with a frontend, maybe a backend or database), or something else entirely — writing, research, planning, a general project?"

Wait for the answer. Store it as the project type: **app** or **general**. This decides which questions get asked below.

---

## 2. Open the kickoff

If **app**, say exactly this:

"Let's set up your new app project. I'm going to ask you questions one at a time — take your time with each answer, and I'll ask for more detail if I need it.

What do you want this app to do for you?"

If **general**, say exactly this:

"Let's set up your new project. I'm going to ask you questions one at a time — take your time with each answer, and I'll ask for more detail if I need it.

What's the idea? Describe it however feels natural."

Wait for their answer.
If the answer is vague, ask one follow-up before moving on:
- "Who is this for — just you, or other users too?"
- "What problem does it solve?"
- "What does done look like?"

Do not move to Step 3 until you can write a clear 2–3 sentence project description.

---

## 3. Interview — one question at a time

Ask each question below in order. Wait for a clear answer before asking the next one. If an answer is unclear, ask one follow-up question before moving on.

### If app — ask these first

**Architecture: Does it need to save data?**
"Does this app need to save data between sessions or between different users?
- No → we'll build a static frontend (HTML/CSS/JS only)
- Yes → we'll need a backend and database
- Not sure yet → that's fine, we'll start static and plan to upgrade

Which fits best?"

Ask the follow-up only if relevant:
"Does this app need to hide any secrets from the browser — like API keys or business logic?
If yes, we'll need a backend even if there's no database."

**Tech stack**
"What tools are you planning to use? If you're not sure, say so and I'll suggest a simple starting stack.

- Frontend: (e.g. HTML/CSS/JS, React)
- Backend: (e.g. Node + Express, Python + FastAPI, or none)
- Database: (e.g. Supabase, SQLite, or none)
- Auth: (e.g. Supabase Auth, Clerk, or none)
- Deployment: (e.g. Vercel, Railway, local only)
- AI or external APIs: (e.g. Anthropic API, Stripe, or none)"

**User flow**
"Walk me through this app as a user seeing it for the first time.
What's the first screen? What can they do? Where do they go next?
Keep going until the job is done."

If the answer is thin, ask: "What screens does this app need? Just a simple list."

**Data model** — ask only if the app saves data:
"What are the 'things' in this app and how do they relate?
Example: Users have Projects. Projects have Tasks. Tasks have Comments.
Even one sentence helps."

### Both — ask these next

**Current status**
"Where does this project stand right now? Brand new, already started, or picking up something stalled?"

**What's built or decided already**
"What exists already — files, decisions, research, a prototype? Or are we starting from zero?"

**What's next**
"What are the first 3 things that need to happen to move this forward?"

**Tools**
"For each of those tasks — is it thinking and planning (Chat), building and editing files (Claude Code), or browser and desktop work (Cowork)?"

### If app — ask this next

**Environment and secrets**
"Do you have any API keys or environment variables this app will need?
Don't share the actual values — just tell me what variables will exist."

### If general — ask these next

**Key terms and structure**
"Are there specific terms, naming conventions, or a folder structure I should know about for this project?"

**Key files**
"What are the most important files in this project? Just the ones that matter most."

### Both — ask last

**Known issues or risks**
"Anything already broken, blocked, or uncertain that I should know going in?"
For app projects, also ask: "What's the hardest part to build?"

---

## 4. Fill out project-context.md

Using the answers from Step 3, write a complete project-context.md file. Use the matching template below — no placeholders, no empty sections.

**If app**, use this template:

```markdown
# Project: [Project Name]
Last updated: [YYYY-MM-DD] by Claude Code

## What this project is
[2–3 sentences — what it is, who it's for, what problem it solves]

## Architecture decision
**Does this app need to save data between sessions or between users?**
- [x] [Chosen option: Static frontend / Full stack / Undecided]

**Does this app need to hide secrets from the browser?**
- [x] [Yes / No]

**Current answer:** [Static frontend / Full stack / Undecided]

## Tech stack
| Layer | Tool/Language | Notes |
|---|---|---|
| Frontend | [value] | |
| Backend | [value or none] | |
| Database | [value or none] | |
| Auth | [value or none] | |
| Deployment | [value] | |
| AI / APIs | [value or none] | |

## Data model
[From the data model question, or "Not applicable — static frontend"]

## User flow
[From the user flow question — the path a user takes through the app start to finish]

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

## File structure
```
/project-root
  /src        → [what lives here]
  /assets     → [what lives here]
  /docs       → reference guides
  /archive    → archived context docs
  index.html  → [what this is]
```

## Environment and credentials
- .env file: [exists / not yet created]
- Variables needed: [list from the environment question, or "none"]
- Where secrets are stored: [local .env / Vercel dashboard / not set up yet]

## Key decisions made
- [YYYY-MM-DD] — Project initialized
- [YYYY-MM-DD] — Architecture: [Static frontend / Full stack]

## Known issues
[From the known issues question, or "None at this time"]

## Context for each tool

### Chat
Thinking, planning, decisions, and fuzzy problems.
Flag architecture changes or scope changes before acting.

### Claude Code
Building and editing files. Tech stack: [summary].
Run /start-of-day at the start of every session.
Run /end-of-day at the end of every session.

### Cowork
Browser tasks, desktop automation, file management.
Use project-context-updater.html on Cowork-heavy days.

## Change log
- [YYYY-MM-DD] — Project initialized — Source: Claude Code
```

**If general**, use this template:

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
[Key terms and naming conventions from the structure question]

## File map (key files)
| File | Purpose |
|---|---|
| `project-context.md` | Project status and orientation |
| `project-memory.md` | Session decisions and reasoning |
| `[other files]` | [purpose] |

## Key decisions made
- [YYYY-MM-DD] — Project initialized

## Known issues
[From the known issues question, or "None at this time"]

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

## 5. Create project-memory.md

Write the following file to the project root. If **app**, include the second key-decisions bullet; if **general**, omit it.

```markdown
# Project Memory
Last updated: [YYYY-MM-DD]

This file captures decisions, reasoning, and session context that
project-context.md doesn't hold. It is Claude's memory between sessions.

---

## Key decisions (permanent record)

- [YYYY-MM-DD] — Project initialized
- [YYYY-MM-DD] — Architecture decision: [Static frontend / Full stack]     ← app projects only

---

## Sessions

<!-- end-of-day skill appends new sessions here -->
```

---

## 6. Save both files

If this folder isn't a git repo yet, initialize it first:

```bash
git rev-parse --is-inside-work-tree || git init
```

Then commit:

```bash
git add project-context.md project-memory.md
git commit -m "New [app ]project initialized — [Project Name]"
```

Use "New app project initialized" for app projects, "New project initialized" for general ones.

---

## 7. Publish to GitHub

Use the `publish-to-github` skill to create the GitHub repo and push this initial commit. It will ask for a repo name (default to the project's folder name) and public/private (default private) — don't skip that confirmation.

If the skill stops because `gh` isn't installed or authenticated, tell the user and continue to Step 8 anyway — the project is still fully set up locally, it just isn't backed up to GitHub yet. Don't block finishing the project over this.

---

## 8. Done

Tell the user:

"Your [app ]project is set up and committed[, and pushed to GitHub / — not yet pushed to GitHub, see above].

From here:
- Start every session with /start-of-day
- End every session with /end-of-day
- Use Chat for [architecture decisions and ]planning

What are we working on in this first session?"

Fill in the bracketed parts based on project type and what happened in Step 7; drop the brackets and extra spacing.
