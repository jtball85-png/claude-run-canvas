"""
push_course.py
--------------
Reads a template JSON file and pushes it to a Canvas course.
Creates modules, pages, assignments, discussions, and quizzes from the template.

Usage:
  python scripts/push_course.py --template templates/business-and-finance.json --course 301
  python scripts/push_course.py --template templates/business-and-finance.json --course 301 --dry-run
  python scripts/push_course.py --template templates/business-and-finance.json --course 301 --clear-first

Arguments:
  --template      Path to the template JSON file (relative to project root)
  --course        Canvas course ID to push into (use sandbox ID for testing)
  --dry-run       Print what would be created without actually calling the API
  --clear-first   Delete all existing modules from the course before pushing
"""

import os
import re
import sys
import json
import argparse
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("CANVAS_API_TOKEN")
BASE_URL = os.getenv("CANVAS_BASE_URL")
SITE_ROOT = BASE_URL.removesuffix("/api/v1") if BASE_URL else None

if not TOKEN:
    print("ERROR: CANVAS_API_TOKEN is missing from your .env file.")
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": "claude-run-canvas/1.0 (Ventura Adult and Continuing Education)"
}


# ---------------------------------------------------------------------------
# Core API helpers
# ---------------------------------------------------------------------------

def api_get(endpoint, params=None):
    """GET from Canvas API, returns list (handles pagination)."""
    results = []
    url = f"{BASE_URL}{endpoint}"
    while url:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"  ERROR {response.status_code}: {response.text[:200]}")
            return results
        data = response.json()
        if isinstance(data, list):
            results.extend(data)
        else:
            return data  # single object response
        url = None
        params = None
        for part in response.headers.get("Link", "").split(","):
            if 'rel="next"' in part:
                url = part.split(";")[0].strip().strip("<>")
    return results


def api_post(endpoint, data, dry_run=False):
    """POST to Canvas API. Returns response JSON or a fake dict in dry-run mode."""
    if dry_run:
        print(f"  [DRY RUN] POST {endpoint}")
        return {"id": 9999, "url": "dry-run"}
    response = requests.post(f"{BASE_URL}{endpoint}", headers=HEADERS, json=data)
    if response.status_code not in (200, 201):
        print(f"  ERROR {response.status_code}: {response.text[:200]}")
        return None
    return response.json()


def api_delete(endpoint, dry_run=False):
    """DELETE from Canvas API."""
    if dry_run:
        print(f"  [DRY RUN] DELETE {endpoint}")
        return True
    response = requests.delete(f"{BASE_URL}{endpoint}", headers=HEADERS)
    return response.status_code in (200, 204)


# ---------------------------------------------------------------------------
# Clear existing modules
# ---------------------------------------------------------------------------

def clear_modules(course_id, dry_run=False):
    print(f"Clearing existing modules from course {course_id}...")
    modules = api_get(f"/courses/{course_id}/modules", params={"per_page": 100})
    if not modules:
        print("  No existing modules found.")
        return
    for module in modules:
        print(f"  Deleting: {module['name']}")
        api_delete(f"/courses/{course_id}/modules/{module['id']}", dry_run=dry_run)
    print(f"  Cleared {len(modules)} module(s).\n")


# ---------------------------------------------------------------------------
# Item creators
# ---------------------------------------------------------------------------

def create_module(course_id, module, dry_run=False):
    print(f"\nCreating module: {module['name']}")
    result = api_post(
        f"/courses/{course_id}/modules",
        {"module": {"name": module["name"], "position": module["position"]}},
        dry_run=dry_run
    )
    return result.get("id") if result else None


def add_to_module(course_id, module_id, item_type, content_id=None, page_url=None, title="", dry_run=False):
    """Add any item type to a module."""
    payload = {"module_item": {"type": item_type, "title": title}}
    if content_id:
        payload["module_item"]["content_id"] = content_id
    if page_url:
        payload["module_item"]["page_url"] = page_url
    api_post(f"/courses/{course_id}/modules/{module_id}/items", payload, dry_run=dry_run)


def create_page(course_id, module_id, item, dry_run=False):
    print(f"  + Page: {item['title']}")
    body = resolve_image_placeholders(course_id, item.get("body", ""), item.get("images", {}), dry_run=dry_run)
    page = api_post(
        f"/courses/{course_id}/pages",
        {"wiki_page": {"title": item["title"], "body": body, "published": False}},
        dry_run=dry_run
    )
    if not page:
        return
    add_to_module(course_id, module_id, "Page",
                  page_url=page.get("url") or "dry-run",
                  title=item["title"], dry_run=dry_run)


