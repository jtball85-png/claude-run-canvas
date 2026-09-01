# -*- coding: utf-8 -*-
"""Build Unit 5: Percent, Day 11 (module position 12) into a local module
fragment for the Business Math course.

Day 11 closes out Unit 5 (13 CBO objectives, split across Days 9-11) by
covering the two remaining objectives -- Solve multi-step percent problems
(taught by the book as TWO separate lessons: Part A Discount and Markup, and
Part B Percent of Increase and Decrease) and Calculate interest -- then the
book's own whole-unit Percent Review (self-paced), then an original graded
Unit 5 Quiz + Unit 5 Test. This is also the FINAL day of the entire
Business Math 11-content-day build. Mirrors Day 8's (Unit 4 close-out day)
pattern exactly.

Source: General Math Review: Basic Skills with Math (Howett & Eichhorn),
read directly from the real textbook pages by a research agent -- Practice
52 (Multi-Step Problems, Part A: Discount and Markup, pp.102-103), Practice
53 (Calculate Interest, pp.103-105), Practice 56 (Multi-Step Problems, Part
B: Percent of Increase and Decrease, pp.108-109), plus the book's own
"Percent Review" Progress Check (pp.112-113). Every worksheet problem and
review problem is transcribed verbatim from the book; every answer was
independently computed and double-checked. Quiz/Test questions are original
(not copied from the book), matching the Unit 1-4 precedent.

No videos are embedded on any Day 11 reading page: no Math Antics video
covers discount/markup, percent of increase/decrease, or interest as a
single dedicated topic. Khan Academy links are offered instead on the Want
More Practice page.

HARD RULE: this script does not import or call anything from
push_course.py and never touches Canvas or the network for Canvas
purposes. It only generates local PDFs (via worksheet_pdf.py's FPDF
classes) and writes a local JSON fragment file. Worksheet/Review
assignment descriptions use the literal placeholder string
"PENDING_CANVAS_UPLOAD" in place of a real Canvas file download URL,
since no live Canvas upload happens in this pass.
"""
import os
import json

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from worksheet_pdf import Worksheet, AnswerKey, OUTDIR

FRAGMENT_DIR = r"C:\Users\jball.VACE\Documents\Claude Projects\Master Business Finance Program\Lesson Planning\Business Math"
DAY11_POSITION = 12
UNIT5_LABEL = "Unit 5: Percent"
PLACEHOLDER = "PENDING_CANVAS_UPLOAD"

# ===========================================================================
# HTML helpers (identical design system to Unit 1-4's rebuild scripts --
# duplicated locally rather than imported, since this script must not import
# anything from other build scripts or push_course.py)
# ===========================================================================
WRAP_OPEN = '<div style="font-family:Arial,Helvetica,sans-serif;line-height:1.55;color:#1F2937;max-width:920px;margin:0 auto;">'
WRAP_CLOSE = '</div>'


def banner(eyebrow, title, subtitle):
    return (f'<div style="background:#003462;color:white;border-radius:4px;padding:20px 24px;margin:0 0 16px;">'
            f'<div style="font-size:12px;color:#FFCF01;">{eyebrow}</div>'
            f'<h1 style="margin:4px 0 4px;font-size:28px;line-height:1.15;color:white;">{title}</h1>'
            f'<div style="font-size:17px;line-height:1.35;color:#B5E3F0;">{subtitle}</div></div>')


def slim_header(label):
    return (f'<div style="background:#003462;color:white;border-radius:4px;padding:14px 20px;margin:0 0 16px;">'
            f'<div style="font-size:13px;letter-spacing:0.02em;color:#FFCF01;">{label}</div></div>')


def box(title, body_html, accent="teal"):
    color = "#00B7A3" if accent == "teal" else "#B5E3F0"
    h2 = f'<h2 style="font-size:20px;line-height:1.25;margin:0 0 10px;color:#003462;">{title}</h2>' if title else ""
    return (f'<div style="border-left:5px solid {color};background:#FFFFFF;border-top:1px solid #CBD5E1;'
            f'border-right:1px solid #CBD5E1;border-bottom:1px solid #CBD5E1;border-radius:4px;padding:16px 18px;margin:14px 0;">'
            f'{h2}{body_html}</div>')


def callout(label, text):
    return (f'<div style="background:#F5F7FA;border-left:5px solid #FFCF01;border-radius:4px;padding:12px 14px;margin:12px 0;">'
            f'<strong style="color:#003462;">{label}</strong><p style="margin:6px 0 0;">{text}</p></div>')


