"""
MajiSafe Data Models
Core business logic and database operations for water infrastructure management
"""

import json
from datetime import datetime
from typing import List, Dict, Optional, Any
from database import db_manager

class Village:
    """Village model for community water demand tracking"""
    
    def __init__(self, id: int, name: str, current_demand: int = 0, 
                 total_requests: int = 0, created_at: datetime = None):
        self.id = id
        self.name = name
        self.current_demand = current_demand
        self.total_requests = total_requests
        self.created_at = created_at or datetime.now()
    
    def add_request(self) -> None:
        """Add a new water request to this village"""
        self.current_demand += 1
        self.total_requests += 1
        
        # Update database
        db_manager.execute_update("""
            UPDATE villages 
            SET current_demand = ?, total_requests = ?
            WHERE id = ?
        """, (self.current_demand, self.total_requests, self.id))
        
        # Log the request
        ActivityLogEntry.log_sms_request(self.id)
    
    def get_demand_ratio(self, total_demand: int) -> float:
        """Calculate this village's demand ratio"""
        if total_demand == 0:
            return 0.0
        return self.current_demand / total_demand
    
    @classmethod
    def get_by_id(cls, village_id: int) -> Optional['Village']:
        """Get village by ID"""
        result = db_manager.execute_query(
            "SELECT * FROM villages WHERE id = ?", (village_id,)
        )
        if result:
            row = result[0]
            return cls(
                id=row['id'],
                name=row['name'],
                current_demand=row['current_demand'],
                total_requests=row['total_requests'],
                created_at=datetime.fromisoformat(row['created_at'])
            )
        return None
    
    @classmethod
    def get_by_name(cls, name: str) -> Optional['Village']:
        """Get village by name"""
        result = db_manager.execute_query(
            "SELECT * FROM villages WHERE name = ?", (name,)
        )
        if result:
            row = result[0]
            return cls(
                id=row['id'],
                name=row['name'],
                current_demand=row['current_demand'],
                total_requests=row['total_requests'],
                created_at=datetime.fromisoformat(row['created_at'])
            )
        return None
    
    @classmethod
    def get_all(cls) -> List['Village']:
        """Get all villages"""
        results = db_manager.execute_query("SELECT * FROM villages ORDER BY name")
        return [
            cls(
                id=row['id'],
                name=row['name'],
                current_demand=row['current_demand'],
                total_requests=row['total_requests'],
                created_at=datetime.fromisoformat(row['created_at'])
            )
            for row in results
        ]

