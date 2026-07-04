#!/usr/bin/env python3
"""Generate ESP32-HARNESS datasheet PDF using reportlab canvas (no PIL dependency)."""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

CYAN = HexColor("#00d4ff")
DARK = HexColor("#0a0a0f")
MUTED = HexColor("#6b6b7b")
LIGHT = HexColor("#e8e8ed")
BG = HexColor("#f5f5f5")
WHITE = white

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ESP32-HARNESS-Datasheet.pdf")

W, H = letter

def draw(c):
    # Page 1 - Cover
    c.setFillColor(DARK)
    c.rect(0, 0, W, H, fill=1)

    # Cyan accent bar
    c.setFillColor(CYAN)
    c.rect(0.8*inch, H - 1.2*inch, 3*inch, 3, fill=1)

    # Title
    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 36)
    c.drawString(0.8*inch, H - 1.6*inch, "ESP32-HARNESS")

    c.setFillColor(LIGHT)
    c.setFont("Helvetica", 14)
    c.drawString(0.8*inch, H - 2.0*inch, "Advanced ESP32 Pentesting, Audit & Telemetry Firmware")

    # Specs box
    y = H - 2.8*inch
    specs = [
        ("Controller", "ESP32-WROOM-32 (Dual-core 240 MHz)"),
        ("RF Transceiver", "NRF24L01+ PA/LNA (2.4 GHz ISM)"),
        ("Storage", "MicroSD (FAT32/exFAT, up to 32 GB)"),
        ("Display", "OLED SSD1306 (128x64, I2C)"),
        ("Battery", "LiPo 3.7V 1000mAh, ~4 hours"),
        ("License", "MIT"),
    ]

    c.setStrokeColor(HexColor("#1e1e2a"))
    c.setLineWidth(0.5)
    for label, val in specs:
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 9)
        c.drawString(0.8*inch, y, label.upper())
        c.setFillColor(LIGHT)
        c.setFont("Helvetica", 11)
        c.drawString(2.4*inch, y, val)
        c.setStrokeColor(HexColor("#1e1e2a"))
        c.line(0.8*inch, y - 6, 6*inch, y - 6)
        y -= 28

    # Capabilities
    y -= 0.3*inch
    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.8*inch, y, "Capabilities")
    y -= 0.3*inch

    caps = [
        "2.4 GHz Wi-Fi Research - Passive/active wireless recon, 802.11 frame capture",
        "NRF24L01+ Integration - ISM band spectrum analysis, channel mapping",
        "Packet Injection - Controlled RF transmission for protocol testing",
        "BLE Enumeration - Bluetooth Low Energy device discovery",
        "Deauth Detection - Real-time deauth/disassoc attack monitoring",
        "Forensic Capture - Full PCAP to SD, UTC timestamps, Wireshark export",
        "GPIO Events - Hardware sensors, MQTT/HTTP telemetry, OLED display",
    ]
    for cap in caps:
        c.setFillColor(LIGHT)
        c.setFont("Helvetica", 9)
        c.drawString(1.0*inch, y, cap)
        y -= 16

    # Footer
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(0.8*inch, 0.5*inch, "github.com/ykrishhh/ESP32-HARNESS  |  MIT License  |  Built for the security research community")

    c.showPage()

    # Page 2 - Architecture
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, fill=1)

    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(0.8*inch, H - 1*inch, "Architecture")

    c.setFillColor(CYAN)
    c.rect(0.8*inch, H - 1.15*inch, 1.5*inch, 2, fill=1)

    # Architecture blocks
    y = H - 1.8*inch
    blocks = [
        ("ESP32-WROOM-32", "Main controller"),
        ("Core Framework", "CLI, PCAP Engine, Logger, Config"),
        ("Wi-Fi Engine", "Scan, Capture, Deauth detect"),
        ("RF24 Engine", "NRF24L01+ spectrum & injection"),
        ("BLE Engine", "Device enumeration & scanning"),
        ("Telemetry Output", "MQTT, HTTP, Serial"),
        ("MicroSD Card", "PCAP storage & logs"),
        ("OLED Display", "SSD1306 status UI"),
        ("GPIO Triggers", "Hardware sensor integration"),
    ]

    for name, desc in blocks:
        # Block background
        c.setFillColor(BG)
        c.roundRect(0.8*inch, y - 8, 5.6*inch, 36, 3, fill=1)

        c.setFillColor(DARK)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1.0*inch, y + 10, name)

        c.setFillColor(MUTED)
        c.setFont("Helvetica", 9)
        c.drawString(1.0*inch, y - 2, desc)

        y -= 48

    # Usage Flow
    y -= 0.3*inch
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(0.8*inch, y, "Usage Flow")

    y -= 0.4*inch
    flow = [
        "1. Flash firmware to ESP32-WROOM-32",
        "2. Load configuration (Wi-Fi, RF24, BLE, or Telemetry mode)",
        "3. Select target network or device",
        "4. Capture packets to MicroSD",
        "5. Export PCAP for Wireshark analysis",
    ]
    for step in flow:
        c.setFillColor(DARK)
        c.setFont("Courier", 10)
        c.drawString(1.0*inch, y, step)
        y -= 20

    # Legal
    y -= 0.4*inch
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(0.8*inch, y, "This tool is designed exclusively for authorized security testing, educational purposes,")
    c.drawString(0.8*inch, y - 12, "and legitimate RF research. Users are responsible for compliance with local laws.")

    c.showPage()
    c.save()

c = canvas.Canvas(OUT, pagesize=letter)
draw(c)
print(f"PDF: {OUT} ({os.path.getsize(OUT)} bytes)")