def meta_line(book_pages, cbo):
    return f'<p style="margin:0 0 10px;color:#003462;font-style:italic;font-size:13px;">Book pages: {book_pages} &middot; CBO Objective: {cbo}</p>'


def video_embed(video_id, title):
    return (f'<div style="margin:14px 0;"><div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;'
            f'border-radius:6px;border:1px solid #CBD5E1;"><iframe style="position:absolute;top:0;left:0;width:100%;height:100%;" '
            f'src="https://www.youtube.com/embed/{video_id}" title="{title}" allow="accelerometer; autoplay; clipboard-write; '
            f'encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe></div>'
            f'<p style="margin:6px 0 0;font-size:12px;color:#6B7280;">Video: <em>{title}</em> (Math Antics, YouTube)</p></div>')


def pdf_link(label, url):
    return (f'<a href="{url}" style="display:inline-block;background:#003462;color:white;padding:8px 14px;'
            f'border-radius:4px;text-decoration:none;font-size:14px;">{label}</a>')


def resource_list(items):
    lis = "".join(
        f'<li style="margin-bottom:10px;"><a href="{url}" style="color:#003462;font-weight:bold;">{title}</a>'
        f'<br><span style="font-size:13px;color:#4B5563;">{desc}</span></li>'
        for title, url, desc in items
    )
    return f'<ul style="margin:0;padding-left:20px;">{lis}</ul>'


def sa(text, weight=100):
    return {"text": text, "weight": weight}


def q_short(text, points, *answers):
    return {"question_type": "short_answer_question", "question_text": text, "points_possible": points,
            "answers": [sa(a) if isinstance(a, str) else sa(*a) for a in answers]}


def worksheet_description(ws_title, book_pages, day_label="Day 11 &middot; Unit 5 Worksheet"):
    return (
        WRAP_OPEN
        + banner(day_label, ws_title, f"Self-check practice &mdash; not graded. Book pages {book_pages}.")
        + box("", (
            '<p style="margin:0 0 12px;">This worksheet is a clean, printable PDF (typeset from the book\'s own problems) &mdash; '
            'print it, work it on paper with your calculator, then check the Answer Key below before moving on.</p>'
            f'{pdf_link("Download Worksheet (PDF)", PLACEHOLDER)}'
        ))
        + f'<details style="margin-top:14px;"><summary style="cursor:pointer;color:#003462;font-weight:bold;">Answer Key</summary>'
          f'<div style="margin-top:10px;">{pdf_link("Download Answer Key (PDF)", PLACEHOLDER)}</div></details>'
        + WRAP_CLOSE
    )


# ===========================================================================
# DAY 11 READING PAGES
# ===========================================================================

discount_markup_body = slim_header("Day 11 &middot; Unit 5 Reading") + meta_line("102-103", "Solve multi-step percent problems") + (
    '<h2>Multi-Step Problems, Part A: Discount and Markup</h2>'
    '<p>In some percent problems, you have to use two operations to find an answer. First find a percent of a number. Then add or '
    'subtract this new amount with the original amount in the problem.</p>'
    '<p><em>Example:</em> Dave bought a coat on sale. The coat used to cost $65. He bought it for 20% off the old price. How much '
    'did Dave pay for the coat?</p>'
    '<p><strong>Step 1.</strong> Change 20% to a fraction: 20% = 1/5.<br>'
    '<strong>Step 2.</strong> Multiply $65 by 1/5 = $13.<br>'
    '<strong>Step 3.</strong> Subtract $13 from $65 = $52.</p>'
    '<p>Dave paid <strong>$52</strong> for the coat.</p>'
    + box("Breaking It Down", (
        '<p style="margin:0;">This is a <strong>two-step</strong> problem: first find the percent-piece using last unit&rsquo;s '
        'skill (change the percent to a fraction or decimal, then multiply it by the original number). Then decide whether to '
        '<strong>add</strong> or <strong>subtract</strong> that piece from the original amount &mdash; it depends on whether the '
        'situation is a discount/markdown (subtract) or a markup/increase (add).</p>'
    ), accent="blue")
    + callout("Common Mistakes to Avoid", (
        'The most common error is stopping after step 1-2 and forgetting the add/subtract step &mdash; always re-read the question '
        'to confirm what final number is being asked for (the discounted price? the amount taken out? the new total?). Also, read '
        'carefully whether the situation calls for <strong>adding</strong> like a tax or markup, or <strong>subtracting</strong> '
        'like a discount &mdash; the wrong direction gives a completely wrong answer even when the percent math itself is correct.'
    ))
)

