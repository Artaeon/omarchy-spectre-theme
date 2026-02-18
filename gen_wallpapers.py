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


# ─────────────────────────────────────────────────────────────
# 8. Glowing Cross — monumental cross made of Matrix characters
# ─────────────────────────────────────────────────────────────
def wallpaper_cross():
    """A towering glowing cross made of cascading Matrix characters."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    random.seed(777)

    font_bg = get_font(10)
    font_sm = get_font(16)
    font_md = get_font(22)
    font_lg = get_font(30)

    green = (0, 255, 65)
    bright = (180, 255, 210)
    chars = MATRIX_CHARS + list("✝✟†‡")

    cx, cy = W // 2, H // 2

    # Background scatter
    for _ in range(8000):
        x = random.randint(0, W)
        y = random.randint(0, H)
        a = random.uniform(0.02, 0.06)
        draw.text((x, y), random.choice(MATRIX_CHARS), fill=blend(BG, green, a), font=font_bg)

    # Cross dimensions
    cross_h = 1400   # total height
    cross_w = 800    # crossbeam width
    beam_thick = 140  # thickness of beams
    crossbeam_y = cy - 200  # where horizontal beam sits

    def in_cross(px, py):
        """Check if point is inside the cross shape."""
        # Vertical beam
        if abs(px - cx) < beam_thick // 2:
            if cy - cross_h // 2 < py < cy + cross_h // 2:
                return True
        # Horizontal crossbeam
        if abs(py - crossbeam_y) < beam_thick // 2:
            if abs(px - cx) < cross_w // 2:
                return True
        return False

    def cross_dist(px, py):
        """Distance to nearest cross edge for glow."""
        dists = []
        # Vertical beam edges
        if cy - cross_h // 2 < py < cy + cross_h // 2:
            dists.append(abs(abs(px - cx) - beam_thick // 2))
        # Horizontal beam edges
        if abs(px - cx) < cross_w // 2:
            dists.append(abs(abs(py - crossbeam_y) - beam_thick // 2))
        # Ends
        if abs(px - cx) < beam_thick // 2:
            dists.append(abs(py - (cy - cross_h // 2)))
            dists.append(abs(py - (cy + cross_h // 2)))
        if abs(py - crossbeam_y) < beam_thick // 2:
            dists.append(abs(px - (cx - cross_w // 2)))
            dists.append(abs(px - (cx + cross_w // 2)))
        return min(dists) if dists else 999

    # Fill cross with dense characters
    step = 16
    for y in range(cy - cross_h // 2 - 10, cy + cross_h // 2 + 10, step):
        for x in range(cx - cross_w // 2 - 10, cx + cross_w // 2 + 10, step):
            if in_cross(x, y):
                char = random.choice(chars)
                # Edge glow
                ed = cross_dist(x, y)
                if ed < 20:
                    a = random.uniform(0.75, 0.95)
                    c = bright
                    f = font_lg
                elif ed < 40:
                    a = random.uniform(0.55, 0.75)
                    c = green
                    f = font_md
                else:
                    a = random.uniform(0.30, 0.55)
                    c = green
                    f = font_sm
                draw.text((x, y), char, fill=blend(BG, c, a), font=f)

    # Matrix rain falling through the cross
    for col in range(cx - cross_w // 2, cx + cross_w // 2, 34):
        stream_len = random.randint(8, 25)
        start_y = random.randint(cy - cross_h // 2, cy + 200)
        for i in range(stream_len):
            y = start_y + i * 36
            x = col + random.randint(-5, 5)
            if not in_cross(x, y):
                continue
            t = i / stream_len
            if i == 0:
                color = blend(BG, bright, 0.90)
            else:
                color = blend(BG, green, max(0.1, 0.70 * (1 - t)))
            draw.text((x, y), random.choice(MATRIX_CHARS), fill=color, font=font_md)

    # Radiant glow behind cross
    for r in range(800, 0, -4):
        a = 0.03 * (1 - r / 800) ** 2
        if a > 0.001:
            draw.ellipse([cx - r, cy - 100 - r, cx + r, cy - 100 + r],
                         outline=blend(BG, green, a))

    # Light rays emanating from cross center
    for angle_deg in range(0, 360, 15):
        angle = math.radians(angle_deg)
        for r in range(50, 700, 3):
            x = cx + int(r * math.cos(angle))
            y = crossbeam_y + int(r * math.sin(angle))
            if 0 <= x < W and 0 <= y < H:
                a = 0.06 * (1 - r / 700) ** 1.5
                if a > 0.003:
                    draw.point((x, y), fill=blend(BG, green, a))

    img = img.filter(ImageFilter.GaussianBlur(radius=0.4))
    img.save("backgrounds/8-cross.png", "PNG", optimize=True)
    print("Saved backgrounds/8-cross.png")


# ─────────────────────────────────────────────────────────────
# 9. Jesus Silhouette — Christ figure with outstretched arms
# ─────────────────────────────────────────────────────────────
def wallpaper_jesus():
    """Silhouette of Jesus with outstretched arms, composed of Matrix code."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    random.seed(333)

    font_bg = get_font(10)
    font_sm = get_font(14)
    font_md = get_font(20)
    font_lg = get_font(28)

    green = (0, 255, 65)
    bright = (180, 255, 210)
    gold = (200, 255, 150)
    chars = MATRIX_CHARS + list("01✝")

    cx, cy = W // 2, H // 2 + 50

    # Background scatter
    for _ in range(6000):
        x = random.randint(0, W)
        y = random.randint(0, H)
        a = random.uniform(0.02, 0.05)
        draw.text((x, y), random.choice(MATRIX_CHARS), fill=blend(BG, green, a), font=font_bg)

    def in_figure(px, py):
        """Jesus silhouette: head + body + outstretched arms + robe."""
        nx = (px - cx) / 500
        ny = (py - cy) / 600

        # Head (circle)
        head_cy = -0.75
        if nx ** 2 + (ny - head_cy) ** 2 < 0.025:
            return True

        # Halo (ring around head, slightly larger)
        head_dist = nx ** 2 + (ny - head_cy) ** 2
        if 0.03 < head_dist < 0.05:
            return True

        # Neck
        if abs(nx) < 0.04 and -0.62 < ny < -0.55:
            return True

        # Torso (tapers slightly)
        if -0.55 < ny < 0.1:
            torso_w = 0.12 + 0.03 * ((ny + 0.55) / 0.65)
            if abs(nx) < torso_w:
                return True

        # Arms outstretched (slight downward angle)
        arm_y_center = -0.40
        arm_droop = 0.15  # how much arms droop at edges
        if 0.12 < abs(nx) < 0.85:
            arm_y = arm_y_center + arm_droop * ((abs(nx) - 0.12) / 0.73) ** 1.3
            if abs(ny - arm_y) < 0.04:
                return True

        # Hands (slightly wider at arm ends)
        for sign in [-1, 1]:
            hand_cx = sign * 0.85
            hand_cy = arm_y_center + arm_droop
            if (nx - hand_cx) ** 2 + (ny - hand_cy) ** 2 < 0.003:
                return True

        # Robe (flowing down, wider at bottom)
        if 0.1 < ny < 0.85:
            robe_t = (ny - 0.1) / 0.75
            robe_w = 0.12 + 0.25 * robe_t ** 0.7
            if abs(nx) < robe_w:
                return True

        return False

    # Fill figure with characters
    step = 14
    for y in range(cy - 550, cy + 550, step):
        for x in range(cx - 500, cx + 500, step):
            if in_figure(x, y):
                char = random.choice(chars)
                # Brightness based on proximity to center
                dist = math.sqrt((x - cx) ** 2 + (y - cy + 100) ** 2) / 500
                if dist < 0.2:
                    a = random.uniform(0.70, 0.90)
                    c = bright
                    f = font_lg
                elif dist < 0.5:
                    a = random.uniform(0.45, 0.65)
                    c = green
                    f = font_md
                else:
                    a = random.uniform(0.25, 0.45)
                    c = green
                    f = font_sm

                draw.text((x, y), char, fill=blend(BG, c, a), font=f)

    # Halo glow behind head
    halo_cy = cy - 450
    for r in range(200, 0, -2):
        a = 0.06 * (1 - r / 200) ** 1.5
        if a > 0.002:
            draw.ellipse([cx - r, halo_cy - r, cx + r, halo_cy + r],
                         outline=blend(BG, gold, a))

    # Light radiating from figure
    for angle_deg in range(0, 360, 8):
        angle = math.radians(angle_deg)
        for r in range(100, 900, 3):
            x = cx + int(r * math.cos(angle))
            y = halo_cy + int(r * math.sin(angle))
            if 0 <= x < W and 0 <= y < H:
                a = 0.04 * (1 - r / 900) ** 2
                if a > 0.002:
                    draw.point((x, y), fill=blend(BG, gold, a))

    # Matrix rain flowing around the figure
    for col in range(0, W, 40):
        if abs(col - cx) < 250:
            continue  # skip over the figure
        stream_len = random.randint(8, 20)
        start_y = random.randint(-200, H)
        for i in range(stream_len):
            y = start_y + i * 34
            if y < 0 or y > H:
                continue
            t = i / stream_len
            color = blend(BG, green, max(0.05, 0.30 * (1 - t)))
            draw.text((col, y), random.choice(MATRIX_CHARS), fill=color, font=font_sm)

    img = img.filter(ImageFilter.GaussianBlur(radius=0.4))
    img.save("backgrounds/9-jesus.png", "PNG", optimize=True)
    print("Saved backgrounds/9-jesus.png")


