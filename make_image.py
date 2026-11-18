#!/usr/bin/env python3
"""
make_image.py - Generates the newspaper front page for 18 November 2026.

Renders at 2048x2048 using PIL primitives and DejaVu fonts, then downscales
with LANCZOS filter to 1024x1024 to produce a crisp, high-contrast entry.png.
"""

import math
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions (2x supersampling)
W, H = 2048, 2048
OUT_W, OUT_H = 1024, 1024

# Font definitions
FONT_SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SANS_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Color Palette (Broadsheet editorial style)
BG_COLOR = (248, 248, 246)         # Editorial warm newsprint
INK_BLACK = (17, 24, 39)           # Deep black ink
INK_DARK = (31, 41, 55)            # Secondary dark ink
INK_MUTED = (75, 85, 99)           # Muted gray body text
BORDER_DARK = (17, 24, 39)         # Bold rule color
BORDER_LIGHT = (209, 213, 219)     # Hairline rule color
ACCENT_RED = (185, 28, 28)         # Editorial crimson
ACCENT_BLUE = (30, 58, 138)        # Diplomatic navy
CARD_BG = (255, 255, 255)          # Crisp white panel fill
PICTO_BG = (241, 245, 249)         # Light cool slate panel


def wrap_text(text, font, max_width, draw):
    """Wrap text into lines fitting within max_width."""
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        candidate = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)
    if current_line:
        lines.append(" ".join(current_line))
    return lines


def draw_star(draw, cx, cy, r_outer, r_inner, fill, points=5):
    """Draw a balanced 5-pointed star."""
    pts = []
    angle_step = math.pi / points
    for i in range(2 * points):
        r = r_outer if i % 2 == 0 else r_inner
        ang = i * angle_step - math.pi / 2
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def draw_usa_flag(draw, x, y, w, h):
    """Draw stylized USA flag."""
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK_BLACK, width=2)
    stripe_h = h / 13.0
    for i in range(13):
        if i % 2 == 0:
            sy = y + i * stripe_h
            draw.rectangle([x, sy, x + w, sy + stripe_h], fill=(185, 28, 28))
    # Canton
    canton_w = w * 0.42
    canton_h = stripe_h * 7
    draw.rectangle([x, y, x + canton_w, y + canton_h], fill=(30, 58, 138))
    # Canton star grid
    for row in range(3):
        for col in range(4):
            sx = x + 10 + col * (canton_w - 20) / 3
            sy = y + 8 + row * (canton_h - 16) / 2
            draw_star(draw, sx, sy, 3.5, 1.5, fill=(255, 255, 255))


def draw_china_flag(draw, x, y, w, h):
    """Draw stylized China flag."""
    draw.rectangle([x, y, x + w, y + h], fill=(220, 38, 38), outline=INK_BLACK, width=2)
    # Big star
    bx = x + w * 0.22
    by = y + h * 0.32
    draw_star(draw, bx, by, 16, 7, fill=(250, 204, 21))
    # 4 small stars
    small_positions = [
        (bx + 30, by - 20),
        (bx + 40, by - 5),
        (bx + 40, by + 15),
        (bx + 30, by + 30),
    ]
    for sx, sy in small_positions:
        draw_star(draw, sx, sy, 5.5, 2.5, fill=(250, 204, 21))


def draw_russia_flag(draw, x, y, w, h):
    """Draw stylized Russia flag."""
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK_BLACK, width=2)
    h3 = h / 3.0
    draw.rectangle([x, y, x + w, y + h3], fill=(255, 255, 255))
    draw.rectangle([x, y + h3, x + w, y + 2 * h3], fill=(29, 78, 216))
    draw.rectangle([x, y + 2 * h3, x + w, y + h], fill=(220, 38, 38))
    draw.rectangle([x, y, x + w, y + h], outline=INK_BLACK, width=2)


