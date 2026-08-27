"""
extract_solution_images.py
---------------------------
Extracts per-exercise solution screenshots from the Computer Basics
"Printable Solutions Guide" PDF for use as collapsible "Example of a
Completed Submission" sections on Hands-On/Skill Builder Canvas items.

The guide has one heading per exercise ("HO x.y ..." / "SB x.y ...") and,
for most exercises, one embedded screenshot right after it. Some exercises
have no screenshot at all (results-dependent, or a text-only deliverable) --
the guide says so explicitly ("There is no screenshot for this exercise."),
and this script correctly produces no image for those; don't force one.

Usage:
  python scripts/extract_solution_images.py              # index + extract all chapters
  python scripts/extract_solution_images.py --chapters 7,8,9,10
  python scripts/extract_solution_images.py --index-only # just print what's available, don't extract

Output: PNGs saved to
  <course source root>/Answer Keys/Extracted Solutions/Chapter N/{HO|SB} X.Y.png
at 300 DPI, cropped from a full-page render (not the PDF's raw low-res
embedded stream) so they stay sharp.
"""
import argparse
import json
import os
import re

import pdfplumber
import pypdfium2 as pdfium

SRC_ROOT = r"C:\Users\jball.VACE\Documents\VACE DOCS\Business Program\Class Components\Microsoft Lab Learning\Intro Into Computer Basics Windows 11 Edition"
PDF_PATH = SRC_ROOT + r"\Answer Keys\WTCB11_Printable_Solutions_Guide.pdf"
EXTRACT_ROOT = SRC_ROOT + r"\Answer Keys\Extracted Solutions"

HEADING_RE = re.compile(r"^(HO|SB) (\d+)\.(\d+) ")
DPI = 300


def build_index(pdf_path=PDF_PATH):
    """Returns a list of {kind, chapter, num, page, title_line, has_image, bbox}
    for every HO/SB exercise heading found in the guide."""
    index = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            words = page.extract_words()
            lines = {}
            for w in words:
                lines.setdefault(round(w["top"]), []).append(w)
            line_items = []
            for top in sorted(lines.keys()):
                ws = sorted(lines[top], key=lambda w: w["x0"])
                line_items.append((top, " ".join(w["text"] for w in ws)))

            headings = []
            for top, text in line_items:
                m = HEADING_RE.match(text)
                if m:
                    headings.append({
                        "top": top, "kind": m.group(1),
                        "chapter": int(m.group(2)), "num": int(m.group(3)),
                        "title_line": text,
                    })
            if not headings:
                continue

            for i, h in enumerate(headings):
                y_start = h["top"]
                y_end = headings[i + 1]["top"] if i + 1 < len(headings) else page.height
                best = None
                for im in page.images:
                    if y_start - 2 <= im["top"] < y_end:
                        best = im
                        break
                index.append({
                    "kind": h["kind"], "chapter": h["chapter"], "num": h["num"],
                    "page": page_num, "title_line": h["title_line"],
                    "has_image": best is not None,
                    "bbox": {k: best[k] for k in ("x0", "x1", "top", "bottom")} if best else None,
                })
    return index


def extract_images(index, chapters=None):
    """Crops and saves the PNG for every index entry with has_image=True
    (optionally filtered to a set of chapter numbers). Returns a list of
    {kind, chapter, num, filename, path} for what was written."""
    pdf = pdfium.PdfDocument(PDF_PATH)
    scale = DPI / 72.0
    page_cache = {}

    def render(page_num):
        if page_num not in page_cache:
            page_cache[page_num] = pdf[page_num].render(scale=scale).to_pil()
        return page_cache[page_num]

    written = []
    for e in index:
        if not e["has_image"]:
            continue
        if chapters is not None and e["chapter"] not in chapters:
            continue
        fname = f"{e['kind']} {e['chapter']}.{e['num']}.png"
        out_dir = os.path.join(EXTRACT_ROOT, f"Chapter {e['chapter']}")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, fname)

        img = render(e["page"])
        b = e["bbox"]
        crop = img.crop((int(b["x0"] * scale), int(b["top"] * scale),
                          int(b["x1"] * scale), int(b["bottom"] * scale)))
        crop.save(out_path)
        written.append({"kind": e["kind"], "chapter": e["chapter"], "num": e["num"],
                         "filename": fname, "path": out_path})
    return written


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapters", help="Comma-separated chapter numbers to extract (default: all)")
    parser.add_argument("--index-only", action="store_true", help="Print the index without extracting images")
    args = parser.parse_args()

    chapters = {int(c) for c in args.chapters.split(",")} if args.chapters else None

    index = build_index()
    print(f"Found {len(index)} exercises in the guide "
          f"({sum(1 for e in index if e['has_image'])} with a screenshot, "
          f"{sum(1 for e in index if not e['has_image'])} without).")

    if chapters:
        index = [e for e in index if e["chapter"] in chapters]
        print(f"Filtered to chapters {sorted(chapters)}: {len(index)} exercises.")

    for e in index:
        print(f"  {e['kind']} {e['chapter']}.{e['num']:<3} page {e['page']:<3} "
              f"{'HAS IMAGE' if e['has_image'] else 'no screenshot'}  ({e['title_line']})")

    if args.index_only:
        return

    written = extract_images(index, chapters=chapters)
    print(f"\nExtracted {len(written)} images to {EXTRACT_ROOT}")


if __name__ == "__main__":
    main()