interest_body = slim_header("Day 11 &middot; Unit 5 Reading") + meta_line("103-105", "Calculate interest") + (
    '<h2>Calculate Interest</h2>'
    '<p>Interest is money someone pays for using someone else&rsquo;s money. A bank pays you interest for using your money in a '
    'savings account. You pay a bank interest for using the bank&rsquo;s money on a loan.</p>'
    '<p>To find interest, multiply the principal by the rate by the time.</p>'
    '<p>The principal is the money you borrow or save. The rate is the percent of the interest. The time is the number of years.</p>'
    '<p>When the time period for interest is not one year, change the time to a fraction of a year.</p>'
    '<p>When the time period is more than one year, write the time as a mixed number. For example, one year and six months = '
    '1 6/12 = 1 1/2.</p>'
    + box("Breaking It Down", (
        '<p style="margin:0 0 10px;">The rule uses three variables: <strong>principal</strong> (the money borrowed or saved), '
        '<strong>rate</strong> (the percent of interest), and <strong>time</strong> (the number of years). As an '
        'instructor-added memory aid, this is sometimes written as the formula <strong>I = P &times; R &times; T</strong> &mdash; '
        'though the textbook itself only states the rule in words, never that symbolic form.</p>'
        '<p style="margin:0;">The one new mechanical step this topic adds is converting a time period given in months into a '
        'fraction of a year: divide the number of months by 12 (months/12). Once you have principal, rate (as a decimal or '
        'fraction), and time (as a fraction or mixed number of years), multiply straight across.</p>'
    ), accent="blue")
    + '<p><em>Example:</em> Find the interest on $900 at 7% annual interest for one year.</p>'
    '<p>900 &times; 7/100 &times; 1 = <strong>$63</strong>.</p>'
    '<p><em>Example:</em> Find the interest on $900 at 7% annual interest for 8 months.</p>'
    '<p>7% = 7/100; 8 months = 8/12 = 2/3 of a year; 900 &times; 7/100 &times; 2/3 = <strong>$42</strong>.</p>'
    + box("A Bridging Example", (
        '<p style="margin:0 0 8px;"><em>Instructor-authored &mdash; Practice 53&rsquo;s second half jumps straight to harder '
        'combinations (a decimal rate together with a mixed-number time) without a matching worked example. Here&rsquo;s a '
        'bridge.</em></p>'
        '<p style="margin:0;">Find the interest on $1,200 at 4.5% annual interest for 1 year 4 months.<br>'
        '<strong>Step 1.</strong> 4.5% = .045.<br>'
        '<strong>Step 2.</strong> 1 year 4 months = 1 4/12 = 1 1/3 years (as a decimal, about 1.333).<br>'
        '<strong>Step 3.</strong> $1,200 &times; .045 &times; 1.333... = <strong>$72.00</strong>.</p>'
    ))
    + callout("Common Mistakes to Avoid", (
        'Always convert the rate to a decimal or fraction before multiplying &mdash; multiplying by &ldquo;7&rdquo; instead of '
        '&ldquo;.07&rdquo; (or 7/100) gives an answer 100 times too large. Also, money answers always carry two decimal places '
        '(for example, write &ldquo;$21.60&rdquo;, not &ldquo;$21.6&rdquo;).'
    ))
    + callout("A note on video", (
        'There is no dedicated Math Antics video for calculating interest, so none is embedded here. A Khan Academy simple '
        'interest resource is linked on the Want More Practice page if you&rsquo;d like extra practice.'
    ))
)

increase_decrease_body = slim_header("Day 11 &middot; Unit 5 Reading") + meta_line("108-109", "Solve multi-step percent problems") + (
    '<h2>Multi-Step Problems, Part B: Percent of Increase and Decrease</h2>'
    '<p>In some problems you have to compare the difference between two amounts to an original amount. First subtract to find the '
    'difference. Then make a fraction with the difference as the numerator and the original amount as the denominator. Change the '
    'fraction to a percent.</p>'
    '<p><em>Example:</em> Last year Jane paid $480 a month for rent. This year she pays $552 a month. By what percent did '
    'Jane&rsquo;s rent increase?</p>'
    '<p><strong>Step 1.</strong> $552 &minus; $480 = $72.<br>'
    '<strong>Step 2.</strong> 72/480 = 3/20.<br>'
    '<strong>Step 3.</strong> 3/20 &times; 100% = 15%.</p>'
    '<p>Jane&rsquo;s rent went up <strong>15%</strong>.</p>'
    + box("Breaking It Down", (
        '<p style="margin:0 0 8px;">Contrast this with Part A: Part A found a <strong>dollar amount</strong> (multiply a percent '
        'by the original, then add or subtract). Part B finds a <strong>percent</strong> (subtract first, then divide and convert '
        'to a percent) &mdash; the two skills share the &ldquo;multi-step problems&rdquo; name but are not the same operation.</p>'
        '<p style="margin:0;">The &ldquo;original amount&rdquo; (the denominator in step 2) is always the <strong>starting</strong> '
        'value &mdash; never the ending value &mdash; even when the problem describes a decrease.</p>'
    ), accent="blue")
    + callout("Common Mistakes to Avoid", (
        'Dividing by the wrong amount &mdash; using the new/ending amount as the denominator instead of the original/starting '
        'amount &mdash; is the single most common error on this skill. Always identify which number came <em>first</em> in time '
        'before you set up the fraction.'
    ))
)

