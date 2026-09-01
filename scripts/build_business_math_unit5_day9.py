# -*- coding: utf-8 -*-
"""Build Unit 5: Percent, Day 9 (module position 10) into a local module
fragment for the Business Math course.

Day 9 covers the first 4 of Unit 5's 13 CBO objectives (Percent has 13
objectives split across Days 9-11): Write Percents (Practice 45, pp.90-91),
Percents and Decimals (Practice 46, pp.92-94), Percents and Fractions
(Practice 47, pp.94-96), and Common Fractions, Decimals, and Percents
(Practice 48, p.97).

Unlike Day 8 and earlier days, Day 9 has NO printable worksheets and NO PDF
generation -- every practice item is a native Canvas practice_quiz
(ungraded self-check), matching the Decimals-unit precedent for
practice-quiz items referenced in the build instructions.

Source: read directly from the real textbook (General Math Review: Basic
Skills with Math, Howett & Eichhorn) pages 90-97 by a research agent on
2026-09-01; content (explanations, examples, problems, answers) already
verified against the real book. See also the Unit 5 Percent Content Brief
in Lesson Planning/Business Math for additional context.

Video IDs verified real via the YouTube oEmbed API prior to this build:
JeVSmq1Nrpw (Math Antics - What Are Percentages?), kmVfZ9o-2gg (Math
Antics - Percents And Equivalent Fractions).

HARD RULE: this script does not import or call anything from
push_course.py or any sibling build script, and never touches Canvas or
the network. It only writes a local JSON fragment file.
"""
import os
import json

FRAGMENT_DIR = r"C:\Users\jball.VACE\Documents\Claude Projects\Master Business Finance Program\Lesson Planning\Business Math"
DAY9_POSITION = 10
UNIT5_LABEL = "Unit 5: Percent"

# ===========================================================================
# HTML helpers (identical design system to prior days' build scripts --
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


def percent_table(rows):
    """Reproduces the book's Common Fractions, Decimals, and Percents chart
    (p.97) as an actual HTML table, styled to match the page's visual
    system -- navy header row, white body, clean borders."""
    header = (
        '<tr>'
        '<th style="background:#003462;color:white;padding:8px 12px;text-align:left;font-size:13px;">Percent</th>'
        '<th style="background:#003462;color:white;padding:8px 12px;text-align:left;font-size:13px;">Decimal</th>'
        '<th style="background:#003462;color:white;padding:8px 12px;text-align:left;font-size:13px;">Fraction</th>'
        '</tr>'
    )
    body_rows = "".join(
        f'<tr><td style="padding:7px 12px;border-bottom:1px solid #CBD5E1;">{pct}</td>'
        f'<td style="padding:7px 12px;border-bottom:1px solid #CBD5E1;">{dec}</td>'
        f'<td style="padding:7px 12px;border-bottom:1px solid #CBD5E1;">{frac}</td></tr>'
        for pct, dec, frac in rows
    )
    return (f'<table style="border-collapse:collapse;width:100%;max-width:480px;margin:14px 0;'
            f'border:1px solid #CBD5E1;border-radius:4px;overflow:hidden;">{header}{body_rows}</table>')


# ===========================================================================
# Verified real YouTube video IDs (mathantics official channel -- confirmed
# via the YouTube oEmbed API prior to this build. Never guess a video ID.)
# ===========================================================================
V_WHAT_ARE_PERCENTAGES = "JeVSmq1Nrpw"   # Math Antics - What Are Percentages?
V_PERCENTS_FRACTIONS = "kmVfZ9o-2gg"    # Math Antics - Percents And Equivalent Fractions

# ===========================================================================
# DAY 9 READING PAGES
# ===========================================================================

