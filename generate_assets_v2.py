#!/usr/bin/env python3
"""Generate ESP32-HARNESS assets v2 — visually striking, not boring."""
import os, math

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(OUT_DIR, "assets")
os.makedirs(ASSETS, exist_ok=True)

# === PDF ===
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_LEFT

W, H = letter
CYAN = HexColor("#00d4ff")
DARK = HexColor("#0a0a0f")
DARK2 = HexColor("#111118")
DARK3 = HexColor("#16161f")
MUTED = HexColor("#6b6b7b")
LIGHT = HexColor("#e8e8ed")
GREEN = HexColor("#28c840")

def draw_grid_pattern(c, x0, y0, w, h, spacing=20, color=HexColor("#1e1e2a")):
    """Draw subtle grid pattern."""
    c.setStrokeColor(color)
    c.setLineWidth(0.3)
    for x in range(int(x0), int(x0 + w), spacing):
        c.line(x, y0, x, y0 + h)
    for y in range(int(y0), int(y0 + h), spacing):
        c.line(x0, y, x0 + w, y)

def draw_circuit_traces(c, x0, y0, w, h):
    """Draw decorative circuit trace pattern."""
    c.setStrokeColor(HexColor("#00d4ff30"))
    c.setLineWidth(0.8)
    # Horizontal traces
    for i in range(5):
        y = y0 + h * (0.1 + i * 0.2)
        x_start = x0 + w * (0.1 + (i % 3) * 0.25)
        x_end = x0 + w * (0.4 + (i % 3) * 0.2)
        c.line(x_start, y, x_end, y)
        # Node dots
        c.setFillColor(HexColor("#00d4ff40"))
        c.circle(x_end, y, 2, fill=1)
        # Vertical branch
        if i % 2 == 0:
            c.line(x_end, y, x_end, y + 15)
            c.circle(x_end, y + 15, 1.5, fill=1)

def draw_waveform(c, x0, y, width, amplitude=8, segments=30):
    """Draw a sine waveform."""
    c.setStrokeColor(CYAN)
    c.setLineWidth(1)
    path = c.beginPath()
    for i in range(segments + 1):
        x = x0 + (width * i / segments)
        val = y + amplitude * math.sin(i * 0.4)
        if i == 0:
            path.moveTo(x, val)
        else:
            path.lineTo(x, val)
    c.drawPath(path)

