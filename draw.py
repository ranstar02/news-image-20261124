#!/usr/bin/env python3
"""Render the news-image-20261124 entry: a one-page newspaper front page
summing up Tuesday 24 November 2026. All shapes are drawn from scratch
with Pillow; no photos, no external assets, no network.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (25, 25, 25)
RED = (166, 30, 34)
BLUE = (23, 69, 110)
TEAL = (20, 101, 90)
GOLD = (192, 138, 30)
ORANGE = (214, 110, 30)
GREY = (90, 86, 78)
LIGHT = (232, 226, 212)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def center_text(draw, y, text, fnt, fill, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


def globe(draw, cx, cy, r):
    """Simple globe pictogram: blue disc, green land blobs, red crack."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLUE,
                 outline=INK, width=4)
    # land masses (abstract blobs)
    draw.ellipse([cx - r * 0.62, cy - r * 0.55, cx - r * 0.05, cy - r * 0.05],
                 fill=(46, 139, 87))
    draw.ellipse([cx + r * 0.05, cy + r * 0.10, cx + r * 0.60, cy + r * 0.55],
                 fill=(46, 139, 87))
    draw.ellipse([cx - r * 0.25, cy + r * 0.30, cx + r * 0.30, cy + r * 0.62],
                 fill=(46, 139, 87))
    # latitude lines
    for dy, half in ((-0.45, 0.89), (0.45, 0.89)):
        y = cy + r * dy
        x = r * half
        draw.arc([cx - x, y - 6, cx + x, y + 6], 0, 180, fill=(255, 255, 255),
                 width=2)
    # red crack across the globe
    draw.line([(cx - r * 0.7, cy - r * 0.75), (cx - r * 0.1, cy - r * 0.15),
               (cx + r * 0.35, cy + r * 0.25), (cx + r * 0.75, cy + r * 0.8)],
              fill=RED, width=7)


def burst(draw, cx, cy, s, color=ORANGE):
    """Starburst / explosion pictogram."""
    import math
    r = 42 * s
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=color, outline=INK)
    draw.ellipse([cx - r * 0.28, cy - r * 0.28, cx + r * 0.28, cy + r * 0.28],
                 fill=(255, 214, 90), outline=INK, width=2)


def ship(draw, cx, cy, s):
    """Ship on waves with a flame."""
    draw.polygon([(cx - 70 * s, cy), (cx + 70 * s, cy), (cx + 55 * s, cy + 26 * s),
                  (cx - 55 * s, cy + 26 * s)], fill=(120, 40, 30), outline=INK,
                 width=2)
    draw.rectangle([cx - 30 * s, cy - 26 * s, cx + 10 * s, cy], fill=INK)
    draw.rectangle([cx + 18 * s, cy - 18 * s, cx + 40 * s, cy], fill=INK)
    # flame on deck
    draw.polygon([(cx + 28 * s, cy - 18 * s), (cx + 18 * s, cy - 44 * s),
                  (cx + 34 * s, cy - 30 * s), (cx + 44 * s, cy - 52 * s),
                  (cx + 52 * s, cy - 26 * s)], fill=ORANGE, outline=INK)
    for i, x in enumerate((-80, -20, 40)):
        draw.arc([cx + x * s, cy + 34 * s, cx + (x + 44) * s, cy + 52 * s],
                 180, 360, fill=BLUE, width=4)


def chip(draw, cx, cy, s):
    """Computer chip pictogram with a rising arrow."""
    draw.rectangle([cx - 42 * s, cy - 42 * s, cx + 42 * s, cy + 42 * s],
                   fill=INK, outline=INK)
    draw.rectangle([cx - 26 * s, cy - 26 * s, cx + 26 * s, cy + 26 * s],
                   fill=(46, 139, 87), outline=(255, 255, 255), width=2)
    for i in range(3):
        for x in (-42, 42):
            y = cy + (i - 1) * 26 * s
            draw.line([(x * s + cx, y), (x * s + cx + (14 if x < 0 else -14) * s,
                        y)], fill=INK, width=4)
        for y in (-42, 42):
            x = cx + (i - 1) * 26 * s
            draw.line([(x, y * s + cy), (x, y * s + cy + (14 if y < 0 else -14) * s)],
                      fill=INK, width=4)
    # rising arrow
    draw.line([(cx + 58 * s, cy + 34 * s), (cx + 58 * s, cy - 34 * s)],
              fill=RED, width=6)
    draw.polygon([(cx + 46 * s, cy - 22 * s), (cx + 58 * s, cy - 44 * s),
                  (cx + 70 * s, cy - 22 * s)], fill=RED)