def create_assignment(course_id, module_id, item, dry_run=False):
    print(f"  + Assignment: {item['title']}")
    description = resolve_image_placeholders(course_id, item.get("description", ""), item.get("images", {}), dry_run=dry_run)
    assignment = api_post(
        f"/courses/{course_id}/assignments",
        {"assignment": {
            "name": item["title"],
            "description": description,
            "points_possible": item.get("points_possible", 0),
            "submission_types": item.get("submission_types", ["none"]),
            "published": False
        }},
        dry_run=dry_run
    )
    if not assignment:
        return
    add_to_module(course_id, module_id, "Assignment",
                  content_id=assignment.get("id"),
                  title=item["title"], dry_run=dry_run)


def create_discussion(course_id, module_id, item, dry_run=False):
    print(f"  + Discussion: {item['title']}")
    discussion = api_post(
        f"/courses/{course_id}/discussion_topics",
        {"title": item["title"],
         "message": item.get("message", ""),
         "require_initial_post": item.get("requires_initial_post", False),
         "published": False},
        dry_run=dry_run
    )
    if not discussion:
        return
    add_to_module(course_id, module_id, "Discussion",
                  content_id=discussion.get("id"),
                  title=item["title"], dry_run=dry_run)


def upload_file_to_canvas(course_id, local_path, display_name, parent_folder_path="course files"):
    """Runs Canvas's 3-step file upload (preflight -> binary upload -> confirm)
    and returns the resulting file object dict, or None on failure. Shared by
    create_file() (module File items) and upload_image() (inline embeds) --
    the upload mechanic is identical, only what's done with the result differs."""
    if not local_path or not os.path.exists(local_path):
        print(f"  ERROR: file not found: {local_path}")
        return None

    file_size = os.path.getsize(local_path)

    preflight = requests.post(
        f"{BASE_URL}/courses/{course_id}/files",
        headers=HEADERS,
        data={"name": display_name, "size": file_size, "parent_folder_path": parent_folder_path}
    )
    if preflight.status_code not in (200, 201):
        print(f"  ERROR {preflight.status_code}: {preflight.text[:200]}")
        return None
    preflight_data = preflight.json()
    upload_url = preflight_data["upload_url"]
    upload_params = preflight_data["upload_params"]

    with open(local_path, "rb") as f:
        upload_response = requests.post(
            upload_url,
            data=upload_params,
            files={"file": (display_name, f)},
            allow_redirects=False
        )

    if upload_response.status_code in (200, 201):
        file_obj = upload_response.json()
    elif upload_response.status_code in (301, 302, 303):
        location = upload_response.headers.get("Location")
        confirm = requests.get(location, headers=HEADERS)
        if confirm.status_code not in (200, 201):
            print(f"  ERROR confirming upload {confirm.status_code}: {confirm.text[:200]}")
            return None
        file_obj = confirm.json()
    else:
        print(f"  ERROR {upload_response.status_code} uploading file: {upload_response.text[:200]}")
        return None

    if not file_obj.get("id"):
        print(f"  ERROR: no file id returned: {file_obj}")
        return None
    return file_obj


def create_file(course_id, module_id, item, dry_run=False):
    """Upload a local file to Canvas course Files and add it to the module."""
    local_path = item.get("path")
    display_name = item.get("title") or os.path.basename(local_path or "")
    print(f"  + File: {display_name}")

    if dry_run:
        print(f"  [DRY RUN] POST /courses/{course_id}/files")
        add_to_module(course_id, module_id, "File", content_id=9999,
                      title=display_name, dry_run=dry_run)
        return

    file_obj = upload_file_to_canvas(course_id, local_path, display_name)
    if not file_obj:
        return

    add_to_module(course_id, module_id, "File", content_id=file_obj["id"],
                  title=display_name, dry_run=dry_run)


# ---------------------------------------------------------------------------
# Inline image embedding
# ---------------------------------------------------------------------------

IMG_PLACEHOLDER_RE = re.compile(r"\{\{img:([^|}]+)\|([^}]*)\}\}")


def upload_image(course_id, local_path, alt_text, parent_folder_path="course files/textbook-images"):
    """Uploads an image (via the same 3-step flow as create_file) and returns
    a ready-to-use <img> tag pointing at the file's direct download URL
    (the "url" field, which carries its own access verifier token and serves
    raw image bytes). NOTE: an earlier version of this function used
    "preview_url" instead -- that endpoint serves Canvas's interactive
    document-viewer widget (HTML, not raw image bytes) and does not render
    inline as an <img>. Confirmed broken in the sandbox (2026-08-24); "url"
    is the correct field for hotlinking a Canvas-hosted file as an image."""
    display_name = os.path.basename(local_path)
    file_obj = upload_file_to_canvas(course_id, local_path, display_name, parent_folder_path)
    if not file_obj:
        return f"<p><em>[image failed to upload: {display_name}]</em></p>"
    src = file_obj["url"]
    return f'<img src="{src}" alt="{alt_text}" style="max-width:100%;height:auto;">'


