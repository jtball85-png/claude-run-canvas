# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from worksheet_pdf import Worksheet, AnswerKey, OUTDIR, NAVY, GOLD, TEAL, GRAY, BLACK


# ===========================================================================
# Worksheet 4: Addition with Carrying (pp.12-13, answers p.174)
# ===========================================================================
grid4 = [
    ("44","+","57"),("78","+","24"),("37","+","63"),("91","+","89"),("46","+","98"),("73","+","28"),("68","+","35"),
    ("15","+","88"),("74","+","56"),("63","+","79"),("84","+","28"),("97","+","36"),("46","+","99"),("67","+","63"),
    ("68","+","46"),("87","+","75"),("89","+","52"),("53","+","27"),("62","+","48"),("18","+","55"),("77","+","66"),
    ("341","+","59"),("228","+","85"),("368","+","92"),("625","+","77"),("439","+","46"),("773","+","96"),
    ("48","+","485"),("92","+","378"),("57","+","974"),("65","+","573"),("83","+","267"),("24","+","388"),
    ("775","+","638"),("593","+","549"),("206","+","297"),("335","+","866"),("184","+","499"),("288","+","827"),
]
grid4_answers = [101,102,100,180,144,101,103, 103,130,142,112,133,145,130, 114,162,141,80,110,73,143,
                 400,313,460,702,485,869, 533,470,1031,638,350,412, 1413,1142,503,1201,683,1115]
horiz4 = ["739 + 494 =","867 + 584 =","766 + 804 =","932 + 1,478 =","2,551 + 488 =","368 + 2,944 =",
          "6,544 + 2,476 =","3,982 + 1,077 =","1,256 + 4,855 =","10,649 + 23,288 =","53,279 + 17,072 ="]
horiz4_answers = [1233,1451,1570,2410,3039,3312,9020,5059,6111,33937,70351]
word4 = [
    "The distance from New York to Cleveland is 507 miles. The distance from Cleveland to Chicago is 343 miles. What is the distance from New York to Chicago by way of Cleveland?",
    "In a recent election for mayor, Mr. Green got 4,987 votes and Mr. Munro got 4,062 votes. Find the total number of votes cast for these two candidates.",
    "Sam's truck weighs 3,478 pounds. If he loads it with 1,800 pounds of topsoil, what is the combined weight of the truck and the topsoil?",
    "The Johnsons pay $548 a month for rent and $176 a month on their car loan. What is the total of these monthly expenses?",
    "In June volunteer firefighters raised $16,479 toward the purchase of a new vehicle. In July they raised another $14,208. Altogether how much money did they raise in June and July?",
]
word4_answers = ["850 miles", "9,049 votes", "5,278 pounds", "$724", "$30,687"]

# ===========================================================================
# Worksheet 5: Addition of More Than Two Numbers (pp.14-15, answers p.175)
# ===========================================================================
grid5 = [
    ("17","88","53"),("44","60","67"),("38","27","69"),("47","96","80"),("39","53","58"),("24","25","73"),("43","44","19"),
    ("26","55","66"),("45","32","29"),("59","80","41"),("88","47","70"),("66","25","63"),("56","63","34"),("12","84","57"),
    ("236","1,940","375"),("808","2,767","741"),("375","3,086","829"),("686","6,421","506"),("327","8,448","338"),
    ("58","964","4,277","52"),("23","158","3,284","41"),("77","841","1,624","12"),("94","349","6,953","54"),("79","926","1,756","88"),
]
grid5_answers = [158,171,134,223,150,122,106, 147,106,180,205,154,153,153, 2551,4316,4290,7613,9113, 5351,3506,2554,7450,2849]
horiz5 = ["318 + 9,907 + 24,063 =","7,613 + 24 + 88,552 =","8,016 + 11,238 + 127 =","43 + 1,752 + 18,406 =",
          "79,088 + 314 + 2,607 =","935 + 22,463 + 8,142 ="]
horiz5_answers = [34288,96189,19381,20201,82009,31540]
word5 = ["In March Don's Music Shop sold 1,026 tapes, in April they sold 963 tapes, and in May they sold 1,372 tapes. What were the total sales for those three months?",
         "For lunch Manny had a bowl of chicken soup (207 calories), a ham sandwich (324 calories), coffee with cream (30 calories), and a piece of apple pie (330 calories). What was the total number of calories in his lunch?",
         "Gordon paid $115 for new brakes, $19 for a new shock absorber, and $18 for an oil change. Find the total of these items."]
