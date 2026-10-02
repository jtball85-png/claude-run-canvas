"""
go_live_course.py
-----------------
Takes a built course live for students, the same way the Intro courses
(467/451/468) were set up:

  1. Trims the course menu to Home, Modules, Syllabus, Pages, Assignments,
     Discussions, Quizzes, Files, Grades, Rubrics -- every other tab hidden.
  2. Publishes every module and every item inside it (publishing a module
     item publishes its page/assignment/quiz/file too).
  3. Publishes the course itself if it is still unpublished.

Optional per course:
  --syllabus       build the Syllabus from the front page's At A Glance /
                   Instructor / Description / Cohort Schedules / Course Map
                   boxes, plus a How You're Graded table and expectations
  --hide-tabs      hide extra menu items (e.g. discussions when there are none)
  --hide-folders   hide image folders from the Files browser (embeds still work)

Prints a summary of anything left unpublished afterward.

Usage (run from repo root so .env loads):
  python scripts/go_live_course.py --dry-run 452
  python scripts/go_live_course.py 452 --syllabus --hide-tabs discussions \
      --hide-folders textbook-images,solution-screenshots,images
"""

import argparse
import os
import re
import sys
from collections import Counter

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_intro_canvas_tour import VISIBLE_TABS, NEVER_HIDE, get_all  # noqa: E402
from create_program_overview_course import BASE_URL, HEADERS, box, heading  # noqa: E402

DRY_RUN = False


def send(method, endpoint, payload=None):
    if DRY_RUN:
        print(f"    [DRY RUN] {method} {endpoint} {payload or ''}")
        return {}
    r = requests.request(method, f"{BASE_URL}{endpoint}", headers=HEADERS, json=payload)
    if r.status_code >= 400:
        print(f"    ERROR {r.status_code} {method} {endpoint}: {r.text[:200]}")
        return None
    return r.json() if r.text else {}


def set_tabs(cid, extra_hidden=()):
    visible = [t for t in VISIBLE_TABS if t not in extra_hidden]
    tabs = get_all(f"/courses/{cid}/tabs")
    for pos, tab_id in enumerate(visible, start=1):
        if tab_id != "home":
            send("PUT", f"/courses/{cid}/tabs/{tab_id}", {"hidden": False, "position": pos})
    hidden = []
    for t in tabs:
        if t["id"] not in visible and t["id"] not in NEVER_HIDE and not t.get("hidden"):
            send("PUT", f"/courses/{cid}/tabs/{t['id']}", {"hidden": True})
            hidden.append(t["label"])
    print(f"  menu: hid {', '.join(hidden) or 'nothing'}")


def publish_modules(cid):
    mods = get_all(f"/courses/{cid}/modules")
    items_published = 0
    for m in mods:
        for item in get_all(f"/courses/{cid}/modules/{m['id']}/items"):
            if item.get("published") is False:
                if send("PUT", f"/courses/{cid}/modules/{m['id']}/items/{item['id']}",
                        {"module_item": {"published": True}}) is not None:
                    items_published += 1
        if not m["published"]:
            send("PUT", f"/courses/{cid}/modules/{m['id']}", {"module": {"published": True}})
            print(f"  published module: {m['name']}")
    print(f"  published {items_published} module items")


def hide_folders(cid, names):
    """Hides folders (e.g. textbook/solution images) from the Files browser.
    Hidden files stay viewable by direct link, so images embedded in pages
    and assignments keep displaying for students."""
    for f in get_all(f"/courses/{cid}/folders"):
        short = f["full_name"].rsplit("/", 1)[-1]
        if short in names and not f.get("hidden"):
            send("PUT", f"/folders/{f['id']}", {"hidden": True})
            print(f"  hid folder from Files: {f['full_name']} ({f['files_count']} files)")


SYLLABUS_BOXES = ["Course At A Glance", "Your Instructor", "Course Description", "Cohort Schedules", "Course Map"]


def front_page_boxes(body):
    """Splits a front page built with create_program_overview_course.box() into
    {h2 heading: box html}. Boxes are siblings, so each one runs from its own
    border-left div to the next one (the last also carries the page wrapper's
    closing </div>, which is trimmed)."""
    starts = [m.start() for m in re.finditer(r'<div style="border-left:5px solid', body)]
    boxes = {}
    for i, s in enumerate(starts):
        chunk = body[s:starts[i + 1]] if i + 1 < len(starts) else body[s:body.rfind("</div>")]
        h = re.search(r"<h2[^>]*>(.*?)</h2>", chunk)
        if h:
            boxes[h.group(1)] = chunk
    return boxes


