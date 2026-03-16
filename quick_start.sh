#!/bin/bash
# Simple MajiSafe Launcher

echo "🚀 Starting MajiSafe Platform..."

# Create logs directory
mkdir -p logs

# Start Flask Platform
echo "Starting Flask Platform..."
cd backend
python app.py &
FLASK_PID=$!
cd ..

echo "✅ Flask Platform started (PID: $FLASK_PID)"
echo "🌐 Dashboard: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop"

# Wait for Ctrl+C
trap 'echo "Stopping..."; kill $FLASK_PID 2>/dev/null; exit 0' INT

wait
