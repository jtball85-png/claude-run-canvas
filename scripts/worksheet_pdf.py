# -*- coding: utf-8 -*-
"""Generates clean, printable Worksheet + Answer Key PDFs for Business Math
Unit 1, Day 2 -- replaces the crooked textbook-scan images with typeset,
print-ready documents built from the same real problems/answers."""
import os
from fpdf import FPDF

NAVY = (0, 52, 98)
GOLD = (255, 207, 1)
TEAL = (0, 183, 163)
GRAY = (100, 116, 139)
BLACK = (31, 41, 55)

OUTDIR = r"C:\Users\jball.VACE\Documents\Claude Projects\Claude Run Canvas\generated_worksheets"
os.makedirs(OUTDIR, exist_ok=True)


class Worksheet(FPDF):
    def __init__(self, ws_num, topic, book_pages, unit_label="Unit 1: Whole Numbers"):
        super().__init__(orientation="P", unit="mm", format="Letter")
        self.ws_num = ws_num
        self.topic = topic
        self.book_pages = book_pages
        self.unit_label = unit_label
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(15, 15, 15)

    def title_text(self):
        return self.topic if self.ws_num == "Review" else f"Worksheet {self.ws_num}: {self.topic}"

    def header(self):
        self.set_fill_color(*NAVY)
        self.rect(0, 0, self.w, 20, "F")
        self.set_xy(15, 4)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(255, 255, 255)
        self.cell(0, 6, self.title_text(), ln=1)
        self.set_x(15)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*GOLD)
        self.cell(0, 5, f"Business Math \u00b7 {self.unit_label} \u00b7 Book pages {self.book_pages}", ln=1)
        self.ln(10)
        self.set_text_color(*BLACK)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 8, f"{self.title_text()} - Page {self.page_no()}", align="C")

    def name_date_line(self):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*BLACK)
        self.cell(95, 6, "Name: " + "_" * 30)
        self.cell(0, 6, "Date: " + "_" * 20, ln=1)
        self.ln(3)

    def instructions(self, text):
        self.set_font("Helvetica", "I", 10)
        self.set_text_color(*GRAY)
        self.multi_cell(0, 5, text)
        self.ln(2)
        self.set_text_color(*BLACK)

    def section_heading(self, text):
        self.ln(2)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*NAVY)
        self.cell(0, 7, text, ln=1)
        self.set_draw_color(*TEAL)
        self.set_line_width(0.6)
        y = self.get_y()
        self.line(15, y, self.w - 15, y)
        self.ln(3)
        self.set_text_color(*BLACK)

    # -- vertical (stacked) problems: addition/subtraction/multiplication ----
    def vertical_grid(self, problems, cols=4, box_w=44, box_h=34):
        """problems: list of (number, top, op, bottom) tuples."""
        x0 = self.get_x()
        col = 0
        row_y = self.get_y()
        for num, top, op, bottom in problems:
            if row_y + box_h > self.h - 20:
                self.add_page()
                row_y = self.get_y()
            x = x0 + col * box_w
            y = row_y
            self.set_xy(x, y)
            self.set_font("Helvetica", "", 8)
            self.set_text_color(*GRAY)
            self.cell(box_w - 4, 5, f"{num}.")
            self.set_xy(x, y + 5)
            self.set_font("Helvetica", "", 13)
            self.set_text_color(*BLACK)
            self.cell(box_w - 6, 6, top, align="R")
            self.set_xy(x, y + 11)
            self.cell(box_w - 6, 6, f"{op} {bottom}", align="R")
            self.set_draw_color(*BLACK)
            self.set_line_width(0.3)
            self.line(x + 4, y + 17.5, x + box_w - 4, y + 17.5)
            col += 1
            if col >= cols:
                col = 0
                row_y += box_h
        self.set_xy(x0, row_y + (box_h if col != 0 else 0))
        self.ln(2)

    # -- vertical stack of 3+ addends (e.g. "Addition of More Than Two Numbers") --
    def vertical_grid_multi(self, problems, cols=4, box_w=44, op="+"):
        """problems: list of (number, [line1, line2, ...]) -- all lines added,
        op prefixed on every line after the first. Box height auto-sizes to the
        tallest problem in this call so every row lines up cleanly."""
        max_lines = max(len(lines) for _, lines in problems)
        line_h = 6
        box_h = 5 + max_lines * line_h + 6 + 6  # label + stacked lines + rule gap + spacing
        x0 = self.get_x()
        col = 0
        row_y = self.get_y()
        for num, lines in problems:
            if row_y + box_h > self.h - 20:
                self.add_page()
                row_y = self.get_y()
            x = x0 + col * box_w
            y = row_y
            self.set_xy(x, y)
            self.set_font("Helvetica", "", 8)
            self.set_text_color(*GRAY)
            self.cell(box_w - 4, 5, f"{num}.")
            self.set_font("Helvetica", "", 13)
            self.set_text_color(*BLACK)
            for i, line in enumerate(lines):
                text = line if i == 0 else f"{op} {line}"
                self.set_xy(x, y + 5 + i * line_h)
                self.cell(box_w - 6, line_h, text, align="R")
            rule_y = y + 5 + max_lines * line_h + 1.5
            self.set_draw_color(*BLACK)
            self.set_line_width(0.3)
            self.line(x + 4, rule_y, x + box_w - 4, rule_y)
            col += 1
            if col >= cols:
                col = 0
                row_y += box_h
        self.set_xy(x0, row_y + (box_h if col != 0 else 0))
        self.ln(2)

    # -- division problems (drawn bracket) ------------------------------------
    def division_grid(self, problems, cols=4, box_w=44, box_h=30):
        """problems: list of (number, divisor, dividend) tuples."""
        x0 = self.get_x()
        col = 0
        row_y = self.get_y()
        for num, divisor, dividend in problems:
            if row_y + box_h > self.h - 20:
                self.add_page()
                row_y = self.get_y()
            x = x0 + col * box_w
            y = row_y
            self.set_xy(x, y)
            self.set_font("Helvetica", "", 8)
            self.set_text_color(*GRAY)
            self.cell(box_w - 4, 5, f"{num}.")
            self.set_font("Helvetica", "", 13)
            self.set_text_color(*BLACK)
            ty = y + 8
            dw = self.get_string_width(dividend) + 4
            bx = x + 14
            self.set_draw_color(*BLACK)
            self.set_line_width(0.35)
            # bracket: vertical line then top horizontal line
            self.line(bx, ty - 5, bx, ty + 2)
            self.line(bx, ty - 5, bx + dw, ty - 5)
            self.set_xy(x, ty - 5.5)
            self.cell(bx - x - 1, 6, divisor, align="R")
            self.set_xy(bx + 1, ty - 4.5)
            self.cell(dw, 6, dividend)
            col += 1
            if col >= cols:
                col = 0
                row_y += box_h
        self.set_xy(x0, row_y + (box_h if col != 0 else 0))
        self.ln(2)

    # -- horizontal equations (rewrite-and-solve) -----------------------------
    def horizontal_list(self, problems, cols=2):
        """problems: list of (number, expression) tuples, e.g. '739 + 494 ='"""
        x0 = self.get_x()
        col = 0
        row_h = 16
        col_w = (self.w - 30) / cols
        row_y = self.get_y()
        for num, expr in problems:
            if row_y + row_h > self.h - 20:
                self.add_page()
                row_y = self.get_y()
            x = x0 + col * col_w
            self.set_xy(x, row_y)
            self.set_font("Helvetica", "", 12)
            self.set_text_color(*BLACK)
            self.cell(col_w - 4, 7, f"{num}.  {expr}", ln=0)
            col += 1
            if col >= cols:
                col = 0
                row_y += row_h
        self.set_xy(x0, row_y + (row_h if col != 0 else 0))
        self.ln(4)

    # -- word problems ---------------------------------------------------------
    def word_problems(self, problems, blank_lines=2):
        """problems: list of (number, text) tuples."""
        for num, text in problems:
            self.set_font("Helvetica", "", 11)
            self.set_text_color(*BLACK)
            self.set_x(15)
            self.multi_cell(0, 6, f"{num}.  {text}")
            for _ in range(blank_lines):
                self.ln(6)
                y = self.get_y()
                self.set_draw_color(200, 200, 200)
                self.set_line_width(0.2)
                self.line(20, y, self.w - 15, y)
            self.ln(4)
            if self.get_y() > self.h - 30:
                self.add_page()


