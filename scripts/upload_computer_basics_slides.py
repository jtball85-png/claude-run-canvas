"""
upload_computer_basics_slides.py
--------------------------------
Uploads the Computer Basics daily slide decks (Day 01-09) into a student-visible
"Daily Lessons" folder in a course's Files so students can follow along in class.

The decks are uploaded exactly as they are in the hub project, including the
embedded interactive quizzes -- students take every quiz and test in the deck
as practice (with instant feedback) before the graded Canvas version (Josh,
2026-10-06: a "take it in Canvas" placeholder confused students). The source
files are never modified.

Re-running overwrites the existing copies in the folder (Canvas on_duplicate=overwrite).
Every upload ends with the same report --check prints.

--check changes nothing. It reports:
  1. Slides: is each Canvas copy byte-identical to the current deck? (OUT OF DATE = deck edited since the last upload.)
  2. Quizzes: does each deck's practice quiz match the real graded Canvas quiz
     of the same title (question count, points, question text, answer choices,
     correct answers)? Decks and Canvas quizzes are maintained separately, so
     an edit to one never changes the other.

Usage:
  python scripts/upload_computer_basics_slides.py --course 452
  python scripts/upload_computer_basics_slides.py --course 452 --dry-run
  python scripts/upload_computer_basics_slides.py --course 452 --check
"""

import os
import re
import sys
import glob
import html
import json
import argparse
import tempfile

import requests

sys.path.insert(0, os.path.dirname(__file__))
from push_course import BASE_URL, HEADERS, api_get  # noqa: E402

SOURCE_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "Master Business Finance Program",
    "Lesson Planning", "Computer Basics", "Daily Lesson Plans",
)
FOLDER = "Daily Lessons"

QUIZ_RUN = re.compile(
    r"(?:<div class='quiz-question' id='qq-\d+'><script type='application/json' "
    r"class='quiz-data'>.*?</script></div>\s*)+",
    re.S,
)
# A quiz slide: <h2>Title</h2><div class='body'><p>3 questions &middot; 3 pts</p> + question run
QUIZ_SLIDE = re.compile(
    r"<h2>([^<]*)</h2><div class='body'><p>(\d+) questions &middot; ([\d.]+) pts</p>("
    + QUIZ_RUN.pattern + ")",
    re.S,
)


def display_name(path):
    # "Day 01 - Chapter 1 Logging In ... - Slides.html" -> "Day 01 - Chapter 1 Logging In ....html"
    return os.path.basename(path).replace(" - Slides.html", ".html")


def find_decks():
    decks = sorted(glob.glob(os.path.join(SOURCE_DIR, "Day * - Slides.html")))
    if not decks:
        sys.exit(f"No decks found in {os.path.abspath(SOURCE_DIR)}")
    return decks


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def find_folder(course_id):
    for f in api_get(f"/courses/{course_id}/folders"):
        if f["full_name"] == f"course files/{FOLDER}":
            return f
    return None


def ensure_folder(course_id, dry_run):
    f = find_folder(course_id)
    if f:
        if f.get("hidden") or f.get("locked") or f.get("hidden_for_user"):
            print(f"  folder '{FOLDER}' exists but is hidden/locked -- making it visible")
            if not dry_run:
                requests.put(f"{BASE_URL}/folders/{f['id']}", headers=HEADERS,
                             data={"hidden": "false", "locked": "false"}).raise_for_status()
        return f["id"]
    print(f"  creating folder '{FOLDER}'")
    if dry_run:
        return None
    r = requests.post(f"{BASE_URL}/courses/{course_id}/folders", headers=HEADERS,
                      data={"name": FOLDER, "parent_folder_path": "/"})
    r.raise_for_status()
    return r.json()["id"]


def upload(course_id, name, content):
    data = content.encode("utf-8")
    pre = requests.post(f"{BASE_URL}/courses/{course_id}/files", headers=HEADERS, data={
        "name": name, "size": len(data), "content_type": "text/html",
        "parent_folder_path": FOLDER, "on_duplicate": "overwrite",
    })
    pre.raise_for_status()
    pre = pre.json()
    with tempfile.TemporaryFile() as tmp:
        tmp.write(data)
        tmp.seek(0)
        up = requests.post(pre["upload_url"], data=pre["upload_params"],
                           files={"file": (name, tmp, "text/html")}, allow_redirects=False)
    if up.status_code in (301, 302, 303):
        up = requests.get(up.headers["Location"], headers=HEADERS)
    up.raise_for_status()
    return up.json()


# ---------------------------------------------------------------------------
# --check
# ---------------------------------------------------------------------------

def check_slides(course_id, decks):
    """Compares each Canvas copy to the current deck. Returns problem count."""
    print("\nSLIDES in Files > Daily Lessons (Canvas copy vs. your current deck)")
    folder = find_folder(course_id)
    if not folder:
        print(f"  MISSING   folder '{FOLDER}' does not exist in course {course_id}")
        return len(decks)
    problems = 0
    if folder.get("hidden") or folder.get("locked"):
        print(f"  HIDDEN    folder '{FOLDER}' is hidden or locked -- students can't see it")
        problems += 1
    canvas = {f["display_name"]: f for f in api_get(f"/folders/{folder['id']}/files")}
    expected = set()
    for path in decks:
        name = display_name(path)
        expected.add(name)
        f = canvas.get(name)
        if not f:
            print(f"  MISSING   {name}")
            problems += 1
            continue
        want = read(path).encode("utf-8")
        got = requests.get(f["url"], headers=HEADERS).content
        if got != want:
            print(f"  OUT OF DATE  {name}  (deck changed since last upload -- re-run without --check)")
            problems += 1
        elif f.get("hidden") or f.get("locked"):
            print(f"  HIDDEN    {name}  (up to date, but students can't see it)")
            problems += 1
        else:
            print(f"  ok        {name}")
    for name in sorted(set(canvas) - expected):
        print(f"  EXTRA     {name}  (in Canvas, no matching deck -- renamed or removed?)")
        problems += 1
    return problems


