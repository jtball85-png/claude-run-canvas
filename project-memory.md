# Project Memory
Last updated: 2026-09-28

This file captures decisions, reasoning, and session context that
project-context.md doesn't hold. It is Claude's memory between sessions.

---

## Key decisions (permanent record)

---

## Sessions

## Session — 2026-09-28

**Focus:** Setting up the 2026-27 pilot Intro courses (467 Bookkeeping, 451 Business Administration, 468 Business & Accounting) for students; Canvas admin cleanup.

**Decisions made:**
- Josh enrolled as Teacher in course 329 "Orientation" (not course 3 "Passport to Canvas") and it was added to his Dashboard favorites — Josh chose 329; favoriting requires an enrollment.
- Student emails come from the Orientation course 329 roster (Josh's instruction); students matched by SIS ID Number.
- Enrolled 14 students as active StudentEnrollment, no notification: 467 — Archer, Hernandez Cortez, Kingston, Muro, Schultz, Vitruls; 451 — J. Gonzalez, N. Gonzalez, Kims, Lopez, Menchaca; 468 — Galindo, Szatkowski, Torres. Jessica Perez (ID 14703897) left out per Josh — no Canvas account found. Argelia Muro (user 1027) has no SIS ID and is not in 329; Josh approved adding her.
- No announcements or notification emails to these students for now (Josh).
- Mariya Messier added as Teacher to 467/451/468 using user 114 (Mariya.Messier@adultedventura.edu) — she has two other Canvas accounts (venturausd.org, yahoo.com) that were not used.
- Intro courses are an introduction only: student menu limited to Home, Modules, Syllabus, Pages, Assignments, Discussions, Quizzes, Files, Grades, Rubrics; all other tabs hidden.
- New Students module and its 3 assignments (New Student Paperwork, CASAS Testing, Student Assessment) removed from all 3 Intro courses (Josh).
- Each Intro course now has a published "Getting to Know Canvas" module: a "What is ___?" page per menu item (What it is / Where to find it / Try it) plus practice examples (assignment + rubric, discussion, quiz, Canvas Quick Guide PDF). Practice assignment and quiz have omit_from_final_grade=true. Home page has a Start button linking to the module's first item so Next buttons walk the tour.
- Styling for new pages reuses box()/heading()/INSTRUCTORS_HTML/COHORT_SCHEDULES_HTML imported from scripts/create_program_overview_course.py.
- Susan Vinson (user 153) removed from Account Teacher and deleted from the root account — retired (Josh).

**Problems solved:**
- Program Overview modules in the Intro courses were unpublished, so students couldn't see them — now published.
- Temp scripts outside the repo don't find .env with bare load_dotenv(); load with an explicit path to the repo's .env. Python is invoked as `py -3` on this machine (`python` is the Store alias).

**Approaches discussed:**
- Making Mariya a read-only teacher in the Intro courses: a custom Teacher-based course role (e.g. "Instructor (View Only)") in sub-account 106 would only be cosmetic, because her root-account "Account Teacher" admin role (role 113) grants course content/wiki/file add-edit-delete in every course. Narrowing role 113 affects all 13 holders.
- Canvas Rubrics tab is teacher-only; students see rubrics only inside assignments.

**Left unresolved:**
- Mariya read-only access: no option chosen yet (custom course role alone vs. also changing her Account Teacher admin role).
- 468's Welcome page is still titled/written "Business & Finance" while the course is "Business & Accounting" — Josh hasn't said whether to rename.
- After Susan Vinson's deletion, courses 176, 177, 178, 246, 315, 319 have no teacher; 178 (1 student) and 315 (3 students) still have enrolled students.
- Possible duplicate admin accounts noticed: Edina Loasky / Edina Loskay; Scott Collins (two logins). "Jeffey" Albaugh display-name typo.
- Screenshot roster may have continued past Arely Menchaca — not confirmed.

**Files changed this session:**
 scripts/build_intro_canvas_tour.py | 550 +++++++++++++++++++++++++++++++++++++
 templates/computer-basics.json     | 219 +++++++++++++++
 2 files changed, 769 insertions(+)
(templates/computer-basics.json was an uncommitted change from before this session — not touched today)

## Session — 2026-03-24

**Focus:** Upgrade project to new session management system — add .claude/commands/ folder with /start-of-day, /end-of-day, /new-project skills; create project-memory.md.

**Decisions made:**
- Adopted .claude/commands/ as the location for custom slash commands — this is the Claude Code convention for project-scoped skills.
- project-memory.md replaces the old captains-log.md pattern — session context now lives here, not in a separate log file.
- No captains-log.md existed in this project, so no archive migration was needed.

**Files changed this session:**
 .claude/commands/end-of-day.md   | new file
 .claude/commands/new-project.md  | new file
 .claude/commands/start-of-day.md | new file
 project-memory.md                | new file

