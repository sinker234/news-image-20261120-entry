#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news poster (1024x1024 PNG).

A broadsheet front page, drawn entirely in code with PIL: no photos,
no downloaded assets. Every story was checked against reputable
reporting on the morning of 20 November 2026.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 34
PAPER = (248, 244, 233)
INK = (24, 24, 22)
RED = (163, 22, 33)
MUTED = (92, 84, 70)
HERO_TINT = (238, 230, 209)
RULE = (24, 24, 22)
TICKER_BG = (24, 24, 22)

FDIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FDIR + name, size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
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


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def fit_text(draw, text, fnt_name, size, width, max_lines=3):
    """Shrink font until text wraps to at most max_lines within width."""
    while size > 10:
        fnt = font(fnt_name, size)
        lines = wrap(draw, text, fnt, width)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 2
    fnt = font(fnt_name, size)
    return fnt, wrap(draw, text, fnt, width)


def draw_scales(draw, cx, cy, s, color):
    """Simple scales of justice, centred at (cx, cy), size s."""
    top = cy - s // 2
    base = cy + s // 2
    # pole
    draw.line([(cx, top), (cx, base - 6)], fill=color, width=5)
    # beam
    draw.line([(cx - s // 2, top + 8), (cx + s // 2, top + 8)],
              fill=color, width=5)
    # centre finial
    draw.ellipse([cx - 4, top - 8, cx + 4, top], fill=color)
    # pans
    for side in (-1, 1):
        px = cx + side * (s // 2 - 4)
        draw.line([(px, top + 8), (px, base - 26)], fill=color, width=3)
        draw.line([(px - 16, base - 26), (px + 16, base - 26)],
                  fill=color, width=3)
        draw.polygon([(px - 22, base - 26), (px + 22, base - 26),
                      (px, base - 4)], outline=color, fill=None)
        draw.line([(px - 22, base - 26), (px, base - 4)], fill=color, width=2)
        draw.line([(px + 22, base - 26), (px, base - 4)], fill=color, width=2)
    # base
    draw.line([(cx - 26, base), (cx + 26, base)], fill=color, width=5)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN

    # ---------- Masthead ----------
    y = 26
    title = "THE WORLD IN A DAY"
    tf = font(SERIF_B, 62)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, y), title, font=tf, fill=INK)
    y += 78
    d.line([(x0, y), (x1, y)], fill=RULE, width=3)
    d.line([(x0, y + 5), (x1, y + 5)], fill=RULE, width=1)
    y += 14
    dateline = "F R I D A Y  ·  2 0  N O V E M B E R  2 0 2 6"
    df = font(SANS_B, 24)
    dw = d.textlength(dateline, font=df)
    d.text(((W - dw) / 2, y), dateline, font=df, fill=RED)
    y += 40
    d.line([(x0, y), (x1, y)], fill=RULE, width=1)

    # ---------- Hero: ICJ verdict ----------
    hy = y + 12
    hh = 240
    d.rectangle([x0, hy, x1, hy + hh], fill=HERO_TINT,
                outline=RULE, width=2)
    hx = x0 + 22
    hw = x1 - x0 - 190  # leave room for the scales icon
    ky = hy + 16
    kf = font(SANS_B, 19)
    d.text((hx, ky), "THE HAGUE  ·  THE WORLD COURT", font=kf, fill=RED)
    headline = "MYANMAR GUILTY OF GENOCIDE"
    hf, hlines = fit_text(d, headline, SERIF_B, 52, hw, max_lines=2)
    ly = draw_lines(d, hlines, hx, ky + 30, hf, INK, 56)
    deck = ("The International Court of Justice rules Myanmar committed "
            "genocide against the Rohingya — the first time in the court's "
            "80-year history a state has been held responsible. "
            "9–6; reparations ordered.")
    bf = font(SANS, 19)
    blines = wrap(d, deck, bf, hw)
    draw_lines(d, blines, hx, ly + 6, bf, INK, 25)
    draw_scales(d, x1 - 78, hy + hh // 2 + 6, 110, INK)

    # ---------- Row 2: two panels ----------
    ry = hy + hh + 16
    rh = 196
    col_w = (x1 - x0 - 16) // 2

    def panel(px, py, pw, ph, kicker, title, body, title_size=27):
        d.rectangle([px, py, px + pw, py + ph], outline=RULE, width=2)
        ix = px + 16
        iw = pw - 32
        kf2 = font(SANS_B, 17)
        d.text((ix, py + 12), kicker, font=kf2, fill=RED)
        tf2, tlines = fit_text(d, title, SERIF_B, title_size, iw, max_lines=2)
        ty = draw_lines(d, tlines, ix, py + 38, tf2, INK, title_size + 6)
        bf2 = font(SANS, 17)
        bl = wrap(d, body, bf2, iw)
        draw_lines(d, bl, ix, ty + 4, bf2, INK, 22)

    panel(x0, ry, col_w, rh,
          "SHENZHEN  ·  THE SUMMIT",
          "THREE LEADERS, ONE TABLE",
          "Trump, Xi and Putin hold the first US–China–Russia "
          "summit. A “peace declaration” pledges nuclear-risk "
          "talks — no breakthrough on Ukraine or Iran.")
    panel(x0 + col_w + 16, ry, col_w, rh,
          "INDIA  ·  CYCLONE AKVAN",
          "STORM BEARS DOWN ON ODISHA",
          "Landfall due at noon today near Gopalpur, with "
          "winds gusting to 110 km/h. 300,000 people moved "
          "to safety; a red alert covers the coast.")

    # ---------- Row 3: three panels ----------
    ry2 = ry + rh + 16
    rh2 = 192
    col3 = (x1 - x0 - 32) // 3
    panel(x0, ry2, col3, rh2,
          "WASHINGTON  ·  IRAN",
          "NO IRAN CALL UNTIL 2027",
          "Trump says he is “not rushing” on new strikes, "
          "despite Netanyahu pressing for another offensive.",
          title_size=24)
    panel(x0 + col3 + 16, ry2, col3, rh2,
          "ANTALYA  ·  COP31",
          "FOSSIL FUELS VANISH FROM DRAFT",
          "The new climate text is cut from 144 points to 80 "
          "and drops every mention of fossil fuels. Talks "
          "close Friday.",
          title_size=24)
    panel(x0 + 2 * (col3 + 16), ry2, col3, rh2,
          "SPACE  ·  VOYAGER 1",
          "A LIGHT-DAY FROM HOME",
          "NASA confirms the probe is 26 billion km out — "
          "the first craft ever that far. Its signal takes "
          "a full day to reach Earth.",
          title_size=24)

    # ---------- Row 4: Meta strip ----------
    ry3 = ry2 + rh2 + 16
    rh3 = 88
    d.rectangle([x0, ry3, x1, ry3 + rh3], outline=RULE, width=2)
    kf3 = font(SANS_B, 17)
    d.text((x0 + 16, ry3 + 8), "TECH  ·  META", font=kf3, fill=RED)
    mt = "META RETHINKS ITS 2030 NET-ZERO GOAL"
    mf = font(SERIF_B, 23)
    d.text((x0 + 16, ry3 + 32), mt, font=mf, fill=INK)
    mb = "The company says it is “reevaluating” the target as its AI buildout swells energy use."
    mbf = font(SANS, 16)
    d.text((x0 + 16, ry3 + 64), mb, font=mbf, fill=MUTED)

    # ---------- Ticker ----------
    ty0 = ry3 + rh3 + 16
    th = 40
    d.rectangle([x0, ty0, x1, ty0 + th], fill=TICKER_BG)
    tick = ("ALSO:  Fiji declares disaster as El Niño drought bites   ·   "
            "Somalia expels UAE envoy   ·   Gazans return as Israeli "
            "operation ends")
    tf3 = font(SANS_B, 15)
    tw3 = d.textlength(tick, font=tf3)
    # shrink until it fits the strip
    while tw3 > (x1 - x0 - 24) and tf3.size > 11:
        tf3 = font(SANS_B, tf3.size - 1)
        tw3 = d.textlength(tick, font=tf3)
    d.text((x0 + 12, ty0 + (th - tf3.size) // 2 - 2), tick, font=tf3,
           fill=(248, 244, 233))

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