writing_percents_body = slim_header("Day 9 &middot; Unit 5 Reading") + meta_line("90-91", "Write percents") + (
    '<h2>Writing Percents</h2>'
    '<p>Like a fraction or a decimal, a percent shows a part of a whole. Fractions divide a whole into 2 parts or 3 parts or 4 '
    'parts and so on. Decimals divide a whole into 10 parts or 100 parts, or 1,000 parts and so on. The word <em>percent</em> '
    'means &ldquo;out of 100.&rdquo; Percents divide a whole into 100 parts and only 100 parts. A percent is very much like a '
    'two-place decimal (hundredths).</p>'
    '<p>The book illustrates this with a picture: a figure divided into 100 small squares, with 70 of the squares shaded. The '
    'fraction 70/100, which reduces to 7/10, tells how much of the figure is shaded. The decimal .70, which simplifies to .7, also '
    'tells how much of the figure is shaded. 70% of the figure is shaded.</p>'
    '<p>To work with percent, think of a whole as 100%.</p>'
    + box("Breaking It Down", (
        '<p style="margin:0;">Picture a square cut into a 10-by-10 grid &mdash; 100 identical little squares. Shading 70 of those '
        '100 squares is exactly the same amount as the fraction 7/10, the decimal .7, and 70%. All three are just different ways '
        'of writing the same &ldquo;70 out of 100&rdquo; idea. Because a whole is always 100%, two everyday patterns come up '
        'constantly: if a problem gives you the percent used up and asks what percent is left, subtract from 100%; if a problem '
        'tells you something has multiplied (doubled, tripled, quadrupled), multiply 100% by that number.</p>'
    ), accent="blue")
    + '<p><em>Example:</em> Jordan spends 35% of his income for rent. What percent of his income is left for everything else?</p>'
    '<p>100% represents Jordan&rsquo;s total income. To find the percent that goes for everything besides rent, subtract 35% from '
    '100%. &rarr; 100% &minus; 35% = 65%</p>'
    '<p>Jordan has <strong>65%</strong> of his income left after paying rent.</p>'
    '<p><em>Example:</em> In the fifteen years the Johnsons have owned their house, the value of the house has doubled. The value '
    'now is what percent of the value fifteen years ago?</p>'
    '<p>Remember that one whole is 100%. If something doubles, it becomes 2 &times; 100%. &rarr; 2 &times; 100% = 200%</p>'
    '<p>The Johnsons&rsquo; house is worth <strong>200%</strong> of its value fifteen years ago.</p>'
    + box("A Second Example", (
        '<p style="margin:0;"><em>Instructor-authored &mdash; Practice 45&rsquo;s own items already cover both patterns '
        '(subtract-from-100% and multiply-100%), so here&rsquo;s one more subtract-from-100% example.</em><br>'
        'A store reports that 62% of its inventory sold during a clearance sale. What percent of the inventory is still unsold?<br>'
        '100% &minus; 62% = <strong>38%</strong> of the inventory is still unsold.</p>'
    ))
    + callout("Common Mistakes to Avoid", (
        'It is tempting to assume a percent can never go above 100% &mdash; but it can. 100% is only the whole; once something '
        'more than doubles, triples, or grows past its original amount, the percent that describes it climbs right past 100% '
        '(200%, 300%, 400%, and so on). Watch for the word &ldquo;of&rdquo; and phrases like &ldquo;doubled&rdquo; or &ldquo;four '
        'times&rdquo; &mdash; those signal a multiply-100% problem, not a subtract-from-100% one.'
    ))
    + video_embed(V_WHAT_ARE_PERCENTAGES, "Math Antics - What Are Percentages?")
)