def build_pdf():
    path = os.path.join(OUT_DIR, "ESP32-HARNESS-Datasheet.pdf")
    c = canvas.Canvas(path, pagesize=letter)

    # === PAGE 1: Cover ===
    c.setFillColor(DARK)
    c.rect(0, 0, W, H, fill=1)

    # Grid pattern background
    draw_grid_pattern(c, 0, 0, W, H, spacing=24, color=HexColor("#0f0f18"))

    # Decorative circuit traces top-right
    draw_circuit_traces(c, W * 0.5, H * 0.6, W * 0.45, H * 0.35)

    # Waveform decoration
    draw_waveform(c, 0.8*inch, H - 0.8*inch, 3*inch, amplitude=6)

    # Cyan accent bar
    c.setFillColor(CYAN)
    c.rect(0.8*inch, H - 1.1*inch, 2.5*inch, 3, fill=1)

    # Title block
    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 42)
    c.drawString(0.8*inch, H - 1.6*inch, "ESP32")

    c.setFillColor(LIGHT)
    c.setFont("Helvetica-Bold", 42)
    c.drawString(3.1*inch, H - 1.6*inch, "-HARNESS")

    # Subtitle with accent line
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 13)
    c.drawString(0.8*inch, H - 2.0*inch, "ADVANCED PENTESTING, AUDIT & TELEMETRY FIRMWARE")

    # Version badge
    c.setStrokeColor(CYAN)
    c.setLineWidth(1)
    c.roundRect(0.8*inch, H - 2.5*inch, 1.2*inch, 0.35*inch, 3, stroke=1)
    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1.0*inch, H - 2.38*inch, "v1.0  MIT")

    # Right side: large decorative "2.4" watermark
    c.setFillColor(HexColor("#00d4ff08"))
    c.setFont("Helvetica-Bold", 180)
    c.drawRightString(W - 0.5*inch, H * 0.3, "2.4")

    c.setFillColor(HexColor("#00d4ff15"))
    c.setFont("Helvetica", 14)
    c.drawRightString(W - 0.5*inch, H * 0.3 - 20, "GHz")

    # Specs section
    y = H - 3.2*inch
    specs = [
        ("CONTROLLER", "ESP32-WROOM-32", "Dual-core 240 MHz, 520 KB SRAM"),
        ("RF TRANSCEIVER", "NRF24L01+ PA/LNA", "2.4 GHz ISM, +20 dBm, 250 kbps - 2 Mbps"),
        ("STORAGE", "MicroSD Module", "FAT32/exFAT, SPI, up to 32 GB"),
        ("DISPLAY", "OLED SSD1306", "128x64 monochrome, I2C"),
        ("BATTERY", "LiPo 3.7V 1000mAh", "USB-C charging, ~4 hours runtime"),
    ]

    for label, value, note in specs:
        # Label
        c.setFillColor(CYAN)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(0.8*inch, y, label)

        # Value
        c.setFillColor(LIGHT)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(2.6*inch, y + 2, value)

        # Note
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(2.6*inch, y - 10, note)

        # Separator
        c.setStrokeColor(HexColor("#1e1e2a"))
        c.setLineWidth(0.5)
        c.line(0.8*inch, y - 18, W - 0.8*inch, y - 18)

        y -= 36

    # Capabilities preview
    y -= 0.2*inch
    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.8*inch, y, "CAPABILITIES")
    c.rect(0.8*inch, y - 4, 1*inch, 2, fill=1)

    y -= 0.35*inch
    caps = [
        ("Wi-Fi Research", "802.11 frame capture, deauth monitoring, probe tracking"),
        ("RF24 Spectrum", "ISM band analysis, channel mapping, signal visualization"),
        ("Packet Injection", "Controlled RF transmission for protocol testing"),
        ("BLE Enumeration", "Bluetooth Low Energy device discovery"),
        ("Forensic Capture", "Full PCAP to SD, UTC timestamps, Wireshark export"),
        ("GPIO Events", "Hardware sensors, MQTT/HTTP telemetry"),
    ]

    for name, desc in caps:
        c.setFillColor(LIGHT)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(1.0*inch, y, name)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(2.8*inch, y, desc)
        y -= 16

    # Footer
    c.setStrokeColor(HexColor("#1e1e2a"))
    c.setLineWidth(0.5)
    c.line(0.8*inch, 0.7*inch, W - 0.8*inch, 0.7*inch)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7)
    c.drawString(0.8*inch, 0.5*inch, "github.com/ykrishhh/ESP32-HARNESS")
    c.drawRightString(W - 0.8*inch, 0.5*inch, "Built for the security research community")

    c.showPage()

    # === PAGE 2: Architecture + Flow ===
    c.setFillColor(DARK)
    c.rect(0, 0, W, H, fill=1)
    draw_grid_pattern(c, 0, 0, W, H, spacing=24, color=HexColor("#0f0f18"))

    # Header
    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(0.8*inch, H - 0.8*inch, "SYSTEM ARCHITECTURE")
    c.rect(0.8*inch, H - 0.95*inch, 1.8*inch, 2, fill=1)

    # Architecture as connected blocks with lines
    y = H - 1.5*inch
    blocks = [
        ("ESP32-WROOM-32", "Main controller", True),
        ("Core Framework", "CLI, PCAP Engine, Logger, Config", False),
        ("Wi-Fi Engine", "Scan, Capture, Deauth detect", False),
        ("RF24 Engine", "NRF24L01+ spectrum & injection", False),
        ("BLE Engine", "Device enumeration & scanning", False),
        ("Telemetry Output", "MQTT, HTTP, Serial", False),
    ]

    for name, desc, highlight in blocks:
        # Block
        if highlight:
            c.setFillColor(HexColor("#00d4ff10"))
            c.setStrokeColor(CYAN)
            c.setLineWidth(1)
        else:
            c.setFillColor(DARK3)
            c.setStrokeColor(HexColor("#1e1e2a"))
            c.setLineWidth(0.5)

        c.roundRect(0.8*inch, y - 6, 5.6*inch, 40, 4, fill=1, stroke=1)

        # Connection line
        if not highlight:
            c.setStrokeColor(HexColor("#00d4ff30"))
            c.setLineWidth(0.5)
            c.line(0.8*inch, y + 34, 0.8*inch, y + 40)

        c.setFillColor(CYAN if highlight else LIGHT)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1.1*inch, y + 10, name)

        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(1.1*inch, y, desc)

        y -= 52

    # Right column: usage flow
    y = H - 1.5*inch
    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(7*inch, y, "USAGE FLOW")

    y -= 0.4*inch
    flow = [
        ("01", "Flash firmware to ESP32-WROOM-32"),
        ("02", "Load config (Wi-Fi / RF24 / BLE / Telemetry)"),
        ("03", "Select target network or device"),
        ("04", "Capture packets to MicroSD"),
        ("05", "Export PCAP for Wireshark analysis"),
    ]

    for num, step in flow:
        # Number circle
        c.setFillColor(CYAN)
        c.circle(7.3*inch, y + 4, 10, fill=1)
        c.setFillColor(DARK)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(7.3*inch, y + 1, num)

        # Step text
        c.setFillColor(LIGHT)
        c.setFont("Helvetica", 9)
        c.drawString(7.6*inch, y, step)

        # Connecting line
        c.setStrokeColor(HexColor("#00d4ff30"))
        c.setLineWidth(0.5)
        c.line(7.3*inch, y - 6, 7.3*inch, y - 16)

        y -= 32

    # Bottom: component table
    y = 3.5*inch
    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.8*inch, y, "COMPONENT MATRIX")
    c.rect(0.8*inch, y - 4, 1.4*inch, 2, fill=1)

    y -= 0.3*inch
    table = [
        ("COMPONENT", "INTERFACE", "PROTOCOL"),
        ("ESP32-WROOM-32", "UART / USB", "Serial 115200"),
        ("NRF24L01+ PA/LNA", "SPI", "SPI 10 MHz"),
        ("MicroSD Module", "SPI", "SPI 25 MHz"),
        ("OLED SSD1306", "I2C", "I2C 400 kHz"),
        ("LiPo Battery", "ADC", "3.7V nominal"),
    ]

    col_x = [0.8*inch, 2.8*inch, 4.5*inch]
    for i, (c1, c2, c3) in enumerate(table):
        if i == 0:
            c.setFillColor(CYAN)
            c.setFont("Helvetica-Bold", 8)
        else:
            c.setFillColor(LIGHT if i % 2 == 1 else MUTED)
            c.setFont("Helvetica", 8)

        c.drawString(col_x[0], y, c1)
        c.drawString(col_x[1], y, c2)
        c.drawString(col_x[2], y, c3)

        if i == 0:
            c.setStrokeColor(CYAN)
            c.setLineWidth(0.5)
            c.line(0.8*inch, y - 6, 6*inch, y - 6)

        y -= 16

    # Footer
    c.setStrokeColor(HexColor("#1e1e2a"))
    c.setLineWidth(0.5)
    c.line(0.8*inch, 0.7*inch, W - 0.8*inch, 0.7*inch)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7)
    c.drawString(0.8*inch, 0.5*inch, "ESP32-HARNESS Datasheet v1.0")
    c.drawRightString(W - 0.8*inch, 0.5*inch, "MIT License")

    c.showPage()
    c.save()
    print(f"PDF: {path} ({os.path.getsize(path)} bytes)")


