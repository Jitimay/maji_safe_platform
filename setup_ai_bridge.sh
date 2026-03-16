#!/bin/bash
# AI Bridge Setup Script

echo "🤖 Setting up AI Bridge for MajiSafe..."

# Install Python dependencies
pip install openai pyserial requests python-dotenv

# Create environment file
cat > .env << EOF
OPENAI_API_KEY=your-openai-api-key-here
PLATFORM_URL=http://localhost:5000
ARDUINO_PORT=/dev/ttyUSB0
ARDUINO_BAUD=115200
EOF

# Create systemd service for auto-start
sudo tee /etc/systemd/system/majisafe-ai.service > /dev/null << EOF
[Unit]
Description=MajiSafe AI Bridge
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/venv/bin
ExecStart=$(pwd)/venv/bin/python ai_bridge.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo "✅ AI Bridge setup complete!"
echo ""
echo "Next steps:"
echo "1. Add your OpenAI API key to .env file"
echo "2. Update Arduino port in .env if needed"
echo "3. Start AI bridge: python ai_bridge.py"
echo "4. Enable auto-start: sudo systemctl enable majisafe-ai"
