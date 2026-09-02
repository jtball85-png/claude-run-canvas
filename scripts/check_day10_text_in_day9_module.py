# -*- coding: utf-8 -*-
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from push_course import api_get

COURSE_ID = 456
items = api_get(f"/courses/{COURSE_ID}/modules/2099/items")
items.sort(key=lambda x: x["position"])
items = items[10:]  # the original Day 10 items, now positions 11-26

for it in items:
    title = it["title"]
    body = ""
    if it["type"] == "Page":
        p = api_get(f"/courses/{COURSE_ID}/pages/{it['page_url']}")
        body = p.get("body", "")
    elif it["type"] == "Assignment":
        a = api_get(f"/courses/{COURSE_ID}/assignments/{it['content_id']}")
        body = a.get("description", "") or ""
    elif it["type"] == "Quiz":
        q = api_get(f"/courses/{COURSE_ID}/quizzes/{it['content_id']}")
        body = q.get("description", "") or ""
    hits = re.findall(r".{20}Day 10.{20}", body)
    title_hit = "Day 10" in title
    print(f"--- {title} (title has 'Day 10': {title_hit}) ---")
    for h in hits:
        print("   ", repr(h))