# === SVG Logo — Circuit board style ===
def build_logo():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 180">
  <defs>
    <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#00d4ff;stop-opacity:0.15"/>
      <stop offset="100%" style="stop-color:#00d4ff;stop-opacity:0"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <!-- Background -->
  <rect width="600" height="180" rx="6" fill="#0a0a0f"/>
  <rect width="600" height="180" rx="6" fill="url(#g1)"/>
  <rect x="1" y="1" width="598" height="178" rx="5" stroke="#1e1e2a" stroke-width="1" fill="none"/>
  <!-- Circuit traces -->
  <g stroke="#00d4ff" stroke-width="0.8" opacity="0.2" fill="none">
    <path d="M480,20 L520,20 L520,50 L560,50"/>
    <path d="M480,40 L500,40 L500,70 L540,70"/>
    <path d="M500,90 L540,90 L540,120 L580,120"/>
    <circle cx="560" cy="50" r="3" fill="#00d4ff" opacity="0.3"/>
    <circle cx="540" cy="70" r="3" fill="#00d4ff" opacity="0.3"/>
    <circle cx="580" cy="120" r="3" fill="#00d4ff" opacity="0.3"/>
  </g>
  <!-- Main text -->
  <text x="30" y="80" font-family="'Share Tech Mono',monospace" font-size="48" font-weight="bold" fill="#00d4ff" filter="url(#glow)">ESP32</text>
  <text x="230" y="80" font-family="'Share Tech Mono',monospace" font-size="48" font-weight="bold" fill="#e8e8ed">-HARNESS</text>
  <!-- Accent line -->
  <rect x="30" y="95" width="60" height="2" rx="1" fill="#00d4ff"/>
  <!-- Subtitle -->
  <text x="30" y="120" font-family="'Share Tech Mono',monospace" font-size="12" fill="#6b6b7b" letter-spacing="3">PENTESTING  AUDIT  TELEMETRY</text>
  <!-- Version + license -->
  <text x="30" y="150" font-family="'Share Tech Mono',monospace" font-size="10" fill="#6b6b7b">v1.0</text>
  <text x="80" y="150" font-family="'Share Tech Mono',monospace" font-size="10" fill="#28c840">MIT</text>
  <text x="120" y="150" font-family="'Share Tech Mono',monospace" font-size="10" fill="#6b6b7b">ESP32-WROOM-32</text>