percents_decimals_body = slim_header("Day 9 &middot; Unit 5 Reading") + meta_line("92-94", "Convert between percents and decimals") + (
    '<h2>Percents and Decimals</h2>'
    '<p>It is easy to change decimals to percents. Move the decimal point two places to the right and write a percent sign. '
    'Sometimes you will have to put zeros after the decimal to get two places.</p>'
    '<p>To change a percent to a decimal, move the decimal point two places to the left. Then take off the percent sign. '
    'Sometimes you will have to put zeros at the left to get two places.</p>'
    + box("Breaking It Down", (
        '<p style="margin:0;">Both conversions move the decimal point exactly two places &mdash; the only thing that changes is '
        'the direction. Decimal &rarr; percent moves the point two places to the <strong>right</strong> and adds a % sign. '
        'Percent &rarr; decimal moves the point two places to the <strong>left</strong> and drops the % sign. If there aren&rsquo;t '
        'enough digits to move two full places, fill in with a zero first (after the decimal for decimal &rarr; percent, or before '
        'the front digit for percent &rarr; decimal) before you shift the point.</p>'
    ), accent="blue")
    + '<p><em>Change .35 to a percent:</em> .35 = <strong>35%</strong></p>'
    '<p><em>Change .052 to a percent:</em> .052 = <strong>5.2%</strong></p>'
    '<p><em>Change .7 to a percent (add a zero first):</em> .7 = .70 = <strong>70%</strong></p>'
    '<p><em>Change 65% to a decimal:</em> 65% = <strong>.65</strong></p>'
    '<p><em>Change 2.8% to a decimal (add a zero at the left first):</em> 2.8% = 02.8% = <strong>.028</strong></p>'
    '<p><em>Change 20% to a decimal:</em> 20% = <strong>.2</strong> (the trailing zero drops off &mdash; it doesn&rsquo;t change '
    'the value)</p>'
    + callout("Common Mistakes to Avoid", (
        'Watch the &ldquo;add a zero&rdquo; edge cases in both directions. Going decimal &rarr; percent, a number like .7 only has '
        'one decimal place, so write it as .70 first, then shift the point two places right to get 70%. Going percent &rarr; '
        'decimal, a number like 2.8% only has one digit before the decimal point, so write it as 02.8% first, then shift the point '
        'two places left to get .028. Skipping the zero-padding step is the single most common error on these conversions.'
    ))
    + callout("Same skill, same video", (
        'There isn&rsquo;t a separate Math Antics video for decimal-percent conversion &mdash; it&rsquo;s the same video from the '
        'Writing Percents reading (Math Antics - What Are Percentages?). Rewatch it there if you need the basics of what a percent '
        'represents again.'
    ))
)

percents_fractions_body = slim_header("Day 9 &middot; Unit 5 Reading") + meta_line("94-96", "Convert between percents and fractions") + (
    '<h2>Percents and Fractions</h2>'
    '<p>Percents are different from common fractions in two ways. One difference is that 100 is the only number that can be a '
    'denominator for percents. The other difference is that the denominator is not written. Instead of writing 100, we write the '
    '% sign.</p>'
    '<p>One method for changing a fraction to a percent is to multiply the fraction by 100%. The other method is to change the '
    'fraction to a decimal first. Then change the decimal to a percent.</p>'
    '<p>To change a percent to a fraction, write the digits in the percent as the numerator. Write 100 as the denominator. Then '
    'reduce the fraction.</p>'
    '<p>When a percent has a decimal in it, first change the percent to a decimal. Then change the decimal to a fraction and '
    'reduce.</p>'
    '<p>When a percent has a fraction in it, write the digits in the percent as the numerator. Write 100 as the denominator. Then '
    'divide the numerator by the denominator.</p>'
    + box("Breaking It Down", (
        '<p style="margin:0 0 10px;">Fraction &rarr; percent has two valid routes: multiply the fraction by 100% (good when the '
        'fraction multiplies out cleanly), or convert the fraction to a decimal first, then shift the decimal point (good when '
        'long division gives a clean decimal). Either route gets the same answer.</p>'
        '<p style="margin:0;">Percent &rarr; fraction has three sub-cases depending on what the percent looks like: a plain whole '
        'number percent (write it over 100 and reduce), a percent with a decimal in it (convert to a decimal first, then to a '
        'fraction, then reduce), and a percent with a fraction in it (write the digits over 100, then divide numerator by '
        'denominator, which usually means converting a mixed number to an improper fraction first).</p>'
    ), accent="blue")
    + '<p><em>Change 2/5 to a percent (multiply-by-100% method):</em> 2/5 &times; 100% = <strong>40%</strong></p>'
    '<p><em>Change 3/4 to a percent (decimal-first method):</em> 3/4 = .75 = <strong>75%</strong></p>'
    '<p><em>Change 85% to a fraction:</em> 85/100, reduce by 5 &rarr; <strong>17/20</strong></p>'
    '<p><em>Change 8.4% to a fraction:</em> 8.4% = .084 = 84/1,000 &rarr; reduce by 4 &rarr; <strong>21/250</strong></p>'
    '<p><em>Change 58 1/3% to a fraction:</em> (58 1/3)/100 = (175/3) &divide; (100/1) = 175/3 &times; 1/100 = <strong>7/12</strong></p>'
    + callout("Common Mistakes to Avoid", (
        'When a percent has a fraction in it, like 58 1/3%, students often forget to convert the mixed number to an improper '
        'fraction before dividing by 100 &mdash; that&rsquo;s the step that trips people up. Change 58 1/3 to 175/3 first, '
        '<em>then</em> divide by 100 (which means multiplying by 1/100), rather than trying to divide a mixed number directly.'
    ))
    + video_embed(V_PERCENTS_FRACTIONS, "Math Antics - Percents And Equivalent Fractions")
)

