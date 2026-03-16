#!/usr/bin/env python3
"""
MajiSafe Platform Setup Validation
Validates that all required files and dependencies are in place
"""

import os
import sys

def check_file_structure():
    """Check if all required files exist"""
    required_files = [
        'backend/app.py',
        'backend/requirements.txt',
        'frontend/templates/index.html',
        'frontend/static/css/style.css',
        'frontend/static/js/app.js',
        'run.py',
        'setup.py',
        'README.md'
    ]
    
    required_dirs = [
        'backend',
        'frontend',
        'frontend/templates',
        'frontend/static',
        'frontend/static/css',
        'frontend/static/js',
        'data'
    ]
    
    print("=== File Structure Validation ===")
    
    # Check directories
    for directory in required_dirs:
        if os.path.exists(directory) and os.path.isdir(directory):
            print(f"✓ Directory: {directory}")
        else:
            print(f"✗ Missing directory: {directory}")
            return False
    
    # Check files
    for file_path in required_files:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            print(f"✓ File: {file_path}")
        else:
            print(f"✗ Missing file: {file_path}")
            return False
    
    return True

def check_dependencies():
    """Check if required Python packages are available"""
    print("\n=== Dependency Validation ===")
    
    required_packages = [
        'flask',
        'flask_cors',
        'flask_socketio'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ Package: {package}")
        except ImportError:
            print(f"✗ Missing package: {package}")
            return False
    
    return True

def check_flask_app():
    """Basic validation of Flask app configuration"""
    print("\n=== Flask App Validation ===")
    
    try:
        sys.path.insert(0, 'backend')
        from app import app, socketio
        
        # Check if app is configured correctly
        if app.config.get('SECRET_KEY'):
            print("✓ Flask app has secret key")
        else:
            print("✗ Flask app missing secret key")
            return False
        
        # Check if SocketIO is configured
        if socketio:
            print("✓ SocketIO configured")
        else:
            print("✗ SocketIO not configured")
            return False
        
        # Check routes
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        expected_routes = ['/', '/health']
        
        for route in expected_routes:
            if route in routes:
                print(f"✓ Route: {route}")
            else:
                print(f"✗ Missing route: {route}")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Flask app validation failed: {e}")
        return False

def main():
    """Main validation function"""
    print("MajiSafe Platform Setup Validation")
    print("=" * 40)
    
    all_checks_passed = True
    
    # Run all validation checks
    if not check_file_structure():
        all_checks_passed = False
    
    if not check_dependencies():
        all_checks_passed = False
    
    if not check_flask_app():
        all_checks_passed = False
    
    print("\n" + "=" * 40)
    if all_checks_passed:
        print("✓ All validation checks passed!")
        print("The MajiSafe platform is ready to run.")
        print("\nTo start the platform:")
        print("  python run.py")
        print("\nOr manually:")
        print("  cd backend && python app.py")
    else:
        print("✗ Some validation checks failed.")
        print("Please run setup.py to fix missing dependencies.")
        sys.exit(1)

if __name__ == "__main__":
    main()