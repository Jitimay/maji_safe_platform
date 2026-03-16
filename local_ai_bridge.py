"""
Local AI Bridge for MajiSafe - No External APIs
Uses local pattern matching and rule-based AI
"""

import re
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List

class LocalWaterAI:
    def __init__(self):
        self.demand_history = []
        self.pump_patterns = {}
        
    def analyze_sms(self, sender: str, message: str) -> Dict:
        """Local SMS analysis using pattern matching"""
        msg = message.lower().strip()
        
        # Water request patterns
        water_keywords = ['water', 'pump', 'need', 'urgent', 'help', 'dry', 'empty']
        urgency_keywords = ['urgent', 'emergency', 'now', 'asap', 'quickly']
        
        is_water_request = any(word in msg for word in water_keywords)
        is_urgent = any(word in msg for word in urgency_keywords)
        
        # Village detection from sender or message
        village = "A"
        if "village b" in msg or "b" in sender.lower():
            village = "B"
        
        urgency = "high" if is_urgent else "medium"
        
        return {
            "is_water_request": is_water_request,
            "village": village,
            "urgency": urgency,
            "confidence": 0.9 if is_water_request else 0.3
        }
    
    def analyze_demand_pattern(self, village_data: Dict) -> Dict:
        """Local demand analysis"""
        village_a_requests = village_data.get('village_a', 0)
        village_b_requests = village_data.get('village_b', 0)
        total_requests = village_a_requests + village_b_requests
        
        # Simple rule-based decisions
        if total_requests >= 8:
            return {
                "pump1_action": "start",
                "pump2_action": "start", 
                "priority_village": "A" if village_a_requests > village_b_requests else "B",
                "reason": f"High demand detected: {total_requests} requests"
            }
        elif total_requests >= 4:
            priority = "A" if village_a_requests > village_b_requests else "B"
            return {
                "pump1_action": "start" if priority == "A" else "maintain",
                "pump2_action": "start" if priority == "B" else "maintain",
                "priority_village": priority,
                "reason": f"Medium demand: {total_requests} requests"
            }
        else:
            return {
                "pump1_action": "maintain",
                "pump2_action": "maintain",
                "priority_village": "none",
                "reason": f"Low demand: {total_requests} requests"
            }
    
    def predict_peak_hours(self) -> List[int]:
        """Predict peak demand hours based on typical patterns"""
        # Common peak hours for rural water usage
        return [6, 7, 8, 17, 18, 19]  # Morning and evening
    
    def should_preemptive_start(self) -> bool:
        """Check if pumps should start preemptively"""
        current_hour = datetime.now().hour
        return current_hour in self.predict_peak_hours()

class LocalAIBridge:
    def __init__(self, platform_url: str = "http://localhost:5000"):
        self.ai = LocalWaterAI()
        self.platform_url = platform_url
        self.last_decision = None
        
    def process_sms_local(self, sender: str, message: str):
        """Process SMS with local AI"""
        analysis = self.ai.analyze_sms(sender, message)
        
        if analysis["is_water_request"]:
            village = "village-a" if analysis["village"] == "A" else "village-b"
            
            # Send to platform
            import requests
            try:
                requests.post(f"{self.platform_url}/api/sms/request/{village}")
                print(f"Local AI: {village} water request - {analysis['urgency']} priority")
            except:
                print(f"Platform offline - logged locally: {village} request")
            
            # Immediate action for urgent requests
            if analysis["urgency"] == "high":
                self.make_pump_decision()
        
        return analysis
    
    def make_pump_decision(self):
        """Make local pump control decision"""
        try:
            import requests
            response = requests.get(f"{self.platform_url}/api/demand/villages")
            data = response.json()
            
            village_data = {
                "village_a": data.get("village_a", {}).get("requests", 0),
                "village_b": data.get("village_b", {}).get("requests", 0)
            }
            
            decision = self.ai.analyze_demand_pattern(village_data)
            
            # Execute pump commands
            if decision["pump1_action"] in ["start", "stop"]:
                requests.post(f"{self.platform_url}/api/pumps/1/{decision['pump1_action']}")
            
            if decision["pump2_action"] in ["start", "stop"]:
                requests.post(f"{self.platform_url}/api/pumps/2/{decision['pump2_action']}")
            
            self.last_decision = decision
            print(f"Local AI Decision: {decision['reason']}")
            
        except Exception as e:
            print(f"Decision error: {e}")
            # Fallback: start pump 1 for any urgent request
            try:
                requests.post(f"{self.platform_url}/api/pumps/1/start")
            except:
                pass

def run_local_ai_bridge():
    """Run local AI bridge"""
    import serial
    from threading import Thread
    
    bridge = LocalAIBridge()
    
    try:
        arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        print("Local AI Bridge connected to Arduino")
    except:
        print("Arduino not found - running in simulation mode")
        arduino = None
    
    def periodic_analysis():
        """Periodic AI analysis"""
        while True:
            try:
                # Check if preemptive action needed
                if bridge.ai.should_preemptive_start():
                    bridge.make_pump_decision()
                
                time.sleep(300)  # Every 5 minutes
            except:
                time.sleep(60)
    
    def arduino_monitor():
        """Monitor Arduino output"""
        if not arduino:
            return
            
        buffer = ""
        while True:
            try:
                if arduino.in_waiting:
                    data = arduino.readline().decode('utf-8', errors='ignore')
                    buffer += data
                    
                    if '\n' in buffer:
                        lines = buffer.split('\n')
                        for line in lines[:-1]:
                            if "From :" in line:
                                # Parse SMS data
                                parts = line.split("From :")[1].split("Msg  :")
                                if len(parts) == 2:
                                    sender = parts[0].strip()
                                    message = parts[1].strip()
                                    bridge.process_sms_local(sender, message)
                        buffer = lines[-1]
                
                time.sleep(0.1)
            except Exception as e:
                print(f"Arduino monitor error: {e}")
                time.sleep(1)
    
    # Start monitoring threads
    Thread(target=periodic_analysis, daemon=True).start()
    Thread(target=arduino_monitor, daemon=True).start()
    
    print("🤖 Local AI Bridge running - No external APIs needed")
    print("Features: SMS analysis, demand prediction, auto pump control")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Local AI Bridge stopped")
        if arduino:
            arduino.close()

if __name__ == "__main__":
    run_local_ai_bridge()