word5_answers = ["3,361 tapes","891 calories","$152"]

# ===========================================================================
# Worksheet 6: Subtraction with Regrouping (pp.16-17, answers p.175)
# ===========================================================================
grid6 = [
    ("58","-","29"),("96","-","48"),("47","-","28"),("58","-","19"),("51","-","43"),("32","-","16"),("93","-","65"),
    ("52","-","25"),("64","-","38"),("25","-","16"),("87","-","18"),("91","-","55"),("33","-","16"),("46","-","28"),
    ("811","-","243"),("572","-","418"),("467","-","199"),("340","-","238"),("551","-","365"),("760","-","467"),
    ("6,175","-","496"),("7,240","-","384"),("5,628","-","979"),("6,425","-","556"),("3,183","-","287"),
    ("4,236","-","1,448"),("5,668","-","2,699"),("6,673","-","3,887"),("4,290","-","2,947"),("3,837","-","2,608"),
]
grid6_answers = [29,48,19,39,8,16,28, 27,26,9,69,36,17,18, 568,154,268,102,186,293, 5679,6856,4649,5869,2896, 2788,2969,2786,1343,1229]
horiz6 = ["564 - 85 =","414 - 56 =","666 - 79 =","5,335 - 2,914 =","2,414 - 1,671 =","7,380 - 4,093 =",
          "15,624 - 9,587 =","34,124 - 5,025 =","86,472 - 9,913 ="]
horiz6_answers = [479,358,587,2421,743,3287,6037,29099,76559]
word6 = ["683 people signed up to go on a trip to Miami. 506 people actually went on the trip. How many people who signed up did not go?",
         "The Garcias must drive 413 miles to get to their son's house. They stopped to eat lunch after they had driven 225 miles. How much farther did they have to drive?",
         "Sam Brown earns $23,246 a year. Jane Brown earns $29,175 a year. How much more does Jane make in a year than Sam?",
         "The Globe Theatre holds 420 people. At a Saturday night show, 87 seats were empty. How many people were at the show that night?"]
word6_answers = ["177 people","188 miles","$5,929","333 people"]

# ===========================================================================
# Worksheet 7: Regrouping with Zeros (pp.18-19, answers p.175)
# ===========================================================================
grid7 = [
    ("801","-","236"),("407","-","209"),("503","-","388"),("808","-","619"),("506","-","218"),("707","-","379"),
    ("706","-","267"),("503","-","125"),("802","-","708"),("901","-","355"),("704","-","477"),("206","-","168"),
    ("600","-","226"),("800","-","354"),("500","-","189"),("900","-","614"),("300","-","108"),("400","-","376"),
    ("4,000","-","1,256"),("3,000","-","2,338"),("8,000","-","4,411"),("2,000","-","1,950"),("7,000","-","3,076"),("6,000","-","2,447"),
]
grid7_answers = [565,198,115,189,288,328, 439,378,94,546,227,38, 374,446,311,286,192,24, 2744,662,3589,50,3924,3553]
horiz7 = ["7,000 - 1,270 =","3,000 - 1,681 =","9,000 - 4,023 =","18,007 - 5,668 =","20,050 - 9,266 =","30,600 - 9,482 =",
          "90,040 - 18,255 =","60,000 - 13,478 =","40,005 - 20,386 ="]
horiz7_answers = [5730,1319,4977,12339,10784,21118,71785,46522,19619]
word7 = ["The town of Midvale wants to raise $850,000 to build a new health center. They have collected $473,260 so far. How much more money do they need?",
         "The Martinez family bought a house for $128,000. They made a down payment of $19,200. How much more do they owe for the house?",
         "Frank borrowed $2,800 to buy a used car. So far he has paid back $1,675. How much more does Frank owe on the loan?",
         "The U.S. produces 7,120,000 barrels of crude oil each day. Iraq produces 450,000 barrels a day. In one day, the U.S. produces how much more oil than Iraq?"]
word7_answers = ["$376,740","$108,800","$1,125","6,670,000 barrels"]