</svg>"""
    path = os.path.join(ASSETS, "esp32-harness-logo.svg")
    with open(path, "w") as f:
        f.write(svg)
    print(f"Logo: {path} ({len(svg)} bytes)")


# === OG Image — Wide format for social ===
def build_og():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0a0a0f"/>
      <stop offset="100%" style="stop-color:#0f1218"/>
    </linearGradient>
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#00d4ff;stop-opacity:0.2"/>
      <stop offset="100%" style="stop-color:#00d4ff;stop-opacity:0"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <rect width="1200" height="630" fill="url(#accent)"/>
  <rect x="40" y="40" width="1120" height="550" rx="8" stroke="#1e1e2a" stroke-width="1" fill="none"/>
  <!-- Grid pattern -->
  <g stroke="#1e1e2a" stroke-width="0.3" opacity="0.4">
    <line x1="200" y1="40" x2="200" y2="590"/>
    <line x1="400" y1="40" x2="400" y2="590"/>
    <line x1="600" y1="40" x2="600" y2="590"/>
    <line x1="800" y1="40" x2="800" y2="590"/>
    <line x1="1000" y1="40" x2="1000" y2="590"/>
    <line x1="40" y1="150" x2="1160" y2="150"/>
    <line x1="40" y1="300" x2="1160" y2="300"/>
    <line x1="40" y1="450" x2="1160" y2="450"/>
  </g>
  <!-- Circuit traces right side -->
  <g stroke="#00d4ff" stroke-width="1" opacity="0.15" fill="none">
    <path d="M800,100 L900,100 L900,180 L1000,180 L1000,250"/>
    <path d="M850,200 L950,200 L950,300 L1050,300"/>
    <path d="M900,350 L1000,350 L1000,420 L1100,420"/>
    <circle cx="1000" cy="250" r="4" fill="#00d4ff" opacity="0.3"/>
    <circle cx="1050" cy="300" r="4" fill="#00d4ff" opacity="0.3"/>
    <circle cx="1100" cy="420" r="4" fill="#00d4ff" opacity="0.3"/>
  </g>
  <!-- Title -->
  <text x="80" y="220" font-family="'Share Tech Mono',monospace" font-size="96" font-weight="bold" fill="#00d4ff" filter="url(#glow)">ESP32</text>
  <text x="480" y="220" font-family="'Share Tech Mono',monospace" font-size="96" font-weight="bold" fill="#e8e8ed">-HARNESS</text>
  <!-- Accent bar -->
  <rect x="80" y="245" width="100" height="4" rx="2" fill="#00d4ff"/>
  <!-- Subtitle -->
  <text x="80" y="290" font-family="'Share Tech Mono',monospace" font-size="22" fill="#6b6b7b" letter-spacing="4">PENTESTING, AUDIT &amp; TELEMETRY FIRMWARE</text>
  <!-- Features line -->
  <text x="80" y="340" font-family="'Share Tech Mono',monospace" font-size="16" fill="#6b6b7b">2.4 GHz Research  |  NRF24L01+  |  BLE 5.0  |  Forensic Capture</text>
  <!-- GitHub -->
  <text x="80" y="400" font-family="'Share Tech Mono',monospace" font-size="18" fill="#28c840">github.com/ykrishhh/ESP32-HARNESS</text>
  <!-- Bottom bar -->
  <text x="80" y="520" font-family="'Share Tech Mono',monospace" font-size="14" fill="#6b6b7b">ESP32-WROOM-32  |  MIT License  |  Open Source</text>
  <rect x="80" y="540" width="80" height="3" rx="1" fill="#00d4ff" opacity="0.5"/>
</svg>"""
    path = os.path.join(ASSETS, "og-image.svg")
    with open(path, "w") as f:
        f.write(svg)
    print(f"OG: {path} ({len(svg)} bytes)")


