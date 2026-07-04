#!/usr/bin/env python3
"""Generate PDF document and SVG logo for ESP32-HARNESS."""
import os

# --- PDF Generation ---
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

CYAN = HexColor("#00d4ff")
DARK = HexColor("#0a0a0f")
MUTED = HexColor("#6b6b7b")

def build_pdf():
    path = os.path.join(OUT_DIR, "ESP32-HARNESS-Datasheet.pdf")
    doc = SimpleDocTemplate(path, pagesize=letter,
                            topMargin=0.6*inch, bottomMargin=0.6*inch,
                            leftMargin=0.8*inch, rightMargin=0.8*inch)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("Title2", parent=styles["Title"],
                                  fontSize=28, textColor=CYAN, spaceAfter=6,
                                  fontName="Helvetica-Bold")
    h2 = ParagraphStyle("H2", parent=styles["Heading2"],
                         fontSize=16, textColor=DARK, spaceBefore=18, spaceAfter=8,
                         fontName="Helvetica-Bold")
    body = ParagraphStyle("Body2", parent=styles["Normal"],
                           fontSize=10, leading=15, textColor=DARK)
    mono = ParagraphStyle("Mono", parent=body,
                           fontName="Courier", fontSize=9, leading=13)
    small = ParagraphStyle("Small", parent=body, fontSize=8, textColor=MUTED)

    story = []

    # Title
    story.append(Paragraph("ESP32-HARNESS", title_style))
    story.append(Paragraph("Advanced ESP32 Pentesting, Audit &amp; Telemetry Firmware", body))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1, color=CYAN))
    story.append(Spacer(1, 12))

    # Overview
    story.append(Paragraph("Overview", h2))
    story.append(Paragraph(
        "ESP32-HARNESS transforms the ESP32 into a portable, self-contained security research platform. "
        "Built for authorized penetration testing, security auditing, and RF telemetry, it consolidates "
        "multiple hardware tools into a single firmware running on a $5 microcontroller.", body))
    story.append(Spacer(1, 12))

    # Key Specs Table
    story.append(Paragraph("Key Specifications", h2))
    spec_data = [
        ["Component", "Specification"],
        ["Controller", "ESP32-WROOM-32 (Dual-core 240 MHz, Wi-Fi + BLE, 520 KB SRAM)"],
        ["RF Transceiver", "NRF24L01+ PA/LNA (2.4 GHz ISM, +20 dBm, 250 kbps - 2 Mbps)"],
        ["Storage", "MicroSD Module (FAT32/exFAT, SPI, up to 32 GB)"],
        ["Display", "OLED SSD1306 (128x64, I2C)"],
        ["Battery", "LiPo 3.7V 1000mAh, USB-C charging, ~4 hours runtime"],
        ["Development", "Arduino IDE / PlatformIO"],
        ["License", "MIT"],
    ]
    t = Table(spec_data, colWidths=[1.6*inch, 4.8*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), CYAN),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("LEADING", (0, 0), (-1, -1), 13),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#dddddd")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f8f8f8"), HexColor("#ffffff")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 18))

    # Capabilities
    story.append(Paragraph("Capabilities", h2))
    caps = [
        ("<b>2.4 GHz Wi-Fi Research</b> - Passive/active wireless recon, raw 802.11 frame capture (PCAP export), deauth monitoring, probe request tracking.",),
        ("<b>NRF24L01+ Integration</b> - ISM band spectrum analysis, channel utilization mapping, signal strength visualization.",),
        ("<b>Packet Injection</b> - Controlled RF packet transmission for protocol resilience testing.",),
        ("<b>BLE Enumeration</b> - Bluetooth Low Energy device discovery and advertisement analysis.",),
        ("<b>Deauthentication Detection</b> - Real-time monitoring for deauth/disassoc attacks.",),
        ("<b>Forensic Capture</b> - Full packet capture to SD/SPIFFS, UTC-timestamped logs, Wireshark export, hash-verified integrity.",),
        ("<b>GPIO-Triggered Events</b> - Hardware sensor integration, MQTT/HTTP telemetry, OLED status display.",),
    ]
    for c in caps:
        story.append(Paragraph(c[0], body))
        story.append(Spacer(1, 4))
    story.append(Spacer(1, 12))

    # Architecture
    story.append(Paragraph("Architecture", h2))
    story.append(Paragraph(
        "The firmware is organized into modular engines: Core Framework (CLI, PCAP Engine, Logger, Config), "
        "Wi-Fi Engine (Scan, Capture, Deauth detect), RF24 Engine (NRF24L01+ spectrum &amp; injection), "
        "BLE Engine (Device enumeration &amp; scanning), and Telemetry Output (MQTT, HTTP, Serial). "
        "Storage is handled by MicroSD Card and SPIFFS. The OLED Display provides real-time status via SSD1306.",
        body))
    story.append(Spacer(1, 12))

    # Hardware Requirements
    story.append(Paragraph("Hardware Bill of Materials", h2))
    bom_data = [
        ["Component", "Purpose", "Required?"],
        ["ESP32-WROOM-32", "Main controller", "Yes"],
        ["NRF24L01+ PA/LNA", "2.4 GHz RF transceiver", "Optional"],
        ["MicroSD Module", "Capture storage", "Optional"],
        ["OLED SSD1306", "Status display", "Optional"],
        ["LiPo Battery", "Portable operation", "Optional"],
    ]
    t2 = Table(bom_data, colWidths=[2.0*inch, 3.0*inch, 1.2*inch])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), CYAN),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("LEADING", (0, 0), (-1, -1), 13),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#dddddd")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f8f8f8"), HexColor("#ffffff")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t2)
    story.append(Spacer(1, 18))

    # Usage Flow
    story.append(Paragraph("Usage Flow", h2))
    flow = [
        "1. Flash firmware to ESP32-WROOM-32",
        "2. Load configuration (Wi-Fi scan, RF24, BLE, or Telemetry mode)",
        "3. Select target network or device",
        "4. Capture packets to MicroSD",
        "5. Export PCAP for Wireshark analysis",
    ]
    for f in flow:
        story.append(Paragraph(f, mono))
        story.append(Spacer(1, 2))
    story.append(Spacer(1, 18))

    # Legal
    story.append(Paragraph("Legal Notice", h2))
    story.append(Paragraph(
        "This tool is designed exclusively for authorized security testing, educational purposes, "
        "and legitimate RF research. Users are responsible for compliance with local laws and regulations.",
        small))
    story.append(Spacer(1, 24))

    # Footer
    story.append(HRFlowable(width="100%", thickness=0.5, color=MUTED))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "github.com/ykrishhh/ESP32-HARNESS | MIT License | Built for the security research community",
        small))

    doc.build(story)
    print(f"PDF generated: {path} ({os.path.getsize(path)} bytes)")


