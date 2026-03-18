"""
list_courses.py
---------------
Pulls all courses from the Canvas account and prints a summary.
Handles pagination so it returns ALL courses, not just the first page.
Run with: python scripts/list_courses.py
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("CANVAS_API_TOKEN")
BASE_URL = os.getenv("CANVAS_BASE_URL")

if not TOKEN:
    print("ERROR: CANVAS_API_TOKEN is missing from your .env file.")
    exit(1)

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": "claude-run-canvas/1.0 (Ventura Adult and Continuing Education)"
}

def get_all_pages(url, params=None):
    """Fetch all pages of a paginated Canvas API endpoint."""
    results = []
    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"ERROR: {response.status_code} -- {response.text}")
            break
        results.extend(response.json())
        # Canvas puts the next page URL in the Link header
        url = None
        params = None  # params only needed on first request
        link_header = response.headers.get("Link", "")
        for part in link_header.split(","):
            if 'rel="next"' in part:
                url = part.split(";")[0].strip().strip("<>")
    return results

def list_courses():
    print("Fetching courses...\n")

    courses = get_all_pages(
        f"{BASE_URL}/accounts/1/courses",
        params={
            "per_page": 100,
            "include[]": "total_students"
        }
    )

    if not courses:
        print("No courses found.")
        return

    # Sort by name
    courses.sort(key=lambda c: c.get("name", "").lower())

    print(f"{'ID':<10} {'WORKFLOW':<12} {'STUDENTS':<10} COURSE NAME")
    print("-" * 70)
    for course in courses:
        cid = course.get("id", "")
        name = course.get("name", "(no name)")
        workflow = course.get("workflow_state", "")
        students = course.get("total_students", "-")
        print(f"{cid:<10} {workflow:<12} {str(students):<10} {name}")

    print(f"\nTotal: {len(courses)} courses")

if __name__ == "__main__":
    list_courses()