common_equivalents_body = slim_header("Day 9 &middot; Unit 5 Reading") + meta_line("97", "Identify common fractions, decimals, and percents") + (
    '<h2>Common Fractions, Decimals, and Percents</h2>'
    '<p>The chart on this page includes some of the fractions, decimals, and percents you will use most often in your work. '
    'Memorize the equivalent fraction and decimal for each percent.</p>'
    + box("Breaking It Down", (
        '<p style="margin:0;">This page isn&rsquo;t a new skill &mdash; it&rsquo;s a memorization chart. The percents below (like '
        '50%, 25%, 33 1/3%) come up constantly in real-world percent problems, and every remaining lesson in this unit &mdash; '
        'finding the part, finding the percent, finding the whole &mdash; goes faster once you can recognize these fraction and '
        'decimal equivalents instantly instead of converting them from scratch every time. Take the time to memorize this table '
        'now; it pays off for the rest of Unit 5.</p>'
    ), accent="blue")
    + percent_table([
        ("50%", ".5", "1/2"), ("25%", ".25", "1/4"), ("75%", ".75", "3/4"),
        ("12 1/2%", ".125", "1/8"), ("37 1/2%", ".375", "3/8"), ("62 1/2%", ".625", "5/8"), ("87 1/2%", ".875", "7/8"),
        ("33 1/3%", ".33 1/3", "1/3"), ("66 2/3%", ".66 2/3", "2/3"),
        ("20%", ".2", "1/5"), ("40%", ".4", "2/5"), ("60%", ".6", "3/5"), ("80%", ".8", "4/5"),
        ("10%", ".1", "1/10"), ("30%", ".3", "3/10"), ("70%", ".7", "7/10"), ("90%", ".9", "9/10"),
        ("16 2/3%", ".16 2/3", "1/6"), ("83 1/3%", ".83 1/3", "5/6"),
    ])
)

day9_want_more_body = (
    WRAP_OPEN
    + banner("Day 9 &middot; Unit 5", "Want More Practice?", "Optional extra videos and practice for today's skills.")
    + box("Percents", resource_list([
        ("Math Antics - What Are Percentages? (video)", f"https://www.youtube.com/watch?v={V_WHAT_ARE_PERCENTAGES}",
         "Covers what a percent is and how it relates to fractions and decimals."),
        ("Math Antics - Percents And Equivalent Fractions (video)", f"https://www.youtube.com/watch?v={V_PERCENTS_FRACTIONS}",
         "Covers converting between percents and fractions."),
        ("Khan Academy - Percent word problems", "https://www.khanacademy.org/math/pre-algebra/pre-algebra-ratios-rates/pre-algebra-percent-word-problems/a/intro-to-percents",
         "A full set of lessons and practice problems on percents."),
        ("GCFGlobal - Percentages", "https://edu.gcfglobal.org/en/percentages/",
         "A workplace-flavored explanation of percents with practice problems."),
    ]))
    + WRAP_CLOSE
)

