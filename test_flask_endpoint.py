#!/usr/bin/env python3
"""
Test Flask endpoint for dashboard metrics
"""

import sys
import os
import json

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_flask_endpoint():
    """Test the Flask endpoint directly"""
    print("Testing Flask Dashboard Endpoint")
    print("=" * 40)
    
    try:
        # Initialize database first
        from database import init_database
        print("1. Initializing database...")
        init_database()
        print("   ✓ Database initialized")
        
        # Import Flask app
        from app import app
        print("2. Importing Flask app...")
        print("   ✓ Flask app imported successfully")
        
        # Create test client
        print("3. Creating test client...")
        with app.test_client() as client:
            print("   ✓ Test client created")
            
            # Test health endpoint first
            print("4. Testing health endpoint...")
            health_response = client.get('/health')
            print(f"   ✓ Health status: {health_response.status_code}")
            print(f"   ✓ Health data: {health_response.get_json()}")
            
            # Test dashboard metrics endpoint
            print("5. Testing dashboard metrics endpoint...")
            response = client.get('/api/dashboard/metrics')
            print(f"   ✓ Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.get_json()
                print("   ✓ Dashboard metrics response:")
                print(json.dumps(data, indent=2))
                
                # Validate required fields
                required_fields = ['total_water_distributed', 'current_requests', 'communities_served', 'pump_statuses']
                for field in required_fields:
                    if field in data:
                        print(f"   ✓ {field}: {data[field]}")
                    else:
                        print(f"   ❌ Missing field: {field}")
                        return False
                
                print("\n✅ Dashboard endpoint test successful!")
                return True
            else:
                print(f"   ❌ Endpoint returned status {response.status_code}")
                print(f"   ❌ Error: {response.get_data(as_text=True)}")
                return False
                
    except Exception as e:
        print(f"\n❌ Error during Flask test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_flask_endpoint()
    sys.exit(0 if success else 1)