# -*- coding: utf-8 -*-
"""Build Unit 5: Percent, Day 10 (module position 11) into a local module
fragment for the Business Math course.

Day 10 covers 7 CBO objectives of Unit 5: Percent -- the "percent triangle
taught three ways" middle chunk of the unit: Identify the percent/whole/part,
Find the part, Use proportion to find the part, Find the percent, Use
proportion to find the percent, Find the whole, Use proportion to find the
whole. Each topic is a reading followed by a short, ungraded, native Canvas
practice_quiz self-check -- there are NO worksheets and NO PDFs generated on
Day 10 (unlike Days 7-8), and no printable materials of any kind.

Source: read directly from the real textbook pages (General Math Review:
Basic Skills with Math, Howett & Eichhorn), book pages 98-102 and 105-111,
by a research agent -- Practice 49 (Identifying the Percent, Whole, and
Part), 50 (Finding the Part), 51 (Using Proportion to Find the Part), 54
(Finding the Percent), 55 (Using Proportion to Find the Percent), 57
(Finding the Whole), 58 (Using Proportion to Find the Whole). Note: in the
real book this content is NOT contiguous on the page -- Interest and two
Multi-Step Problems lessons (which belong to Day 11) are physically
interleaved between some of these sections. Day 10's items below are
sequenced in CBO objective order, not raw book page order -- a deliberate,
confirmed decision.

Video IDs verified 2026-09-01 via the YouTube oEmbed API (mathantics
channel confirmed): rR95Cbcjzus (Finding A Percent Of A Number), Uf-Rl1e2I4Q
(What Percent Is It?), HxEQxS0QSwg (Percents Missing Total).

HARD RULE: this script does not import or call anything from
push_course.py or any other build script, and never touches Canvas or the
network. It only writes a local JSON fragment file.
"""
import os
import json

FRAGMENT_DIR = r"C:\Users\jball.VACE\Documents\Claude Projects\Master Business Finance Program\Lesson Planning\Business Math"
DAY10_POSITION = 11
UNIT5_LABEL = "Unit 5: Percent"

# ===========================================================================
# HTML helpers (identical design system to prior Unit rebuild scripts --
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


# ===========================================================================
# Verified real YouTube video IDs (mathantics official channel -- confirmed
# 2026-09-01 via the YouTube oEmbed API. Never guess a video ID.)
# ===========================================================================
V_FINDING_PART = "rR95Cbcjzus"     # Math Antics - Finding A Percent Of A Number
V_FINDING_PERCENT = "Uf-Rl1e2I4Q"  # Math Antics - What Percent Is It?
V_FINDING_WHOLE = "HxEQxS0QSwg"    # Math Antics - Percents Missing Total

# ===========================================================================
# DAY 10 READING PAGES
# ===========================================================================

identify_ppw_body = slim_header("Day 10 &middot; Unit 5 Reading") + meta_line("98", "Identify the percent, the whole, and the part") + (
    '<h2>Identifying the Percent, the Whole, and the Part</h2>'
    '<p>Anne calculated her rent increase. 5% of her current rent of $480 a month is $24.</p>'
    '<p>Anne&rsquo;s situation is a typical percent problem. It has a percent, a whole, and a part.</p>'
    '<p>The percent is easy to identify. It has the % sign. The word <em>of</em> suggests multiplication. The word that follows '
    '<em>of</em> is usually the whole. (For Anne the whole is her monthly rent.) The verb <em>is</em> suggests the = sign. The '
    'product of multiplying the percent times the whole is the part.</p>'
    + box("Breaking It Down", (
        '<p style="margin:0;">This lesson is not computation &mdash; it is sentence-parsing. Three simple clues do almost all the '
        'work: the % sign always marks the <strong>percent</strong>. The word <em>of</em> is usually followed by the '
        '<strong>whole</strong>. The verb <em>is</em> usually comes right before the <strong>part</strong>. Read the sentence once '
        'looking only for those three markers before you try to compute anything.</p>'
    ), accent="blue")
    + '<p><em>Example:</em> Identify the percent, the whole, and the part in the statement: 5% of $480 is $24.</p>'
    '<p>% = 5%, whole = $480, part = $24.</p>'
    + callout("Common Mistakes to Avoid", (
        'Sentence order can vary &mdash; not every problem puts the whole right after &ldquo;of&rdquo; and the part right after '
        '&ldquo;is,&rdquo; in that reading order. For example, in &ldquo;12 is 25% of 48,&rdquo; the part (12) comes '
        '<strong>first</strong> in the sentence, before the word &ldquo;of.&rdquo; Don&rsquo;t just pattern-match word position '
        '&mdash; actually identify which number plays which role.'
    ))
)