DAY9_OVERVIEW_BODY = (
    WRAP_OPEN
    + banner("Day 9 &middot; Unit 5: Percent", "Day 9 Overview",
        "The first 4 of Unit 5's 13 objectives -- writing percents, and converting between percents, decimals, and fractions.")
    + box("Learning Objectives Covered Today", (
        '<ul style="margin:0;padding-left:20px;"><li>Write percents</li>'
        '<li>Convert between percents and decimals</li><li>Convert between percents and fractions</li>'
        '<li>Identify common fractions, decimals, and percents</li></ul>'
    ))
    + box("How Today Works", (
        '<p style="margin:0 0 8px;">Each topic below is a short reading followed by a short, <strong>ungraded self-check practice '
        'quiz</strong> right in Canvas &mdash; not a printable worksheet this time. Answer the questions, then use Canvas&rsquo;s '
        'own feedback to check your work before moving to the next topic.</p>'
        '<p style="margin:0;">These practice quizzes are not graded and do not count toward your grade &mdash; they&rsquo;re just '
        'a quick way to check that each skill is sticking before you move on.</p>'
    ), accent="blue")
    + box("Today&rsquo;s Tasks", (
        '<ol style="margin:0;padding-left:20px;"><li>Writing Percents &mdash; read, then Practice 45</li>'
        '<li>Percents and Decimals &mdash; read, then Practice 46</li>'
        '<li>Percents and Fractions &mdash; read, then Practice 47</li>'
        '<li>Common Fractions, Decimals, and Percents &mdash; read, then Practice 48</li></ol>'
    ))
    + WRAP_CLOSE
)

print("Day 9 reading pages built.")

# ===========================================================================
# PRACTICE QUIZZES (native Canvas practice_quiz, ungraded self-check --
# transcribed verbatim from the real Unit 5 textbook pages, Practice 45-48,
# pp.90-97)
# ===========================================================================

practice45 = {
    "type": "quiz", "title": "Practice 45: Write Percents", "quiz_type": "practice_quiz",
    "description": WRAP_OPEN + banner("Day 9 &middot; Unit 5 Practice", "Practice 45: Write Percents",
        "Self-check &mdash; not graded. Book pages 90-91.") + WRAP_CLOSE,
    "questions": [
        q_short("The Rodriguez family has paid off 75% of their mortgage. What percent of the mortgage do they still have to pay?", 1, "25%"),
        q_short("One evening during a flu epidemic, 30% of Marla's students were absent from her exercise class. What percent of the students came to class?", 1, "70%"),
        q_short("Junior got 82% of the problems right on his last math test. What percent of the problems did he get wrong?", 1, "18%"),
        q_short("12% of the employees at the Municipal Hospital walk to work. What percent arrive by some means other than walking?", 1, "88%"),
        q_short("Serena makes four times what she made when she first got out of school. Her income now is what percent of her income when she first left school?", 1, "400%"),
        q_short("The current population of Eastport is three times what it was in 1960. The population now is what percent of the 1960 population?", 1, "300%"),
    ],
}

practice46 = {
    "type": "quiz", "title": "Practice 46: Convert Between Percents and Decimals", "quiz_type": "practice_quiz",
    "description": WRAP_OPEN + banner("Day 9 &middot; Unit 5 Practice", "Practice 46: Convert Between Percents and Decimals",
        "Self-check &mdash; not graded. Book pages 92-94.") + WRAP_CLOSE,
    "questions": [
        q_short("Change .65 to a percent.", 1, "65%"),
        q_short("Change .06 to a percent.", 1, "6%"),
        q_short("Change .045 to a percent.", 1, "4.5%"),
        q_short("Change .16 2/3 to a percent.", 1, "16 2/3%"),
        q_short("Change .8 to a percent.", 1, "80%"),
        q_short("Change .25 to a percent.", 1, "25%"),
        q_short("Change .06 1/4 to a percent.", 1, "6 1/4%"),
        q_short("Change .82 to a percent.", 1, "82%"),
        q_short("Change 2.8 to a percent.", 1, "280%"),
        q_short("Change .5 to a percent.", 1, "50%"),
        q_short("Change .625 to a percent.", 1, "62.5%"),
        q_short("Change 55% to a decimal.", 1, ".55", "0.55"),
        q_short("Change 8% to a decimal.", 1, ".08", "0.08"),
        q_short("Change 12.5% to a decimal.", 1, ".125", "0.125"),
        q_short("Change 2% to a decimal.", 1, ".02", "0.02"),
        q_short("Change 6.4% to a decimal.", 1, ".064", "0.064"),
        q_short("Change 33 1/3% to a decimal.", 1, ".33 1/3", "0.33 1/3"),
        q_short("Change 60% to a decimal.", 1, ".6", "0.6"),
        q_short("Change 225% to a decimal.", 1, "2.25"),
        q_short("Change 90% to a decimal.", 1, ".9", "0.9"),
        q_short("Change 0.4% to a decimal.", 1, ".004", "0.004"),
        q_short("Change 20% to a decimal.", 1, ".2", "0.2"),
        q_short("Change 500% to a decimal.", 1, "5"),
    ],
}

