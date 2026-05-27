#!/usr/bin/env python3
"""
NVO Investment Analysis PDF Export
V6.2 design system — aligned with PortDive desktop app
"""
import os, math
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, Color
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, NextPageTemplate,
    Paragraph, Spacer, PageBreak, Table, TableStyle, Flowable, Image,
    KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ═══════════════════════════════════════════════════════════════════
# PATHS
# ═══════════════════════════════════════════════════════════════════
BASE = "/Users/hf./Documents/portdive/deep-dives"
LOGO_PD = os.path.join(BASE, "portdive-logo-with-wordmark.png")
LOGO_NVO_BIG = os.path.join(BASE, "NVO_BIG.png")
LOGO_NVO_SM = os.path.join(BASE, "NVO.png")

# ═══════════════════════════════════════════════════════════════════
# V6.2 COLOR TOKENS (Light mode for print)
# ═══════════════════════════════════════════════════════════════════
TEAL       = HexColor("#1FA39B")
TEAL_DK    = HexColor("#158682")
CORAL      = HexColor("#FF6B6B")
BLUE       = HexColor("#3D72FF")
YELLOW     = HexColor("#F9E95E")
YELLOW_DK  = HexColor("#B8A830")
CHROME     = HexColor("#4B5563")
CHROME_STR = HexColor("#1F2937")
NAVY       = HexColor("#0A1A1F")
SURFACE_ALT= HexColor("#F0F4F2")
TEXT_PRI   = HexColor("#0A1A1F")
TEXT_SEC   = HexColor("#5A6570")
TEXT_MUT   = HexColor("#8A9199")
BORDER_CLR = HexColor("#D0D5D8")
QUOTE_BG   = HexColor("#F5F8F7")
ROW_ALT    = HexColor("#F5F8F6")
SCORE_BG   = HexColor("#0F2028")
TEAL_TINT  = HexColor("#E9F7F6")
CORAL_TINT = HexColor("#FFF0F0")
BLUE_TINT  = HexColor("#ECF0FF")
YELLOW_TINT= HexColor("#FDFBE8")

# ═══════════════════════════════════════════════════════════════════
# FONTS
# ═══════════════════════════════════════════════════════════════════
pdfmetrics.registerFont(TTFont("Geist", "/Users/hf./Library/Fonts/Geist-VariableFont_wght.ttf"))
pdfmetrics.registerFont(TTFont("LoraIt", "/Users/hf./Library/Fonts/Lora-Italic-VariableFont_wght.ttf"))
HF = BF = BFB = HFR = "Geist"
BFI = BFBI = "LoraIt"

PW, PH = letter
M  = inch
CW = PW - 2 * M

# ═══════════════════════════════════════════════════════════════════
# CUSTOM FLOWABLES
# ═══════════════════════════════════════════════════════════════════

class ScoreRing(Flowable):
    """Circular arc score display — matches app's donut ring."""
    def __init__(self, score, max_score=100, diameter=64):
        Flowable.__init__(self)
        self.score = score
        self.max_score = max_score
        self.d = diameter
        self.width = diameter
        self.height = diameter

    def draw(self):
        c = self.canv
        r = self.d / 2
        cx, cy = r, r
        # Track ring (gray)
        c.setStrokeColor(BORDER_CLR)
        c.setLineWidth(3)
        c.circle(cx, cy, r - 4, stroke=1, fill=0)
        # Score arc (teal)
        pct = self.score / self.max_score
        c.setStrokeColor(TEAL)
        c.setLineWidth(3.5)
        start_angle = 90
        sweep = pct * 360
        # ReportLab arc: x1,y1,x2,y2 bounding box
        c.arc(cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4,
              startAng=start_angle, extent=sweep)
        # Score text centered
        c.setFillColor(NAVY)
        c.setFont(HF, 22)
        c.drawCentredString(cx, cy - 8, str(self.score))


class SectionHeader(Flowable):
    """Premium section header — navy uppercase + thin teal hairline."""
    def __init__(self, text, width=None):
        Flowable.__init__(self)
        self._w = width or CW
        self._text = text.upper()
        self._style = ParagraphStyle(
            'sec_h', fontName=HF, fontSize=13, leading=17,
            textColor=NAVY)
        self._para = Paragraph(self._text, self._style)
        _, h = self._para.wrap(self._w, 10000)
        self.width = self._w
        self.height = h + 6

    def draw(self):
        self._para.wrap(self._w, 10000)
        self._para.drawOn(self.canv, 0, 6)
        self.canv.setStrokeColor(TEAL)
        self.canv.setLineWidth(0.75)
        self.canv.line(0, 2, self._w, 2)


