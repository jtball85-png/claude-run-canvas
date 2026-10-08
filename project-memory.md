# Project Memory
Last updated: 2026-10-08

This file captures decisions, reasoning, and session context that
project-context.md doesn't hold. It is Claude's memory between sessions.

---

## Key decisions (permanent record)

---

## Sessions

## Session — 2026-10-08 (checkpoint 2)

**Focus:** Fix 452 Chapter 2 exercise instructions (Hands-On 2.1-2.2, 2.3, 2.7-2.10) in Canvas, templates, and Day 3 lesson plan/slides.

**Decisions made:**
- 2.1-2.2: example image replaced with Josh's own snapped File Explorer screenshot, with OneDrive name, colleague names, recent files and a "Cindy Docs" icon blurred (Josh loved the blur, now a standing rule for teacher screenshots). Canvas file 22677 "HO 2.2 Snap Example.png" (hidden textbook-images folder); local copy in Extracted Solutions/Chapter 2. "What to submit" asks for whole screen, File Explorer filling exactly half.
- 2.3: classroom PCs aren't touchscreens, so submission is now Text Entry with one question only: "Does your computer support touch? (Yes or No)" (Josh dropped the Pen and touch text question). Rubric 461 criterion reworded in place (same ids), still 2 pts. Day 3 Overview says "written answer".
- 2.7-2.10: amber note added: if Alt+Tab can't be captured, submit a Task View screenshot showing Calculator, Notepad and Paint, plus a comment; full credit either way. Rubric 464 reworded in place to accept Alt+Tab box or Task View.

**Problems solved:**
- All changes verified in 452; posted grades untouched (rubrics edited in place, not replaced). Both templates (computer-internet-fundamentals.json, computer-basics.json) updated to match. Day 03 Slides, Day 03 Lesson Plan.md and lesson-plan-content.json updated (Master Business Finance Program/Lesson Planning/Computer Basics/Daily Lesson Plans); all 9 decks re-uploaded to 452, check ALL GOOD.

**Left unresolved:**
- 2.7-2.10 example images (HO 2.7-2.10) don't show the Alt+Tab box or Task View; Josh may send a Task View screenshot (blur before use).
- Template changes uncommitted: templates/computer-basics.json (also had older uncommitted changes), templates/computer-internet-fundamentals.json (untracked), scripts/upload_computer_basics_slides.py.

**Files changed this session:**
 scripts/upload_computer_basics_slides.py |  79 +++++- (older, uncommitted)
 templates/computer-basics.json           | 461 ++++++++++++++++++++++++++++++- (uncommitted)
 templates/computer-internet-fundamentals.json (untracked)

## Session — 2026-10-08 (checkpoint)

**Focus:** Grade course 452 assignments through Day 3, Chapter 2 (assignments 8386-8405).

**Decisions made:**
- Josh: Windows 10 students get full credit where Win10 differs (Argelia 1.4-1.6, Natalia 2.1-2.2, Ashley 2.6); also full credit for Ashley 2.1-2.2 (snapped Chrome, not File Explorer), Rick 2.6 (app list cut off), Jose Skill Builders 2.1-2.3 (screenshot 3 after Show Desktop), Jessica Perez 2.7-2.10 (no Alt+Tab, no comment).
- Hands-On 2.7-2.10: full credit class-wide. The Snipping Tool closes the Alt+Tab box; 7 students commented on it.
- Josh asked whether resubmissions are caught. From now on every grading draft gets its own "Resubmissions" section (old score → new), even when empty.

**Problems solved:**
- Posted 82 pending submissions (15 students), all full credit, no comments; verified all 82 in Canvas; 0 left needing grading through Day 3. No pending resubmissions; the 9 earlier resubmissions were already graded on their latest attempt.
- Jeremiah Kims Hands-On 2.7-2.10 raised 0/4 → 4/4 (Josh approved), with comment "Updated to full credit. The Snipping Tool can't capture the Alt+Tab box, so no need to resubmit!"

