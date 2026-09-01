# -*- coding: utf-8 -*-
"""Post-push verification for Business Math Days 9-11 (Unit 5: Percent) in
live course 456. Checks: every quiz's real question count/points via the
/quizzes/:id/questions endpoint (the quiz object's own aggregate fields go
stale per project memory), and that worksheet PDF files serve real bytes."""
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from push_course import api_get, SITE_ROOT, HEADERS

COURSE_ID = 456
NEW_MODULE_IDS = [2099, 2100, 2101]


def check_quizzes():
    print("=== Quiz verification (via /quizzes/:id/questions, not stale aggregate fields) ===")
    issues = []
    for mid in NEW_MODULE_IDS:
        items = api_get(f"/courses/{COURSE_ID}/modules/{mid}/items")
        for it in items:
            if it.get("type") != "Quiz":
                continue
            quiz_id = it["content_id"]
            title = it["title"]
            questions = api_get(f"/courses/{COURSE_ID}/quizzes/{quiz_id}/questions")
            n = len(questions)
            total_pts = sum(q.get("points_possible", 0) or 0 for q in questions)
            zero_pt = [q["id"] for q in questions if not q.get("points_possible")]
            status = "OK"
            if n == 0:
                status = "EMPTY -- NO QUESTIONS"
                issues.append(f"{title}: no questions found")
            if zero_pt:
                status = f"WARNING: {len(zero_pt)} zero-point questions"
                issues.append(f"{title}: {len(zero_pt)} zero-point questions (ids {zero_pt})")
            print(f"  [{status}] {title}: {n} questions, {total_pts} total pts")
    return issues


def check_worksheet_files():
    print("\n=== Worksheet file verification (real bytes, correct size) ===")
    issues = []
    mid = 2101  # Day 11
    items = api_get(f"/courses/{COURSE_ID}/modules/{mid}/items")
    for it in items:
        if it.get("type") != "Assignment":
            continue
        assignment_id = it["content_id"]
        a = api_get(f"/courses/{COURSE_ID}/assignments/{assignment_id}")
        desc = a.get("description", "")
        import re
        urls = re.findall(r'href="([^"]+/files/\d+/download[^"]*)"', desc)
        for url in urls:
            req = urllib.request.Request(url, headers=HEADERS)
            try:
                with urllib.request.urlopen(req, timeout=20) as resp:
                    data = resp.read()
                size = len(data)
                is_pdf = data[:4] == b"%PDF"
                status = "OK" if is_pdf and size > 500 else "SUSPECT"
                if status != "OK":
                    issues.append(f"{it['title']}: {url} -> size={size} is_pdf={is_pdf}")
                print(f"  [{status}] {it['title']}: {size} bytes, PDF magic={is_pdf}")
            except Exception as e:
                issues.append(f"{it['title']}: {url} -> ERROR {e}")
                print(f"  [ERROR] {it['title']}: {url} -> {e}")
    return issues


def main():
    all_issues = []
    all_issues += check_quizzes()
    all_issues += check_worksheet_files()
    print("\n=== Summary ===")
    if all_issues:
        print(f"{len(all_issues)} issue(s) found:")
        for i in all_issues:
            print(" -", i)
    else:
        print("No issues found. All quizzes have real questions/points, all worksheet files serve real PDF bytes.")


if __name__ == "__main__":
    main()