day11_want_more_body = (
    WRAP_OPEN
    + banner("Day 11 &middot; Unit 5", "Want More Practice?", "Optional extra practice for today's skills.")
    + box("Percent &mdash; Multi-Step and Interest", resource_list([
        ("Khan Academy - Percent word problems: increase and decrease",
         "https://www.khanacademy.org/math/pre-algebra/pre-algebra-ratios-rates/pre-algebra-percent-word-problems/a/percent-word-problem-increase-and-decrease",
         "Percent of increase and decrease, discounts, and markups."),
        ("Khan Academy - Simple interest",
         "https://www.khanacademy.org/math/pre-algebra/pre-algebra-ratios-rates/pre-algebra-percent-word-problems/a/simple-interest",
         "Simple interest word problems, practiced online."),
    ]))
    + WRAP_CLOSE
)

DAY11_OVERVIEW_BODY = (
    WRAP_OPEN
    + banner("Day 11 &middot; Unit 5: Percent", "Day 11 Overview",
        "The final two objectives of Unit 5, then the book's own whole-unit review, quiz, and test that close out both "
        "Unit 5 and the entire Business Math course.")
    + box("Learning Objectives Covered Today", (
        '<ul style="margin:0;padding-left:20px;"><li>Solve multi-step percent problems (discount and markup)</li>'
        '<li>Calculate interest</li><li>Solve multi-step percent problems (percent of increase and decrease)</li></ul>'
    ))
    + callout("Two Skills, One Name", (
        'The book teaches &ldquo;Multi-Step Problems&rdquo; as <strong>two distinct skills</strong> that happen to share one '
        'name: <strong>Part A (Discount and Markup)</strong> finds a dollar amount, and <strong>Part B (Percent of Increase and '
        'Decrease)</strong> finds a percent. Don&rsquo;t let the shared name make you think they&rsquo;re the same thing &mdash; '
        'they use different final steps and answer different kinds of questions.'
    ))
    + box("How Today Works", (
        '<p style="margin:0 0 8px;">Each topic below is a short reading followed by a printable worksheet &mdash; the book&rsquo;s '
        'own practice problems, done on paper with your calculator. These worksheets are <strong>not graded</strong>; check your '
        'work against the Answer Key dropdown at the bottom of each one before moving to the next topic.</p>'
        '<p style="margin:0;">The day ends with the book&rsquo;s own <strong>Percent Review</strong> (a self-check with a '
        '&ldquo;which pages to review&rdquo; chart built in, covering all 13 objectives of Unit 5), then the graded '
        '<strong>Unit 5 Quiz</strong> and <strong>Unit 5 Test</strong>, which close out both Unit 5 and the full Business Math '
        'course.</p>'
    ), accent="blue")
    + box("Today&rsquo;s Tasks", (
        '<ol style="margin:0;padding-left:20px;"><li>Multi-Step Problems, Part A: Discount and Markup &mdash; read, then '
        'Worksheet 52</li><li>Calculate Interest &mdash; read, then Worksheet 53</li>'
        '<li>Multi-Step Problems, Part B: Percent of Increase and Decrease &mdash; read, then Worksheet 56</li>'
        '<li>Percent Review (self-check)</li><li>Unit 5 Quiz</li><li>Unit 5 Test</li></ol>'
    ))
    + WRAP_CLOSE
)

print("Day 11 reading pages built.")

# ===========================================================================
# WORKSHEET PDF GENERATION (Worksheets 52, 53, 56 + Percent Review),
# transcribed verbatim from the real Unit 5 textbook pages (Practice 52,
# pp.102-103; Practice 53, pp.103-105; Practice 56, pp.108-109; Review
# pp.112-113). All answers independently computed and double-checked against
# the transcribed problems.
# ===========================================================================