# === Banner — For README header ===
def build_banner():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 200">
  <defs>
    <linearGradient id="bg2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#0a0a0f"/>
      <stop offset="100%" style="stop-color:#111118"/>
    </linearGradient>
    <filter id="glow2">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="800" height="200" rx="6" fill="url(#bg2)"/>
  <rect width="800" height="200" rx="6" stroke="#1e1e2a" stroke-width="1" fill="none"/>
  <!-- Circuit decoration -->
  <g stroke="#00d4ff" stroke-width="0.6" opacity="0.15" fill="none">
    <path d="M600,30 L650,30 L650,60 L700,60 L700,90"/>
    <path d="M620,50 L670,50 L670,80 L720,80"/>
    <path d="M640,70 L690,70 L690,110 L740,110"/>
    <circle cx="700" cy="90" r="3" fill="#00d4ff" opacity="0.3"/>
    <circle cx="720" cy="80" r="3" fill="#00d4ff" opacity="0.3"/>
    <circle cx="740" cy="110" r="3" fill="#00d4ff" opacity="0.3"/>
  </g>
  <!-- Title -->
  <text x="40" y="100" font-family="'Share Tech Mono',monospace" font-size="42" font-weight="bold" fill="#00d4ff" filter="url(#glow2)">ESP32</text>
  <text x="210" y="100" font-family="'Share Tech Mono',monospace" font-size="42" font-weight="bold" fill="#e8e8ed">-HARNESS</text>
  <!-- Accent -->
  <rect x="40" y="115" width="50" height="2" rx="1" fill="#00d4ff"/>
  <!-- Subtitle -->
  <text x="40" y="145" font-family="'Share Tech Mono',monospace" font-size="12" fill="#6b6b7b" letter-spacing="2">PENTESTING &amp; TELEMETRY FIRMWARE</text>
  <!-- Stats -->
  <text x="40" y="175" font-family="'Share Tech Mono',monospace" font-size="10" fill="#28c840">3 Radios</text>
  <text x="130" y="175" font-family="'Share Tech Mono',monospace" font-size="10" fill="#6b6b7b">|</text>
  <text x="150" y="175" font-family="'Share Tech Mono',monospace" font-size="10" fill="#28c840">7 Modes</text>
  <text x="230" y="175" font-family="'Share Tech Mono',monospace" font-size="10" fill="#6b6b7b">|</text>
  <text x="250" y="175" font-family="'Share Tech Mono',monospace" font-size="10" fill="#28c840">$5 Hardware</text>
  <text x="370" y="175" font-family="'Share Tech Mono',monospace" font-size="10" fill="#6b6b7b">|</text>
  <text x="390" y="175" font-family="'Share Tech Mono',monospace" font-size="10" fill="#28c840">MIT</text>
</svg>"""
    path = os.path.join(ASSETS, "banner.svg")
    with open(path, "w") as f:
        f.write(svg)
    print(f"Banner: {path} ({len(svg)} bytes)")


if __name__ == "__main__":
    build_pdf()
    build_logo()
    build_og()
    build_banner()
    print("\nAll v2 assets generated.")
