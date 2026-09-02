# -*- coding: utf-8 -*-
"""Restructures Business Math (course 456) from 11 Canvas Day modules down
to 10, matching the real Wk8-10 calendar (which only has 10 Tue/Wed/Thu
instructional slots -- see `Business Math Pacing & Calendar Analysis.md`).

Days 9 and 10 (both lightweight, practice-quiz-only Percent lessons) are
already taught together in one classroom sitting per the Day 09-10 combined
lesson plan -- this script makes the Canvas course match that reality:

1. Move Day 10's 16 module items into Day 9's module (module 2099), reusing
   the SAME underlying Page/Quiz objects (module items are just references;
   Pages/Quizzes/Assignments are course-level content, not module-owned --
   confirmed by the Outlook build's "deleting a module doesn't delete its
   content" finding). No content is duplicated or recreated.
2. Delete the now-empty Day 10 module container (2100).
3. Rename module 2099 to reflect the merged content.
4. Rename + reposition the old Day 11 module (2101) down to "Day 10" at
   position 11.
5. Update the Course Overview page's Course Map table: merge the old Day
   9/10 rows into one, renumber the old Day 11 row down to Day 10.

HARD RULE: no content (Page/Quiz/Assignment objects) is deleted or
recreated -- only ModuleItem references and module containers are touched,
plus one page body edit. Verifies the live module list before and after.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from push_course import api_get, api_post, api_put, api_delete

COURSE_ID = 456
DAY9_MODULE_ID = 2099
DAY10_MODULE_ID = 2100
DAY11_MODULE_ID = 2101

DAY9_NEW_NAME = "Day 9, Unit 5: Percent (Writing Percents, Conversions, Finding the Part, Percent, and Whole)"
DAY10_NEW_NAME = "Day 10, Unit 5: Percent (Multi-Step Problems, Interest, Review, Quiz, Test)"

OVERVIEW_PAGE_URL = "business-math-welcome"

OLD_MAP_ROWS = (
    '<tr><td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Day 9</td>'
    '<td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Unit 5 &middot; Percent</td>'
    '<td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Writing Percents and Converting Between Percents, Decimals, and Fractions</td></tr>'
    '<tr><td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Day 10</td>'
    '<td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Unit 5 &middot; Percent</td>'
    '<td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Finding the Part, the Percent, and the Whole</td></tr>'
    '<tr><td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Day 11</td>'
    '<td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Unit 5 &middot; Percent</td>'
    '<td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Interest, Multi-Step Percent Problems, and Percent Review</td></tr>'
)

NEW_MAP_ROWS = (
    '<tr><td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Day 9</td>'
    '<td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Unit 5 &middot; Percent</td>'
    '<td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Writing Percents, Converting Between Percents/Decimals/Fractions, and Finding the Part, the Percent, and the Whole</td></tr>'
    '<tr><td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Day 10</td>'
    '<td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Unit 5 &middot; Percent</td>'
    '<td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Interest, Multi-Step Percent Problems, and Percent Review</td></tr>'
)


def main():
    print("=== Verifying live module list before restructure ===")
    mods_before = api_get(f"/courses/{COURSE_ID}/modules")
    for m in sorted(mods_before, key=lambda x: x.get("position", 0)):
        print(m["position"], m["id"], m["name"])
    print(f"({len(mods_before)} modules before)\n")

    print("=== Step 1: Moving Day 10's 16 items into Day 9's module (2099) ===")
    day10_items = api_get(f"/courses/{COURSE_ID}/modules/{DAY10_MODULE_ID}/items")
    day10_items.sort(key=lambda x: x["position"])
    assert len(day10_items) == 16, f"expected 16 Day 10 items, found {len(day10_items)}"

    for it in day10_items:
        payload = {"module_item": {"type": it["type"], "title": it["title"]}}
        if it.get("content_id"):
            payload["module_item"]["content_id"] = it["content_id"]
        if it.get("page_url"):
            payload["module_item"]["page_url"] = it["page_url"]
        result = api_post(f"/courses/{COURSE_ID}/modules/{DAY9_MODULE_ID}/items", payload)
        status = "OK" if result else "FAILED"
        print(f"  [{status}] moved: {it['title']}")

    print("\n=== Step 2: Verifying Day 9's module now has 26 items ===")
    day9_items_after = api_get(f"/courses/{COURSE_ID}/modules/{DAY9_MODULE_ID}/items")
    print(f"  Day 9 module now has {len(day9_items_after)} items (expected 26)")
    assert len(day9_items_after) == 26, "STOP: Day 9 module does not have 26 items -- do not delete Day 10 module yet"

    print("\n=== Step 3: Deleting the now-empty Day 10 module container ===")
    deleted = api_delete(f"/courses/{COURSE_ID}/modules/{DAY10_MODULE_ID}")
    print(f"  Module {DAY10_MODULE_ID} deleted: {deleted}")

    print("\n=== Step 4: Renaming Day 9's module to reflect merged content ===")
    r1 = api_put(f"/courses/{COURSE_ID}/modules/{DAY9_MODULE_ID}", {"module": {"name": DAY9_NEW_NAME}})
    print(f"  Renamed module {DAY9_MODULE_ID}: {'OK' if r1 else 'FAILED'}")

    print("\n=== Step 5: Renaming + repositioning old Day 11 module to Day 10 ===")
    r2 = api_put(f"/courses/{COURSE_ID}/modules/{DAY11_MODULE_ID}", {"module": {"name": DAY10_NEW_NAME, "position": 11}})
    print(f"  Renamed/repositioned module {DAY11_MODULE_ID}: {'OK' if r2 else 'FAILED'}")

    print("\n=== Step 6: Updating Course Overview page's Course Map table ===")
    page = api_get(f"/courses/{COURSE_ID}/pages/{OVERVIEW_PAGE_URL}")
    body = page["body"]
    if OLD_MAP_ROWS not in body:
        print("  ERROR: expected old Day 9/10/11 table rows not found verbatim in the live page body -- skipping page edit, fix manually.")
    else:
        new_body = body.replace(OLD_MAP_ROWS, NEW_MAP_ROWS)
        r3 = api_put(f"/courses/{COURSE_ID}/pages/{OVERVIEW_PAGE_URL}", {"wiki_page": {"body": new_body}})
        print(f"  Course Overview page updated: {'OK' if r3 else 'FAILED'}")

    print("\n=== Verifying live module list after restructure ===")
    mods_after = api_get(f"/courses/{COURSE_ID}/modules")
    for m in sorted(mods_after, key=lambda x: x.get("position", 0)):
        print(m["position"], m["id"], m["name"])
    print(f"({len(mods_after)} modules after)")

    before_ids = {m["id"] for m in mods_before}
    after_ids = {m["id"] for m in mods_after}
    print(f"\nRemoved module ids: {before_ids - after_ids} (expect {{{DAY10_MODULE_ID}}})")
    print(f"Added module ids: {after_ids - before_ids} (expect empty set)")


if __name__ == "__main__":
    main()