finding_part_body = slim_header("Day 10 &middot; Unit 5 Reading") + meta_line("99-100", "Find the part") + (
    '<h2>Finding the Part</h2>'
    '<p>At the Peerless Package Company, 20% of the 35 employees work part-time. How many of the employees work part-time?</p>'
    '<p>In the last lesson you learned that percent &times; whole = part. For Peerless Package, the percent is 20% and the whole '
    'is the 35 employees. To multiply by a percent, first change the percent to a decimal or a fraction. In this lesson you can '
    'practice both methods.</p>'
    '<p>You can also change the percent to a fraction to solve for the part.</p>'
    + box("Breaking It Down", (
        '<p style="margin:0;">Finding the part is just percent &times; whole = part. You can&rsquo;t multiply directly by a percent '
        'sign, so first convert the percent to a decimal or a fraction &mdash; they are just two ways to do the exact same '
        'multiplication. Pick whichever conversion is easier for the numbers in front of you (a percent like 20% converts to a '
        'clean decimal, .2, while a percent like 12 1/2% is often easier as the fraction 1/8).</p>'
    ), accent="blue")
    + '<p><em>Example (decimal method):</em> Use a decimal to find 20% of 35. 20% = .2; 35 &times; .2 = 7. There are 7 part-time '
    'employees.</p>'
    '<p><em>Example (fraction method):</em> Use a fraction to find 20% of 35. 20% = 20/100 = 1/5; 1/5 &times; 35/1 = 7. 20% of 35 '
    'is 7.</p>'
    + callout("Common Mistakes to Avoid", (
        'Don&rsquo;t skip the conversion step &mdash; you cannot multiply a number directly by &ldquo;20%.&rdquo; You have to '
        'convert it to .2 or 1/5 first, and only then multiply by the whole.'
    ))
    + video_embed(V_FINDING_PART, "Math Antics - Finding A Percent Of A Number")
)

proportion_part_body = slim_header("Day 10 &middot; Unit 5 Reading") + meta_line("101-102", "Use proportion to find the part") + (
    '<h2>Using Proportion to Find the Part</h2>'
    '<p>The plant where Alexis works makes hammers. 18% of the hammers are shipped outside the country. One month the factory '
    'produced 400 hammers. How many were shipped outside the country?</p>'
    '<p>Besides first changing a percent to a decimal or changing a percent to a fraction, there is another way to solve percent '
    'problems. Set up a proportion using the model shown here. Then solve the proportion.</p>'
    '<p style="text-align:center;font-size:20px;color:#003462;font-weight:bold;">part/whole = %/100</p>'
    '<p>With a proportion, you do not need to change the percent to a decimal or to a fraction.</p>'
    + box("Breaking It Down", (
        '<p style="margin:0;">The part/whole = %/100 template is the key idea of this reading &mdash; and it is the '
        '<strong>first of three appearances</strong> of this exact same proportion in Unit 5. It will come back twice more '
        '(finding the percent, finding the whole), with only the unknown letter moving to a different spot in the template. Learn '
        'the template once here and you already know most of the next two lessons.</p>'
    ), accent="blue")
    + '<p><em>Example:</em> Use a proportion to find 18% of 400. n/400 = 18/100. n = (400 &times; 18)/100 = 72. 72 hammers were '
    'shipped outside the country.</p>'
    + callout("Common Mistakes to Avoid", (
        'Cross-multiply diagonally, not straight across &mdash; the same rule from Unit 4. And always set the percent&rsquo;s own '
        'ratio as %/100, never something else &mdash; 100 belongs on the bottom of that ratio every time.'
    ))
    + callout("Same skill, same video", (
        'This teaches the same underlying goal as the last reading &mdash; finding a part &mdash; just by a different method. '
        'Rewatch the <em>Math Antics - Finding A Percent Of A Number</em> video from the Finding the Part reading if you want to '
        'see the skill again.'
    ))
)