def draw_vector_pictogram(draw, box_x, box_y, box_w, box_h):
    """Draw clean vector pictogram: globe with diplomatic lines and 3 flags."""
    # Box container
    draw.rectangle(
        [box_x, box_y, box_x + box_w, box_y + box_h],
        fill=PICTO_BG,
        outline=BORDER_LIGHT,
        width=2,
    )
    # Header strip inside pictogram
    draw.rectangle(
        [box_x, box_y, box_x + box_w, box_y + 44],
        fill=(226, 232, 240),
    )
    font_pic_header = ImageFont.truetype(FONT_SANS_BOLD, 22)
    draw.text(
        (box_x + 20, box_y + 11),
        "DIPLOMATIC VECTOR: APEC TRILATERAL SUMMIT — BEIJING",
        font=font_pic_header,
        fill=ACCENT_BLUE,
    )

    # Globe center & radius
    gx = box_x + int(box_w * 0.58)
    gy = box_y + int(box_h * 0.55)
    gr = 175

    # Diplomatic connection arcs to globe center
    flag_w, flag_h = 170, 95
    fx_usa, fy_usa = box_x + 60, box_y + 75
    fx_chn, fy_chn = box_x + 60, box_y + 225
    fx_rus, fy_rus = box_x + 60, box_y + 375

    # Target point (Beijing coordinates on globe)
    beijing_x = gx - 30
    beijing_y = gy - 35

    # Draw connection lines from flag cards to Beijing
    for fx, fy in [(fx_usa, fy_usa), (fx_chn, fy_chn), (fx_rus, fy_rus)]:
        draw.line([(fx + flag_w + 10, fy + flag_h // 2), (beijing_x, beijing_y)], fill=(148, 163, 184), width=3)

    # Globe base fill
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(219, 234, 254), outline=ACCENT_BLUE, width=4)

    # Simplified landmass polygons inside globe
    # Eurasia / Asia
    draw.polygon([
        (gx - 60, gy - 120), (gx + 40, gy - 110), (gx + 120, gy - 70),
        (gx + 130, gy - 10), (gx + 70, gy + 30), (gx - 10, gy + 40),
        (gx - 50, gy - 10), (gx - 90, gy - 50), (gx - 80, gy - 90)
    ], fill=(134, 239, 172), outline=(34, 197, 94), width=2)

    # Africa / Middle East hint
    draw.polygon([
        (gx - 120, gy - 20), (gx - 50, gy + 10), (gx - 40, gy + 80),
        (gx - 80, gy + 120), (gx - 110, gy + 60), (gx - 130, gy + 10)
    ], fill=(134, 239, 172), outline=(34, 197, 94), width=2)

    # Latitude lines (ellipses)
    draw.ellipse([gx - gr + 8, gy - 60, gx + gr - 8, gy + 60], outline=(147, 197, 253), width=2)
    draw.ellipse([gx - gr + 25, gy - 110, gx + gr - 25, gy - 10], outline=(147, 197, 253), width=2)
    draw.ellipse([gx - gr + 25, gy + 10, gx + gr - 25, gy + 110], outline=(147, 197, 253), width=2)
    # Equator line
    draw.line([(gx - gr, gy), (gx + gr, gy)], fill=(59, 130, 246), width=2)
    # Longitude meridian arcs
    draw.ellipse([gx - 70, gy - gr, gx + 70, gy + gr], outline=(59, 130, 246), width=2)
    draw.ellipse([gx - 130, gy - gr, gx + 130, gy + gr], outline=(147, 197, 253), width=2)
    # Globe outline redraw
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=ACCENT_BLUE, width=4)

    # Beijing Summit indicator dot
    draw.ellipse([beijing_x - 10, beijing_y - 10, beijing_x + 10, beijing_y + 10], fill=(220, 38, 38), outline=(255, 255, 255), width=2)
    draw_star(draw, beijing_x, beijing_y, 7, 3, fill=(255, 255, 255))
    font_lbl = ImageFont.truetype(FONT_SANS_BOLD, 20)
    draw.text((beijing_x + 14, beijing_y - 12), "BEIJING SUMMIT", font=font_lbl, fill=INK_BLACK)

    # 3 Flags with labels
    font_flag_lbl = ImageFont.truetype(FONT_SANS_BOLD, 18)

    # USA
    draw_usa_flag(draw, fx_usa, fy_usa, flag_w, flag_h)
    draw.text((fx_usa, fy_usa + flag_h + 4), "UNITED STATES", font=font_flag_lbl, fill=INK_DARK)

    # CHINA
    draw_china_flag(draw, fx_chn, fy_chn, flag_w, flag_h)
    draw.text((fx_chn, fy_chn + flag_h + 4), "CHINA (HOST)", font=font_flag_lbl, fill=INK_DARK)

    # RUSSIA
    draw_russia_flag(draw, fx_rus, fy_rus, flag_w, flag_h)
    draw.text((fx_rus, fy_rus + flag_h + 4), "RUSSIA", font=font_flag_lbl, fill=INK_DARK)

    # Bottom caption strip inside box
    cap_y = box_y + box_h - 38
    draw.rectangle([box_x, cap_y, box_x + box_w, box_y + box_h], fill=(226, 232, 240))
    font_cap = ImageFont.truetype(FONT_SANS_REG, 19)
    draw.text(
        (box_x + 20, cap_y + 9),
        "Geopolitical Summit: Presidents Trump, Xi, and Putin confer on multilateral governance.",
        font=font_cap,
        fill=INK_MUTED,
    )


def create_front_page():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Margins and grid lines
    m_left = 60
    m_right = W - 60
    col_split_x = 1270  # Divider between lead and right column

    # =========================================================================
    # TOP HEADER & MASTHEAD
    # =========================================================================
    # Top info line
    font_meta = ImageFont.truetype(FONT_SANS_BOLD, 22)
    draw.text((m_left, 42), "INTERNATIONAL EDITION", font=font_meta, fill=INK_MUTED)
    draw.text((m_right - 440, 42), "GLOBAL INTELLIGENCE SUMMARY", font=font_meta, fill=INK_MUTED)

    # Thin rule above masthead
    draw.line([(m_left, 74), (m_right, 74)], fill=BORDER_LIGHT, width=2)

    # Masthead: "THE WORLD"
    font_masthead = ImageFont.truetype(FONT_SERIF_BOLD, 140)
    masthead_text = "THE WORLD"
    bbox_mh = draw.textbbox((0, 0), masthead_text, font=font_masthead)
    mh_w = bbox_mh[2] - bbox_mh[0]
    draw.text(((W - mh_w) // 2, 85), masthead_text, font=font_masthead, fill=INK_BLACK)

    # Dateline Banner Bar
    bar_y0, bar_y1 = 250, 302
    draw.rectangle([m_left, bar_y0, m_right, bar_y1], fill=INK_BLACK)
    font_date = ImageFont.truetype(FONT_SANS_BOLD, 28)
    date_text = "WEDNESDAY 18 NOVEMBER 2026"
    bbox_date = draw.textbbox((0, 0), date_text, font=font_date)
    dw = bbox_date[2] - bbox_date[0]
    draw.text(((W - dw) // 2, bar_y0 + 12), date_text, font=font_date, fill=(255, 255, 255))

    # Edition indicators on sides of dateline banner
    font_subdate = ImageFont.truetype(FONT_SANS_BOLD, 20)
    draw.text((m_left + 24, bar_y0 + 16), "VOL. CLXXIV NO. 62", font=font_subdate, fill=(209, 213, 219))
    draw.text((m_right - 230, bar_y0 + 16), "DAILY BROADSHEET", font=font_subdate, fill=(209, 213, 219))

    # Divider below banner
    draw.line([(m_left, bar_y1 + 10), (m_right, bar_y1 + 10)], fill=BORDER_DARK, width=2)

    # =========================================================================
    # MAIN COLUMN LAYOUT
    # Left: Lead story (X: 60 -> 1240)
    # Right: 5 short stories (X: 1300 -> 1988)
    # =========================================================================
    body_y_top = 328
    body_y_bottom = 1750

    # Vertical column separator
    draw.line([(col_split_x, body_y_top), (col_split_x, body_y_bottom)], fill=BORDER_LIGHT, width=2)

    # -------------------------------------------------------------------------
    # LEFT COLUMN: LEAD STORY (Asia / Diplomacy)
    # -------------------------------------------------------------------------
    cur_x = m_left
    lead_w = col_split_x - m_left - 30

    # Section tag badge
    badge_w, badge_h = 280, 36
    draw.rectangle([cur_x, body_y_top, cur_x + badge_w, body_y_top + badge_h], fill=ACCENT_RED)
    font_badge = ImageFont.truetype(FONT_SANS_BOLD, 22)
    draw.text((cur_x + 14, body_y_top + 6), "ASIA / DIPLOMACY", font=font_badge, fill=(255, 255, 255))

    font_kicker = ImageFont.truetype(FONT_SANS_BOLD, 22)
    draw.text((cur_x + badge_w + 16, body_y_top + 6), "APEC SUMMIT CONVENES IN CHINA", font=font_kicker, fill=INK_MUTED)

    # Lead Headline
    lead_hl_y = body_y_top + 48
    font_lead_hl = ImageFont.truetype(FONT_SERIF_BOLD, 54)
    lead_headline = "Trump meets Xi and Putin in Beijing"
    hl_lines = wrap_text(lead_headline, font_lead_hl, lead_w, draw)
    line_y = lead_hl_y
    for line in hl_lines:
        draw.text((cur_x, line_y), line, font=font_lead_hl, fill=INK_BLACK)
        line_y += 66

    # Lead Subdeck / Dek
    font_dek = ImageFont.truetype(FONT_SERIF_REG, 29)
    lead_dek = (
        "Xi says Russia and China should lead a multipolar world as US President arrives "
        "for high-stakes trilateral summit amid APEC gathering."
    )
    dek_lines = wrap_text(lead_dek, font_dek, lead_w, draw)
    line_y += 6
    for line in dek_lines:
        draw.text((cur_x, line_y), line, font=font_dek, fill=INK_DARK)
        line_y += 40

    # Vector Pictogram illustration box
    pic_box_y = line_y + 16
    pic_box_h = 515
    draw_vector_pictogram(draw, cur_x, pic_box_y, lead_w, pic_box_h)

    # Lead Story Body Text
    body_text_y = pic_box_y + pic_box_h + 24
    font_lead_body = ImageFont.truetype(FONT_SERIF_REG, 25)
    lead_narrative = (
        "BEIJING — In an extraordinary diplomatic realignment, Donald Trump met with Chinese President "
        "Xi Jinping and Russian President Vladimir Putin today on the sidelines of the APEC Summit. "
        "President Xi framed the summit as a cornerstone for global restructuring, declaring that Beijing "
        "and Moscow must guide a multipolar world order. Discussions centered on strategic balance, "
        "regional conflicts, and trade relations, marking the first direct trilateral encounter of its kind."
    )
    body_lines = wrap_text(lead_narrative, font_lead_body, lead_w, draw)
    b_y = body_text_y
    for bline in body_lines:
        draw.text((cur_x, b_y), bline, font=font_lead_body, fill=INK_DARK)
        b_y += 36

    # -------------------------------------------------------------------------
    # RIGHT COLUMN: FIVE REGIONAL / WORLD STORIES
    # -------------------------------------------------------------------------
    rx = col_split_x + 30
    rw = m_right - rx

    stories = [
        {
            "tag": "EUROPE / WAR",
            "tag_color": ACCENT_RED,
            "headline": "Ukraine Strikes Kerch Bridge in Crimea",
            "body": "Ukrainian forces targeted the strategic Crimean span, inflicting fresh damage and delivering a symbolic blow to Putin.",
        },
        {
            "tag": "MIDDLE EAST",
            "tag_color": (154, 52, 18),
            "headline": "Iran Attacks Bahrain, Kuwait; Tanker Hit",
            "body": "Iranian strikes hit targets in Bahrain and Kuwait; an ADNOC vessel was struck in the strategic Strait of Hormuz.",
        },
        {
            "tag": "MARKETS / TECH",
            "tag_color": (6, 95, 70),
            "headline": "Nvidia Beats Earnings, Rebuffs Huang Calls",
            "body": "Nvidia reported blockbuster quarterly results and firmly dismissed shareholder petitions to reinstate Jensen Huang.",
        },
        {
            "tag": "US POLITICS",
            "tag_color": (55, 48, 163),
            "headline": "Peltola Wins Alaska, Setting Senate at 56-44",
            "body": "Democrat Mary Peltola clinched the contested Alaska Senate race, establishing the final chamber balance at 56-44.",
        },
        {
            "tag": "RUSSIA",
            "tag_color": (30, 41, 59),
            "headline": "19 Dead in Siberian Military Plane Crash",
            "body": "A Russian military transport plane crashed during severe conditions in Siberia, killing all 19 servicemen aboard.",
        },
    ]

    total_h = body_y_bottom - body_y_top
    slot_h = total_h / len(stories)

    font_st_tag = ImageFont.truetype(FONT_SANS_BOLD, 21)
    font_st_hl = ImageFont.truetype(FONT_SERIF_BOLD, 30)
    font_st_body = ImageFont.truetype(FONT_SANS_REG, 23)

    for i, s in enumerate(stories):
        sy = body_y_top + int(i * slot_h)

        # Story Tag
        draw.text((rx, sy), s["tag"], font=font_st_tag, fill=s["tag_color"])

        # Story Headline
        hl_y = sy + 32
        hl_lines = wrap_text(s["headline"], font_st_hl, rw, draw)
        for hline in hl_lines:
            draw.text((rx, hl_y), hline, font=font_st_hl, fill=INK_BLACK)
            hl_y += 38

        # Story Body (short line)
        body_y = hl_y + 6
        sb_lines = wrap_text(s["body"], font_st_body, rw, draw)
        for sline in sb_lines:
            draw.text((rx, body_y), sline, font=font_st_body, fill=INK_MUTED)
            body_y += 31

        # Divider line between stories (except after last story)
        if i < len(stories) - 1:
            div_y = body_y_top + int((i + 1) * slot_h) - 14
            draw.line([(rx, div_y), (m_right, div_y)], fill=BORDER_LIGHT, width=1)

    # =========================================================================
    # BOTTOM STRIP: SPACE & HEALTH
    # =========================================================================
    # Bold double horizontal rule above bottom strip
    strip_y_top = 1762
    draw.line([(m_left, strip_y_top), (m_right, strip_y_top)], fill=BORDER_DARK, width=3)
    draw.line([(m_left, strip_y_top + 6), (m_right, strip_y_top + 6)], fill=BORDER_DARK, width=1)

    bottom_col_w = (m_right - m_left - 50) // 2
    b1_x = m_left
    b2_x = m_left + bottom_col_w + 50

    # Vertical divider between the two bottom stories
    draw.line(
        [(m_left + bottom_col_w + 25, strip_y_top + 16), (m_left + bottom_col_w + 25, 1990)],
        fill=BORDER_LIGHT,
        width=2,
    )

    # Bottom Story 1: SPACE
    font_bot_tag = ImageFont.truetype(FONT_SANS_BOLD, 22)
    font_bot_hl = ImageFont.truetype(FONT_SERIF_BOLD, 31)
    font_bot_body = ImageFont.truetype(FONT_SANS_REG, 23)

    draw.text((b1_x, strip_y_top + 18), "SPACE EXPLORATION", font=font_bot_tag, fill=ACCENT_BLUE)
    draw.text(
        (b1_x, strip_y_top + 52),
        "NASA's Voyager 1 reaches one light-day from Earth",
        font=font_bot_hl,
        fill=INK_BLACK,
    )
    b1_summary = (
        "Humanity's farthest explorer surpasses 14.1 billion miles, reaching a milestone of 24 light-hours."
    )
    b1_lines = wrap_text(b1_summary, font_bot_body, bottom_col_w, draw)
    for idx, bl in enumerate(b1_lines):
        draw.text((b1_x, strip_y_top + 98 + idx * 30), bl, font=font_bot_body, fill=INK_MUTED)

    # Bottom Story 2: HEALTH
    draw.text((b2_x, strip_y_top + 18), "PUBLIC HEALTH", font=font_bot_tag, fill=ACCENT_RED)
    draw.text(
        (b2_x, strip_y_top + 52),
        "United States loses measles elimination status",
        font=font_bot_hl,
        fill=INK_BLACK,
    )
    b2_summary = (
        "Health authorities report domestic transmission chains ending 26 years of official eradication."
    )
    b2_lines = wrap_text(b2_summary, font_bot_body, bottom_col_w, draw)
    for idx, bl in enumerate(b2_lines):
        draw.text((b2_x, strip_y_top + 98 + idx * 30), bl, font=font_bot_body, fill=INK_MUTED)

    # =========================================================================
    # FOOTER BAR
    # =========================================================================
    footer_y = 2006
    draw.line([(m_left, footer_y), (m_right, footer_y)], fill=BORDER_LIGHT, width=1)
    font_footer = ImageFont.truetype(FONT_SANS_REG, 19)
    footer_str = "THE WORLD • SPECIAL EDITION • COMPILATION OF 18 NOVEMBER 2026 WORLD EVENTS • MAKE.FUN ENTRY"
    bbox_ft = draw.textbbox((0, 0), footer_str, font=font_footer)
    ft_w = bbox_ft[2] - bbox_ft[0]
    draw.text(((W - ft_w) // 2, footer_y + 10), footer_str, font=font_footer, fill=(156, 163, 175))

    # =========================================================================
    # DOWNSCALE & SAVE
    # =========================================================================
    downscaled = img.resize((OUT_W, OUT_H), Image.Resampling.LANCZOS)
    downscaled.save("entry.png", "PNG", optimize=True)
    print(f"Generated entry.png: {OUT_W}x{OUT_H}")


if __name__ == "__main__":
    create_front_page()
