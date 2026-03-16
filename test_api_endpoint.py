#!/usr/bin/env python3
"""
Simple test for the API endpoint
"""

import urllib.request
import json
import time

def test_api():
    try:
        # Wait a moment for server to be ready
        time.sleep(2)
        
        # Make request to the API
        with urllib.request.urlopen('http://localhost:5000/api/dashboard/metrics') as response:
            data = json.loads(response.read().decode())
            
        print("✅ API endpoint working!")
        print("Response:")
        print(json.dumps(data, indent=2))
        
        # Validate the response structure
        required_fields = ['total_water_distributed', 'current_requests', 'communities_served', 'pump_statuses']
        for field in required_fields:
            if field not in data:
                print(f"❌ Missing required field: {field}")
                return False
        
        print("✅ All required fields present!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_api()