# ===========================================================================
# Worksheet 8: Multiplication with Carrying (pp.20-21, answers p.176)
# ===========================================================================
grid8 = [
    ("74","x","6"),("82","x","9"),("37","x","8"),("68","x","5"),("39","x","4"),("22","x","9"),("54","x","3"),
    ("36","x","38"),("42","x","65"),("25","x","43"),("84","x","36"),("77","x","46"),("64","x","55"),("33","x","78"),
]
grid8_answers = [444,738,296,340,156,198,162, 1368,2730,1075,3024,3542,3520,2574]
horiz8 = ["778 x 63 =","46 x 684 =","277 x 28 =","82 x 756 =","24 x 866 =","679 x 34 =","73 x 492 =","536 x 57 =",
          "48 x 30 =","75 x 50 =","60 x 167 =","20 x 396 ="]
horiz8_answers = [49014,31464,7756,61992,20784,23086,35916,30552,1440,3750,10020,7920]
word8 = ["Rodney makes $370 a week. There are 52 weeks in a year. How much does Rodney make in one year?",
         "One gallon of paint costs $16. Find the price of seven gallons of paint.",
         "Donell can drive 27 miles on one gallon of gasoline. How far can he drive on 12 gallons of gasoline?",
         "There are 12 inches in one foot. How many inches long is a board that measures 15 feet?",
         "Marcella drove at an average speed of 64 mph for three hours. How far did she drive?",
         "Jose makes $14 an hour. How much does he earn in a week if he works 35 hours?",
         "Mark is paying back a car loan. He has to pay $160 a month for 24 months. Find the total amount he is paying back."]
word8_answers = ["$19,240","$112","324 miles","180 inches","192 miles","$490","$3,840"]

# ===========================================================================
# Worksheet 9: Division by One Digit (pp.22-23, answers p.176)
# ===========================================================================
div9 = [("3","141"),("9","207"),("2","170"),("5","280"),("7","308"), ("8","616"),("7","252"),("6","270"),("5","345"),("4","348"),
        ("3","237"),("6","348"),("5","320"),("8","704"),("3","276"), ("9","2,484"),("2","1,678"),("7","2,562"),("3","2,553"),("6","5,568")]
div9_answers = [47,23,85,56,44, 77,36,45,69,87, 79,58,64,88,92, 276,839,366,851,928]
word9 = ["Three friends equally shared a raffle prize of $750. How much did each of them get?",
         "The Simpsons paid $13,800 for a five-acre piece of land. What was the price of one acre?"]
word9_answers = ["$250","$2,760"]

# ===========================================================================
# Worksheet 10: Division with Remainders (pp.24-25, answers p.176)
# ===========================================================================
div10 = [("7","292"),("2","79"),("9","204"),("6","316"),("3","236"), ("4","243"),("3","169"),("8","357"),("7","515"),("6","398"),
          ("5","467"),("9","698"),("8","300"),("2","199"),("7","519"), ("4","270"),("3","245"),("7","353"),("9","431"),("5","328")]
div10_answers = ["41r5","39r1","22r6","52r4","78r2", "60r3","56r1","44r5","73r4","66r2", "93r2","77r5","37r4","99r1","74r1", "67r2","81r2","50r3","47r8","65r3"]
horiz10 = ["1,542 \u00f7 8 =","5,050 \u00f7 7 =","2,743 \u00f7 9 =","1,760 \u00f7 3 =","3,845 \u00f7 6 =","7,355 \u00f7 9 =","7,366 \u00f7 8 =","2,277 \u00f7 5 =",
           "2,183 \u00f7 8 =","4,765 \u00f7 6 =","1,937 \u00f7 2 =","2,330 \u00f7 4 ="]
horiz10_answers = ["192r6","721r3","304r7","586r2","640r5","817r2","920r6","455r2","272r7","794r1","968r1","582r2"]
word10 = ["To make a climbing toy for her children, Mary is sawing pieces of wood each 4 feet long from a piece that is 19 feet long. How many pieces can Mary cut from the long piece?",
          "Using the same information: assuming no waste, what will be the length of the remaining piece?",
          "Antonio is a carpenter. He needs 9 feet of molding to trim small windows in an attic. He has a total of 40 feet of molding. How many windows can he trim with his supply of molding?",
          "Using the same information: if Antonio uses his supply of molding for attic windows, how many feet of molding will be left?"]
word10_answers = ["4 pieces","3 feet","4 windows","4 feet"]