finding_percent_body = slim_header("Day 10 &middot; Unit 5 Reading") + meta_line("105-106", "Find the percent") + (
    '<h2>Finding the Percent</h2>'
    '<p>Max works 40 hours a week as a landscaper. He spends eight hours every week maintaining equipment. What percent of his '
    'time at work is spent maintaining equipment?</p>'
    '<p>When you studied fractions, you learned how to find what part one number is of another. You made a fraction with the part '
    'as the numerator (top number) and the whole as the denominator (bottom number). The steps are the same for finding what '
    'percent one number is of another. Make a fraction with the part over the whole. Then change the fraction to a percent.</p>'
    + box("Breaking It Down", (
        '<p style="margin:0;">Three steps: put the part over the whole as a fraction, reduce it, then convert that fraction to a '
        'percent. This is the same fraction-to-percent conversion skill from Objective 3 (Percents and Fractions) on Day 9 &mdash; '
        'this lesson just adds the first step of building the fraction from a word problem.</p>'
    ), accent="blue")
    + '<p><em>Example:</em> 8 is what percent of 40? 8/40 = 1/5; 1/5 &times; 100%/1 = 20%. Max spends 20% of his work time '
    'maintaining equipment.</p>'
    + callout("Common Mistakes to Avoid", (
        'Make sure you know which number is the &ldquo;part&rdquo; and which is the &ldquo;whole&rdquo; before you form the '
        'fraction. The sentence can be phrased either order &mdash; &ldquo;X is what percent of Y&rdquo; or &ldquo;what percent of '
        'Y is X&rdquo; &mdash; but Y (the number that follows &ldquo;of&rdquo;) is always the whole, and always belongs on the '
        'bottom.'
    ))
    + video_embed(V_FINDING_PERCENT, "Math Antics - What Percent Is It?")
)

proportion_percent_body = slim_header("Day 10 &middot; Unit 5 Reading") + meta_line("106-107", "Use proportion to find the percent") + (
    '<h2>Using Proportion to Find the Percent</h2>'
    '<p>Donald spends ten hours of every work day away from home. He spends two of those hours driving. What percent of his time '
    'away from home does Donald spend driving?</p>'
    '<p>Proportion is a convenient way to set up percent problems. Use the model shown here.</p>'
    '<p style="text-align:center;font-size:20px;color:#003462;font-weight:bold;">part/whole = %/100</p>'
    + box("Breaking It Down", (
        '<p style="margin:0;">This is the exact same part/whole = %/100 template from the Using Proportion to Find the Part '
        'reading &mdash; the second of its three appearances in Unit 5. The only change is which spot in the template is unknown: '
        'last time it was the part, this time it is the percent.</p>'
    ), accent="blue")
    + '<p><em>Example:</em> 2 is what percent of 10? 2/10 = p/100. p = (2 &times; 100)/10 = 20%. Donald spends 20% of his time away '
    'from home driving.</p>'
    + callout("Common Mistakes to Avoid", (
        'Set up the proportion carefully &mdash; the part still goes over the whole on the left side, and the unknown percent still '
        'goes over 100 on the right side. Only the letter moves; the template itself never changes.'
    ))
    + callout("Same skill, same video", (
        'This teaches the same underlying goal as the last reading &mdash; finding a percent &mdash; just by proportion instead of '
        'the fraction method. Rewatch the <em>Math Antics - What Percent Is It?</em> video from the Finding the Percent reading if '
        'you want to see the skill again.'
    ))
)