def generate_ws52():
    """Multi-Step Problems, Part A: Discount and Markup (Practice 52,
    pp.102-103) -- 5 word problems, numbered 1-5."""
    ws = Worksheet(52, "Discount and Markup", "102-103", unit_label=UNIT5_LABEL)
    ws.add_page()
    ws.name_date_line()
    ws.instructions("Solve each problem. Show your work.")
    pairs = []

    block1 = [
        (1, "Selma makes $560 a week. Her employer takes out 15% of her pay for taxes and Social Security. How much does "
            "Selma take home each week?"),
        (2, "Frank took a math test with 40 problems. He got 85% of the problems right. How many problems did he get wrong?"),
        (3, "Don bought tapes for $15.60. The sales tax in his state is 5%. How much did the tapes cost including sales tax?"),
        (4, "In June Petra's phone bill was $24.50. In July her bill was 30% more because of long distance calls. How much "
            "was her July phone bill?"),
        (5, "On a normal work day about 24,000 people ride the buses in Midvale. Monday was a holiday, and the number of "
            "riders was down 35%. How many people rode the buses on Monday?"),
    ]
    block1_answers = ["$476", "6", "$16.38", "$31.85", "15,600"]
    ws.word_problems(block1, blank_lines=2)
    pairs.extend(zip([n for n, _ in block1], block1_answers))

    ws.output(os.path.join(OUTDIR, "Worksheet-52-Discount-and-Markup.pdf"))
    ak = AnswerKey(52, "Discount and Markup", "102-103")
    ak.add_page()
    ak.answers(pairs, cols=3)
    ak.output(os.path.join(OUTDIR, "Worksheet-52-Answer-Key.pdf"))
    print(f"  Worksheet 52: Discount and Markup -- {len(pairs)} problems")
    return len(pairs)


def generate_ws53():
    """Calculate Interest (Practice 53, pp.103-105) -- 8 short compute-only
    items, numbered 1-8."""
    ws = Worksheet(53, "Calculate Interest", "103-105", unit_label=UNIT5_LABEL)
    ws.add_page()
    ws.name_date_line()
    ws.instructions("Find the interest for each of the following.")
    pairs = []

    block1 = [
        (1, "$800 at 6% annual interest for one year."),
        (2, "$600 at 3.5% annual interest for one year."),
        (3, "$400 at 12% annual interest for one year."),
        (4, "$450 at 4.8% annual interest for one year."),
        (5, "$480 at 5% annual interest for 5 months."),
        (6, "$2,400 at 10% annual interest for 1 year 8 months."),
        (7, "$360 at 3.5% annual interest for 1 year 4 months."),
        (8, "$3,600 at 9% annual interest for 1 year 9 months."),
    ]
    block1_answers = ["$48", "$21", "$48", "$21.60", "$10.00", "$400.00", "$16.80", "$567.00"]
    ws.horizontal_list(block1, cols=2)
    pairs.extend(zip([n for n, _ in block1], block1_answers))

    ws.output(os.path.join(OUTDIR, "Worksheet-53-Calculate-Interest.pdf"))
    ak = AnswerKey(53, "Calculate Interest", "103-105")
    ak.add_page()
    ak.answers(pairs, cols=3)
    ak.output(os.path.join(OUTDIR, "Worksheet-53-Answer-Key.pdf"))
    print(f"  Worksheet 53: Calculate Interest -- {len(pairs)} problems")
    return len(pairs)


def generate_ws56():
    """Multi-Step Problems, Part B: Percent of Increase and Decrease
    (Practice 56, pp.108-109) -- 5 word problems, numbered 1-5."""
    ws = Worksheet(56, "Percent of Increase and Decrease", "108-109", unit_label=UNIT5_LABEL)
    ws.add_page()
    ws.name_date_line()
    ws.instructions("Solve each problem. Show your work.")
    pairs = []

    block1 = [
        (1, "Last year Nancy made $16.20 an hour. This year she makes $17.82 an hour. By what percent did her wage increase?"),
        (2, "Mr. Walek runs a shoe store. He pays an average of $45 for a pair of shoes. He charges his customers an average "
            "of $63. By what percent does he mark up the price of a pair of shoes?"),
        (3, "Two years ago Larry bought gas for $1.20 a gallon. This year he pays $1.26 a gallon. By what percent did the "
            "price go up?"),
        (4, "Jeff bought a T.V. on sale for $187. Before the sale the T.V. cost $220. Find the percent of discount on the "
            "original price."),
        (5, "Last year there were 16 students in Mr. Green's night school math class. This year there are 22 students. By "
            "what percent did the number of students increase?"),
    ]
    block1_answers = ["10%", "40%", "5%", "15%", "37.5%"]
    ws.word_problems(block1, blank_lines=2)
    pairs.extend(zip([n for n, _ in block1], block1_answers))

    ws.output(os.path.join(OUTDIR, "Worksheet-56-Percent-of-Increase-and-Decrease.pdf"))
    ak = AnswerKey(56, "Percent of Increase and Decrease", "108-109")
    ak.add_page()
    ak.answers(pairs, cols=3)
    ak.output(os.path.join(OUTDIR, "Worksheet-56-Answer-Key.pdf"))
    print(f"  Worksheet 56: Percent of Increase and Decrease -- {len(pairs)} problems")
    return len(pairs)


