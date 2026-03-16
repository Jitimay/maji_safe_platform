#!/bin/bash
# MajiSafe Platform - Stop All Components

echo "🛑 Stopping MajiSafe Platform..."

# Kill all related processes
pkill -f "python.*app.py"
pkill -f "python.*local_ai_bridge.py" 
pkill -f "python.*arduino_bridge.py"
pkill -f "python.*run.py"

# Wait for processes to stop
sleep 2

echo "✅ All MajiSafe services stopped"