practice47 = {
    "type": "quiz", "title": "Practice 47: Convert Between Percents and Fractions", "quiz_type": "practice_quiz",
    "description": WRAP_OPEN + banner("Day 9 &middot; Unit 5 Practice", "Practice 47: Convert Between Percents and Fractions",
        "Self-check &mdash; not graded. Book pages 94-96.") + WRAP_CLOSE,
    "questions": [
        q_short("Change 7/10 to a percent.", 1, "70%"),
        q_short("Change 3/5 to a percent.", 1, "60%"),
        q_short("Change 1/9 to a percent.", 1, "11 1/9%"),
        q_short("Change 9/50 to a percent.", 1, "18%"),
        q_short("Change 8/25 to a percent.", 1, "32%"),
        q_short("Change 3/8 to a percent.", 1, "37.5%", "37 1/2%"),
        q_short("Change 1/3 to a percent.", 1, "33 1/3%"),
        q_short("Change 1/2 to a percent.", 1, "50%"),
        q_short("Change 5/12 to a percent.", 1, "41 2/3%"),
        q_short("Change 9/20 to a percent.", 1, "45%"),
        q_short("Change 1/16 to a percent.", 1, "6.25%", "6 1/4%"),
        q_short("Change 1/4 to a percent.", 1, "25%"),
        q_short("Change 35% to a fraction, reduced.", 1, "7/20"),
        q_short("Change 2% to a fraction, reduced.", 1, "1/50"),
        q_short("Change 24% to a fraction, reduced.", 1, "6/25"),
        q_short("Change 30% to a fraction, reduced.", 1, "3/10"),
        q_short("Change 44% to a fraction, reduced.", 1, "11/25"),
        q_short("Change 6% to a fraction, reduced.", 1, "3/50"),
        q_short("Change 150% to a fraction, reduced.", 1, "1 1/2", "3/2"),
        q_short("Change 3% to a fraction, reduced.", 1, "3/100"),
        q_short("Change 4.8% to a fraction, reduced.", 1, "6/125"),
        q_short("Change 10.5% to a fraction, reduced.", 1, "21/200"),
        q_short("Change .04% to a fraction, reduced.", 1, "1/2,500", "1/2500"),
        q_short("Change 2.75% to a fraction, reduced.", 1, "11/400"),
        q_short("Change 12 1/2% to a fraction, reduced.", 1, "1/8"),
        q_short("Change 83 1/3% to a fraction, reduced.", 1, "5/6"),
        q_short("Change 42 6/7% to a fraction, reduced.", 1, "3/7"),
        q_short("Change 8 1/3% to a fraction, reduced.", 1, "1/12"),
        q_short("Change 90% to a fraction, reduced.", 1, "9/10"),
        q_short("Change 215% to a fraction, reduced.", 1, "2 3/20", "43/20"),
        q_short("Change 6.4% to a fraction, reduced.", 1, "8/125"),
        q_short("Change 22 2/9% to a fraction, reduced.", 1, "2/9"),
    ],
}