def generate_review():
    """Percent Review (Progress Check, pp.112-113) -- all 23 verbatim review
    problems, kept at their ORIGINAL book numbers so the Progress Check
    table below stays accurate."""
    rv = Worksheet("Review", "Percent Review", "112-113", unit_label=UNIT5_LABEL)
    rv.add_page()
    rv.name_date_line()
    rv.instructions("These problems cover everything in Unit 5. Solve each one, then check your answers against "
                     "the Answer Key. The chart at the end tells you which pages to revisit for any you miss.")

    pairs = []

    rv.instructions("For problems 1-4, convert as directed.")
    block1 = [
        (1, "Change .09 to a percent."),
        (2, "Change 48% to a decimal."),
        (3, "Change 5/12 to a percent."),
        (4, "Change 85% to a fraction."),
    ]
    block1_answers = ["9%", ".48", "41 2/3%", "17/20"]
    rv.horizontal_list(block1, cols=2)
    pairs.extend(zip([n for n, _ in block1], block1_answers))

    rv.instructions("For problems 5-8, find the percent of the number.")
    block2 = [
        (5, "Find 15% of 125."),
        (6, "What is 370% of 90?"),
        (7, "What is 4.8% of 800?"),
        (8, "Find 66 2/3% of 129."),
    ]
    block2_answers = ["18.75", "333", "38.4", "86"]
    rv.horizontal_list(block2, cols=2)
    pairs.extend(zip([n for n, _ in block2], block2_answers))

    rv.instructions("Solve problems 9-10.")
    block3 = [
        (9, "The Lopez family makes $28,600 a year. They spend 25% of their income on mortgage payments. How much do they "
            "spend in a year on mortgage payments?"),
        (10, "Evan bought a shirt for $29.80. He had to pay 5% sales tax. How much did Evan pay for the shirt including tax?"),
    ]
    block3_answers = ["$7,150", "$31.29"]
    rv.word_problems(block3, blank_lines=1)
    pairs.extend(zip([n for n, _ in block3], block3_answers))

    rv.instructions("Find the interest for problems 11-12.")
    block4 = [
        (11, "Find the interest on $1,600 at 5% annual interest for one year."),
        (12, "Find the interest on $720 at 15% annual interest for nine months."),
    ]
    block4_answers = ["$80", "$81"]
    rv.horizontal_list(block4, cols=2)
    pairs.extend(zip([n for n, _ in block4], block4_answers))

    rv.instructions("For problems 13-16, find the percent.")
    block5 = [
        (13, "45 is what percent of 75?"),
        (14, "36 is what percent of 54?"),
        (15, "48 is what percent of 192?"),
        (16, "60 is what percent of 96?"),
    ]
    block5_answers = ["60%", "66 2/3%", "25%", "62.5%"]
    rv.horizontal_list(block5, cols=2)
    pairs.extend(zip([n for n, _ in block5], block5_answers))

    rv.instructions("Solve problems 17-18.")
    block6 = [
        (17, "Last year Fred made $460 a week. This year he got a raise of $23 a week. His raise is what percent of his "
             "old weekly salary?"),
        (18, "Before Joe went on a diet, he weighed 180 pounds. Now he weighs 153 pounds. What percent of his weight did "
             "he lose?"),
    ]
    block6_answers = ["5%", "15%"]
    rv.word_problems(block6, blank_lines=1)
    pairs.extend(zip([n for n, _ in block6], block6_answers))

    rv.instructions("For problems 19-22, find the whole number.")
    block7 = [
        (19, "30% of what number is 57?"),
        (20, "75% of what number is 108?"),
        (21, "48% of what number is 60?"),
        (22, "33 1/3% of what number is 24?"),
    ]
    block7_answers = ["190", "144", "125", "72"]
    rv.horizontal_list(block7, cols=2)
    pairs.extend(zip([n for n, _ in block7], block7_answers))

    rv.instructions("Solve problem 23.")
    block8 = [
        (23, "There were 240,000 people living in Central County in 1980. That was 75% of the number living there in "
             "1995. How many people lived in Central County in 1995?"),
    ]
    block8_answers = ["320,000"]
    rv.word_problems(block8, blank_lines=1)
    pairs.extend(zip([n for n, _ in block8], block8_answers))

    rv.section_heading("Progress Check")
    rv.set_font("Helvetica", "", 10)
    rv.multi_cell(0, 5.5, "Check your answers against the Answer Key. Then revisit the review pages for any "
                          "problems you missed, and correct your answers before moving on.")
    rv.ln(2)
    chart = [("1 to 4", "90 to 97"), ("5 to 10", "99 to 102"), ("11 to 12", "103 to 104"),
             ("13 to 18", "105 to 108"), ("19 to 23", "109 to 111")]
    rv.set_font("Helvetica", "B", 10)
    rv.cell(70, 7, "If you missed problems")
    rv.cell(0, 7, "Review pages", ln=1)
    rv.set_font("Helvetica", "", 10)
    for missed, review_pages in chart:
        rv.cell(70, 6.5, missed)
        rv.cell(0, 6.5, review_pages, ln=1)

    rv.output(os.path.join(OUTDIR, "Percent-Review.pdf"))
    ak_rv = AnswerKey("Review", "Percent Review", "112-113")
    ak_rv.add_page()
    pairs.sort(key=lambda p: p[0])
    ak_rv.answers(pairs, cols=3)
    ak_rv.output(os.path.join(OUTDIR, "Percent-Review-Answer-Key.pdf"))
    print(f"  Percent Review -- {len(pairs)} problems")
    return len(pairs)


