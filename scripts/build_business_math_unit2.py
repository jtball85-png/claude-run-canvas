# -*- coding: utf-8 -*-
"""Build Unit 2: Decimals (Day 3 + Day 4) into Business Math course 456.

Day 3 (module position 4) = single-step topics (place value, read/write,
compare, round decimals) as ungraded practice quizzes -- mirrors Day 1's
pattern exactly.

Day 4 (module position 5) = multi-step topics (add/subtract/multiply/
divide decimals, 3 division sub-skills) as printable worksheets, closing
with the book's own Decimals Review (self-paced) + an original graded
Unit 2 Quiz + Unit 2 Test -- mirrors Day 2's pattern exactly.

Source: `Lesson Planning/Business Math/Unit 2 Decimals Content Brief.md`,
a source-verified deep-read of all 21 real textbook pages (pp.30-50),
produced 2026-09-01. Worksheet problems and reading-page worked examples
are transcribed verbatim from that brief; Quiz/Test questions are original
(not copied from the book), matching the Unit 1 precedent.

Also dumps day3/day4-module-fragment.json into this repo's
`Lesson Planning/Business Math/` folder as the source-of-truth record,
matching Unit 1's day1/day2-module-fragment.json.
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from push_course import (create_module, create_page, create_quiz, create_assignment,
                          add_to_module, upload_file_to_canvas, SITE_ROOT)
from worksheet_pdf import Worksheet, AnswerKey, OUTDIR

COURSE_ID = 456
DAY3_POSITION = 4
DAY4_POSITION = 5
FRAGMENT_DIR = r"C:\Users\jball.VACE\Documents\Claude Projects\Master Business Finance Program\Lesson Planning\Business Math"

# ===========================================================================
# HTML helpers (identical design system to Unit 1's rebuild script)
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


# ===========================================================================
# Verified real YouTube video IDs (Math Antics/mathantics official channel,
# confirmed via oEmbed 2026-09-01 -- author_name == "mathantics" checked for
# every one). Never guess a video ID.
# ===========================================================================
V_DECIMAL_PLACE_VALUE = "KG6ILNOiMgM"    # Math Antics - Decimal Place Value
V_COMPARE_DECIMALS = "rALUd3wW29s"       # Comparing Decimal Numbers - Math Antics Extras
V_ROUNDING = "fd-E18EqSVk"               # Math Antics - Rounding (whole numbers, reused)
V_DECIMAL_ARITHMETIC = "kwh4SD1ToFc"     # Math Antics - Decimal Arithmetic (covers +-x/div)

# ===========================================================================
# DAY 3 READING PAGES
# ===========================================================================

place_value_body = slim_header("Day 3 &middot; Unit 2 Reading") + meta_line("30-32", "Identify place value in decimals") + (
    '<h2>Place Value in Decimals</h2>'
    '<p>A decimal is a kind of fraction. Like a fraction, a decimal shows a part of a whole. Decimals divide a whole into 10 parts, '
    'or 100 parts, or 1,000 parts, and so on. You have used decimals since you first handled money &mdash; $.70 is a decimal, and it '
    'means 70 of the 100 equal parts in a dollar.</p>'
    '<p>Decimals get their names from the number of places on the right side of the decimal point. The decimal point separates whole '
    'numbers from decimals. A <strong>place</strong> is the position of a digit &mdash; the decimal point itself does not take up a place.</p>'
    '<p><strong>Mixed decimals</strong> are numbers with digits on both sides of the decimal point. $4.95 is a mixed decimal: 4 whole '
    'dollars and 95/100 of a dollar.</p>'
    + box("Breaking It Down", (
        '<p style="margin:0;">A decimal is really the same place-value system as whole numbers, just mirrored across the decimal '
        'point. Whole-number places (ones, tens, hundreds...) get bigger as you move left; decimal places (tenths, hundredths, '
        'thousandths...) get smaller as you move right &mdash; each one is 10 times smaller than the last. As you move to the right, '
        'the whole is being divided into more and more parts.</p>'
    ), accent="blue")
    + '<p><em>Example:</em> What is the value of 6 in the number .68?</p>'
    '<p>The digit 6 is in the tenths place. It has a value of 6 out of ten equal parts in one whole.</p>'
    + box("A Second Example", (
        '<p style="margin:0;"><em>What is the value of 4 in the number .347?</em><br>'
        'Counting from the decimal point: 3 is tenths, 4 is hundredths, 7 is thousandths. The 4 is in the <strong>hundredths</strong> '
        'place, so its value is 4 out of 100 equal parts of the whole (4 hundredths).</p>'
    ))
    + callout("Common Mistakes to Avoid", (
        'Just like with whole numbers, don&rsquo;t confuse <em>place</em> and <em>value</em> &mdash; the value of a digit is what '
        'it&rsquo;s actually worth (&ldquo;4 hundredths&rdquo;), not just its name (&ldquo;hundredths&rdquo;). Also remember decimal '
        'places get <strong>smaller</strong> moving right, the opposite direction from whole-number places.'
    ))
    + video_embed(V_DECIMAL_PLACE_VALUE, "Math Antics - Decimal Place Value")
)

reading_writing_body = slim_header("Day 3 &middot; Unit 2 Reading") + meta_line("32-34", "Read and write decimals") + (
    '<h2>Reading and Writing Decimals</h2>'
    '<p>Remember that a decimal gets its name from the number of places at the right of the decimal point. To read a decimal, count '
    'the places at the right of the point. With mixed decimals, separate the whole number and the decimal with the word <em>and</em>.</p>'
    '<p>When you write decimals, decide how many places you need, then use zeros in places that are not filled.</p>'
    + box("Breaking It Down", (
        '<p style="margin:0;">Reading a decimal is a two-step move: count how many places are to the right of the decimal point, and '
        'that count tells you the name of the smallest place (one place = tenths, two = hundredths, three = thousandths...). Writing a '
        'decimal from words works the same in reverse &mdash; the last word tells you how many decimal places you need, and any place '
        'you don&rsquo;t have a digit for gets a zero.</p>'
    ), accent="blue")
    + '<p><em>Example:</em> Read the decimal .042.</p>'
    '<p>Count the decimal places. The decimal .042 has three. Three places are thousandths. Read .042 as <em>forty-two thousandths</em>.</p>'
    '<p><em>Example:</em> Read 13.09.</p>'
    '<p>Count the decimal places. The mixed decimal 13.09 has two. Two decimal places are hundredths. Read 13.09 as <em>thirteen and '
    'nine hundredths</em>.</p>'
    '<p><em>Example:</em> Write eleven and nine thousandths as a mixed decimal.</p>'
    '<p><strong>Step 1.</strong> Write the whole number 11.<br>'
    '<strong>Step 2.</strong> Decide how many places you need. Thousandths need three places.<br>'
    '<strong>Step 3.</strong> The number 9 needs only one place. Put zeros in the first two decimal places.</p>'
    '<p>Answer: <strong>11.009</strong>.</p>'
    + box("A Second Example (writing)", (
        '<p style="margin:0;"><em>Write four hundred six thousandths as a decimal.</em><br>'
        'Thousandths needs three places. 406 already has three digits, so no zero-padding is needed. Answer: <strong>.406</strong>.</p>'
    ))
    + callout("Common Mistakes to Avoid", (
        'When writing FROM words, count your digits against the place name before you&rsquo;re done &mdash; &ldquo;sixteen '
        'millionths&rdquo; needs six decimal places (.000016), and it&rsquo;s easy to drop a zero. When reading, remember a mixed '
        'decimal is read with the word <em>and</em> separating the whole number from the decimal &mdash; &ldquo;and&rdquo; marks the '
        'decimal point, not just a filler word.'
    ))
    + callout("Want a video for this one?", (
        'This skill is really decimal place value applied to reading/writing &mdash; if you want a refresher, revisit the Decimal '
        'Place Value video on the previous page, or check the Khan Academy link on the <strong>Want More Practice?</strong> page.'
    ))
)

compare_body = slim_header("Day 3 &middot; Unit 2 Reading") + meta_line("34-35", "Compare decimals") + (
    '<h2>Comparing Decimals</h2>'
    '<p>When you compare decimals, first change the decimals to new decimals with the same number of places. You can put zeros to the '
    'right of a decimal without changing its value &mdash; for example .5 and .50 have the same value.</p>'
    + box("Breaking It Down", (
        '<p style="margin:0;">Comparing decimals gets confusing because a &ldquo;longer&rdquo; decimal isn&rsquo;t automatically '
        'bigger &mdash; .5 is bigger than .49 even though .49 has more digits. The fix is the book&rsquo;s own trick: pad every '
        'decimal with trailing zeros until they all have the same number of places, then compare like whole numbers. .5 becomes .50, '
        'and .50 &gt; .49 is easy to see.</p>'
    ), accent="blue")
    + '<p><em>Example:</em> Cal wants to know which is heavier, a package that weighs .08 pound or a package that weighs .6 pound. '
    'Which decimal is greater, .08 or .6?</p>'
    '<p><strong>Step 1.</strong> Put a zero at the right of .6 to change it to .60. Both decimals are hundredths now.<br>'
    '<strong>Step 2.</strong> Decide which is greater, .08 or .60. Sixty hundredths is more than eight hundredths.</p>'
    '<p>The decimal .6 is greater, so the package that weighs .6 pound is heavier.</p>'
    + box("A Second Example (three decimals)", (
        '<p style="margin:0;"><em>Which decimal has the greatest value: .34, .3, or .304?</em><br>'
        'Put zeros at the right until all three are thousandths: .340, .300, .304. Three hundred forty thousandths is the biggest. '
        '<strong>.34 has the greatest value.</strong></p>'
    ))
    + callout("Common Mistakes to Avoid", (
        'Never compare decimals by counting digits &mdash; a 3-digit decimal isn&rsquo;t automatically bigger than a 1-digit one. '
        '<strong>Always</strong> pad with zeros to equal length first, then compare.'
    ))
    + video_embed(V_COMPARE_DECIMALS, "Comparing Decimal Numbers - Math Antics Extras")
)

rounding_body = slim_header("Day 3 &middot; Unit 2 Reading") + meta_line("35-37", "Round decimals") + (
    '<h2>Rounding Decimals</h2>'
    '<p>To round off a number, you must know the place value of each digit in the number.</p>'
    '<p>To round a decimal:</p>'
    '<ol style="margin:0 0 10px;padding-left:20px;">'
    '<li>Underline the digit in the place to which you want to round.</li>'
    '<li>If the digit to the right of the underlined digit is more than 4, add 1 to the underlined digit.</li>'
    '<li>If the digit to the right of the underlined digit is less than 5, do not change the underlined digit.</li>'
    '<li>Drop the digits to the right of the underlined digit.</li>'
    '</ol>'
    + box("Breaking It Down", (
        '<p style="margin:0;">This is the exact same rounding rule from Day 1, just applied past the decimal point instead of before '
        'it: find your target place, look at exactly one digit to its right, and round up or stay based on that single digit. The '
        'only new twist is that &ldquo;dropping&rdquo; digits after a decimal point (instead of replacing them with zeros) is what '
        'actually shortens the number.</p>'
    ), accent="blue")
    + '<p><em>Example:</em> Sandra shipped a package that weighed 2.48 pounds. Round 2.48 to the nearest tenth.</p>'
    '<p><strong>Step 1.</strong> Underline the digit in the tenths place, 4: 2.<u>4</u>8<br>'
    '<strong>Step 2.</strong> The digit to the right of 4 is 8. Add 1 to 4, and drop the digit to the right.</p>'
    '<p>To the nearest tenth of a pound, the package weighs <strong>2.5</strong> pounds.</p>'
    '<p><em>Example:</em> Round .732 to the nearest hundredth.</p>'
    '<p><strong>Step 1.</strong> Underline the digit in the hundredths place, 3: .7<u>3</u>2<br>'
    '<strong>Step 2.</strong> The digit to the right of 3 is 2. Do not change 3, but drop the digit to the right.</p>'
    '<p>.732 to the nearest hundredth is <strong>.73</strong>.</p>'
    + box("A Third Example (carrying)", (
        '<p style="margin:0;"><em>Round .0198 to the nearest thousandth.</em><br>'
        'Underline the thousandths digit, 9: .01<u>9</u>8. The digit to the right is 8, so add 1 to 9. Since 1 + 9 = 10, carry 1 over '
        'to the hundredths column, and drop the digit to the right. <strong>.0198 to the nearest thousandth is .020.</strong></p>'
    ))
    + callout("Common Mistakes to Avoid", (
        'Same rule as whole-number rounding &mdash; look at exactly <strong>one</strong> digit, not several. A decimal-specific slip: '
        'rounding .0198 to the nearest thousandth gives .020, not .02 &mdash; keep the trailing zero that shows you rounded to '
        'thousandths, don&rsquo;t simplify it away.'
    ))
    + callout("Same skill, same video", (
        'This is the exact same rounding rule as Day 1&rsquo;s Rounding Whole Numbers reading &mdash; rewatch that video there if you '
        'need a refresher, or check the Want More Practice? page.'
    ))
)

# ===========================================================================
# DAY 3 PRACTICE QUIZZES (Practice 12-15, transcribed from the book, verified
# against Unit 2 Decimals Content Brief.md)
# ===========================================================================

practice12 = {
    "type": "quiz", "title": "Practice 12: Place Value in Decimals", "quiz_type": "practice_quiz",
    "description": WRAP_OPEN + banner("Day 3 &middot; Unit 2 Practice", "Practice 12: Place Value in Decimals",
        "Self-check &mdash; not graded. Book pages 30-32.") + WRAP_CLOSE,
    "questions": [
        q_short("In the number 3.2, what digit is in the tenths place?", 1, "2"),
        q_short("In the number .189, what digit is in the tenths place?", 1, "1"),
        q_short("In the number 5.38, what digit is in the hundredths place?", 1, "8"),
        q_short("In the number 3.4921, what digit is in the hundredths place?", 1, "9"),
        q_short("In the number .345, what digit is in the thousandths place?", 1, "5"),
        q_short("In the number 12.1185, what digit is in the thousandths place?", 1, "8"),
        q_short("Use the number 5.39. The digit 3 is in the ___ place.", 1, "tenths"),
        q_short("Use the number 5.39. The digit 3 has a value of 3 out of how many equal parts in one whole?", 1, "10", "ten"),
        q_short("Use the number 5.39. The digit 9 is in the ___ place.", 1, "hundredths"),
        q_short("Use the number 5.39. The digit 9 has a value of 9 out of how many equal parts in one whole?", 1, "100", "one hundred"),
    ],
}

practice13 = {
    "type": "quiz", "title": "Practice 13: Reading and Writing Decimals", "quiz_type": "practice_quiz",
    "description": WRAP_OPEN + banner("Day 3 &middot; Unit 2 Practice", "Practice 13: Reading and Writing Decimals",
        "Self-check &mdash; not graded. Book pages 32-34.") + WRAP_CLOSE,
    "questions": [
        q_short("Fill in the missing word: .3 = three ___.", 1, "tenths"),
        q_short("Fill in the missing word: .06 = six ___.", 1, "hundredths"),
        q_short("Fill in the missing word: .015 = fifteen ___.", 1, "thousandths"),
        q_short("4.2 is read \u201cfour ___ two ___.\u201d What are the two missing words, in order?", 1, "and, tenths", "and tenths"),
        q_short("8.07 is read \u201ceight ___ seven ___.\u201d What are the two missing words, in order?", 1, "and, hundredths", "and hundredths"),
        q_short("Write \u201cthree tenths\u201d as a decimal.", 1, ".3", "0.3"),
        q_short("Write \u201cthirteen thousandths\u201d as a decimal.", 1, ".013", "0.013"),
        q_short("Write \u201ctwo hundredths\u201d as a decimal.", 1, ".02", "0.02"),
        q_short("Write \u201cfive and four hundredths\u201d as a mixed decimal.", 1, "5.04"),
        q_short("Write \u201cthirty and seven tenths\u201d as a mixed decimal.", 1, "30.7"),
        q_short("Write \u201ctwelve ten-thousandths\u201d as a decimal.", 1, ".0012", "0.0012"),
        q_short("Write \u201csixteen millionths\u201d as a decimal.", 1, ".000016", "0.000016"),
        q_short("Write \u201ctwenty-six and nine tenths\u201d as a mixed decimal.", 1, "26.9"),
    ],
}

practice14 = {
    "type": "quiz", "title": "Practice 14: Comparing Decimals", "quiz_type": "practice_quiz",
    "description": WRAP_OPEN + banner("Day 3 &middot; Unit 2 Practice", "Practice 14: Comparing Decimals",
        "Self-check &mdash; not graded. Book pages 34-35.") + WRAP_CLOSE,
    "questions": [
        q_short("Which is greater: .9 or .95?", 1, ".95"),
        q_short("Which is greater: .27 or .3?", 1, ".3"),
        q_short("Which is greater: .07 or .052?", 1, ".07"),
        q_short("Which is greater: .297 or .4?", 1, ".4"),
        q_short("Which is greater: .004 or .04?", 1, ".04"),
        q_short("Which is greater: .05 or .061?", 1, ".061"),
        q_short("Which is greater: .64 or .626?", 1, ".64"),
        q_short("Which is greater: .33 or .323?", 1, ".33"),
        q_short("Which is greater: .564 or .55?", 1, ".564"),
        q_short("Which is greatest: .7, .07, or .67?", 1, ".7"),
        q_short("Which is greatest: .407, .43, or .4?", 1, ".43"),
        q_short("Which is greatest: .0012, .201, or .12?", 1, ".201"),
        q_short("Which is greatest: .29, .3, or .302?", 1, ".302"),
        q_short("Which is greatest: .5, .055, or .505?", 1, ".505"),
        q_short("Which is greatest: .707, .77, or .07?", 1, ".77"),
        q_short("Which is greatest: .08, .028, or .82?", 1, ".82"),
        q_short("Which is greatest: .79, .097, or .709?", 1, ".79"),
        q_short("Which is greatest: .033, .03, or .3303?", 1, ".3303"),
    ],
}

practice15 = {
    "type": "quiz", "title": "Practice 15: Rounding Decimals", "quiz_type": "practice_quiz",
    "description": WRAP_OPEN + banner("Day 3 &middot; Unit 2 Practice", "Practice 15: Rounding Decimals",
        "Self-check &mdash; not graded. Book pages 35-37.") + WRAP_CLOSE,
    "questions": [
        q_short("Round .39 to the nearest tenth.", 1, ".4", "0.4"),
        q_short("Round 2.13 to the nearest tenth.", 1, "2.1"),
        q_short("Round .454 to the nearest tenth.", 1, ".5", "0.5"),
        q_short("Round 8.276 to the nearest tenth.", 1, "8.3"),
        q_short("Round 7.98 to the nearest tenth.", 1, "8.0", "8"),
        q_short("Round .073 to the nearest hundredth.", 1, ".07", "0.07"),
        q_short("Round .635 to the nearest hundredth.", 1, ".64", "0.64"),
        q_short("Round 12.498 to the nearest hundredth.", 1, "12.50", "12.5"),
        q_short("Round .4239 to the nearest hundredth.", 1, ".42", "0.42"),
        q_short("Round 6.337 to the nearest hundredth.", 1, "6.34"),
        q_short("Round .1047 to the nearest thousandth.", 1, ".105", "0.105"),
        q_short("Round 2.8817 to the nearest thousandth.", 1, "2.882"),
        q_short("Round .0066 to the nearest thousandth.", 1, ".007", "0.007"),
        q_short("Round .0395 to the nearest thousandth.", 1, ".040", "0.04", ".04"),
        q_short("Round 4.4892 to the nearest thousandth.", 1, "4.489"),
        q_short("Round 7.36 to the nearest whole number.", 1, "7"),
        q_short("Round 2.552 to the nearest whole number.", 1, "3"),
        q_short("Round 9.74 to the nearest whole number.", 1, "10"),
        q_short("Round 307.2 to the nearest whole number.", 1, "307"),
        q_short("Round 41.83 to the nearest whole number.", 1, "42"),
        q_short("One meter is equal to 1.0936 yards. Find the amount to the nearest hundredth yard.", 1, "1.09"),
        q_short("One meter is equal to 1.0936 yards. Find the amount to the nearest tenth yard.", 1, "1.1"),
    ],
}

day3_want_more_body = (
    WRAP_OPEN
    + banner("Day 3 &middot; Unit 2", "Want More Practice?", "Optional extra videos and practice for today's skills &mdash; use these if you want more repetition before Day 4.")
    + box("Place Value &amp; Reading/Writing Decimals", resource_list([
        ("Math Antics - Decimal Place Value (video)", f"https://www.youtube.com/watch?v={V_DECIMAL_PLACE_VALUE}",
         "Same video embedded on the Place Value reading."),
        ("Khan Academy - Decimals in written form", "https://www.khanacademy.org/math/arithmetic-home/arith-decimals",
         "Free interactive practice: decimal place value, reading, and writing."),
    ]))
    + box("Comparing Decimals", resource_list([
        ("Comparing Decimal Numbers - Math Antics Extras (video)", f"https://www.youtube.com/watch?v={V_COMPARE_DECIMALS}",
         "Same video embedded on the Compare Decimals reading."),
        ("Khan Academy - Compare decimals", "https://www.khanacademy.org/math/arithmetic-home/arith-decimals/comparing-decimals/e/comparing_decimals_1",
         "Interactive comparison drills with instant feedback."),
    ]), accent="blue")
    + box("Rounding Decimals", resource_list([
        ("Math Antics - Rounding (video)", f"https://www.youtube.com/watch?v={V_ROUNDING}",
         "Same rounding rule from Day 1, applied to decimals."),
        ("Khan Academy - Round decimals", "https://www.khanacademy.org/math/arithmetic-home/arith-decimals/rounding-decimals/e/rounding_numbers_0.5",
         "Interactive rounding drills."),
    ]))
    + WRAP_CLOSE
)

DAY3_OVERVIEW_BODY = (
    WRAP_OPEN
    + banner("Day 3 &middot; Unit 2: Decimals", "Day 3 Overview",
        "How decimals work &mdash; place value, reading and writing them, comparing them, and rounding them. Same skills as Day 1's whole numbers, now applied past the decimal point.")
    + box("Learning Objectives Covered Today", (
        '<ul style="margin:0;padding-left:20px;"><li>Identify place value in decimals</li><li>Read and write decimals</li>'
        '<li>Compare decimals</li><li>Round decimals</li></ul>'
    ))
    + box("Why It Matters", (
        '<p style="margin:0;">Decimals are everywhere in business math &mdash; prices, hourly wages, measurements, percentages. '
        'Getting comfortable reading, comparing, and rounding them now makes every later unit (and every real invoice, paycheck, or '
        'price tag) much easier to work with.</p>'
    ), accent="blue")
    + box("Today&rsquo;s Tasks", (
        '<ol style="margin:0;padding-left:20px;"><li>Place Value in Decimals &mdash; read, then complete Practice 12</li>'
        '<li>Reading and Writing Decimals &mdash; read, then complete Practice 13</li>'
        '<li>Comparing Decimals &mdash; read, then complete Practice 14</li>'
        '<li>Rounding Decimals &mdash; read, then complete Practice 15</li></ol>'
    ))
    + callout("Note", (
        'Practice 12-15 are self-check practice quizzes, not graded &mdash; use them to see what&rsquo;s solid and what needs another '
        'look before Day 4, when we start adding, subtracting, multiplying, and dividing decimals.'
    ))
    + WRAP_CLOSE
)

DAY3_ITEMS = [
    {"type": "page", "title": "Day 3 Overview", "body": DAY3_OVERVIEW_BODY},
    {"type": "page", "title": "Place Value in Decimals — Reading", "body": place_value_body},
    practice12,
    {"type": "page", "title": "Reading and Writing Decimals — Reading", "body": reading_writing_body},
    practice13,
    {"type": "page", "title": "Comparing Decimals — Reading", "body": compare_body},
    practice14,
    {"type": "page", "title": "Rounding Decimals — Reading", "body": rounding_body},
    practice15,
    {"type": "page", "title": "Day 3: Want More Practice?", "body": day3_want_more_body},
]

print("Day 3 content module built:", len(DAY3_ITEMS), "items")

# ===========================================================================
# DAY 4 READING PAGES
# ===========================================================================

add_body = slim_header("Day 4 &middot; Unit 2 Reading") + meta_line("38-39", "Add decimals") + (
    '<h2>Addition of Decimals</h2>'
    '<p>To add decimals, line up the numbers with the decimal points under each other. Remember that a whole number is understood to '
    'have a decimal point to the right.</p>'
    + box("Breaking It Down", (
        '<p style="margin:0;">Adding decimals is ordinary column addition with one extra rule: line up the decimal points first, not '
        'the right-hand digits like you would with whole numbers. Once the points are stacked, treat every column exactly like '
        'whole-number addition &mdash; carry when a column totals 10 or more.</p>'
    ), accent="blue")
    + '<p><em>Example:</em> Richard is a plumber. He wants to know the combined thickness of three copper fittings: one is .63 inch '
    'thick, the second is 2 inches thick, and the third is 1.279 inches thick. .63 + 2 + 1.279 =</p>'
    '<p><strong>Step 1.</strong> Line up the numbers with the points under each other (2 becomes 2.000).<br>'
    '<strong>Step 2.</strong> Add each column.</p>'
    '<p>The combined thickness of the fittings is <strong>3.909</strong> inches.</p>'
    + box("A Second Example", (
        '<p style="margin:0;"><em>Chicago&rsquo;s average April temperature is 47.8&deg;. St. Louis is 8.3&deg; higher. What is St. '
        'Louis&rsquo;s average April temperature?</em><br>'
        '47.8 + 8.3 = <strong>56.1&deg;</strong>.</p>'
    ))
    + callout("Common Mistakes to Avoid", (
        'The #1 decimal-addition error is lining up the last digit instead of the decimal point &mdash; .5 + 12 is NOT .5 stacked '
        'under the 2 of 12; it&rsquo;s .50 stacked under 12.00. When a number has no visible decimal point (like a whole number), '
        'remember it has an invisible one at the far right.'
    ))
    + video_embed(V_DECIMAL_ARITHMETIC, "Math Antics - Decimal Arithmetic")
)

subtract_body = slim_header("Day 4 &middot; Unit 2 Reading") + meta_line("40-41", "Subtract decimals") + (
    '<h2>Subtraction of Decimals</h2>'
    '<p>To subtract decimals, line up the decimals with the points under each other just like addition. Remember to put a point at '
    'the right of a whole number. Put zeros at the right until each decimal has the same number of places &mdash; you will need the '
    'zeros for borrowing.</p>'
    + box("Breaking It Down", (
        '<p style="margin:0;">Subtracting decimals uses the same point-alignment rule as addition, plus one more step: pad the '
        'shorter decimal with zeros on the right until both numbers have the same number of places. Those zeros aren&rsquo;t just '
        'filler &mdash; they&rsquo;re what you actually borrow from when regrouping.</p>'
    ), accent="blue")
    + '<p><em>Example:</em> From a board 5 meters long, Jamal cut a piece .38 meter long. How long was the remaining piece? 5 &minus; .38 =</p>'
    '<p><strong>Step 1.</strong> Put a decimal point at the right of 5.<br>'
    '<strong>Step 2.</strong> Line up the numbers with the points under each other.<br>'
    '<strong>Step 3.</strong> Put two zeros at the right of 5 to give each decimal the same number of places: 5.00.<br>'
    '<strong>Step 4.</strong> Regroup and subtract.</p>'
    '<p>The remaining piece was <strong>4.62</strong> meters long.</p>'
    + box("A Second Example", (
        '<p style="margin:0;"><em>The United States covers about 3.3 million square miles; Canada covers about 3.8 million. How much '
        'bigger is Canada?</em><br>'
        '3.8 &minus; 3.3 = <strong>.5</strong> million square miles bigger.</p>'
    ))
    + callout("Common Mistakes to Avoid", (
        'Forgetting to zero-pad before subtracting is the most common mistake &mdash; 5 &minus; .38 only works cleanly once 5 becomes '
        '5.00. Skipping that step leads to lining up the wrong columns entirely.'
    ))
    + callout("Same skill, same video", (
        'This is the same Decimal Arithmetic video from the Add Decimals reading &mdash; rewatch it there if you need the subtraction '
        'portion again.'
    ))
)

multiply_body = slim_header("Day 4 &middot; Unit 2 Reading") + meta_line("42-43", "Multiply decimals") + (
    '<h2>Multiplication of Decimals</h2>'
    '<p>To multiply decimals, count the decimal places in each number. Put the total number of decimal places in the answer. '
    'Sometimes you will need to put extra zeros in your answer.</p>'
    + box("Breaking It Down", (
        '<p style="margin:0;">Multiplying decimals is the one operation where you do <strong>not</strong> line up the decimal points '
        'first &mdash; just multiply the digits as if there were no decimal points at all, then count. Add up the total number of '
        'decimal places in both numbers you&rsquo;re multiplying, and that&rsquo;s how many decimal places belong in the answer.</p>'
    ), accent="blue")
    + '<p><em>Example:</em> Sean has to ship a 6.5-pound package to a foreign country. One pound is .45 kilograms. .45 &times; 6.5 =</p>'
    '<p><strong>Step 1.</strong> Multiply the numbers as whole numbers: 45 &times; 65 = 2,925.<br>'
    '<strong>Step 2.</strong> Count the decimal places: .45 has two, 6.5 has one.<br>'
    '<strong>Step 3.</strong> Put the total (2 + 1 = 3) decimal places in the answer.</p>'
    '<p>The package weighs <strong>2.925</strong> kilograms.</p>'
    '<p><em>Example:</em> .3 &times; .07 =</p>'
    '<p>.07 has two decimal places and .3 has one, so the answer needs three decimal places (2 + 1 = 3). 3 &times; 7 = 21, and a zero '
    'is added to the left of 21 to make three places: <strong>.021</strong>.</p>'
    + box("A Second Example", (
        '<p style="margin:0;"><em>Adrienne works overtime for $18.60 an hour. Last week she worked 7.5 hours overtime. How much did '
        'she make for overtime work?</em><br>'
        '$18.60 &times; 7.5 = <strong>$139.50</strong>.</p>'
    ))
    + callout("Common Mistakes to Avoid", (
        'It&rsquo;s tempting to line up decimal points here out of habit from adding/subtracting &mdash; resist that. Multiply first, '
        'ignoring the points completely, then count decimal places in both original numbers and place the point in the answer. If '
        'the digit-only product doesn&rsquo;t have enough digits, pad with a leading zero (like .3 &times; .07 = .021, not .21).'
    ))
    + callout("Same skill, same video", (
        'This is the same Decimal Arithmetic video from the Add Decimals reading &mdash; rewatch it there for the multiplication '
        'portion.'
    ))
)

divide_whole_body = slim_header("Day 4 &middot; Unit 2 Reading") + meta_line("44-45", "Divide decimals by whole numbers") + (
    '<h2>Division of Decimals by Whole Numbers</h2>'
    '<p>To divide a decimal by a whole number, line up the problem carefully. Then divide and bring the decimal point up into the '
    'answer above its position in the problem. Sometimes you will need to put zeros in your answers.</p>'
    + box("Breaking It Down", (
        '<p style="margin:0;">Dividing a decimal by a whole number works almost exactly like whole-number long division &mdash; the '
        'only difference is that the decimal point in the answer goes directly above the decimal point in the problem, the moment '
        'you reach it. Everything else (divide, multiply, subtract, bring down) is the same 4-step cycle from Day 2.</p>'
    ), accent="blue")
    + '<p><em>Example:</em> Larry wants to cut a board that is 4.68 meters long into six equal pieces. How long will each shelf be? '
    '4.68 &divide; 6 =</p>'
    '<p><strong>Step 1.</strong> Rewrite the problem and divide.<br>'
    '<strong>Step 2.</strong> Bring the decimal point up into the answer above its position in the problem.</p>'
    '<p>Each shelf will be <strong>.78</strong> meter long.</p>'
    '<p><em>Example:</em> .512 &divide; 8 =</p>'
    '<p>To show that 8 does not divide into .5, put a zero above the 5. <strong>Answer: .064</strong>.</p>'
    + box("A Second Example", (
        '<p style="margin:0;"><em>John works 35 hours a week. In a week he makes $505.75 before taxes. How much does John make in '
        'one hour?</em><br>'
        '$505.75 &divide; 35 = <strong>$14.45</strong> an hour.</p>'
    ))
    + callout("Common Mistakes to Avoid", (
        'Don&rsquo;t wait until the end to add the decimal point &mdash; bring it straight up into the answer the instant you reach '
        'it in the division, in the exact same column. And if the divisor doesn&rsquo;t go into the first digit(s) after the point, '
        'that spot gets a zero in the answer (like .512 &divide; 8 = .064, not .64).'
    ))
    + callout("Same skill, same video", (
        'This is the same Decimal Arithmetic video from the Add Decimals reading &mdash; rewatch it there for the division portion.'
    ))
)

divide_decimal_body = slim_header("Day 4 &middot; Unit 2 Reading") + meta_line("45-47", "Divide decimals by decimals") + (
    '<h2>Division of Decimals by Decimals</h2>'
    '<p>To divide a decimal by a decimal, first make a new problem. Change the number you are dividing by (the <strong>divisor</strong>) '
    'into a whole number by moving its decimal point to the right end. Then move the decimal point in the other number (the '
    '<strong>dividend</strong>) the same number of places.</p>'
    + box("Breaking It Down", (
        '<p style="margin:0;">You can&rsquo;t easily divide by a decimal, so the trick is to turn the divisor into a whole number '
        'first: move its decimal point all the way to the right. Whatever you do to the divisor, you must do to the dividend too '
        '&mdash; move its decimal point the same number of places (adding zeros if you run out of digits). Once the divisor is a '
        'whole number, this becomes an ordinary decimal-by-whole-number division, just like the previous page.</p>'
    ), accent="blue")
    + '<p><em>Example:</em> How many pieces of pipe, .8 meter long each, can Tony cut from a pipe that is 3.68 meters long? '
    '3.68 &divide; .8 =</p>'
    '<p><strong>Step 1.</strong> Move the decimal point in the divisor, .8, one place to the right to make it a whole number (8).<br>'
    '<strong>Step 2.</strong> Move the decimal point in the dividend, 3.68, one place to the right (36.8).<br>'
    '<strong>Step 3.</strong> Divide, and bring the decimal point up into the answer above its new position.</p>'
    '<p>36.8 &divide; 8 = 4.6, so Tony can cut <strong>4.6, or 4 complete pieces</strong> &mdash; the math gives 4.6, but only 4 whole '
    'pieces of pipe can actually be cut.</p>'
    '<p><em>Example:</em> 5.6 &divide; .07 =</p>'
    '<p>Move both decimal points two places to the right (560 &divide; 7). Since the answer is a whole number, no decimal point is '
    'needed: <strong>80</strong>.</p>'
    + box("A Second Example", (
        '<p style="margin:0;"><em>Charlene drove 267.5 miles on 12.5 gallons of gas. How far did she drive on one gallon?</em><br>'
        '267.5 &divide; 12.5 = <strong>21.4</strong> miles per gallon.</p>'
    ))
    + callout("Common Mistakes to Avoid", (
        'The most common slip is moving the decimal point in only one of the two numbers &mdash; both the divisor AND the dividend '
        'move by the same number of places, every time. And watch real-world remainders: Tony&rsquo;s pipe problem (3.68 &divide; .8 '
        '= 4.6) means only 4 whole pieces can actually be cut, even though the math answer is 4.6.'
    ))
    + callout("Same skill, same video", (
        'This is the same Decimal Arithmetic video from the Add Decimals reading &mdash; rewatch it there for the division portion.'
    ))
)

divide_whole_by_decimal_body = slim_header("Day 4 &middot; Unit 2 Reading") + meta_line("47-48", "Divide whole numbers by decimals") + (
    '<h2>Division of Whole Numbers by Decimals</h2>'
    '<p>To divide a whole number by a decimal, remember to put a decimal point at the right of the whole number. Then move the points '
    'in both the divisor and the dividend &mdash; you will have to put zeros in the dividend.</p>'
    '<p>Not every division problem comes out even. When this happens, choose a place to round to. Then divide one place beyond the '
    'place you want to round to.</p>'
    + box("Breaking It Down", (
        '<p style="margin:0;">This is the same &ldquo;make the divisor a whole number&rdquo; trick as the previous page, just '
        'starting from a whole-number dividend instead of a decimal one. Give the whole number an (invisible) decimal point at its '
        'right end, then move both decimal points the same number of places &mdash; padding the dividend with zeros as needed. '
        'Sometimes the division won&rsquo;t come out even; when that happens, divide one extra place past where you want to round, '
        'then round normally, the same way you rounded decimals on Day 3.</p>'
    ), accent="blue")
    + '<p><em>Example:</em> How many nickels ($.05) are there in eight dollars ($8)? 8 &divide; .05 =</p>'
    '<p><strong>Step 1.</strong> Move the decimal point in the divisor, .05, two places to the right to make it a whole number (5).<br>'
    '<strong>Step 2.</strong> Put a decimal point to the right of 8, then two zeros, and move the point the same two places (800).<br>'
    '<strong>Step 3.</strong> Divide. Since there is no decimal part to the answer, drop the decimal point.</p>'
    '<p>There are <strong>160</strong> nickels in $8.</p>'
    '<p><em>Example:</em> Find 8 &divide; 1.5 to the nearest tenth.</p>'
    '<p>Since you want the nearest tenth, divide to the hundredths place (one place beyond), then round: 8 &divide; 1.5 = 5.33..., '
    'which rounds to <strong>5.3</strong>.</p>'
    + box("A Second Example", (
        '<p style="margin:0;"><em>Sandy paid $6 for 2.2 pounds of lamb. To the nearest cent, what was the price of one pound?</em><br>'
        '$6 &divide; 2.2 = $2.727..., which rounds to <strong>$2.73</strong> a pound.</p>'
    ))
    + callout("Common Mistakes to Avoid", (
        'Don&rsquo;t forget the whole number needs zeros added after its (invisible) decimal point before you can shift it &mdash; '
        '8 &divide; .05 means 8 becomes 8.00 before moving the point. And when a division doesn&rsquo;t terminate, divide one place '
        'further than your target rounding place before you round, so your rounding decision is based on a real digit, not a guess.'
    ))
    + callout("Same skill, same video", (
        'This is the same Decimal Arithmetic video from the Add Decimals reading &mdash; rewatch it there for the division portion.'
    ))
)

day4_want_more_body = (
    WRAP_OPEN
    + banner("Day 4 &middot; Unit 2", "Want More Practice?", "Optional extra videos and practice for today's skills.")
    + box("Adding &amp; Subtracting Decimals", resource_list([
        ("Math Antics - Decimal Arithmetic (video)", f"https://www.youtube.com/watch?v={V_DECIMAL_ARITHMETIC}",
         "Covers adding, subtracting, multiplying, and dividing decimals in one video."),
        ("Khan Academy - Add and subtract decimals", "https://www.khanacademy.org/math/arithmetic-home/arith-decimals/adding-decimals/e/adding_decimals",
         "Practice sets for decimal addition and subtraction, including regrouping."),
    ]))
    + box("Multiplying Decimals", resource_list([
        ("Khan Academy - Multiplying decimals", "https://www.khanacademy.org/math/arithmetic-home/arith-decimals/multiplying-decimals/e/multiplying_decimals",
         "Practice placing the decimal point correctly in a product."),
    ]), accent="blue")
    + box("Dividing Decimals", resource_list([
        ("Division: Remainders vs. Decimals - Math Antics Extras (video)", "https://www.youtube.com/watch?v=LEsLbfMr0mw",
         "A related Math Antics Extras video on how division and decimals connect."),
        ("Khan Academy - Dividing decimals", "https://www.khanacademy.org/math/arithmetic-home/arith-decimals/dividing-decimals/e/dividing_completely",
         "Practice dividing by a whole number and by a decimal."),
    ]))
    + WRAP_CLOSE
)

DAY4_OVERVIEW_BODY = (
    WRAP_OPEN
    + banner("Day 4 &middot; Unit 2: Decimals", "Day 4 Overview",
        "The four operations with decimals &mdash; adding, subtracting, multiplying, and dividing, including the three ways division "
        "can involve decimals &mdash; then a full Unit 2 review, quiz, and test.")
    + box("Learning Objectives Covered Today", (
        '<ul style="margin:0;padding-left:20px;"><li>Add decimals</li><li>Subtract decimals</li><li>Multiply decimals</li>'
        '<li>Divide decimals by whole numbers</li><li>Divide decimals by decimals</li><li>Divide whole numbers by decimals</li></ul>'
    ))
    + box("How Today Works", (
        '<p style="margin:0 0 8px;">Each topic below is a short reading followed by a printable worksheet &mdash; the book&rsquo;s '
        'own practice problems, done on paper with your calculator. These worksheets are <strong>not graded</strong>; check your work '
        'against the Answer Key dropdown at the bottom of each one before moving to the next topic.</p>'
        '<p style="margin:0;">The day ends with the book&rsquo;s own <strong>Decimals Review</strong> (a self-check with a '
        '&ldquo;which pages to review&rdquo; chart built in), then the graded <strong>Unit 2 Quiz</strong> and <strong>Unit 2 '
        'Test</strong>.</p>'
    ), accent="blue")
    + box("Today&rsquo;s Tasks", (
        '<ol style="margin:0;padding-left:20px;"><li>Addition of Decimals &mdash; read, then Worksheet 16</li>'
        '<li>Subtraction of Decimals &mdash; read, then Worksheet 17</li>'
        '<li>Multiplication of Decimals &mdash; read, then Worksheet 18</li>'
        '<li>Division of Decimals by Whole Numbers &mdash; read, then Worksheet 19</li>'
        '<li>Division of Decimals by Decimals &mdash; read, then Worksheet 20</li>'
        '<li>Division of Whole Numbers by Decimals &mdash; read, then Worksheet 21</li>'
        '<li>Decimals Review (self-check)</li><li>Unit 2 Quiz</li><li>Unit 2 Test</li></ol>'
    ))
    + WRAP_CLOSE
)

print("Day 4 reading pages built.")

# ===========================================================================
# WORKSHEET PDF GENERATION (Worksheets 16-21 + Decimals Review), transcribed
# verbatim from Unit 2 Decimals Content Brief.md (Practice 16-21, pp.38-48,
# plus the Decimals Review pp.49-50). All answers independently computed and
# double-checked against the real book page images (see build session notes).
# ===========================================================================

UNIT2_LABEL = "Unit 2: Decimals"


def make_ws(ws_num, topic, pages, horiz=None, horiz_answers=None, word=None, word_answers=None,
            instr="Solve each problem. Show your work."):
    ws = Worksheet(ws_num, topic, pages, unit_label=UNIT2_LABEL)
    ws.add_page()
    ws.name_date_line()
    ws.instructions(instr)
    n = 0
    pairs = []
    if horiz:
        probs = [(i + 1, expr) for i, expr in enumerate(horiz)]
        n += len(horiz)
        ws.horizontal_list(probs, cols=2)
        pairs.extend(zip(range(1, n + 1), horiz_answers))
    if word:
        ws.section_heading("Solve each problem.")
        probs = [(n + i + 1, text) for i, text in enumerate(word)]
        n += len(word)
        ws.word_problems(probs)
        pairs.extend(zip(range(n - len(word) + 1, n + 1), word_answers))
    ws.output(os.path.join(OUTDIR, f"Worksheet-{ws_num}-{topic.replace(' ', '-')}.pdf"))
    ak = AnswerKey(ws_num, topic, pages)
    ak.add_page()
    ak.answers(pairs, cols=4)
    ak.output(os.path.join(OUTDIR, f"Worksheet-{ws_num}-Answer-Key.pdf"))
    print(f"  Worksheet {ws_num}: {topic} -- {n} problems")
    return n


def generate_worksheets():
    print("Generating Unit 2 worksheet PDFs...")

    # -- Worksheet 16: Add Decimals (Practice 16, pp.38-39) -----------------
    horiz16 = [".28 + .3 + .709 =", ".34 + .959 + .6 =", ".3 + .8 + .6 =", ".27 + .94 + .08 =",
               ".68 + .7 + .697 =", ".3 + .4177 + .274 =", "2.1 + 66 + 3.97 =", ".506 + 5.6 + 4 =",
               "70 + 6.256 + .49 =", "5 + .92 + .747 ="]
    horiz16_answers = ["1.289", "1.899", "1.7", "1.29", "2.077", ".9917", "72.07", "10.106", "76.746", "6.667"]
    word16 = [
        "The average April temperature in Chicago is 47.8°. The average April temperature in St. Louis is 8.3° higher than in Chicago. Find the average April temperature for St. Louis.",
        "In 1995 the town of Elmford spent $2.2 million for education. In 1996 it spent $.85 million more. How much did it spend on education in 1996?",
        "On Monday Ann drove 3.7 miles to take her children to school. She also drove 1.9 miles to a gas station, 4.6 miles to a shopping center and 5.8 miles back home. How many miles did she drive in total?",
        "In 1970 there were about 3.7 billion people in the world. In the year 2000 there will be about 2.6 billion more people. What will be the world population in 2000?",
        "The reading on the mileage gauge of Pete's car was 36,405.2 miles on Friday morning. By Sunday night Pete had driven 768.9 more miles. What was the reading Sunday night?",
        "Rachel's normal temperature is 98.6°. When she was ill, her temperature went up 4.9°. What was her temperature when she was ill?",
        "Jack works part-time at a garage. Monday he worked 4.5 hours. Wednesday he worked 3.25 hours. Friday he worked 5 hours. How many hours did he work altogether that week?",
        "At Software Depot, Nita bought a computer game for $35.96, a hint book for $9.49, and a joystick for $39.95. How much did she spend before tax?",
    ]
    word16_answers = ["56.1°", "$3.05 million", "16.0 miles", "6.3 billion", "37,174.1 miles", "103.5°", "12.75 hours", "$85.40"]
    make_ws(16, "Add Decimals", "38-39", horiz=horiz16, horiz_answers=horiz16_answers, word=word16, word_answers=word16_answers)

    # -- Worksheet 17: Subtract Decimals (Practice 17, pp.40-41) ------------
    horiz17 = ["6 - .359 =", "12 - .35 =", ".7 - .482 =", ".38 - .098 =", "4 - .059 =", ".02 - .004 =",
               "3.8 - 2.947 =", "5.8 - .399 =", ".63 - .406 =", "20 - 3.89 =", "6 - 2.075 =", "8.76 - 3 =",
               ".07 - .052 =", "30 - .8 =", ".3 - .049 =", "3 - .35 =", "12.9 - 10.06 =", ".936 - .08 ="]
    horiz17_answers = ["5.641", "11.65", ".218", ".282", "3.941", ".016", ".853", "5.401", ".224", "16.11", "3.925", "5.76",
                        ".018", "29.2", ".251", "2.65", "2.84", ".856"]
    word17 = [
        "The area of the United States is about 3.3 million square miles. The area of Canada is about 3.8 million square miles. How much bigger is Canada in area?",
        "There are about 257.9 million people living in the U.S. About 27.8 million people live in Canada. How many more people live in the U.S. than in Canada?",
        "When George bought his used car, the mileage gauge read 15,023.4 miles. In two months the gauge read 19,376.8 miles. How many miles did George drive the first two months?",
        "Ty Cobb's batting average for his career was .367. Rogers Hornsby's average was .358. How much better was Ty Cobb's average?",
        "Judith is 1.6 meters tall. Her daughter Emma is 1.35 meters tall. How much taller is Judith than her daughter?",
        "In 1980 there were 7.5 million people living in the Chicago area. In 1990 there were 8.1 million in that area. By how much did the population grow from 1980 to 1990?",
        "Deion bought a piece of lumber 2 meters long. From it he cut a piece 1.85 meters long. How long was the leftover piece?",
    ]
    word17_answers = [".5 million sq mi", "230.1 million more", "4,353.4 miles", ".009", ".25 meters", ".6 million", ".15 meters"]
    make_ws(17, "Subtract Decimals", "40-41", horiz=horiz17, horiz_answers=horiz17_answers, word=word17, word_answers=word17_answers)

    # -- Worksheet 18: Multiply Decimals (Practice 18, pp.42-43) ------------
    horiz18 = [".6 × 9.1 =", ".8 × 7.23 =", ".974 × 7 =", ".4 × 83.9 =", "1.9 × 8.6 =", ".96 × 3.3 =",
               "7 × 2.6 =", ".82 × 9 =", "8 × .03 =", ".23 × 71 =", "348 × .05 =", ".16 × 352 =",
               ".12 × 3.5 =", "3.6 × 1.8 =", "25 × 5.25 =", ".09 × .8 =", ".047 × .4 =", ".006 × .07 =",
               ".048 × .66 =", ".0635 × 4 =", "1.2 × .009 ="]
    horiz18_answers = ["5.46", "5.784", "6.818", "33.56", "16.34", "3.168", "18.2", "7.38", ".24", "16.33", "17.4", "56.32",
                        ".42", "6.48", "131.25", ".072", ".0188", ".00042", ".03168", ".254", ".0108"]
    word18 = [
        "Jose weighs 180 pounds. One pound equals .45 kilograms. What is Jose's weight in kilograms?",
        "Adrienne works overtime for $18.60 an hour. Last week she worked 7.5 hours overtime. How much did she make for overtime work?",
        "Ruby bought 2.3 pounds of chicken at $1.79 a pound. How much did she pay? Round your answer to the nearest cent.",
        "Fred walks at an average speed of 3.6 miles per hour. How far can he walk in 2.5 hours?",
        "Mark bought 4.25 feet of lumber. The lumber cost $3.40 a foot. What was the total cost of the lumber?",
    ]
    word18_answers = ["81 kg", "$139.50", "$4.12", "9 miles", "$14.45"]
    make_ws(18, "Multiply Decimals", "42-43", horiz=horiz18, horiz_answers=horiz18_answers, word=word18, word_answers=word18_answers)

    # -- Worksheet 19: Divide Decimals by Whole Numbers (Practice 19, pp.44-45) --
    horiz19 = ["29.6 ÷ 8 =", "3.12 ÷ 6 =", "13.16 ÷ 4 =", "4.368 ÷ 7 =", "2.01 ÷ 3 =", "67.2 ÷ 24 =",
               ".342 ÷ 9 =", ".324 ÷ 12 =", ".702 ÷ 18 =", "1.633 ÷ 23 =", "2.88 ÷ 32 =", ".136 ÷ 8 =",
               "$1.48 ÷ 4 =", "$.96 ÷ 12 =", "$4.20 ÷ 3 =", "$8.25 ÷ 11 =", "$1.35 ÷ 45 =", "$10.08 ÷ 9 ="]
    horiz19_answers = ["3.7", ".52", "3.29", ".624", ".67", "2.8", ".038", ".027", ".039", ".071", ".09", ".017",
                        "$.37", "$.08", "$1.40", "$.75", "$.03", "$1.12"]
    word19 = [
        "Jake is a plumber. He wants to cut a piece of pipe 2.52 meters long into four equal pieces. How long will each piece be?",
        "John works 35 hours a week. In a week he makes $505.75 before taxes. How much does John make in one hour?",
    ]
    word19_answers = [".63 meters", "$14.45"]
    make_ws(19, "Divide Decimals by Whole Numbers", "44-45", horiz=horiz19, horiz_answers=horiz19_answers,
            word=word19, word_answers=word19_answers, instr="Divide each problem.")

    # -- Worksheet 20: Divide Decimals by Decimals (Practice 20, pp.45-47) --
    horiz20 = ["2.38 ÷ .7 =", ".504 ÷ .9 =", "2.34 ÷ .3 =", ".567 ÷ .09 =", ".0348 ÷ .06 =", ".072 ÷ .04 =",
               "7.8 ÷ .003 =", "5.31 ÷ .009 =", "85.02 ÷ .026 =", "2.82 ÷ .006 =", "55.2 ÷ .92 =", "40.45 ÷ .809 ="]
    horiz20_answers = ["3.4", ".56", "7.8", "6.3", ".58", "1.8", "2,600", "590", "3,270", "470", "60", "50"]
    word20 = ["Charlene drove 267.5 miles on 12.5 gallons of gas. How far did she drive on one gallon?"]
    word20_answers = ["21.4 miles"]
    make_ws(20, "Divide Decimals by Decimals", "45-47", horiz=horiz20, horiz_answers=horiz20_answers,
            word=word20, word_answers=word20_answers, instr="Divide each problem.")

    # -- Worksheet 21: Divide Whole Numbers by Decimals (Practice 21, pp.47-48) --
    horiz21 = ["36 ÷ 2.4 =", "30 ÷ .75 =", "39 ÷ .06 =", "54 ÷ 4.5 =", "20 ÷ .08 =", "18 ÷ .036 =",
               "9 ÷ 1.3 = (nearest tenth)", "12 ÷ .7 = (nearest tenth)", "5 ÷ .3 = (nearest tenth)",
               "20 ÷ 1.4 = (nearest hundredth)", "18 ÷ 3.1 = (nearest hundredth)", "1 ÷ .85 = (nearest hundredth)"]
    horiz21_answers = ["15", "40", "650", "12", "250", "500", "6.9", "17.1", "16.7", "14.29", "5.81", "1.18"]
    word21 = [
        "A 50-acre parcel of land is to be divided up into three equal pieces. Find, to the nearest tenth, the number of acres in each piece.",
        "Sandy paid $6 for 2.2 pounds of lamb. To the nearest cent, what was the price of one pound of lamb?",
    ]
    word21_answers = ["16.7 acres", "$2.73"]
    make_ws(21, "Divide Whole Numbers by Decimals", "47-48", horiz=horiz21, horiz_answers=horiz21_answers,
            word=word21, word_answers=word21_answers, instr="Divide each problem. Round where noted.")

    # -- Decimals Review (Self-Paced Practice, pp.49-50) ---------------------
    rv = Worksheet("Review", "Decimals Review", "49-50", unit_label=UNIT2_LABEL)
    rv.add_page()
    rv.name_date_line()
    rv.instructions("These problems cover everything in Unit 2. Solve each one, then check your answers against "
                     "the Answer Key. The chart at the end tells you which pages to revisit for any you miss.")
    review_text = [
        "Write .004 in words.", "Write 8.1 in words.",
        "Write eighteen thousandths as a decimal.", "Write one and eight hundredths as a decimal.",
        "Which decimal is greater, .52 or .504?", "Round 2.38 to the nearest tenth.",
    ]
    review_text_answers = ["four thousandths", "eight and one tenth", ".018", "1.08", ".52", "2.4"]
    n = 0
    pairs_rv = []
    probs = [(i + 1, q) for i, q in enumerate(review_text)]
    n += len(review_text)
    rv.word_problems(probs, blank_lines=1)
    pairs_rv.extend(zip(range(1, n + 1), review_text_answers))

    rv.section_heading("Solve each problem.")
    review_horiz = [".0052 + .84 + .072 =", ".26 + 14.7 + 13 =", "11 - .509 =", "8.3 - 2.052 =", "3.24 - .966 =",
                     ".47 × 9 =", "3.4 × 1.9 =", "4.3 × .38 =", ".110 ÷ 23 = (nearest ten-thousandth)",
                     ".621 ÷ .09 =", "54 ÷ .27 ="]
    review_horiz_answers = [".9172", "27.96", "10.491", "6.248", "2.274", "4.23", "6.46", "1.634", "~.0048", "6.9", "200"]
    probs = [(n + i + 1, expr) for i, expr in enumerate(review_horiz)]
    n += len(review_horiz)
    rv.horizontal_list(probs, cols=2)
    pairs_rv.extend(zip(range(n - len(review_horiz) + 1, n + 1), review_horiz_answers))

    rv.section_heading("Solve each problem.")
    review_word = [
        "According to the 1970 census, there were 8.4 million people in the Los Angeles area. In 1990 there were 6.1 million more people. How many people lived in Los Angeles in 1990?",
        "Jorge is 1.9 meters tall. His son Mateo is 1.05 meters tall. How much taller is Jorge than Mateo?",
        "Jennifer makes $14.90 an hour. How much does she make on a day when she works 8.5 hours?",
        "Joe wants to cut a board that is 10.8 feet long into four equal pieces. How long will each piece be?",
    ]
    review_word_answers = ["14.5 million", ".85 meters", "$126.65", "2.7 feet"]
    probs = [(n + i + 1, text) for i, text in enumerate(review_word)]
    n += len(review_word)
    rv.word_problems(probs)
    pairs_rv.extend(zip(range(n - len(review_word) + 1, n + 1), review_word_answers))

    rv.section_heading("Progress Check")
    rv.set_font("Helvetica", "", 10)
    rv.multi_cell(0, 5.5, "Check your answers against the Answer Key. Then revisit the review pages for any "
                          "problems you missed, and correct your answers before moving on to Unit 3.")
    rv.ln(2)
    chart = [("1 to 5", "32 to 35"), ("6", "35 to 37"), ("7 to 9", "38 to 39"), ("10 to 13", "40 to 41"),
             ("14 to 17", "42 to 43"), ("18 to 21", "44 to 48")]
    rv.set_font("Helvetica", "B", 10)
    rv.cell(70, 7, "If you missed problems")
    rv.cell(0, 7, "Review pages", ln=1)
    rv.set_font("Helvetica", "", 10)
    for missed, review_pages in chart:
        rv.cell(70, 6.5, missed)
        rv.cell(0, 6.5, review_pages, ln=1)

    rv.output(os.path.join(OUTDIR, "Decimals-Review.pdf"))
    ak_rv = AnswerKey("Review", "Decimals Review", "49-50")
    ak_rv.add_page()
    ak_rv.answers(pairs_rv, cols=4)
    ak_rv.output(os.path.join(OUTDIR, "Decimals-Review-Answer-Key.pdf"))
    print(f"  Decimals Review -- {n} problems")

    print("All Unit 2 worksheets generated.\n")


print("Worksheet generation function defined.")

# ===========================================================================
# UPLOAD WORKSHEET PDFs TO CANVAS + CACHE URLS
# ===========================================================================
PDF_URLS_CACHE = os.path.join(OUTDIR, "pdf_urls_unit2.json")


def upload_worksheets():
    print("Uploading Unit 2 worksheet PDFs to Canvas...")
    names = ["Worksheet-16-Add-Decimals", "Worksheet-17-Subtract-Decimals", "Worksheet-18-Multiply-Decimals",
             "Worksheet-19-Divide-Decimals-by-Whole-Numbers", "Worksheet-20-Divide-Decimals-by-Decimals",
             "Worksheet-21-Divide-Whole-Numbers-by-Decimals"]
    urls = {}
    for i, base in enumerate(names, start=16):
        for kind, fname in [("worksheet", f"{base}.pdf"), ("answer_key", f"Worksheet-{i}-Answer-Key.pdf")]:
            local = os.path.join(OUTDIR, fname)
            f = upload_file_to_canvas(COURSE_ID, local, fname)
            if f:
                urls[fname] = f"{SITE_ROOT}/files/{f['id']}/download?download_frd=1&verifier={f.get('uuid', '')}"
                print(f"  uploaded {fname} -> file id {f['id']}")
    for fname in ["Decimals-Review.pdf", "Decimals-Review-Answer-Key.pdf"]:
        local = os.path.join(OUTDIR, fname)
        f = upload_file_to_canvas(COURSE_ID, local, fname)
        if f:
            urls[fname] = f"{SITE_ROOT}/files/{f['id']}/download?download_frd=1&verifier={f.get('uuid', '')}"
            print(f"  uploaded {fname} -> file id {f['id']}")
    with open(PDF_URLS_CACHE, "w", encoding="utf-8") as fh:
        json.dump(urls, fh, indent=2)
    print(f"Cached {len(urls)} PDF URLs to {PDF_URLS_CACHE}\n")
    return urls


def worksheet_description(ws_title, book_pages, pdf_name, ans_pdf_name, urls):
    pdf_url = urls[pdf_name]
    ans_url = urls[ans_pdf_name]
    return (
        WRAP_OPEN
        + banner("Day 4 &middot; Unit 2 Worksheet", ws_title, f"Self-check practice &mdash; not graded. Book pages {book_pages}.")
        + box("", (
            '<p style="margin:0 0 12px;">This worksheet is a clean, printable PDF (typeset from the book\'s own problems) &mdash; '
            'print it, work it on paper with your calculator, then check the Answer Key below before moving on.</p>'
            f'{pdf_link("Download Worksheet (PDF)", pdf_url)}'
        ))
        + f'<details style="margin-top:14px;"><summary style="cursor:pointer;color:#003462;font-weight:bold;">Answer Key</summary>'
          f'<div style="margin-top:10px;">{pdf_link("Download Answer Key (PDF)", ans_url)}</div></details>'
        + WRAP_CLOSE
    )


# ===========================================================================
# UNIT 2 QUIZ + TEST (original questions, not copied from the book -- same
# distinction Unit 1 used: Practice/Worksheet = book-verbatim, Quiz/Test =
# original)
# ===========================================================================

UNIT2_QUIZ_BANNER = WRAP_OPEN + banner("Unit 2 &middot; Decimals", "Unit 2 Quiz",
    "A quick, graded check across all 10 Unit 2 objectives.") + WRAP_CLOSE

unit2_quiz = {
    "type": "quiz", "title": "Unit 2 Quiz", "quiz_type": "assignment",
    "description": UNIT2_QUIZ_BANNER, "points_possible": 20,
    "questions": [
        q_short("In the number 6.483, what digit is in the hundredths place?", 2, "8"),
        q_short("Write “seven and twenty-five thousandths” as a decimal.", 2, "7.025"),
        q_short("Which decimal is greater, .68 or .608?", 2, ".68"),
        q_short("Round 5.647 to the nearest hundredth.", 2, "5.65"),
        q_short("Add: 2.6 + .375 + 14 =", 2, "16.975"),
        q_short("Subtract: 9 − 3.28 =", 2, "5.72"),
        q_short("Multiply: 1.4 × .06 =", 2, ".084", "0.084"),
        q_short("Divide: 8.55 ÷ 5 =", 2, "1.71"),
        q_short("Divide: 4.2 ÷ .07 =", 2, "60"),
        q_short("Divide: 45 ÷ 1.5 =", 2, "30"),
    ],
}

UNIT2_TEST_BANNER = WRAP_OPEN + banner("Unit 2 &middot; Decimals", "Unit 2 Test",
    "A comprehensive, graded test across all 10 Unit 2 objectives.") + WRAP_CLOSE

unit2_test = {
    "type": "quiz", "title": "Unit 2 Test", "quiz_type": "assignment",
    "description": UNIT2_TEST_BANNER, "points_possible": 42,
    "questions": [
        q_short("In the number 3.947, what digit is in the thousandths place?", 2, "7"),
        q_short("Write “twelve and six hundredths” as a decimal.", 2, "12.06"),
        q_short("Which decimal is greatest: .43, .409, or .5?", 2, ".5"),
        q_short("Round 18.362 to the nearest tenth.", 2, "18.4"),
        q_short("Round .0847 to the nearest hundredth.", 2, ".08", "0.08"),
        q_short("Add: 4.8 + 12 + .935 =", 2, "17.735"),
        q_short("Marisol bought groceries totaling $23.47, $8.99, and $15.60. Find the total.", 3, "$48.06", "48.06"),
        q_short("Subtract: 15 − 6.74 =", 2, "8.26"),
        q_short("A rope 8 meters long has a 2.65-meter piece cut from it. How long is the piece that's left?", 3, "5.35 meters", "5.35"),
        q_short("Multiply: 2.3 × .48 =", 2, "1.104"),
        q_short("Diego earns $16.25 an hour. How much does he earn for 6.5 hours of work, to the nearest cent?", 3, "$105.63", "105.63"),
        q_short("Divide: 6.72 ÷ 8 =", 2, ".84", "0.84"),
        q_short("A 12.6-meter cable is cut into 6 equal pieces. How long is each piece?", 3, "2.1 meters", "2.1"),
        q_short("Divide: 3.5 ÷ .05 =", 2, "70"),
        q_short("Divide: .486 ÷ .09 =", 2, "5.4"),
        q_short("Divide: 27 ÷ .45 =", 2, "60"),
        q_short("A 40-pound sack of flour is repackaged into 2.5-pound bags. How many bags can be filled?", 3, "16 bags", "16"),
        q_short("Find 7 ÷ 1.2 to the nearest tenth.", 3, "5.8"),
    ],
}

print("Unit 2 Quiz + Test defined.")


def build_day4_items(urls):
    review_description = (
        WRAP_OPEN
        + banner("Day 4 &middot; Unit 2 Self-Paced Practice", "Decimals Review", "Self-check &mdash; not graded. Book pages 49-50.")
        + box("", (
            '<p style="margin:0 0 12px;">These problems cover everything in Unit 2. Print the PDF, solve each problem, then check '
            'your answers against the Answer Key. Revisit any topic\'s reading page for problems you miss before moving on to the '
            'Unit 2 Quiz.</p>'
            f'{pdf_link("Download Decimals Review (PDF)", urls["Decimals-Review.pdf"])}'
        ))
        + f'<details style="margin-top:14px;"><summary style="cursor:pointer;color:#003462;font-weight:bold;">Answer Key</summary>'
          f'<div style="margin-top:10px;">{pdf_link("Download Answer Key (PDF)", urls["Decimals-Review-Answer-Key.pdf"])}</div></details>'
        + WRAP_CLOSE
    )

    return [
        {"type": "page", "title": "Day 4 Overview", "body": DAY4_OVERVIEW_BODY},
        {"type": "page", "title": "Addition of Decimals — Reading", "body": add_body},
        {"type": "assignment", "title": "Worksheet 16: Add Decimals",
         "description": worksheet_description("Worksheet 16: Add Decimals", "38-39",
             "Worksheet-16-Add-Decimals.pdf", "Worksheet-16-Answer-Key.pdf", urls),
         "points_possible": 0, "submission_types": ["on_paper"]},
        {"type": "page", "title": "Subtraction of Decimals — Reading", "body": subtract_body},
        {"type": "assignment", "title": "Worksheet 17: Subtract Decimals",
         "description": worksheet_description("Worksheet 17: Subtract Decimals", "40-41",
             "Worksheet-17-Subtract-Decimals.pdf", "Worksheet-17-Answer-Key.pdf", urls),
         "points_possible": 0, "submission_types": ["on_paper"]},
        {"type": "page", "title": "Multiplication of Decimals — Reading", "body": multiply_body},
        {"type": "assignment", "title": "Worksheet 18: Multiply Decimals",
         "description": worksheet_description("Worksheet 18: Multiply Decimals", "42-43",
             "Worksheet-18-Multiply-Decimals.pdf", "Worksheet-18-Answer-Key.pdf", urls),
         "points_possible": 0, "submission_types": ["on_paper"]},
        {"type": "page", "title": "Division of Decimals by Whole Numbers — Reading", "body": divide_whole_body},
        {"type": "assignment", "title": "Worksheet 19: Divide Decimals by Whole Numbers",
         "description": worksheet_description("Worksheet 19: Divide Decimals by Whole Numbers", "44-45",
             "Worksheet-19-Divide-Decimals-by-Whole-Numbers.pdf", "Worksheet-19-Answer-Key.pdf", urls),
         "points_possible": 0, "submission_types": ["on_paper"]},
        {"type": "page", "title": "Division of Decimals by Decimals — Reading", "body": divide_decimal_body},
        {"type": "assignment", "title": "Worksheet 20: Divide Decimals by Decimals",
         "description": worksheet_description("Worksheet 20: Divide Decimals by Decimals", "45-47",
             "Worksheet-20-Divide-Decimals-by-Decimals.pdf", "Worksheet-20-Answer-Key.pdf", urls),
         "points_possible": 0, "submission_types": ["on_paper"]},
        {"type": "page", "title": "Division of Whole Numbers by Decimals — Reading", "body": divide_whole_by_decimal_body},
        {"type": "assignment", "title": "Worksheet 21: Divide Whole Numbers by Decimals",
         "description": worksheet_description("Worksheet 21: Divide Whole Numbers by Decimals", "47-48",
             "Worksheet-21-Divide-Whole-Numbers-by-Decimals.pdf", "Worksheet-21-Answer-Key.pdf", urls),
         "points_possible": 0, "submission_types": ["on_paper"]},
        {"type": "assignment", "title": "Decimals Review (Self-Paced Practice)",
         "description": review_description, "points_possible": 0, "submission_types": ["on_paper"]},
        unit2_quiz,
        unit2_test,
        {"type": "page", "title": "Day 4: Want More Practice?", "body": day4_want_more_body},
    ]


# ===========================================================================
# EXECUTE
# ===========================================================================

def push_items(module_id, items):
    handlers = {"page": create_page, "assignment": create_assignment, "quiz": create_quiz}
    for item in items:
        handlers[item["type"]](COURSE_ID, module_id, item, dry_run=False)


if __name__ == "__main__":
    dump_fragments = {
        "day3": {"course_name": "Business Math 26/27", "modules": [
            {"name": "Day 3, Unit 2: Decimals (Place Value, Reading & Writing, Comparing, Rounding)",
             "position": DAY3_POSITION, "items": DAY3_ITEMS}
        ]},
    }

    print("\n=== Generating worksheet PDFs ===")
    generate_worksheets()

    print("=== Uploading worksheets to Canvas ===")
    urls = upload_worksheets()

    DAY4_ITEMS = build_day4_items(urls)
    dump_fragments["day4"] = {"course_name": "Business Math 26/27", "modules": [
        {"name": "Day 4, Unit 2: Decimals (Addition, Subtraction, Multiplication, Division, Review, Quiz, Test)",
         "position": DAY4_POSITION, "items": DAY4_ITEMS}
    ]}

    print("=== Writing fragment JSON files to Master Business Finance Program repo ===")
    with open(os.path.join(FRAGMENT_DIR, "day3-module-fragment.json"), "w", encoding="utf-8") as f:
        json.dump(dump_fragments["day3"], f, indent=2, ensure_ascii=False)
    with open(os.path.join(FRAGMENT_DIR, "day4-module-fragment.json"), "w", encoding="utf-8") as f:
        json.dump(dump_fragments["day4"], f, indent=2, ensure_ascii=False)
    print("  Fragment files written.\n")

    print("=== Creating Day 3 module + items ===")
    day3_module_id = create_module(COURSE_ID, {"name": dump_fragments["day3"]["modules"][0]["name"], "position": DAY3_POSITION})
    push_items(day3_module_id, DAY3_ITEMS)

    print("\n=== Creating Day 4 module + items ===")
    day4_module_id = create_module(COURSE_ID, {"name": dump_fragments["day4"]["modules"][0]["name"], "position": DAY4_POSITION})
    push_items(day4_module_id, DAY4_ITEMS)

    print(f"\nDone. Day 3 module id={day3_module_id}, Day 4 module id={day4_module_id}")
