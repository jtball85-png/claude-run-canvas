"""
build_intro_canvas_tour.py
--------------------------
Turns the "Intro to the <Program> Program (2026-27 Pilot)" courses
(467 Bookkeeping, 451 Business Administration, 468 Business & Accounting)
into a student-facing Canvas orientation:

  1. Removes the old "New Students" module and its 3 assignments
     (New Student Paperwork, CASAS Testing, Student Assessment).
  2. Publishes the "Program Overview" module.
  3. Builds a published "Getting to Know Canvas" module: one styled
     "What is ___?" explainer page per visible menu item, plus a simple
     example of each (practice assignment + rubric, practice discussion,
     practice quiz, Canvas Quick Guide PDF, filled-in syllabus), and adds
     a description + Start button for the tour at the bottom of the home page.
  4. Trims the course menu to Home, Modules, Syllabus, Pages, Assignments,
     Discussions, Quizzes, Files, Grades, Rubrics -- everything else hidden.

Practice items are graded but omitted from the final grade so Grades shows
real rows without counting. No announcements/notifications are sent.
Idempotent: existing items are matched by title and reused, not duplicated.

Usage (run from repo root so .env loads):
  python scripts/build_intro_canvas_tour.py --dry-run 467
  python scripts/build_intro_canvas_tour.py 467 451 468
"""

import argparse
import os
import sys

import requests
from fpdf import FPDF

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from create_program_overview_course import (  # noqa: E402
    BASE_URL, HEADERS, INSTRUCTORS_HTML, COHORT_SCHEDULES_HTML, box, heading,
)

PROGRAM_NAMES = {467: "Bookkeeping", 451: "Business Administration", 468: "Business & Accounting"}

OLD_MODULE = "New Students"
OVERVIEW_MODULE = "Program Overview"
TOUR_MODULE = "Getting to Know Canvas"

VISIBLE_TABS = ["home", "modules", "syllabus", "pages", "assignments", "discussions",
                "quizzes", "files", "grades", "rubrics"]
NEVER_HIDE = {"home", "settings"}  # Canvas won't hide these

QUICK_GUIDE_PDF = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               "generated_worksheets", "Canvas-Quick-Guide.pdf")
QUICK_GUIDE_NAME = "Canvas Quick Guide.pdf"

PRACTICE_ASSIGNMENT = "Practice Assignment: Introduce Yourself"
PRACTICE_RUBRIC = "Introduce Yourself Rubric"
PRACTICE_DISCUSSION = "Practice Discussion: Say Hello to Your Classmates"
PRACTICE_QUIZ = "Practice Quiz: Canvas Basics"
CTA_ID = "getting-to-know-canvas-cta"

DRY_RUN = False


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def get_all(endpoint, params=None):
    url, out = f"{BASE_URL}{endpoint}", []
    params = dict(params or {}, per_page=100)
    while url:
        r = requests.get(url, headers=HEADERS, params=params)
        r.raise_for_status()
        out.extend(r.json())
        url, params = r.links.get("next", {}).get("url"), None
    return out


def send(method, endpoint, payload=None):
    if DRY_RUN:
        print(f"    [DRY RUN] {method} {endpoint}")
        return {"id": 0, "url": "dry-run", "assignment_id": 0}
    r = requests.request(method, f"{BASE_URL}{endpoint}", headers=HEADERS, json=payload)
    if r.status_code >= 400:
        sys.exit(f"ERROR {r.status_code} {method} {endpoint}: {r.text[:300]}")
    return r.json() if r.text else {}


def find(items, key, value):
    return next((i for i in items if i.get(key) == value), None)


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------

