import os, requests
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("CANVAS_API_TOKEN")
BASE_URL = os.getenv("CANVAS_BASE_URL")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "User-Agent": "claude-run-canvas/1.0"}
COURSE_ID = 454

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

modules = get_all_pages(f"{BASE_URL}/courses/{COURSE_ID}/modules", params={"per_page": 100})
for m in modules:
    print(f"\n=== {m['name']} (id {m['id']}, pos {m['position']}) ===")
    items = get_all_pages(f"{BASE_URL}/courses/{COURSE_ID}/modules/{m['id']}/items", params={"per_page": 100})
    for it in items:
        print(f"  [{it['position']}] {it['type']}: {it['title']}")
