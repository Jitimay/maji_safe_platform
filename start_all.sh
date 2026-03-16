#!/bin/bash
# MajiSafe Platform - Run All Components

echo "🚀 Starting MajiSafe Water Management Platform..."
echo "=================================================="

# Create logs directory
mkdir -p logs

# Kill existing processes
echo "🧹 Cleaning up existing processes..."
pkill -f "python.*app.py" 2>/dev/null
pkill -f "python.*local_ai_bridge.py" 2>/dev/null
pkill -f "python.*arduino_bridge.py" 2>/dev/null

# Start Flask Platform
echo ""
echo "1️⃣ Starting Flask Web Platform..."
cd backend
nohup python app.py > ../logs/flask.log 2>&1 &
cd ..
sleep 3

# Start Local AI Bridge
echo "2️⃣ Starting Local AI Bridge..."
nohup python local_ai_bridge.py > logs/ai_bridge.log 2>&1 &
sleep 2

# Start Arduino Bridge (if Arduino connected)
echo "3️⃣ Checking Arduino Connection..."
if ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null; then
    echo "📱 Arduino detected - Starting Arduino Bridge..."
    nohup python arduino_bridge.py > logs/arduino_bridge.log 2>&1 &
    sleep 2
else
    echo "⚠️  Arduino not detected - Skipping Arduino Bridge"
fi

# Check services
echo ""
echo "🔍 Service Status:"
if pgrep -f "python.*app.py" > /dev/null; then
    echo "✅ Flask Platform running"
else
    echo "❌ Flask Platform failed"
fi

if pgrep -f "python.*local_ai_bridge.py" > /dev/null; then
    echo "✅ Local AI Bridge running"
else
    echo "❌ Local AI Bridge failed"
fi

if pgrep -f "python.*arduino_bridge.py" > /dev/null; then
    echo "✅ Arduino Bridge running"
else
    echo "⚠️  Arduino Bridge not running"
fi

echo ""
echo "🌐 Access Dashboard: http://localhost:5000"
echo "📋 Stop all: ./stop_all.sh"
echo ""
echo "✅ MajiSafe Platform started!"
