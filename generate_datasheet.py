#!/usr/bin/env python3
"""ESP32-HARNESS High-End Visual Datasheet Generator"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import math, os

W, H = A4
OUT = os.path.join(os.path.dirname(__file__), 'ESP32-HARNESS-Datasheet-v2.pdf')

# Colors
BG = HexColor('#04040a')
S1 = HexColor('#080814')
S2 = HexColor('#0d0d1e')
S3 = HexColor('#141428')
BD = HexColor('#1a1a32')
BDB = HexColor('#26264a')
CYAN = HexColor('#00d4ff')
CYAN_DIM = HexColor('#00d4ff')
VIOLET = HexColor('#7c3aed')
VIOLET_B = HexColor('#a855f7')
GREEN = HexColor('#00ff88')
AMBER = HexColor('#f59e0b')
RED = HexColor('#ef4444')
TX = HexColor('#e8e8ff')
T2 = HexColor('#7070a0')
T3 = HexColor('#3a3a60')
T4 = HexColor('#1e1e38')
WHITE = HexColor('#ffffff')

def draw_bg(c, page_num=0):
    """Dark background with subtle grid"""
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Grid lines
    c.setStrokeColor(HexColor('#0a0a1a'))
    c.setLineWidth(0.3)
    for x in range(0, int(W), 20):
        c.line(x, 0, x, H)
    for y in range(0, int(H), 20):
        c.line(0, y, W, y)
    # Top accent line
    c.setStrokeColor(CYAN)
    c.setLineWidth(2)
    c.line(0, H - 2, W, H - 2)
    # Corner accents
    c.setStrokeColor(CYAN)
    c.setLineWidth(1)
    c.line(0, H - 30, 30, H - 30)
    c.line(30, H, 30, H - 30)
    c.line(W - 30, 0, W - 30, 30)
    c.line(W, 30, W - 30, 30)

def draw_chip(c, x, y, w, h, color=CYAN, label='', sublabel=''):
    """Draw a styled chip/badge"""
    c.setFillColor(Color(color.red, color.green, color.blue, 0.12))
    c.setStrokeColor(Color(color.red, color.green, color.blue, 0.4))
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, 4, fill=1, stroke=1)
    if label:
        c.setFillColor(color)
        c.setFont('Helvetica-Bold', 8)
        c.drawCentredString(x + w/2, y + h/2 + (3 if sublabel else 0), label)
    if sublabel:
        c.setFillColor(T2)
        c.setFont('Helvetica', 6)
        c.drawCentredString(x + w/2, y + h/2 - 8, sublabel)

def draw_glow_circle(c, x, y, r, color=CYAN, alpha=0.15):
    """Draw a glow effect circle"""
    for i in range(5, 0, -1):
        a = alpha * (i / 5) * 0.3
        c.setFillColor(Color(color.red, color.green, color.blue, a))
        c.circle(x, y, r + i * 8, fill=1, stroke=0)

def draw_page1_cover(c):
    """Cover page"""
    draw_bg(c, 0)
    
    # Large glow orbs
    draw_glow_circle(c, W * 0.3, H * 0.7, 120, CYAN, 0.08)
    draw_glow_circle(c, W * 0.75, H * 0.25, 100, VIOLET, 0.06)
    
    # Top bar
    c.setFillColor(T3)
    c.setFont('Helvetica', 8)
    c.drawString(30, H - 45, 'ESP32-HARNESS')
    c.setFillColor(T3)
    c.drawRightString(W - 30, H - 45, 'v1.0  |  MIT License')
    
    # Main title area
    y = H - 140
    
    # ESP32 chip badge
    draw_chip(c, 30, y + 10, 60, 22, AMBER, 'ESP32', 'v1.0')
    draw_chip(c, 100, y + 10, 80, 22, GREEN, 'MIT', 'License')
    
    y -= 40
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 52)
    c.drawString(30, y, 'ESP32')
    y -= 55
    c.setFillColor(CYAN)
    c.setFont('Helvetica-Bold', 52)
    c.drawString(30, y, 'HARNESS')
    
    y -= 35
    c.setFillColor(T2)
    c.setFont('Helvetica', 13)
    c.drawString(30, y, 'Advanced Pentesting, Audit & Telemetry Firmware')
    
    y -= 20
    c.setFillColor(T3)
    c.setFont('Helvetica', 10)
    c.drawString(30, y, '2.4 GHz Research  |  RF24 Experimentation  |  BLE Scanning  |  Forensic Capture')
    
    # Feature chips
    y -= 50
    chips = [
        ('2.4 GHz', 'Wi-Fi Engine', CYAN),
        ('RF24', 'NRF24L01+', VIOLET_B),
        ('BLE', 'Bluetooth', GREEN),
        ('PCAP', 'Forensic', AMBER),
        ('MQTT', 'Telemetry', RED),
        ('GPIO', 'Hardware', CYAN),
    ]
    x = 30
    for label, sub, color in chips:
        cw = 72
        draw_chip(c, x, y, cw, 36, color, label, sub)
        x += cw + 8
    
    # Hardware spec boxes
    y -= 70
    c.setFillColor(T3)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(30, y + 5, '// HARDWARE SPECIFICATIONS')
    
    y -= 25
    specs = [
        ('ESP32-WROOM-32', 'Dual-core 240 MHz', '520 KB SRAM', CYAN),
        ('NRF24L01+ PA/LNA', '2.4 GHz ISM', '+20 dBm', VIOLET_B),
        ('MicroSD Module', 'FAT32/exFAT', 'Up to 32 GB', GREEN),
        ('SSD1306 OLED', '128x64 Mono', 'I2C 400kHz', AMBER),
        ('LiPo 3.7V', '1000mAh', '~4 hrs runtime', RED),
    ]
    x = 30
    bw = (W - 60 - 40) / 5
    for name, spec1, spec2, color in specs:
        # Box
        c.setFillColor(Color(color.red, color.green, color.blue, 0.06))
        c.setStrokeColor(Color(color.red, color.green, color.blue, 0.25))
        c.setLineWidth(0.8)
        c.roundRect(x, y, bw, 65, 6, fill=1, stroke=1)
        # Top accent
        c.setStrokeColor(color)
        c.setLineWidth(2)
        c.line(x + 2, y + 65, x + bw - 2, y + 65)
        # Text
        c.setFillColor(color)
        c.setFont('Helvetica-Bold', 8)
        c.drawString(x + 6, y + 48, name)
        c.setFillColor(T2)
        c.setFont('Helvetica', 7)
        c.drawString(x + 6, y + 33, spec1)
        c.drawString(x + 6, y + 20, spec2)
        x += bw + 8
    
    # Capabilities section
    y -= 100
    c.setFillColor(T3)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(30, y + 5, '// CAPABILITIES')
    
    y -= 20
    caps = [
        ('Wi-Fi Research', '802.11 frame capture, deauth monitoring, probe tracking', CYAN),
        ('RF24 Spectrum', 'ISM band analysis, channel mapping, signal visualization', VIOLET_B),
        ('Packet Injection', 'Controlled RF transmission for protocol testing', GREEN),
        ('BLE Enumeration', 'Bluetooth Low Energy device discovery & RSSI tracking', AMBER),
        ('Forensic Capture', 'Full PCAP to SD, UTC timestamps, Wireshark export', RED),
        ('GPIO Events', 'Hardware sensors, MQTT/HTTP telemetry output', CYAN),
    ]
    for i, (name, desc, color) in enumerate(caps):
        col = i % 2
        row = i // 2
        cx = 30 + col * (W/2 - 30)
        cy = y - row * 38
        # Dot
        c.setFillColor(color)
        c.circle(cx + 4, cy + 4, 3, fill=1, stroke=0)
        # Name
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(cx + 14, cy + 2, name)
        # Desc
        c.setFillColor(T2)
        c.setFont('Helvetica', 7)
        c.drawString(cx + 14, cy - 10, desc)
    
    # Footer
    c.setFillColor(T4)
    c.rect(0, 0, W, 30, fill=1, stroke=0)
    c.setFillColor(T3)
    c.setFont('Helvetica', 7)
    c.drawString(30, 11, 'github.com/ykrishhh/ESP32-HARNESS')
    c.drawRightString(W - 30, 11, 'Built for authorized security research only')
    c.setFillColor(CYAN)
    c.setFont('Helvetica-Bold', 7)
    c.drawCentredString(W/2, 11, 'ESP32-HARNESS Datasheet v1.0')

def draw_page2_features(c):
    """Features & Architecture page"""
    draw_bg(c, 1)
    
    y = H - 50
    c.setFillColor(T3)
    c.setFont('Helvetica', 8)
    c.drawString(30, y, 'ESP32-HARNESS  |  Features & Architecture')
    c.setFillColor(T3)
    c.drawRightString(W - 30, y, '2 / 3')
    
    y -= 40
    c.setFillColor(CYAN)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(30, y, '// PLANNED_CAPABILITIES')
    
    y -= 25
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 24)
    c.drawString(30, y, 'Firmware ')
    c.setFillColor(CYAN)
    c.drawString(30 + c.stringWidth('Firmware ', 'Helvetica-Bold', 24), y, 'Features')
    
    y -= 18
    c.setFillColor(T2)
    c.setFont('Helvetica', 10)
    c.drawString(30, y, 'Four research domains consolidated into one $5 microcontroller firmware.')
    
    # Feature cards - 2 columns
    y -= 35
    features = [
        ('Wi-Fi Engine', '2.4 GHz', [
            'Passive Wi-Fi scanning & SSID enumeration',
            'Raw 802.11 packet capture (PCAP)',
            'Deauth attack detection & alerting',
            'Probe request tracking & device fingerprinting',
        ], CYAN),
        ('RF24 / NRF24L01+ Engine', '2.4 GHz ISM', [
            'Channel utilization & signal strength mapping',
            'Controlled RF packet injection for testing',
            'BLE & proprietary frequency hopping analysis',
            'Spectrum sweep across all 128 channels',
        ], VIOLET_B),
        ('Bluetooth / BLE Engine', 'BLE 4.0+', [
            'BLE device discovery & RSSI tracking',
            'Advertisement packet analysis & parsing',
            'Service & characteristic enumeration',
            'Classic BT device scanning',
        ], GREEN),
        ('On-Device Forensic Capture', 'SD / SPIFFS', [
            'Full PCAP recording to SD / SPIFFS',
            'UTC-synchronized event logging',
            'SHA-256 hash chain of custody',
            'Direct Wireshark-compatible export',
        ], AMBER),
        ('Network Enumeration', 'Discovery', [
            'mDNS / SSDP device discovery',
            'Service fingerprinting via banner grab',
            'ARP-based host enumeration',
            'HTTP/MQTT client for remote reporting',
        ], RED),
        ('Remote Telemetry Output', 'MQTT / HTTP', [
            'MQTT broker publish with TLS support',
            'HTTP POST JSON telemetry',
            'GPIO-triggered hardware sensor events',
            'OLED status display (SSD1306)',
        ], CYAN),
    ]
    
    cw = (W - 60 - 12) / 2
    ch = 105
    for i, (title, badge, items, color) in enumerate(features):
        col = i % 2
        row = i // 2
        cx = 30 + col * (cw + 12)
        cy = y - row * (ch + 12)
        
        # Card background
        c.setFillColor(Color(0.03, 0.03, 0.08, 0.9))
        c.setStrokeColor(Color(color.red, color.green, color.blue, 0.15))
        c.setLineWidth(0.8)
        c.roundRect(cx, cy, cw, ch, 8, fill=1, stroke=1)
        
        # Top accent
        c.setStrokeColor(color)
        c.setLineWidth(2)
        c.line(cx + 2, cy + ch, cx + cw - 2, cy + ch)
        
        # Badge
        c.setFillColor(Color(color.red, color.green, color.blue, 0.12))
        c.roundRect(cx + 10, cy + ch - 22, 60, 16, 3, fill=1, stroke=0)
        c.setFillColor(color)
        c.setFont('Helvetica-Bold', 6)
        c.drawCentredString(cx + 40, cy + ch - 18, badge)
        
        # Title
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(cx + 10, cy + ch - 38, title)
        
        # Items
        c.setFillColor(T2)
        c.setFont('Helvetica', 7)
        for j, item in enumerate(items):
            iy = cy + ch - 52 - j * 13
            c.setFillColor(color)
            c.drawString(cx + 10, iy + 2, '\u2192')
            c.setFillColor(T2)
            c.drawString(cx + 22, iy, item)
    
    # Architecture section
    y_arch = y - 3 * (ch + 12) - 40
    c.setFillColor(T3)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(30, y_arch, '// FIRMWARE_ARCHITECTURE')
    
    y_arch -= 25
    # Architecture boxes
    arch_boxes = [
        # Row 1 - Top
        [('ESP32-HARNESS FIRMWARE', W - 60, 28, Color(0, 0.83, 1, 0.15), Color(0, 0.83, 1, 0.4), WHITE)],
        # Row 2 - Engines
        [('Wi-Fi Engine', (W-80)/4, 22, Color(0, 0.83, 1, 0.08), Color(0, 0.83, 1, 0.25), CYAN),
         ('RF24 Engine', (W-80)/4, 22, Color(0.49, 0.23, 0.93, 0.08), Color(0.49, 0.23, 0.93, 0.25), VIOLET_B),
         ('BLE Engine', (W-80)/4, 22, Color(0, 1, 0.53, 0.08), Color(0, 1, 0.53, 0.25), GREEN),
         ('Telemetry Output', (W-80)/4, 22, Color(0, 0.83, 1, 0.08), Color(0, 0.83, 1, 0.25), CYAN)],
        # Row 3 - Core
        [('Core Framework', (W-80)/3, 22, Color(0, 1, 0.53, 0.08), Color(0, 1, 0.53, 0.25), GREEN),
         ('Task Scheduler', (W-80)/3, 22, Color(0, 1, 0.53, 0.08), Color(0, 1, 0.53, 0.25), GREEN),
         ('Storage Manager', (W-80)/3, 22, Color(0, 1, 0.53, 0.08), Color(0, 1, 0.53, 0.25), GREEN)],
        # Row 4 - HAL
        [('ESP-IDF / Arduino HAL', (W-80)/2, 22, Color(0.96, 0.62, 0.04, 0.08), Color(0.96, 0.62, 0.04, 0.25), AMBER),
         ('FreeRTOS', (W-80)/2, 22, Color(0.96, 0.62, 0.04, 0.08), Color(0.96, 0.62, 0.04, 0.25), AMBER)],
    ]
    
    for row in arch_boxes:
        total_w = sum(b[1] for b in row) + (len(row) - 1) * 8
        start_x = (W - total_w) / 2
        for label, bw, bh, bg_col, border_col, text_col in row:
            c.setFillColor(bg_col)
            c.setStrokeColor(border_col)
            c.setLineWidth(0.8)
            c.roundRect(start_x, y_arch, bw, bh, 4, fill=1, stroke=1)
            c.setFillColor(text_col)
            c.setFont('Helvetica-Bold', 8)
            c.drawCentredString(start_x + bw/2, y_arch + 7, label)
            start_x += bw + 8
        y_arch -= 32
        # Connector line
        c.setStrokeColor(BDB)
        c.setLineWidth(0.5)
        c.line(W/2, y_arch + 28, W/2, y_arch + 8)
    
    # Footer
    c.setFillColor(T4)
    c.rect(0, 0, W, 30, fill=1, stroke=0)
    c.setFillColor(T3)
    c.setFont('Helvetica', 7)
    c.drawString(30, 11, 'github.com/ykrishhh/ESP32-HARNESS')
    c.drawRightString(W - 30, 11, 'Built for authorized security research only')

def draw_page3_setup(c):
    """Quick Start & Hardware page"""
    draw_bg(c, 2)
    
    y = H - 50
    c.setFillColor(T3)
    c.setFont('Helvetica', 8)
    c.drawString(30, y, 'ESP32-HARNESS  |  Quick Start & Hardware')
    c.setFillColor(T3)
    c.drawRightString(W - 30, y, '3 / 3')
    
    y -= 40
    c.setFillColor(CYAN)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(30, y, '// QUICK_START')
    
    y -= 25
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 24)
    c.drawString(30, y, 'Get ')
    c.setFillColor(CYAN)
    c.drawString(30 + c.stringWidth('Get ', 'Helvetica-Bold', 24), y, 'Started')
    
    y -= 18
    c.setFillColor(T2)
    c.setFont('Helvetica', 10)
    c.drawString(30, y, 'From zero to flashing in under 5 minutes.')
    
    # Quick start steps
    y -= 35
    steps = [
        ('01', 'Clone', 'git clone https://github.com/ykrishhh/ESP32-HARNESS.git', CYAN),
        ('02', 'Install', 'pip install platformio && pio pkg install', VIOLET_B),
        ('03', 'Configure', 'Edit config.h — set RF24_ENABLED, SD_ENABLED, MQTT_TELEMETRY', GREEN),
        ('04', 'Flash', 'pio run --target upload', AMBER),
        ('05', 'Monitor', 'pio device monitor --baud 115200', RED),
    ]
    
    for num, label, cmd, color in steps:
        # Step number circle
        c.setFillColor(Color(color.red, color.green, color.blue, 0.15))
        c.circle(48, y + 4, 14, fill=1, stroke=0)
        c.setFillColor(color)
        c.setFont('Helvetica-Bold', 12)
        c.drawCentredString(48, y, num)
        
        # Label
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 11)
        c.drawString(70, y + 2, label)
        
        # Command box
        c.setFillColor(S2)
        c.setStrokeColor(BD)
        c.setLineWidth(0.5)
        c.roundRect(70, y - 18, W - 100, 16, 3, fill=1, stroke=1)
        c.setFillColor(T2)
        c.setFont('Helvetica', 7)
        c.drawString(78, y - 14, cmd)
        
        y -= 48
    
    # Hardware table
    y -= 15
    c.setFillColor(T3)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(30, y, '// BILL_OF_MATERIALS')
    
    y -= 20
    c.setFillColor(T2)
    c.setFont('Helvetica', 10)
    c.drawString(30, y, 'Minimum viable setup costs under $10. Full research rig under $25.')
    
    y -= 25
    # Table header
    cols = [30, 150, 260, 370, 450]
    headers = ['Component', 'Model / Spec', 'Purpose', 'Cost', 'Status']
    c.setFillColor(S2)
    c.setStrokeColor(BD)
    c.setLineWidth(0.5)
    c.roundRect(25, y - 5, W - 50, 18, 3, fill=1, stroke=1)
    c.setFillColor(T3)
    c.setFont('Helvetica-Bold', 7)
    for i, h in enumerate(headers):
        c.drawString(cols[i], y, h)
    
    y -= 22
    rows = [
        ('ESP32 Module', 'ESP32-WROOM-32 / DevKitC', 'Main controller', '~$3-5', 'Required', GREEN),
        ('NRF24L01+ PA/LNA', '2.4 GHz transceiver + antenna', 'RF24 experimentation', '~$2-4', 'Optional', T2),
        ('MicroSD Module', 'SPI interface, FAT32', 'PCAP capture storage', '~$1-2', 'Optional', T2),
        ('OLED Display', 'SSD1306 128x64, I2C', 'Real-time status display', '~$2-3', 'Optional', T2),
        ('LiPo Battery', '3.7V 1000mAh + TP4056', 'Portable field operation', '~$3-5', 'Optional', T2),
    ]
    
    for comp, model, purpose, cost, status, status_color in rows:
        # Row bg
        c.setFillColor(Color(0.03, 0.03, 0.08, 0.6))
        c.rect(25, y - 8, W - 50, 18, fill=1, stroke=0)
        c.setStrokeColor(Color(1, 1, 1, 0.03))
        c.setLineWidth(0.3)
        c.line(25, y - 8, W - 25, y - 8)
        
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 8)
        c.drawString(cols[0], y, comp)
        c.setFillColor(T2)
        c.setFont('Helvetica', 7)
        c.drawString(cols[1], y, model)
        c.drawString(cols[2], y, purpose)
        c.setFillColor(GREEN)
        c.setFont('Helvetica-Bold', 8)
        c.drawString(cols[3], y, cost)
        
        # Status badge
        if status == 'Required':
            c.setFillColor(Color(0, 1, 0.53, 0.12))
            c.roundRect(cols[4] - 2, y - 4, 55, 14, 7, fill=1, stroke=0)
            c.setFillColor(GREEN)
        else:
            c.setFillColor(Color(1, 1, 1, 0.04))
            c.roundRect(cols[4] - 2, y - 4, 55, 14, 7, fill=1, stroke=0)
            c.setFillColor(T2)
        c.setFont('Helvetica-Bold', 7)
        c.drawCentredString(cols[4] + 25, y, status)
        
        y -= 20
    
    # Component matrix
    y -= 20
    c.setFillColor(T3)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(30, y, '// COMPONENT_MATRIX')
    
    y -= 20
    c.setFillColor(S2)
    c.setStrokeColor(BD)
    c.setLineWidth(0.5)
    c.roundRect(25, y - 5, W - 50, 18, 3, fill=1, stroke=1)
    c.setFillColor(T3)
    c.setFont('Helvetica-Bold', 7)
    mcols = [30, 180, 300, 420]
    mheaders = ['Component', 'Interface', 'Protocol', 'Speed']
    for i, h in enumerate(mheaders):
        c.drawString(mcols[i], y, h)
    
    y -= 20
    mrows = [
        ('ESP32-WROOM-32', 'UART / USB', 'Serial', '115200 baud'),
        ('NRF24L01+ PA/LNA', 'SPI', 'SPI', '10 MHz'),
        ('MicroSD Module', 'SPI', 'SPI', '25 MHz'),
        ('OLED SSD1306', 'I2C', 'I2C', '400 kHz'),
        ('LiPo Battery', 'ADC', '3.7V', 'nominal'),
    ]
    
    for comp, iface, proto, speed in mrows:
        c.setFillColor(Color(0.03, 0.03, 0.08, 0.6))
        c.rect(25, y - 8, W - 50, 18, fill=1, stroke=0)
        c.setStrokeColor(Color(1, 1, 1, 0.03))
        c.line(25, y - 8, W - 25, y - 8)
        
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 8)
        c.drawString(mcols[0], y, comp)
        c.setFillColor(T2)
        c.setFont('Helvetica', 7)
        c.drawString(mcols[1], y, iface)
        c.drawString(mcols[2], y, proto)
        c.setFillColor(CYAN)
        c.setFont('Helvetica-Bold', 7)
        c.drawString(mcols[3], y, speed)
        y -= 20
    
    # Footer
    c.setFillColor(T4)
    c.rect(0, 0, W, 30, fill=1, stroke=0)
    c.setFillColor(T3)
    c.setFont('Helvetica', 7)
    c.drawString(30, 11, 'github.com/ykrishhh/ESP32-HARNESS')
    c.drawRightString(W - 30, 11, 'Built for authorized security research only')
    c.setFillColor(CYAN)
    c.setFont('Helvetica-Bold', 7)
    c.drawCentredString(W/2, 11, 'ESP32-HARNESS Datasheet v1.0  |  MIT License')

def main():
    c = canvas.Canvas(OUT, pagesize=A4)
    c.setTitle('ESP32-HARNESS Datasheet v1.0')
    c.setAuthor('ykrishhh')
    c.setSubject('Advanced Pentesting, Audit & Telemetry Firmware')
    
    draw_page1_cover(c)
    c.showPage()
    
    draw_page2_features(c)
    c.showPage()
    
    draw_page3_setup(c)
    c.showPage()
    
    c.save()
    print(f'PDF generated: {OUT}')
    print(f'Size: {os.path.getsize(OUT) / 1024:.1f} KB')

if __name__ == '__main__':
    main()
