#include <Arduino.h>
#include <WiFi.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include "config.h"

// FreeRTOS Task Handles
TaskHandle_t wifiTaskHandle = NULL;
TaskHandle_t bleTaskHandle = NULL;

// Globals to track packet rates for spam detection
volatile int packetCount = 0;
unsigned long lastCheckTime = 0;

// Custom Advertiser Callback to scan packets
class AuditAdvertiserCallbacks: public BLEAdvertisedDeviceCallbacks {
    void onResult(BLEAdvertisedDevice advertisedDevice) {
        packetCount++;
        
        // Print device info
        Serial.printf("[+] Scanned BLE Device | MAC: %s | RSSI: %d | Name: %s\n", 
                      advertisedDevice.getAddress().toString().c_str(),
                      advertisedDevice.getRSSI(),
                      advertisedDevice.getName().c_str());

        // Check if device matches common BLE spam behavior (blank names, high RSSI, changing MACs)
        if (advertisedDevice.getName().length() == 0 && advertisedDevice.getRSSI() > -40) {
            Serial.printf("[!] Warning: High-power blank BLE packet detected from MAC: %s\n", 
                          advertisedDevice.getAddress().toString().c_str());
        }
    }
};

// Wi-Fi Auditor Task
void wifiAuditorTask(void *parameter) {
    Serial.println("[*] Wi-Fi Auditor Task initialized on core 0.");
    
    while(true) {
        Serial.println("[*] Starting Wi-Fi channel scan...");
        int n = WiFi.scanNetworks();
        Serial.println("[+] Wi-Fi scan completed.");
        
        if (n == 0) {
            Serial.println("[-] No Wi-Fi networks found.");
        } else {
            Serial.printf("[+] Found %d networks:\n", n);
            for (int i = 0; i < n; ++i) {
                // Print SSID, RSSI, Channel, and Encryption Type
                Serial.printf("    %2d: %s (RSSI: %d) Ch: %d [Enc: %d]\n", 
                              i + 1, WiFi.SSID(i).c_str(), WiFi.RSSI(i), WiFi.channel(i), (int)WiFi.encryptionType(i));
            }
        }
        WiFi.scanDelete();
        
        // Sleep for 30 seconds
        vTaskDelay(30000 / portTICK_PERIOD_MS);
    }
}

// BLE Auditor Task
void bleAuditorTask(void *parameter) {
    Serial.println("[*] BLE Auditor Task initialized on core 1.");
    
    BLEDevice::init("ESP32-Security-Harness");
    BLEScan* pBLEScan = BLEDevice::getBLEScan();
    pBLEScan->setAdvertisedDeviceCallbacks(new AuditAdvertiserCallbacks());
    pBLEScan->setActiveScan(true);
    pBLEScan->setInterval(100);
    pBLEScan->setWindow(99);

    while(true) {
        packetCount = 0;
        lastCheckTime = millis();
        
        Serial.println("[*] Starting BLE scan...");
        BLEScanResults foundDevices = pBLEScan->start(SCAN_TIME_SECONDS, false);
        pBLEScan->clearResults();
        
        unsigned long duration = millis() - lastCheckTime;
        float rate = (float)packetCount / (duration / 1000.0);
        
        Serial.printf("[+] BLE scan completed. Total Packets: %d | Rate: %.2f/sec\n", packetCount, rate);
        
        if (rate > BLE_PACKET_THRESHOLD_PER_SEC) {
            Serial.printf("[!] ALERT: High BLE activity rate detected (%.2f packets/sec)! Possible flood attack in progress.\n", rate);
            digitalWrite(ALERT_LED_PIN, HIGH);
        } else {
            digitalWrite(ALERT_LED_PIN, LOW);
        }
        
        // Sleep for 5 seconds
        vTaskDelay(5000 / portTICK_PERIOD_MS);
    }
}

void setup() {
    Serial.begin(115200);
    delay(1000);
    Serial.println("--- ESP32 Auditing & Pentesting Firmware Initialized ---");

    pinMode(STATUS_LED_PIN, OUTPUT);
    pinMode(ALERT_LED_PIN, OUTPUT);
    
    // Blink status LED twice to signal boot
    digitalWrite(STATUS_LED_PIN, HIGH); delay(200);
    digitalWrite(STATUS_LED_PIN, LOW); delay(200);
    digitalWrite(STATUS_LED_PIN, HIGH); delay(200);
    digitalWrite(STATUS_LED_PIN, LOW);

    // Set Wi-Fi to station mode and disconnect
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();

    // Create FreeRTOS Tasks pinned to separate cores
    xTaskCreatePinnedToCore(wifiAuditorTask, "WiFiAuditor", 4096, NULL, 1, &wifiTaskHandle, 0);
    xTaskCreatePinnedToCore(bleAuditorTask, "BLEAuditor", 4096, NULL, 1, &bleTaskHandle, 1);
}

void loop() {
    // Keep status LED breathing or pulsing to indicate system up time
    digitalWrite(STATUS_LED_PIN, HIGH);
    delay(500);
    digitalWrite(STATUS_LED_PIN, LOW);
    delay(500);
}
