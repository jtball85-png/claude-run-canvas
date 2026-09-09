# -*- coding: utf-8 -*-
"""One-off targeted update of Business Math (course 456) Day 1 reading pages,
per Josh's feedback (2026-09-09): examples were too wordy/sentence-based --
rebuilt as visual place-value tables + step-by-step callouts instead of prose.

Only the 3 reading pages' body HTML changes. Practice quizzes, Day 1 Overview,
and Want More Practice? are untouched. Source of truth for the new bodies is
the sibling repo's day1-module-fragment.json (Master Business Finance
Program), read directly here so nothing gets retyped/out of sync.

Uses targeted PUTs against already-live Pages (matched by url slug), same
pattern as rebuild_business_math_unit1_content.py -- never push_course.py's
delete-and-rebuild path.
"""
import json
import os
import sys

import requests
from dotenv import load_dotenv

sys.path.insert(0, "scripts")
from push_course import HEADERS  # noqa: E402

load_dotenv()
BASE_URL = os.getenv("CANVAS_BASE_URL")
COURSE_ID = 456

FRAGMENT_PATH = (
    r"C:\Users\jball.VACE\Documents\Claude Projects"
    r"\Master Business Finance Program\Lesson Planning\Business Math"
    r"\day1-module-fragment.json"
)

SLUG_BY_TITLE = {
    "Place Value — Reading": "place-value-reading",
    "Reading and Writing Whole Numbers — Reading": "reading-and-writing-whole-numbers-reading",
    "Rounding Whole Numbers — Reading": "rounding-whole-numbers-reading",
}


def api_get(endpoint):
    r = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS)
    r.raise_for_status()
    return r.json()


def api_put(endpoint, data):
    r = requests.put(f"{BASE_URL}{endpoint}", headers=HEADERS, json=data)
    if r.status_code not in (200, 201):
        print(f"  ERROR {r.status_code}: {r.text[:300]}")
        return None
    return r.json()


def update_page(url_slug, body):
    print(f"  PUT page: {url_slug} ({len(body)} chars)")
    return api_put(f"/courses/{COURSE_ID}/pages/{url_slug}", {"wiki_page": {"body": body}})


ENTITY_MAP = {
    "&middot;": "·",
    "&mdash;": "—",
    "&minus;": "−",
    "&rsquo;": "’",
    "&ldquo;": "“",
    "&rdquo;": "”",
    "&times;": "×",
    "&divide;": "÷",
    "&rarr;": "→",
}


def normalize(html):
    # Canvas's RCE re-serializes saved HTML: named entities become literal
    # unicode chars. Normalize before comparing so a clean round-trip reads
    # as a match instead of a false-positive mismatch.
    for entity, char in ENTITY_MAP.items():
        html = html.replace(entity, char)
    return html


if __name__ == "__main__":
    with open(FRAGMENT_PATH, encoding="utf-8") as f:
        fragment = json.load(f)

    items = fragment["modules"][0]["items"]
    bodies_by_title = {
        it["title"]: it["body"] for it in items if it["type"] == "page" and it["title"] in SLUG_BY_TITLE
    }
    missing = set(SLUG_BY_TITLE) - set(bodies_by_title)
    if missing:
        print(f"ERROR: fragment is missing expected page(s): {missing}")
        sys.exit(1)

    print(f"Pushing {len(bodies_by_title)} updated reading pages to course {COURSE_ID}...")
    for title, slug in SLUG_BY_TITLE.items():
        update_page(slug, bodies_by_title[title])

    print("\nVerifying live page bodies match what was pushed...")
    all_ok = True
    for title, slug in SLUG_BY_TITLE.items():
        live = api_get(f"/courses/{COURSE_ID}/pages/{slug}")
        live_body = live.get("body", "")
        expected = normalize(bodies_by_title[title])
        ok = live_body == expected
        all_ok = all_ok and ok
        print(f"  {slug}: {'OK' if ok else 'MISMATCH'} (live {len(live_body)} chars, expected {len(expected)} chars)")

    print("\nAll pages verified clean." if all_ok else "\nWARNING: one or more pages did not verify cleanly -- check above.")