# ===========================================================================
# Worksheet 11: Division by Larger Numbers (pp.26-27, answers p.177)
# ===========================================================================
div11 = [("24","192"),("89","623"),("38","228"),("62","310"), ("78","732"),("18","105"),("87","360"),("60","495"),
          ("41","1,968"),("67","3,752"),("52","3,380"),("49","2,548"), ("23","2,093"),("72","5,544"),("54","3,510"),("28","2,492")]
div11_answers = [8,7,6,5, "9r30","5r15","4r12","8r15", 48,56,65,52, 91,77,65,89]
horiz11 = ["1,616 \u00f7 22 =","6,910 \u00f7 85 =","1,412 \u00f7 39 =","2,406 \u00f7 91 =","2,554 \u00f7 86 =","2,216 \u00f7 44 =","6,237 \u00f7 76 =","2,132 \u00f7 29 ="]
horiz11_answers = ["73r10","81r25","36r8","26r40","29r60","50r16","82r5","73r15"]
word11 = ["How many two-pound boxes can be filled with 178 pounds of salt?",
          "Last year the Melinos paid $7,440 in mortgage payments. There are 12 months in a year. How much did they pay each month?",
          "Nora and Doug bought a new TV for $612. They agreed to make 17 equal monthly payments. How much will they pay each month?",
          "There are 16 ounces in a pound. How many pounds are there in 560 ounces?"]
word11_answers = ["89 boxes","$620","$36","35 pounds"]

# ===========================================================================
# Whole Numbers Review (pp.28-29, answers p.177) -- Self-Paced Practice
# ===========================================================================
review_fill = ["60,009,040 is read \"sixty ___, nine ___, forty.\" What are the two missing words (in order)?",
               "5,300,000 is read \"five ___, three hundred ___.\" What are the two missing words (in order)?"]
review_fill_answers = ["million, thousand","million, thousand"]
review_figures = ["Write \"fifteen thousand, two hundred six\" in figures.","Write \"four million, one hundred twenty thousand, eight\" in figures."]
review_figures_answers = ["15,206","4,120,008"]
review_misc = ["What is 328 rounded to the nearest ten?","What is 19,512 rounded to the nearest thousand?"]
review_misc_answers = ["330","20,000"]
review_grid = [("86","+","75"), ("43","96","77")]  # #7 two-addend, #8 three-addend
review_grid_answers = [161, 216]
review_horiz = ["6,927 + 434 + 56 =","7,274 - 5,142 =","800 - 73 =","50,030 - 8,916 =","73 x 64 =","26 x 785 =","4,086 x 39 ="]
review_horiz_answers = [7417, 2132, 727, 41114, 4672, 20410, 159354]
review_div = [("52","4,836")]
review_div_answers = ["93"]
review_div2 = ["3,960 \u00f7 8 =","3,627 \u00f7 42 ="]
review_div2_answers = ["495","86r15"]
review_word = ["The distance from Eugene to Portland is 109 miles. The distance from Portland to Seattle is 174 miles. What is the distance from Eugene to Seattle by way of Portland?",
               "403 people belong to the Midvale Employees' Union. Of these, 287 voted to strike. How many members did not vote to strike?",
               "Joelle can type 83 words per minute. How many words can she type in 12 minutes?",
               "Colin can drive 24 miles on one gallon of gasoline. How many gallons will he need to go on a 768-mile trip?"]
review_word_answers = ["283 miles","116 members","996 words","32 gallons"]


