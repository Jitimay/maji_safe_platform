# MajiSafe Database Schema

## Overview

The MajiSafe platform uses SQLite for local data storage with a comprehensive schema supporting water infrastructure management, community demand tracking, and system activity logging.

## Database Schema

### Tables

#### 1. Villages Table
Stores information about rural communities served by the water system.

```sql
CREATE TABLE villages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    current_demand INTEGER DEFAULT 0,
    total_requests INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Fields:**
- `id`: Unique village identifier
- `name`: Village name (e.g., "Village A", "Village B")
- `current_demand`: Current number of water requests
- `total_requests`: Total historical requests
- `created_at`: Record creation timestamp

#### 2. Pumps Table
Manages water pump information and operational status.

```sql
CREATE TABLE pumps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    village_id INTEGER NOT NULL,
    status VARCHAR(10) DEFAULT 'OFF',
    runtime_minutes INTEGER DEFAULT 0,
    last_started TIMESTAMP,
    last_stopped TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (village_id) REFERENCES villages(id)
);
```

**Fields:**
- `id`: Unique pump identifier
- `village_id`: Associated village (foreign key)
- `status`: Current status ('ON' or 'OFF')
- `runtime_minutes`: Total accumulated runtime
- `last_started`: Timestamp of last start operation
- `last_stopped`: Timestamp of last stop operation
- `created_at`: Record creation timestamp

#### 3. Water Distribution Table
Tracks water allocation and distribution records.

```sql
CREATE TABLE water_distribution (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    village_id INTEGER NOT NULL,
    amount_liters DECIMAL(10,2) NOT NULL,
    distribution_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    allocation_ratio DECIMAL(5,4),
    FOREIGN KEY (village_id) REFERENCES villages(id)
);
```

**Fields:**
- `id`: Unique distribution record identifier
- `village_id`: Target village (foreign key)
- `amount_liters`: Water amount distributed in liters
- `distribution_timestamp`: When distribution occurred
- `allocation_ratio`: Calculated allocation ratio (0.0-1.0)

#### 4. Activity Log Table
Comprehensive system event logging for monitoring and troubleshooting.

```sql
CREATE TABLE activity_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    village_id INTEGER,
    pump_id INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT,
    FOREIGN KEY (village_id) REFERENCES villages(id),
    FOREIGN KEY (pump_id) REFERENCES pumps(id)
);
```

**Fields:**
- `id`: Unique log entry identifier
- `event_type`: Event category (e.g., 'PUMP_START', 'SMS_REQUEST', 'WATER_DISTRIBUTION')
- `description`: Human-readable event description
- `village_id`: Associated village (optional, foreign key)
- `pump_id`: Associated pump (optional, foreign key)
- `timestamp`: Event occurrence time
- `metadata`: JSON-formatted additional event data

#### 5. SMS Requests Table
Tracks simulated SMS-based water requests from communities.

```sql
CREATE TABLE sms_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    village_id INTEGER NOT NULL,
    request_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    simulated BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (village_id) REFERENCES villages(id)
);
```

**Fields:**
- `id`: Unique request identifier
- `village_id`: Requesting village (foreign key)
- `request_timestamp`: When request was received
- `simulated`: Flag indicating if request is simulated (TRUE for demo)

## Sample Data

The database initializes with demonstration data:

### Villages
- **Village A**: 5 current demand, 5 total requests
- **Village B**: 3 current demand, 3 total requests

### Pumps
- **Pump 1**: Associated with Village A, status OFF
- **Pump 2**: Associated with Village B, status OFF

### Activity Log
- System startup events
- Sample data creation events
- Initial SMS request events

### SMS Requests
- 5 simulated requests for Village A
- 3 simulated requests for Village B

## Database Operations

### Initialization
```bash
# Initialize database schema and sample data
python3 init_db.py

# Verify database setup
python3 verify_db.py

# Test all operations
python3 test_database_operations.py
```

### Key Operations
- **Village demand tracking**: Automatic increment on SMS requests
- **Pump control**: Start/stop operations with runtime tracking
- **Water distribution**: Proportional allocation based on demand ratios
- **Activity logging**: Automatic event logging for all system operations
- **Real-time updates**: Database changes trigger UI updates via WebSocket

## Requirements Validation

This schema implementation satisfies the following requirements:

- **Requirement 11.1**: Village information storage (name, demand)
- **Requirement 11.2**: Pump information storage (status, runtime, village association)
- **Requirement 11.3**: Water distribution records (timestamps, amounts)
- **Requirement 11.4**: Activity log entries (timestamps, event descriptions)

## File Structure

```
backend/
├── database.py          # Database manager and schema
├── models.py           # Data models and business logic
├── init_db.py          # Database initialization script
├── verify_db.py        # Database verification utility
├── test_database_operations.py  # Comprehensive test suite
└── data/
    └── majisafe.db     # SQLite database file
```