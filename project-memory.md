# Project Memory
Last updated: 2026-10-06

This file captures decisions, reasoning, and session context that
project-context.md doesn't hold. It is Claude's memory between sessions.

---

## Key decisions (permanent record)

---

## Sessions

## Session — 2026-10-06

**Focus:** Course 452 — quiz attempts, restoring practice quizzes in the Daily Lessons decks, grading submitted assignments.

**Decisions made:**
- 452: all 15 quizzes set to 2 attempts, scoring keep_highest (Josh). All 76 assignments already allowed unlimited attempts — unchanged. Template/push_course.py don't set allowed_attempts, so a rebuild from template reverts to 1 attempt.
- 452 Daily Lessons decks now uploaded unchanged WITH embedded interactive quizzes as student practice (Josh: the "take it in Canvas" placeholder confused students). Reverses 2026-10-05 stripping. Practice questions are identical to the graded quizzes — Josh accepted this. upload_computer_basics_slides.py updated (no stripping; --check compares Canvas copy to the raw deck). New file ids 21774-21782.
- Grading workflow (Josh): Claude drafts scores against each rubric, shows a table (full credit / partial-zero with reasons / borderline calls), posts only after approval with posted_grade + rubric_assessment + short student comment ending "You can resubmit anytime." only when points are off.
- Hands-On 1.1 (Log In to Windows): any screenshot gets full credit (Josh). Short written answers graded leniently (Jessica Gonzalez 1.3 "protects your accounts" → 2/2).

**Problems solved:**
- Graded all 49 pending 452 submissions (15 students): 41 full credit, 8 with points off + note — Jessica Gonzalez 1.2 0/3 (pottery photo, wrong file), Natalia Gonzalez 1.2 0/3 (Recycle Bin not moved), Jeremiah Kims 1.4-1.6 3/4, SB 1.1 3.5/5, 1.7-1.8 1.5/3, 2.1-2.2 2/4, 2.6 1.5/3, 2.7-2.10 0/4. All verified in Canvas; 452 has no manual post policy, so grades are visible to students immediately. 0 submissions left needing grading.

**Left unresolved:**
- Josh to open a Daily Lessons deck in 452 Student View — Canvas rendering of uploaded .html not yet seen.
- Adding allowed_attempts: 2 to the 452 template so a rebuild keeps it (offered, not answered).

**Files changed this session:**
 scripts/upload_computer_basics_slides.py | 271 +++++++++++++++++++++++++++++++
 templates/computer-basics.json           | 219 +++++++++++++++++++++++++
 2 files changed, 490 insertions(+)

## Session — 2026-10-05

**Focus:** Put Josh's Computer Basics lesson materials in a student-visible folder in course 452 so students can follow along; fix the Day 2 prerequisite in 454.

**Decisions made:**
- Only the Slides decks (Day 01-09) go to students, not the .md lesson plans — the .md files are teacher-facing (timings, cold-call questions, hours model) (Josh chose "Slides only").
- Reinforcement 01 Slides deck left out — it is teacher notes only (seating, login troubleshooting).
- 452 Files > "Daily Lessons" folder, visible to students immediately (Josh).
- Decks embed the graded Canvas quizzes with correct answers (163 questions; e.g. Desktop Features Check is verbatim). Josh chose to strip them: each quiz run is replaced with "This check is a graded quiz. Take it in Canvas from today's module."
- One version of each lesson: teacher decks in `Master Business Finance Program/Lesson Planning/Computer Basics/Daily Lesson Plans/` stay the only source. Student copies are built on the fly by scripts/upload_computer_basics_slides.py and exist only in Canvas (uploaded with on_duplicate=overwrite; 452 file ids 21639-21647, folder 3019).
- Josh asked how he can know his and students' copies are updated correctly → added `--check` (changes nothing): (1) Canvas copy byte-identical to a fresh student copy of each deck (ok / OUT OF DATE / MISSING / HIDDEN / EXTRA); (2) each deck's practice quiz vs. the graded Canvas quiz of the same title (count, points, wording, choices, correct answers → DIFFERENT). Every upload ends with the same report. Routine: Josh says "update the Computer Basics slides in 452" → run upload, show report. If a quiz is DIFFERENT, ask Josh which side is right — decks and Canvas quizzes are maintained separately.

**Problems solved:**
- 454 Day 2, Chapter 2: Email had no prerequisite and none of its 14 items had completion requirements (likely wiped by the WebSim rebuild of Day 2), so Day 3 could never unlock. Re-ran go_live_course.set_prerequisites(454): Days 1-6 chained, every Day item has a requirement (must_view 38, must_submit 23, must_mark_done 10).
- `--check` verified against deliberately edited scratch copies (slide text change, flipped correct answer, reworded question) — all three flagged.

**Left unresolved:**
- Josh to open a Daily Lessons deck in 452 Student View — Canvas rendering of uploaded .html files not yet seen.
- scripts/upload_computer_basics_slides.py not committed (Josh not asked yet).
- Rebuilding a Day module's items can wipe its prerequisite/requirements — re-run `go_live_course.py <id> --prerequisites` after any rebuild.

