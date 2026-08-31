"""
push_word_day6.py
One-off surgical push: adds ONLY the Day 6 module (Word Chapter 5) to the
already-live course 455, without touching existing modules.
"""
import json
import sys
sys.path.insert(0, "scripts")
from push_course import create_module, ITEM_HANDLERS

TEMPLATE = "templates/microsoft-word-2627.json"
COURSE_ID = 455
DRY_RUN = "--dry-run" in sys.argv

with open(TEMPLATE, encoding="utf-8") as f:
    template = json.load(f)

day6 = next(m for m in template["modules"] if m["name"].startswith("Day 6"))

print(f"Template : {template['course_name']}")
print(f"Target   : Course ID {COURSE_ID}")
print(f"Module   : {day6['name']} ({len(day6['items'])} items)")
print(f"Mode     : {'DRY RUN' if DRY_RUN else 'LIVE'}\n")

module_id = create_module(COURSE_ID, day6, dry_run=DRY_RUN)
if not module_id:
    print("Module creation failed, aborting.")
    sys.exit(1)

for item in day6.get("items", []):
    item_type = item.get("type", "").lower()
    handler = ITEM_HANDLERS.get(item_type)
    if handler:
        handler(COURSE_ID, module_id, item, dry_run=DRY_RUN)
    else:
        print(f"  UNKNOWN item type: {item.get('type')} -- skipping")

print("\nDone.")
