# Requirements Document

## Introduction

MajiSafe is a smart water infrastructure management platform that helps NGOs and governments monitor and manage rural water systems. The platform connects water pumps, communities, and demand data into a unified dashboard, enabling efficient water distribution based on community demand through SMS requests.

## Glossary

- **MajiSafe_Platform**: The complete water infrastructure management system
- **Water_Dashboard**: The main monitoring interface displaying system metrics
- **Community_Demand_Monitor**: Component tracking water requests from villages
- **Smart_Distribution_Algorithm**: Logic that allocates water based on demand patterns
- **Pump_Controller**: Interface for managing water pump operations
- **SMS_Simulator**: Component simulating SMS-based water requests
- **Village**: A rural community with water access needs (Village A or Village B)
- **Water_Pump**: Physical device that moves water from source to communities
- **Water_Tank**: Shared water storage serving multiple villages
- **Impact_Tracker**: Component measuring platform effectiveness metrics

## Requirements

### Requirement 1: Water Infrastructure Dashboard

**User Story:** As an NGO operator, I want to view key water system metrics on a dashboard, so that I can monitor overall system performance.

#### Acceptance Criteria

1. THE Water_Dashboard SHALL display total water distributed today in liters
2. THE Water_Dashboard SHALL display the current number of water requests
3. THE Water_Dashboard SHALL display the number of communities currently served
4. THE Water_Dashboard SHALL display pump status as ON or OFF for each pump
5. THE Water_Dashboard SHALL present all metrics as visual cards with clear labels

### Requirement 2: Community Demand Monitoring

**User Story:** As a water system manager, I want to monitor demand from each village, so that I can understand community water needs.

#### Acceptance Criteria

1. THE Community_Demand_Monitor SHALL track water requests from Village A
2. THE Community_Demand_Monitor SHALL track water requests from Village B
3. THE Community_Demand_Monitor SHALL display demand comparison using a bar chart
4. WHEN demand data changes, THE Community_Demand_Monitor SHALL update the display in real-time

### Requirement 3: Smart Water Distribution

**User Story:** As a system administrator, I want automated water distribution based on demand, so that water allocation is fair and efficient.

#### Acceptance Criteria

1. THE Smart_Distribution_Algorithm SHALL calculate water allocation based on village demand ratios
2. WHEN distribution decisions are made, THE Smart_Distribution_Algorithm SHALL log the allocation amounts
3. THE Water_Dashboard SHALL display current distribution decisions
4. THE Smart_Distribution_Algorithm SHALL prioritize villages with higher demand ratios

### Requirement 4: Pump Control Management

**User Story:** As a field technician, I want to control water pumps remotely, so that I can manage water flow efficiently.

#### Acceptance Criteria

1. THE Pump_Controller SHALL display status for Village A pump as ON or OFF
2. THE Pump_Controller SHALL display status for Village B pump as ON or OFF
3. WHEN a start button is clicked, THE Pump_Controller SHALL activate the corresponding pump
4. WHEN a stop button is clicked, THE Pump_Controller SHALL deactivate the corresponding pump
5. THE Pump_Controller SHALL display runtime duration for each active pump

### Requirement 5: Water Flow Estimation

**User Story:** As a water manager, I want to estimate water distribution amounts, so that I can track resource usage.

#### Acceptance Criteria

1. THE MajiSafe_Platform SHALL simulate water flow at 20 liters per minute per pump
2. WHILE a pump is active, THE MajiSafe_Platform SHALL calculate accumulated water distributed
3. THE Water_Dashboard SHALL display estimated liters distributed for each village
4. THE MajiSafe_Platform SHALL update water estimates every minute while pumps are running

### Requirement 6: SMS Request Simulation

**User Story:** As a demo operator, I want to simulate SMS water requests, so that I can demonstrate community interaction capabilities.

#### Acceptance Criteria

1. THE SMS_Simulator SHALL provide a button to add requests for Village A
2. THE SMS_Simulator SHALL provide a button to add requests for Village B
3. WHEN a request button is clicked, THE SMS_Simulator SHALL increment the demand count for that village
4. THE SMS_Simulator SHALL update the Community_Demand_Monitor with new request data

### Requirement 7: Impact Measurement Dashboard

**User Story:** As an NGO director, I want to view impact metrics, so that I can report on program effectiveness.

#### Acceptance Criteria

1. THE Impact_Tracker SHALL display total water distributed across all communities
2. THE Impact_Tracker SHALL estimate people served based on water distribution (assume 20 liters per person per day)
3. THE Impact_Tracker SHALL display the number of communities served
4. THE Impact_Tracker SHALL update metrics in real-time as water is distributed

### Requirement 8: System Map Visualization

**User Story:** As a system operator, I want to see a visual map of the water infrastructure, so that I can understand system topology and status.

#### Acceptance Criteria

1. THE MajiSafe_Platform SHALL display a diagram showing Village A and Village B locations
2. THE MajiSafe_Platform SHALL display pump locations for each village
3. THE MajiSafe_Platform SHALL show pump status using color indicators (Green for active, Red for inactive)
4. THE MajiSafe_Platform SHALL display the shared water tank connection

### Requirement 9: Activity Logging

**User Story:** As a system administrator, I want to view system activity history, so that I can track operations and troubleshoot issues.

#### Acceptance Criteria

1. THE MajiSafe_Platform SHALL log all pump start and stop events with timestamps
2. THE MajiSafe_Platform SHALL log all water distribution decisions with amounts
3. THE MajiSafe_Platform SHALL log all SMS request events by village
4. THE MajiSafe_Platform SHALL display activity log as a chronological timeline
5. THE MajiSafe_Platform SHALL limit activity log display to the most recent 50 events

### Requirement 10: Local Development Environment

**User Story:** As a developer, I want to run the platform locally, so that I can develop and demonstrate the system.

#### Acceptance Criteria

1. THE MajiSafe_Platform SHALL run on a local laptop using Python backend
2. THE MajiSafe_Platform SHALL use SQLite database for local data storage
3. THE MajiSafe_Platform SHALL serve a web interface accessible via browser
4. THE MajiSafe_Platform SHALL include sample test data for demonstration
5. THE MajiSafe_Platform SHALL provide clear setup and run instructions

### Requirement 11: Data Persistence and Schema

**User Story:** As a system architect, I want structured data storage, so that system state is maintained reliably.

#### Acceptance Criteria

1. THE MajiSafe_Platform SHALL store village information including name and current demand
2. THE MajiSafe_Platform SHALL store pump information including status, runtime, and associated village
3. THE MajiSafe_Platform SHALL store water distribution records with timestamps and amounts
4. THE MajiSafe_Platform SHALL store activity log entries with timestamps and event descriptions
5. THE MajiSafe_Platform SHALL initialize database with sample data for Village A and Village B

### Requirement 12: Web Interface Design

**User Story:** As a platform user, I want a modern and intuitive interface, so that I can efficiently monitor and control the water system.

#### Acceptance Criteria

1. THE MajiSafe_Platform SHALL use a card-based layout for displaying metrics
2. THE MajiSafe_Platform SHALL use Chart.js for rendering demand comparison charts
3. THE MajiSafe_Platform SHALL use clear status indicators with appropriate colors
4. THE MajiSafe_Platform SHALL provide responsive design suitable for laptop screens
5. THE MajiSafe_Platform SHALL use modern CSS styling with clean visual hierarchy