finding_whole_body = slim_header("Day 10 &middot; Unit 5 Reading") + meta_line("109-110", "Find the whole") + (
    '<h2>Finding the Whole</h2>'
    '<p>There are 12 mechanics working at Ted&rsquo;s Tire Company. Mechanics are 80% of the total number of employees. How many '
    'employees does Ted&rsquo;s have?</p>'
    '<p>Finding the whole is &ldquo;backwards&rdquo; from finding the part. For Ted&rsquo;s Tire Company, you are looking for the '
    'number of employees that, when multiplied by 80%, gives 12. First change the percent to a fraction or a decimal. Then divide '
    'the part by the fraction or decimal.</p>'
    '<p>It is a good idea to check these &ldquo;backwards&rdquo; problems. To check the example, find 80% of 15. The answer should '
    'be 12.</p>'
    + box("Breaking It Down", (
        '<p style="margin:0;">Finding the Whole is the reverse of Finding the Part &mdash; and it is the most error-prone of the '
        'three, because students default to multiplying out of habit. When you are looking for the <strong>whole</strong> (the '
        'bigger total), you <strong>divide</strong> the part by the percent&rsquo;s decimal or fraction, instead of multiplying.</p>'
    ), accent="blue")
    + '<p><em>Example (fraction method):</em> 80% of what number is 12? 80% = 4/5; 12 &divide; 4/5 = 12 &times; 5/4 = 15.</p>'
    '<p><em>Example (decimal method):</em> 80% = .8; 12 &divide; .8 = 15.</p>'
    '<p>There are 15 employees. Check: 80% of 15 = 12. &#10003;</p>'
    + callout("Common Mistakes to Avoid", (
        'If you multiply here instead of dividing, you will get a much smaller wrong answer. Before you compute, always ask '
        '&ldquo;am I looking for a smaller piece (multiply) or the bigger total (divide)?&rdquo; Finding the whole always means '
        'dividing.'
    ))
    + video_embed(V_FINDING_WHOLE, "Math Antics - Percents Missing Total")
)

proportion_whole_body = slim_header("Day 10 &middot; Unit 5 Reading") + meta_line("110-111", "Use proportion to find the whole") + (
    '<h2>Using Proportion to Find the Whole</h2>'
    '<p>In a recent vote only 30% of the employees at Ace Electronics said they would join a union. Of all the workers, 84 voted '
    'to join a union. How many employees are there at Ace?</p>'
    '<p>Again, proportion is a useful way to set up percent problems. Use the model shown here. Remember that you are looking for '
    'the whole, the total number of employees at Ace Electronics.</p>'
    '<p style="text-align:center;font-size:20px;color:#003462;font-weight:bold;">part/whole = %/100</p>'
    + box("Breaking It Down", (
        '<p style="margin:0;">This closes out Unit 5&rsquo;s &ldquo;three ways, three unknowns&rdquo; structure &mdash; part/whole '
        '= %/100 has now shown up as the way to find the part, the percent, and (here, for the third and final time) the whole. '
        'Same template every time; only the unknown letter&rsquo;s position changes.</p>'
    ), accent="blue")
    + '<p><em>Example:</em> 30% of what number is 84? 84/w = 30/100. w = (84 &times; 100)/30 = 280. There are 280 employees at Ace '
    'Electronics.</p>'
    + callout("Common Mistakes to Avoid", (
        'The unknown whole (w) still belongs on the bottom of the part/whole ratio, on the left side of the proportion &mdash; '
        'don&rsquo;t accidentally set it up as if it were the unknown part. Cross-multiply diagonally and divide by the number left '
        'standing next to w to solve.'
    ))
    + callout("Same skill, same video", (
        'This teaches the same underlying goal as the last reading &mdash; finding the whole &mdash; just by proportion instead of '
        'dividing by a decimal or fraction. Rewatch the <em>Math Antics - Percents Missing Total</em> video from the Finding the '
        'Whole reading if you want to see the skill again.'
    ))
)

