#!/usr/bin/env python3
"""
MajiSafe Platform Runner
Starts the Flask application with proper environment setup
"""

import os
import sys
import subprocess

def get_python_executable():
    """Get the correct Python executable (virtual environment if available)"""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if sys.platform == "win32":
        venv_python = os.path.join(script_dir, "venv", "Scripts", "python.exe")
    else:
        venv_python = os.path.join(script_dir, "venv", "bin", "python")
    
    if os.path.exists(venv_python):
        return venv_python
    else:
        return sys.executable

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import flask_cors
        import flask_socketio
        return True
    except ImportError:
        return False

def main():
    """Main runner function"""
    print("=== MajiSafe Water Infrastructure Management Platform ===")
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if virtual environment exists
    venv_path = os.path.join(script_dir, "venv")
    if not os.path.exists(venv_path):
        print("Virtual environment not found. Running setup...")
        subprocess.run([sys.executable, os.path.join(script_dir, "setup.py")], check=True)
    
    # Get Python executable
    python_exe = get_python_executable()
    
    # Check dependencies
    if not check_dependencies():
        print("Dependencies not found. Please run setup.py first.")
        sys.exit(1)
    
    # Change to backend directory
    backend_dir = os.path.join(script_dir, "backend")
    
    print("Starting MajiSafe platform...")
    print("Access the dashboard at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Run the Flask application
        subprocess.run([python_exe, "app.py"], cwd=backend_dir, check=True)
    except KeyboardInterrupt:
        print("\nMajiSafe platform stopped.")
    except subprocess.CalledProcessError as e:
        print(f"Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()