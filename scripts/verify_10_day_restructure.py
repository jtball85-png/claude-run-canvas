# -*- coding: utf-8 -*-
"""Final verification of the 11->10 day restructure for course 456."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from push_course import api_get

COURSE_ID = 456

mods = api_get(f"/courses/{COURSE_ID}/modules")
mods.sort(key=lambda m: m["position"])
print(f"=== {len(mods)} modules total ===")
for m in mods:
    print(m["position"], m["id"], m["name"])

print("\n=== Module 2099 (merged Day 9) item order ===")
items = api_get(f"/courses/{COURSE_ID}/modules/2099/items")
items.sort(key=lambda x: x["position"])
for it in items:
    print(f"  {it['position']:2d}  {it['type']:10s}  {it['title']}")
print(f"  Total: {len(items)} (expect 26)")

print("\n=== Module 2101 (renamed Day 10, was Day 11) item order ===")
items2 = api_get(f"/courses/{COURSE_ID}/modules/2101/items")
items2.sort(key=lambda x: x["position"])
for it in items2:
    print(f"  {it['position']:2d}  {it['type']:10s}  {it['title']}")
print(f"  Total: {len(items2)} (expect 11)")

print("\n=== Checking no orphaned duplicate quizzes exist for Practice 49-58 ===")
quizzes = api_get(f"/courses/{COURSE_ID}/quizzes")
from collections import Counter
titles = Counter(q["title"] for q in quizzes)
dupes = {t: c for t, c in titles.items() if c > 1}
print(f"  Total quizzes in course: {len(quizzes)}")
print(f"  Duplicate titles: {dupes if dupes else 'none'}")
