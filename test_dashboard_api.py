#!/usr/bin/env python3
"""
Test script for dashboard API endpoint
"""

import sys
import os
sys.path.append('backend')

from database import init_database
from models import Village, Pump, WaterDistribution

def test_dashboard_metrics():
    """Test the dashboard metrics functionality"""
    print("Initializing database...")
    init_database()
    
    print("Testing dashboard metrics calculation...")
    
    # Get total water distributed
    total_water_distributed = WaterDistribution.get_total_distributed()
    print(f"Total water distributed: {total_water_distributed} liters")
    
    # Get all villages to calculate current requests and communities served
    villages = Village.get_all()
    current_requests = sum(village.current_demand for village in villages)
    communities_served = len(villages)
    
    print(f"Current requests: {current_requests}")
    print(f"Communities served: {communities_served}")
    
    # Get all pumps and their statuses
    pumps = Pump.get_all()
    pump_statuses = []
    
    for pump in pumps:
        village = Village.get_by_id(pump.village_id)
        village_name = village.name if village else f"Village {pump.village_id}"
        
        pump_status = {
            "pump_id": str(pump.id),
            "status": pump.status,
            "village": village_name,
            "runtime_minutes": pump.get_current_runtime()
        }
        pump_statuses.append(pump_status)
        print(f"Pump {pump.id}: {pump_status}")
    
    # Create the dashboard metrics response
    dashboard_data = {
        "total_water_distributed": total_water_distributed,
        "current_requests": current_requests,
        "communities_served": communities_served,
        "pump_statuses": pump_statuses
    }
    
    print("\nDashboard metrics response:")
    import json
    print(json.dumps(dashboard_data, indent=2))
    
    return dashboard_data

if __name__ == "__main__":
    test_dashboard_metrics()