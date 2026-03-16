# MajiSafe Platform - Quick Start Commands

## Single Command Launch Options:

### Option 1: Bash Script (Linux/Mac)
```bash
chmod +x start_all.sh
./start_all.sh
```

### Option 2: Python Launcher (Cross-platform)
```bash
python launch.py
```

### Option 3: Docker Compose (Future)
```bash
docker-compose up
```

## What Gets Started:

1. **Flask Web Platform** (Port 5000)
   - Cyberpunk dashboard interface
   - REST API endpoints
   - WebSocket real-time updates

2. **Local AI Bridge**
   - SMS pattern recognition
   - Smart pump control decisions
   - Demand prediction algorithms

3. **Arduino Bridge** (if Arduino detected)
   - Serial communication with Arduino
   - SMS relay to platform
   - Hardware pump control

## Platform Access:

- **Dashboard**: http://localhost:5000
- **AI Thinking**: http://localhost:5000 (AI Thinking tab)
- **Settings**: http://localhost:5000 (Settings tab)

## Stop All Services:

```bash
./stop_all.sh
# or
Ctrl+C (in launcher terminal)
```

## Logs:

- Flask Platform: `logs/flask.log`
- AI Bridge: `logs/ai_bridge.log`
- Arduino Bridge: `logs/arduino_bridge.log`

## Service Monitoring:

The launcher automatically:
- ✅ Checks service health
- 🔄 Restarts failed services
- 📊 Monitors system status
- 🚨 Reports errors

## Requirements:

- Python 3.8+
- Virtual environment activated
- Arduino connected (optional)
- Port 5000 available
