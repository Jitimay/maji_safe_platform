#!/usr/bin/env python3
"""
Arduino Serial Bridge for MajiSafe Platform
Connects Arduino SMS controller to web platform
"""

import serial
import requests
import json
import time
import re
from threading import Thread

class ArduinoBridge:
    def __init__(self, serial_port='/dev/ttyUSB0', baud_rate=115200, platform_url='http://localhost:5000'):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.platform_url = platform_url
        self.arduino = None
        
    def connect_arduino(self):
        """Connect to Arduino via serial"""
        try:
            self.arduino = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            print(f"Connected to Arduino on {self.serial_port}")
            return True
        except Exception as e:
            print(f"Failed to connect to Arduino: {e}")
            return False
    
    def send_to_platform(self, endpoint, data=None):
        """Send data to MajiSafe platform"""
        try:
            url = f"{self.platform_url}{endpoint}"
            if data:
                response = requests.post(url, json=data)
            else:
                response = requests.post(url)
            return response.status_code == 200
        except Exception as e:
            print(f"Platform communication error: {e}")
            return False
    
    def parse_arduino_message(self, message):
        """Parse Arduino serial messages"""
        message = message.strip()
        
        # SMS received pattern
        if "From :" in message and "Msg  :" in message:
            lines = message.split('\n')
            sender = ""
            msg = ""
            for line in lines:
                if line.startswith("From :"):
                    sender = line.replace("From :", "").strip()
                elif line.startswith("Msg  :"):
                    msg = line.replace("Msg  :", "").strip()
            
            if sender and msg:
                self.handle_sms_request(sender, msg)
        
        # Pump status changes
        elif "Pump 1 ON" in message:
            self.send_to_platform("/api/pumps/1/start")
        elif "Pump 1 OFF" in message:
            self.send_to_platform("/api/pumps/1/stop")
        elif "Pump 2 ON" in message:
            self.send_to_platform("/api/pumps/2/start")
        elif "Pump 2 OFF" in message:
            self.send_to_platform("/api/pumps/2/stop")
    
    def handle_sms_request(self, sender, message):
        """Handle SMS water requests"""
        # Map phone numbers to villages (customize as needed)
        village_map = {
            # Add your village phone number mappings
            "+254700000001": "village-a",
            "+254700000002": "village-b"
        }
        
        village = village_map.get(sender, "village-a")  # Default to village-a
        
        # Send SMS request to platform
        self.send_to_platform(f"/api/sms/request/{village}")
        print(f"SMS request from {village}: {message}")
    
    def listen_arduino(self):
        """Listen to Arduino serial output"""
        buffer = ""
        while True:
            try:
                if self.arduino and self.arduino.in_waiting:
                    data = self.arduino.readline().decode('utf-8', errors='ignore')
                    buffer += data
                    
                    # Process complete messages
                    if '\n' in buffer:
                        lines = buffer.split('\n')
                        for line in lines[:-1]:  # Process all complete lines
                            if line.strip():
                                print(f"Arduino: {line}")
                                self.parse_arduino_message(line)
                        buffer = lines[-1]  # Keep incomplete line
                
                time.sleep(0.1)
            except Exception as e:
                print(f"Serial read error: {e}")
                time.sleep(1)
    
    def send_pump_command(self, pump_id, action):
        """Send pump command to Arduino"""
        if self.arduino:
            if pump_id == 1:
                command = "pump1 on" if action == "start" else "pump1 off"
            else:
                command = "pump2 on" if action == "start" else "pump2 off"
            
            # Simulate SMS command (you could modify Arduino to accept serial commands)
            print(f"Would send to Arduino: {command}")
    
    def run(self):
        """Start the bridge"""
        if not self.connect_arduino():
            return
        
        print("Arduino Bridge started. Monitoring serial communication...")
        
        # Start listening thread
        listen_thread = Thread(target=self.listen_arduino, daemon=True)
        listen_thread.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Bridge stopped")
            if self.arduino:
                self.arduino.close()

if __name__ == "__main__":
    # Configure your settings
    bridge = ArduinoBridge(
        serial_port='/dev/ttyUSB0',  # Adjust for your system
        baud_rate=115200,
        platform_url='http://localhost:5000'
    )
    bridge.run()