practice48 = {
    "type": "quiz", "title": "Practice 48: Common Fractions, Decimals, and Percents", "quiz_type": "practice_quiz",
    "description": WRAP_OPEN + banner("Day 9 &middot; Unit 5 Practice", "Practice 48: Common Fractions, Decimals, and Percents",
        "Self-check &mdash; not graded. Book page 97.") + WRAP_CLOSE,
    "questions": [
        q_short("Give the decimal and fraction equivalents of 50%.", 1, "0.5, 1/2", ".5, 1/2"),
        q_short("Give the decimal and fraction equivalents of 25%.", 1, "0.25, 1/4", ".25, 1/4"),
        q_short("Give the decimal and fraction equivalents of 75%.", 1, "0.75, 3/4", ".75, 3/4"),
        q_short("Give the decimal and fraction equivalents of 12 1/2%.", 1, "0.125, 1/8", ".125, 1/8"),
        q_short("Give the decimal and fraction equivalents of 37 1/2%.", 1, "0.375, 3/8", ".375, 3/8"),
        q_short("Give the decimal and fraction equivalents of 62 1/2%.", 1, "0.625, 5/8", ".625, 5/8"),
        q_short("Give the decimal and fraction equivalents of 87 1/2%.", 1, "0.875, 7/8", ".875, 7/8"),
        q_short("Give the decimal and fraction equivalents of 33 1/3%.", 1, "0.33 1/3, 1/3", ".33 1/3, 1/3"),
        q_short("Give the decimal and fraction equivalents of 66 2/3%.", 1, "0.66 2/3, 2/3", ".66 2/3, 2/3"),
        q_short("Give the decimal and fraction equivalents of 20%.", 1, "0.2, 1/5", ".2, 1/5"),
        q_short("Give the decimal and fraction equivalents of 40%.", 1, "0.4, 2/5", ".4, 2/5"),
        q_short("Give the decimal and fraction equivalents of 60%.", 1, "0.6, 3/5", ".6, 3/5"),
        q_short("Give the decimal and fraction equivalents of 80%.", 1, "0.8, 4/5", ".8, 4/5"),
        q_short("Give the decimal and fraction equivalents of 10%.", 1, "0.1, 1/10", ".1, 1/10"),
        q_short("Give the decimal and fraction equivalents of 30%.", 1, "0.3, 3/10", ".3, 3/10"),
        q_short("Give the decimal and fraction equivalents of 70%.", 1, "0.7, 7/10", ".7, 7/10"),
        q_short("Give the decimal and fraction equivalents of 90%.", 1, "0.9, 9/10", ".9, 9/10"),
        q_short("Give the decimal and fraction equivalents of 16 2/3%.", 1, "0.16 2/3, 1/6", ".16 2/3, 1/6"),
        q_short("Give the decimal and fraction equivalents of 83 1/3%.", 1, "0.83 1/3, 5/6", ".83 1/3, 5/6"),
    ],
}

print("Practice 45-48 defined.")


# ===========================================================================
# ASSEMBLE DAY 9 ITEMS
# ===========================================================================

def build_day9_items():
    return [
        {"type": "page", "title": "Day 9 Overview", "body": DAY9_OVERVIEW_BODY},
        {"type": "page", "title": "Writing Percents — Reading", "body": writing_percents_body},
        practice45,
        {"type": "page", "title": "Percents and Decimals — Reading", "body": percents_decimals_body},
        practice46,
        {"type": "page", "title": "Percents and Fractions — Reading", "body": percents_fractions_body},
        practice47,
        {"type": "page", "title": "Common Fractions, Decimals, and Percents — Reading", "body": common_equivalents_body},
        practice48,
        {"type": "page", "title": "Day 9: Want More Practice?", "body": day9_want_more_body},
    ]


# ===========================================================================
# EXECUTE (local-only: JSON fragment write, no Canvas calls, no network)
# ===========================================================================

if __name__ == "__main__":
    DAY9_ITEMS = build_day9_items()

    fragment = {"course_name": "Business Math 26/27", "modules": [
        {"name": "Day 9, Unit 5: Percent (Writing Percents, Percent-Decimal-Fraction Conversions)",
         "position": DAY9_POSITION, "items": DAY9_ITEMS}
    ]}

    out_path = os.path.join(FRAGMENT_DIR, "day9-module-fragment.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(fragment, f, indent=2, ensure_ascii=False)

    print(f"\nWrote fragment: {out_path}")
    print(f"Total items in Day 9 module: {len(DAY9_ITEMS)}")
    print("Done. (No Canvas calls made -- local files only.)")
