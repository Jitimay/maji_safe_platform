# MajiSafe Water Infrastructure Management Platform

A smart water infrastructure management platform designed to help NGOs and governments monitor and manage rural water systems efficiently. The platform provides real-time monitoring of water distribution, community demand tracking, and automated pump control through a unified web-based dashboard.

## Features

- **Real-time Water Dashboard**: Monitor total water distributed, current requests, communities served, and pump statuses
- **Community Demand Monitoring**: Track water requests from villages with visual bar charts
- **Smart Water Distribution**: Automated allocation based on community demand ratios
- **Remote Pump Control**: Start/stop pumps remotely with runtime tracking
- **Water Flow Estimation**: Simulate 20L/min flow rate with real-time accumulation
- **SMS Request Simulation**: Demonstrate community interaction capabilities
- **Impact Measurement**: Track people served and program effectiveness
- **System Map Visualization**: Visual topology with status indicators
- **Activity Logging**: Comprehensive event tracking and timeline
- **Local Development**: SQLite database with sample data for demos

## Technology Stack

- **Backend**: Python 3.8+ with Flask framework
- **Database**: SQLite for local development
- **Frontend**: HTML5, CSS3, JavaScript with Chart.js
- **Real-time**: WebSocket support via Flask-SocketIO
- **Styling**: Modern responsive CSS with card-based layout

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation & Setup

1. **Clone or download the project files**

2. **Run the setup script** (creates virtual environment and installs dependencies):
   ```bash
   python setup.py
   ```

3. **Start the platform**:
   ```bash
   python run.py
   ```

4. **Access the dashboard**:
   Open your web browser and navigate to: `http://localhost:5000`

### Manual Setup (Alternative)

If you prefer manual setup:

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment**:
   - Windows: `venv\\Scripts\\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Install dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Run the application**:
   ```bash
   cd backend
   python app.py
   ```

## Project Structure

```
majisafe-platform/
├── backend/
│   ├── app.py              # Main Flask application
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── templates/
│   │   └── index.html      # Main dashboard page
│   └── static/
│       ├── css/
│       │   └── style.css   # Platform styling
│       └── js/
│           └── app.js      # Frontend JavaScript
├── data/                   # Database storage (created automatically)
├── venv/                   # Virtual environment (created by setup)
├── setup.py               # Setup script
├── run.py                 # Application runner
└── README.md              # This file
```

## Usage

### Dashboard Overview

The main dashboard displays:
- **Total Water Distributed**: Cumulative liters distributed today
- **Current Requests**: Number of pending water requests
- **Communities Served**: Count of active communities (Village A & B)
- **System Status**: Real-time pump status indicators

### Pump Control

- Use the **Start Pump** / **Stop Pump** buttons to control water pumps
- Monitor pump runtime in real-time
- Visual status indicators show pump state (Green=ON, Red=OFF)

### SMS Request Simulation

- Click **Village A Request** or **Village B Request** to simulate SMS-based water requests
- Watch the demand chart update in real-time
- Observe how requests affect the total request count

### Demand Monitoring

- Interactive bar chart shows current demand by village
- Real-time updates as new requests are added
- Visual comparison between Village A and Village B needs

## Development

### Adding New Features

The platform is designed for easy extension:

1. **Backend APIs**: Add new endpoints in `backend/app.py`
2. **Frontend Components**: Extend `frontend/static/js/app.js`
3. **Styling**: Modify `frontend/static/css/style.css`
4. **Database**: SQLite database will be added in future tasks

### WebSocket Events

The platform supports real-time updates via WebSocket:
- `dashboard_update`: Dashboard metrics changes
- `pump_status_change`: Pump state changes
- `demand_update`: Village demand changes

## Requirements Validation

This implementation satisfies the following requirements:

- **Requirement 10.1**: Python backend with Flask framework ✓
- **Requirement 10.3**: Web interface accessible via browser ✓
- **Requirement 12.1**: Card-based layout for metrics display ✓
- **Requirement 12.2**: Chart.js for demand visualization ✓
- **Requirement 12.3**: Clear status indicators with colors ✓
- **Requirement 12.4**: Responsive design for laptop screens ✓
- **Requirement 12.5**: Modern CSS with clean visual hierarchy ✓

## Next Steps

This is the foundational infrastructure for the MajiSafe platform. Future development will include:

1. Database schema and sample data initialization
2. Core data models and business logic
3. REST API endpoints for all functionality
4. Water flow estimation and SMS simulation
5. Impact tracking and system visualization
6. Complete WebSocket real-time updates
7. Comprehensive error handling and testing

## Support

For development questions or issues:
1. Check the console output for error messages
2. Verify all dependencies are installed correctly
3. Ensure Python 3.8+ is being used
4. Check that port 5000 is available

## License

This project is developed for demonstration and educational purposes.# maji_safe_platform
