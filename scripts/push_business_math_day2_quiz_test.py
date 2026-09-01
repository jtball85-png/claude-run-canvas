"""One-off: adds Unit 1 Quiz and Unit 1 Test to the already-live Day 2 module
(id 2092) in course 456, after an earlier push crashed mid-quiz on a Windows
console encoding bug (now fixed in push_course.py). Reads the two quiz items
straight out of templates/business-math-day2.json rather than redefining
them, so there's a single source of truth."""
import json
import sys
sys.path.insert(0, "scripts")
from push_course import create_quiz

COURSE_ID = 456
MODULE_ID = 2092

with open("templates/business-math-day2.json", encoding="utf-8") as f:
    template = json.load(f)

items = template["modules"][0]["items"]
quiz_items = [it for it in items if it["type"] == "quiz"]
assert len(quiz_items) == 2, f"expected 2 quiz items, found {len(quiz_items)}"

for item in quiz_items:
    create_quiz(COURSE_ID, MODULE_ID, item, dry_run=False)

print("\nDone.")