def clean(text):
    text = re.sub(r"<[^>]+>", " ", html.unescape(str(text)))
    return re.sub(r"\s+", " ", text).strip()


def deck_question(q):
    """Normalizes a deck quiz-data question to (type, text, choices, correct)."""
    if q["type"] == "short_answer_question":
        accepted = frozenset(clean(a) for a in q["accepted"])
        return q["type"], clean(q["text"]), accepted, accepted
    choices = tuple(clean(a["text"]) for a in q["answers"])
    correct = frozenset(clean(a["text"]) for a in q["answers"] if a["correct"])
    return q["type"], clean(q["text"]), choices, correct


def canvas_question(q):
    """Normalizes a Canvas quiz question the same way as deck_question()."""
    if q["question_type"] == "short_answer_question":
        accepted = frozenset(clean(a["text"]) for a in q["answers"])
        return q["question_type"], clean(q["question_text"]), accepted, accepted
    choices = tuple(clean(a["text"]) for a in q["answers"])
    correct = frozenset(clean(a["text"]) for a in q["answers"] if float(a.get("weight") or 0) > 0)
    return q["question_type"], clean(q["question_text"]), choices, correct


def short(s, n=70):
    return s if len(s) <= n else s[:n - 3] + "..."


def check_quizzes(course_id, decks):
    """Compares each deck's practice quiz with the graded Canvas quiz of the same title."""
    print("\nQUIZZES (practice copy in your deck vs. the graded quiz in Canvas)")
    canvas = {q["title"].strip(): q for q in api_get(f"/courses/{course_id}/quizzes", {"per_page": 100})}
    problems = 0
    for path in decks:
        for m in QUIZ_SLIDE.finditer(read(path)):
            title, count, pts = html.unescape(m.group(1)).strip(), int(m.group(2)), float(m.group(3))
            mine = [deck_question(json.loads(x))
                    for x in re.findall(r"class='quiz-data'>(.*?)</script>", m.group(4), re.S)]
            quiz = canvas.get(title)
            if not quiz:
                print(f"  MISSING   {title}  (no Canvas quiz with this title)")
                problems += 1
                continue
            theirs = [canvas_question(q)
                      for q in api_get(f"/courses/{course_id}/quizzes/{quiz['id']}/questions", {"per_page": 100})]
            diffs = []
            if len(mine) != len(theirs):
                diffs.append(f"deck has {len(mine)} questions, Canvas has {len(theirs)}")
            if count != len(mine):
                diffs.append(f"deck slide says {count} questions but contains {len(mine)}")
            if pts != float(quiz["points_possible"] or 0):
                diffs.append(f"deck says {pts:g} pts, Canvas quiz is worth {quiz['points_possible']:g}")
            for i, (a, b) in enumerate(zip(mine, theirs), 1):
                if a[1] != b[1]:
                    diffs.append(f"Q{i} wording differs\n        deck:   {short(a[1])}\n        Canvas: {short(b[1])}")
                elif a[0] != b[0]:
                    diffs.append(f"Q{i} question type differs (deck {a[0]}, Canvas {b[0]})")
                elif a[3] != b[3]:
                    diffs.append(f"Q{i} correct answer differs  (deck: {', '.join(sorted(a[3]))} | "
                                 f"Canvas: {', '.join(sorted(b[3]))})")
                elif a[2] != b[2]:
                    diffs.append(f"Q{i} answer choices differ  ({short(a[1], 50)})")
            if diffs:
                problems += 1
                print(f"  DIFFERENT {title}")
                for d in diffs:
                    print(f"      - {d}")
            else:
                print(f"  ok        {title}  ({len(mine)} questions)")
    return problems


def check(course_id, decks):
    problems = check_slides(course_id, decks) + check_quizzes(course_id, decks)
    print("\n" + ("ALL GOOD -- students' copies match your decks, and every practice quiz "
                  "matches its graded Canvas quiz." if not problems else
                  f"{problems} item(s) need attention (see above)."))
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--course", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check", action="store_true", help="report only; change nothing")
    args = ap.parse_args()

    decks = find_decks()
    if args.check:
        sys.exit(1 if check(args.course, decks) else 0)

    ensure_folder(args.course, args.dry_run)
    for path in decks:
        content = read(path)
        n = len(QUIZ_SLIDE.findall(content))
        name = display_name(path)
        if args.dry_run:
            print(f"  [dry-run] {name} ({n} practice quizzes)")
            continue
        f = upload(args.course, name, content)
        print(f"  uploaded {name} ({n} practice quizzes) -> file {f['id']}")
    if not args.dry_run:
        check(args.course, decks)


if __name__ == "__main__":
    main()
