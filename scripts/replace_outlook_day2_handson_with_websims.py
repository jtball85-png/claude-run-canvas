# -*- coding: utf-8 -*-
"""Replaces course 454's 3 Day 2 (Chapter 2: Email) Hands-On assignments --
which have sat with literal "[SUBMISSION-EMAIL-PLACEHOLDER]" text since the
course was built, waiting on a real mailbox address that was never set up --
with 3 ungraded Pages pointing students at the real WebSims for each DYS
exercise instead, per Josh's decision (2026-10-05): scrub the email-mailbox
model entirely, point students at the now-confirmed WebSim access method
(labyrinthelab.com/msoffice -- no login, built this same session) instead.
Confirmed with Josh: make these ungraded practice pointers (same pattern as
the existing "eLab Self-Paced Practice" item already in this module), not a
different graded deliverable -- course point total drops by 14 pts (5+3+6).

Each new Page keeps the same topic/skill breakdown as the old assignment
(already sourced from the real textbook pages during the original Day 2
build), reframed from "do this in real Outlook and email it" to "practice
this in the matching WebSim" -- no submission, no rubric, no email.

Does NOT touch: the Reading pages, the Chapter 2 Presentation, the eLab
Self-Paced Practice link, the Chapter 2 Quiz/Test (eLab or Canvas) -- only
the 3 Hands-On assignments and their module item slots.

Course 454 is unpublished / 0 students, so deleting the old Assignment
objects outright (not just unlinking them) is safe -- matches how course
453's triplicated content was handled, not surgical-only caution reserved
for live courses with real submissions.
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
COURSE_ID = 454
MODULE_ID = 2075

WEBSIM_HOWTO = (
    '<div style="background:#F5F7FA;border-left:5px solid #FFCF01;border-radius:4px;'
    'padding:12px 14px;margin:12px 0;">'
    '<strong style="color:#003462;">How to find these WebSims</strong>'
    '<p style="margin:6px 0 0;">Go to '
    '<a href="https://www.labyrinthelab.com/msoffice/index.php?qversion=TWowMFRXL0l4aFVXWTdQd2h3TnZldz09" '
    'target="_blank" rel="noopener" style="color:#003462;font-weight:bold;">labyrinthelab.com/msoffice</a> '
    "&rarr; <strong>FastCourse Outlook 2021</strong> &rarr; <strong>View Learning Resources</strong> &rarr; "
    "<strong>Chapter 2: Email</strong>. Each part below names the exact WebSim to look for (e.g. "
    '"DYS OU2-D2") &mdash; click it to open it right in your browser. No login, no account, free with '
    "your textbook.</p></div>"
)

NOT_GRADED_NOTE = (
    '<div style="background:#F5F7FA;border-radius:4px;padding:10px 12px;font-size:13px;margin-top:4px;">'
    "<strong style=\"color:#003462;\">This is self-paced practice &mdash; nothing to submit.</strong> "
    "Your understanding of Chapter 2 is assessed by the Chapter 2 Quiz and Test later in this module."
    "</div>"
)


def header(eyebrow, title):
    return (
        '<div style="background:#003462;color:white;border-radius:4px;padding:20px 24px;margin:0 0 16px;">'
        f'<div style="font-size:12px;color:#FFCF01;">{eyebrow}</div>'
        f'<h1 style="margin:4px 0 4px;font-size:28px;line-height:1.15;color:white;">{title}</h1>'
        '<div style="font-size:17px;line-height:1.35;color:#B5E3F0;">Self-paced WebSim practice &mdash; not graded</div>'
        "</div>"
    )


def part_card(accent, heading, body_html):
    color = "#00B7A3" if accent == "teal" else "#B5E3F0"
    return (
        f'<div style="border-left:5px solid {color};background:#FFFFFF;border-top:1px solid #CBD5E1;'
        "border-right:1px solid #CBD5E1;border-bottom:1px solid #CBD5E1;border-radius:4px;"
        'padding:16px 18px;margin:14px 0;">'
        f'<h2 style="font-size:20px;line-height:1.25;margin:0 0 10px;color:#003462;">{heading}</h2>'
        f"{body_html}</div>"
    )


def wrap(eyebrow, title, parts):
    body = '<div style="font-family:Arial,Helvetica,sans-serif;line-height:1.55;color:#1F2937;max-width:920px;margin:0 auto;">'
    body += header(eyebrow, title)
    body += WEBSIM_HOWTO
    accents = ["teal", "blue"]
    for i, (heading, text) in enumerate(parts):
        body += part_card(accents[i % 2], heading, f'<p style="margin:0;">{text}</p>')
    body += NOT_GRADED_NOTE
    body += "</div>"
    return body


PAGES = [
    {
        "old_item_id": 15739,
        "old_assignment_id": 8592,
        "title": "Practice: OU2-D2–D6 — Compose, Sign, Attach & Check Your Email",
        "eyebrow": "Book pages: 17-26 · Develop Your Skills OU2-D2 through OU2-D6",
        "parts": [
            (
                "WebSim OU2-D2: Multiple Recipients",
                "Practice addressing a message To multiple people, Cc a classmate, and Bcc yourself &mdash; see how each field works differently.",
            ),
            (
                "WebSim OU2-D3: Create Signatures",
                "Practice creating two signatures &mdash; a &ldquo;Professional&rdquo; one (your name, a title, contact info) and a &ldquo;Casual&rdquo; one (a short informal sign-off) &mdash; and setting defaults for New Messages vs. Replies/Forwards.",
            ),
            (
                "WebSim OU2-D4: Apply a Signature",
                "Practice manually switching which signature is applied to a message, via Message &rarr; Signature, before sending.",
            ),
            (
                "WebSim OU2-D5: Attach a File",
                "Practice attaching a file to a message via Message &rarr; Attach File before sending.",
            ),
            (
                "WebSim OU2-D6: Spelling & Grammar Check",
                "Practice running Spelling &amp; Grammar Check (F7) on a message and correcting the flagged errors before sending.",
            ),
        ],
    },
    {
        "old_item_id": 15741,
        "old_assignment_id": 8593,
        "title": "Practice: OU2-D7–D9 — Read, Reply, Forward, Flag & Print",
        "eyebrow": "Book pages: 29-34 · Develop Your Skills OU2-D7 through OU2-D9",
        "parts": [
            (
                "WebSim OU2-D7: Save an Attachment",
                "Practice opening a message with an attachment, saving it with Save As, and confirming the save.",
            ),
            (
                "WebSim OU2-D8: Reply and Forward",
                "Practice replying to a message with a short note, and forwarding a message with your own note added above the original.",
            ),
            (
                "WebSim OU2-D9: Flag and Print",
                "Practice flagging a message for follow-up and reviewing the Backstage Print options (Memo vs. Table style).",
            ),
        ],
    },
    {
        "old_item_id": 15743,
        "old_assignment_id": 8594,
        "title": "Practice: OU2-D10–D15 — Folders, Quick Steps, Rules, Search, Delete & Archive",
        "eyebrow": "Book pages: 35-43 · Develop Your Skills OU2-D10 through OU2-D15",
        "parts": [
            (
                "WebSim OU2-D10: Folders & Favorites",
                "Practice creating new folders and adding one to Favorites.",
            ),
            (
                "WebSim OU2-D11: Move Messages",
                "Practice moving messages into folders by dragging, and via Home &rarr; Move &rarr; Other Folder.",
            ),
            (
                "WebSim OU2-D12: Quick Step & Rule",
                "Practice creating a Quick Step (Move to Folder) and a Rule (a condition + an action) via Home &rarr; Quick Steps / Rules.",
            ),
            (
                "WebSim OU2-D13: Search",
                "Practice using the Search box to find a message by keyword.",
            ),
            (
                "WebSim OU2-D14: Delete",
                "Practice deleting a message and emptying Deleted Items.",
            ),
            (
                "WebSim OU2-D15: Archive",
                "Practice archiving an old message via the Move to Archive Folder button.",
            ),
        ],
    },
]


def api_get(endpoint):
    r = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS)
    r.raise_for_status()
    return r.json()


def api_post(endpoint, data):
    r = requests.post(f"{BASE_URL}{endpoint}", headers=HEADERS, json=data)
    if r.status_code not in (200, 201):
        print(f"  ERROR {r.status_code}: {r.text[:400]}")
        return None
    return r.json()


def api_put(endpoint, data):
    r = requests.put(f"{BASE_URL}{endpoint}", headers=HEADERS, json=data)
    if r.status_code not in (200, 201):
        print(f"  ERROR {r.status_code}: {r.text[:400]}")
        return None
    return r.json()


def api_delete(endpoint):
    r = requests.delete(f"{BASE_URL}{endpoint}", headers=HEADERS)
    return r.status_code


if __name__ == "__main__":
    before = api_get(f"/courses/{COURSE_ID}/modules/{MODULE_ID}/items?per_page=50")
    print(f"Module {MODULE_ID} before: {len(before)} items")

    for spec in PAGES:
        body = wrap(spec["eyebrow"], spec["title"], spec["parts"])

        print(f"\nCreating page: {spec['title']}")
        page = api_post(f"/courses/{COURSE_ID}/pages", {
            "wiki_page": {"title": spec["title"], "body": body, "published": False}
        })
        if page is None:
            sys.exit(1)
        slug = page["url"]
        print(f"  Created page slug: {slug}")

        old_item = next(it for it in before if it["id"] == spec["old_item_id"])
        position = old_item["position"]

        new_item = api_post(f"/courses/{COURSE_ID}/modules/{MODULE_ID}/items", {
            "module_item": {
                "title": spec["title"],
                "type": "Page",
                "page_url": slug,
                "position": position,
            }
        })
        if new_item is None:
            sys.exit(1)
        print(f"  Inserted module item {new_item['id']} at position {position}")

        del_code = api_delete(f"/courses/{COURSE_ID}/modules/{MODULE_ID}/items/{spec['old_item_id']}")
        print(f"  Deleted old module item {spec['old_item_id']} (status {del_code})")

        del_code = api_delete(f"/courses/{COURSE_ID}/assignments/{spec['old_assignment_id']}")
        print(f"  Deleted old assignment {spec['old_assignment_id']} (status {del_code})")

    after = api_get(f"/courses/{COURSE_ID}/modules/{MODULE_ID}/items?per_page=50")
    print(f"\nModule {MODULE_ID} after: {len(after)} items (was {len(before)})")
    for it in sorted(after, key=lambda x: x["position"]):
        print(f"  {it['position']:>2}  {it['type']:<12} {it.get('title')}")