def make(ws_num, topic, pages, grid=None, grid_answers=None, div=None, div_answers=None,
         horiz=None, horiz_answers=None, word=None, word_answers=None,
         grid_instr="Solve each problem. Show your work.", div_instr="Divide each problem.",
         extra_sections=None):
    ws = Worksheet(ws_num, topic, pages)
    ws.add_page()
    ws.name_date_line()
    n = 0
    all_pairs = []

    if grid:
        ws.instructions(grid_instr)
        probs = []
        for top, op, bottom in grid:
            n += 1
            probs.append((n, top, op, bottom))
        ws.vertical_grid(probs, cols=4, box_w=44, box_h=34)
        all_pairs.extend(zip(range(n - len(grid) + 1, n + 1), grid_answers))

    if div:
        ws.instructions(div_instr)
        probs = [(n + i + 1, d, v) for i, (d, v) in enumerate(div)]
        n += len(div)
        ws.division_grid(probs, cols=4, box_w=44, box_h=32)
        all_pairs.extend(zip(range(n - len(div) + 1, n + 1), div_answers))

    if horiz:
        ws.section_heading("Rewrite and solve each problem.")
        probs = [(n + i + 1, expr) for i, expr in enumerate(horiz)]
        n += len(horiz)
        ws.horizontal_list(probs, cols=2)
        all_pairs.extend(zip(range(n - len(horiz) + 1, n + 1), horiz_answers))

    if word:
        ws.section_heading("Solve each problem.")
        probs = [(n + i + 1, text) for i, text in enumerate(word)]
        n += len(word)
        ws.word_problems(probs)
        all_pairs.extend(zip(range(n - len(word) + 1, n + 1), word_answers))

    ws.output(os.path.join(OUTDIR, f"Worksheet-{ws_num}-{topic.replace(' ', '-')}.pdf"))

    ak = AnswerKey(ws_num, topic, pages)
    ak.add_page()
    ak.answers(all_pairs, cols=4)
    ak.output(os.path.join(OUTDIR, f"Worksheet-{ws_num}-Answer-Key.pdf"))
    print(f"Worksheet {ws_num}: {topic} -- {n} problems")
    return n


make(4, "Addition with Carrying", "12-13", grid=grid4, grid_answers=grid4_answers,
     horiz=horiz4, horiz_answers=horiz4_answers, word=word4, word_answers=word4_answers,
     grid_instr="Add each problem. Show your work in the space provided.")

# ---------------------------------------------------------------------------
# Worksheet 5 (custom -- uses vertical_grid_multi for 3- and 4-addend stacks)
# ---------------------------------------------------------------------------
ws5 = Worksheet(5, "Addition of More Than Two Numbers", "14-15")
ws5.add_page()
ws5.name_date_line()
ws5.instructions("Solve each problem. Show your work.")
n = 0
pairs5 = []
three_addend = grid5[:19]  # 7+7+5 rows of 3 addends
probs = [(n + i + 1, list(g)) for i, g in enumerate(three_addend)]
n += len(three_addend)
ws5.vertical_grid_multi(probs, cols=4, box_w=44)
pairs5.extend(zip(range(n - len(three_addend) + 1, n + 1), grid5_answers[:19]))

four_addend = grid5[19:]  # 5 rows of 4 addends
probs = [(n + i + 1, list(g)) for i, g in enumerate(four_addend)]
n += len(four_addend)
ws5.vertical_grid_multi(probs, cols=4, box_w=44)
pairs5.extend(zip(range(n - len(four_addend) + 1, n + 1), grid5_answers[19:]))

ws5.section_heading("Rewrite and add each problem.")
probs = [(n + i + 1, expr) for i, expr in enumerate(horiz5)]
n += len(horiz5)
ws5.horizontal_list(probs, cols=2)
pairs5.extend(zip(range(n - len(horiz5) + 1, n + 1), horiz5_answers))

ws5.section_heading("Solve each problem.")
probs = [(n + i + 1, text) for i, text in enumerate(word5)]
n += len(word5)
ws5.word_problems(probs)
pairs5.extend(zip(range(n - len(word5) + 1, n + 1), word5_answers))

ws5.output(os.path.join(OUTDIR, "Worksheet-5-Addition-of-More-Than-Two-Numbers.pdf"))
ak5 = AnswerKey(5, "Addition of More Than Two Numbers", "14-15")
ak5.add_page()
ak5.answers(pairs5, cols=4)
ak5.output(os.path.join(OUTDIR, "Worksheet-5-Answer-Key.pdf"))
print(f"Worksheet 5: Addition of More Than Two Numbers -- {n} problems")

make(6, "Subtraction with Regrouping", "16-17", grid=grid6, grid_answers=grid6_answers,
     horiz=horiz6, horiz_answers=horiz6_answers, word=word6, word_answers=word6_answers,
     grid_instr="Subtract each problem. Show your work.")

make(7, "Regrouping with Zeros", "18-19", grid=grid7, grid_answers=grid7_answers,
     horiz=horiz7, horiz_answers=horiz7_answers, word=word7, word_answers=word7_answers,
     grid_instr="Subtract each problem. Show your work.")

