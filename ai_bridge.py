"""
AI Bridge for MajiSafe Water Management
Connects Arduino hardware to AI decision-making system
"""

import openai
import requests
import json
from datetime import datetime
from typing import Dict, List

class WaterManagementAI:
    def __init__(self, api_key: str, platform_url: str = "http://localhost:5000"):
        self.client = openai.OpenAI(api_key=api_key)
        self.platform_url = platform_url
        
    def analyze_water_demand(self, village_data: Dict) -> Dict:
        """AI analysis of water demand patterns"""
        prompt = f"""
        Analyze water demand data:
        Village A: {village_data.get('village_a', 0)} requests
        Village B: {village_data.get('village_b', 0)} requests
        Time: {datetime.now().strftime('%H:%M')}
        
        Provide pump control recommendations in JSON:
        {{
            "pump1_action": "start/stop/maintain",
            "pump2_action": "start/stop/maintain", 
            "priority_village": "A/B",
            "reason": "explanation"
        }}
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except:
            return {"error": "AI analysis failed"}
    
    def process_sms_with_ai(self, sender: str, message: str) -> Dict:
        """AI processing of SMS requests"""
        prompt = f"""
        SMS from {sender}: "{message}"
        
        Determine:
        1. Is this a water request? (yes/no)
        2. Which village? (A/B)
        3. Urgency level? (low/medium/high)
        4. Recommended action?
        
        Respond in JSON format.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except:
            return {"is_water_request": True, "village": "A", "urgency": "medium"}

class AIBridge:
    def __init__(self, openai_key: str):
        self.ai = WaterManagementAI(openai_key)
        self.platform_url = "http://localhost:5000"
        
    def get_platform_data(self) -> Dict:
        """Get current data from platform"""
        try:
            response = requests.get(f"{self.platform_url}/api/demand/villages")
            return response.json()
        except:
            return {"village_a": {"requests": 0}, "village_b": {"requests": 0}}
    
    def send_pump_command(self, pump_id: int, action: str):
        """Send AI-recommended pump command"""
        try:
            requests.post(f"{self.platform_url}/api/pumps/{pump_id}/{action}")
            print(f"AI Command: Pump {pump_id} {action}")
        except Exception as e:
            print(f"Command failed: {e}")
    
    def process_ai_recommendations(self):
        """Get AI recommendations and execute"""
        data = self.get_platform_data()
        village_data = {
            "village_a": data.get("village_a", {}).get("requests", 0),
            "village_b": data.get("village_b", {}).get("requests", 0)
        }
        
        recommendations = self.ai.analyze_water_demand(village_data)
        
        if "error" not in recommendations:
            # Execute AI recommendations
            if recommendations.get("pump1_action") in ["start", "stop"]:
                self.send_pump_command(1, recommendations["pump1_action"])
            
            if recommendations.get("pump2_action") in ["start", "stop"]:
                self.send_pump_command(2, recommendations["pump2_action"])
            
            print(f"AI Decision: {recommendations.get('reason', 'No reason provided')}")
        
        return recommendations
    
    def handle_sms_ai(self, sender: str, message: str):
        """Process SMS through AI"""
        analysis = self.ai.process_sms_with_ai(sender, message)
        
        if analysis.get("is_water_request"):
            village = "village-a" if analysis.get("village") == "A" else "village-b"
            urgency = analysis.get("urgency", "medium")
            
            # Log to platform
            requests.post(f"{self.platform_url}/api/sms/request/{village}")
            
            # If high urgency, trigger immediate AI analysis
            if urgency == "high":
                self.process_ai_recommendations()
            
            print(f"AI SMS Analysis: {village} - {urgency} urgency")
        
        return analysis

# Integration with Arduino Bridge
def enhanced_arduino_bridge():
    """Enhanced Arduino bridge with AI"""
    import serial
    import time
    from threading import Thread
    
    # Initialize AI Bridge
    ai_bridge = AIBridge("your-openai-api-key")
    
    # Arduino connection
    arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    
    def ai_decision_loop():
        """Periodic AI decision making"""
        while True:
            try:
                ai_bridge.process_ai_recommendations()
                time.sleep(300)  # Every 5 minutes
            except Exception as e:
                print(f"AI loop error: {e}")
                time.sleep(60)
    
    def arduino_listener():
        """Listen to Arduino with AI processing"""
        buffer = ""
        while True:
            try:
                if arduino.in_waiting:
                    data = arduino.readline().decode('utf-8', errors='ignore')
                    buffer += data
                    
                    if '\n' in buffer:
                        lines = buffer.split('\n')
                        for line in lines[:-1]:
                            if "From :" in line and "Msg  :" in line:
                                # Extract SMS data and process with AI
                                sender = extract_sender(line)
                                message = extract_message(line)
                                ai_bridge.handle_sms_ai(sender, message)
                        buffer = lines[-1]
                
                time.sleep(0.1)
            except Exception as e:
                print(f"Arduino listener error: {e}")
                time.sleep(1)
    
    # Start threads
    Thread(target=ai_decision_loop, daemon=True).start()
    Thread(target=arduino_listener, daemon=True).start()
    
    print("AI-Enhanced Arduino Bridge started")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        arduino.close()

def extract_sender(line):
    """Extract sender from Arduino output"""
    if "From :" in line:
        return line.split("From :")[1].split("Msg  :")[0].strip()
    return ""

def extract_message(line):
    """Extract message from Arduino output"""
    if "Msg  :" in line:
        return line.split("Msg  :")[1].strip()
    return ""

if __name__ == "__main__":
    enhanced_arduino_bridge()
