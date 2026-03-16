#!/bin/bash
# MajiSafe Platform - Run All Components
# Single command to start the complete water management system

echo "🚀 Starting MajiSafe Water Management Platform..."
echo "=================================================="

# Function to check if process is running
check_process() {
    if pgrep -f "$1" > /dev/null; then
        echo "✅ $2 is running"
        return 0
    else
        echo "❌ $2 is not running"
        return 1
    fi
}

# Function to start component in background
start_component() {
    echo "🔄 Starting $2..."
    nohup $1 > logs/$3.log 2>&1 &
    sleep 2
    if check_process "$1" "$2"; then
        echo "✅ $2 started successfully"
    else
        echo "❌ Failed to start $2"
    fi
}

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
start_component "python app.py" "Flask Platform" "flask"
cd ..

# Start Local AI Bridge
echo ""
echo "2️⃣ Starting Local AI Bridge..."
start_component "python local_ai_bridge.py" "Local AI Bridge" "ai_bridge"

# Start Arduino Bridge (if Arduino connected)
echo ""
echo "3️⃣ Checking Arduino Connection..."
if ls /dev/ttyUSB* 2>/dev/null || ls /dev/ttyACM* 2>/dev/null; then
    echo "📱 Arduino detected - Starting Arduino Bridge..."
    start_component "python arduino_bridge.py" "Arduino Bridge" "arduino_bridge"
else
    echo "⚠️  Arduino not detected - Skipping Arduino Bridge"
fi

# Wait for all services to initialize
echo ""
echo "⏳ Initializing services..."
sleep 5

# Check all services
echo ""
echo "🔍 Service Status Check:"
echo "========================"
check_process "python.*app.py" "Flask Platform"
check_process "python.*local_ai_bridge.py" "Local AI Bridge"
check_process "python.*arduino_bridge.py" "Arduino Bridge"

echo ""
echo "🌐 Platform URLs:"
echo "=================="
echo "📊 Dashboard: http://localhost:5000"
echo "🤖 AI Thinking: http://localhost:5000 (AI Thinking tab)"
echo "⚙️  Settings: http://localhost:5000 (Settings tab)"

echo ""
echo "📋 Available Commands:"
echo "======================"
echo "• View logs: tail -f logs/flask.log"
echo "• Stop all: ./stop_all.sh"
echo "• Restart: ./start_all.sh"

echo ""
echo "✅ MajiSafe Platform is running!"
echo "Press Ctrl+C to stop all services"

# Keep script running and monitor services
trap 'echo ""; echo "🛑 Stopping all services..."; pkill -f "python.*app.py"; pkill -f "python.*local_ai_bridge.py"; pkill -f "python.*arduino_bridge.py"; echo "✅ All services stopped"; exit 0' INT

# Monitor services
while true do
    sleep 30
    if ! check_process "python.*app.py" "Flask Platform" > /dev/null; then
        echo "⚠️  Flask Platform stopped - Restarting..."
        cd backend && nohup python app.py > ../logs/flask.log 2>&1 & cd ..
    fi
    if ! check_process "python.*local_ai_bridge.py" "Local AI Bridge" > /dev/null; then
        echo "⚠️  AI Bridge stopped - Restarting..."
        nohup python local_ai_bridge.py > logs/ai_bridge.log 2>&1 &
    fi
done