class AnswerKey(FPDF):
    def __init__(self, ws_num, topic, book_pages):
        super().__init__(orientation="P", unit="mm", format="Letter")
        self.ws_num = ws_num
        self.topic = topic
        self.book_pages = book_pages
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(15, 15, 15)

    def title_text(self):
        base = self.topic if self.ws_num == "Review" else f"Worksheet {self.ws_num}: {self.topic}"
        return f"Answer Key - {base}"

    def header(self):
        self.set_fill_color(*GOLD)
        self.rect(0, 0, self.w, 18, "F")
        self.set_xy(15, 4)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*NAVY)
        self.cell(0, 6, self.title_text(), ln=1)
        self.ln(8)
        self.set_text_color(*BLACK)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 8, f"{self.title_text()} - Page {self.page_no()}", align="C")

    def answers(self, pairs, cols=4):
        """pairs: list of (number, answer)."""
        self.set_font("Helvetica", "", 11)
        col_w = (self.w - 30) / cols
        row_h = 8
        col = 0
        x0 = self.get_x()
        row_y = self.get_y()
        for num, ans in pairs:
            if row_y + row_h > self.h - 20:
                self.add_page()
                row_y = self.get_y()
            x = x0 + col * col_w
            self.set_xy(x, row_y)
            self.set_text_color(*GRAY)
            self.cell(8, row_h, f"{num}.")
            self.set_text_color(*BLACK)
            self.cell(col_w - 8, row_h, str(ans))
            col += 1
            if col >= cols:
                col = 0
                row_y += row_h
        self.set_xy(x0, row_y + (row_h if col != 0 else 0))
        self.ln(4)


print("worksheet_pdf module ready")