class Pump:
    """Pump model for water pump control and monitoring"""
    
    def __init__(self, id: int, village_id: int, status: str = 'OFF',
                 runtime_minutes: int = 0, last_started: datetime = None,
                 last_stopped: datetime = None, created_at: datetime = None):
        self.id = id
        self.village_id = village_id
        self.status = status
        self.runtime_minutes = runtime_minutes
        self.last_started = last_started
        self.last_stopped = last_stopped
        self.created_at = created_at or datetime.now()
    
    def start(self) -> bool:
        """Start the pump"""
        if self.status == 'ON':
            return False  # Already running
        
        self.status = 'ON'
        self.last_started = datetime.now()
        
        # Update database
        db_manager.execute_update("""
            UPDATE pumps 
            SET status = ?, last_started = ?
            WHERE id = ?
        """, (self.status, self.last_started.isoformat(), self.id))
        
        # Log the event
        ActivityLogEntry.log_pump_event(self.id, 'START')
        
        return True
    
    def stop(self) -> bool:
        """Stop the pump"""
        if self.status == 'OFF':
            return False  # Already stopped
        
        # Calculate runtime for this session
        if self.last_started:
            session_runtime = (datetime.now() - self.last_started).total_seconds() / 60
            self.runtime_minutes += int(session_runtime)
        
        self.status = 'OFF'
        self.last_stopped = datetime.now()
        
        # Update database
        db_manager.execute_update("""
            UPDATE pumps 
            SET status = ?, runtime_minutes = ?, last_stopped = ?
            WHERE id = ?
        """, (self.status, self.runtime_minutes, self.last_stopped.isoformat(), self.id))
        
        # Log the event
        ActivityLogEntry.log_pump_event(self.id, 'STOP')
        
        return True
    
    def get_current_runtime(self) -> int:
        """Get current runtime in minutes"""
        if self.status == 'ON' and self.last_started:
            session_runtime = (datetime.now() - self.last_started).total_seconds() / 60
            return self.runtime_minutes + int(session_runtime)
        return self.runtime_minutes
    
    def calculate_water_distributed(self) -> float:
        """Calculate water distributed based on 20L/min flow rate"""
        current_runtime = self.get_current_runtime()
        return current_runtime * 20.0  # 20 liters per minute
    
    @classmethod
    def get_by_id(cls, pump_id: int) -> Optional['Pump']:
        """Get pump by ID"""
        result = db_manager.execute_query(
            "SELECT * FROM pumps WHERE id = ?", (pump_id,)
        )
        if result:
            row = result[0]
            return cls(
                id=row['id'],
                village_id=row['village_id'],
                status=row['status'],
                runtime_minutes=row['runtime_minutes'],
                last_started=datetime.fromisoformat(row['last_started']) if row['last_started'] else None,
                last_stopped=datetime.fromisoformat(row['last_stopped']) if row['last_stopped'] else None,
                created_at=datetime.fromisoformat(row['created_at'])
            )
        return None
    
    @classmethod
    def get_by_village_id(cls, village_id: int) -> Optional['Pump']:
        """Get pump by village ID"""
        result = db_manager.execute_query(
            "SELECT * FROM pumps WHERE village_id = ?", (village_id,)
        )
        if result:
            row = result[0]
            return cls(
                id=row['id'],
                village_id=row['village_id'],
                status=row['status'],
                runtime_minutes=row['runtime_minutes'],
                last_started=datetime.fromisoformat(row['last_started']) if row['last_started'] else None,
                last_stopped=datetime.fromisoformat(row['last_stopped']) if row['last_stopped'] else None,
                created_at=datetime.fromisoformat(row['created_at'])
            )
        return None
    
    @classmethod
    def get_all(cls) -> List['Pump']:
        """Get all pumps"""
        results = db_manager.execute_query("SELECT * FROM pumps ORDER BY id")
        return [
            cls(
                id=row['id'],
                village_id=row['village_id'],
                status=row['status'],
                runtime_minutes=row['runtime_minutes'],
                last_started=datetime.fromisoformat(row['last_started']) if row['last_started'] else None,
                last_stopped=datetime.fromisoformat(row['last_stopped']) if row['last_stopped'] else None,
                created_at=datetime.fromisoformat(row['created_at'])
            )
            for row in results
        ]

class WaterDistribution:
    """Water distribution model for allocation tracking"""
    
    def __init__(self, id: int, village_id: int, amount_liters: float,
                 distribution_timestamp: datetime = None, allocation_ratio: float = None):
        self.id = id
        self.village_id = village_id
        self.amount_liters = amount_liters
        self.distribution_timestamp = distribution_timestamp or datetime.now()
        self.allocation_ratio = allocation_ratio
    
    @staticmethod
    def calculate_allocation(villages: List[Village]) -> Dict[int, float]:
        """Calculate water allocation ratios based on village demand"""
        total_demand = sum(village.current_demand for village in villages)
        
        if total_demand == 0:
            # Equal allocation if no demand
            equal_ratio = 1.0 / len(villages) if villages else 0.0
            return {village.id: equal_ratio for village in villages}
        
        # Proportional allocation based on demand
        allocations = {}
        for village in villages:
            allocations[village.id] = village.get_demand_ratio(total_demand)
        
        return allocations
    
    @classmethod
    def create_distribution_record(cls, village_id: int, amount_liters: float, 
                                 allocation_ratio: float) -> 'WaterDistribution':
        """Create a new distribution record"""
        # Insert into database
        result = db_manager.execute_update("""
            INSERT INTO water_distribution (village_id, amount_liters, allocation_ratio)
            VALUES (?, ?, ?)
        """, (village_id, amount_liters, allocation_ratio))
        
        # Get the created record
        records = db_manager.execute_query(
            "SELECT * FROM water_distribution WHERE rowid = last_insert_rowid()"
        )
        
        if records:
            row = records[0]
            distribution = cls(
                id=row['id'],
                village_id=row['village_id'],
                amount_liters=row['amount_liters'],
                distribution_timestamp=datetime.fromisoformat(row['distribution_timestamp']),
                allocation_ratio=row['allocation_ratio']
            )
            
            # Log the distribution event
            ActivityLogEntry.log_distribution_event(village_id, amount_liters)
            
            return distribution
        
        return None
    
    @classmethod
    def get_by_village_id(cls, village_id: int, limit: int = None) -> List['WaterDistribution']:
        """Get distribution records for a village"""
        query = "SELECT * FROM water_distribution WHERE village_id = ? ORDER BY distribution_timestamp DESC"
        params = (village_id,)
        
        if limit:
            query += " LIMIT ?"
            params = (village_id, limit)
        
        results = db_manager.execute_query(query, params)
        return [
            cls(
                id=row['id'],
                village_id=row['village_id'],
                amount_liters=row['amount_liters'],
                distribution_timestamp=datetime.fromisoformat(row['distribution_timestamp']),
                allocation_ratio=row['allocation_ratio']
            )
            for row in results
        ]
    
    @classmethod
    def get_total_distributed(cls) -> float:
        """Get total water distributed across all villages"""
        result = db_manager.execute_query(
            "SELECT SUM(amount_liters) as total FROM water_distribution"
        )
        return result[0]['total'] or 0.0