make(8, "Multiplication with Carrying", "20-21", grid=grid8, grid_answers=grid8_answers,
     horiz=horiz8, horiz_answers=horiz8_answers, word=word8, word_answers=word8_answers,
     grid_instr="Multiply each problem. Show your work.")

make(9, "Division by One Digit", "22-23", div=div9, div_answers=div9_answers,
     word=word9, word_answers=word9_answers)

make(10, "Division with Remainders", "24-25", div=div10, div_answers=div10_answers,
     horiz=horiz10, horiz_answers=horiz10_answers, word=word10, word_answers=word10_answers)

make(11, "Division by Larger Numbers", "26-27", div=div11, div_answers=div11_answers,
     horiz=horiz11, horiz_answers=horiz11_answers, word=word11, word_answers=word11_answers)

# ---------------------------------------------------------------------------
# Whole Numbers Review (custom -- Self-Paced Practice, mixed problem types)
# ---------------------------------------------------------------------------
rv = Worksheet("Review", "Whole Numbers Review", "28-29")
rv.add_page()
rv.name_date_line()
rv.instructions("These problems cover everything in Unit 1. Solve each one, then check your answers against "
                 "the Answer Key. The chart at the end tells you which pages to revisit for any you miss.")
n = 0
pairs_rv = []

text_qs = review_fill + review_figures + review_misc
text_answers = review_fill_answers + review_figures_answers + review_misc_answers
probs = [(n + i + 1, q) for i, q in enumerate(text_qs)]
n += len(text_qs)
rv.word_problems(probs, blank_lines=1)
pairs_rv.extend(zip(range(n - len(text_qs) + 1, n + 1), text_answers))

rv.section_heading("Add, subtract, multiply, divide.")
grid_probs = [(n + 1, "86", "+", "75")]
n += 1
rv.vertical_grid(grid_probs, cols=4, box_w=44, box_h=34)
pairs_rv.append((n, review_grid_answers[0]))

multi_probs = [(n + 1, ["43", "96", "77"])]
n += 1
rv.vertical_grid_multi(multi_probs, cols=4, box_w=44)
pairs_rv.append((n, review_grid_answers[1]))

all_horiz = review_horiz + review_div2
all_horiz_answers = review_horiz_answers + review_div2_answers
probs = [(n + i + 1, expr) for i, expr in enumerate(all_horiz)]
n += len(all_horiz)
rv.horizontal_list(probs, cols=2)
pairs_rv.extend(zip(range(n - len(all_horiz) + 1, n + 1), all_horiz_answers))

div_probs = [(n + 1, "52", "4,836")]
n += 1
rv.division_grid(div_probs, cols=4, box_w=44, box_h=32)
pairs_rv.append((n, review_div_answers[0]))

rv.section_heading("Solve each problem.")
probs = [(n + i + 1, text) for i, text in enumerate(review_word)]
n += len(review_word)
rv.word_problems(probs)
pairs_rv.extend(zip(range(n - len(review_word) + 1, n + 1), review_word_answers))

# Progress-check "which pages to review" chart, reproduced from the book
rv.section_heading("Progress Check")
rv.set_font("Helvetica", "", 10)
rv.set_text_color(*BLACK)
rv.multi_cell(0, 5.5, "Check your answers against the Answer Key. Then revisit the review pages for any "
                       "problems you missed, and correct your answers before moving on to Unit 2.")
rv.ln(2)
chart = [("1 to 4", "7 to 9"), ("5 to 6", "10"), ("7 to 10", "11 to 15"),
         ("11 to 14", "16 to 19"), ("15 to 18", "20 to 21"), ("19 to 22", "22 to 27")]
rv.set_font("Helvetica", "B", 10)
rv.cell(70, 7, "If you missed problems")
rv.cell(0, 7, "Review pages", ln=1)
rv.set_font("Helvetica", "", 10)
for missed, review_pages in chart:
    rv.cell(70, 6.5, missed)
    rv.cell(0, 6.5, review_pages, ln=1)

rv.output(os.path.join(OUTDIR, "Whole-Numbers-Review.pdf"))
ak_rv = AnswerKey("Review", "Whole Numbers Review", "28-29")
ak_rv.add_page()
ak_rv.answers(pairs_rv, cols=4)
ak_rv.output(os.path.join(OUTDIR, "Whole-Numbers-Review-Answer-Key.pdf"))
print(f"Whole Numbers Review -- {n} problems")

print("\nAll worksheets generated.")
