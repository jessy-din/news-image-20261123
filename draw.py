#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news front page, 1024x1024 PNG.

Deterministic: no timestamps, no randomness, fixed palette and layout.
Render with:  python3 draw.py   (writes entry.png next to this file)
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

# ---- palette -------------------------------------------------------------
INK = (18, 18, 18)
PAPER = (252, 251, 247)
RED = (178, 34, 28)
GREY = (96, 96, 96)
RULE = (30, 30, 30)
SEA_DARK = (16, 42, 74)
SEA = (24, 64, 108)
SKY_TOP = (232, 196, 150)
SKY_BOT = (214, 158, 110)
SHIP = (38, 44, 52)
SMOKE = (120, 118, 112)
FIRE = (240, 140, 40)
FIRE2 = (250, 200, 70)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, x0, x1, y, w=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=w)


def kicker(draw, x, y, text, size=17):
    f = font(SANS_B, size)
    draw.text((x, y), text, font=f, fill=RED)
    return y + size + 6


# ---- hero art: dusk sea, warship, explosion, drones ----------------------
def hero_art(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=SKY_TOP)
    # sky gradient bands
    bands = 24
    for i in range(bands):
        t = i / (bands - 1)
        r = int(SKY_TOP[0] + (SKY_BOT[0] - SKY_TOP[0]) * t)
        g = int(SKY_TOP[1] + (SKY_BOT[1] - SKY_TOP[1]) * t)
        b = int(SKY_TOP[2] + (SKY_BOT[2] - SKY_TOP[2]) * t)
        yy0 = y0 + int((y1 - y0) * 0.55 * i / bands)
        yy1 = y0 + int((y1 - y0) * 0.55 * (i + 1) / bands)
        draw.rectangle([x0, yy0, x1, yy1], fill=(r, g, b))
    # low sun
    cx, cy = x0 + int((x1 - x0) * 0.82), y0 + int((y1 - y0) * 0.30)
    draw.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(250, 214, 140))
    # sea
    sea_y = y0 + int((y1 - y0) * 0.55)
    draw.rectangle([x0, sea_y, x1, y1], fill=SEA)
    for i in range(5):
        yy = sea_y + 14 + i * 16
        draw.line([(x0 + 20 + i * 30, yy), (x1 - 60 - i * 22, yy)],
                  fill=SEA_DARK, width=3)
    # warship silhouette (hull + superstructure + mast)
    hx0, hx1 = x0 + 60, x0 + 430
    hy = y1 - 46
    draw.polygon([(hx0, hy), (hx1, hy), (hx1 - 26, hy - 34),
                  (hx0 + 40, hy - 34)], fill=SHIP)
    draw.rectangle([hx0 + 120, hy - 66, hx0 + 250, hy - 34], fill=SHIP)
    draw.rectangle([hx0 + 168, hy - 92, hx0 + 196, hy - 66], fill=SHIP)
    draw.line([(hx0 + 182, hy - 92), (hx0 + 182, hy - 108)],
              fill=SHIP, width=4)
    # explosion burst above the stern (kept inside the art box)
    ex, ey = hx0 + 330, hy - 40
    for r, col in ((46, FIRE), (30, FIRE2), (16, (255, 240, 180))):
        pts = []
        import math
        for k in range(12):
            ang = k * math.pi / 6
            rr = r if k % 2 == 0 else r * 0.55
            pts.append((ex + rr * math.cos(ang), ey + rr * math.sin(ang)))
        draw.polygon(pts, fill=col)
    # smoke plume (kept inside the art box)
    draw.ellipse([ex - 56, ey - 66, ex - 4, ey - 12], fill=SMOKE)
    draw.ellipse([ex - 34, ey - 84, ex + 14, ey - 30], fill=(140, 138, 132))
    # three small drones
    for dx, dy in ((x0 + 620, y0 + 26), (x0 + 700, y0 + 58),
                   (x0 + 560, y0 + 70)):
        draw.ellipse([dx - 12, dy - 4, dx + 12, dy + 4], fill=(30, 30, 30))
        draw.line([(dx - 22, dy - 8), (dx + 22, dy - 8)], fill=(30, 30, 30),
                  width=2)
        draw.line([(dx, dy + 4), (dx, dy + 12)], fill=(30, 30, 30), width=2)
    # caption bar inside art, bottom-left
    draw.rectangle([x0, y1 - 26, x0 + 600, y1], fill=(0, 0, 0))
    draw.text((x0 + 12, y1 - 22),
              "OFF THE LIBYAN COAST  \u2014  UKRAINIAN DRONES STRIKE",
              font=font(SANS_B, 14), fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36                      # margin
    X1 = W - M

    # ---- masthead --------------------------------------------------------
    f_top = font(SANS_B, 20)
    top = "THE WORLD IN ONE DAY"
    tw = d.textlength(top, font=f_top)
    d.text(((W - tw) / 2, 18), top, font=f_top, fill=INK)
    # thin rules flanking the masthead
    hrule(d, M, (W - tw) / 2 - 16, 30, 1)
    hrule(d, (W + tw) / 2 + 16, X1, 30, 1)

    # ---- date: the largest type on the page (auto-fit to the margins) ----
    date = "MONDAY 23 NOVEMBER 2026"
    size = 62
    while True:
        f_date = font(SERIF_B, size)
        dw = d.textlength(date, font=f_date)
        if dw <= X1 - M or size <= 40:
            break
        size -= 1
    d.text(((W - dw) / 2, 48), date, font=f_date, fill=INK)
    hrule(d, M, X1, 118, 3)

    # ---- hero art --------------------------------------------------------
    hero_art(d, M, 130, X1, 296)

    # ---- hero kicker + headline (max 2 lines) + deck ---------------------
    y = kicker(d, M, 308, "UKRAINE WAR SPREADS TO THE MEDITERRANEAN", 19)
    f_hero = font(SERIF_B, 40)
    hero_lines = wrap(d, "Ukrainian drones strike Russian warship off Libya",
                      f_hero, X1 - M)
    y = draw_lines(d, hero_lines, M, y, f_hero, INK, 48)
    f_deck = font(SANS, 19)
    deck = ("Zelensky says the strikes sank the Russian corvette Merkury and "
            "hit the cargo vessel Angara \u2014 the war\u2019s reach now "
            "stretches to North Africa.")
    y = draw_lines(d, wrap(d, deck, f_deck, X1 - M), M, y + 4, f_deck,
                   (40, 40, 40), 25)
    hrule(d, M, X1, 508, 2)

    # ---- three medium stories --------------------------------------------
    mediums = [
        ("CLIMATE  \u00b7  COP31, ANTALYA",
         "COP31 ends with no climate deal",
         "The longest UN climate talks in history close in Antalya with no "
         "major agreement, exposing deep divisions between nations."),
        ("UKRAINE  \u00b7  KYIV REGION",
         "Russian strikes kill 15 near Kyiv",
         "A boy, 7, is pulled alive from rubble after a block of flats "
         "collapses in Dymer. Zelensky urges the US to release Patriot "
         "missiles."),
        ("GAZA",
         "Gaza now a \u2018toxic wasteland\u2019, Oxfam says",
         "Israeli attacks have left Gaza toxic and polluted, Oxfam warns, "
         "with contamination across almost the whole territory."),
    ]
    col_w = (X1 - M - 2 * 24) // 3
    y0 = 522
    for i, (kick, head, body) in enumerate(mediums):
        x = M + i * (col_w + 24)
        yy = kicker(d, x, y0, kick, 15)
        f_h = font(SERIF_B, 23)
        yy = draw_lines(d, wrap(d, head, f_h, col_w), x, yy, f_h, INK, 28)
        f_b = font(SANS, 16)
        draw_lines(d, wrap(d, body, f_b, col_w), x, yy + 3, f_b,
                   (40, 40, 40), 21)
    hrule(d, M, X1, 690, 2)

    # ---- four small stories, 2 x 2 ---------------------------------------
    smalls = [
        ("TECH  \u00b7  NVIDIA",
         "Nvidia reinstates chief Jensen Huang",
         "Trump says \u201cI made the deal\u201d as Huang returns after an "
         "affair with an alleged spy."),
        ("IRAN  \u00b7  STRAIT OF HORMUZ",
         "Tankers set ablaze in Hormuz",
         "Oil tankers burn in the strait as Tehran warns its enemies seek "
         "unrest at home."),
        ("BELGIUM",
         "Flights axed in cost-of-living strike",
         "Belgian flights are cancelled and Brussels sees clashes after an "
         "anti-austerity protest."),
        ("ASIA  \u00b7  INDIA\u2013NEPAL",
         "India pledges $1.6bn to Nepal",
         "New Delhi promises $1.6 billion in a reset of ties with "
         "Kathmandu."),
    ]
    sw = (X1 - M - 24) // 2
    y0 = 704
    for i, (kick, head, body) in enumerate(smalls):
        x = M + (i % 2) * (sw + 24)
        yy = y0 + (i // 2) * 84
        yy = kicker(d, x, yy, kick, 14)
        f_h = font(SERIF_B, 20)
        yy = draw_lines(d, wrap(d, head, f_h, sw), x, yy, f_h, INK, 24)
        f_b = font(SANS, 15)
        draw_lines(d, wrap(d, body, f_b, sw), x, yy + 2, f_b,
                   (40, 40, 40), 19)
    hrule(d, M, X1, 880, 2)

    # ---- briefs -----------------------------------------------------------
    y = kicker(d, M, 892, "ALSO ON 23 NOVEMBER", 16)
    briefs = [
        "Democrats win largest US House majority since 1992",
        "France: far-left march against Macron",
        "Nigeria: race to find survivors after boat tragedy",
        "Mexico: soldiers attacked after drug lord arrest",
        "Kenya and DR Congo agree to restore ties",
        "Iran flogs singer who performed without hijab",
        "Colombia marks 10 years since FARC peace deal",
        "Sudan: drone attacks kill four near Khartoum",
    ]
    f_br = font(SANS_B, 14)
    bw = (X1 - M - 24) // 2
    for i, b in enumerate(briefs):
        x = M + (i % 2) * (bw + 24)
        yy = y + (i // 2) * 22
        # fit each brief to one line; shorten if needed
        txt = b
        while d.textlength("\u2022  " + txt, font=f_br) > bw and len(txt) > 10:
            txt = txt.rsplit(" ", 1)[0] + "\u2026"
        d.text((x, yy), "\u2022  " + txt, font=f_br, fill=INK)
    # ---- footer -----------------------------------------------------------
    f_f = font(SANS, 12)
    foot = "Sources: BBC World \u00b7 Al Jazeera \u2014 all stories reported 23 November 2026"
    fw = d.textlength(foot, font=f_f)
    d.text(((W - fw) / 2, H - 20), foot, font=f_f, fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