day10_want_more_body = (
    WRAP_OPEN
    + banner("Day 10 &middot; Unit 5", "Want More Practice?", "Optional extra videos and practice for today's skills.")
    + box("Percent: Part, Percent, and Whole", resource_list([
        ("Math Antics - Finding A Percent Of A Number (video)", f"https://www.youtube.com/watch?v={V_FINDING_PART}",
         "Covers finding the part when you know the percent and the whole."),
        ("Math Antics - What Percent Is It? (video)", f"https://www.youtube.com/watch?v={V_FINDING_PERCENT}",
         "Covers finding the percent when you know the part and the whole."),
        ("Math Antics - Percents Missing Total (video)", f"https://www.youtube.com/watch?v={V_FINDING_WHOLE}",
         "Covers finding the whole when you know the percent and the part."),
        ("Khan Academy - Percent word problems", "https://www.khanacademy.org/math/pre-algebra/pre-algebra-ratios-rates/pre-algebra-percent-word-problems/a/intro-to-percents",
         "More practice finding the part, percent, and whole."),
    ]))
    + WRAP_CLOSE
)

DAY10_OVERVIEW_BODY = (
    WRAP_OPEN
    + banner("Day 10 &middot; Unit 5: Percent", "Day 10 Overview",
        "The percent triangle &mdash; percent, whole, and part &mdash; taught three times, once for each unknown, and each time "
        "by two different methods.")
    + box("Learning Objectives Covered Today", (
        '<ul style="margin:0;padding-left:20px;">'
        '<li>Identify the percent, the whole, and the part</li>'
        '<li>Find the part</li>'
        '<li>Use proportion to find the part</li>'
        '<li>Find the percent</li>'
        '<li>Use proportion to find the percent</li>'
        '<li>Find the whole</li>'
        '<li>Use proportion to find the whole</li>'
        '</ul>'
    ))
    + box("How Today Works", (
        '<p style="margin:0 0 8px;">Every percent problem has three parts: a <strong>percent</strong>, a <strong>whole</strong>, '
        'and a <strong>part</strong>. Today teaches how to find whichever one of the three is missing &mdash; the part, the '
        'percent, or the whole &mdash; three times in a row, once for each unknown.</p>'
        '<p style="margin:0 0 8px;">Each time, you will learn <strong>two different methods</strong> for finding the missing '
        'piece: first change-to-decimal-or-fraction, then proportion (using the template part/whole = %/100). The proportion '
        'template is the same all three times &mdash; only the unknown letter moves.</p>'
        '<p style="margin:0;">Each topic below is a short reading followed by a short, <strong>ungraded self-check practice '
        'quiz</strong>. These practice quizzes do not count toward your grade &mdash; use them to check your understanding before '
        'moving to the next topic.</p>'
    ), accent="blue")
    + box("Today&rsquo;s Tasks", (
        '<ol style="margin:0;padding-left:20px;">'
        '<li>Identifying the Percent, the Whole, and the Part &mdash; read, then Practice 49</li>'
        '<li>Finding the Part &mdash; read, then Practice 50</li>'
        '<li>Using Proportion to Find the Part &mdash; read, then Practice 51</li>'
        '<li>Finding the Percent &mdash; read, then Practice 54</li>'
        '<li>Using Proportion to Find the Percent &mdash; read, then Practice 55</li>'
        '<li>Finding the Whole &mdash; read, then Practice 57</li>'
        '<li>Using Proportion to Find the Whole &mdash; read, then Practice 58</li>'
        '</ol>'
    ))
    + WRAP_CLOSE
)

print("Day 10 reading pages built.")

# ===========================================================================
# DAY 10 PRACTICE QUIZZES (native Canvas practice_quiz, ungraded self-checks
# -- no worksheets, no PDFs on Day 10)
# ===========================================================================

