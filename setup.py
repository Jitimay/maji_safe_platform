#!/usr/bin/env python3
"""
MajiSafe Platform Setup Script
Creates virtual environment and installs dependencies
"""

import os
import sys
import subprocess
import venv

def create_virtual_environment():
    """Create Python virtual environment"""
    venv_path = "venv"
    
    if os.path.exists(venv_path):
        print(f"Virtual environment already exists at {venv_path}")
        return venv_path
    
    print("Creating Python virtual environment...")
    venv.create(venv_path, with_pip=True)
    print(f"Virtual environment created at {venv_path}")
    
    return venv_path

def install_dependencies(venv_path):
    """Install Python dependencies"""
    if sys.platform == "win32":
        pip_path = os.path.join(venv_path, "Scripts", "pip")
        python_path = os.path.join(venv_path, "Scripts", "python")
    else:
        pip_path = os.path.join(venv_path, "bin", "pip")
        python_path = os.path.join(venv_path, "bin", "python")
    
    print("Installing Python dependencies...")
    subprocess.run([pip_path, "install", "-r", "backend/requirements.txt"], check=True)
    print("Dependencies installed successfully")
    
    return python_path

def main():
    """Main setup function"""
    print("=== MajiSafe Platform Setup ===")
    
    try:
        # Create virtual environment
        venv_path = create_virtual_environment()
        
        # Install dependencies
        python_path = install_dependencies(venv_path)
        
        print("\n=== Setup Complete ===")
        print("To run the MajiSafe platform:")
        print("1. Activate virtual environment:")
        if sys.platform == "win32":
            print(f"   {venv_path}\\Scripts\\activate")
        else:
            print(f"   source {venv_path}/bin/activate")
        print("2. Run the application:")
        print("   python run.py")
        print("\nOr simply run: python run.py (it will use the virtual environment automatically)")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during setup: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()