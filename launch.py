#!/usr/bin/env python3
"""
MajiSafe Platform Launcher
Single Python command to run all components
"""

import subprocess
import time
import os
import signal
import sys
from threading import Thread

class MajiSafeLauncher:
    def __init__(self):
        self.processes = {}
        self.running = True
        
    def start_component(self, name, command, cwd=None):
        """Start a component process"""
        try:
            print(f"🔄 Starting {name}...")
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.processes[name] = process
            time.sleep(2)
            
            if process.poll() is None:
                print(f"✅ {name} started (PID: {process.pid})")
                return True
            else:
                print(f"❌ {name} failed to start")
                return False
        except Exception as e:
            print(f"❌ Error starting {name}: {e}")
            return False
    
    def check_arduino(self):
        """Check if Arduino is connected"""
        import glob
        ports = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
        return len(ports) > 0
    
    def monitor_processes(self):
        """Monitor and restart failed processes"""
        while self.running:
            time.sleep(10)
            for name, process in self.processes.items():
                if process.poll() is not None:
                    print(f"⚠️  {name} stopped - Restarting...")
                    if name == "Flask Platform":
                        self.start_component(name, "python app.py", "backend")
                    elif name == "Local AI Bridge":
                        self.start_component(name, "python local_ai_bridge.py")
                    elif name == "Arduino Bridge":
                        self.start_component(name, "python arduino_bridge.py")
    
    def stop_all(self):
        """Stop all processes"""
        print("\n🛑 Stopping all services...")
        self.running = False
        
        for name, process in self.processes.items():
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {name} stopped")
            except:
                process.kill()
                print(f"🔪 {name} force killed")
        
        print("✅ All services stopped")
    
    def run(self):
        """Run the complete platform"""
        print("🚀 MajiSafe Platform Launcher")
        print("=" * 40)
        
        # Create logs directory
        os.makedirs("logs", exist_ok=True)
        
        # Start components
        success_count = 0
        
        # 1. Flask Platform
        if self.start_component("Flask Platform", "python app.py", "backend"):
            success_count += 1
        
        # 2. Local AI Bridge
        if self.start_component("Local AI Bridge", "python local_ai_bridge.py"):
            success_count += 1
        
        # 3. Arduino Bridge (if Arduino detected)
        if self.check_arduino():
            print("📱 Arduino detected")
            if self.start_component("Arduino Bridge", "python arduino_bridge.py"):
                success_count += 1
        else:
            print("⚠️  No Arduino detected - Skipping Arduino Bridge")
        
        print(f"\n✅ {success_count} services started successfully")
        
        if success_count > 0:
            print("\n🌐 Platform Access:")
            print("Dashboard: http://localhost:5000")
            print("AI Thinking: http://localhost:5000 (AI Thinking tab)")
            
            # Start monitoring thread
            monitor_thread = Thread(target=self.monitor_processes, daemon=True)
            monitor_thread.start()
            
            print("\n📋 Press Ctrl+C to stop all services")
            
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.stop_all()
        else:
            print("❌ No services started successfully")

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Shutdown signal received...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    launcher = MajiSafeLauncher()
    launcher.run()