class QuoteBlock(Flowable):
    """Left-accent quote block with Lora Italic editorial voice."""
    def __init__(self, text, width=None, accent=TEAL):
        Flowable.__init__(self)
        self._w = width or CW
        self.accent = accent
        self._style = ParagraphStyle(
            'qb', fontName=BFI, fontSize=9.2, leading=14.5,
            textColor=TEXT_SEC, leftIndent=14, rightIndent=10)
        self._para = Paragraph(text, self._style)
        _, h = self._para.wrap(self._w - 24, 10000)
        self.width = self._w
        self.height = h + 14

    def draw(self):
        c = self.canv
        c.setFillColor(QUOTE_BG)
        c.roundRect(0, 0, self._w, self.height, 3, fill=1, stroke=0)
        c.setFillColor(self.accent)
        c.rect(0, 2, 3, self.height - 4, fill=1, stroke=0)
        self._para.wrap(self._w - 24, 10000)
        self._para.drawOn(c, 6, 7)


class ChromeRule(Flowable):
    def __init__(self, width=None, thickness=0.75):
        Flowable.__init__(self)
        self.width = width or CW
        self.height = thickness + 4
        self._t = thickness
    def draw(self):
        self.canv.setStrokeColor(CHROME)
        self.canv.setLineWidth(self._t)
        self.canv.line(0, 2, self.width, 2)


# ═══════════════════════════════════════════════════════════════════
# STYLES
# ═══════════════════════════════════════════════════════════════════
S = {}
S['body'] = ParagraphStyle('body', fontName=BF, fontSize=9.5, leading=15,
    textColor=TEXT_PRI, spaceBefore=3, spaceAfter=6, alignment=TA_JUSTIFY)
S['bsm'] = ParagraphStyle('bsm', parent=S['body'], fontSize=8.5, leading=13)
S['h3'] = ParagraphStyle('h3', fontName=HF, fontSize=9.5, leading=13,
    textColor=CHROME, spaceBefore=10, spaceAfter=3)
S['bul'] = ParagraphStyle('bul', fontName=BF, fontSize=9, leading=14,
    textColor=TEXT_PRI, leftIndent=16, firstLineIndent=-10,
    spaceBefore=2, spaceAfter=3)
S['csm'] = ParagraphStyle('csm', fontName=HFR, fontSize=8.5, leading=12,
    textColor=TEXT_SEC, alignment=TA_CENTER)
S['cap'] = ParagraphStyle('cap', fontName=HFR, fontSize=7, leading=10,
    textColor=TEXT_MUT, spaceBefore=1, spaceAfter=1)

# ═══════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════
def sp(pts=8): return Spacer(1, pts)
def sec(text, *first_content):
    """Section header kept together with first content to prevent orphan headers."""
    items = [SectionHeader(text), Spacer(1, 8)]
    items.extend(first_content)
    return KeepTogether(items)
def h3(text): return Paragraph(text, S['h3'])
def body(text): return Paragraph(text, S['body'])
def bsm(text): return Paragraph(text, S['bsm'])
def bul(text): return Paragraph(f"\u2022  {text}", S['bul'])
def quote(text, accent=TEAL): return QuoteBlock(text, CW, accent)


def make_table(headers, rows, col_pcts=None):
    nc = len(headers)
    cw = [CW * p for p in col_pcts] if col_pcts else [CW / nc] * nc
    data = [headers] + rows
    cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), HF), ('FONTSIZE', (0, 0), (-1, 0), 7.5),
        ('LEADING', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 1), (-1, -1), BF), ('FONTSIZE', (0, 1), (-1, -1), 8.2),
        ('LEADING', (0, 1), (-1, -1), 11.5),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_PRI),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, TEAL),
        ('LINEBELOW', (0, 1), (-1, -1), 0.4, BORDER_CLR),
        ('BOX', (0, 0), (-1, -1), 0.4, BORDER_CLR),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            cmds.append(('BACKGROUND', (0, i), (-1, i), ROW_ALT))
    t = Table(data, colWidths=cw, repeatRows=1)
    t.setStyle(TableStyle(cmds))
    return t


def make_metric_grid(metrics, cols=4):
    rows = []
    for i in range(0, len(metrics), cols):
        row = []
        for v, l, s in metrics[i:i+cols]:
            hex_c = '#1FA39B' if s == 'positive' else '#FF6B6B' if s == 'negative' else '#0A1A1F'
            cell = Paragraph(
                f"<font name='{HF}' size='11' color='{hex_c}'>{v}</font>"
                f"<br/><font name='{HFR}' size='6.5' color='#8A9199'>{l}</font>",
                ParagraphStyle('mc', alignment=TA_CENTER, spaceBefore=4, spaceAfter=4))
            row.append(cell)
        while len(row) < cols: row.append("")
        rows.append(row)
    cw = [CW / cols] * cols
    mt = Table(rows, colWidths=cw, rowHeights=[48] * len(rows))
    mt.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,-1), SURFACE_ALT),
        ('BOX', (0,0), (-1,-1), 0.4, BORDER_CLR),
        ('INNERGRID', (0,0), (-1,-1), 0.3, BORDER_CLR),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    return mt