practice49 = {
    "type": "quiz", "title": "Practice 49: Identify the Percent, the Whole, and the Part", "quiz_type": "practice_quiz",
    "description": WRAP_OPEN + banner("Day 10 &middot; Unit 5 Practice", "Practice 49: Identify the Percent, the Whole, and the Part",
        "Self-check &mdash; not graded. Book page 98.") + WRAP_CLOSE,
    "questions": [
        q_short("Identify the percent, the whole, and the part: 50% of 88 is 44.", 2, "50%, 88, 44"),
        q_short("Identify the percent, the whole, and the part: 12 is 25% of 48.", 2, "25%, 48, 12"),
        q_short("Identify the percent, the whole, and the part: 90% of $300 is $270.", 2, "90%, $300, $270", "90%, 300, 270"),
        q_short("On a test with 20 problems, Maxim got 75% right. He got 15 problems right. Identify the percent, the whole, and the part.", 2, "75%, 20, 15"),
    ],
}

practice50 = {
    "type": "quiz", "title": "Practice 50: Finding the Part", "quiz_type": "practice_quiz",
    "description": WRAP_OPEN + banner("Day 10 &middot; Unit 5 Practice", "Practice 50: Finding the Part",
        "Self-check &mdash; not graded. Book pages 99-100.") + WRAP_CLOSE,
    "questions": [
        q_short("75% of 48 = ?", 1, "36"),
        q_short("30% of 60 = ?", 1, "18"),
        q_short("10% of 18 = ?", 1, "1.8"),
        q_short("35% of 80 = ?", 1, "28"),
        q_short("16% of 300 = ?", 1, "48"),
        q_short("21% of 400 = ?", 1, "84"),
        q_short("12.5% of 56 = ?", 1, "7"),
        q_short("6.5% of 400 = ?", 1, "26"),
        q_short("1.2% of 800 = ?", 1, "9.6"),
        q_short("Mr. and Mrs. Caruso make $32,500 a year. They put 12% of their income into a retirement plan. How much do they put in their retirement plan in a year?", 1, "$3,900", "3900"),
        q_short("The sales tax in Jermaine's state is 6%. She bought a coat for $85. How much was the sales tax on the coat?", 1, "$5.10", "5.10"),
        q_short("60% of 80 = ?", 1, "48"),
        q_short("25% of 32 = ?", 1, "8"),
        q_short("30% of 50 = ?", 1, "15"),
        q_short("20% of 55 = ?", 1, "11"),
        q_short("75% of 48 = ?", 1, "36"),
        q_short("50% of 92 = ?", 1, "46"),
        q_short("35% of 180 = ?", 1, "63"),
        q_short("66 2/3% of 150 = ?", 1, "100"),
        q_short("12 1/2% of 40 = ?", 1, "5"),
        q_short("Ching Mae's English test had 30 questions. She got 90% of them right. How many questions did she get right?", 1, "27"),
        q_short("Raul weighed 144 pounds. He started working out with weights and gained 12 1/2% of his weight. How many pounds did he gain?", 1, "18"),
        q_short("Gloria makes $630 a week. Her employer takes out 20% of her pay for taxes and social security. How much does Gloria's employer take out each week?", 1, "$126", "126"),
    ],
}

practice51 = {
    "type": "quiz", "title": "Practice 51: Use Proportion to Find the Part", "quiz_type": "practice_quiz",
    "description": WRAP_OPEN + banner("Day 10 &middot; Unit 5 Practice", "Practice 51: Use Proportion to Find the Part",
        "Self-check &mdash; not graded. Book pages 101-102.") + WRAP_CLOSE,
    "questions": [
        q_short("Use proportion to find 6% of 250.", 1, "15"),
        q_short("Use proportion to find 75% of 84.", 1, "63"),
        q_short("Use proportion to find 30% of 130.", 1, "39"),
        q_short("Use proportion to find 37.5% of 72.", 1, "27"),
        q_short("Use proportion to find 4.5% of 500.", 1, "22.5"),
        q_short("Use proportion to find 12% of 600.", 1, "72"),
        q_short("Use proportion to find 60% of 380.", 1, "228"),
        q_short("Use proportion to find 50% of 204.", 1, "102"),
        q_short("Use proportion to find 15% of 7,000.", 1, "1,050", "1050"),
        q_short("When Kate bought her house, it was worth $90,000. Now it is worth 140% of the price Kate paid. What is the value of the house now?", 1, "$126,000", "126000"),
        q_short("1,500 people were interviewed in a recent poll. 65% of them approved of the President's foreign policies. How many of them approved?", 1, "975"),
        q_short("The Jays have played 15 games and won 60% of them. How many games have they won?", 1, "9"),
        q_short("There are 45 employees in Arlene's office. 40% of them have worked in the office less than one year. How many of the employees have worked there less than a year?", 1, "18"),
    ],
}

