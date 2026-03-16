# MajiSafe Platform - Quick Start

## Simple Launch (Recommended):

```bash
./quick_start.sh
```

This starts just the Flask platform at http://localhost:5000

## Full Launch (All Components):

```bash
python launch.py
```

This starts:
- Flask Platform
- Local AI Bridge  
- Arduino Bridge (if detected)

## Manual Start:

```bash
# Just the web platform
cd backend && python app.py

# Add AI bridge
python local_ai_bridge.py

# Add Arduino bridge  
python arduino_bridge.py
```

## Access:

- **Dashboard**: http://localhost:5000
- **AI Thinking**: Click "AI THINKING" tab
- **Settings**: Click "SETTINGS" tab

## Your Arduino:

Your Arduino code works as-is! The bridges will automatically detect and integrate with your SMS pump controller.

## Troubleshooting:

If services fail to start:
1. Check Python virtual environment is activated
2. Install requirements: `pip install -r backend/requirements.txt`
3. Check port 5000 is available
4. Use `python launch.py` for better error messages
