# -*- coding: utf-8 -*-
"""Adds a new "How to Access the WebSims" section to course 454's existing
"How to Use Your Class Resources" page, per Josh's request (2026-10-05):
a clean, clear way to show students how to reach the Labyrinth WebSims.

Confirmed directly by Labyrinth tech/sales support (Mark Perkins,
mperkins@lablearning.com, email 2026-10-05): WebSim access via
https://www.labyrinthelab.com/msoffice/index.php?qversion=TWowMFRXL0l4aFVXWTdQd2h3TnZldz09
is included free with the textbook, no separate login/account/license key
-- students just click through to their course and launch a resource. This
is a more reliable path than the Canvas-embedded "eLab Self-Paced Practice"
LTI links (which Labyrinth's own Canvas Integration Admin Guide says
*does* require a one-time registration + license key the first time --
unverified whether that actually triggers for this FastCourse title, since
the physical book prints no individual code). Both sections are kept side
by side on the page; this new one is the guaranteed-working option.

Surgical PUT against the live page (never push_course.py's delete-and-
rebuild path), matching this project's established pattern.
"""
import os
import sys

import requests
from dotenv import load_dotenv

sys.path.insert(0, "scripts")
from push_course import HEADERS  # noqa: E402

load_dotenv()
BASE_URL = os.getenv("CANVAS_BASE_URL")
COURSE_ID = 454
PAGE_SLUG = "how-to-use-class-resources"

NEW_SECTION = (
    '<div style="border-left:5px solid #FFCF01;background:#FFFFFF;'
    "border-top:1px solid #CBD5E1;border-right:1px solid #CBD5E1;"
    "border-bottom:1px solid #CBD5E1;border-radius:4px;padding:16px 18px;"
    'margin:14px 0;">'
    '<h2 style="font-size:20px;line-height:1.25;margin:0 0 10px;color:#003462;">'
    "How to Access the WebSims</h2>"
    '<p style="margin:0 0 10px;">Your textbook includes free access to Labyrinth\'s WebSims '
    "&mdash; interactive simulations of real Outlook screens where you can click through a "
    "task exactly like you would in the real app. No account, login, or purchase required "
    "&mdash; it's included with your book.</p>"
    '<ol style="margin:0 0 10px;padding-left:22px;">'
    '<li style="margin-bottom:8px;">Go to '
    '<a href="https://www.labyrinthelab.com/msoffice/index.php?qversion=TWowMFRXL0l4aFVXWTdQd2h3TnZldz09" '
    'target="_blank" rel="noopener" style="color:#003462;font-weight:bold;">'
    "labyrinthelab.com/msoffice</a> (bookmark this page &mdash; you'll use it all course long).</li>"
    '<li style="margin-bottom:8px;">Scroll down to the <strong>FastCourse Series</strong> section '
    "and find <strong>FastCourse Outlook 2021</strong>.</li>"
    '<li style="margin-bottom:8px;">Click <strong>View Learning Resources</strong>.</li>'
    '<li style="margin-bottom:8px;">Click the chapter that matches today\'s lesson '
    "(Chapter 1&ndash;5).</li>"
    '<li style="margin-bottom:0;">Click any WebSim, video, or presentation in the list to launch '
    "it right in your browser &mdash; nothing to install, nothing to log into.</li>"
    "</ol>"
    '<div style="background:#F5F7FA;border-radius:4px;padding:10px 12px;font-size:13px;">'
    '<strong style="color:#003462;">No login screen?</strong> That\'s normal &mdash; this page '
    "doesn't require one. If anything ever asks you for a password or payment here, stop and "
    "tell your instructor before entering anything.</div>"
    "</div>"
)

QUICK_REF_ROW = (
    "<tr><td style=\"vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;\">"
    "WebSims (chapter simulations &amp; videos)</td>"
    "<td style=\"vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;\">"
    "<a href=\"https://www.labyrinthelab.com/msoffice/index.php?qversion=TWowMFRXL0l4aFVXWTdQd2h3TnZldz09\" "
    "target=\"_blank\" rel=\"noopener\" style=\"color:#003462;\">labyrinthelab.com/msoffice</a> "
    "&rarr; FastCourse Outlook 2021 &rarr; View Learning Resources &rarr; your chapter"
    "</td></tr>"
)

INSERT_BEFORE = '<div style="background:#F5F7FA;border-left:5px solid #FFCF01;border-radius:4px;padding:16px 18px;margin:14px 0;"><h2 style="font-size:18px;'


def api_get(endpoint):
    r = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS)
    r.raise_for_status()
    return r.json()


def api_put(endpoint, data):
    r = requests.put(f"{BASE_URL}{endpoint}", headers=HEADERS, json=data)
    if r.status_code not in (200, 201):
        print(f"  ERROR {r.status_code}: {r.text[:400]}")
        return None
    return r.json()


if __name__ == "__main__":
    live = api_get(f"/courses/{COURSE_ID}/pages/{PAGE_SLUG}")
    body = live["body"]

    if "How to Access the WebSims" in body:
        print("Section already present -- not re-adding.")
        sys.exit(0)

    idx = body.find(INSERT_BEFORE)
    if idx == -1:
        sys.exit("ERROR: could not find the Quick Reference callout marker to insert before")
    new_body = body[:idx] + NEW_SECTION + body[idx:]

    row_marker = "</tbody></table>"
    row_idx = new_body.find(row_marker)
    if row_idx == -1:
        sys.exit("ERROR: could not find the Quick Reference table's closing tag")
    new_body = new_body[:row_idx] + QUICK_REF_ROW + new_body[row_idx:]

    print(f"Updating page '{PAGE_SLUG}' in course {COURSE_ID} ({len(body)} -> {len(new_body)} chars)...")
    result = api_put(f"/courses/{COURSE_ID}/pages/{PAGE_SLUG}", {"wiki_page": {"body": new_body}})
    if result is None:
        sys.exit(1)

    live_check = api_get(f"/courses/{COURSE_ID}/pages/{PAGE_SLUG}")
    ok = "How to Access the WebSims" in live_check["body"] and "WebSims (chapter simulations" in live_check["body"]
    print("Verified clean." if ok else "WARNING: verification did not find expected content.")
