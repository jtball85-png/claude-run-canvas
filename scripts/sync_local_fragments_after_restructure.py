# -*- coding: utf-8 -*-
"""Pulls the live, post-restructure state of course 456's Course Overview
page and modules 2099 (merged Day 9) / 2101 (renamed Day 10) back down
into local JSON fragment files, so the repo exactly mirrors what's live
rather than risking drift from hand-reconstructing the HTML.

Writes:
  day9-module-fragment.json  <- module 2099 (merged Day 9+10 content)
  day10-module-fragment.json <- module 2101 (renamed former Day 11)
  course-overview-fragment.json <- live Course Overview page

Old day10-module-fragment.json and day11-module-fragment.json content is
superseded by this -- the calling context deletes/renames the actual repo
files afterward.
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from push_course import api_get

COURSE_ID = 456
FRAGMENT_DIR = r"C:\Users\jball.VACE\Documents\Claude Projects\Master Business Finance Program\Lesson Planning\Business Math"


def dump_module(module_id, out_filename):
    mod = next(m for m in api_get(f"/courses/{COURSE_ID}/modules") if m["id"] == module_id)
    items = api_get(f"/courses/{COURSE_ID}/modules/{module_id}/items")
    items.sort(key=lambda x: x["position"])

    frag_items = []
    for it in items:
        t = it["type"]
        if t == "Page":
            p = api_get(f"/courses/{COURSE_ID}/pages/{it['page_url']}")
            frag_items.append({"type": "page", "title": p["title"], "body": p["body"]})
        elif t == "Assignment":
            a = api_get(f"/courses/{COURSE_ID}/assignments/{it['content_id']}")
            frag_items.append({
                "type": "assignment", "title": a["name"], "description": a.get("description", "") or "",
                "points_possible": a.get("points_possible", 0),
                "submission_types": a.get("submission_types", []),
            })
        elif t == "Quiz":
            q = api_get(f"/courses/{COURSE_ID}/quizzes/{it['content_id']}")
            questions = api_get(f"/courses/{COURSE_ID}/quizzes/{it['content_id']}/questions")
            questions.sort(key=lambda x: x.get("position") or 0)
            q_items = []
            for qq in questions:
                q_items.append({
                    "question_type": qq["question_type"],
                    "question_text": qq["question_text"],
                    "points_possible": qq["points_possible"],
                    "answers": [{"text": a.get("text", ""), "weight": a.get("weight", 0)} for a in qq.get("answers", [])],
                })
            frag_items.append({
                "type": "quiz", "title": q["title"], "quiz_type": q["quiz_type"],
                "description": q.get("description", "") or "",
                "points_possible": q.get("points_possible", 0),
                "questions": q_items,
            })
        else:
            print(f"  WARNING: unhandled item type {t} for {it['title']} -- skipped")

    fragment = {"course_name": "Business Math 26/27", "modules": [
        {"name": mod["name"], "position": mod["position"], "items": frag_items}
    ]}
    out_path = os.path.join(FRAGMENT_DIR, out_filename)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(fragment, fh, indent=2, ensure_ascii=False)
    print(f"Wrote {out_path} ({len(frag_items)} items)")


def dump_overview():
    page = api_get(f"/courses/{COURSE_ID}/pages/business-math-welcome")
    fragment = {"name": "Course Overview", "position": 1, "items": [
        {"type": "page", "title": page["title"], "body": page["body"]}
    ]}
    out_path = os.path.join(FRAGMENT_DIR, "course-overview-fragment.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(fragment, fh, indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    dump_module(2099, "day9-module-fragment.json")
    dump_module(2101, "day10-module-fragment.json")
    dump_overview()
