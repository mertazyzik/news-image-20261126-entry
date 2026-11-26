#!/usr/bin/env python3
"""Render a one-page newspaper front page summing up 26 November 2026.

Deterministic: fixed text, fixed layout, fixed fonts -> identical bytes
on every run. Output: entry.png, 1024x1024.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 236)
INK = (22, 22, 22)
RULE = (22, 22, 22)
ACCENT = (158, 28, 28)
MUTED = (96, 90, 80)
LIGHT_LINE = (180, 172, 158)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def para(draw, x, y, width, text, fnt, fill=INK, leading=1.28):
    lines = wrap(draw, text, fnt, width)
    lh = int(fnt.size * leading)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def kicker(draw, x, y, text):
    f = font(SANS_B, 15)
    draw.text((x, y), text.upper(), font=f, fill=ACCENT)
    return y + 22


def headline(draw, x, y, width, text, size=30):
    f = font(SERIF_B, size)
    lines = wrap(draw, text, f, width)
    lh = int(size * 1.06)
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=INK)
        y += lh
    return y + 4


def rule(draw, x, y, width, wdt=2, color=RULE):
    draw.line([(x, y), (x + width, y)], fill=color, width=wdt)
    return y + wdt + 6


def story(draw, x, y, width, kick, head, body, head_size=27, body_size=17):
    y = kicker(draw, x, y, kick)
    y = headline(draw, x, y, width, head, size=head_size)
    y = para(draw, x, y, width, body, font(SERIF, body_size),
             leading=1.32)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 44  # margin
    cw = W - 2 * mx  # content width

    # ---- masthead ----
    y = 30
    d.text((mx, y), "THE WORLD IN ONE DAY", font=font(SERIF_B, 58),
           fill=INK)
    y += 66
    d.text((mx, y), "THURSDAY, 26 NOVEMBER 2026  ·  ONE PAGE, SEVEN STORIES, THE DAY AS IT HAPPENED",
           font=font(SANS_B, 15), fill=MUTED)
    y += 26
    d.line([(mx, y), (mx + cw, y)], fill=RULE, width=4)
    y += 14

    # ---- lead story, full width ----
    y = story(
        d, mx, y, cw,
        "Washington · Trade",
        "Trump unveils new tariffs on 14 nations",
        "The White House proposed duties of 15% to 40% under Section 301, "
        "accusing China, the EU and 12 others of flooding world markets. "
        "China faces 20%, rising to 40% if the trade truce lapses in "
        "January; most others are capped by existing deals. Markets "
        "rallied — the bite is smaller than feared.",
        head_size=40, body_size=19)
    y += 4
    y = rule(d, mx, y, cw, wdt=2)
    y += 6

    # ---- two columns: UK-EU | SpaceX ----
    col_w = (cw - 28) // 2
    y_top = y
    y2 = story(
        d, mx, y, col_w,
        "London · Brexit reset",
        "UK–EU treaty has a 10-year exit clause",
        "Texts published today: either side quitting the food deal "
        "within a decade must pay to rebuild the border checks it "
        "scraps. Farm exports are forecast to rise 16%.",
        head_size=27, body_size=17)
    y3 = story(
        d, mx + col_w + 28, y, col_w,
        "Washington · Space",
        "FCC clears SpaceX for a million satellites",
        "The Starmind constellation — data centres in orbit for AI — "
        "wins the first US approval of its kind. First satellite by "
        "2033, full fleet by 2040. Astronomers warn of a crowded sky.",
        head_size=27, body_size=17)
    y = max(y2, y3) + 6
    d.line([(mx + col_w + 14, y_top),
            (mx + col_w + 14, y - 8)], fill=LIGHT_LINE, width=1)
    y = rule(d, mx, y, cw, wdt=1, color=LIGHT_LINE)
    y += 4

    # ---- three columns: mine | Gaza | Myanmar ----
    col3 = (cw - 2 * 24) // 3
    x1, x2, x3 = mx, mx + col3 + 24, mx + 2 * (col3 + 24)
    ya = story(
        d, x1, y, col3,
        "Bogor, West Java",
        "13 dead as rain floods illegal gold mine",
        "A pit 100 metres deep filled with water on Monday. "
        "Thirteen miners are confirmed dead and 13 still missing; "
        "heavy rain halted the rescue today.",
        head_size=23, body_size=16)
    yb = story(
        d, x2, y, col3,
        "Gaza",
        "Strikes kill 8 as ceasefire frays",
        "Overnight raids hit Deir al-Balah and Gaza City, killing a "
        "Hamas education official and his wife — the third senior "
        "official killed in three nights.",
        head_size=23, body_size=16)
    yc = story(
        d, x3, y, col3,
        "The Hague",
        "Myanmar defies genocide ruling",
        "Min Aung Hlaing says his government will not obey parts of "
        "the World Court's order — the first time the ICJ has found "
        "a state guilty of genocide.",
        head_size=23, body_size=16)
    y = max(ya, yb, yc) + 8
    y = rule(d, mx, y, cw, wdt=2)
    y += 4

    # ---- also strip ----
    f_also = font(SANS_B, 15)
    d.text((mx, y), "ALSO IN THE NEWS", font=f_also, fill=ACCENT)
    y += 24
    items = [
        "German boat dealer 'supplied a third of Channel crossings', BBC finds",
        "31 killed as fuel-tanker fire engulfs Cairo ring road",
        "Duran Duran guitarist Andy Taylor dies, aged 65",
        "Seven hurt in Bangkok refinery blast; FedEx jet overshoots Miami runway",
        "Macy's Thanksgiving parade postponed as storms hit the US",
    ]
    f_item = font(SERIF, 16)
    for it in items:
        d.text((mx + 16, y), "•", font=f_item, fill=ACCENT)
        y = para(d, mx + 36, y, cw - 36, it, f_item, leading=1.15)
        y += 2
    y += 6
    y = rule(d, mx, y, cw, wdt=1, color=LIGHT_LINE)
    y += 2

    # ---- bottom feature: DR Congo + the day in numbers ----
    yb = story(
        d, mx, y, col_w,
        "Kinshasa · Diplomacy",
        "DR Congo protests Ugandan general's threats",
        "Kinshasa summoned Uganda's envoy after Gen. Muhoozi "
        "Kainerugaba, the president's son, posted threats against "
        "DR Congo online.",
        head_size=22, body_size=15)
    nx = mx + col_w + 28
    d.rectangle([(nx, y), (nx + col_w, y + 108)], outline=LIGHT_LINE,
                width=1)
    d.text((nx + 14, y + 9), "THE DAY IN NUMBERS",
           font=font(SANS_B, 14), fill=ACCENT)
    nums = [("14", "nations face new US tariffs"),
            ("1,000,000", "satellites in SpaceX's Starmind plan"),
            ("13 + 13", "dead and missing in the Bogor mine flood"),
            ("31", "killed in the Cairo tanker fire")]
    ny = y + 32
    for n, label in nums:
        d.text((nx + 14, ny), n, font=font(SERIF_B, 16), fill=INK)
        d.text((nx + 118, ny + 2), label, font=font(SERIF, 14),
               fill=INK)
        ny += 19
    y = max(yb, y + 108) + 6

    # ---- footer ----
    y = H - 46
    d.line([(mx, y), (mx + cw, y)], fill=RULE, width=2)
    y += 10
    d.text((mx, y),
           "Sources: BBC, Reuters, AP, CNN, USTR, FCC — 26 November 2026  ·  Drawn by an AI agent for make.fun",
           font=font(SANS, 13), fill=MUTED)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
