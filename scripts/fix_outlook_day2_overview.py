# -*- coding: utf-8 -*-
"""Rewrites course 454's Day 2 Overview page: removes the last remaining
"[SUBMISSION-EMAIL-PLACEHOLDER]" reference and the now-wrong "instructor
prep: send a starter email" box (no real Inbox/starter email needed once
OU2-D7-D9 is WebSim practice, not a real-Outlook exercise), rewords Today's
Tasks from "complete Hands-On" to "practice (WebSims)", and replaces the
"How Hands-On grading works today" explanation with the new one: WebSims
are self-paced/ungraded, Quiz+Test are the real graded assessment. Matches
replace_outlook_day2_handson_with_websims.py's decision, same session.

Uses the exact live body (fetched fresh, literal em/en-dash characters --
Canvas's RCE already normalized this page's HTML entities on an earlier
save), not hand-typed &mdash;/&ndash; source.
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
PAGE_SLUG = "day-2-overview-tasks-and-competencies"

OLD_PREP_BOX = (
    '<div style="background:#F5F7FA;border-left:5px solid #FFCF01;border-radius:4px;padding:12px 14px;margin:12px 0;">'
    '<strong style="color:#003462;">Before class: instructor prep</strong>'
    '<p style="margin:6px 0 0;">Send each student a starter email (with a file attached) from the submission '
    "mailbox before this day begins — the Handling Incoming Messages exercises need a real message with "
    "an attachment already sitting in each student's Inbox.</p></div>"
)

OLD_TASKS = (
    "<li>Sending Messages — read, then complete Hands-On OU2-D2–D6</li>"
    "<li>Handling Incoming Messages — read, then complete Hands-On OU2-D7–D9</li>"
    "<li>Organizing Messages — read, then complete Hands-On OU2-D10–D15</li>"
)
NEW_TASKS = (
    "<li>Sending Messages — read, then practice OU2-D2–D6 (WebSims)</li>"
    "<li>Handling Incoming Messages — read, then practice OU2-D7–D9 (WebSims)</li>"
    "<li>Organizing Messages — read, then practice OU2-D10–D15 (WebSims)</li>"
)

OLD_GRADING_BOX = (
    '<div style="background:#F5F7FA;border-left:5px solid #FFCF01;border-radius:4px;padding:12px 14px;margin:12px 0;">'
    '<strong style="color:#003462;">How Hands-On grading works today</strong>'
    "<p style=\"margin:6px 0 0;\">Unlike Chapter 1, today's Develop Your Skills exercises are built around WebSims "
    "(Labyrinth's simulated Outlook environment) — but WebSim completion doesn't produce a screenshot you "
    "control the way real Outlook does. Instead, you'll work live in your real VACE Outlook account and prove "
    "each exercise by sending a real email to <strong>[SUBMISSION-EMAIL-PLACEHOLDER — Josh to provide before "
    "publishing]</strong>, the monitored inbox your instructor checks for completion. The WebSim link is still "
    "available below for review/practice before or after each reading.</p></div>"
)
NEW_GRADING_BOX = (
    '<div style="background:#F5F7FA;border-left:5px solid #FFCF01;border-radius:4px;padding:12px 14px;margin:12px 0;">'
    "<strong style=\"color:#003462;\">How today's Develop Your Skills exercises work</strong>"
    "<p style=\"margin:6px 0 0;\">Unlike Chapter 1, today's Develop Your Skills exercises are built around WebSims "
    "(Labyrinth's simulated Outlook environment), not real-Outlook tasks — so instead of a graded Hands-On "
    "assignment, each reading is followed by a self-paced WebSim practice page listing the matching WebSims and "
    "how to find them. Nothing to submit for these. Your grade for this chapter comes from the Chapter 2 Quiz "
    "and Test later in this module.</p></div>"
)


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
    original_len = len(body)

    for label, old, new in [
        ("prep box", OLD_PREP_BOX, ""),
        ("tasks list", OLD_TASKS, NEW_TASKS),
        ("grading box", OLD_GRADING_BOX, NEW_GRADING_BOX),
    ]:
        if old not in body:
            sys.exit(f"ERROR: {label} not found verbatim -- aborting, nothing written")
        body = body.replace(old, new, 1)

    print(f"Updating page '{PAGE_SLUG}' in course {COURSE_ID} ({original_len} -> {len(body)} chars)...")
    result = api_put(f"/courses/{COURSE_ID}/pages/{PAGE_SLUG}", {"wiki_page": {"body": body}})
    if result is None:
        sys.exit(1)

    check = api_get(f"/courses/{COURSE_ID}/pages/{PAGE_SLUG}")
    ok = (
        "SUBMISSION-EMAIL-PLACEHOLDER" not in check["body"]
        and "practice OU2-D2" in check["body"]
        and "How today's Develop Your Skills exercises work" in check["body"]
        and "instructor prep" not in check["body"]
    )
    print("Verified clean." if ok else "WARNING: verification did not find expected content.")
