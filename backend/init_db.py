#!/usr/bin/env python3
"""
MajiSafe Database Initialization Script
Standalone script to initialize the SQLite database schema and sample data
"""

import sys
import os

# Add backend directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_database, db_manager

def main():
    """Initialize database with schema and sample data"""
    print("=" * 50)
    print("MajiSafe Database Initialization")
    print("=" * 50)
    
    try:
        # Initialize database
        init_database()
        
        # Verify initialization by checking tables
        print("\nVerifying database initialization...")
        
        # Check villages
        villages = db_manager.execute_query("SELECT * FROM villages")
        print(f"✓ Villages table: {len(villages)} records")
        
        # Check pumps
        pumps = db_manager.execute_query("SELECT * FROM pumps")
        print(f"✓ Pumps table: {len(pumps)} records")
        
        # Check activity log
        activities = db_manager.execute_query("SELECT * FROM activity_log")
        print(f"✓ Activity log table: {len(activities)} records")
        
        # Check SMS requests
        sms_requests = db_manager.execute_query("SELECT * FROM sms_requests")
        print(f"✓ SMS requests table: {len(sms_requests)} records")
        
        print("\n" + "=" * 50)
        print("Database initialization completed successfully!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Error during database initialization: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()