practice54 = {
    "type": "quiz", "title": "Practice 54: Finding the Percent", "quiz_type": "practice_quiz",
    "description": WRAP_OPEN + banner("Day 10 &middot; Unit 5 Practice", "Practice 54: Finding the Percent",
        "Self-check &mdash; not graded. Book pages 105-106.") + WRAP_CLOSE,
    "questions": [
        q_short("12 is what percent of 48?", 1, "25%"),
        q_short("What percent of 32 is 16?", 1, "50%"),
        q_short("What percent of 45 is 36?", 1, "80%"),
        q_short("14 is what percent of 21?", 1, "66 2/3%"),
        q_short("16 is what percent of 160?", 1, "10%"),
        q_short("18 is what percent of 45?", 1, "40%"),
        q_short("What percent of 50 is 15?", 1, "30%"),
        q_short("30 is what percent of 48?", 1, "62.5%", "62 1/2%"),
        q_short("The Mejias make $2,200 a month. They spend $660 a month for food. What percent of their income do the Mejias spend on food?", 1, "30%"),
        q_short("Last year Marvin weighed 220 pounds. He went on a diet and lost 22 pounds. What percent of his weight did he lose?", 1, "10%"),
        q_short("350 people work at the Allied Paper Products factory. 210 workers at the factory are part of the volunteer savings plan. What percent of the workers participate in the savings plan?", 1, "60%"),
    ],
}

practice55 = {
    "type": "quiz", "title": "Practice 55: Use Proportion to Find the Percent", "quiz_type": "practice_quiz",
    "description": WRAP_OPEN + banner("Day 10 &middot; Unit 5 Practice", "Practice 55: Use Proportion to Find the Percent",
        "Self-check &mdash; not graded. Book pages 106-107.") + WRAP_CLOSE,
    "questions": [
        q_short("Use proportion: 15 is what percent of 75?", 1, "20%"),
        q_short("Use proportion: what percent of 48 is 30?", 1, "62.5%", "62 1/2%"),
        q_short("Use proportion: 60 is what percent of 90?", 1, "66 2/3%"),
        q_short("Use proportion: 70 is what percent of 200?", 1, "35%"),
        q_short("Use proportion: what percent of 230 is 23?", 1, "10%"),
        q_short("Use proportion: 95 is what percent of 190?", 1, "50%"),
        q_short("Use proportion: 126 is what percent of 140?", 1, "90%"),
        q_short("Use proportion: 400 is what percent of 320?", 1, "125%"),
        q_short("Use proportion: 27 is what percent of 300?", 1, "9%"),
        q_short("Use proportion: what percent of 200 is 125?", 1, "62.5%", "62 1/2%"),
        q_short("Wallis took a test with 50 problems. She got 42 problems right. What percent of the problems did Wallis get right?", 1, "84%"),
        q_short("Jonelle borrowed $4,000. She had to pay $440 interest on the amount she borrowed. The interest was what percent of the loan?", 1, "11%"),
        q_short("Norman works 20 hours a week for a food co-op. He spends about 12 of those hours making deliveries. What percent of his time working for the co-op is spent making deliveries?", 1, "60%"),
    ],
}

