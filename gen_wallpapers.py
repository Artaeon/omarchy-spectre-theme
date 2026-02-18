#!/usr/bin/env python3
"""Generate dark Matrix-themed wallpapers for omarchy spectre theme."""

import random
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 3840, 2160
BG = (10, 10, 10)

MATRIX_CHARS = list("アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン")
HEX = "0123456789ABCDEF"


def blend(bg, fg, alpha):
    return tuple(int(bg[i] * (1 - alpha) + fg[i] * alpha) for i in range(3))


def get_font(size):
    paths = [
        "/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Bold.ttf",
        "/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Regular.ttf",
        "/usr/share/fonts/TTF/JetBrainsMono-Bold.ttf",
        "/usr/share/fonts/noto/NotoSansMono-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSansMono-Bold.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def wallpaper_matrix_rain():
    """Bright neon green Matrix digital rain on deep black."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    font_lg = get_font(30)
    font_md = get_font(24)
    font_sm = get_font(18)

    random.seed(42)
    col_width = 34
    char_height = 36
    cols = W // col_width + 1

    # Layer 1: Background scatter (ghostly glow)
    for _ in range(5000):
        x = random.randint(0, W)
        y = random.randint(0, H)
        char = random.choice(MATRIX_CHARS)
        a = random.uniform(0.04, 0.10)
        draw.text((x, y), char, fill=blend(BG, (0, 255, 65), a), font=font_sm)

    # Layer 2: Main dense rain streams
    for col in range(cols):
        x = col * col_width
        num_streams = random.randint(1, 2)

        for _ in range(num_streams):
            stream_len = random.randint(15, 50)
            start_y = random.randint(-800, H)

            for i in range(stream_len):
                y = start_y + i * char_height
                if y < -40 or y > H + 40:
                    continue

                char = random.choice(MATRIX_CHARS)
                t = i / stream_len

                if i == 0:
                    # Head of stream: brightest white-green
                    color = blend(BG, (180, 255, 200), 0.95)
                    f = font_lg
                elif i == 1:
                    color = blend(BG, (100, 255, 130), 0.85)
                    f = font_lg
                elif t < 0.15:
                    color = blend(BG, (0, 255, 65), 0.80)
                    f = font_lg
                elif t < 0.35:
                    fade = (t - 0.15) / 0.2
                    color = blend(BG, (0, 220, 55), 0.70 - 0.15 * fade)
                    f = font_md
                elif t < 0.6:
                    fade = (t - 0.35) / 0.25
                    color = blend(BG, (0, 180, 40), 0.50 - 0.15 * fade)
                    f = font_md
                elif t < 0.85:
                    fade = (t - 0.6) / 0.25
                    color = blend(BG, (0, 130, 30), 0.30 - 0.10 * fade)
                    f = font_sm
                else:
                    fade = (t - 0.85) / 0.15
                    color = blend(BG, (0, 80, 20), 0.15 - 0.06 * fade)
                    f = font_sm

                draw.text((x, y), char, fill=color, font=f)

    # Layer 3: Mid-ground streams (offset)
    random.seed(88)
    for col in range(0, cols, 2):
        x = col * col_width + 17
        stream_len = random.randint(10, 30)
        start_y = random.randint(-200, H)

        for i in range(stream_len):
            y = start_y + i * 30
            if y < -30 or y > H + 30:
                continue
            char = random.choice(MATRIX_CHARS)
            t = i / stream_len
            alpha = 0.55 * (1 - t * 0.8)
            draw.text((x, y), char, fill=blend(BG, (0, 200, 50), alpha), font=font_md)

    img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
    img.save("backgrounds/1-matrix-rain.png", "PNG", optimize=True)
    print("Saved backgrounds/1-matrix-rain.png")


def wallpaper_circuit():
    """Dense circuit board with neon green traces on dark background."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    random.seed(77)

    bright = (0, 255, 65)
    med = (0, 200, 50)
    dark = (0, 150, 35)

    # Grid of thick horizontal traces
    for _ in range(120):
        y = random.randint(0, H)
        x1 = random.randint(0, W)
        length = random.randint(200, 1200)
        w = random.choice([1, 2, 2, 3])
        a = random.uniform(0.15, 0.45)
        draw.line([(x1, y), (x1 + length, y)], fill=blend(BG, dark, a), width=w)

    # Grid of thick vertical traces
    for _ in range(120):
        x = random.randint(0, W)
        y1 = random.randint(0, H)
        length = random.randint(200, 900)
        w = random.choice([1, 2, 2, 3])
        a = random.uniform(0.15, 0.45)
        draw.line([(x, y1), (x, y1 + length)], fill=blend(BG, dark, a), width=w)

    # Connection nodes
    nodes = [(random.randint(0, W), random.randint(0, H)) for _ in range(400)]

    for i, (x1, y1) in enumerate(nodes):
        nearest = sorted(
            range(len(nodes)),
            key=lambda j: math.hypot(nodes[j][0] - x1, nodes[j][1] - y1)
        )[1:random.randint(2, 5)]

        for j in nearest:
            x2, y2 = nodes[j]
            dist = math.hypot(x2 - x1, y2 - y1)
            if dist > 350:
                continue
            a = 0.20 + 0.25 * (1 - dist / 350)
            color = blend(BG, dark, a)
            w = 2 if a > 0.30 else 1
            mid_x = x1 if random.random() < 0.5 else x2
            draw.line([(x1, y1), (mid_x, y2), (x2, y2)], fill=color, width=w)

    # Large node dots — glowing green
    for x, y in nodes:
        size = random.randint(4, 10)
        a = random.uniform(0.40, 0.85)
        draw.ellipse([x - size, y - size, x + size, y + size], fill=blend(BG, med, a))
        # Inner bright dot
        if size > 5:
            draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=blend(BG, bright, a * 0.9))

    # IC chips - larger
    for _ in range(70):
        x = random.randint(50, W - 100)
        y = random.randint(50, H - 60)
        w = random.randint(25, 65)
        h = random.randint(18, 40)
        a = random.uniform(0.20, 0.45)
        color = blend(BG, dark, a)
        draw.rectangle([x, y, x + w, y + h], outline=color, width=2)
        fill_a = a * 0.10
        draw.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=blend(BG, med, fill_a))
        pin_color = blend(BG, dark, a * 0.7)
        for px in range(x + 5, x + w - 3, 8):
            draw.line([(px, y - 6), (px, y)], fill=pin_color, width=2)
            draw.line([(px, y + h), (px, y + h + 6)], fill=pin_color, width=2)

    # Target rings — glowing
    for _ in range(20):
        cx = random.randint(100, W - 100)
        cy = random.randint(100, H - 100)
        max_r = random.randint(50, 140)
        for r in range(12, max_r, 18):
            a = 0.18 * (1 - r / max_r)
            if a > 0.03:
                draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                             outline=blend(BG, med, a), width=2)
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=blend(BG, bright, 0.5))

    img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
    img.save("backgrounds/2-circuit.png", "PNG", optimize=True)
    print("Saved backgrounds/2-circuit.png")


