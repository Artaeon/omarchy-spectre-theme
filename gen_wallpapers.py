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


# ─────────────────────────────────────────────────────────────
# 1. Matrix Rain — classic falling katakana
# ─────────────────────────────────────────────────────────────
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


# ─────────────────────────────────────────────────────────────
# 2. Circuit Board — neon traces and glowing nodes
# ─────────────────────────────────────────────────────────────
def wallpaper_circuit():
    """Dense circuit board with neon green traces on dark background."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    random.seed(77)

    bright = (0, 255, 65)
    med = (0, 200, 50)
    dark = (0, 150, 35)

    for _ in range(120):
        y = random.randint(0, H)
        x1 = random.randint(0, W)
        length = random.randint(200, 1200)
        w = random.choice([1, 2, 2, 3])
        a = random.uniform(0.15, 0.45)
        draw.line([(x1, y), (x1 + length, y)], fill=blend(BG, dark, a), width=w)

    for _ in range(120):
        x = random.randint(0, W)
        y1 = random.randint(0, H)
        length = random.randint(200, 900)
        w = random.choice([1, 2, 2, 3])
        a = random.uniform(0.15, 0.45)
        draw.line([(x, y1), (x, y1 + length)], fill=blend(BG, dark, a), width=w)

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

    for x, y in nodes:
        size = random.randint(4, 10)
        a = random.uniform(0.40, 0.85)
        draw.ellipse([x - size, y - size, x + size, y + size], fill=blend(BG, med, a))
        if size > 5:
            draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=blend(BG, bright, a * 0.9))

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


# ─────────────────────────────────────────────────────────────
# 3. Hex Dump — forensic memory dump
# ─────────────────────────────────────────────────────────────
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

    sep = blend(BG, (0, 255, 65), 0.12)
    draw.line([(addr_end, 0), (addr_end, H)], fill=sep, width=1)
    draw.line([(ascii_start - cw, 0), (ascii_start - cw, H)], fill=sep, width=1)

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

        addr = row * bytes_per_line
        draw.text((margin, y), f"{addr:08X}", fill=blend(BG, (0, 200, 50), base_alpha * 0.70), font=font)

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

        for col in range(bytes_per_line):
            ax = ascii_start + col * cw
            if ax > W - margin:
                break
            char = chr(random.randint(33, 126)) if random.random() > 0.3 else random.choice("._-:;|")
            draw.text((ax, y), char, fill=blend(BG, (0, 200, 50), base_alpha * 0.50), font=font_sm)

    for z_start, z_end, _ in hot_zones:
        mid_y = int(((z_start + z_end) / 2) * H)
        for dy in range(-6, 7):
            la = 0.06 * (1 - abs(dy) / 7)
            draw.line([(0, mid_y + dy), (W, mid_y + dy)], fill=blend(BG, (0, 255, 65), la))

    img = img.filter(ImageFilter.GaussianBlur(radius=0.2))
    img.save("backgrounds/3-hexdump.png", "PNG", optimize=True)
    print("Saved backgrounds/3-hexdump.png")


# ─────────────────────────────────────────────────────────────
# 4. Binary Rain — classic 0s and 1s cascade
# ─────────────────────────────────────────────────────────────
def wallpaper_binary_rain():
    """Cascading binary digits (0s and 1s) in varying sizes and intensities."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    font_lg = get_font(36)
    font_md = get_font(24)
    font_sm = get_font(16)
    font_xs = get_font(12)

    random.seed(101)

    # Layer 1: Tiny background binary noise
    for _ in range(12000):
        x = random.randint(0, W)
        y = random.randint(0, H)
        char = random.choice("01")
        a = random.uniform(0.03, 0.08)
        draw.text((x, y), char, fill=blend(BG, (0, 255, 65), a), font=font_xs)

    # Layer 2: Dense columns of binary
    col_width = 22
    cols = W // col_width + 1
    for col in range(cols):
        x = col * col_width
        num_streams = random.randint(0, 2)

        for _ in range(num_streams):
            stream_len = random.randint(20, 65)
            start_y = random.randint(-600, H)
            speed = random.uniform(0.6, 1.4)

            for i in range(stream_len):
                y = start_y + int(i * 28 * speed)
                if y < -30 or y > H + 30:
                    continue

                char = random.choice("01")
                t = i / stream_len

                if i < 2:
                    # Head: bright white-green
                    color = blend(BG, (200, 255, 220), 0.92 - i * 0.08)
                    f = font_lg
                elif t < 0.2:
                    color = blend(BG, (0, 255, 65), 0.78)
                    f = font_md
                elif t < 0.5:
                    fade = (t - 0.2) / 0.3
                    color = blend(BG, (0, 200, 45), 0.60 - 0.20 * fade)
                    f = font_md
                elif t < 0.8:
                    fade = (t - 0.5) / 0.3
                    color = blend(BG, (0, 150, 35), 0.35 - 0.15 * fade)
                    f = font_sm
                else:
                    fade = (t - 0.8) / 0.2
                    color = blend(BG, (0, 100, 25), 0.15 - 0.07 * fade)
                    f = font_sm

                draw.text((x, y), char, fill=color, font=f)

    # Layer 3: Scattered large binary for depth
    for _ in range(200):
        x = random.randint(0, W)
        y = random.randint(0, H)
        char = random.choice("01")
        a = random.uniform(0.15, 0.40)
        draw.text((x, y), char, fill=blend(BG, (0, 255, 65), a), font=font_lg)

    img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
    img.save("backgrounds/4-binary-rain.png", "PNG", optimize=True)
    print("Saved backgrounds/4-binary-rain.png")


