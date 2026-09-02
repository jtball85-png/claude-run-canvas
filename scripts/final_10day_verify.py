# -*- coding: utf-8 -*-
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from push_course import api_get

COURSE_ID = 456

print("=== Final module list ===")
mods = api_get(f"/courses/{COURSE_ID}/modules")
mods.sort(key=lambda m: m["position"])
for m in mods:
    print(m["position"], m["id"], m["name"])
print(f"({len(mods)} modules)\n")

all_titles = []
for m in mods:
    items = api_get(f"/courses/{COURSE_ID}/modules/{m['id']}/items")
    for it in items:
        all_titles.append((it["title"], m["name"], it["type"]))

from collections import Counter
title_counts = Counter(t for t, _, _ in all_titles)
dupes = {t: c for t, c in title_counts.items() if c > 1}
print("=== Duplicate item titles across the whole course ===")
print(dupes if dupes else "none")

print("\n=== Any remaining 'Day 11' anywhere in module 2099 or 2101 item titles ===")
for m in mods:
    if m["id"] not in (2099, 2101):
        continue
    items = api_get(f"/courses/{COURSE_ID}/modules/{m['id']}/items")
    for it in items:
        if "Day 11" in it["title"]:
            print(f"  FOUND: {it['title']} in module {m['name']}")
print("(none printed above = clean)")

print("\n=== Course Overview page's Course Map (Day 8-10 rows) ===")
page = api_get(f"/courses/{COURSE_ID}/pages/business-math-welcome")
body = page["body"]
idx = body.find(">Ratios, Proportions")
print(body[idx-50:idx+900])