def grading_box(cid):
    assignments = get_all(f"/courses/{cid}/assignments")
    kinds = Counter()
    for a in assignments:
        # Drop the numbering so items group by type: "Hands-On 1.4-1.6: ..." -> "Hands-On",
        # "Hands-On OU2-D7–D9: ..." -> "Hands-On", "Chapter 1 Quiz (eLab)" -> "Quiz (eLab)",
        # "Skill Builders 2.1-2.3" -> "Skill Builder".
        label = a["name"].split(":")[0]
        label = re.sub(r"\S*\d\S*|\bChapters?\b|\bDay\b|&|[–—]", " ", label)
        label = re.sub(r"(Builder)s\b", r"\1", " ".join(label.split()))
        if "(Self-Paced Practice)" in label:
            label = "Self-Paced Practice Review"
        elif a.get("is_quiz_assignment") and not re.search(r"quiz|test|assessment", label, re.I):
            label = "Quiz"  # one-off quiz titles like "Desktop Features Check"
        kinds[label or a["name"]] += 1
    total = sum(a.get("points_possible") or 0 for a in assignments)
    rows = "".join(
        f'<tr><td style="border-bottom:1px solid #E5E7EB;padding:8px 10px;">{k}</td>'
        f'<td style="border-bottom:1px solid #E5E7EB;padding:8px 10px;">{n}</td></tr>'
        for k, n in kinds.most_common())
    return box("#00B7A3", heading("How You're Graded") + (
        f'<p style="margin:0 0 10px;">Your grade is based on total points: every graded item adds to one running '
        f"total ({total:g} points in all). Check <strong>Grades</strong> any time to see your scores and "
        "your instructor's feedback.</p>"
        '<table style="width:100%;border-collapse:collapse;background:white;"><tbody>'
        '<tr><th style="text-align:left;color:#003462;border-bottom:2px solid #00B7A3;padding:8px 10px;">Type of graded work</th>'
        '<th style="text-align:left;color:#003462;border-bottom:2px solid #00B7A3;padding:8px 10px;">Number of items</th></tr>'
        + rows + "</tbody></table>"))


EXPECTATIONS_BOX = box("#B5E3F0", heading("What We Expect From You") + (
    '<ul style="margin:0;padding-left:20px;">'
    "<li>Log in to Canvas every day you have class, and work through <strong>Modules</strong> from top to bottom.</li>"
    "<li>Complete each day's readings, Hands-On exercises, and Skill Builders before moving on.</li>"
    "<li>Compare your work to the <strong>Example of a Completed Submission</strong> before you submit.</li>"
    "<li>Let your instructor know ahead of time about any days you can't attend.</li>"
    "<li>Ask for help early. Your instructor is in the room and on Canvas.</li></ul>"))


def set_syllabus(cid, course_name):
    front = requests.get(f"{BASE_URL}/courses/{cid}/front_page", headers=HEADERS).json()
    boxes = front_page_boxes(front.get("body") or "")
    missing = [h for h in SYLLABUS_BOXES if h not in boxes]
    if missing:
        print(f"  syllabus SKIPPED: front page missing {missing}")
        return
    title = course_name.rsplit(" ", 1)[0] if re.search(r"\d+/\d+$", course_name) else course_name
    body = (
        '<div style="font-family:Arial,Helvetica,sans-serif;line-height:1.55;color:#1F2937;max-width:920px;margin:0 auto;">'
        '<div style="background:#003462;color:white;border-radius:4px;padding:20px 24px;margin:0 0 16px;">'
        '<div style="font-size:12px;color:#FFCF01;">Course Syllabus — 2026-27</div>'
        f'<h1 style="margin:4px 0 4px;font-size:28px;line-height:1.15;color:white;">{title}</h1>'
        '<div style="font-size:17px;line-height:1.35;color:#B5E3F0;">Who, when, what, and how you\'re graded</div>'
        "</div>"
        + "".join(boxes[h] for h in SYLLABUS_BOXES)
        + grading_box(cid) + EXPECTATIONS_BOX + "</div>"
    )
    send("PUT", f"/courses/{cid}", {"course": {"syllabus_body": body}})
    print("  syllabus written")


def publish_course(cid):
    c = requests.get(f"{BASE_URL}/courses/{cid}", headers=HEADERS).json()
    if c["workflow_state"] != "available":
        send("PUT", f"/courses/{cid}", {"offer": True})
        print("  published course")


def report(cid):
    mods = get_all(f"/courses/{cid}/modules")
    left = [(m["name"], i["type"], i["title"]) for m in mods
            for i in get_all(f"/courses/{cid}/modules/{m['id']}/items") if i.get("published") is False]
    left += [(m["name"], "Module", "") for m in mods if not m["published"]]
    visible = [t["label"] for t in get_all(f"/courses/{cid}/tabs") if not t.get("hidden")]
    print(f"  visible menu: {', '.join(visible)}")
    print(f"  modules: {len(mods)}, still unpublished: {len(left)}")
    for x in left:
        print("    -", x)


def main():
    global DRY_RUN
    ap = argparse.ArgumentParser()
    ap.add_argument("course_ids", nargs="+", type=int)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--hide-tabs", default="", help="extra tab ids to hide, e.g. discussions")
    ap.add_argument("--hide-folders", default="", help="folder names to hide from Files, e.g. textbook-images,images")
    ap.add_argument("--syllabus", action="store_true", help="build syllabus from the front page boxes")
    args = ap.parse_args()
    DRY_RUN = args.dry_run
    split = lambda s: {x.strip() for x in s.split(",") if x.strip()}
    for cid in args.course_ids:
        name = requests.get(f"{BASE_URL}/courses/{cid}", headers=HEADERS).json()["name"]
        print(f"\n=== {cid}: {name} ===")
        set_tabs(cid, split(args.hide_tabs))
        if args.hide_folders:
            hide_folders(cid, split(args.hide_folders))
        publish_modules(cid)
        publish_course(cid)
        # after publishing: unpublished quizzes report 0 points, which would skew the grading total
        if args.syllabus:
            set_syllabus(cid, name)
        if not DRY_RUN:
            report(cid)


if __name__ == "__main__":
    main()