**Files changed this session:**
 scripts/add_outlook_websim_access_section.py       | 119 ++++++++++
 scripts/fix_outlook_day2_overview.py               | 109 +++++++++
 .../replace_outlook_day2_handson_with_websims.py   | 247 +++++++++++++++++++++
 templates/computer-basics.json                     | 219 ++++++++++++++++++
 4 files changed, 694 insertions(+)
 (uncommitted, new: scripts/upload_computer_basics_slides.py)

## Session — 2026-10-02

**Focus:** Add Nicole Hofferbert as teacher; take Josh's classes live (student menu, publish modules, syllabus, prerequisites), starting with 452.

**Decisions made:**
- Nicole Hofferbert (user 627, Nicole.Hofferbert@adultedventura.edu) added as active Teacher to 467, 451, 468, 452, 454, 455, 456 (Josh).
- 452, 454, 455 are Josh's classes: syllabus and Welcome page list only Josh as instructor (Josh). Intro courses 467/451/468 list Josh and Mariya — confirmed already correct.
- Taken live (452 Computer & Internet Fundamentals, 454 Outlook, 455 Word): student menu Home, Modules, Syllabus, Pages, Assignments, Quizzes, Files, Grades, Rubrics; Discussions hidden (no discussions exist); all modules and items published; course image folders (textbook-images, solution-screenshots, images) hidden from Files so only Presentations show — hidden files still render embedded.
- Syllabus for each class built from the front page boxes (Course At A Glance, Your Instructor, Course Description, Cohort Schedules, Course Map) plus generated How You're Graded table (total points: 452=603, 454=480, 455=595) and What We Expect box.
- "Solution" screenshots in 452 are intentional "Example of a Completed Submission" images inside Additional Skill Builder assignments — fine for students to see.
- Prerequisites (Josh): each "Day ..." module requires the previous Day module; Day 1 and Course Overview / How to Use Class Resources open. Every Day-module item has a completion requirement; no sequential order within a day. Pages/Files/ExternalTool = must_view; online assignments and quizzes = must_submit; eLab (external_tool) and no-submission assignments = must_mark_done (13 items in 454) because eLab grade passback to Canvas is unconfirmed.
- All of the above is in scripts/go_live_course.py (--syllabus, --hide-tabs, --hide-folders, --prerequisites); safe to re-run.

**Problems solved:**
- Unpublished Classic Quizzes report 0 points_possible — syllabus grading total must be computed after publishing (454 first showed 293, correct is 480). Script now publishes before writing the syllabus.
- Re-running go_live_course without --hide-tabs re-showed Discussions; set_tabs now auto-hides Discussions when a course has no discussion topics.

**Left unresolved:**
- 456 Business Math not yet taken live; Josh not yet asked whether it gets prerequisites.
- Confirm in Student View that Day 2 shows locked in 452/454/455.
- If eLab passes scores back to Canvas, switch the 10 eLab quiz/test items in 454 from must_mark_done to must_submit.
- Nicole is a teacher in all 7 courses but not named on any Welcome page/syllabus (Josh: his classes list only him).

**Files changed this session:**
 scripts/go_live_course.py      |  51 ++++++++++
 templates/computer-basics.json | 219 +++++++++++++++++++++++++++++++++++++++++
 2 files changed, 270 insertions(+)
(diff vs HEAD~1 only; go_live_course.py was created this session across commits 83c15de, dc7f372, 8f72b67. computer-basics.json is pre-existing uncommitted work)

## Session — 2026-09-28 (continued, after first wrap-up)

**Focus:** Finishing Intro course rosters; student roster spreadsheet.

**Decisions made:**
- Jessica Perez (user 1049, SIS 14703897, jessica.perez@adultedventura.edu) enrolled as active student in 467 Bookkeeping — her Canvas account was created after the earlier roster pass (per staff note: Accounting Clerk student, starting 10/6). Bookkeeping cohort is now 7.
- Argelia Muro (user 1027) now has SIS ID 7298964 and is in 329 Orientation and 467 — the account used earlier is her real one.
- Student roster workbook kept outside the git repo (C:\Users\jball.VACE\Documents\Intro Program Students 2026-27.xlsx) so student data is never pushed to GitHub. Final columns per Josh: Photo, Name, School Email, Program; tabs "By Program" and "All Students".
- Personal email and phone dropped from the workbook (Josh: "that's fine").

**Problems solved:**
- Student photos pulled from Canvas avatar_url (GET /users/:id?include[]=avatar_url, download with auth header). URLs ending in avatar-50.png are the default placeholder, not a photo.

**Approaches discussed:**
- Personal emails/phones are not stored in Canvas: each student has one account and only the school email as a communication channel. They must come from the enrollment spreadsheet.
- skills xlsx recalc.py does not run on this Windows machine (LibreOffice needs socket.AF_UNIX).

**Left unresolved:**
- No Canvas profile photo yet for Argelia Muro, Jessica Perez, Michelle Torres — workbook shows "No photo".
- Items from the earlier 2026-09-28 entry still open (Mariya read-only access, 468 Welcome page title, teacherless courses after Susan Vinson's deletion, duplicate admin accounts).

**Files changed this session:**
 project-context.md             |   7 +-
 project-memory.md              |  39 +++++++-
 templates/computer-basics.json | 219 +++++++++++++++++++++++++++++++++++++++++
 3 files changed, 261 insertions(+), 4 deletions(-)
(no repo files changed after the first wrap-up; computer-basics.json is pre-existing uncommitted work)

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