def wallpaper_hexdump():
    """Full-screen hex dump with neon green text on black like a forensic tool."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    font = get_font(26)
    font_sm = get_font(22)

    random.seed(55)
    line_h = 32
    cw = 15
    rows = H // line_h + 1
    margin = 20
    bytes_per_line = 56

    addr_end = margin + 10 * cw
    hex_start = addr_end + cw
    hex_end = hex_start + bytes_per_line * 3 * cw
    ascii_start = hex_end + 2 * cw

    # Separator lines
    sep = blend(BG, (0, 255, 65), 0.12)
    draw.line([(addr_end, 0), (addr_end, H)], fill=sep, width=1)
    draw.line([(ascii_start - cw, 0), (ascii_start - cw, H)], fill=sep, width=1)

    # Header
    hdr_color = blend(BG, (0, 255, 65), 0.55)
    draw.text((margin, 4), "OFFSET", fill=hdr_color, font=font_sm)
    hdr_bytes = " ".join(f"{i:02X}" for i in range(min(bytes_per_line, 32)))
    draw.text((hex_start, 4), hdr_bytes + " ...", fill=blend(BG, (0, 255, 65), 0.35), font=font_sm)
    draw.text((ascii_start, 4), "DECODED ASCII", fill=hdr_color, font=font_sm)
    draw.line([(margin, 32), (W - margin, 32)], fill=blend(BG, (0, 255, 65), 0.25), width=2)

    hot_zones = [
        (0.08, 0.22, 0.85),
        (0.30, 0.48, 1.0),
        (0.55, 0.68, 0.75),
        (0.75, 0.93, 0.90),
    ]

    for row in range(1, rows):
        y = row * line_h + 8
        row_pos = row / rows

        intensity = 0.15
        for z_start, z_end, z_peak in hot_zones:
            if z_start <= row_pos <= z_end:
                mid = (z_start + z_end) / 2
                dist = abs(row_pos - mid) / ((z_end - z_start) / 2)
                intensity = max(intensity, z_peak * (1 - dist ** 2))

        base_alpha = 0.06 + 0.55 * intensity

        # Address
        addr = row * bytes_per_line
        draw.text((margin, y), f"{addr:08X}", fill=blend(BG, (0, 200, 50), base_alpha * 0.70), font=font)

        # Hex bytes
        for col in range(bytes_per_line):
            bx = hex_start + col * 3 * cw
            if col % 8 == 0 and col > 0:
                bx += cw

            b = f"{random.randint(0,255):02X}"
            v = random.uniform(0.5, 1.5)
            a = max(0.04, min(0.85, base_alpha * v))

            if random.random() < 0.05 and intensity > 0.4:
                a = min(0.95, a * 2.2)
                fg = (0, 255, 65)
            elif random.random() < 0.03:
                a = min(0.85, a * 1.8)
                fg = (100, 255, 130)
            else:
                fg = (0, 220, 55)

            draw.text((bx, y), b, fill=blend(BG, fg, a), font=font)

        # ASCII column
        for col in range(bytes_per_line):
            ax = ascii_start + col * cw
            if ax > W - margin:
                break
            char = chr(random.randint(33, 126)) if random.random() > 0.3 else random.choice("._-:;|")
            draw.text((ax, y), char, fill=blend(BG, (0, 200, 50), base_alpha * 0.50), font=font_sm)

    # Hot zone glow bars
    for z_start, z_end, _ in hot_zones:
        mid_y = int(((z_start + z_end) / 2) * H)
        for dy in range(-6, 7):
            la = 0.06 * (1 - abs(dy) / 7)
            draw.line([(0, mid_y + dy), (W, mid_y + dy)], fill=blend(BG, (0, 255, 65), la))

    img = img.filter(ImageFilter.GaussianBlur(radius=0.2))
    img.save("backgrounds/3-hexdump.png", "PNG", optimize=True)
    print("Saved backgrounds/3-hexdump.png")


if __name__ == "__main__":
    wallpaper_matrix_rain()
    wallpaper_circuit()
    wallpaper_hexdump()
    print("Done!")
