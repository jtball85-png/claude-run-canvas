# -*- coding: utf-8 -*-
"""Fixes leftover "Day 10" banner text/titles inside module 2099 (merged
Day 9), which otherwise collides with the page titled "Day 10 Overview"
now legitimately living in module 2101 (the renamed former Day 11).
Relabels the original Day 10 sub-section as "Day 9, Part 2" throughout."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from push_course import api_get, api_put

COURSE_ID = 456
MODULE_ID = 2099

items = api_get(f"/courses/{COURSE_ID}/modules/{MODULE_ID}/items")
items.sort(key=lambda x: x["position"])
items = items[10:]  # original Day 10 items, now positions 11-26

TITLE_RENAMES = {
    "Day 10 Overview": "Day 9 Overview, Part 2",
    "Day 10: Want More Practice?": "Day 9: Want More Practice? (Part 2)",
}

for it in items:
    changed = False
    new_title = TITLE_RENAMES.get(it["title"], it["title"])

    if it["type"] == "Page":
        p = api_get(f"/courses/{COURSE_ID}/pages/{it['page_url']}")
        body = p.get("body", "")
        new_body = body.replace("Day 10", "Day 9, Part 2")
        if new_body != body or new_title != it["title"]:
            api_put(f"/courses/{COURSE_ID}/pages/{it['page_url']}",
                    {"wiki_page": {"title": new_title, "body": new_body}})
            changed = True
    elif it["type"] == "Assignment":
        a = api_get(f"/courses/{COURSE_ID}/assignments/{it['content_id']}")
        desc = a.get("description", "") or ""
        new_desc = desc.replace("Day 10", "Day 9, Part 2")
        if new_desc != desc:
            api_put(f"/courses/{COURSE_ID}/assignments/{it['content_id']}",
                    {"assignment": {"description": new_desc}})
            changed = True
    elif it["type"] == "Quiz":
        q = api_get(f"/courses/{COURSE_ID}/quizzes/{it['content_id']}")
        desc = q.get("description", "") or ""
        new_desc = desc.replace("Day 10", "Day 9, Part 2")
        if new_desc != desc:
            api_put(f"/courses/{COURSE_ID}/quizzes/{it['content_id']}",
                    {"quiz": {"description": new_desc}})
            changed = True

    if new_title != it["title"]:
        api_put(f"/courses/{COURSE_ID}/modules/{MODULE_ID}/items/{it['id']}",
                {"module_item": {"title": new_title}})
        changed = True

    print(f"  [{'FIXED' if changed else 'ok'}] {it['title']}" + (f" -> {new_title}" if new_title != it['title'] else ""))

print("\nDone.")
