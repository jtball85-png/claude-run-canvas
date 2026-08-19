# Project: Claude Run Canvas
Last updated: 2026-03-24 by Claude Code

## What this project is
We are building a set of tools and scripts that allow Canvas LMS admins and instructors at Ventura Adult and Continuing Education to use Claude and the Canvas API to manage, build, and standardize courses. The project is for the admin team (starting with two contributors) and aims to bring consistency across 4–5 programs by creating shared course templates, reducing manual repetitive work, and giving instructors a smarter way to build and maintain their Canvas content.

## Current status
Business and Finance course (6 modules, 29 items) live in sandbox 301. Computer Basics: Windows 11 Edition course (10 chapters, ~55 items — Pages, Files, Assignments, Quizzes) also live in sandbox 301, built chapter-by-chapter from the Labyrinth Learning instructor package and verified against the CBO and official Answer Key. push_course.py now handles Page, Assignment, Discussion, Quiz, and File (real Canvas file upload, 3-step preflight/upload/confirm) item types.

## Where we left off
Last commit: 183bdd5 — Update project-context.md -- Business and Finance template complete, session 2 wrap-up
In progress: none
Branch: main

## What's next
- [ ] Josh reviewing full 10-chapter Computer Basics build in Canvas sandbox (course 301)
- [ ] Once approved, spin up a dedicated Canvas course for Computer Basics instead of sharing sandbox 301 with Business and Finance, and push there
- [ ] Get Labyrinth eLabs portal access code so WebSim/video links can be added as External URL items (Chapter 10 especially relies on WebSims for system-settings exercises)
- [ ] Josh getting access to the actual ebook — once available, the 9 Hands-On exercises per chapter (currently only titles/outcomes from the Solutions Guide) can be scripted with their real step-by-step instructions
- [ ] Review Business and Finance template in Canvas sandbox (course 301) — check pages, quizzes, discussions look correct
- [ ] Decide on next program template to build (Medical Assistant? Computer programs?)
- [ ] Add Alex Kohanim as GitHub collaborator (do in GitHub settings)
- [ ] Set git user name/email (currently auto-configured from hostname)

## File structure
/Claude Run Canvas
  /scripts
    test_connection.py  → confirms API token and base URL are working
    list_courses.py     → pulls all courses from the account (178 total)
    push_course.py      → reads a template JSON and pushes it to a Canvas course
  /templates
    business-and-finance.json  → full template (6 modules, 29 items) — real content, Chat-designed
  /docs                → How-to guides, SOPs (empty for now)
  /archive             → Archived context docs
  .env                 → API credentials (never committed to GitHub)
  .gitignore           → Excludes .env and system files
  project-context.md   → This file

## Key decisions made
- **Template format**: JSON files in /templates — one file per program. push_course.py reads them and pushes to Canvas.
- **Sandbox for testing**: Course ID 301 (Sandbox Course - Josh Ball Training) — use this before pushing to any real course
- **Template design in Chat**: Actual course content (syllabus, objectives, lesson text, assignments) gets written in Chat using an artifact, then pasted into the JSON
- **First template**: Business and Finance — full template (6 modules, 29 items) pushed to sandbox 301 on 2026-03-18. Includes Pages, Assignments, Discussions, and Quizzes with embedded questions.
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
- 2026-08-19 — Built and pushed Chapters 2-10 of Computer Basics, completing the full 10-chapter course in sandbox 301. Each chapter cross-verified: CBO objectives (from the Business and Finance CBO), Lecture Notes, Test Bank questions checked against the official Answer Key (100% match on spot-checks), Additional Skill Builder exercises used verbatim, in-book Skill Builders and Hands-On exercises named from the Printable Solutions Guide, and each chapter's PowerPoint uploaded as a real Canvas File. Course total: ~55 items across 10 modules. Known gap: exact Hands-On step-by-step instructions aren't available without the physical textbook (Josh is getting ebook access) — Source: Claude Code
- 2026-08-19 — Second, deeper Chapter 1 correction (Josh caught this too): the source package has a taxonomy I'd missed — 9 in-book Hands-On exercises (HO 1.1-1.9, the main chapter content) and 1 in-book Skill Builder (SB 1.1), both distinct from the "Additional Skill Builder" file used in the first fix. Found via `Course Preparation Document.pdf` (defines Hands-On vs. Skill Builder vs. Try This at Home) and `WTCB11_Printable_Solutions_Guide.pdf` (titles/outcomes/screenshots for every exercise per chapter — the only source for these since the textbook itself isn't in the instructor package). Also added File-upload support to `push_course.py` (Canvas's 3-step file API: preflight POST, upload POST, confirm) since the PPT was being described in prose instead of actually placed in the course. Rebuilt Chapter 1: Page now walks through all 9 Hands-On exercises by name, added Skill Builder 1.1 as its own assignment, uploaded the PPT as a real Canvas File, kept Additional Skill Builder 1.1 and the Quiz. Deleted and re-pushed in sandbox 301 — Source: Claude Code
- 2026-08-19 — Corrected the Chapter 1 assignment: it had been invented rather than sourced from the actual `Additional Skill Builders/Unit 1/Chapter 01/Exercise/WTCB11 Additional Skill Builder 1.1.docx` file (Josh caught this). Deleted the wrong module/page/assignment/quiz from sandbox 301 and re-pushed with the real exercise ("Pin an App to the Start Menu"). Lesson: open every file in a chapter's source folder (including Additional Skill Builders subfolders) before building — don't rely on Table of Contents + Lecture Notes + Test Bank alone — Source: Claude Code
- 2026-08-19 — Built and pushed `templates/computer-basics.json` (Chapter 1: Getting Your First Look — Page, Assignment, 10-question Quiz) to sandbox 301, alongside the existing Business and Finance modules (not cleared). Content built from the Business and Finance CBO's Computer & Internet Fundamentals objectives plus the Labyrinth Learning instructor package (Lecture Notes, Test Bank, verified against the official Answer Key). Driven from the `Master Business Finance Program` hub project — see its `Lesson Planning/Computer Basics/` folder for the source lesson plan. First chapter of a planned 10-chapter build — Source: Claude Code
- 2026-03-24 — Session management system added: .claude/commands/ with /start-of-day, /end-of-day, /new-project; project-memory.md created — Source: Claude Code
- 2026-03-18 — Project kickoff complete. Context doc created. — Source: Chat
- 2026-03-18 — Repo initialized, .gitignore added, pushed to GitHub. Canvas API token stored in .env. test_connection.py confirmed working (Account ID 1, Ventura Adult and Continuing Education). — Source: Claude Code
- 2026-03-18 — list_courses.py built and run — 178 courses found. push_course.py built. business-and-finance.json skeleton template created (4 modules, 13 items). Pipeline tested live against sandbox course 301 — all modules and pages created successfully. — Source: Claude Code
- 2026-03-18 — Real Business and Finance template dropped in from Chat (6 modules, 29 items). push_course.py updated to support Discussion and Quiz types (with embedded questions) and --clear-first flag. Full template pushed live to sandbox 301 with zero errors. — Source: Claude Code
