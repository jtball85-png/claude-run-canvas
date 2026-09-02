# -*- coding: utf-8 -*-
"""Fixes the Course Overview page's Course Map table (Day 9/10/11 rows ->
Day 9/10), using the literal middot character since Canvas decodes
&middot; to the actual · character when storing page bodies."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from push_course import api_get, api_put

COURSE_ID = 456
OVERVIEW_PAGE_URL = "business-math-welcome"

OLD_MAP_ROWS = (
    '<tr><td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Day 9</td>'
    '<td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Unit 5 · Percent</td>'
    '<td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Writing Percents and Converting Between Percents, Decimals, and Fractions</td></tr>'
    '<tr><td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Day 10</td>'
    '<td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Unit 5 · Percent</td>'
    '<td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Finding the Part, the Percent, and the Whole</td></tr>'
    '<tr><td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Day 11</td>'
    '<td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Unit 5 · Percent</td>'
    '<td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Interest, Multi-Step Percent Problems, and Percent Review</td></tr>'
)

NEW_MAP_ROWS = (
    '<tr><td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Day 9</td>'
    '<td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Unit 5 · Percent</td>'
    '<td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Writing Percents, Converting Between Percents/Decimals/Fractions, and Finding the Part, the Percent, and the Whole</td></tr>'
    '<tr><td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Day 10</td>'
    '<td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Unit 5 · Percent</td>'
    '<td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Interest, Multi-Step Percent Problems, and Percent Review</td></tr>'
)


def main():
    page = api_get(f"/courses/{COURSE_ID}/pages/{OVERVIEW_PAGE_URL}")
    body = page["body"]
    if OLD_MAP_ROWS not in body:
        print("ERROR: still not found. Aborting -- fix manually.")
        return
    new_body = body.replace(OLD_MAP_ROWS, NEW_MAP_ROWS)
    result = api_put(f"/courses/{COURSE_ID}/pages/{OVERVIEW_PAGE_URL}", {"wiki_page": {"body": new_body}})
    print("Course Overview page updated:", "OK" if result else "FAILED")

    # verify
    page2 = api_get(f"/courses/{COURSE_ID}/pages/{OVERVIEW_PAGE_URL}")
    idx = page2["body"].find(">Day 9<")
    print(page2["body"][idx-20:idx+700])


if __name__ == "__main__":
    main()
