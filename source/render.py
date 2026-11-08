#!/usr/bin/env python3
"""Render the static 4tRitch profile artwork from bundled fonts and local art."""
from pathlib import Path
import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ART = ROOT / "source" / "art"
FONTS_DIR = ROOT / "source" / "fonts"
ASSETS.mkdir(parents=True, exist_ok=True)
S = 2
W = 746
FONT_FILES = {
    "mono": FONTS_DIR / "NotoSansMono-Regular.ttf",
    "bold": FONTS_DIR / "NotoSansMono-Bold.ttf",
    "serif": FONTS_DIR / "NotoSerif-Italic.ttf",
    "serifbold": FONTS_DIR / "NotoSerif-BoldItalic.ttf",
    "jp": FONTS_DIR / "NotoSansCJK-Regular-subset.ttf",
}
BG = (13, 12, 21)
INK = (18, 16, 28)
ASH = (222, 216, 228)
SILVER = (174, 165, 185)
LAV = (190, 165, 210)

_font_cache = {}
def font(size, kind="mono"):
    key = (kind, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(str(FONT_FILES[kind]), int(size * S))
    return _font_cache[key]

def xy(values):
    return tuple(int(value * S) for value in values)

class Panel:
    def __init__(self, width, height, seed=2):
        self.width, self.height = width, height
        rw, rh = width * S, height * S
        rng = np.random.default_rng(seed)
        x = np.linspace(0, 1, rw, dtype=np.float32)[None, :, None]
        y = np.linspace(0, 1, rh, dtype=np.float32)[:, None, None]
        base = np.array([18, 17, 27], dtype=np.float32)[None, None, :]
        grad = 7 * (1 - x) + 4 * np.sin(2 * np.pi * x) * np.sin(np.pi * y)
        grain = rng.normal(0, 2.5, (rh, rw, 1)).astype(np.float32)
        rgb = np.clip(base + grad * np.array([.4, .3, .65])[None, None, :] + grain, 0, 255).astype(np.uint8)
        self.im = Image.fromarray(rgb, "RGB").convert("RGBA")
        self.d = ImageDraw.Draw(self.im, "RGBA")
        for yy in range(3, rh, 8):
            self.d.line((0, yy, rw, yy), fill=(6, 5, 15, 26), width=1)
        random.seed(seed)
        for _ in range(max(3, width // 90)):
            xx, yy = random.randint(0, rw), random.randint(0, rh)
            self.d.line((xx, yy, xx + random.randint(8, 45) * S, yy), fill=(206, 190, 222, random.randint(8, 20)), width=1)

    def line(self, coords, color=SILVER, width=1):
        if len(color) == 4 and color[3] < 255:
            overlay = Image.new("RGBA", self.im.size, (0, 0, 0, 0))
            ImageDraw.Draw(overlay, "RGBA").line(xy(coords), fill=color, width=max(1, int(width * S)))
            self.im = Image.alpha_composite(self.im, overlay)
            self.d = ImageDraw.Draw(self.im, "RGBA")
        else:
            self.d.line(xy(coords), fill=color, width=max(1, int(width * S)))

    def rect(self, coords, fill=None, outline=None, width=1):
        if fill and len(fill) == 4 and fill[3] < 255:
            overlay = Image.new("RGBA", self.im.size, (0, 0, 0, 0))
            ImageDraw.Draw(overlay, "RGBA").rectangle(xy(coords), fill=fill)
            self.im = Image.alpha_composite(self.im, overlay)
            self.d = ImageDraw.Draw(self.im, "RGBA")
            if outline:
                self.d.rectangle(xy(coords), outline=outline, width=max(1, int(width * S)))
        else:
            self.d.rectangle(xy(coords), fill=fill, outline=outline, width=max(1, int(width * S)))

    def ellipse(self, coords, outline=None, fill=None, width=1):
        translucent = any(color and len(color) == 4 and color[3] < 255 for color in (outline, fill))
        if translucent:
            overlay = Image.new("RGBA", self.im.size, (0, 0, 0, 0))
            ImageDraw.Draw(overlay, "RGBA").ellipse(xy(coords), outline=outline, fill=fill, width=max(1, int(width * S)))
            self.im = Image.alpha_composite(self.im, overlay)
            self.d = ImageDraw.Draw(self.im, "RGBA")
        else:
            self.d.ellipse(xy(coords), outline=outline, fill=fill, width=max(1, int(width * S)))

    def polygon(self, points, fill, outline=None, width=1):
        pts = [xy(point) for point in points]
        if len(fill) == 4 and fill[3] < 255:
            overlay = Image.new("RGBA", self.im.size, (0, 0, 0, 0))
            ImageDraw.Draw(overlay, "RGBA").polygon(pts, fill=fill)
            self.im = Image.alpha_composite(self.im, overlay)
            self.d = ImageDraw.Draw(self.im, "RGBA")
        else:
            self.d.polygon(pts, fill=fill)
        if outline:
            self.d.line(pts + [pts[0]], fill=outline, width=max(1, int(width * S)))

    def text(self, x, y, value, size=12, color=ASH, kind="mono", anchor="lt"):
        rgba = color if len(color) == 4 else (*color, 255)
        self.d.text(xy((x, y)), value, font=font(size, kind), fill=rgba, anchor=anchor)

    def frame(self, x0, y0, x1, y1, bevel=True):
        chamfer = min(6, max(2, (y1 - y0) / 4))
        shape = [(x0 + chamfer, y0), (x1 - chamfer, y0), (x1, y0 + chamfer),
                 (x1, y1 - chamfer), (x1 - chamfer, y1), (x0 + chamfer, y1),
                 (x0, y1 - chamfer), (x0, y0 + chamfer)]
        self.polygon(shape, (16, 14, 24, 228), (133, 124, 147, 255), 1)
        inset = 2
        inner = [(x0 + chamfer + inset, y0 + inset), (x1 - chamfer - inset, y0 + inset),
                 (x1 - inset, y0 + chamfer + inset), (x1 - inset, y1 - chamfer - inset),
                 (x1 - chamfer - inset, y1 - inset), (x0 + chamfer + inset, y1 - inset),
                 (x0 + inset, y1 - chamfer - inset), (x0 + inset, y0 + chamfer + inset)]
        points = [xy(point) for point in inner]
        self.d.line(points + [points[0]], fill=(81, 74, 96, 255), width=S)
        self.line((x0 + chamfer + 3, y0 + 1, x1 - chamfer - 3, y0 + 1), (218, 209, 226, 175))
        self.line((x0 + 1, y0 + chamfer + 2, x0 + 1, y1 - chamfer - 2), (170, 160, 183, 150))
        self.line((x0 + chamfer + 3, y1 - 1, x1 - chamfer - 3, y1 - 1), (49, 43, 61, 255))
        for sx, sy in ((x0 + 5, y0 + 5), (x1 - 5, y0 + 5), (x0 + 5, y1 - 5), (x1 - 5, y1 - 5)):
            self.ellipse((sx - 1.3, sy - 1.3, sx + 1.3, sy + 1.3), outline=(142, 131, 154, 255), fill=(39, 35, 49, 255))

    def metal_bar(self, x, y, width, height, seed=7, colors=None):
        """Composite a textured metallic gradient rather than a flat header block."""
        rw, rh = width * S, height * S
        rng = np.random.default_rng(seed)
        gradient = np.linspace(0, 1, rh, dtype=np.float32)[:, None, None]
        top_color, bottom_color = colors or ((79, 69, 91), (39, 34, 50))
        top = np.array(top_color, dtype=np.float32)[None, None, :]
        bottom = np.array(bottom_color, dtype=np.float32)[None, None, :]
        grain = rng.normal(0, 2.0, (rh, rw, 1)).astype(np.float32)
        pixels = np.clip(top * (1 - gradient) + bottom * gradient + grain, 0, 255).astype(np.uint8)
        layer = Image.fromarray(pixels, "RGB").convert("RGBA")
        self.im.alpha_composite(layer, xy((x, y)))
        self.d = ImageDraw.Draw(self.im, "RGBA")
        self.line((x + 1, y + 1, x + width - 1, y + 1), (219, 209, 229, 145))
        self.line((x + 1, y + height - 1, x + width - 1, y + height - 1), (23, 21, 32, 230))

    def scanlines(self, x, y, width, height, step=3):
        overlay = Image.new("RGBA", self.im.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay, "RGBA")
        for yy in range(y + 1, y + height, step):
            draw.line(xy((x, yy, x + width, yy)), fill=(172, 157, 187, 10), width=1)
        self.im = Image.alpha_composite(self.im, overlay)
        self.d = ImageDraw.Draw(self.im, "RGBA")

    def panel_title(self, x, y, width, title, size=11):
        self.metal_bar(x + 1, y + 1, width - 2, 18, seed=len(title))
        self.rect((x + 7, y + 6, x + 11, y + 10), LAV)
        self.text(x + 15, y + 4, title, size, ASH, "jp" if any(ord(c) > 127 for c in title) else "bold")

    def artwork(self, filename, x, y, width, height, fade_left=False):
        im = Image.open(ART / filename).convert("RGBA")
        scale = max(width * S / im.width, height * S / im.height)
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.Resampling.LANCZOS)
        ox, oy = (im.width - width * S) // 2, (im.height - height * S) // 2
        im = im.crop((ox, oy, ox + width * S, oy + height * S))
        lum = ImageEnhance.Contrast(im.convert("L")).enhance(1.08)
        tinted = Image.merge("RGB", (lum.point(lambda c: int(c * .72)), lum.point(lambda c: int(c * .67)), lum.point(lambda c: min(255, int(c * .86))))).convert("RGBA")
        alpha = np.full((height * S, width * S), 222, dtype=np.uint8)
        if fade_left:
            alpha = (alpha * np.linspace(0, 1, width * S)[None, :]).astype(np.uint8)
        tinted.putalpha(Image.fromarray(alpha, "L"))
        self.im.alpha_composite(tinted, xy((x, y)))
        self.d = ImageDraw.Draw(self.im, "RGBA")

    def save(self, name):
        image = self.im.convert("RGB")
        image.save(ASSETS / name, optimize=True)
        return image

def technology_mark(panel, name, x, y):
    """Draw compact single-color marks; no placeholder abbreviation tiles."""
    c = (214, 205, 224, 255)
    if name == "RUST":
        panel.ellipse((x + 8, y + 2, x + 26, y + 20), outline=c, width=1)
        panel.ellipse((x + 13, y + 7, x + 21, y + 15), outline=c, width=1)
        for angle in range(0, 360, 45):
            a = math.radians(angle)
            panel.line((x + 17 + 8 * math.cos(a), y + 11 + 8 * math.sin(a), x + 17 + 10 * math.cos(a), y + 11 + 10 * math.sin(a)), c)
        panel.text(x + 14, y + 6, "R", 8, c, "bold")
    elif name == "C#":
        panel.text(x + 8, y + 2, "C#", 14, c, "bold")
    elif name == "TS":
        panel.rect((x + 8, y + 1, x + 28, y + 21), c)
        panel.text(x + 12, y + 8, "TS", 8, INK, "bold")
    elif name == "SVELTE":
        panel.polygon([(x+15,y+1),(x+23,y+4),(x+25,y+8),(x+22,y+12),(x+25,y+16),(x+22,y+21),(x+15,y+22),(x+9,y+19),(x+8,y+15),(x+12,y+10),(x+11,y+6)], c)
        panel.line((x+13,y+7,x+21,y+6), INK, 2)
        panel.line((x+13,y+16,x+21,y+15), INK, 2)
    elif name == "GO":
        panel.ellipse((x+5,y+5,x+31,y+17), outline=c, width=1)
        panel.text(x+10,y+4,"go",11,c,"bold")
    elif name == "PG":
        # PostgreSQL elephant head, trunk, eye, and two short legs.
        panel.polygon([(x+11,y+5),(x+14,y+2),(x+21,y+2),(x+25,y+6),(x+25,y+11),
                       (x+29,y+12),(x+28,y+16),(x+25,y+18),(x+23,y+16),(x+22,y+21),
                       (x+19,y+21),(x+19,y+17),(x+15,y+17),(x+15,y+21),(x+12,y+21),
                       (x+12,y+16),(x+9,y+14),(x+9,y+10),(x+6,y+9),(x+7,y+6)], c)
        panel.ellipse((x+18,y+6,x+20,y+8), fill=INK)
    elif name == "DOCKER":
        panel.line((x+5,y+16,x+29,y+16),c,2)
        for dx in (7,13,19): panel.rect((x+dx,y+10,x+dx+4,y+14),c)
        panel.rect((x+13,y+5,x+17,y+9),c)
        panel.polygon([(x+5,y+17),(x+29,y+17),(x+25,y+21),(x+10,y+21)], c)
    elif name == "LINUX":
        panel.ellipse((x+11,y+2,x+23,y+19), outline=c, width=1)
        panel.ellipse((x+13,y+6,x+15,y+8), fill=c)
        panel.ellipse((x+19,y+6,x+21,y+8), fill=c)
        panel.polygon([(x+14,y+12),(x+20,y+12),(x+18,y+15)], c)
        panel.ellipse((x+8,y+18,x+26,y+22), outline=c)
    elif name == "GIT":
        panel.line((x+11,y+4,x+23,y+16),c,2)
        panel.line((x+11,y+4,x+11,y+19),c,2)
        for px,py in ((11,4),(23,16),(11,19)): panel.ellipse((x+px-2,y+py-2,x+px+2,y+py+2),fill=c)
    else:
        panel.text(x + 10, y + 2, ">_", 13, c, "bold")

def draw_music_note(panel, x, y, color=ASH):
    panel.line((x + 8, y + 2, x + 8, y + 12), color, 1)
    panel.line((x + 8, y + 2, x + 14, y), color, 1)
    panel.ellipse((x + 2, y + 10, x + 8, y + 14), fill=color)
    panel.ellipse((x + 8, y + 8, x + 14, y + 12), fill=color)

def draw_transport_icon(panel, action, cx, cy, color):
    if action in ("previous", "next"):
        direction = -1 if action == "previous" else 1
        for offset in (-4, 2):
            tip = cx + direction * (offset + 3)
            base = cx + direction * offset
            panel.polygon([(base,cy-5),(base,cy+5),(tip,cy)], color)
        edge = cx - 7 if direction < 0 else cx + 6
        panel.line((edge, cy - 6, edge, cy + 6), color)
    elif action == "stop":
        panel.rect((cx - 5, cy - 5, cx + 5, cy + 5), color)
    elif action == "play":
        panel.polygon([(cx - 4,cy - 6),(cx - 4,cy + 6),(cx + 6,cy)], color)
    elif action == "pause":
        panel.rect((cx - 5, cy - 6, cx - 1, cy + 6), color)
        panel.rect((cx + 2, cy - 6, cx + 6, cy + 6), color)
    else:
        panel.text(cx - 4, cy - 7, "R", 8, color, "bold")

def render():
    # 746:529 source canvas: compact reference proportions, rendered at 2x.
    parts = []

    p = Panel(W, 112, 11)
    p.artwork("skyline.png", 0, 0, 610, 112)
    p.artwork("portrait.png", 500, 0, 246, 112, fade_left=True)
    p.rect((0, 0, W, 112), (13, 11, 23, 75))
    p.scanlines(0, 0, W, 112, step=3)
    for sx, sy in ((21, 22), (42, 22), (17, 43), (38, 43)):
        p.polygon([(sx, sy + 14), (sx + 10, sy), (sx + 23, sy), (sx + 13, sy + 14)], (153, 128, 183, 235))
    p.text(60, 18, "4tRitch", 39, (224, 215, 232), "serifbold")
    p.line((67, 66, 310, 66), (180, 160, 195, 230), 1)
    p.text(73, 72, "S O F T W A R E   D E V E L O P E R", 8, (215, 205, 222))
    p.text(73, 91, "SYSTEM / 00-A   •   PERSONAL ARCHIVE", 6, (179, 163, 193))
    p.text(580, 5, "システムメニュー", 9, ASH, "jp")
    p.line((578, 21, 738, 21), (174, 159, 190, 180))
    for i, label in enumerate(("PROFILE", "PROJECTS", "TECH STACK", "STATUS")):
        yy = 27 + i * 19
        if i == 0:
            p.rect((583, yy, 738, yy + 17), (118, 91, 139, 135))
            p.polygon([(588,yy+5),(588,yy+12),(593,yy+8)], ASH)
        p.text(599, yy + 3, label, 8, ASH if i == 0 else SILVER)
    p.line((0, 110, W, 110), (177, 158, 194, 255), 1)
    parts.append(p.save("01-hero.png"))

    p = Panel(W, 108, 21)
    for x0, x1 in ((3, 139), (145, 493), (499, 743)):
        p.frame(x0, 2, x1, 106)
        p.panel_title(x0 + 2, 4, x1 - x0 - 4, "メニュー / MENU" if x0 == 3 else "WHOAMI / 自己紹介" if x0 == 145 else "SYSTEM STATUS", 9)
    for i, label in enumerate(("01  PROFILE", "02  PROJECTS", "03  TECH STACK", "04  CONTACT")):
        yy = 29 + i * 17
        if i == 0: p.rect((13, yy, 129, yy + 15), (118, 96, 147, 155), (162, 142, 180, 255))
        p.text(19, yy + 3, label, 8, (224, 214, 230) if i == 0 else SILVER, "mono")
    p.text(157, 31, "Hi, I'm 4tRitch.", 14, (232, 225, 237), "bold")
    p.text(158, 52, "> Rust / C# / Svelte / Go", 9, (197, 176, 220))
    p.text(158, 68, "> Building anime tools,", 8, (217, 209, 226))
    p.text(169, 82, "creative software & UI.", 8, (217, 209, 226))
    p.text(158, 92, "> Linux, games, retro tech.", 7, (180, 171, 196))
    p.artwork("tower.png", 507, 28, 69, 70)
    p.rect((506, 27, 577, 99), outline=(122, 108, 143, 255))
    for yy, key, value in ((31,"OS","ARCH"),(47,"WM","HYPRLAND"),(63,"SH","FISH"),(79,"ED","NEOVIM")):
        p.text(584, yy, key, 7, (173, 160, 185), "bold")
        p.text(600, yy, "/", 7, (129, 115, 144))
        p.text(610, yy, value, 7, ASH, "bold")
    parts.append(p.save("02-system.png"))

    p = Panel(W, 66, 22)
    p.frame(3, 2, 743, 64)
    p.metal_bar(7, 5, 732, 16, seed=22)
    p.text(14, 8, "技術スタック  /  TECH STACK", 9, (226, 218, 235), "jp")
    p.text(560, 8, "[ SYSTEM COMPONENTS : 10 ]", 7, (180, 163, 198))
    tech = [("RUST","RUST"),("C#","C SHARP"),("TS","TYPESCRIPT"),("SVELTE","SVELTE"),("GO","GOLANG"),("PG","POSTGRES"),("DOCKER","DOCKER"),("LINUX","LINUX"),("GIT","GIT"),("CLI","CLI / TUI")]
    for i, (mark, label) in enumerate(tech):
        x = 12 + i * 72
        if i: p.line((x - 5, 25, x - 5, 61), (130, 116, 150, 150))
        technology_mark(p, mark, x + 13, 23)
        p.text(x + 3, 47, label, 6 if len(label) > 8 else 7, (218, 211, 226))
    parts.append(p.save("03-stack.png"))

    p = Panel(W, 27, 23)
    p.frame(3, 2, 743, 25)
    p.metal_bar(7, 5, 732, 18, seed=23)
    p.text(14, 7, "注目のプロジェクト / FEATURED PROJECTS", 9, (228, 218, 235), "jp")
    for i in range(7):
        x = 533 + i * 25
        p.polygon([(x,15),(x+8,7),(x+17,7),(x+10,15)], (131, 119, 148, 145))
    card_specs = [
        ("05-okaimono.png", "Okaimono", ("Anime collection,", "calendar & friends."), ("RUST", "SVELTE"), "trolley.png", False),
        ("06-webcore.png", "webcore-ui", ("Retro web UI studies,", "2005–2008 aesthetics."), ("HTML", "CSS"), "monitor.png", True),
        ("07-clikity.png", "Clikity", ("ClickUp task creator,", "desktop via Tauri."), ("TAURI", "SVELTE"), "city.png", False),
    ]
    cards = []
    for idx, (filename, title, lines, tags, art, selected) in enumerate(card_specs):
        cp = Panel(242, 85, 34 + len(title))
        cp.frame(2, 2, 240, 83)
        cp.artwork(art, 7, 8, 80, 69)
        cp.line((92, 7, 92, 78), (153, 127, 176, 200), 1)
        cp.text(101, 7, title, 13, (231, 220, 237), "serifbold")
        cp.line((100, 25, 235, 25), (146, 128, 174, 170))
        cp.text(101, 30, lines[0], 7, (220, 213, 228))
        cp.text(101, 42, lines[1], 7, (220, 213, 228))
        for tag_idx, tag in enumerate(tags):
            tx = 101 + tag_idx * 67
            cp.rect((tx, 63, tx + 61, 77), (48, 42, 59, 255), (127, 111, 143, 255))
            cp.text(tx + 5, 66, tag, 6, (221, 209, 231))
        if selected:
            cp.line((4, 2, 238, 2), (190, 145, 212, 255), 2)
            cp.polygon([(89, 36), (89, 48), (95, 42)], (190, 157, 218, 255))
        cards.append(cp.save(filename))
    row = Image.new("RGB", (W * S, 85 * S), BG)
    for x, card in zip((2, 252, 502), cards): row.paste(card, (x * S, 0))
    parts.extend([p.save("04-projects-header.png"), row])

    p = Panel(W, 94, 45)
    p.frame(3, 2, 743, 92)
    p.metal_bar(7, 5, 732, 17, seed=45)
    draw_music_note(p, 12, 7, (229, 216, 234))
    p.text(30, 7, "NOW PLAYING  /  再生中", 9, (229, 216, 234), "jp")
    p.text(583, 8, "AUDIO PLAYER // DEMO", 6, (188, 172, 204))
    p.artwork("album.png", 12, 28, 61, 56)
    p.rect((11, 27, 74, 85), outline=(161, 144, 177, 255))
    p.text(84, 29, "LOST SIGNAL  /  DEMO TRACK", 9, (228, 215, 231), "serifbold")
    p.text(84, 47, "MP3 · 320 KBPS · 44.1 KHZ", 6, (179, 167, 196))
    p.text(84, 60, "STEREO   02:14 / 04:27", 7, (208, 194, 220))
    p.rect((84, 74, 426, 85), (17, 14, 26, 255), (145, 130, 159, 255))
    for i in range(25):
        color = (177, 144, 199, 255) if i < 13 else (61, 55, 72, 255)
        p.rect((89 + i * 13, 77, 98 + i * 13, 82), color)
    rng = random.Random(47)
    for i in range(18):
        height = rng.randint(4, 23)
        xx = 447 + i * 6
        for yy in range(0, height, 4): p.rect((xx, 82 - yy, xx + 3, 85 - yy), (147 + min(45, yy), 123 + min(40, yy), 168 + min(40, yy), 255))
    # The optical disc has a softly shaded metallic face and sits behind six controls.
    p.ellipse((653, 27, 739, 113), fill=(92, 78, 108, 78), outline=(160, 143, 178, 255), width=2)
    p.ellipse((661, 35, 731, 105), outline=(83, 73, 100, 230))
    p.ellipse((674, 48, 718, 92), outline=(152, 136, 169, 200))
    for angle in range(0, 360, 30):
        radians = math.radians(angle)
        p.line((696 + 24 * math.cos(radians), 70 + 24 * math.sin(radians),
                696 + 33 * math.cos(radians), 70 + 33 * math.sin(radians)), (206, 195, 218, 45))
    p.ellipse((686, 60, 706, 80), fill=(32, 27, 41, 255), outline=(193, 174, 204, 255))
    actions = ("previous", "stop", "play", "pause", "next", "repeat")
    for i, action in enumerate(actions):
        x, selected = 512 + i * 35, action == "pause"
        top, bottom = ((140, 111, 157), (69, 55, 84)) if selected else ((105, 99, 114), (46, 42, 55))
        p.metal_bar(x + 1, 52, 30, 29, seed=50 + i, colors=(top, bottom))
        points = [(x + 3,52),(x + 29,52),(x + 31,54),(x + 31,79),(x + 29,81),(x + 3,81),(x + 1,79),(x + 1,54)]
        pts = [xy(point) for point in points]
        p.d.line(pts + [pts[0]], fill=(190, 180, 198, 255), width=S)
        p.line((x + 4, 54, x + 28, 54), (233, 225, 238, 170))
        icon_color = (244, 232, 248, 255) if selected else (216, 207, 224, 255)
        draw_transport_icon(p, action, x + 16, 66, icon_color)
    parts.append(p.save("08-player.png"))

    p = Panel(W, 37, 61)
    p.frame(3, 2, 743, 35)
    p.text(13, 10, "4tRitch@arch:~/dev$", 8, (229, 216, 233))
    p.rect((163, 12, 169, 22), (213, 201, 223, 255))
    p.text(397, 10, "○ PROJECTS   △ LINKS   × EXIT", 7, (194, 179, 211))
    p.text(714, 10, "2026", 6, (175, 162, 195))
    parts.append(p.save("09-footer.png"))

    preview = Image.new("RGB", (W * S, 529 * S), BG)
    top = 0
    for part in parts:
        preview.paste(part, (0, top))
        top += part.height
    if top != preview.height:
        raise ValueError(f"Rendered section total {top // S}px does not match 529px target")
    preview.save(ROOT / "PREVIEW.png", optimize=True)
    print(f"Done: {ROOT / 'PREVIEW.png'} ({W}x529 source pixels, 2x output)")

if __name__ == "__main__":
    render()
