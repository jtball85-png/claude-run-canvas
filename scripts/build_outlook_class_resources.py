"""
build_outlook_class_resources.py
---------------------------------
Course-by-course Class Resources pass, course 454 (Microsoft Outlook 26/27) --
second course in the pass after 452 (Computer and Internet Fundamentals).

Confirmed with Josh: this course's recurring resources are Chapter
Presentations and eLab Self-Paced Practice (no Skill Builders / Typing.com --
those are Computer Basics-specific).

Steps:
1. Create Files > Presentations folder under course files (2694), move the
   5 chapter PPT files into it via parent_folder_id (not re-upload).
2. Create "How to Use Class Resources" page (2 sections).
3. Insert "How to Use Class Resources" module at position 2 (right after
   Course Overview, before Day 1) with that page as its one item.
4. Insert a "Class Resources" section into the Course Overview (welcome)
   page, between "Course Map" and "How Classes Are Taught".
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("CANVAS_API_TOKEN")
BASE_URL = os.getenv("CANVAS_BASE_URL")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": "claude-run-canvas/1.0 (Ventura Adult and Continuing Education)",
}
COURSE_ID = 454
PRESENTATIONS_PARENT_FOLDER_ID = 2694  # "course files"
PPT_FILE_IDS = [20564, 20573, 20593, 20604, 20617]


def get_all_pages(url, params=None):
    results = []
    while url:
        r = requests.get(url, headers=HEADERS, params=params)
        r.raise_for_status()
        results.extend(r.json())
        url = None
        params = None
        for part in r.headers.get("Link", "").split(","):
            if 'rel="next"' in part:
                url = part.split(";")[0].strip().strip("<>")
    return results


RESOURCES_PAGE_BODY = """<div style="font-family:Arial,Helvetica,sans-serif;line-height:1.55;color:#1F2937;max-width:920px;margin:0 auto;"><div style="background:#003462;color:white;border-radius:4px;padding:20px 24px;margin:0 0 16px;"><div style="font-size:12px;color:#FFCF01;">Microsoft Outlook &middot; Class Resources</div><h1 style="margin:4px 0 4px;font-size:28px;line-height:1.15;color:white;">How to Use Your Class Resources</h1><div style="font-size:17px;line-height:1.35;color:#B5E3F0;">Two things you'll use throughout this course &mdash; and exactly where to find each one.</div></div><div style="border-left:5px solid #00B7A3;background:#FFFFFF;border-top:1px solid #CBD5E1;border-right:1px solid #CBD5E1;border-bottom:1px solid #CBD5E1;border-radius:4px;padding:16px 18px;margin:14px 0;"><h2 style="font-size:20px;line-height:1.25;margin:0 0 10px;color:#003462;">Chapter Presentations</h2><p style="margin:0 0 10px;">Each day opens with a short PowerPoint presentation covering that chapter's key concepts &mdash; a quick overview before you move into the reading and Hands-On exercises.</p><p style="margin:0;"><strong>Where to find them:</strong> embedded right at the top of each day's module, so you'll see the current chapter's presentation as soon as you start that day. If you want to review an earlier chapter's slides or look ahead, every presentation is also organized in <strong>Files &rsaquo; Presentations</strong>.</p></div><div style="border-left:5px solid #B5E3F0;background:#FFFFFF;border-top:1px solid #CBD5E1;border-right:1px solid #CBD5E1;border-bottom:1px solid #CBD5E1;border-radius:4px;padding:16px 18px;margin:14px 0;"><h2 style="font-size:20px;line-height:1.25;margin:0 0 10px;color:#003462;">eLab Self-Paced Practice</h2><p style="margin:0 0 10px;">Each chapter includes an eLab Self-Paced Practice link &mdash; an interactive WebSim environment where you can practice that chapter's Outlook skills at your own pace, without touching your real mailbox. Use it before a Hands-On exercise for a low-stakes trial run, or after to reinforce what you've learned.</p><p style="margin:0;"><strong>Where to find it:</strong> embedded in each day's module, usually right before that chapter's Quiz/Test items &mdash; look for the link titled <strong>&ldquo;eLab: Chapter X Self-Paced Practice.&rdquo;</strong></p></div><div style="background:#F5F7FA;border-left:5px solid #FFCF01;border-radius:4px;padding:16px 18px;margin:14px 0;"><h2 style="font-size:18px;line-height:1.25;margin:0 0 10px;color:#003462;">Quick Reference: Where Is Everything?</h2><table style="width:100%;border-collapse:collapse;background:white;table-layout:auto;"><tbody><tr><th style="text-align:left;color:#003462;border-bottom:2px solid #00B7A3;padding:8px 10px;">Resource</th><th style="text-align:left;color:#003462;border-bottom:2px solid #00B7A3;padding:8px 10px;">Find it</th></tr><tr><td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">A chapter's presentation</td><td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Top of that day's module (fastest) &mdash; or <strong>Files &rsaquo; Presentations</strong> to browse all 5</td></tr><tr><td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">A chapter's eLab Self-Paced Practice</td><td style="vertical-align:top;border-bottom:1px solid #E5E7EB;padding:8px 10px;">Within that day's module, right before the chapter's Quiz/Test</td></tr></tbody></table></div></div>"""

COURSE_MAP_ANCHOR = '</table></div><div style="border-left:5px solid #B5E3F0;background:#FFFFFF;border-top:1px solid #CBD5E1;border-right:1px solid #CBD5E1;border-bottom:1px solid #CBD5E1;border-radius:4px;padding:16px 18px;margin:14px 0;"><h2 style="font-size:20px;line-height:1.25;margin:0 0 10px;color:#003462;">How Classes Are Taught</h2>'

