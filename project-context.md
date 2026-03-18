# Project: Claude Run Canvas
Last updated: 2026-03-18 by Chat

## What this project is
We are building a set of tools and scripts that allow Canvas LMS admins and instructors at Ventura Adult and Continuing Education to use Claude and the Canvas API to manage, build, and standardize courses. The project is for the admin team (starting with two contributors) and aims to bring consistency across 4–5 programs by creating shared course templates, reducing manual repetitive work, and giving instructors a smarter way to build and maintain their Canvas content.

## Current status
Foundation complete. Repo live on GitHub, Canvas API connection confirmed working. Ready to build first real script.

## Where we left off
Last commit: d94668e — Add test_connection.py -- confirms Canvas API connection working
In progress: none
Branch: main

## What's next
- [ ] Create folder structure: /scripts, /templates, /docs
- [ ] Write first real script — pull list of courses from the account
- [ ] Add Alex Kohanim as GitHub collaborator
- [ ] Set git user name/email (currently auto-configured from hostname)

## File structure
/Claude Run Canvas
  /scripts      → Python or JS scripts for Canvas API interactions
  /templates    → Course template definitions (JSON or structured files)
  /docs         → How-to guides, SOPs, onboarding docs for other instructors
  /archive      → Archived context docs
  .env          → API credentials (never committed to GitHub)
  .gitignore    → Must include .env
  README.md     → Project overview and setup instructions for collaborators

## Key decisions made
- **New Developer Key**: We will create a dedicated Developer Key for this project, not reuse existing ones (CertMaster, Cengage, Quizizz keys are for other tools)
- **First deliverable**: A course template pushed via API to a test course in Canvas
- **Claude Code for all scripting**: All API scripts and automation will be written and run in Claude Code
- **GitHub for collaboration**: Repo will be shared with at least one other contributor (Alex Kohanim) who will also push changes
- **User-Agent header required**: Canvas is enforcing User-Agent headers on all API requests — all scripts must include this from the start

## Known issues
- Canvas User-Agent enforcement date not confirmed — check API Change Log before first API call
- .env file must never be committed — .gitignore setup is critical before first push
- GitHub collaborator access for Alex.Kohanim@adultedventura.edu needs to be set up after repo creation (user must do this themselves in GitHub settings)

## Context for each tool

### Chat
- Use Chat for planning, decisions, template design, and thinking through Canvas structure
- Tone: practical and direct — this is a working admin tool, not an academic project
- Always think about adult education context: varied literacy levels, multiple programs, small admin team
- When suggesting approaches, prefer simple and maintainable over clever
- Do not revisit key decisions (Developer Key, GitHub, Claude Code for scripting) unless user raises it

### Claude Code
- Tech stack: TBD at setup — likely Python for Canvas API scripts (canvas-python or direct REST calls)
- Canvas API base URL: https://adultedventura.instructure.com/api/v1 (confirm before first call)
- All scripts must include User-Agent header in requests
- .env file stores API token — never hardcode credentials
- Captain's Log skill handles end-of-day updates automatically
- Files off-limits: .env (never touch, never commit)

### Cowork
- Use Cowork when instructed for browser tasks: navigating Canvas admin panel, setting up Developer Keys, managing GitHub collaborator access
- Canvas admin panel: Ventura Adult and Continuing Education account
- GitHub: new repo to be created under user's GitHub account
- Use project-context-updater.html on Cowork-heavy days

## Change log
Auto-updated by Captain's Log at end of every Code session.
On Cowork-heavy days, use project-context-updater.html instead.
- 2026-03-18 — Project kickoff complete. Context doc created. — Source: Chat
- 2026-03-18 — Repo initialized, .gitignore added, pushed to GitHub. Canvas API token stored in .env. test_connection.py confirmed working (Account ID 1, Ventura Adult and Continuing Education). — Source: Claude Code