practice57 = {
    "type": "quiz", "title": "Practice 57: Finding the Whole", "quiz_type": "practice_quiz",
    "description": WRAP_OPEN + banner("Day 10 &middot; Unit 5 Practice", "Practice 57: Finding the Whole",
        "Self-check &mdash; not graded. Book pages 109-110.") + WRAP_CLOSE,
    "questions": [
        q_short("60% of what number is 27?", 1, "45"),
        q_short("12 1/2% of what number is 8?", 1, "64"),
        q_short("50% of what number is 14?", 1, "28"),
        q_short("60% of what number is 24?", 1, "40"),
        q_short("25% of what number is 40?", 1, "160"),
        q_short("16 2/3% of what number is 25?", 1, "150"),
        q_short("40% of what number is 52?", 1, "130"),
        q_short("37 1/2% of what number is 45?", 1, "120"),
        q_short("83 1/3% of what number is 35?", 1, "42"),
        q_short("75% of what number is 150?", 1, "200"),
        q_short("70% of the members of a carpenters' union voted to strike. 210 members voted to strike. How many members are there in the union?", 1, "300"),
        q_short("Marcus pays $190 a month on his car loan. This is 10% of his monthly income. Find his monthly income.", 1, "$1,900", "1900"),
        q_short("Maya got 48 questions right on a Spanish test. Her score was 80%. How many questions were on the test?", 1, "60"),
    ],
}

practice58 = {
    "type": "quiz", "title": "Practice 58: Use Proportion to Find the Whole", "quiz_type": "practice_quiz",
    "description": WRAP_OPEN + banner("Day 10 &middot; Unit 5 Practice", "Practice 58: Use Proportion to Find the Whole",
        "Self-check &mdash; not graded. Book pages 110-111.") + WRAP_CLOSE,
    "questions": [
        q_short("Use proportion: 75% of what number is 15?", 1, "20"),
        q_short("Use proportion: 40% of what number is 24?", 1, "60"),
        q_short("Use proportion: 20% of what number is 35?", 1, "175"),
        q_short("Use proportion: 15% of what number is 36?", 1, "240"),
        q_short("Use proportion: 8% of what number is 28?", 1, "350"),
        q_short("Use proportion: 95% of what number is 380?", 1, "400"),
        q_short("The Hawks lost 28 games last season. They lost 35% of the games they played. How many games did the Hawks play?", 1, "80"),
    ],
}

print("Day 10 practice quizzes defined.")


# ===========================================================================
# ASSEMBLE DAY 10 ITEMS
# ===========================================================================

def build_day10_items():
    return [
        {"type": "page", "title": "Day 10 Overview", "body": DAY10_OVERVIEW_BODY},
        {"type": "page", "title": "Identifying the Percent, the Whole, and the Part — Reading", "body": identify_ppw_body},
        practice49,
        {"type": "page", "title": "Finding the Part — Reading", "body": finding_part_body},
        practice50,
        {"type": "page", "title": "Using Proportion to Find the Part — Reading", "body": proportion_part_body},
        practice51,
        {"type": "page", "title": "Finding the Percent — Reading", "body": finding_percent_body},
        practice54,
        {"type": "page", "title": "Using Proportion to Find the Percent — Reading", "body": proportion_percent_body},
        practice55,
        {"type": "page", "title": "Finding the Whole — Reading", "body": finding_whole_body},
        practice57,
        {"type": "page", "title": "Using Proportion to Find the Whole — Reading", "body": proportion_whole_body},
        practice58,
        {"type": "page", "title": "Day 10: Want More Practice?", "body": day10_want_more_body},
    ]


# ===========================================================================
# EXECUTE (local-only: JSON fragment write, no Canvas calls, no PDFs)
# ===========================================================================

if __name__ == "__main__":
    DAY10_ITEMS = build_day10_items()

    fragment = {"course_name": "Business Math 26/27", "modules": [
        {"name": "Day 10, Unit 5: Percent (Finding the Part, Percent, and Whole)",
         "position": DAY10_POSITION, "items": DAY10_ITEMS}
    ]}

    out_path = os.path.join(FRAGMENT_DIR, "day10-module-fragment.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(fragment, f, indent=2, ensure_ascii=False)

    print(f"\nWrote fragment: {out_path}")
    print(f"Total items in Day 10 module: {len(DAY10_ITEMS)}")
    print("Done. (No Canvas calls made -- local file only, no PDFs generated.)")
