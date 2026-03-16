"""
MajiSafe Database Schema and Initialization
SQLite database setup for water infrastructure management
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, Dict, Any

class DatabaseManager:
    """Manages SQLite database operations for MajiSafe platform"""
    
    def __init__(self, db_path: str = "data/majisafe.db"):
        self.db_path = db_path
        self.ensure_database_directory()
    
    def ensure_database_directory(self):
        """Ensure the database directory exists"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def initialize_schema(self):
        """Create all database tables"""
        conn = self.get_connection()
        try:
            # Create villages table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS villages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(50) NOT NULL UNIQUE,
                    current_demand INTEGER DEFAULT 0,
                    total_requests INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create pumps table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS pumps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    village_id INTEGER NOT NULL,
                    status VARCHAR(10) DEFAULT 'OFF',
                    runtime_minutes INTEGER DEFAULT 0,
                    last_started TIMESTAMP,
                    last_stopped TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (village_id) REFERENCES villages(id)
                )
            """)
            
            # Create water_distribution table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS water_distribution (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    village_id INTEGER NOT NULL,
                    amount_liters DECIMAL(10,2) NOT NULL,
                    distribution_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    allocation_ratio DECIMAL(5,4),
                    FOREIGN KEY (village_id) REFERENCES villages(id)
                )
            """)
            
            # Create activity_log table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type VARCHAR(50) NOT NULL,
                    description TEXT NOT NULL,
                    village_id INTEGER,
                    pump_id INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT,
                    FOREIGN KEY (village_id) REFERENCES villages(id),
                    FOREIGN KEY (pump_id) REFERENCES pumps(id)
                )
            """)
            
            # Create sms_requests table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sms_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    village_id INTEGER NOT NULL,
                    request_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    simulated BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (village_id) REFERENCES villages(id)
                )
            """)
            
            conn.commit()
            print("Database schema initialized successfully")
            
        except sqlite3.Error as e:
            print(f"Error initializing database schema: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def initialize_sample_data(self):
        """Insert sample data for demonstration"""
        conn = self.get_connection()
        try:
            # Check if data already exists
            cursor = conn.execute("SELECT COUNT(*) FROM villages")
            if cursor.fetchone()[0] > 0:
                print("Sample data already exists, skipping initialization")
                return
            
            # Insert sample villages
            conn.execute("""
                INSERT INTO villages (name, current_demand, total_requests)
                VALUES ('Village A', 5, 5)
            """)
            
            conn.execute("""
                INSERT INTO villages (name, current_demand, total_requests)
                VALUES ('Village B', 3, 3)
            """)
            
            # Get village IDs
            village_a_id = conn.execute(
                "SELECT id FROM villages WHERE name = 'Village A'"
            ).fetchone()[0]
            
            village_b_id = conn.execute(
                "SELECT id FROM villages WHERE name = 'Village B'"
            ).fetchone()[0]
            
            # Insert sample pumps
            conn.execute("""
                INSERT INTO pumps (village_id, status, runtime_minutes)
                VALUES (?, 'OFF', 0)
            """, (village_a_id,))
            
            conn.execute("""
                INSERT INTO pumps (village_id, status, runtime_minutes)
                VALUES (?, 'OFF', 0)
            """, (village_b_id,))
            
            # Insert initial activity log entries
            conn.execute("""
                INSERT INTO activity_log (event_type, description, village_id)
                VALUES ('SYSTEM_STARTUP', 'MajiSafe platform initialized', NULL)
            """)
            
            conn.execute("""
                INSERT INTO activity_log (event_type, description, village_id)
                VALUES ('SAMPLE_DATA', 'Sample villages and pumps created', NULL)
            """)
            
            # Insert sample SMS requests
            for _ in range(5):
                conn.execute("""
                    INSERT INTO sms_requests (village_id, simulated)
                    VALUES (?, TRUE)
                """, (village_a_id,))
            
            for _ in range(3):
                conn.execute("""
                    INSERT INTO sms_requests (village_id, simulated)
                    VALUES (?, TRUE)
                """, (village_b_id,))
            
            conn.commit()
            print("Sample data initialized successfully")
            
        except sqlite3.Error as e:
            print(f"Error initializing sample data: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def reset_database(self):
        """Drop all tables and recreate schema"""
        conn = self.get_connection()
        try:
            # Drop tables in reverse order due to foreign keys
            tables = ['sms_requests', 'activity_log', 'water_distribution', 'pumps', 'villages']
            for table in tables:
                conn.execute(f"DROP TABLE IF EXISTS {table}")
            
            conn.commit()
            print("Database reset successfully")
            
        except sqlite3.Error as e:
            print(f"Error resetting database: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> list:
        """Execute a SELECT query and return results"""
        conn = self.get_connection()
        try:
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            raise
        finally:
            conn.close()
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an INSERT/UPDATE/DELETE query and return affected rows"""
        conn = self.get_connection()
        try:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Error executing update: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()

# Global database manager instance
db_manager = DatabaseManager()

def init_database():
    """Initialize database schema and sample data"""
    print("Initializing MajiSafe database...")
    db_manager.initialize_schema()
    db_manager.initialize_sample_data()
    print("Database initialization complete")

if __name__ == "__main__":
    # Initialize database when run directly
    init_database()