# ─────────────────────────────────────────────────────────────
# 5. Cyber Grid — 3D perspective grid with data points
# ─────────────────────────────────────────────────────────────
def wallpaper_cyber_grid():
    """Retro 3D perspective grid like a cyber landscape with data pulses."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    font_sm = get_font(14)
    random.seed(202)

    cx, cy = W // 2, H // 2 + 200  # vanishing point below center
    green = (0, 255, 65)
    dark_green = (0, 150, 35)

    # Horizon glow
    for dy in range(-300, 300):
        y = cy + dy
        if 0 <= y < H:
            a = 0.08 * (1 - abs(dy) / 300) ** 2
            draw.line([(0, y), (W, y)], fill=blend(BG, green, a), width=1)

    # Perspective horizontal lines (ground plane)
    for i in range(1, 80):
        t = i / 80
        # Exponential spacing for perspective
        y = cy + int((t ** 1.8) * (H - cy + 200))
        if y > H + 50:
            continue
        a = max(0.04, 0.35 * (1 - t * 0.7))
        w = 2 if t < 0.3 else 1
        draw.line([(0, y), (W, y)], fill=blend(BG, dark_green, a), width=w)

    # Perspective vertical lines (receding into vanishing point)
    num_vlines = 50
    for i in range(-num_vlines, num_vlines + 1):
        spread = i / num_vlines
        # Bottom of screen (near)
        bx = cx + int(spread * W * 1.2)
        # At horizon (far)
        tx = cx + int(spread * 60)
        a = max(0.04, 0.30 * (1 - abs(spread) * 0.5))
        w = 2 if abs(spread) < 0.15 else 1
        draw.line([(tx, cy), (bx, H + 50)], fill=blend(BG, dark_green, a), width=w)

    # Sky grid (above horizon) — more subtle
    for i in range(1, 40):
        t = i / 40
        y = cy - int((t ** 1.5) * cy * 0.9)
        if y < -50:
            continue
        a = max(0.02, 0.15 * (1 - t * 0.8))
        draw.line([(0, y), (W, y)], fill=blend(BG, dark_green, a), width=1)

    for i in range(-num_vlines, num_vlines + 1):
        spread = i / num_vlines
        bx = cx + int(spread * W * 0.8)
        tx = cx + int(spread * 40)
        a = max(0.02, 0.12 * (1 - abs(spread) * 0.5))
        draw.line([(tx, cy), (bx, -50)], fill=blend(BG, dark_green, a), width=1)

    # Data points at grid intersections (ground plane)
    for _ in range(300):
        t = random.uniform(0.05, 0.95)
        spread = random.uniform(-0.9, 0.9)
        y = cy + int((t ** 1.8) * (H - cy + 200))
        x_near = cx + int(spread * W * 1.2)
        x_far = cx + int(spread * 60)
        x = int(x_far + (x_near - x_far) * t)

        if 0 <= x <= W and 0 <= y <= H:
            size = max(1, int(3 * (1 - t * 0.6)))
            a = random.uniform(0.3, 0.8) * (1 - t * 0.5)

            # Some nodes pulse brighter
            if random.random() < 0.15:
                a = min(0.95, a * 2)
                c = (180, 255, 200)
            else:
                c = green

            draw.ellipse([x - size, y - size, x + size, y + size],
                         fill=blend(BG, c, a))

            # Occasional data labels
            if random.random() < 0.08 and size >= 2:
                label = random.choice([
                    f"{random.randint(0,255):02X}", f"0x{random.randint(0,65535):04X}",
                    f"{random.uniform(0,1):.2f}", f"N{random.randint(1,999)}",
                ])
                draw.text((x + 6, y - 6), label,
                          fill=blend(BG, green, a * 0.5), font=font_sm)

    # Central bright "sun" / data beacon
    for r in range(200, 0, -2):
        a = 0.12 * (1 - r / 200) ** 2
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=blend(BG, green, a))

    img = img.filter(ImageFilter.GaussianBlur(radius=0.4))
    img.save("backgrounds/5-cyber-grid.png", "PNG", optimize=True)
    print("Saved backgrounds/5-cyber-grid.png")


# ─────────────────────────────────────────────────────────────
# 6. Terminal Scroll — hacker output flooding the screen
# ─────────────────────────────────────────────────────────────
def wallpaper_terminal_scroll():
    """Screen full of scrolling terminal output like a hacking session."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    font = get_font(18)
    font_sm = get_font(14)
    random.seed(303)

    green = (0, 255, 65)
    dim_green = (0, 150, 35)
    bright = (180, 255, 200)
    red = (255, 50, 50)
    yellow = (200, 200, 0)
    cyan = (0, 200, 200)

    line_h = 24
    rows = H // line_h + 1
    margin = 30

    # Line templates — realistic hacking output
    templates = [
        ("dim", "[{time}] Scanning port {port}/tcp..."),
        ("green", "[{time}] PORT {port}/tcp OPEN — {service}"),
        ("dim", "[{time}] Trying {ip}:{port}..."),
        ("bright", "[{time}] Connection established to {ip}"),
        ("red", "[{time}] WARNING: Firewall detected on {ip}"),
        ("dim", "[{time}] Enumerating users on {ip}..."),
        ("green", "[{time}] Found user: {user}@{ip}"),
        ("dim", "[{time}] Bruteforce attempt {n}/1000 on {ip}:{port}"),
        ("bright", "[{time}] ACCESS GRANTED — root@{ip}"),
        ("dim", "[{time}] Downloading /etc/passwd from {ip}..."),
        ("yellow", "[{time}] ALERT: IDS triggered on {ip}"),
        ("dim", "[{time}] Pivoting through {ip} to subnet {subnet}"),
        ("green", "[{time}] Extracting credentials from {ip}:/var/db"),
        ("dim", "[{time}] ARP scan: {ip} ({mac})"),
        ("cyan", "[{time}] Reverse shell opened on {ip}:{port}"),
        ("dim", "[{time}] Exfiltrating {size}MB via DNS tunnel"),
        ("red", "[{time}] CRITICAL: Honeypot detected at {ip}"),
        ("green", "[{time}] Hashcat: cracked {n} hashes ({rate} H/s)"),
        ("dim", "[{time}] nmap -sV -sC {ip} — scanning..."),
        ("bright", "[{time}] CVE-2024-{cve} exploit successful on {ip}"),
        ("dim", "[{time}] Injecting payload into {ip}:{port}"),
        ("dim", "[{time}] SQLi test: ' OR 1=1 -- on {ip}/login"),
        ("green", "[{time}] Database dumped: {n} records from {ip}"),
        ("dim", "[{time}] Establishing SOCKS proxy via {ip}"),
        ("yellow", "[{time}] Rotating proxy to {ip}:{port}"),
    ]

    services = ["ssh", "http", "https", "ftp", "mysql", "redis", "smtp", "dns", "rdp", "vnc"]
    users = ["root", "admin", "www-data", "postgres", "deploy", "git", "daemon", "operator"]

    for row in range(rows):
        y = row * line_h
        t = row / rows

        # Fade at top and bottom
        base_a = 1.0
        if t < 0.05:
            base_a = t / 0.05
        elif t > 0.95:
            base_a = (1 - t) / 0.05

        style, template = random.choice(templates)
        text = template.format(
            time=f"{random.randint(10,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}",
            port=random.choice([22, 80, 443, 3306, 8080, 8443, 21, 25, 53, 6379, 5432, 3389]),
            ip=f"{random.randint(10,192)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
            service=random.choice(services),
            user=random.choice(users),
            n=random.randint(1, 9999),
            subnet=f"{random.randint(10,172)}.{random.randint(0,255)}.{random.randint(0,255)}.0/24",
            mac=":".join(f"{random.randint(0,255):02x}" for _ in range(6)),
            size=random.randint(1, 500),
            rate=f"{random.randint(100,9999)}k",
            cve=f"{random.randint(1000,9999)}",
        )

        if style == "dim":
            color = blend(BG, dim_green, 0.35 * base_a)
        elif style == "green":
            color = blend(BG, green, 0.65 * base_a)
        elif style == "bright":
            color = blend(BG, bright, 0.80 * base_a)
        elif style == "red":
            color = blend(BG, red, 0.55 * base_a)
        elif style == "yellow":
            color = blend(BG, yellow, 0.45 * base_a)
        elif style == "cyan":
            color = blend(BG, cyan, 0.55 * base_a)
        else:
            color = blend(BG, green, 0.40 * base_a)

        # Random indentation for variety
        indent = random.choice([0, 0, 0, 20, 20, 40])
        draw.text((margin + indent, y), text, fill=color, font=font)

    # Scanline effect — horizontal lines every 2px
    for y in range(0, H, 4):
        draw.line([(0, y), (W, y)], fill=blend(BG, (0, 0, 0), 0.15), width=1)

    # Bright focus band in center
    for dy in range(-80, 80):
        y = H // 2 + dy
        a = 0.04 * (1 - abs(dy) / 80) ** 2
        draw.line([(0, y), (W, y)], fill=blend(BG, green, a), width=1)

    img = img.filter(ImageFilter.GaussianBlur(radius=0.2))
    img.save("backgrounds/6-terminal-scroll.png", "PNG", optimize=True)
    print("Saved backgrounds/6-terminal-scroll.png")


