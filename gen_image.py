#!/usr/bin/env python3
"""Renders entry.png: a front page summing up the world news of 18 November 2026.

Six stories, one per tile, each with a drawn pictogram, a short headline and a
one-line detail, under a masthead that names the day. Rendered with Pillow at
1024x1024 (the gate's limit) so it stays legible when scaled down.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (12, 18, 33)
CARD = (247, 246, 242)
INK = (18, 22, 32)
MUTED = (86, 94, 110)
ACCENT = (198, 40, 40)
BLUE = (28, 78, 156)
GOLD = (214, 158, 46)
TEAL = (18, 116, 118)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
d.text((36, 30), "THE WORLD", font=font(62), fill=(255, 255, 255))
d.text((36, 104), "WEDNESDAY 18 NOVEMBER 2026", font=font(34), fill=GOLD)
d.text((36, 146), "one day's news, six stories", font=font(22, False), fill=(150, 160, 180))
d.line((36, 182, W - 36, 182), fill=(60, 70, 95), width=3)

# ---------------------------------------------------------------- tiles
M = 30
GAP = 14
TOP = 196
COLS, ROWS = 2, 3
cw = (W - 2 * M - GAP * (COLS - 1)) // COLS
ch = (H - TOP - M - GAP * (ROWS - 1)) // ROWS


def tile(i):
    r, c = divmod(i, COLS)
    x = M + c * (cw + GAP)
    y = TOP + r * (ch + GAP)
    return x, y


CATS = ["WORLD", "EUROPE", "HEALTH", "CYBER", "BUSINESS", "ASIA"]
CATCOLORS = [ACCENT, BLUE, (146, 43, 33), (90, 60, 140), (22, 130, 70), GOLD]


def card(i):
    x, y = tile(i)
    d.rounded_rectangle((x, y, x + cw, y + ch), radius=14, fill=CARD)
    cc = CATCOLORS[i]
    d.rounded_rectangle((x, y, x + 10, y + ch), radius=5, fill=cc)
    # category chip
    chf = font(15)
    tw = d.textlength(CATS[i], font=chf)
    d.rounded_rectangle((x + 26, y + 16, x + 26 + tw + 20, y + 42), radius=11, fill=cc)
    d.text((x + 36, y + 20), CATS[i], font=chf, fill=(255, 255, 255))
    return x, y


def text_block(x, y, headline, detail, hcolor=INK):
    tx = x + 132
    maxw = cw - 132 - 18
    fh = font(30)
    hl = wrap(d, headline, fh, maxw)[:3]
    fd = font(19, False)
    dl = wrap(d, detail, fd, maxw)[:5]
    total = len(hl) * 33 + 6 + len(dl) * 24
    cy = y + 20 + max(0, (ch - 60 - total) // 2)
    for ln in hl:
        d.text((tx, cy), ln, font=fh, fill=hcolor)
        cy += 33
    cy += 6
    for ln in dl:
        d.text((tx, cy), ln, font=fd, fill=MUTED)
        cy += 24


def star(cx, cy, r, fill):
    import math
    pts = []
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.45
        a = -math.pi / 2 + k * math.pi / 5
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)


# 1. Middle East: US strikes Iran / Hormuz
x, y = card(0)
ix, iy = x + 66, y + ch // 2
# missile
d.polygon([(ix - 34, iy - 34), (ix + 26, iy - 10), (ix + 26, iy + 10), (ix - 34, iy + 34)], fill=ACCENT)
d.polygon([(ix + 26, iy - 10), (ix + 46, iy), (ix + 26, iy + 10)], fill=ACCENT)
d.line((ix - 44, iy - 20, ix - 30, iy - 20), fill=ACCENT, width=5)
d.line((ix - 44, iy + 20, ix - 30, iy + 20), fill=ACCENT, width=5)
# explosion burst
for a in range(0, 360, 45):
    import math
    r = math.radians(a)
    d.line((ix + 30 + 12 * math.cos(r), iy + 40 + 12 * math.sin(r),
            ix + 30 + 22 * math.cos(r), iy + 40 + 22 * math.sin(r)), fill=GOLD, width=4)
# water line
d.line((x + 18, y + ch - 26, x + 116, y + ch - 26), fill=BLUE, width=5)
text_block(x, y, "US jets bomb Iran's Qeshm; Gulf tankers hit mines",
           "Third Iranian drone attack on Bahrain in five days; two tankers burn in the Strait of Hormuz")

# 2. Europe: Crimean Bridge
x, y = card(1)
ix, iy = x + 66, y + ch // 2 - 6
# bridge deck with a collapse
d.line((ix - 50, iy - 18, ix - 14, iy - 18), fill=INK, width=9)
d.line((ix + 16, iy - 18, ix + 50, iy - 18), fill=INK, width=9)
d.line((ix - 50, iy - 18, ix - 50, iy + 26), fill=INK, width=7)
d.line((ix + 50, iy - 18, ix + 50, iy + 26), fill=INK, width=7)
# falling span
d.line((ix - 12, iy - 12, ix + 2, iy + 18), fill=ACCENT, width=9)
d.line((ix + 9, iy - 4, ix + 20, iy + 24), fill=ACCENT, width=9)
# water
for k in range(3):
    d.arc((ix - 52 + k * 36, iy + 30, ix - 24 + k * 36, iy + 44), 200, 340, fill=BLUE, width=4)
text_block(x, y, "Crimean Bridge span collapses",
           "Zelensky says a seven-phase operation; US warns Kyiv's deep strikes harden Moscow")

# 3. Health: measles
x, y = card(2)
ix, iy = x + 66, y + ch // 2 - 4
d.ellipse((ix - 30, iy - 30, ix + 30, iy + 30), fill=ACCENT)
import math
for a in range(0, 360, 30):
    r = math.radians(a)
    d.line((ix + 30 * math.cos(r), iy + 30 * math.sin(r),
            ix + 44 * math.cos(r), iy + 44 * math.sin(r)), fill=ACCENT, width=6)
d.ellipse((ix - 16, iy - 14, ix - 2, iy), fill=(255, 255, 255))
d.ellipse((ix + 4, iy + 6, ix + 18, iy + 20), fill=(255, 255, 255))
d.text((ix - 34, iy + 44), "26 yrs", font=font(16), fill=INK)
text_block(x, y, "US loses measles-free status",
           "World's worst outbreak since 1991 ends 26 years of elimination, health agencies say")

# 4. Cyber: 200 sites hacked
x, y = card(3)
ix, iy = x + 66, y + ch // 2 - 4
# laptop
d.rounded_rectangle((ix - 44, iy - 30, ix + 44, iy + 16), radius=5, fill=INK)
d.rounded_rectangle((ix - 34, iy - 22, ix + 34, iy + 8), radius=3, fill=(240, 240, 235))
d.polygon([(ix - 56, iy + 16), (ix + 56, iy + 16), (ix + 46, iy + 30), (ix - 46, iy + 30)], fill=INK)
# warning triangle on screen
d.polygon([(ix, iy - 16), (ix + 14, iy + 4), (ix - 14, iy + 4)], fill=ACCENT)
d.text((ix - 3, iy - 12), "!", font=font(15), fill=(255, 255, 255))
text_block(x, y, "Hackers hit 200 big websites",
           "Malicious code slipped in via Optimizely hits BBC, IKEA, Air France and HSBC UAE")

# 5. Business: Nvidia
x, y = card(4)
ix, iy = x + 66, y + ch // 2 - 4
# chip
d.rounded_rectangle((ix - 30, iy - 30, ix + 30, iy + 30), radius=6, fill=TEAL)
d.rectangle((ix - 16, iy - 16, ix + 16, iy + 16), fill=(240, 250, 245))
for k in range(4):
    o = -21 + k * 14
    d.line((ix - 44, iy + o, ix - 30, iy + o), fill=TEAL, width=4)
    d.line((ix + 30, iy + o, ix + 44, iy + o), fill=TEAL, width=4)
# arrow up
d.line((ix + 2, iy + 12, ix + 22, iy - 22), fill=(22, 130, 70), width=7)
d.polygon([(ix + 22, iy - 30), (ix + 28, iy - 12), (ix + 10, iy - 18)], fill=(22, 130, 70))
text_block(x, y, "Nvidia sales double, Huang out",
           "Quarterly revenue $115.8bn, up 103%; board will not reinstate founder as CEO")

# 6. Asia: ASEAN / Quad in Manila
x, y = card(5)
ix, iy = x + 66, y + ch // 2 - 4
# ring of flags
cols = [ACCENT, (255, 255, 255), BLUE, GOLD, TEAL, (120, 60, 160)]
for k in range(6):
    a = math.radians(-90 + k * 60)
    cx = ix + 34 * math.cos(a)
    cy = iy + 34 * math.sin(a)
    d.rectangle((cx - 13, cy - 9, cx + 13, cy + 9), fill=cols[k], outline=INK, width=2)
d.ellipse((ix - 12, iy - 12, ix + 12, iy + 12), fill=BLUE, outline=INK, width=3)
d.arc((ix - 16, iy - 16, ix + 16, iy + 16), 0, 360, fill=INK, width=2)
text_block(x, y, "ASEAN summit closes in Manila",
           "Quad leaders Trump, Modi, Albanese and Takaichi meet; chair passes to Singapore")

img.save("/home/agentuser/makefun/entries/news18/entry.png", optimize=True)
print("bytes", __import__("os").path.getsize("/home/agentuser/makefun/entries/news18/entry.png"))
