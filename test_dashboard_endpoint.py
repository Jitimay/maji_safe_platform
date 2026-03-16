#!/usr/bin/env python3
"""
Test script for dashboard API endpoint
"""

import sys
import os
sys.path.insert(0, 'backend')

from backend.database import init_database
from backend.models import Village, Pump, WaterDistribution

def test_dashboard_endpoint():
    """Test the dashboard metrics functionality"""
    print("Testing Dashboard API Endpoint")
    print("=" * 40)
    
    try:
        # Initialize database
        print("1. Initializing database...")
        init_database()
        print("   ✓ Database initialized")
        
        # Test getting total water distributed
        print("2. Testing total water distributed...")
        total_water = WaterDistribution.get_total_distributed()
        print(f"   ✓ Total water distributed: {total_water}L")
        
        # Test getting villages and current requests
        print("3. Testing village demand tracking...")
        villages = Village.get_all()
        current_requests = sum(village.current_demand for village in villages)
        print(f"   ✓ Villages found: {len(villages)}")
        print(f"   ✓ Current requests: {current_requests}")
        for village in villages:
            print(f"     - {village.name}: {village.current_demand} requests")
        
        # Test getting pump statuses
        print("4. Testing pump status...")
        pumps = Pump.get_all()
        print(f"   ✓ Pumps found: {len(pumps)}")
        for pump in pumps:
            village = Village.get_by_id(pump.village_id)
            village_name = village.name if village else f"Village {pump.village_id}"
            print(f"     - Pump {pump.id} ({village_name}): {pump.status}")
        
        # Simulate the API response
        print("5. Simulating API response...")
        pump_statuses = []
        for pump in pumps:
            village = Village.get_by_id(pump.village_id)
            pump_statuses.append({
                "pump_id": pump.id,
                "status": pump.status,
                "village": village.name if village else f"Village {pump.village_id}",
                "runtime_minutes": pump.get_current_runtime()
            })
        
        api_response = {
            "total_water_distributed": total_water,
            "current_requests": current_requests,
            "communities_served": len(villages),
            "pump_statuses": pump_statuses
        }
        
        print("   ✓ API Response:")
        import json
        print(json.dumps(api_response, indent=2))
        
        print("\n" + "=" * 40)
        print("✅ Dashboard endpoint test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_dashboard_endpoint()
    sys.exit(0 if success else 1)