# ─────────────────────────────────────────────────────────────
# 10. Crown of Thorns — circular crown with Matrix code
# ─────────────────────────────────────────────────────────────
def wallpaper_crown_of_thorns():
    """Crown of thorns ring made of Matrix code with thorny protrusions."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    random.seed(430)

    font_bg = get_font(10)
    font_sm = get_font(14)
    font_md = get_font(20)
    font_lg = get_font(26)

    green = (0, 255, 65)
    bright = (180, 255, 210)
    red_green = (100, 200, 60)
    chars = MATRIX_CHARS + list("01✝†‡×")

    cx, cy = W // 2, H // 2

    # Background subtle rain
    for _ in range(6000):
        x = random.randint(0, W)
        y = random.randint(0, H)
        a = random.uniform(0.02, 0.05)
        draw.text((x, y), random.choice(MATRIX_CHARS), fill=blend(BG, green, a), font=font_bg)

    # Crown parameters
    outer_r = 450
    inner_r = 350
    crown_thickness = outer_r - inner_r

    # Thorns — spiky protrusions
    num_thorns = 40
    thorn_angles = [i * 2 * math.pi / num_thorns + random.uniform(-0.1, 0.1) for i in range(num_thorns)]
    thorn_lengths = [random.randint(60, 150) for _ in range(num_thorns)]

    def in_crown(px, py):
        """Check if point is inside the crown (torus + thorns)."""
        dx = px - cx
        dy = (py - cy) * 1.4  # flatten to make it more oval / perspective
        dist = math.sqrt(dx ** 2 + dy ** 2)

        # Main ring
        if inner_r < dist < outer_r:
            return "ring"

        # Thorns
        angle = math.atan2(dy, dx)
        for i, ta in enumerate(thorn_angles):
            angle_diff = abs(((angle - ta + math.pi) % (2 * math.pi)) - math.pi)
            if angle_diff < 0.06:
                thorn_end = outer_r + thorn_lengths[i]
                if outer_r - 10 < dist < thorn_end:
                    # Taper the thorn
                    thorn_t = (dist - outer_r) / thorn_lengths[i]
                    if angle_diff < 0.06 * (1 - thorn_t * 0.8):
                        return "thorn"

        return None

    # Fill crown with characters
    step = 14
    for y in range(cy - 500, cy + 500, step):
        for x in range(cx - 650, cx + 650, step):
            part = in_crown(x, y)
            if part:
                char = random.choice(chars)
                dx = x - cx
                dy = (y - cy) * 1.4
                dist = math.sqrt(dx ** 2 + dy ** 2)

                if part == "thorn":
                    thorn_t = max(0, (dist - outer_r) / 150)
                    a = random.uniform(0.50, 0.80) * (1 - thorn_t * 0.5)
                    c = bright
                    f = font_md
                else:
                    # Ring: brighter at outer and inner edges
                    edge_dist = min(abs(dist - inner_r), abs(dist - outer_r))
                    if edge_dist < 25:
                        a = random.uniform(0.65, 0.90)
                        c = bright
                        f = font_lg
                    else:
                        a = random.uniform(0.35, 0.55)
                        c = green
                        f = font_md

                draw.text((x, y), char, fill=blend(BG, c, a), font=f)

    # Intertwined braids — sinusoidal paths around the ring
    for braid in range(3):
        phase = braid * 2 * math.pi / 3
        for t in range(0, 3600, 2):
            angle = math.radians(t / 10)
            wave = 30 * math.sin(angle * 8 + phase)
            r = (inner_r + outer_r) / 2 + wave
            x = cx + int(r * math.cos(angle))
            y = cy + int(r * math.sin(angle) / 1.4)
            if 0 <= x < W and 0 <= y < H:
                a = 0.5 + 0.3 * math.sin(angle * 3 + phase)
                draw.text((x, y), random.choice(MATRIX_CHARS),
                          fill=blend(BG, bright, max(0.2, a * 0.6)), font=font_sm)

    # Central glow
    for r in range(350, 0, -3):
        a = 0.02 * (1 - r / 350) ** 2
        if a > 0.001:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                         outline=blend(BG, green, a))

    img = img.filter(ImageFilter.GaussianBlur(radius=0.4))
    img.save("backgrounds/10-crown-of-thorns.png", "PNG", optimize=True)
    print("Saved backgrounds/10-crown-of-thorns.png")


# ─────────────────────────────────────────────────────────────
# 11. Ichthys (Fish) — Christian fish symbol with data streams
# ─────────────────────────────────────────────────────────────
def wallpaper_ichthys():
    """Christian fish (Ichthys) symbol composed of streaming Matrix code."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    random.seed(153)  # John 21:11 — the miraculous catch

    font_bg = get_font(10)
    font_sm = get_font(14)
    font_md = get_font(20)
    font_lg = get_font(28)

    green = (0, 255, 65)
    bright = (180, 255, 210)
    chars = MATRIX_CHARS + list("IXΘYΣ01")  # IXΘYΣ = ICHTHYS

    cx, cy = W // 2, H // 2

    # Background scatter
    for _ in range(6000):
        x = random.randint(0, W)
        y = random.randint(0, H)
        a = random.uniform(0.02, 0.05)
        draw.text((x, y), random.choice(MATRIX_CHARS), fill=blend(BG, green, a), font=font_bg)

    # Fish shape using parametric arcs
    fish_scale = 500
    fish_tail_x = cx - 550  # leftmost point (tail)
    fish_mouth_x = cx + 550  # rightmost point (mouth meets)

    def in_fish(px, py):
        """Ichthys fish: two arcs meeting at a point on the right."""
        nx = (px - cx) / fish_scale
        ny = (py - cy) / fish_scale

        # Upper arc: starts at (-1.1, 0), curves up, ends at (1.1, 0)
        # Lower arc: mirror image
        # Using parametric: the fish is bounded by two circular arcs

        # Simplified: elliptical arcs
        # Upper body line
        if -1.1 <= nx <= 1.1:
            # Fish body height varies: max at center, zero at both ends
            t = (nx + 1.1) / 2.2  # 0 at tail, 1 at mouth
            # Asymmetric: fatter toward front
            body_h = 0.45 * math.sin(t * math.pi) ** 0.7
            if abs(ny) < body_h:
                return True

            # Outline (thick border)
            if abs(abs(ny) - body_h) < 0.04:
                return True

        # Tail: V-shape extending left from the body
        if -1.6 <= nx <= -1.0:
            tail_t = (nx + 1.6) / 0.6  # 0 at far left, 1 at body junction
            tail_spread = 0.35 * (1 - tail_t)
            # Two lines of the tail
            for tail_dir in [-1, 1]:
                target_y = tail_dir * tail_spread
                if abs(ny - target_y) < 0.035:
                    return True

        return False

    def fish_outline_dist(px, py):
        """Distance to nearest fish outline."""
        nx = (px - cx) / fish_scale
        ny = (py - cy) / fish_scale
        if -1.1 <= nx <= 1.1:
            t = (nx + 1.1) / 2.2
            body_h = 0.45 * math.sin(t * math.pi) ** 0.7
            return abs(abs(ny) - body_h) * fish_scale
        return 999

    # Fill fish with characters
    step = 14
    for y in range(cy - 350, cy + 350, step):
        for x in range(cx - 850, cx + 650, step):
            if in_fish(x, y):
                char = random.choice(chars)
                od = fish_outline_dist(x, y)
                if od < 25:
                    a = random.uniform(0.70, 0.92)
                    c = bright
                    f = font_lg
                elif od < 60:
                    a = random.uniform(0.45, 0.65)
                    c = green
                    f = font_md
                else:
                    a = random.uniform(0.25, 0.45)
                    c = green
                    f = font_sm
                draw.text((x, y), char, fill=blend(BG, c, a), font=f)

    # Eye
    eye_x = cx + 320
    eye_y = cy - 40
    for r in range(40, 0, -2):
        a = 0.7 * (1 - r / 40)
        draw.ellipse([eye_x - r, eye_y - r, eye_x + r, eye_y + r],
                     fill=blend(BG, bright, a))

    # "IXΘYΣ" text inside the fish body
    ichthys_font = get_font(50)
    text = "ΙΧΘΥΣ"
    ichthys_color = blend(BG, bright, 0.7)
    draw.text((cx - 120, cy - 25), text, fill=ichthys_color, font=ichthys_font)

    # Data streams flowing through the fish
    for col in range(cx - 500, cx + 500, 50):
        stream_len = random.randint(5, 12)
        start_y = random.randint(cy - 200, cy - 50)
        for i in range(stream_len):
            y = start_y + i * 28
            if not in_fish(col, y):
                continue
            t = i / stream_len
            color = blend(BG, green, max(0.1, 0.50 * (1 - t)))
            draw.text((col, y), random.choice(MATRIX_CHARS), fill=color, font=font_sm)

    # Radial glow
    for r in range(600, 0, -4):
        a = 0.02 * (1 - r / 600) ** 2
        if a > 0.001:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                         outline=blend(BG, green, a))

    img = img.filter(ImageFilter.GaussianBlur(radius=0.4))
    img.save("backgrounds/11-ichthys.png", "PNG", optimize=True)
    print("Saved backgrounds/11-ichthys.png")


