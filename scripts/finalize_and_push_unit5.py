# -*- coding: utf-8 -*-
"""Finalizes Day 11's worksheet PENDING_CANVAS_UPLOAD placeholders with real
Canvas file URLs, then pushes Day 9, 10, and 11 (Unit 5: Percent) into the
live Business Math course (456) via push_course.push_template().

Day 9 and Day 10 have no file uploads (all reading pages + native Canvas
practice_quiz self-checks) so their fragment JSON is pushed as-is. Day 11's
4 worksheet PDFs (already generated locally by build_business_math_unit5_
day11.py) are uploaded here, and its fragment JSON is rewritten in place
with the real download URLs before being pushed.

This completes the full Business Math course build: Course Overview +
Days 1-11 spanning Units 1-5.
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from push_course import upload_file_to_canvas, push_template, SITE_ROOT, api_get

COURSE_ID = 456
FRAGMENT_DIR = r"C:\Users\jball.VACE\Documents\Claude Projects\Master Business Finance Program\Lesson Planning\Business Math"
WORKSHEET_DIR = r"C:\Users\jball.VACE\Documents\Claude Projects\Claude Run Canvas\generated_worksheets"

DAY11_FILES = {
    "Worksheet 52": ("Worksheet-52-Discount-and-Markup.pdf", "Worksheet-52-Answer-Key.pdf"),
    "Worksheet 53": ("Worksheet-53-Calculate-Interest.pdf", "Worksheet-53-Answer-Key.pdf"),
    "Worksheet 56": ("Worksheet-56-Percent-of-Increase-and-Decrease.pdf", "Worksheet-56-Answer-Key.pdf"),
    "Percent Review": ("Percent-Review.pdf", "Percent-Review-Answer-Key.pdf"),
}

_url_cache = {}


def upload_and_get_url(filename):
    if filename in _url_cache:
        return _url_cache[filename]
    local_path = os.path.join(WORKSHEET_DIR, filename)
    if not os.path.exists(local_path):
        raise RuntimeError(f"Local worksheet PDF not found: {local_path}")
    f = upload_file_to_canvas(COURSE_ID, local_path, filename)
    if not f:
        raise RuntimeError(f"Failed to upload {filename}")
    url = f"{SITE_ROOT}/files/{f['id']}/download?download_frd=1&verifier={f.get('uuid', '')}"
    print(f"  uploaded {filename} -> file id {f['id']}")
    _url_cache[filename] = url
    return url


def finalize_fragment(day_num, file_map):
    path = os.path.join(FRAGMENT_DIR, f"day{day_num}-module-fragment.json")
    with open(path, "r", encoding="utf-8") as fh:
        fragment = json.load(fh)

    for item in fragment["modules"][0]["items"]:
        if item.get("type") != "assignment":
            continue
        title = item["title"]
        match = next((k for k in file_map if k in title), None)
        if not match:
            continue
        ws_file, ans_file = file_map[match]
        ws_url = upload_and_get_url(ws_file)
        ans_url = upload_and_get_url(ans_file)
        desc = item["description"]
        if desc.count("PENDING_CANVAS_UPLOAD") != 2:
            raise RuntimeError(f"Expected 2 placeholders in '{title}', found {desc.count('PENDING_CANVAS_UPLOAD')}")
        desc = desc.replace("PENDING_CANVAS_UPLOAD", ws_url, 1)
        desc = desc.replace("PENDING_CANVAS_UPLOAD", ans_url, 1)
        item["description"] = desc
        print(f"  finalized: {title}")

    with open(path, "w", encoding="utf-8") as fh:
        json.dump(fragment, fh, indent=2, ensure_ascii=False)
    print(f"Rewrote {path} with real Canvas URLs.\n")


def main():
    print("=== Verifying live module list before push ===")
    mods_before = api_get(f"/courses/{COURSE_ID}/modules")
    for m in sorted(mods_before, key=lambda x: x.get("position", 0)):
        print(m["position"], m["id"], m["name"])
    print(f"({len(mods_before)} modules before push)\n")

    print("=== Uploading Day 11 worksheets ===")
    finalize_fragment(11, DAY11_FILES)

    print("=== Pushing Day 9 ===")
    push_template(os.path.join(FRAGMENT_DIR, "day9-module-fragment.json"), COURSE_ID, dry_run=False)
    print("=== Pushing Day 10 ===")
    push_template(os.path.join(FRAGMENT_DIR, "day10-module-fragment.json"), COURSE_ID, dry_run=False)
    print("=== Pushing Day 11 ===")
    push_template(os.path.join(FRAGMENT_DIR, "day11-module-fragment.json"), COURSE_ID, dry_run=False)

    print("\n=== Verifying live module list after push ===")
    mods_after = api_get(f"/courses/{COURSE_ID}/modules")
    for m in sorted(mods_after, key=lambda x: x.get("position", 0)):
        print(m["position"], m["id"], m["name"])
    print(f"({len(mods_after)} modules after push)")

    before_ids = {m["id"] for m in mods_before}
    after_ids = {m["id"] for m in mods_after}
    added = after_ids - before_ids
    removed = before_ids - after_ids
    print(f"\nAdded module ids: {added}")
    print(f"Removed module ids: {removed}")
    if removed:
        print("WARNING: modules were removed by this push -- investigate before proceeding!")
    if len(added) != 3:
        print(f"WARNING: expected exactly 3 new modules (Days 9, 10, 11), got {len(added)}")


if __name__ == "__main__":
    main()