def generate_worksheets():
    print("Generating Unit 5 Day 11 worksheet PDFs...")
    generate_ws52()
    generate_ws53()
    generate_ws56()
    generate_review()
    print("All Unit 5 Day 11 worksheets generated.\n")


# ===========================================================================
# UNIT 5 QUIZ + TEST (original questions, not copied from the book -- same
# distinction Unit 1-4 used: Practice/Worksheet = book-verbatim, Quiz/Test =
# original)
# ===========================================================================

UNIT5_QUIZ_BANNER = WRAP_OPEN + banner("Unit 5 &middot; Percent", "Unit 5 Quiz",
    "A quick, graded check across all 13 Unit 5 objectives.") + WRAP_CLOSE

unit5_quiz = {
    "type": "quiz", "title": "Unit 5 Quiz", "quiz_type": "assignment",
    "description": UNIT5_QUIZ_BANNER, "points_possible": 24,
    "questions": [
        q_short("Write 62% as a decimal.", 2, "0.62", ".62"),
        q_short("Write .08 as a percent.", 2, "8%"),
        q_short("Write 3/8 as a percent.", 2, "37.5%", "37 1/2%"),
        q_short("Write 40% as a fraction in lowest terms.", 2, "2/5"),
        q_short("Identify the percent, the whole, and the part: 60% of 50 is 30.", 2, "60%, 50, 30"),
        q_short("Find 25% of 84.", 2, "21"),
        q_short("Use proportion to find 15% of 220.", 2, "33"),
        q_short("Malik earns $2,400 a month and spends 20% on rent. How much does he spend on rent?", 2, "$480", "480"),
        q_short("18 is what percent of 72?", 2, "25%"),
        q_short("Find the interest on $500 at 8% annual interest for one year.", 2, "$40", "40"),
        q_short("40% of what number is 26?", 2, "65"),
        q_short("Last month gas cost $3.20 a gallon. This month it costs $3.52 a gallon. By what percent did the price increase?", 2, "10%"),
    ],
}

UNIT5_TEST_BANNER = WRAP_OPEN + banner("Unit 5 &middot; Percent", "Unit 5 Test",
    "A comprehensive, graded test across all 13 Unit 5 objectives.") + WRAP_CLOSE