def page_shell(eyebrow, title, subtitle, body):
    return (
        '<div style="font-family:Arial,Helvetica,sans-serif;line-height:1.55;color:#1F2937;max-width:920px;margin:0 auto;">'
        '<div style="background:#003462;color:white;border-radius:4px;padding:20px 24px;margin:0 0 16px;">'
        f'<div style="font-size:12px;color:#FFCF01;">{eyebrow}</div>'
        f'<h1 style="margin:4px 0 4px;font-size:28px;line-height:1.15;color:white;">{title}</h1>'
        f'<div style="font-size:17px;line-height:1.35;color:#B5E3F0;">{subtitle}</div>'
        "</div>" + body + "</div>"
    )


def link(href, text):
    return f'<a style="color:#003462;font-weight:bold;" href="{href}">{text}</a>'


def explainer(program, tool, subtitle, what, where, try_it):
    return page_shell(
        f"{program} Program — Getting to Know Canvas",
        f"What {'is' if tool in ('the Syllabus', 'a Rubric') else 'are'} {tool}?",
        subtitle,
        box("#00B7A3", heading("What it is") + what)
        + box("#B5E3F0", heading("Where to find it") + where)
        + box("#FFCF01", heading("Try it") + try_it),
    )


def build_pages(cid, program, ids):
    c = f"/courses/{cid}"
    p = lambda text: f'<p style="margin:0 0 10px;">{text}</p>'
    ul = lambda *items: '<ul style="margin:0;padding-left:20px;">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
    return [
        ("What are Modules?", explainer(
            program, "Modules", "How your coursework is organized, step by step",
            p("A <strong>module</strong> is a folder that groups everything for one topic or week in the order you "
              "should do it: reading pages, files, assignments, discussions and quizzes.")
            + p("In every class in the program, Modules is your main path through the course. Work top to bottom "
                "and you won't miss anything."),
            p("Click <strong>Modules</strong> in the course menu on the left."),
            p(f"You're in a module right now: <strong>{TOUR_MODULE}</strong>. Open "
              + link(f"{c}/modules", "Modules") + " to see it next to the <strong>Program Overview</strong> module."),
        )),
        ("What is the Syllabus?", explainer(
            program, "the Syllabus", "The course's rules of the road",
            p("The <strong>syllabus</strong> is the course summary: who your instructors are, when class meets, "
              "what is expected of you, and how to get help. Below it, Canvas automatically lists every "
              "assignment with its due date."),
            p("Click <strong>Syllabus</strong> in the course menu."),
            p("Open the " + link(f"{c}/assignments/syllabus", "Syllabus") + " for this course and find your "
              "class schedule and your instructors' email addresses."),
        )),
        ("What are Pages?", explainer(
            program, "Pages", "Readings, instructions and information",
            p("A <strong>page</strong> is a web page inside Canvas that holds reading material, instructions, "
              "videos, or links. Pages don't get turned in or graded. They're there for you to read."),
            p("Pages usually appear inside <strong>Modules</strong>. You can also click <strong>Pages</strong> "
              "in the course menu to see all of them in one list."),
            p("You're reading a page right now! Click " + link(f"{c}/pages", "Pages") + " to see every page "
              "in this course, including the Welcome page."),
        )),
        ("What are Assignments?", explainer(
            program, "Assignments", "Work you turn in for a grade",
            p("An <strong>assignment</strong> is work you submit to your instructor: typed answers, an uploaded "
              "file (like a Word document or spreadsheet), or a link. Each assignment shows its due date, points, "
              "and instructions.")
            + ul("Click <strong>Start Assignment</strong> to begin.",
                 "Type your answer or upload your file.",
                 "Click <strong>Submit Assignment</strong>. You'll see a confirmation when it goes through."),
            p("Click <strong>Assignments</strong> in the course menu, or open the assignment from Modules."),
            p("Complete the " + link(f"{c}/assignments/{ids['assignment']}", PRACTICE_ASSIGNMENT)
              + ". It's practice only and won't count toward your grade."),
        )),
        ("What is a Rubric?", explainer(
            program, "a Rubric", "How your work will be scored",
            p("A <strong>rubric</strong> is a scoring guide attached to an assignment. It lists the criteria your "
              "instructor will grade on and how many points each is worth, so you know what a strong submission "
              "looks like <em>before</em> you turn it in.")
            + p("After grading, the rubric shows which rating you earned on each criterion."),
            p("Open an assignment and scroll below the instructions. If it has a rubric, you'll see a scoring table there."),
            p("Open the " + link(f"{c}/assignments/{ids['assignment']}", PRACTICE_ASSIGNMENT)
              + " and look for the <strong>" + PRACTICE_RUBRIC + "</strong> under the instructions."),
        )),
        ("What are Discussions?", explainer(
            program, "Discussions", "Class conversations you can join any time",
            p("A <strong>discussion</strong> is an online conversation. Your instructor posts a question, you post "
              "a reply, and you can respond to classmates. Some discussions require you to post before you can "
              "see other replies."),
            p("Click <strong>Discussions</strong> in the course menu, or open one from Modules."),
            p("Join the " + link(f"{c}/discussion_topics/{ids['discussion']}", PRACTICE_DISCUSSION)
              + " and introduce yourself to your cohort."),
        )),
        ("What are Quizzes?", explainer(
            program, "Quizzes", "Check what you know",
            p("A <strong>quiz</strong> is a set of questions you answer in Canvas, such as multiple choice, "
              "true/false, or short answer. Many quizzes are scored automatically, so you see your results "
              "right after you submit.")
            + ul("Read the instructions: some quizzes are timed or allow only one attempt.",
                 "Answer every question, then click <strong>Submit Quiz</strong>."),
            p("Click <strong>Quizzes</strong> in the course menu, or open one from Modules."),
            p("Take the " + link(f"{c}/quizzes/{ids['quiz']}", PRACTICE_QUIZ)
              + ". You can take it as many times as you like, and it won't count toward your grade."),
        )),
        ("What are Files?", explainer(
            program, "Files", "Documents and handouts for the course",
            p("<strong>Files</strong> holds documents your instructor shares: PDFs, Word documents, spreadsheets, "
              "and handouts. You can view them in Canvas or download them to your computer."),
            p("Click <strong>Files</strong> in the course menu to browse by folder. Files also appear inside Modules."),
            p("Open the " + link(f"{c}/files/{ids['file']}", QUICK_GUIDE_NAME)
              + ", a one-page summary of every menu item in this course. Download it or print it for reference."),
        )),
        ("What are Grades?", explainer(
            program, "Grades", "Your scores and instructor feedback",
            p("<strong>Grades</strong> shows every graded item, your score, and any comments from your instructor. "
              "Click an assignment's name to see the rubric and feedback.")
            + ul("<strong>Submitted:</strong> an icon shows your work is turned in and waiting to be graded.",
                 "<strong>Missing:</strong> the item is past due and not submitted.",
                 "<strong>Comments:</strong> a speech-bubble icon means your instructor left feedback."),
            p("Click <strong>Grades</strong> in the course menu."),
            p("After you finish the practice assignment and practice quiz, open " + link(f"{c}/grades", "Grades")
              + " to see them listed. They're marked as not counting toward your final grade."),
        )),
    ]


