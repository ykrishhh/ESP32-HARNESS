#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

// BLE Scanning Configuration
#define SCAN_TIME_SECONDS 5
#define BLE_PACKET_THRESHOLD_PER_SEC 50 // Threshold to detect BLE spam/flooding attacks

// Hardware pin mapping (for simulated overlays)
#define STATUS_LED_PIN 2
#define ALERT_LED_PIN 4

// Structs for scanned devices
struct ScannedDevice {
    String address;
    int rssi;
    String name;
    bool isSpamCandidate;
};

#endif // CONFIG_H