def make_chip_row(items, cols=3):
    color_map = {"teal": ('#1FA39B', '#E9F7F6'), "coral": ('#FF6B6B', '#FFF0F0'),
                 "blue": ('#3D72FF', '#ECF0FF'), "yellow": ('#B8A830', '#FDFBE8')}
    rows = []
    for i in range(0, len(items), cols):
        row = []
        for text, cname in items[i:i+cols]:
            hex_c, hex_bg = color_map.get(cname, ('#0A1A1F', '#F0F4F2'))
            cell = Paragraph(
                f"<font name='{HF}' size='7' color='{hex_c}'>{text}</font>",
                ParagraphStyle('chip', alignment=TA_CENTER, spaceBefore=2,
                               spaceAfter=2, backColor=HexColor(hex_bg)))
            row.append(cell)
        while len(row) < cols: row.append("")
        rows.append(row)
    t = Table(rows, colWidths=[CW/cols]*cols, rowHeights=[24]*len(rows))
    t.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 2), ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ]))
    return t


def score_verdict_block(score, recommendation, one_liner, confidence):
    """Score ring + verdict text side by side — matches app layout."""
    ring = ScoreRing(score, diameter=60)
    rec_style = ParagraphStyle('rec', fontName=HF, fontSize=16, leading=20, textColor=NAVY)
    liner_style = ParagraphStyle('liner', fontName=BF, fontSize=9, leading=13, textColor=TEXT_SEC)
    conf_style = ParagraphStyle('conf', fontName=HF, fontSize=7.5, leading=10, textColor=TEXT_MUT)
    text_cell = [
        Paragraph(recommendation.upper(), rec_style),
        Spacer(1, 3),
        Paragraph(one_liner, liner_style),
        Spacer(1, 2),
        Paragraph(confidence.upper(), conf_style),
    ]
    # Wrap text items in a single-column inner table
    inner = Table([[item] for item in text_cell], colWidths=[CW - 80])
    inner.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    t = Table([[ring, inner]], colWidths=[70, CW - 70])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (0,0), 0), ('RIGHTPADDING', (0,0), (0,0), 8),
        ('LEFTPADDING', (1,0), (1,0), 4),
    ]))
    return t


def triptych(bull, base, bear):
    """Bull / Base / Bear three-column layout."""
    col_w = (CW - 8) / 3
    bs = ParagraphStyle('trip', fontName=BF, fontSize=7.8, leading=11.5, textColor=TEXT_PRI,
                        spaceBefore=2, spaceAfter=2)
    hs = lambda color: ParagraphStyle('trip_h', fontName=HF, fontSize=8, leading=11,
                                       textColor=color, spaceBefore=2, spaceAfter=2)
    data = [[
        [Paragraph("Bull", hs(TEAL)), Paragraph(bull, bs)],
        [Paragraph("Base", hs(CHROME)), Paragraph(base, bs)],
        [Paragraph("Bear", hs(CORAL)), Paragraph(bear, bs)],
    ]]
    # Flatten into single-row table with inner tables
    cells = []
    for col_items in data[0]:
        inner = Table([[item] for item in col_items], colWidths=[col_w - 8])
        inner.setStyle(TableStyle([
            ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 1), ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ]))
        cells.append(inner)
    t = Table([cells], colWidths=[col_w, col_w, col_w])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), TEAL_TINT),
        ('BACKGROUND', (1,0), (1,0), SURFACE_ALT),
        ('BACKGROUND', (2,0), (2,0), CORAL_TINT),
        ('BOX', (0,0), (-1,-1), 0.4, BORDER_CLR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_CLR),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    return t