class ActivityLogEntry:
    """Activity log model for system event tracking"""
    
    def __init__(self, id: int, event_type: str, description: str,
                 village_id: int = None, pump_id: int = None,
                 timestamp: datetime = None, metadata: Dict = None):
        self.id = id
        self.event_type = event_type
        self.description = description
        self.village_id = village_id
        self.pump_id = pump_id
        self.timestamp = timestamp or datetime.now()
        self.metadata = metadata or {}
    
    @staticmethod
    def log_pump_event(pump_id: int, action: str) -> None:
        """Log a pump start/stop event"""
        pump = Pump.get_by_id(pump_id)
        if not pump:
            return
        
        village = Village.get_by_id(pump.village_id)
        village_name = village.name if village else f"Village {pump.village_id}"
        
        event_type = f"PUMP_{action}"
        description = f"Pump {action.lower()}ed for {village_name}"
        
        metadata = json.dumps({
            "pump_id": pump_id,
            "village_id": pump.village_id,
            "action": action,
            "pump_status": pump.status
        })
        
        db_manager.execute_update("""
            INSERT INTO activity_log (event_type, description, village_id, pump_id, metadata)
            VALUES (?, ?, ?, ?, ?)
        """, (event_type, description, pump.village_id, pump_id, metadata))
    
    @staticmethod
    def log_distribution_event(village_id: int, amount: float) -> None:
        """Log a water distribution event"""
        village = Village.get_by_id(village_id)
        village_name = village.name if village else f"Village {village_id}"
        
        event_type = "WATER_DISTRIBUTION"
        description = f"Distributed {amount:.1f}L to {village_name}"
        
        metadata = json.dumps({
            "village_id": village_id,
            "amount_liters": amount,
            "distribution_type": "automated"
        })
        
        db_manager.execute_update("""
            INSERT INTO activity_log (event_type, description, village_id, metadata)
            VALUES (?, ?, ?, ?)
        """, (event_type, description, village_id, metadata))
    
    @staticmethod
    def log_sms_request(village_id: int) -> None:
        """Log an SMS request event"""
        village = Village.get_by_id(village_id)
        village_name = village.name if village else f"Village {village_id}"
        
        event_type = "SMS_REQUEST"
        description = f"Water request received from {village_name}"
        
        metadata = json.dumps({
            "village_id": village_id,
            "request_type": "simulated",
            "demand_updated": True
        })
        
        db_manager.execute_update("""
            INSERT INTO activity_log (event_type, description, village_id, metadata)
            VALUES (?, ?, ?, ?)
        """, (event_type, description, village_id, metadata))
    
    @classmethod
    def get_recent_events(cls, limit: int = 50) -> List['ActivityLogEntry']:
        """Get recent activity log events"""
        results = db_manager.execute_query("""
            SELECT * FROM activity_log 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        
        return [
            cls(
                id=row['id'],
                event_type=row['event_type'],
                description=row['description'],
                village_id=row['village_id'],
                pump_id=row['pump_id'],
                timestamp=datetime.fromisoformat(row['timestamp']),
                metadata=json.loads(row['metadata']) if row['metadata'] else {}
            )
            for row in results
        ]
    
    @classmethod
    def get_by_type(cls, event_type: str, limit: int = None) -> List['ActivityLogEntry']:
        """Get activity log events by type"""
        query = "SELECT * FROM activity_log WHERE event_type = ? ORDER BY timestamp DESC"
        params = (event_type,)
        
        if limit:
            query += " LIMIT ?"
            params = (event_type, limit)
        
        results = db_manager.execute_query(query, params)
        return [
            cls(
                id=row['id'],
                event_type=row['event_type'],
                description=row['description'],
                village_id=row['village_id'],
                pump_id=row['pump_id'],
                timestamp=datetime.fromisoformat(row['timestamp']),
                metadata=json.loads(row['metadata']) if row['metadata'] else {}
            )
            for row in results
        ]