# ─────────────────────────────────────────────────────────────
# 12. Praying Hands — hands in prayer with Matrix code
# ─────────────────────────────────────────────────────────────
def wallpaper_praying_hands():
    """Praying hands silhouette composed of flowing Matrix characters."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    random.seed(316)  # John 3:16

    font_bg = get_font(10)
    font_sm = get_font(14)
    font_md = get_font(20)
    font_lg = get_font(26)

    green = (0, 255, 65)
    bright = (180, 255, 210)
    gold = (200, 255, 150)
    chars = MATRIX_CHARS + list("01✝†")

    cx, cy = W // 2, H // 2

    # Background scatter
    for _ in range(6000):
        x = random.randint(0, W)
        y = random.randint(0, H)
        a = random.uniform(0.02, 0.05)
        draw.text((x, y), random.choice(MATRIX_CHARS), fill=blend(BG, green, a), font=font_bg)

    def in_praying_hands(px, py):
        """Praying hands: two hands pressed together, fingers pointing up."""
        nx = (px - cx) / 400
        ny = (py - cy) / 550

        # Fingers (top section, pointing up, pressed together)
        if -0.75 < ny < -0.15:
            finger_t = (ny + 0.75) / 0.6  # 0 at top, 1 at base of fingers
            # Fingers taper at top
            finger_w = 0.18 + 0.12 * finger_t
            # Gap in the middle (where hands meet) — very thin
            if abs(nx) < 0.015:
                return False
            if abs(nx) < finger_w:
                return True

        # Palm area (wider, where hands press together)
        if -0.15 < ny < 0.35:
            palm_t = (ny + 0.15) / 0.5
            palm_w = 0.30 + 0.08 * palm_t
            # Slight indentation at center where hands meet
            if abs(nx) < 0.01:
                return False
            if abs(nx) < palm_w:
                return True

        # Wrists (narrowing)
        if 0.35 < ny < 0.65:
            wrist_t = (ny - 0.35) / 0.3
            wrist_w = 0.38 - 0.10 * wrist_t
            # Split into two wrists
            for sign in [-1, 1]:
                wrist_cx = sign * 0.12 * (1 + wrist_t * 0.5)
                if abs(nx - wrist_cx) < wrist_w * 0.4:
                    return True

        # Forearms (separating, angled outward)
        if 0.65 < ny < 1.0:
            arm_t = (ny - 0.65) / 0.35
            for sign in [-1, 1]:
                arm_cx = sign * (0.20 + 0.25 * arm_t)
                arm_w = 0.12 + 0.03 * arm_t
                if abs(nx - arm_cx) < arm_w:
                    return True

        return False

    # Fill with characters
    step = 14
    for y in range(cy - 450, cy + 580, step):
        for x in range(cx - 350, cx + 350, step):
            if in_praying_hands(x, y):
                char = random.choice(chars)
                dist = math.sqrt((x - cx) ** 2 + (y - cy + 50) ** 2) / 400

                if dist < 0.3:
                    a = random.uniform(0.65, 0.88)
                    c = bright
                    f = font_lg
                elif dist < 0.6:
                    a = random.uniform(0.45, 0.65)
                    c = green
                    f = font_md
                else:
                    a = random.uniform(0.25, 0.45)
                    c = green
                    f = font_sm
                draw.text((x, y), char, fill=blend(BG, c, a), font=f)

    # Light emanating upward from fingertips
    for angle_deg in range(-60, 61, 5):
        angle = math.radians(angle_deg - 90)  # centered upward
        for r in range(50, 800, 3):
            x = cx + int(r * math.cos(angle))
            y = (cy - 420) + int(r * math.sin(angle))
            if 0 <= x < W and 0 <= y < H:
                a = 0.05 * (1 - r / 800) ** 2
                if a > 0.002:
                    draw.point((x, y), fill=blend(BG, gold, a))

    # Small cross above the hands
    cross_cy = cy - 520
    cross_h = 100
    cross_w = 60
    beam_t = 14
    for y in range(cross_cy - cross_h // 2, cross_cy + cross_h // 2, 12):
        for x in range(cx - cross_w // 2, cx + cross_w // 2, 12):
            # Vertical
            is_vert = abs(x - cx) < beam_t
            # Horizontal
            is_horiz = abs(y - (cross_cy - cross_h // 6)) < beam_t and abs(x - cx) < cross_w // 2
            if is_vert or is_horiz:
                a = random.uniform(0.60, 0.85)
                draw.text((x, y), random.choice("✝†"),
                          fill=blend(BG, bright, a), font=font_lg)

    # Radial glow
    for r in range(500, 0, -3):
        a = 0.025 * (1 - r / 500) ** 2
        if a > 0.001:
            draw.ellipse([cx - r, cy - 100 - r, cx + r, cy - 100 + r],
                         outline=blend(BG, green, a))

    img = img.filter(ImageFilter.GaussianBlur(radius=0.4))
    img.save("backgrounds/12-praying-hands.png", "PNG", optimize=True)
    print("Saved backgrounds/12-praying-hands.png")


# ─────────────────────────────────────────────────────────────
# 13. Alice Rabbit & Time — Alice rabbit with a clock and Eccl 3:1
# ─────────────────────────────────────────────────────────────
def wallpaper_alice_time():
    """Alice in Wonderland rabbit with a clock and Ecclesiastes 3:1."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    random.seed(1234)

    font_bg = get_font(10)
    font_sm = get_font(16)
    font_md = get_font(22)
    font_lg = get_font(32)
    font_verse = get_font(40)

    green = (0, 255, 65)
    bright = (180, 255, 210)
    chars = MATRIX_CHARS + list("TIC-TOK")

    cx, cy = W // 2, H // 2

    # Background scatter
    for _ in range(6000):
        x = random.randint(0, W)
        y = random.randint(0, H)
        a = random.uniform(0.02, 0.05)
        draw.text((x, y), random.choice(MATRIX_CHARS), fill=blend(BG, green, a), font=font_bg)

    def in_rabbit(px, py):
        """Simple rabbit silhouette (Alice style with waistcoat/clock)."""
        nx = (px - (cx - 400)) / 300
        ny = (py - (cy + 200)) / 400

        # Body (waistcoat)
        if nx**2 + ny**2 < 0.15:
            return True
        # Head
        if nx**2 + (ny + 0.5)**2 < 0.05:
            return True
        # Ears
        if abs(nx - 0.05) < 0.03 and -0.9 < ny < -0.55:
            return True
        if abs(nx + 0.05) < 0.03 and -0.85 < ny < -0.5:
            return True
        return False

    def in_clock(px, py):
        """Pocket watch silhouette."""
        nx = (px - (cx + 400)) / 250
        ny = (py - cy) / 250
        dist = nx**2 + ny**2
        if 0.8 < dist < 1.0: # rim
            return "rim"
        if dist < 0.8: # face
            return "face"
        # stem
        if abs(nx) < 0.05 and -1.1 < ny < -1.0:
            return "rim"
        return None

    # Fill rabbit
    step = 14
    for y in range(cy - 400, cy + 600, step):
        for x in range(cx - 700, cx - 100, step):
            if in_rabbit(x, y):
                char = random.choice(chars)
                a = random.uniform(0.4, 0.8)
                draw.text((x, y), char, fill=blend(BG, bright, a), font=font_md)

    # Fill clock
    for y in range(cy - 300, cy + 300, step):
        for x in range(cx + 150, cx + 650, step):
            part = in_clock(x, y)
            if part == "rim":
                draw.text((x, y), random.choice("01"), fill=blend(BG, bright, 0.9), font=font_lg)
            elif part == "face":
                draw.text((x, y), random.choice(MATRIX_CHARS), fill=blend(BG, green, 0.3), font=font_sm)

    # Clock hands
    draw.line([(cx+400, cy), (cx+400, cy-150)], fill=blend(BG, bright, 0.9), width=4)
    draw.line([(cx+400, cy), (cx+520, cy+50)], fill=blend(BG, bright, 0.9), width=4)

    # Verse: Ecclesiastes 3:1
    verse = "To everything there is a season, and a time to every purpose under the heaven."
    tw = draw.textlength(verse, font=font_verse)
    draw.text(((W - tw) // 2, cy - 400), verse, fill=blend(BG, bright, 0.8), font=font_verse)
    draw.text(((W - draw.textlength("ECCLESIASTES 3:1", font=font_md)) // 2, cy - 340), "ECCLESIASTES 3:1", fill=blend(BG, green, 0.6), font=font_md)

    img = img.filter(ImageFilter.GaussianBlur(radius=0.4))
    img.save("backgrounds/13-alice-time.png", "PNG", optimize=True)
    print("Saved backgrounds/13-alice-time.png")


# ─────────────────────────────────────────────────────────────
# 14. Kingdom of God — Crown and Daniel 2:44
# ─────────────────────────────────────────────────────────────
def wallpaper_kingdom():
    """Kingdom of God Crown with Daniel 2:44."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    random.seed(244)

    font_bg = get_font(10)
    font_md = get_font(24)
    font_lg = get_font(40)
    font_verse = get_font(36)

    green = (0, 255, 65)
    bright = (180, 255, 210)
    gold = (212, 175, 55)

    cx, cy = W // 2, H // 2

    # Background scatter
    for _ in range(6000):
        x = random.randint(0, W)
        y = random.randint(0, H)
        a = random.uniform(0.02, 0.05)
        draw.text((x, y), random.choice(MATRIX_CHARS), fill=blend(BG, green, a), font=font_bg)

    def in_crown(px, py):
        """Regal crown silhouette."""
        nx = (px - cx) / 500
        ny = (py - cy) / 400
        if -0.6 < nx < 0.6 and 0.1 < ny < 0.4: # base
            return "base"
        # peaks
        if -0.6 < nx < -0.4 and -0.2 < ny < 0.1 and abs(nx+0.5) < 0.1 * (1-(ny+0.2)/0.3):
             return "peak"
        if -0.1 < nx < 0.1 and -0.4 < ny < 0.1 and abs(nx) < 0.1 * (1-(ny+0.4)/0.5):
             return "peak"
        if 0.4 < nx < 0.6 and -0.2 < ny < 0.1 and abs(nx-0.5) < 0.1 * (1-(ny+0.2)/0.3):
             return "peak"
        return None

    # Fill crown
    step = 16
    for y in range(cy - 400, cy + 400, step):
        for x in range(cx - 500, cx + 500, step):
            part = in_crown(x, y)
            if part:
                a = random.uniform(0.5, 0.9)
                c = bright if part == "peak" else green
                draw.text((x, y), random.choice(MATRIX_CHARS), fill=blend(BG, c, a), font=font_md)

    # Verse: Daniel 2:44
    verse = "And the God of heaven will set up a kingdom which shall never be destroyed."
    tw = draw.textlength(verse, font=font_verse)
    draw.text(((W - tw) // 2, cy + 300), verse, fill=blend(BG, bright, 0.8), font=font_verse)
    draw.text(((W - draw.textlength("DANIEL 2:44", font=font_md)) // 2, cy + 360), "DANIEL 2:44", fill=blend(BG, green, 0.6), font=font_md)

    # Glow rays
    for i in range(200):
        length = random.randint(300, 600)
        angle = random.uniform(0, 2*math.pi)
        draw.line([(cx, cy), (cx + length*math.cos(angle), cy + length*math.sin(angle))], fill=blend(BG, gold, 0.1), width=1)

    img = img.filter(ImageFilter.GaussianBlur(radius=0.4))
    img.save("backgrounds/14-kingdom.png", "PNG", optimize=True)
    print("Saved backgrounds/14-kingdom.png")


# ─────────────────────────────────────────────────────────────
# 15. Armor of God — Shield and Ephesians 6:11
# ─────────────────────────────────────────────────────────────
def wallpaper_armor():
    """Armor of God Shield with Ephesians 6:11."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    random.seed(611)

    font_bg = get_font(10)
    font_md = get_font(24)
    font_lg = get_font(40)
    font_verse = get_font(36)

    green = (0, 255, 65)
    bright = (180, 255, 210)

    cx, cy = W // 2, H // 2

    # Background scatter
    for _ in range(6000):
        x = random.randint(0, W)
        y = random.randint(0, H)
        a = random.uniform(0.02, 0.05)
        draw.text((x, y), random.choice(MATRIX_CHARS), fill=blend(BG, green, a), font=font_bg)

    def in_shield(px, py):
        """Knight shield silhouette."""
        nx = (px - cx) / 400
        ny = (py - cy) / 500
        if -0.7 < nx < 0.7 and -0.8 < ny < 0.4:
            # tapers to point
            if ny > 0.4: return False
            if ny < 0 and abs(nx) < 0.7: return True
            if ny >= 0 and abs(nx) < 0.7 * (1 - (ny-0)/0.8): return True
        return False

    # Fill shield
    step = 16
    for y in range(cy - 500, cy + 500, step):
        for x in range(cx - 400, cx + 400, step):
            if in_shield(x, y):
                a = random.uniform(0.4, 0.9)
                draw.text((x, y), random.choice(MATRIX_CHARS), fill=blend(BG, green, a), font=font_md)

    # Cross on shield
    for y in range(cy - 400, cy + 200, 20):
        draw.text((cx-10, y), "✝", fill=blend(BG, bright, 0.9), font=font_lg)
    for x in range(cx - 150, cx + 150, 20):
        draw.text((x, cy-150), "✝", fill=blend(BG, bright, 0.9), font=font_lg)

    # Verse: Ephesians 6:11
    verse = "Put on the whole armor of God, that you may be able to stand against the wiles of the devil."
    # Wrap text manually if needed or use small font
    font_v = get_font(30)
    draw.text((cx - 700, cy + 400), verse, fill=blend(BG, bright, 0.8), font=font_v)
    draw.text((cx - 100, cy + 450), "EPHESIANS 6:11", fill=blend(BG, green, 0.6), font=font_md)

    img = img.filter(ImageFilter.GaussianBlur(radius=0.4))
    img.save("backgrounds/15-armor.png", "PNG", optimize=True)
    print("Saved backgrounds/15-armor.png")


# ─────────────────────────────────────────────────────────────
# 16. Lamb of God — Lamb silhouette and John 1:29
# ─────────────────────────────────────────────────────────────
def wallpaper_lamb():
    """Lamb of God with John 1:29."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    random.seed(129)

    font_bg = get_font(10)
    font_md = get_font(24)
    font_lg = get_font(40)
    font_verse = get_font(36)

    green = (0, 255, 65)
    bright = (180, 255, 210)

    cx, cy = W // 2, H // 2

    # Background scatter
    for _ in range(6000):
        x = random.randint(0, W)
        y = random.randint(0, H)
        a = random.uniform(0.02, 0.05)
        draw.text((x, y), random.choice(MATRIX_CHARS), fill=blend(BG, green, a), font=font_bg)

    def in_lamb(px, py):
        """Simple lamb silhouette."""
        nx = (px - cx) / 400
        ny = (py - cy) / 400
        # Body
        if (nx+0.2)**2 + ny**2 < 0.15:
            return True
        # Head
        if (nx-0.4)**2 + (ny+0.3)**2 < 0.02:
            return True
        # Legs
        if abs(nx+0.4) < 0.02 and 0 < ny < 0.4: return True
        if abs(nx+0.0) < 0.02 and 0 < ny < 0.4: return True
        return False

    # Fill lamb
    step = 14
    for y in range(cy - 300, cy + 300, step):
        for x in range(cx - 500, cx + 500, step):
            if in_lamb(x, y):
                a = random.uniform(0.6, 1.0)
                draw.text((x, y), random.choice(MATRIX_CHARS), fill=blend(BG, bright, a), font=font_md)

    # Verse: John 1:29
    verse = "Behold! The Lamb of God who takes away the sin of the world!"
    tw = draw.textlength(verse, font=font_verse)
    draw.text(((W - tw) // 2, cy + 350), verse, fill=blend(BG, bright, 0.8), font=font_verse)
    draw.text(((W - draw.textlength("JOHN 1:29", font=font_md)) // 2, cy + 410), "JOHN 1:29", fill=blend(BG, green, 0.6), font=font_md)

    img = img.filter(ImageFilter.GaussianBlur(radius=0.4))
    img.save("backgrounds/16-lamb.png", "PNG", optimize=True)
    print("Saved backgrounds/16-lamb.png")


# ─────────────────────────────────────────────────────────────
# 17. Alpha & Omega — Symbols and Revelation 22:13
# ─────────────────────────────────────────────────────────────
def wallpaper_alpha_omega():
    """Alpha & Omega symbols with Revelation 22:13."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    random.seed(2213)

    font_bg = get_font(10)
    font_sm = get_font(20)
    font_md = get_font(24)
    font_lg = get_font(50)
    font_xl = get_font(300)
    font_verse = get_font(36)

    green = (0, 255, 65)
    bright = (180, 255, 210)

    cx, cy = W // 2, H // 2

    # Background scatter
    for _ in range(6000):
        x = random.randint(0, W)
        y = random.randint(0, H)
        a = random.uniform(0.02, 0.05)
        draw.text((x, y), random.choice(MATRIX_CHARS), fill=blend(BG, green, a), font=font_bg)

    # Alpha & Omega text
    draw.text((cx - 600, cy - 200), "Α", fill=blend(BG, bright, 0.4), font=font_xl)
    draw.text((cx + 200, cy - 200), "Ω", fill=blend(BG, bright, 0.4), font=font_xl)

    # Central vortex of code
    for i in range(1000):
        radius = random.uniform(10, 800)
        angle = random.uniform(0, 2*math.pi)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        a = 0.8 * (1 - radius / 800)
        draw.text((x, y), random.choice(MATRIX_CHARS), fill=blend(BG, green, a), font=font_sm)

    # Verse: Revelation 22:13
    verse = "I am Alpha and Omega, the beginning and the end, the first and the last."
    tw = draw.textlength(verse, font=font_verse)
    draw.text(((W - tw) // 2, cy + 400), verse, fill=blend(BG, bright, 0.8), font=font_verse)
    draw.text(((W - draw.textlength("REVELATION 22:13", font=font_md)) // 2, cy + 460), "REVELATION 22:13", fill=blend(BG, green, 0.6), font=font_md)

    img = img.filter(ImageFilter.GaussianBlur(radius=0.4))
    img.save("backgrounds/17-alpha-omega.png", "PNG", optimize=True)
    print("Saved backgrounds/17-alpha-omega.png")


if __name__ == "__main__":
    wallpaper_matrix_rain()
    wallpaper_circuit()
    wallpaper_hexdump()
    wallpaper_binary_rain()
    wallpaper_cyber_grid()
    wallpaper_terminal_scroll()
    wallpaper_skull()
    wallpaper_cross()
    wallpaper_jesus()
    wallpaper_crown_of_thorns()
    wallpaper_ichthys()
    wallpaper_praying_hands()
    wallpaper_alice_time()
    wallpaper_kingdom()
    wallpaper_armor()
    wallpaper_lamb()
    wallpaper_alpha_omega()
    print("Done! Generated 17 wallpapers.")