# ═══════════════════════════════════════════════════════════════════
# PAGE TEMPLATES
# ═══════════════════════════════════════════════════════════════════
def _body_hf(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, PH - 28, PW, 28, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#94A3B8"))
    canvas.setFont(HF, 6.5)
    canvas.drawString(M, PH - 19, "INVESTMENT ANALYSIS  |  NVO  |  NYSE")
    canvas.setFillColor(HexColor("#6A7A84"))
    canvas.setFont(HFR, 6)
    canvas.drawRightString(PW - M, PH - 19, "CONFIDENTIAL \u2014 INVESTMENT RESEARCH")
    canvas.setStrokeColor(BORDER_CLR)
    canvas.setLineWidth(0.4)
    canvas.line(M, 36, PW - M, 36)
    canvas.setFillColor(TEXT_MUT)
    canvas.setFont(HFR, 6)
    canvas.drawString(M, 25, "Portdive Alpha Intelligence. Not financial advice.")
    canvas.drawRightString(PW - M, 25, f"Page {doc.page}")
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(2)
    canvas.line(0, 2, PW, 2)
    canvas.restoreState()

def _cover_hf(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(BORDER_CLR)
    canvas.setLineWidth(0.4)
    canvas.line(M, 36, PW - M, 36)
    canvas.setFillColor(TEXT_MUT)
    canvas.setFont(HFR, 6)
    canvas.drawString(M, 25, "Portdive Alpha Intelligence. Not financial advice.")
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(2)
    canvas.line(0, 2, PW, 2)
    canvas.restoreState()


# ═══════════════════════════════════════════════════════════════════
# BUILD REPORT
# ═══════════════════════════════════════════════════════════════════
def build_nvo_report():
    output_path = os.path.join(BASE, "NVO_Investment_Analysis_2026-04-15.pdf")
    story = []

    # ── COVER ───────────────────────────────────────────────────
    story.append(sp(55))

    # Logos: NVO bull + "+" + PortDive — correct aspect ratios
    # NVO_BIG is 1603x1143 (1.40:1), target height 60px → width 84px
    nvo_logo = Image(LOGO_NVO_BIG, width=84, height=60, hAlign='CENTER')
    plus_text = Paragraph("<font name='Geist' size='18' color='#8A9199'>+</font>",
                          ParagraphStyle('plus', alignment=TA_CENTER))
    # PD logo is 1906x531 (3.59:1), target height 44px → width 158px
    pd_logo = Image(LOGO_PD, width=158, height=44, hAlign='CENTER')
    logo_row = Table([[nvo_logo, plus_text, pd_logo]], colWidths=[100, 30, 170])
    logo_row.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    logo_wrapper = Table([[logo_row]], colWidths=[CW])
    logo_wrapper.setStyle(TableStyle([('ALIGN', (0,0), (0,0), 'CENTER')]))
    story.append(logo_wrapper)
    story.append(sp(8))

    # "Investment Analysis" subtitle
    story.append(Paragraph("Investment Analysis", ParagraphStyle(
        'cover_sub', fontName=HFR, fontSize=14, leading=18, textColor=TEAL, alignment=TA_CENTER)))
    story.append(sp(34))

    # Company block on NAVY bar
    ct = Table(
        [[Paragraph("Novo Nordisk A/S", ParagraphStyle('cn', fontName=HF, fontSize=24,
                    textColor=white, alignment=TA_CENTER))],
         [Paragraph("NYSE: NVO", ParagraphStyle('ct', fontName=HFR, fontSize=11,
                    textColor=TEAL, alignment=TA_CENTER))]],
        colWidths=[CW], rowHeights=[42, 22])
    ct.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), NAVY),
        ('TOPPADDING', (0,0), (0,0), 12), ('BOTTOMPADDING', (0,-1), (0,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(ct)
    story.append(sp(34))

    # Score verdict — centered on cover
    story.append(score_verdict_block(
        57, "Hold",
        "Deep value at P/E ~11x with 81% gross margins, but competitive erosion from "
        "Eli Lilly and negative 2026 guidance cycle require proof of stabilization \u2014 "
        "Q1 earnings on May 6 are the critical test.",
        "Medium Confidence"))
    story.append(sp(55))

    # Metadata at bottom of cover
    story.append(ChromeRule(CW))
    story.append(sp(6))
    for line in ["Investment Analysis Pipeline | Skill #41",
                 "Portdive Alpha Intelligence | claude-opus-4-6",
                 "Report Date: April 15, 2026"]:
        story.append(Paragraph(line, S['csm']))

    story.append(NextPageTemplate('Body'))
    story.append(PageBreak())

    # ── 1. EXECUTIVE SUMMARY ──────────────────────────────────
    story.append(sec("1. Executive Summary",
        score_verdict_block(
        57, "Hold",
        "Deep value at P/E ~11x with 81% gross margins, but competitive erosion from "
        "Eli Lilly and negative 2026 guidance cycle require proof of stabilization \u2014 "
        "Q1 earnings on May 6 are the critical test.",
        "Medium Confidence")))
    story.append(sp(8))
    story.append(body(
        "Novo Nordisk is the world\u2019s largest diabetes and obesity care company, generating "
        "~$46B in 2025 revenue (DKK 309B) with blockbuster GLP-1 drugs Ozempic and Wegovy comprising "
        "~67% of sales. The stock has fallen around 50% from its 52-week high of $81.44 to $39.78, "
        "compressing the trailing P/E to ~11x \u2014 well below its 5-year average on most data providers."))
    story.append(sp(4))
    story.append(bsm("<i>Market data as of April 15, 2026. Fundamentals based on FY-2025 results "
                      "(reported Feb 2026). Official reporting currency: DKK.</i>"))
    story.append(sp(8))
    story.append(make_metric_grid([
        ("$39.78", "Price", "negative"), ("$174B", "Market Cap", "neutral"),
        ("~11x", "P/E (TTM)", "positive"), ("~$46B", "Revenue 2025", "neutral"),
        ("81%", "Gross Margin", "positive"), ("-5% to -13%", "2026 Adj Sales (CER)", "negative"),
        ("$35\u2013$81", "52-Wk Range", "negative"), ("~$45", "Consensus Target", "neutral"),
    ]))
    story.append(sp(13))

    # ── 2. COMPANY OVERVIEW ───────────────────────────────────
    story.append(sec("2. Company Overview", h3("BUSINESS MODEL")))
    story.append(body(
        "Novo Nordisk A/S, founded 1923, headquartered in Denmark, operates through two segments:"))
    story.append(bul("<b>Obesity &amp; Diabetes Care</b> (~90%): Ozempic, Wegovy, Rybelsus, insulin. "
                      "Ozempic + Wegovy = ~$32B (67% of revenue)."))
    story.append(bul("<b>Rare Disease</b> (~10%): Rare blood and endocrine disorders, HRT."))
    story.append(sp(8))
    story.append(make_metric_grid([
        ("~$46B", "Revenue", "positive"), ("+11% YoY", "Growth", "positive"),
        ("81%", "Gross Margin", "positive"), ("48,000+", "Employees", "neutral"),
    ]))
    story.append(sp(6))
    story.append(h3("MOAT ASSESSMENT"))
    story.append(body(
        "Moat built on GLP-1 IP, Ozempic/Wegovy brand, regulatory expertise, and manufacturing "
        "scale. However, moat is <b>narrowing</b> \u2014 GLP-1 share has eroded significantly from "
        "its historical dominance as Lilly\u2019s Mounjaro/Zepbound gained rapid share with superior efficacy. "
        "Core semaglutide patent expires 2026; formulation patents extend to early 2030s."))
    story.append(sp(13))

    # ── 3. CORE BUSINESS THESIS ───────────────────────────────
    story.append(sec("3. Core Business Thesis",
        quote(
        "\u201CThe core thesis is a deep value play on the world\u2019s leading GLP-1 franchise "
        "trading at a historically depressed multiple. At ~11x TTM earnings with 81% gross margins, "
        "the market is pricing in a permanent impairment scenario that may overstate the competitive "
        "threat.\u201D")))
    story.append(sp(6))
    story.append(h3("PILLAR 1: VALUATION ANCHOR"))
    story.append(body(
        "P/E ~11x vs a 5-year trailing average well above 20x. Current tracked analyst targets cluster "
        "in the low- to mid-40s (consensus ~$45, range $41\u2013$47), implying ~13% upside from $39.78."))
    story.append(h3("PILLAR 2: ORAL GLP-1 FIRST MOVER"))
    story.append(body(
        "Oral Wegovy, FDA-approved Dec 2025, launched Jan 5, 2026 \u2014 <b>first oral GLP-1 for "
        "obesity</b> in the US. Expands addressable market 30\u201340%. Lilly\u2019s orforglipron "
        "still pending approval."))
    story.append(h3("PILLAR 3: EFFICACY GAP CLOSING"))
    story.append(body(
        "In cross-trial comparisons, high-dose Wegovy (~20.7% weight loss) appears closer to "
        "Zepbound (~20\u201322%), suggesting the absolute efficacy gap is narrower than with standard "
        "Wegovy doses\u2014though direct head-to-head data remain limited."))
    story.append(h3("PILLAR 4: TAM EXPANSION"))
    story.append(body(
        "GLP-1 obesity market: $10.1B (2026) \u2192 $66.6B by 2035 (23.3% CAGR). Even with share "
        "losses, absolute revenue opportunity is growing."))
    story.append(sp(13))

    # ── 4. KEY CATALYSTS ──────────────────────────────────────
    story.append(sec("4. Key Catalysts",
        make_table(
        ["Catalyst", "Date", "Impact", "Probability"],
        [["Q1 2026 Earnings", "May 6, 2026", "High", "Certain"],
         ["Oral Wegovy US Ramp", "Ongoing 2026", "High", "High"],
         ["Wegovy HD Launch", "2026", "Medium", "High"],
         ["CMS BALANCE / Medicare", "2026 TBD", "High", "Medium"],
         ["H1 2026 Results", "Aug 5, 2026", "Medium", "Certain"],
         ["Semaglutide Patent Expiry", "2026", "High", "Certain"]],
        [.40, .20, .20, .20])))
    story.append(sp(8))
    story.append(make_chip_row([
        ("Q1 Earnings \u2014 May 6", "teal"), ("Oral Wegovy Ramp", "teal"),
        ("Wegovy HD Launch", "teal"), ("Medicare Coverage", "teal"),
        ("H1 Results \u2014 Aug 5", "teal"), ("Patent Expiry Risk", "coral"),
    ], cols=3))
    story.append(sp(6))
    story.append(body(
        "Current tracked analyst targets cluster in the low- to mid-40s (consensus ~$45, range "
        "$41\u2013$47 on our data provider). Consensus rating: Sell on limited coverage (3 tracked ratings)."))
    story.append(sp(13))

    # ── 5. SECTOR & MARKET OVERVIEW ───────────────────────────
    story.append(sec("5. Sector & Market Overview",
        body("GLP-1 market is the fastest-growing pharma segment. Obesity GLP-1: $10.1B (2026) to "
        "$66.6B by 2035 (23.3% CAGR). Total GLP-1 market could reach $200B by 2031. "
        "2026 is the <b>year of acceleration</b>: oral approvals, Medicare expansion, "
        "new indications (MASH, CKD, sleep apnea).")))
    story.append(sp(6))
    story.append(h3("REGULATORY"))
    story.append(bul("<b>FDA</b>: Oral semaglutide for obesity approved Dec 2025. Wegovy HD approved. "
                      "Draft obesity guidance still unfinalized."))
    story.append(bul("<b>CMS</b>: BALANCE model aims for ~$50/month out-of-pocket for Medicare GLP-1 "
                      "access; actual cost sharing varies by plan and details remain in flux."))
    story.append(bul("<b>India</b>: Generic semaglutide expanding rapidly. Novo appears to maintain "
                      "a meaningful branded presence, though precise market-share data are limited."))
    story.append(sp(6))
    story.append(h3("PRICING"))
    story.append(body(
        "Branded GLP-1s (>$1,000/month) under pressure: compounding pharmacies, Costco/Walmart "
        "($499/month), CMS negotiations, generic entry. ~150 obesity drugs in development globally."))
    story.append(sp(13))

    # ── 6. COMPETITIVE LANDSCAPE ──────────────────────────────
    story.append(sec("6. Competitive Landscape",
        make_table(
        ["Company", "P/E", "Rev Growth (2026E)", "Market Cap"],
        [["NVO", "~11x", "-5% to -13% (adj CER)", "$182B"],
         ["LLY", "~39x", "+43% (FY25)", "~$854B"]],
        [.25, .25, .25, .25])))
    story.append(sp(6))
    story.append(body(
        "Lilly overtook Novo by revenue. Q4 2025: Mounjaro $7.41B (+110%), Zepbound $4.26B (+123%); "
        "FY 2025 revenue $65.2B. Lilly briefly exceeded $1T market cap in late 2025, currently ~$854B. "
        "Tirzepatide delivers ~20\u201322% weight loss in trials vs semaglutide 14\u201315% (regular dose)."))
    story.append(sp(6))
    story.append(h3("EMERGING COMPETITORS"))
    story.append(bul("<b>Pfizer</b>: Metsera acquisition ($10B). <b>AstraZeneca</b>: Obesity pipeline. "
                      "<b>Amgen</b>: MariTide. <b>Roche</b>: Carmot/CT-388."))
    story.append(sp(6))
    story.append(quote(
        "\u201CNVO at ~11x vs LLY at ~39x reflects the market\u2019s belief that Lilly "
        "has won the GLP-1 war. If that belief proves even partially wrong, NVO\u2019s "
        "re-rating potential is significant.\u201D"))
    story.append(sp(13))

    # ── 7. SECTOR SENTIMENT ───────────────────────────────────
    story.append(sec("7. Sector Sentiment",
        body("GLP-1/obesity remains one of the most bullish healthcare themes. But sentiment has "
        "diverged: Lilly euphoric (briefly >$1T cap in 2025), Novo deeply negative (down ~50%, "
        "9,000 job cuts, declining guidance).")))
    story.append(sp(6))
    story.append(h3("TECHNICAL SNAPSHOT"))
    story.append(bsm("<i>Snapshot as of April 15, 2026 — indicators will shift with price action. "
                      "Source: PortDive Trading Decision Engine V3 (proprietary indicator weights "
                      "and calculations; not sourced from third-party brokers).</i>"))
    story.append(sp(4))
    story.append(make_table(
        ["Indicator", "Daily", "Weekly"],
        [["RSI(14)", "57.8 (neutral)", "35.3 (near oversold)"],
         ["MACD", "Hist turning +", "Deeply negative (-5.63)"],
         ["Stochastics", "92.7 (overbought)", "7.3 (oversold)"],
         ["SuperTrend", "Bullish", "Bearish"],
         ["vs SMA50", "-1.7%", "-31.9%"],
         ["vs SMA200", "-23.2%", "-55.0%"]],
        [.28, .36, .36]))
    story.append(sp(6))
    story.append(body(
        "As of mid-April 2026, daily momentum is recovering (MACD turning positive, SuperTrend bullish). "
        "Weekly trend remains down \u2014 price well below major moving averages with no confirmed reversal."))
    story.append(sp(13))

    # ── 8. SWOT — starts on its own page ────────────────────
    story.append(PageBreak())
    story.append(sec("8. SWOT Analysis"))

    def _swot_cell(title, items, color_hex, tint_hex):
        hdr = Paragraph(f"<font name='{HF}' size='8' color='white'><b>{title}</b></font>",
                        ParagraphStyle('sh', fontName=HF, fontSize=8, leading=12,
                                       textColor=white, alignment=TA_CENTER, spaceBefore=3, spaceAfter=3))
        item_style = ParagraphStyle('si', fontName=BF, fontSize=7.5, leading=11,
                                     textColor=TEXT_PRI, leftIndent=4, rightIndent=4,
                                     spaceBefore=1, spaceAfter=1)
        bullet_items = []
        for item in items:
            bullet_items.append([Paragraph(f"\u2022 <b>{item[0]}</b> \u2014 {item[1]}", item_style)])
        inner_rows = [[hdr]] + bullet_items
        inner = Table(inner_rows, colWidths=[CW/2 - 10])
        cmds = [
            ('BACKGROUND', (0,0), (0,0), HexColor(color_hex)),
            ('TOPPADDING', (0,0), (0,0), 3), ('BOTTOMPADDING', (0,0), (0,0), 3),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,1), (-1,-1), 2), ('BOTTOMPADDING', (0,1), (-1,-1), 2),
            ('BOX', (0,0), (-1,-1), 0.4, BORDER_CLR),
        ]
        for i in range(1, len(inner_rows)):
            cmds.append(('BACKGROUND', (0,i), (0,i), HexColor(tint_hex)))
        inner.setStyle(TableStyle(cmds))
        return inner

    strengths = [
        ("Global GLP-1 Pioneer, ~60% Volume Share", "Around 60% global GLP-1 volume in recent years (share declining); Ozempic/Wegovy household names, 168-country distribution"),
        ("81% Gross Margin", "~$46B revenue funds competitive response"),
        ("First Oral GLP-1 for Obesity", "FDA Dec 2025, launched Jan 2026. Expands TAM 30\u201340%"),
        ("Wegovy HD Narrows Efficacy Gap", "~20.7% weight loss in cross-trial comparisons vs ~20\u201322% for Zepbound; head-to-head data limited"),
        ("Patent Portfolio to Early 2030s", "Formulation patents extend beyond core expiry"),
    ]
    weaknesses = [
        ("67% Revenue from Two Drugs", "Ozempic + Wegovy concentration risk"),
        ("2026 Guidance: -5% to -13% CER", "First negative guidance cycle in years"),
        ("GLP-1 Share Eroding Significantly", "Lilly\u2019s tirzepatide gaining rapid share; NVO Q4 2025 revenue -7.6% YoY"),
        ("9,000 Job Cuts", "Restructuring mode, not growth mode"),
        ("Tirzepatide Efficacy Gap", "Lilly\u2019s oral orforglipron outperformed in head-to-head"),
    ]
    opportunities = [
        ("P/E ~11x vs 5Y Avg >20x", "Significant discount creates deep value if headwinds stabilize"),
        ("GLP-1 TAM: $10B \u2192 $66.6B by 2035", "23% CAGR \u2014 shrinking share of larger pie = growth"),
        ("Medicare/Medicaid Expansion", "CMS BALANCE model targeting ~$50/month OOP; details evolving"),
        ("New Indications (MASH, CKD)", "Approved beyond obesity, expanding prescriber base"),
        ("India Branded Presence", "Novo appears to maintain meaningful branded presence despite growing generic backdrop; precise share data not yet consistently reported"),
    ]
    threats = [
        ("Lilly Tirzepatide Growth", "FY25 revenue $65.2B; Mounjaro $7.41B (+110%) and Zepbound $4.26B (+123%) in Q4"),
        ("Generic/Compounding Competition", "India generics, US compounders at fraction of price"),
        ("~150 Obesity Drugs in Pipeline", "AZN, Roche, Amgen, Pfizer/Metsera all entering"),
        ("Semaglutide Patent Expiry 2026", "Core patent expires this year"),
        ("Structural Pricing Compression", "Costco $499/month, CMS, insurance restrictions"),
    ]

    s_cell = _swot_cell("STRENGTHS", strengths, '#1FA39B', '#E9F7F6')
    w_cell = _swot_cell("WEAKNESSES", weaknesses, '#FF6B6B', '#FFF0F0')
    o_cell = _swot_cell("OPPORTUNITIES", opportunities, '#3D72FF', '#ECF0FF')
    t_cell = _swot_cell("THREATS", threats, '#B8A830', '#FDFBE8')

    swot = Table([[s_cell, w_cell], [o_cell, t_cell]],
                 colWidths=[CW/2 - 2, CW/2 - 2])
    swot.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 2), ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(swot)
    story.append(sp(13))

    # ── 9. THESIS VERDICT — starts on its own page ──────────
    story.append(PageBreak())
    story.append(sec("9. Thesis Verdict",
        score_verdict_block(
        57, "Hold",
        "Novo Nordisk presents one of the most polarizing investment cases in healthcare. "
        "The extreme valuation discount creates genuine deep-value appeal, but competitive "
        "and pricing headwinds are real and accelerating.",
        "Medium Confidence")))
    story.append(sp(8))

    story.append(h3("SCORING BREAKDOWN"))
    story.append(make_table(
        ["Component", "Weight", "Score", "Pts"],
        [["Fundamental Strength", "25%", "70/100", "17.5"],
         ["Catalyst Pipeline", "20%", "55/100", "11.0"],
         ["Competitive Position", "20%", "45/100", "9.0"],
         ["SWOT Balance", "20%", "55/100", "11.0"],
         ["Macro/Sector", "15%", "55/100", "8.25"]],
        [.38, .15, .22, .15]))
    story.append(sp(8))

    story.append(h3("SCENARIOS"))
    story.append(sp(6))
    story.append(triptych(
        "Oral Wegovy drives 30\u201340% TAM expansion. Wegovy HD closes efficacy gap. "
        "Q1 shows stabilizing share. CMS BALANCE unlocks Medicare. "
        "Multiple re-rates 10x \u2192 15\u201318x. Stock $60\u201380 (50\u2013100% upside).",
        "Oral Wegovy modest traction, 2\u20133 quarters to scale. Share losses decelerate. "
        "Revenue -8\u201310% per guidance midpoint. P/E 10\u201312x. "
        "Stock $38\u201350. Fair value ~$45\u201350 (13\u201326% upside).",
        "Lilly orforglipron launches, takes oral share. Generics accelerate. "
        "Revenue decline exceeds -13%. Compounders erode volumes. "
        "P/E compresses to 7\u20138x. Stock tests $30 or below."
    ))
    story.append(sp(8))

    story.append(h3("KEY RISKS"))
    story.append(sp(6))
    story.append(make_chip_row([
        ("Lilly orforglipron FDA approval", "coral"),
        ("Generic semaglutide acceleration", "coral"),
        ("Revenue decline worse than -13%", "coral"),
        ("Compounding pharmacy threat", "yellow"),
        ("Medicare coverage delayed", "yellow"),
        ("150+ pipeline drugs", "yellow"),
    ], cols=3))
    story.append(sp(8))

    story.append(h3("CATALYSTS TO WATCH"))
    story.append(sp(6))
    story.append(make_chip_row([
        ("Q1 Earnings \u2014 May 6", "teal"),
        ("Oral Wegovy Rx Volume", "teal"),
        ("CMS BALANCE Timeline", "blue"),
        ("Lilly Orforglipron FDA", "yellow"),
        ("H1 Results \u2014 Aug 5", "teal"),
        ("India/EM Market Share", "blue"),
    ], cols=3))
    story.append(sp(13))

    # Disclaimer — dark card, unmissable
    disc_styles = {
        'h': ParagraphStyle('dh', fontName=HF, fontSize=9, leading=12,
                            textColor=HexColor("#CBD5E1")),
        'b': ParagraphStyle('db', fontName=BF, fontSize=8, leading=12,
                            textColor=HexColor("#A8B4BC")),
        'w': ParagraphStyle('dw', fontName=HF, fontSize=8, leading=12,
                            textColor=HexColor("#F8FAF9")),
        'm': ParagraphStyle('dm', fontName=BFI, fontSize=7.5, leading=11,
                            textColor=HexColor("#6A7A84")),
    }
    disc_rows = [
        [Paragraph("DISCLAIMER", disc_styles['h'])],
        [Spacer(1, 4)],
        [Paragraph(
            "These reports are for informational and educational purposes only. A report does "
            "NOT constitute investment advice, a buy/sell recommendation, or an offer to buy/sell "
            "any security. Past performance does not guarantee future results. All trading involves "
            "risk; you may lose invested capital. The Elliott Wave methodology, Fibonacci "
            "retracement levels, and technical indicators are tools for analysis but not "
            "certainties. Fundamental assumptions (revenue growth rates, margin expansion, "
            "multiple re-rating, catalyst execution) are subject to change.",
            disc_styles['b'])],
        [Spacer(1, 4)],
        [Paragraph(
            "AI Hallucinations may be part of the reasoning process and create false assumptions, "
            "predictions and statements.",
            disc_styles['b'])],
        [Spacer(1, 6)],
        [Paragraph(
            "PortDive UG. \u2014 AI-GENERATED ANALYSIS \u2014 NO FINANCIAL ADVICE, USE RESPONSIBLY.",
            disc_styles['w'])],
        [Spacer(1, 4)],
        [Paragraph(
            "Generated by Portdive Alpha Intelligence | Investment Analysis Pipeline (Skill #41) "
            "| Model: claude-opus-4-6 | April 15, 2026.",
            disc_styles['m'])],
    ]
    disc_table = Table(disc_rows, colWidths=[CW - 28])
    disc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('TOPPADDING', (0, 0), (0, 0), 14),
        ('BOTTOMPADDING', (0, -1), (0, -1), 14),
        ('TOPPADDING', (0, 1), (-1, -2), 0),
        ('BOTTOMPADDING', (0, 1), (-1, -2), 0),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
    ]))
    # Wrap in outer table for centering
    disc_outer = Table([[disc_table]], colWidths=[CW])
    disc_outer.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'CENTER')]))
    story.append(sp(13))
    story.append(KeepTogether([disc_outer]))

    # ── BUILD ─────────────────────────────────────────────────
    doc = BaseDocTemplate(
        output_path, pagesize=letter,
        leftMargin=M, rightMargin=M,
        topMargin=M, bottomMargin=0.7 * M,
        title="NVO Investment Analysis", author="Portdive Alpha Intelligence")

    cover_frame = Frame(M, 0.7 * M, CW, PH - 1.4 * M, id='cover')
    body_frame  = Frame(M, 0.7 * M, CW, PH - M - 0.7 * M - 8, id='body')

    doc.addPageTemplates([
        PageTemplate(id='Cover', frames=cover_frame, onPage=_cover_hf),
        PageTemplate(id='Body',  frames=body_frame,  onPage=_body_hf),
    ])

    doc.build(story)
    size = os.path.getsize(output_path)
    print(f"OK: {output_path} ({size:,} bytes, {doc.page} pages)")
    return output_path


if __name__ == "__main__":
    build_nvo_report()
