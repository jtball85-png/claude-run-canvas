# -*- coding: utf-8 -*-
"""Fixes leftover "Day 11" banner text/titles inside the module that was
just renamed from "Day 11" to "Day 10" (module 2101), so the visible
content matches its new module label."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from push_course import api_get, api_put

COURSE_ID = 456
MODULE_ID = 2101

items = api_get(f"/courses/{COURSE_ID}/modules/{MODULE_ID}/items")
items.sort(key=lambda x: x["position"])

TITLE_RENAMES = {
    "Day 11 Overview": "Day 10 Overview",
    "Day 11: Want More Practice?": "Day 10: Want More Practice?",
}

for it in items:
    changed = False
    new_title = TITLE_RENAMES.get(it["title"], it["title"])

    if it["type"] == "Page":
        p = api_get(f"/courses/{COURSE_ID}/pages/{it['page_url']}")
        body = p.get("body", "")
        new_body = body.replace("Day 11", "Day 10")
        if new_body != body or new_title != it["title"]:
            api_put(f"/courses/{COURSE_ID}/pages/{it['page_url']}",
                    {"wiki_page": {"title": new_title, "body": new_body}})
            changed = True
    elif it["type"] == "Assignment":
        a = api_get(f"/courses/{COURSE_ID}/assignments/{it['content_id']}")
        desc = a.get("description", "") or ""
        new_desc = desc.replace("Day 11", "Day 10")
        if new_desc != desc:
            api_put(f"/courses/{COURSE_ID}/assignments/{it['content_id']}",
                    {"assignment": {"description": new_desc}})
            changed = True
    elif it["type"] == "Quiz":
        q = api_get(f"/courses/{COURSE_ID}/quizzes/{it['content_id']}")
        desc = q.get("description", "") or ""
        new_desc = desc.replace("Day 11", "Day 10")
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