def resolve_image_placeholders(course_id, html, image_paths_by_filename, dry_run=False):
    """Replaces every {{img:filename|alt text}} placeholder in html with a
    real embedded <img> tag, uploading each referenced image (from
    image_paths_by_filename, a {filename: local_path} map) at most once even
    if it's placeholdered more than once in the same body."""
    if not html or "{{img:" not in html:
        return html

    uploaded_tags = {}

    def replace(match):
        filename, alt_text = match.group(1).strip(), match.group(2).strip()
        if filename in uploaded_tags:
            return uploaded_tags[filename]
        if dry_run:
            tag = f'<img src="[DRY RUN: {filename}]" alt="{alt_text}">'
        else:
            local_path = image_paths_by_filename.get(filename)
            if not local_path:
                print(f"  ERROR: no local path registered for image placeholder '{filename}'")
                tag = f"<p><em>[missing image reference: {filename}]</em></p>"
            else:
                print(f"    uploading image: {filename}")
                tag = upload_image(course_id, local_path, alt_text)
        uploaded_tags[filename] = tag
        return tag

    return IMG_PLACEHOLDER_RE.sub(replace, html)


def create_quiz(course_id, module_id, item, dry_run=False):
    print(f"  + Quiz: {item['title']}")
    quiz = api_post(
        f"/courses/{course_id}/quizzes",
        {"quiz": {
            "title": item["title"],
            "description": item.get("description", ""),
            "quiz_type": "assignment",
            "points_possible": item.get("points_possible", 0),
            "published": False
        }},
        dry_run=dry_run
    )
    if not quiz:
        return
    quiz_id = quiz.get("id")

    # Add questions
    for q in item.get("questions", []):
        answers = [
            {"answer_text": a["text"], "answer_weight": a["weight"]}
            for a in q.get("answers", [])
        ]
        api_post(
            f"/courses/{course_id}/quizzes/{quiz_id}/questions",
            {"question": {
                "question_type": q.get("question_type", "multiple_choice_question"),
                "question_text": q.get("question_text", ""),
                "answers": answers
            }},
            dry_run=dry_run
        )
        if not dry_run:
            print(f"    - Question: {q['question_text'][:60]}...")

    add_to_module(course_id, module_id, "Quiz",
                  content_id=quiz_id,
                  title=item["title"], dry_run=dry_run)


# ---------------------------------------------------------------------------
# Main push logic
# ---------------------------------------------------------------------------

ITEM_HANDLERS = {
    "page":       create_page,
    "assignment": create_assignment,
    "discussion": create_discussion,
    "quiz":       create_quiz,
    "file":       create_file,
}


def push_template(template_path, course_id, dry_run=False, clear_first=False):
    with open(template_path, "r", encoding="utf-8") as f:
        template = json.load(f)

    print(f"\nTemplate : {template.get('course_name')}")
    print(f"Target   : Course ID {course_id}")
    print(f"Modules  : {len(template.get('modules', []))}")
    print(f"Mode     : {'DRY RUN' if dry_run else 'LIVE'}\n")

    if clear_first:
        clear_modules(course_id, dry_run=dry_run)

    for module in template.get("modules", []):
        module_id = create_module(course_id, module, dry_run=dry_run)
        if not module_id:
            print("  SKIPPING items — module creation failed.")
            continue

        for item in module.get("items", []):
            item_type = item.get("type", "").lower()
            handler = ITEM_HANDLERS.get(item_type)
            if handler:
                handler(course_id, module_id, item, dry_run=dry_run)
            else:
                print(f"  UNKNOWN item type: {item.get('type')} — skipping")

    print("\nDone.")


def main():
    parser = argparse.ArgumentParser(description="Push a course template to Canvas.")
    parser.add_argument("--template", required=True, help="Path to template JSON file")
    parser.add_argument("--course", required=True, type=int, help="Canvas course ID")
    parser.add_argument("--dry-run", action="store_true", help="Preview without making API calls")
    parser.add_argument("--clear-first", action="store_true", help="Delete existing modules before pushing")
    args = parser.parse_args()

    if not os.path.exists(args.template):
        print(f"ERROR: Template file not found: {args.template}")
        sys.exit(1)

    push_template(args.template, args.course, dry_run=args.dry_run, clear_first=args.clear_first)


if __name__ == "__main__":
    main()
