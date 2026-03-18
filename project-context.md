# Project: Claude Run Canvas
Last updated: 2026-03-18 by Claude Code

## What this project is
We are building a set of tools and scripts that allow Canvas LMS admins and instructors at Ventura Adult and Continuing Education to use Claude and the Canvas API to manage, build, and standardize courses. The project is for the admin team (starting with two contributors) and aims to bring consistency across 4–5 programs by creating shared course templates, reducing manual repetitive work, and giving instructors a smarter way to build and maintain their Canvas content.

## Current status
Pipeline complete. Can create modules, pages, and assignments in Canvas from a JSON template file. Skeleton template for Business and Finance pushed to sandbox course 301. Ready to design real template content in Chat.

## Where we left off
Last commit: 8a695e6 — Add push_course.py and business-and-finance.json skeleton template -- pipeline tested against sandbox 301
In progress: none
Branch: main

## What's next
- [ ] Go to Chat — design real content for business-and-finance.json (modules, pages, assignments, syllabus)
- [ ] Replace placeholder content in templates/business-and-finance.json with Chat-designed content
- [ ] Re-push updated template to sandbox and review in Canvas
- [ ] Add Alex Kohanim as GitHub collaborator (do in GitHub settings)
- [ ] Set git user name/email (currently auto-configured from hostname)

## File structure
/Claude Run Canvas
  /scripts
    test_connection.py  → confirms API token and base URL are working
    list_courses.py     → pulls all courses from the account (178 total)
    push_course.py      → reads a template JSON and pushes it to a Canvas course
  /templates
    business-and-finance.json  → skeleton template (4 modules, 13 items) — content is placeholder
  /docs                → How-to guides, SOPs (empty for now)
  /archive             → Archived context docs
  .env                 → API credentials (never committed to GitHub)
  .gitignore           → Excludes .env and system files
  project-context.md   → This file

## Key decisions made
- **Template format**: JSON files in /templates — one file per program. push_course.py reads them and pushes to Canvas.
- **Sandbox for testing**: Course ID 301 (Sandbox Course - Josh Ball Training) — use this before pushing to any real course
- **Template design in Chat**: Actual course content (syllabus, objectives, lesson text, assignments) gets written in Chat using an artifact, then pasted into the JSON
- **First template**: Business and Finance — skeleton pushed to sandbox 301 on 2026-03-18
- **Tech stack**: Python, direct REST calls to Canvas API, python-dotenv for credentials, requests library
- **GitHub repo**: https://github.com/jtball85-png/claude-run-canvas
- **Claude Code for all scripting**: All API scripts and automation written and run in Claude Code
- **GitHub for collaboration**: Repo will be shared with Alex Kohanim
- **User-Agent header required**: All scripts include User-Agent header in requests

## Known issues
- Sandbox course 301 now has placeholder modules from today's test push — may want to clear before next real push
- .env file must never be committed — .gitignore is in place
- GitHub collaborator access for Alex.Kohanim@adultedventura.edu still needs to be set up
- Git user name/email is auto-configured from hostname — set manually with git config --global

## Context for each tool

### Chat
- Use Chat for planning, decisions, and template content design
- Next Chat task: design real content for business-and-finance.json using an artifact
- Tone: practical and direct — this is a working admin tool, not an academic project
- Always think about adult education context: varied literacy levels, multiple programs, small admin team
- When suggesting approaches, prefer simple and maintainable over clever

### Claude Code
- Tech stack: Python, requests, python-dotenv
- Canvas API base URL: https://adultedventura.instructure.com/api/v1
- All scripts must include User-Agent header in requests
- .env file stores API token — never hardcode credentials, never commit .env
- Sandbox course ID: 301 — always test here first
- Files off-limits: .env (never touch, never commit)

### Cowork
- Use Cowork when instructed for browser tasks: navigating Canvas admin panel, managing GitHub collaborator access
- Canvas admin panel: Ventura Adult and Continuing Education account
- GitHub: https://github.com/jtball85-png/claude-run-canvas
- Use project-context-updater.html on Cowork-heavy days

## Change log
Auto-updated by Captain's Log at end of every Code session.
On Cowork-heavy days, use project-context-updater.html instead.
- 2026-03-18 — Project kickoff complete. Context doc created. — Source: Chat
- 2026-03-18 — Repo initialized, .gitignore added, pushed to GitHub. Canvas API token stored in .env. test_connection.py confirmed working (Account ID 1, Ventura Adult and Continuing Education). — Source: Claude Code
- 2026-03-18 — list_courses.py built and run — 178 courses found. push_course.py built. business-and-finance.json skeleton template created (4 modules, 13 items). Pipeline tested live against sandbox course 301 — all modules and pages created successfully. — Source: Claude Code
