# -*- coding: utf-8 -*-
"""Read-only inspection of course 456's Day 9/10/11 modules and Course
Overview page before restructuring to 10 real teaching days."""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from push_course import api_get

COURSE_ID = 456

for mid, label in [(2099, "Day 9"), (2100, "Day 10"), (2101, "Day 11")]:
    items = api_get(f"/courses/{COURSE_ID}/modules/{mid}/items")
    print(f"=== Module {mid} ({label}), {len(items)} items ===")
    for it in items:
        print(json.dumps({
            "position": it.get("position"),
            "title": it.get("title"),
            "type": it.get("type"),
            "content_id": it.get("content_id"),
            "page_url": it.get("page_url"),
        }))
    print()

mods = api_get(f"/courses/{COURSE_ID}/modules")
for m in sorted(mods, key=lambda x: x.get("position", 0)):
    print(m["position"], m["id"], m["name"])

pages = api_get(f"/courses/{COURSE_ID}/pages", params={"search_term": "Business Math"})
overview_pages = [p for p in api_get(f"/courses/{COURSE_ID}/pages") if "Welcome" in p.get("title", "")]
print("\nOverview page(s):")
for p in overview_pages:
    print(p["url"], "|", p["title"])
