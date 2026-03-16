"""
AI-Enhanced Platform API
Adds AI decision endpoints to MajiSafe platform
"""

from flask import request
import openai
import json
from datetime import datetime

# Add to your app.py
@app.route('/api/ai/analyze', methods=['POST'])
def ai_analyze():
    """AI analysis endpoint"""
    try:
        # Get current system state
        villages = Village.get_all()
        pumps = Pump.get_all()
        
        data = {
            "villages": [{"name": v.name, "requests": v.current_demand} for v in villages],
            "pumps": [{"id": p.id, "status": p.status, "runtime": p.get_current_runtime()} for p in pumps],
            "timestamp": datetime.now().isoformat()
        }
        
        # AI decision making would go here
        # For now, simple logic:
        total_demand = sum(v.current_demand for v in villages)
        
        recommendations = {
            "action": "start_pumps" if total_demand > 5 else "maintain",
            "priority_village": villages[0].name if villages else "None",
            "confidence": 0.85,
            "reason": f"Total demand: {total_demand} requests"
        }
        
        return jsonify({
            "status": "success",
            "data": data,
            "recommendations": recommendations
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/sms-analysis', methods=['POST'])
def ai_sms_analysis():
    """AI SMS analysis endpoint"""
    data = request.get_json()
    sender = data.get('sender', '')
    message = data.get('message', '')
    
    # Simple AI logic (replace with actual AI)
    analysis = {
        "is_water_request": "water" in message.lower() or "pump" in message.lower(),
        "urgency": "high" if "urgent" in message.lower() else "medium",
        "village": "A" if "village a" in message.lower() else "B",
        "confidence": 0.9
    }
    
    return jsonify({
        "status": "success",
        "analysis": analysis,
        "original": {"sender": sender, "message": message}
    })

@app.route('/api/ai/auto-control', methods=['POST'])
def ai_auto_control():
    """Enable/disable AI auto-control"""
    data = request.get_json()
    enabled = data.get('enabled', False)
    
    # Store AI control state (you'd use database in production)
    app.config['AI_CONTROL_ENABLED'] = enabled
    
    return jsonify({
        "status": "success",
        "ai_control": enabled,
        "message": f"AI auto-control {'enabled' if enabled else 'disabled'}"
    })