CLASS_RESOURCES_SECTION = '</table></div><div style="border-left:5px solid #00B7A3;background:#FFFFFF;border-top:1px solid #CBD5E1;border-right:1px solid #CBD5E1;border-bottom:1px solid #CBD5E1;border-radius:4px;padding:16px 18px;margin:14px 0;"><h2 style="font-size:20px;line-height:1.25;margin:0 0 10px;color:#003462;">Class Resources</h2><p style="margin:0 0 10px;">This course uses chapter Presentations and eLab Self-Paced Practice throughout &mdash; see the <a href="https://adultedventura.instructure.com/courses/454/pages/how-to-use-class-resources" style="color:#003462;">How to Use Class Resources</a> page (right after this one in the modules list) for what each is and exactly where to find it.</p><p style="margin:0;">Every chapter presentation is also organized in <a href="https://adultedventura.instructure.com/courses/454/files" style="color:#003462;">Files &rsaquo; Presentations</a> if you want to browse or review ahead.</p></div><div style="border-left:5px solid #B5E3F0;background:#FFFFFF;border-top:1px solid #CBD5E1;border-right:1px solid #CBD5E1;border-bottom:1px solid #CBD5E1;border-radius:4px;padding:16px 18px;margin:14px 0;"><h2 style="font-size:20px;line-height:1.25;margin:0 0 10px;color:#003462;">How Classes Are Taught</h2>'


def main():
    dry_run = "--live" not in sys.argv

    # --- Step 1: Presentations folder + file moves ---
    print("=== Step 1: Files > Presentations ===")
    if dry_run:
        print(f"[DRY RUN] Would create folder 'Presentations' under {PRESENTATIONS_PARENT_FOLDER_ID}")
        print(f"[DRY RUN] Would move files {PPT_FILE_IDS} into it")
    else:
        r = requests.post(
            f"{BASE_URL}/courses/{COURSE_ID}/folders",
            headers=HEADERS,
            data={"name": "Presentations", "parent_folder_id": PRESENTATIONS_PARENT_FOLDER_ID},
        )
        r.raise_for_status()
        folder_id = r.json()["id"]
        print(f"Created folder Presentations (id {folder_id})")
        for fid in PPT_FILE_IDS:
            r = requests.put(
                f"{BASE_URL}/files/{fid}",
                headers=HEADERS,
                data={"parent_folder_id": folder_id},
            )
            r.raise_for_status()
            print(f"  Moved file {fid} -> folder {folder_id} (now folder_id={r.json().get('folder_id')})")

    # --- Step 2: Resources page ---
    print("\n=== Step 2: How to Use Class Resources page ===")
    if dry_run:
        print("[DRY RUN] Would create page 'How to Use Class Resources'")
    else:
        r = requests.post(
            f"{BASE_URL}/courses/{COURSE_ID}/pages",
            headers=HEADERS,
            data={
                "wiki_page[title]": "How to Use Class Resources",
                "wiki_page[body]": RESOURCES_PAGE_BODY,
                "wiki_page[published]": "false",
            },
        )
        r.raise_for_status()
        page_url = r.json()["url"]
        print(f"Created page: {page_url}")

    # --- Step 3: Module at position 2 ---
    print("\n=== Step 3: How to Use Class Resources module (position 2) ===")
    if dry_run:
        print("[DRY RUN] Would create module 'How to Use Class Resources' at position 2")
        print("[DRY RUN] Would add the page as its one item")
    else:
        r = requests.post(
            f"{BASE_URL}/courses/{COURSE_ID}/modules",
            headers=HEADERS,
            data={"module[name]": "How to Use Class Resources", "module[position]": 2},
        )
        r.raise_for_status()
        module_id = r.json()["id"]
        print(f"Created module {module_id} at position {r.json()['position']}")

        r = requests.post(
            f"{BASE_URL}/courses/{COURSE_ID}/modules/{module_id}/items",
            headers=HEADERS,
            data={
                "module_item[title]": "How to Use Class Resources",
                "module_item[type]": "Page",
                "module_item[page_url]": page_url,
                "module_item[position]": 1,
            },
        )
        r.raise_for_status()
        print(f"Added page item to module {module_id}")

    # --- Step 4: Course Overview page section insert ---
    print("\n=== Step 4: Course Overview 'Class Resources' section ===")
    welcome = requests.get(
        f"{BASE_URL}/courses/{COURSE_ID}/pages/microsoft-outlook-welcome", headers=HEADERS
    ).json()
    body = welcome["body"]
    count = body.count(COURSE_MAP_ANCHOR)
    print(f"Anchor match count: {count}")
    if count != 1:
        print("ABORT: anchor did not match exactly once, refusing to edit.")
        sys.exit(1)
    new_body = body.replace(COURSE_MAP_ANCHOR, CLASS_RESOURCES_SECTION)
    if dry_run:
        print("[DRY RUN] Would PUT updated welcome page body (anchor validated OK)")
    else:
        r = requests.put(
            f"{BASE_URL}/courses/{COURSE_ID}/pages/microsoft-outlook-welcome",
            headers=HEADERS,
            data={"wiki_page[body]": new_body},
        )
        r.raise_for_status()
        print("Updated Course Overview page.")

    print("\nDone." if not dry_run else "\nDry run complete -- pass --live to execute.")


if __name__ == "__main__":
    main()