# ─────────────────────────────────────────────────────────────
# 7. Skull ASCII — hacker skull made of characters
# ─────────────────────────────────────────────────────────────
def wallpaper_skull():
    """A hacker skull composed of ASCII/Matrix characters on dark background."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    random.seed(404)

    font_sm = get_font(14)
    font_md = get_font(20)
    font_bg = get_font(10)

    green = (0, 255, 65)
    bright = (180, 255, 200)
    chars = MATRIX_CHARS + list("01@#$%&!?><{}[]=/\\|;:")

    cx, cy = W // 2, H // 2

    # Background scatter
    for _ in range(8000):
        x = random.randint(0, W)
        y = random.randint(0, H)
        a = random.uniform(0.02, 0.06)
        draw.text((x, y), random.choice(chars), fill=blend(BG, green, a), font=font_bg)

    # Skull shape using parametric math
    # We'll fill the skull shape with dense characters
    def in_skull(px, py):
        """Check if point is inside a skull shape centered at (cx, cy)."""
        # Normalize coordinates
        nx = (px - cx) / 400
        ny = (py - cy) / 500

        # Main cranium (top oval)
        cranium = (nx ** 2) / 1.0 + ((ny + 0.25) ** 2) / 0.85
        if cranium < 1 and ny < 0.35:
            # Left eye socket
            ex_l = ((nx + 0.35) ** 2) / 0.045 + ((ny + 0.05) ** 2) / 0.06
            if ex_l < 1:
                return False
            # Right eye socket
            ex_r = ((nx - 0.35) ** 2) / 0.045 + ((ny + 0.05) ** 2) / 0.06
            if ex_r < 1:
                return False
            # Nose triangle
            if abs(nx) < 0.12 and 0.1 < ny < 0.3 and abs(nx) < 0.12 * (1 - (ny - 0.1) / 0.2):
                return False
            return True

        # Jaw (narrower rectangle below)
        if abs(nx) < 0.65 * (1 - max(0, (ny - 0.35)) * 1.2) and 0.3 < ny < 0.75:
            # Teeth gaps
            if 0.42 < ny < 0.55 and int((nx + 0.6) * 8) % 2 == 0:
                return False
            return True

        return False

    def skull_edge_dist(px, py):
        """Approximate distance to the skull edge for glow effects."""
        nx = (px - cx) / 400
        ny = (py - cy) / 500
        cranium = (nx ** 2) / 1.0 + ((ny + 0.25) ** 2) / 0.85
        return abs(cranium - 1)

    # Fill skull with characters
    step = 14
    for y in range(cy - 520, cy + 420, step):
        for x in range(cx - 450, cx + 450, step):
            if in_skull(x, y):
                char = random.choice(chars)
                # Brighter near edges
                edge_d = skull_edge_dist(x, y)
                if edge_d < 0.15:
                    a = random.uniform(0.65, 0.90)
                    c = bright
                else:
                    a = random.uniform(0.30, 0.60)
                    c = green
                draw.text((x, y), char, fill=blend(BG, c, a), font=font_md)

    # Eye glow — fill eye sockets with bright dots
    for eye_cx in [cx - 140, cx + 140]:
        eye_cy = cy - 25
        for _ in range(600):
            angle = random.uniform(0, 2 * math.pi)
            r = random.uniform(0, 65)
            ex = eye_cx + r * math.cos(angle) * 1.05
            ey = eye_cy + r * math.sin(angle) * 1.1
            a = 0.7 * (1 - r / 65) ** 1.5
            if a > 0.05:
                draw.text((int(ex), int(ey)), random.choice("01"),
                          fill=blend(BG, bright, a), font=font_sm)

    # Radial glow around skull
    for r in range(600, 0, -3):
        a = 0.025 * (1 - r / 600) ** 2
        if a > 0.002:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                         outline=blend(BG, green, a))

    img = img.filter(ImageFilter.GaussianBlur(radius=0.4))
    img.save("backgrounds/7-skull.png", "PNG", optimize=True)
    print("Saved backgrounds/7-skull.png")


if __name__ == "__main__":
    wallpaper_matrix_rain()
    wallpaper_circuit()
    wallpaper_hexdump()
    wallpaper_binary_rain()
    wallpaper_cyber_grid()
    wallpaper_terminal_scroll()
    wallpaper_skull()
    print("Done! Generated 7 wallpapers.")