def factory(draw, cx, cy, s):
    """Factory silhouette with smoke and flame."""
    draw.rectangle([cx - 62 * s, cy - 10 * s, cx + 62 * s, cy + 34 * s],
                   fill=(90, 86, 78), outline=INK, width=2)
    draw.polygon([(cx - 62 * s, cy - 10 * s), (cx - 62 * s, cy - 34 * s),
                  (cx - 30 * s, cy - 34 * s), (cx - 30 * s, cy - 10 * s)],
                 fill=(90, 86, 78), outline=INK)
    draw.rectangle([cx + 34 * s, cy - 52 * s, cx + 48 * s, cy - 10 * s],
                   fill=(120, 40, 30), outline=INK, width=2)
    for x in (-44, -14, 16):
        draw.rectangle([cx + x * s, cy + 4 * s, cx + (x + 16) * s, cy + 20 * s],
                       fill=(255, 214, 90), outline=INK, width=2)
    # smoke puffs
    for i, (dx, dy, r) in enumerate(((0, -62, 9), (10, -76, 11), (-6, -90, 8))):
        draw.ellipse([cx + dx * s - r, cy + dy * s - r, cx + dx * s + r,
                      cy + dy * s + r], fill=(180, 175, 165), outline=GREY)


def king(draw, cx, cy, s):
    """Chess king pictogram on a checker square."""
    draw.rectangle([cx - 52 * s, cy - 52 * s, cx + 52 * s, cy + 52 * s],
                   fill=(255, 255, 255), outline=INK, width=3)
    draw.rectangle([cx - 52 * s, cy - 52 * s, cx, cy], fill=LIGHT)
    draw.rectangle([cx, cy, cx + 52 * s, cy + 52 * s], fill=LIGHT)
    # king in red so it reads on both light and dark squares
    draw.line([(cx, cy - 44 * s), (cx, cy - 26 * s)], fill=RED, width=5)
    draw.line([(cx - 9 * s, cy - 35 * s), (cx + 9 * s, cy - 35 * s)],
              fill=RED, width=5)
    draw.ellipse([cx - 12 * s, cy - 26 * s, cx + 12 * s, cy - 2 * s],
                 fill=RED, outline=INK, width=2)
    draw.polygon([(cx - 16 * s, cy - 2 * s), (cx + 16 * s, cy - 2 * s),
                  (cx + 26 * s, cy + 34 * s), (cx - 26 * s, cy + 34 * s)],
                 fill=RED, outline=INK)
    draw.rectangle([cx - 30 * s, cy + 34 * s, cx + 30 * s, cy + 46 * s],
                   fill=RED, outline=INK)


