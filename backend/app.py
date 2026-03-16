"""
MajiSafe Water Infrastructure Management Platform
Main Flask application with CORS and WebSocket support
"""

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
from models import Village, Pump, WaterDistribution, ActivityLogEntry
from database import init_database

# Initialize Flask app
app = Flask(__name__, 
           static_folder='../frontend/static',
           template_folder='../frontend/templates')

# Configure CORS for cross-origin requests
CORS(app, origins=["http://localhost:5000", "http://127.0.0.1:5000"])

# Configure WebSocket support
socketio = SocketIO(app, cors_allowed_origins="*")

# Basic configuration
app.config['SECRET_KEY'] = 'majisafe-demo-key-2024'
app.config['DATABASE'] = 'majisafe.db'

@app.route('/')
def index():
    """Serve the main dashboard page"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "majisafe-platform"})

@app.route('/api/dashboard/metrics')
def dashboard_metrics():
    """Get dashboard metrics"""
    villages = Village.get_all()
    pumps = Pump.get_all()
    
    total_water = sum(pump.calculate_water_distributed() for pump in pumps)
    current_requests = sum(village.current_demand for village in villages)
    
    pump_statuses = []
    for i, pump in enumerate(pumps, 1):
        pump_statuses.append({
            "pump_id": f"pump-{chr(96+i)}",
            "status": pump.status,
            "runtime_minutes": pump.get_current_runtime()
        })
    
    return jsonify({
        "total_water_distributed": total_water,
        "current_requests": current_requests,
        "communities_served": len(villages),
        "pump_statuses": pump_statuses
    })

@app.route('/api/demand/villages')
def demand_villages():
    """Get village demand data"""
    villages = Village.get_all()
    data = {}
    for village in villages:
        key = f"village_{village.name.split()[-1].lower()}"
        data[key] = {"requests": village.current_demand}
    return jsonify(data)

@app.route('/api/pumps/<int:pump_id>/<action>', methods=['POST'])
def control_pump(pump_id, action):
    """Control pump start/stop"""
    pump = Pump.get_by_id(pump_id)
    if not pump:
        return jsonify({"error": "Pump not found"}), 404
    
    if action == 'start':
        success = pump.start()
    elif action == 'stop':
        success = pump.stop()
    else:
        return jsonify({"error": "Invalid action"}), 400
    
    if success:
        socketio.emit('pump_status_change', {
            "pump_id": f"pump_{chr(96+pump_id)}",
            "status": pump.status
        })
        return jsonify({"status": "success", "pump_status": pump.status})
    else:
        return jsonify({"error": f"Pump already {pump.status.lower()}"}), 400

@app.route('/api/sms/request/<village_id>', methods=['POST'])
def sms_request(village_id):
    """Simulate SMS request"""
    village_name = f"Village {village_id.split('-')[-1].upper()}"
    village = Village.get_by_name(village_name)
    
    if not village:
        return jsonify({"error": "Village not found"}), 404
    
    village.add_request()
    
    socketio.emit('demand_update', {
        f"village_{village_id.split('-')[-1].lower()}": {"requests": village.current_demand}
    })
    
    return jsonify({"status": "success", "village": village.name})

@app.route('/api/impact/metrics')
def impact_metrics():
    """Get impact metrics"""
    pumps = Pump.get_all()
    villages = Village.get_all()
    
    total_water = sum(pump.calculate_water_distributed() for pump in pumps)
    people_served = int(total_water / 20) if total_water > 0 else 0
    
    return jsonify({
        "total_water_distributed": total_water,
        "people_served": people_served,
        "communities_served": len(villages)
    })

@app.route('/api/activity/log')
def activity_log():
    """Get activity log"""
    entries = ActivityLogEntry.get_recent_events(20)
    log_data = []
    
    for entry in entries:
        log_data.append({
            "timestamp": entry.timestamp.isoformat(),
            "event_type": entry.event_type,
            "description": entry.description
        })
    
    return jsonify({"log": log_data})

@app.route('/api/arduino/pump/<int:pump_id>/<action>', methods=['POST'])
def arduino_pump_control(pump_id, action):
    """Arduino pump status update"""
    pump = Pump.get_by_id(pump_id)
    if not pump:
        return jsonify({"error": "Pump not found"}), 404
    
    if action == 'start':
        success = pump.start()
    elif action == 'stop':
        success = pump.stop()
    else:
        return jsonify({"error": "Invalid action"}), 400
    
    if success:
        socketio.emit('pump_status_change', {
            "pump_id": f"pump_{chr(96+pump_id)}",
            "status": pump.status,
            "source": "arduino"
        })
        return jsonify({"status": "success", "pump_status": pump.status})
    else:
        return jsonify({"error": f"Pump already {pump.status.lower()}"}), 400

@app.route('/api/arduino/sms', methods=['POST'])
def arduino_sms_received():
    """Log SMS received by Arduino"""
    data = request.get_json()
    sender = data.get('sender', '')
    message = data.get('message', '')
    village = data.get('village', 'village-a')
    
    # Map to village and add request
    village_obj = Village.get_by_name(f"Village {village.split('-')[-1].upper()}")
    if village_obj:
        village_obj.add_request()
        
        socketio.emit('demand_update', {
            f"village_{village.split('-')[-1].lower()}": {"requests": village_obj.current_demand}
        })
        
        return jsonify({"status": "success", "village": village_obj.name})
    
    return jsonify({"error": "Village not found"}), 404

# WebSocket event handlers
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected to MajiSafe platform')

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected from MajiSafe platform')

if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Ensure database directory exists
    os.makedirs('data', exist_ok=True)
    
    # Run the application
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)