unit5_test = {
    "type": "quiz", "title": "Unit 5 Test", "quiz_type": "assignment",
    "description": UNIT5_TEST_BANNER, "points_possible": 37,
    "questions": [
        q_short("Write 7% as a decimal.", 2, "0.07", ".07"),
        q_short("Write .375 as a percent.", 2, "37.5%", "37 1/2%"),
        q_short("Write 5/6 as a percent.", 2, "83 1/3%"),
        q_short("Write 24% as a fraction in lowest terms.", 2, "6/25"),
        q_short("Identify the percent, the whole, and the part: 40 is 20% of 200.", 2, "20%, 200, 40"),
        q_short("Find 45% of 160.", 2, "72"),
        q_short("Use proportion to find 8% of 650.", 2, "52"),
        q_short("Priya bought a jacket for $84 and paid 7% sales tax. How much was the tax?", 3, "$5.88", "5.88"),
        q_short("27 is what percent of 90?", 2, "30%"),
        q_short("Use proportion: 54 is what percent of 72?", 2, "75%"),
        q_short("Find the interest on $1,200 at 6% annual interest for 6 months.", 3, "$36", "36"),
        q_short("Find the interest on $2,000 at 9% annual interest for 1 year 4 months.", 3, "$240", "240"),
        q_short("35% of what number is 63?", 2, "180"),
        q_short("Use proportion: 12% of what number is 54?", 2, "450"),
        q_short("A phone bill was $60 last month and $75 this month. By what percent did the bill increase?", 3, "25%"),
        q_short("A TV originally cost $340 and is on sale for $272. Find the percent discount.", 3, "20%"),
    ],
}

print("Unit 5 Quiz + Test defined.")


# ===========================================================================
# ASSEMBLE DAY 11 ITEMS
# ===========================================================================

def build_day11_items():
    review_description = (
        WRAP_OPEN
        + banner("Day 11 &middot; Unit 5 Self-Paced Practice", "Percent Review", "Self-check &mdash; not graded. Book pages 112-113.")
        + box("", (
            '<p style="margin:0 0 12px;">These problems cover everything in Unit 5 &mdash; all 13 objectives, from writing '
            'percents through interest and multi-step problems. Print the PDF, solve each problem, then check your answers '
            'against the Answer Key. The Progress Check chart at the end of the PDF tells you which pages to revisit for any '
            'problems you miss, before moving on to the Unit 5 Quiz.</p>'
            f'{pdf_link("Download Percent Review (PDF)", PLACEHOLDER)}'
        ))
        + f'<details style="margin-top:14px;"><summary style="cursor:pointer;color:#003462;font-weight:bold;">Answer Key</summary>'
          f'<div style="margin-top:10px;">{pdf_link("Download Answer Key (PDF)", PLACEHOLDER)}</div></details>'
        + WRAP_CLOSE
    )

    return [
        {"type": "page", "title": "Day 11 Overview", "body": DAY11_OVERVIEW_BODY},
        {"type": "page", "title": "Multi-Step Problems, Part A: Discount and Markup — Reading", "body": discount_markup_body},
        {"type": "assignment", "title": "Worksheet 52: Multi-Step Problems — Discount and Markup",
         "description": worksheet_description("Worksheet 52: Multi-Step Problems — Discount and Markup", "102-103"),
         "points_possible": 0, "submission_types": ["on_paper"]},
        {"type": "page", "title": "Calculate Interest — Reading", "body": interest_body},
        {"type": "assignment", "title": "Worksheet 53: Calculate Interest",
         "description": worksheet_description("Worksheet 53: Calculate Interest", "103-105"),
         "points_possible": 0, "submission_types": ["on_paper"]},
        {"type": "page", "title": "Multi-Step Problems, Part B: Percent of Increase and Decrease — Reading", "body": increase_decrease_body},
        {"type": "assignment", "title": "Worksheet 56: Multi-Step Problems — Percent of Increase and Decrease",
         "description": worksheet_description("Worksheet 56: Multi-Step Problems — Percent of Increase and Decrease", "108-109"),
         "points_possible": 0, "submission_types": ["on_paper"]},
        {"type": "assignment", "title": "Percent Review (Self-Paced Practice)",
         "description": review_description, "points_possible": 0, "submission_types": ["on_paper"]},
        unit5_quiz,
        unit5_test,
        {"type": "page", "title": "Day 11: Want More Practice?", "body": day11_want_more_body},
    ]


# ===========================================================================
# EXECUTE (local-only: PDF generation + JSON fragment write, no Canvas calls)
# ===========================================================================

if __name__ == "__main__":
    print("\n=== Generating worksheet PDFs ===")
    generate_worksheets()

    DAY11_ITEMS = build_day11_items()

    fragment = {"course_name": "Business Math 26/27", "modules": [
        {"name": "Day 11, Unit 5: Percent (Multi-Step Problems, Interest, Review, Quiz, Test)",
         "position": DAY11_POSITION, "items": DAY11_ITEMS}
    ]}

    out_path = os.path.join(FRAGMENT_DIR, "day11-module-fragment.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(fragment, f, indent=2, ensure_ascii=False)

    print(f"\nWrote fragment: {out_path}")
    print(f"Generated worksheet PDFs in: {OUTDIR}")
    print("Done. (No Canvas calls made -- local files only.)")