def card(draw, x, y, w, h, kicker, kcolor, headline, body, pic):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                   outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + 26], fill=kcolor)
    draw.text((x + 10, y + 4), kicker, font=font(SANS_B, 15), fill=(255, 255, 255))
    px, py = x + 14, y + 40
    pic(draw, px + 42, py + 42, 0.55)
    tx = x + 112
    hl = wrap(draw, headline, font(SANS_B, 21), w - 122)
    yy = y + 38
    for line in hl:
        draw.text((tx, yy), line, font=font(SANS_B, 21), fill=INK)
        yy += 25
    bl = wrap(draw, body, font(SANS, 15), w - 20)
    yy = y + 132
    for line in bl[:2]:
        draw.text((x + 10, yy), line, font=font(SANS, 15), fill=(60, 58, 52))
        yy += 19


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 148], fill=INK)
    center_text(d, 14, "THE WORLD IN ONE DAY", font(SERIF, 58),
                (246, 241, 231))
    center_text(d, 86, "TUESDAY,  24  NOVEMBER  2026", font(SANS_B, 34), RED)
    d.line([(28, 140), (W - 28, 140)], fill=(246, 241, 231), width=2)
    center_text(d, 152, "ONE DAY  ·  ONE PAGE  ·  THE STORIES THAT MATTERED",
                font(SANS, 15), GREY)

    # ---- lead story: COP31 ----
    d.rectangle([28, 182, 996, 436], fill=(255, 255, 255), outline=INK, width=3)
    d.rectangle([28, 182, 996, 214], fill=RED)
    d.text((44, 189), "CLIMATE  ·  COP31  ·  LEAD STORY", font=font(SANS_B, 16),
           fill=(255, 255, 255))
    globe(d, 190, 330, 92)
    d.text((320, 232), "COP31 ENDS", font=font(SERIF, 62), fill=INK)
    d.text((320, 296), "WITH NO DEAL", font=font(SERIF, 62), fill=RED)
    lead = ("Climate talks collapse after Saudi pushback. "
            "Negotiations may resume next year, the BBC reports.")
    yy = 366
    for line in wrap(d, lead, font(SANS, 19), 640):
        d.text((320, yy), line, font=font(SANS, 19), fill=(60, 58, 52))
        yy += 25

    # ---- story cards ----
    cards = [
        ("UKRAINE", BLUE, "12 KILLED IN KYIV REGION",
         "Russian drone and missile strikes hit homes in Dymer.",
         burst),
        ("LIBYA SEA", TEAL, "UKRAINE SAYS IT SANK A RUSSIAN WARSHIP",
         "Kyiv claims its forces hit a corvette docked at Benghazi port.",
         ship),
        ("BUSINESS", GOLD, "HUANG BACK AT NVIDIA",
         "Board reinstates the CEO; shares jump 31% in a single day.",
         chip),
        ("INDONESIA", ORANGE, "24 DEAD IN FACTORY FIRE",
         "Candy plant blaze in Banten; about 30 workers still missing.",
         factory),
        ("SPORT", INK, "CHESS CROWN DEFENCE OPENS",
         "Gukesh meets Sindarov in Geneva for the world title.",
         king),
    ]
    cw, ch, gap = 308, 196, 12
    x0, y0 = 28, 456
    for i, (kick, col, hl, body, pic) in enumerate(cards):
        cx = x0 + (i % 3) * (cw + gap)
        cy = y0 + (i // 3) * (ch + gap)
        card(d, cx, cy, cw, ch, kick, col, hl, body, pic)

    # ---- also today cell ----
    ax = x0 + 2 * (cw + gap)
    ay = y0 + 1 * (ch + gap)
    d.rectangle([ax, ay, ax + cw, ay + ch], fill=INK, outline=INK, width=2)
    d.text((ax + 12, ay + 10), "ALSO TODAY", font=font(SANS_B, 16), fill=(255, 214, 90))
    items = [
        "US: O'Hare ground stop amid the Thanksgiving travel rush.",
        "GAZA: Oxfam warns of toxic contamination across the Strip.",
        "US: Rep. Jimmy Gomez resigns after an ethics report.",
    ]
    yy = ay + 40
    for it in items:
        for line in wrap(d, "•  " + it, font(SANS, 14), cw - 24):
            d.text((ax + 12, yy), line, font=font(SANS, 14),
                   fill=(246, 241, 231))
            yy += 18
        yy += 6

    # ---- footer ----
    d.line([(28, 884), (996, 884)], fill=INK, width=2)
    center_text(d, 896, "Stories as first reported on Tuesday 24 November 2026.",
                font(SANS, 15), GREY)
    center_text(d, 920, "Sources: BBC · Reuters · Associated Press · Times of India",
                font(SANS, 14), GREY)
    center_text(d, 952, "Drawn from shapes — no photographs.  THE WORLD IN ONE DAY",
                font(SERIF, 17), INK)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
