"""
push_course.py
--------------
Reads a template JSON file and pushes it to a Canvas course.
Creates modules, pages, and assignments from the template definition.

Usage:
  python scripts/push_course.py --template templates/business-and-finance.json --course 301

Arguments:
  --template   Path to the template JSON file (relative to project root)
  --course     Canvas course ID to push into (use sandbox ID for testing)
  --dry-run    Print what would be created without actually calling the API
"""

import os
import sys
import json
import argparse
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("CANVAS_API_TOKEN")
BASE_URL = os.getenv("CANVAS_BASE_URL")

if not TOKEN:
    print("ERROR: CANVAS_API_TOKEN is missing from your .env file.")
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": "claude-run-canvas/1.0 (Ventura Adult and Continuing Education)"
}


def api_post(endpoint, data, dry_run=False):
    """POST to Canvas API. Returns response JSON or a fake dict in dry-run mode."""
    url = f"{BASE_URL}{endpoint}"
    if dry_run:
        print(f"  [DRY RUN] POST {endpoint}")
        return {"id": 9999, "url": "dry-run"}
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code not in (200, 201):
        print(f"  ERROR {response.status_code}: {response.text[:200]}")
        return None
    return response.json()


def create_module(course_id, module, dry_run=False):
    print(f"\nCreating module: {module['name']}")
    result = api_post(
        f"/courses/{course_id}/modules",
        {"module": {"name": module["name"], "position": module["position"]}},
        dry_run=dry_run
    )
    return result.get("id") if result else None


def create_page(course_id, module_id, item, dry_run=False):
    print(f"  + Page: {item['title']}")
    page = api_post(
        f"/courses/{course_id}/pages",
        {"wiki_page": {"title": item["title"], "body": item.get("body", ""), "published": False}},
        dry_run=dry_run
    )
    if not page:
        return
    page_url = page.get("url") or page.get("id")
    # Add page to module
    api_post(
        f"/courses/{course_id}/modules/{module_id}/items",
        {"module_item": {"type": "Page", "page_url": page_url, "title": item["title"]}},
        dry_run=dry_run
    )


def create_assignment(course_id, module_id, item, dry_run=False):
    print(f"  + Assignment: {item['title']}")
    assignment = api_post(
        f"/courses/{course_id}/assignments",
        {"assignment": {
            "name": item["title"],
            "description": item.get("description", ""),
            "points_possible": item.get("points_possible", 0),
            "submission_types": item.get("submission_types", ["none"]),
            "published": False
        }},
        dry_run=dry_run
    )
    if not assignment:
        return
    assignment_id = assignment.get("id")
    # Add assignment to module
    api_post(
        f"/courses/{course_id}/modules/{module_id}/items",
        {"module_item": {"type": "Assignment", "content_id": assignment_id, "title": item["title"]}},
        dry_run=dry_run
    )


def push_template(template_path, course_id, dry_run=False):
    with open(template_path, "r", encoding="utf-8") as f:
        template = json.load(f)

    print(f"\nTemplate : {template.get('course_name')}")
    print(f"Target   : Course ID {course_id}")
    print(f"Modules  : {len(template.get('modules', []))}")
    if dry_run:
        print("Mode     : DRY RUN (nothing will be created)\n")
    else:
        print("Mode     : LIVE\n")

    for module in template.get("modules", []):
        module_id = create_module(course_id, module, dry_run=dry_run)
        if not module_id:
            print(f"  SKIPPING items — module creation failed.")
            continue

        for item in module.get("items", []):
            if item["type"] == "page":
                create_page(course_id, module_id, item, dry_run=dry_run)
            elif item["type"] == "assignment":
                create_assignment(course_id, module_id, item, dry_run=dry_run)
            else:
                print(f"  UNKNOWN item type: {item['type']} — skipping")

    print("\nDone.")


def main():
    parser = argparse.ArgumentParser(description="Push a course template to Canvas.")
    parser.add_argument("--template", required=True, help="Path to template JSON file")
    parser.add_argument("--course", required=True, type=int, help="Canvas course ID")
    parser.add_argument("--dry-run", action="store_true", help="Preview without making API calls")
    args = parser.parse_args()

    if not os.path.exists(args.template):
        print(f"ERROR: Template file not found: {args.template}")
        sys.exit(1)

    push_template(args.template, args.course, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