# --- SVG Logo ---
def build_svg():
    path = os.path.join(OUT_DIR, "assets")
    os.makedirs(path, exist_ok=True)
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 120" fill="none">
  <rect width="400" height="120" rx="4" fill="#0a0a0f"/>
  <rect x="1" y="1" width="398" height="118" rx="3" stroke="#1e1e2a" stroke-width="1"/>
  <text x="24" y="52" font-family="monospace" font-size="28" font-weight="bold" fill="#00d4ff">ESP32</text>
  <text x="148" y="52" font-family="monospace" font-size="28" font-weight="bold" fill="#e8e8ed">-HARNESS</text>
  <text x="24" y="78" font-family="monospace" font-size="11" fill="#6b6b7b" letter-spacing="1.5">PENTESTING &amp; TELEMETRY FIRMWARE</text>
  <rect x="24" y="92" width="48" height="2" rx="1" fill="#00d4ff"/>
  <text x="290" y="52" font-family="monospace" font-size="10" fill="#6b6b7b">v1.0</text>
  <text x="290" y="72" font-family="monospace" font-size="10" fill="#28c840">MIT</text>
</svg>"""
    svg_path = os.path.join(path, "esp32-harness-logo.svg")
    with open(svg_path, "w") as f:
        f.write(svg)
    print(f"SVG logo: {svg_path}")

    # OG image SVG
    og = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" fill="none">
  <rect width="1200" height="630" fill="#0a0a0f"/>
  <rect x="40" y="40" width="1120" height="550" rx="8" stroke="#1e1e2a" stroke-width="1"/>
  <text x="80" y="200" font-family="monospace" font-size="72" font-weight="bold" fill="#00d4ff">ESP32</text>
  <text x="420" y="200" font-family="monospace" font-size="72" font-weight="bold" fill="#e8e8ed">-HARNESS</text>
  <text x="80" y="280" font-family="monospace" font-size="24" fill="#6b6b7b" letter-spacing="2">PENTESTING, AUDIT &amp; TELEMETRY FIRMWARE</text>
  <rect x="80" y="320" width="80" height="3" rx="1" fill="#00d4ff"/>
  <text x="80" y="380" font-family="monospace" font-size="18" fill="#6b6b7b">2.4 GHz Research | NRF24L01+ | BLE 5.0 | Forensic Capture</text>
  <text x="80" y="440" font-family="monospace" font-size="16" fill="#28c840">github.com/ykrishhh/ESP32-HARNESS</text>
  <text x="80" y="520" font-family="monospace" font-size="14" fill="#6b6b7b">ESP32-WROOM-32 | MIT License | Open Source</text>
</svg>"""
    og_path = os.path.join(path, "og-image.svg")
    with open(og_path, "w") as f:
        f.write(og)
    print(f"OG image: {og_path}")


if __name__ == "__main__":
    build_pdf()
    build_svg()
    print("All assets generated.")