**Left unresolved:**
- Josh to review the Hands-On 2.7-2.10 instructions next (Alt+Tab can't be captured with the Snipping Tool; options: Task View screenshot or Snipping Tool delay timer).
- scripts/upload_computer_basics_slides.py and templates/computer-basics.json still uncommitted.

**Files changed this session:**
 none in the repo (Canvas grading only)

## Session — 2026-10-07 (checkpoint 3)

**Focus:** 452 Daily Lessons decks showed blank boxes for practice quizzes when opened inside Canvas (fine when downloaded).

**Decisions made:**
- Cause: Canvas file preview runs HTML with JavaScript disabled; slide nav is pure CSS (works), quiz questions were JS-rendered (blank). Fix in scripts/upload_computer_basics_slides.py `student_copy()`: every question pre-rendered as no-JS HTML/CSS — radio inputs + :checked rules give click-for-instant-feedback (green Correct!/red "Not quite — correct answer: X", :has() highlights the right answer); the one short-answer question (Day 1 Desktop Features Check) uses a <details> "Check Answer" reveal. Source decks unchanged; --check compares Canvas copy to student_copy(). Students can now change their answer (old JS version locked after first click).
- Students use Chrome and Edge (Josh) — both Chromium; tested in Edge.

**Problems solved:**
- Tested with headless Edge served from a local server sending `Content-Security-Policy: script-src 'none'`: unfixed Day 2 reproduced the 4 blank boxes; fixed version showed all questions, feedback worked, short answer reveal worked; JS-on (downloaded) copy has 14 questions, no duplicates. Edge's --blink-settings=scriptEnabled=false breaks --screenshot; file:// from scratchpad doesn't load — use localhost.
- Re-uploaded Day 01-09 to 452 (file ids 22522-22530); check ALL GOOD (9 slides, 15 quizzes).

**Left unresolved:**
- scripts/upload_computer_basics_slides.py change not committed.
- Josh to confirm in 452 Student View (Day 2 slide 13) — rendering seen only in the local test, not inside Canvas.

**Files changed this session:**
 scripts/upload_computer_basics_slides.py | 79 +++++++++++++++++++++++++++-----  (uncommitted)

## Session — 2026-10-07 (checkpoint 2)

**Focus:** Follow-ups on 452 Chapter 1 grading; commit synced .claude tools.

**Problems solved:**
- Ashley Schultz Hands-On 1.4-1.6: Josh had already set 4/4; follow-up comment posted so the old "screenshot missing" note isn't confusing.
- Jessica Gonzalez Skill Builder 1.1 reviewed: correct (Media Player first in row 1, Clock first in row 2), 5/5 earned on the rubric. Reply posted to her question: "You did it exactly right. Media Player is first and Clock starts the second row. Great job!"
- .claude tools from project-template committed (2c82781).

**Files changed this session:**
 14 files changed, 951 insertions(+), 41 deletions(-)  (.claude agents, commands, skills)

## Session — 2026-10-07 (checkpoint)

**Focus:** Grade all course 452 Chapter 1 assignments; add template Claude tools to this project.

**Decisions made:**
- Grading rules (Josh): ALWAYS read submission comments (include[]=submission_comments) and check ALL attempts (submission_history) before drafting. For every points-off submission, build a local HTML review page (scratchpad, opened with `start`, not published — student work): requirements, each attempt's screenshots, rubric posted vs. recommended, student comments, our note, red recommendation box, SpeedGrader link (courses/452/gradebook/speed_grader?assignment_id=X&student_id=Y).
- Chapter 1 leniency (Josh): Skill Builder 1.1 and Hands-On 1.7-1.8 full credit for all who submitted; Windows 10 students (Natalia Gonzalez) full credit on Start-menu assignments; Arely Menchaca and Yesenia Hernandez Cortez full credit.
- .claude tools copied from `Claude Projects Templates/project-template/.claude`: agents architect/coder/manager/tester; commands checkpoint, dev-team, sync-tools; skills audit-phase, markitdown, publish-to-github. start-of-day / end-of-day / new-project overwritten with template versions (Josh chose "use template versions"): start-of-day now git pulls, end-of-day now pushes, new-project asks app vs. general first.

**Problems solved:**
- Graded 54 pending Chapter 1 submissions in 452 (assignments 8386-8395, Day 1-2 modules 2042/2043): 53 full credit, Ashley Schultz Hands-On 1.4-1.6 initially 2/4. All verified in Canvas.
- Review-page test on Ashley found attempt 1 had the "missing" Calculator-open screenshot. Josh changed her to 4/4 in Canvas; follow-up comment posted ("Found your Calculator screenshot in your first attempt. Full credit, no need to resubmit!").
- Student comments read: Natalia (Win10, ×4), Manuela Lopez and Michelle Torres (no Clock app), Manuela 1.2 (Chromebook), Jessica Gonzalez on Skill Builder 1.1 asked whether she did it right — unanswered.

**Left unresolved:**
- .claude tool changes (3 modified commands, new agents/commands/skills) are uncommitted — offered to commit/push, not answered.
- Jessica Gonzalez's Skill Builder 1.1 comment has no reply.

**Files changed this session:**
 .claude/commands/end-of-day.md   |  34 +++++-
 .claude/commands/new-project.md  | 237 +++++++++++++++++++++++++++++++++------
 .claude/commands/start-of-day.md |  39 ++++++-
 (uncommitted; plus new .claude/agents/, .claude/skills/, checkpoint.md, dev-team.md, sync-tools.md)

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

