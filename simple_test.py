import sys
import os
sys.path.insert(0, 'backend')

try:
    from backend.models import Village, Pump, WaterDistribution
    print("✓ Models imported successfully")
    
    from backend.database import db_manager
    print("✓ Database manager imported successfully")
    
    print("✅ All imports successful - API endpoint should work")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")