def syllabus_html(program):
    return page_shell(
        f"{program} Program", f"Intro to the {program} Program: Syllabus", "2026-27 Pilot",
        box("#00B7A3", heading("About This Course") + (
            f'<p style="margin:0;">This course is your starting point for the {program} program. It introduces '
            "the program, your instructors, and your class schedule, and walks you through the Canvas tools you "
            "will use every day in your program classes.</p>"))
        + box("#B5E3F0", heading("Your Instructors") + INSTRUCTORS_HTML)
        + box("#00B7A3", heading("Cohort Schedules") + COHORT_SCHEDULES_HTML.format(display_name=program))
        + box("#B5E3F0", heading("What We Expect From You") + (
            '<ul style="margin:0;padding-left:20px;">'
            "<li>Log in to Canvas every day you have class, and check Modules for what's next.</li>"
            "<li>Complete the <strong>Getting to Know Canvas</strong> module during your first week.</li>"
            "<li>Turn in work by its due date. Check Grades for feedback.</li>"
            "<li>Ask for help early. Your instructors are in the room and on Canvas.</li></ul>"))
    )


# ---------------------------------------------------------------------------
# Quick Guide PDF
# ---------------------------------------------------------------------------

def build_quick_guide_pdf():
    rows = [
        ("Home", "The course front page: start here."),
        ("Modules", "Your coursework in order, top to bottom."),
        ("Syllabus", "Instructors, schedule, expectations, and due dates."),
        ("Pages", "Readings and instructions to read (not turned in)."),
        ("Assignments", "Work you submit for a grade."),
        ("Discussions", "Online class conversations: post and reply."),
        ("Quizzes", "Questions answered in Canvas, often auto-scored."),
        ("Files", "Handouts and documents to view or download."),
        ("Grades", "Your scores and your instructor's feedback."),
        ("Rubrics", "Scoring guides, shown inside each assignment."),
    ]
    pdf = FPDF(orientation="P", unit="mm", format="Letter")
    pdf.set_margins(18, 18, 18)
    pdf.add_page()
    pdf.set_fill_color(0, 52, 98)
    pdf.rect(0, 0, 216, 34, "F")
    pdf.set_xy(18, 9)
    pdf.set_text_color(255, 207, 1)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 5, "VACE BUSINESS PROGRAMS", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 12, "Canvas Quick Guide", new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(44)
    pdf.set_text_color(31, 41, 55)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, "Every item in your course menu and what it's for. Keep this handy "
                         "during your first weeks in the program.")
    pdf.ln(4)
    for label, desc in rows:
        pdf.set_draw_color(229, 231, 235)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(0, 52, 98)
        pdf.cell(40, 11, label, border="B")
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(31, 41, 55)
        pdf.cell(0, 11, desc, border="B", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_fill_color(0, 183, 163)
    pdf.rect(18, pdf.get_y(), 2, 16, "F")
    pdf.set_x(24)
    pdf.set_font("Helvetica", "B", 11)
    pdf.multi_cell(0, 8, "Tip: When in doubt, click Modules and work from top to bottom.\n"
                         "Need help? Ask your instructor. We're in the room and on Canvas.")
    os.makedirs(os.path.dirname(QUICK_GUIDE_PDF), exist_ok=True)
    pdf.output(QUICK_GUIDE_PDF)


def upload_file(cid, local_path, name):
    if DRY_RUN:
        print(f"    [DRY RUN] upload {name}")
        return {"id": 0}
    pre = requests.post(f"{BASE_URL}/courses/{cid}/files", headers=HEADERS,
                        data={"name": name, "size": os.path.getsize(local_path),
                              "parent_folder_path": "course files", "on_duplicate": "overwrite"})
    pre.raise_for_status()
    pre = pre.json()
    with open(local_path, "rb") as f:
        up = requests.post(pre["upload_url"], data=pre["upload_params"], files={"file": (name, f)},
                           allow_redirects=False)
    if up.status_code in (301, 302, 303):
        up = requests.get(up.headers["Location"], headers=HEADERS)
    up.raise_for_status()
    return up.json()


# ---------------------------------------------------------------------------
# Build steps
# ---------------------------------------------------------------------------

def remove_old_module(cid):
    mod = find(get_all(f"/courses/{cid}/modules"), "name", OLD_MODULE)
    if not mod:
        print(f"  '{OLD_MODULE}' module already gone")
        return
    items = get_all(f"/courses/{cid}/modules/{mod['id']}/items")
    for it in items:
        if it["type"] == "Assignment":
            print(f"  - delete assignment: {it['title']}")
            send("DELETE", f"/courses/{cid}/assignments/{it['content_id']}")
    print(f"  - delete module: {OLD_MODULE}")
    send("DELETE", f"/courses/{cid}/modules/{mod['id']}")


def ensure_assignment(cid, program):
    existing = find(get_all(f"/courses/{cid}/assignments"), "name", PRACTICE_ASSIGNMENT)
    if existing:
        return existing
    print(f"  + assignment: {PRACTICE_ASSIGNMENT}")
    desc = page_shell(
        "Practice — Not Graded Toward Your Final Grade", PRACTICE_ASSIGNMENT, "Try submitting in Canvas",
        box("#00B7A3", heading("Instructions") + (
            '<p style="margin:0 0 10px;">Click <strong>Start Assignment</strong> and type a short introduction '
            "(3–5 sentences) that answers:</p>"
            '<ul style="margin:0;padding-left:20px;">'
            f"<li>Why did you join the {program} program?</li>"
            "<li>What kind of job are you working toward?</li>"
            "<li>One thing you'd like your instructors to know about you.</li></ul>"
            '<p style="margin:10px 0 0;">Then click <strong>Submit Assignment</strong>. Check the rubric below to '
            "see how it will be scored.</p>")))
    return send("POST", f"/courses/{cid}/assignments", {"assignment": {
        "name": PRACTICE_ASSIGNMENT, "description": desc, "submission_types": ["online_text_entry"],
        "points_possible": 10, "grading_type": "points", "omit_from_final_grade": True, "published": True}})


def ensure_rubric(cid, assignment_id):
    if find(get_all(f"/courses/{cid}/rubrics"), "title", PRACTICE_RUBRIC):
        return
    print(f"  + rubric: {PRACTICE_RUBRIC}")
    criteria = [
        ("Complete: answers all three questions", 4, [("All three answered", 4), ("Two answered", 2), ("One or none", 0)]),
        ("Clear: written in full sentences", 3, [("Clear and complete sentences", 3), ("Mostly clear", 2), ("Hard to follow", 0)]),
        ("Submitted in Canvas", 3, [("Submitted", 3), ("Not submitted", 0)]),
    ]
    send("POST", f"/courses/{cid}/rubrics", {
        "rubric": {"title": PRACTICE_RUBRIC, "free_form_criterion_comments": False, "criteria": {
            str(i): {"description": d, "points": pts,
                     "ratings": {str(j): {"description": rd, "points": rp} for j, (rd, rp) in enumerate(rs)}}
            for i, (d, pts, rs) in enumerate(criteria)}},
        "rubric_association": {"association_id": assignment_id, "association_type": "Assignment",
                               "use_for_grading": True, "purpose": "grading"}})


def ensure_discussion(cid, program):
    existing = find(get_all(f"/courses/{cid}/discussion_topics"), "title", PRACTICE_DISCUSSION)
    if existing:
        return existing
    print(f"  + discussion: {PRACTICE_DISCUSSION}")
    msg = page_shell(
        "Practice Discussion", PRACTICE_DISCUSSION, f"Meet your {program} cohort",
        box("#00B7A3", heading("Instructions") + (
            '<ul style="margin:0;padding-left:20px;">'
            "<li>Click <strong>Reply</strong> and share your first name and one thing you're looking forward to "
            "in the program.</li>"
            "<li>Then reply to at least one classmate's post.</li></ul>")))
    return send("POST", f"/courses/{cid}/discussion_topics",
                {"title": PRACTICE_DISCUSSION, "message": msg, "discussion_type": "threaded", "published": True})


def ensure_quiz(cid):
    existing = find(get_all(f"/courses/{cid}/quizzes"), "title", PRACTICE_QUIZ)
    if existing:
        return existing
    print(f"  + quiz: {PRACTICE_QUIZ}")
    quiz = send("POST", f"/courses/{cid}/quizzes", {"quiz": {
        "title": PRACTICE_QUIZ, "quiz_type": "assignment", "allowed_attempts": -1,
        "scoring_policy": "keep_highest", "show_correct_answers": True, "published": False,
        "description": "<p>Three quick questions about the Canvas menu. Take it as many times as you like; "
                       "it won't count toward your final grade.</p>"}})
    questions = [
        ("Where do you find your coursework in the order you should complete it?",
         [("Modules", 100), ("Files", 0), ("People", 0), ("Settings", 0)]),
        ("Where can you see your scores and your instructor's feedback?",
         [("Grades", 100), ("Pages", 0), ("Syllabus", 0), ("Discussions", 0)]),
        ("A rubric tells you...",
         [("How your assignment will be scored", 100), ("Your class schedule", 0),
          ("Where to download handouts", 0), ("Who is in your class", 0)]),
    ]
    for text, answers in questions:
        send("POST", f"/courses/{cid}/quizzes/{quiz['id']}/questions", {"question": {
            "question_type": "multiple_choice_question", "question_text": f"<p>{text}</p>",
            "points_possible": 1,
            "answers": [{"answer_text": a, "answer_weight": w} for a, w in answers]}})
    quiz = send("PUT", f"/courses/{cid}/quizzes/{quiz['id']}", {"quiz": {"published": True}})
    send("PUT", f"/courses/{cid}/assignments/{quiz['assignment_id']}",
         {"assignment": {"omit_from_final_grade": True}})
    return quiz


def ensure_file(cid):
    existing = find(get_all(f"/courses/{cid}/files"), "display_name", QUICK_GUIDE_NAME)
    if existing:
        return existing
    print(f"  + file: {QUICK_GUIDE_NAME}")
    return upload_file(cid, QUICK_GUIDE_PDF, QUICK_GUIDE_NAME)


def ensure_page(cid, title, body):
    existing = find(get_all(f"/courses/{cid}/pages"), "title", title)
    if existing:
        print(f"  ~ update page: {title}")
        return send("PUT", f"/courses/{cid}/pages/{existing['url']}", {"wiki_page": {"body": body, "published": True}})
    print(f"  + page: {title}")
    return send("POST", f"/courses/{cid}/pages", {"wiki_page": {"title": title, "body": body, "published": True}})


def build_tour_module(cid, program):
    a = ensure_assignment(cid, program)
    ensure_rubric(cid, a["id"])
    d = ensure_discussion(cid, program)
    q = ensure_quiz(cid)
    f = ensure_file(cid)
    ids = {"assignment": a["id"], "discussion": d["id"], "quiz": q["id"], "file": f["id"]}

    pages = {title: ensure_page(cid, title, body) for title, body in build_pages(cid, program, ids)}

    modules = get_all(f"/courses/{cid}/modules")
    mod = find(modules, "name", TOUR_MODULE)
    if not mod:
        print(f"  + module: {TOUR_MODULE}")
        mod = send("POST", f"/courses/{cid}/modules", {"module": {"name": TOUR_MODULE, "position": 2}})
    have = {i["title"] for i in get_all(f"/courses/{cid}/modules/{mod['id']}/items")} if not DRY_RUN else set()

    order = [
        ("Page", "What are Modules?"), ("Page", "What is the Syllabus?"), ("Page", "What are Pages?"),
        ("Page", "What are Assignments?"), ("Assignment", PRACTICE_ASSIGNMENT),
        ("Page", "What is a Rubric?"),
        ("Page", "What are Discussions?"), ("Discussion", PRACTICE_DISCUSSION),
        ("Page", "What are Quizzes?"), ("Quiz", PRACTICE_QUIZ),
        ("Page", "What are Files?"), ("File", QUICK_GUIDE_NAME),
        ("Page", "What are Grades?"),
    ]
    content_ids = {"Assignment": a["id"], "Discussion": d["id"], "Quiz": q["id"], "File": f["id"]}
    for pos, (kind, title) in enumerate(order, start=1):
        if title in have:
            continue
        item = {"type": kind, "title": title, "position": pos, "published": True}
        if kind == "Page":
            item["page_url"] = pages[title]["url"]
        else:
            item["content_id"] = content_ids[kind]
        send("POST", f"/courses/{cid}/modules/{mod['id']}/items", {"module_item": item})
    send("PUT", f"/courses/{cid}/modules/{mod['id']}", {"module": {"published": True, "position": 2}})
    return mod


def add_home_page_cta(cid, tour_module):
    """Appends a 'Getting to Know Canvas' box with a Start button to the bottom
    of the course front page. The button opens the module's first item (via
    /modules/items/:id) so Canvas's Next buttons walk students through the tour."""
    if DRY_RUN:
        print("    [DRY RUN] PUT front page with Getting to Know Canvas button")
        return
    front = requests.get(f"{BASE_URL}/courses/{cid}/front_page", headers=HEADERS).json()
    body = front["body"] or ""
    if CTA_ID in body:
        print("  home page button already present")
        return
    first = get_all(f"/courses/{cid}/modules/{tour_module['id']}/items")[0]
    cta = (
        f'<div id="{CTA_ID}">'
        + box("#FFCF01", heading(TOUR_MODULE) + (
            '<p style="margin:0 0 10px;">New to Canvas? Start here. This short tour walks you through every item '
            "in the course menu (Modules, Syllabus, Pages, Assignments, Discussions, Quizzes, Files, Grades, and "
            "Rubrics) with a simple explanation of each and a practice activity you can try. Nothing in the tour "
            "counts toward your grade.</p>"
            '<p style="margin:14px 0 0;">'
            f'<a href="/courses/{cid}/modules/items/{first["id"]}" style="display:inline-block;background:#003462;'
            'color:#FFFFFF;font-weight:bold;text-decoration:none;padding:10px 22px;border-radius:4px;">'
            "Start Getting to Know Canvas &rarr;</a></p>"))
        + "</div>"
    )
    # Insert inside the page's outer wrapper div (before its closing tag) so the box keeps the same width.
    idx = body.rfind("</div>")
    body = body[:idx] + cta + body[idx:] if idx != -1 else body + cta
    print("  ~ home page: add Getting to Know Canvas button")
    send("PUT", f"/courses/{cid}/pages/{front['url']}", {"wiki_page": {"body": body}})


def publish_overview(cid):
    mod = find(get_all(f"/courses/{cid}/modules"), "name", OVERVIEW_MODULE)
    if mod and not mod["published"]:
        print(f"  ~ publish module: {OVERVIEW_MODULE}")
        send("PUT", f"/courses/{cid}/modules/{mod['id']}", {"module": {"published": True, "position": 1}})


def set_syllabus(cid, program):
    print("  ~ syllabus body")
    send("PUT", f"/courses/{cid}", {"course": {"syllabus_body": syllabus_html(program)}})


def set_tabs(cid):
    tabs = get_all(f"/courses/{cid}/tabs")
    for pos, tab_id in enumerate(VISIBLE_TABS, start=1):
        if tab_id == "home":
            continue
        send("PUT", f"/courses/{cid}/tabs/{tab_id}", {"hidden": False, "position": pos})
    for t in tabs:
        if t["id"] not in VISIBLE_TABS and t["id"] not in NEVER_HIDE and not t.get("hidden"):
            print(f"  - hide tab: {t['label']}")
            send("PUT", f"/courses/{cid}/tabs/{t['id']}", {"hidden": True})


def build_one(cid):
    program = PROGRAM_NAMES[cid]
    print(f"\n=== {cid}: Intro to the {program} Program ===")
    remove_old_module(cid)
    publish_overview(cid)
    tour = build_tour_module(cid, program)
    add_home_page_cta(cid, tour)
    set_syllabus(cid, program)
    set_tabs(cid)


def main():
    global DRY_RUN
    ap = argparse.ArgumentParser()
    ap.add_argument("course_ids", nargs="+", type=int, choices=sorted(PROGRAM_NAMES))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    DRY_RUN = args.dry_run
    build_quick_guide_pdf()
    for cid in args.course_ids:
        build_one(cid)


if __name__ == "__main__":
    main()
