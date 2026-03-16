// Add to your Arduino code - WiFi integration
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// MajiSafe platform URL
const char* platformURL = "http://YOUR_SERVER_IP:5000";

void setupWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("WiFi connected!");
}

void sendPumpStatus(int pumpId, String status) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(String(platformURL) + "/api/pumps/" + pumpId + "/" + status.toLowerCase());
    http.addHeader("Content-Type", "application/json");
    
    int httpCode = http.POST("{}");
    if (httpCode > 0) {
      Serial.println("Status sent to platform: " + status);
    }
    http.end();
  }
}

void sendSMSRequest(String village) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(String(platformURL) + "/api/sms/request/" + village);
    http.addHeader("Content-Type", "application/json");
    
    int httpCode = http.POST("{}");
    http.end();
  }
}

// Update your processCommand function:
void processCommand(String sender, String msg) {
  msg.toLowerCase();
  msg.trim();

  String reply = "";
  
  if (msg.indexOf("pump1 on") >= 0) {
    relayOn(RELAY1);
    sendPumpStatus(1, "start");  // Notify platform
    reply = "Pump 1 ON.";
  } else if (msg.indexOf("pump1 off") >= 0) {
    relayOff(RELAY1);
    sendPumpStatus(1, "stop");   // Notify platform
    reply = "Pump 1 OFF.";
  }
  // ... rest of your commands
  
  // Log SMS request to platform
  String village = sender.indexOf("Village") >= 0 ? "village-a" : "village-b";
  sendSMSRequest(village);
  
  if (reply.length() > 0) {
    sendSMS(sender, reply);
  }
}
