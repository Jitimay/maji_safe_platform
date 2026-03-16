# MajiSafe Platform - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
python setup.py
```

### Step 2: Start the Platform
```bash
python run.py
```

### Step 3: Open in Browser
Navigate to: **http://localhost:5000**

---

## 🎯 Demo Features

### Dashboard Metrics
- View total water distributed in liters
- Monitor current water requests
- Track communities served
- See real-time pump status

### Pump Control
- **Start/Stop Village A Pump** - Control water flow to Village A
- **Start/Stop Village B Pump** - Control water flow to Village B
- **Runtime Tracking** - Monitor how long pumps have been running
- **Water Calculation** - Automatic calculation at 20L/min flow rate

### SMS Request Simulation
- Click **"Village A Request"** to simulate water request from Village A
- Click **"Village B Request"** to simulate water request from Village B
- Watch the demand chart update in real-time
- See how requests affect water distribution

### Community Demand Monitoring
- Interactive bar chart showing demand by village
- Real-time updates as requests are added
- Visual comparison between villages

### Impact Metrics
- **Total Water Distributed** - Cumulative liters delivered
- **People Served** - Estimated based on 20L per person per day
- **Communities Served** - Number of active villages

### System Map
- Visual topology showing water infrastructure
- **Green pumps** = Active/Running
- **Red pumps** = Inactive/Stopped
- Shows water tank and village connections

### Activity Log
- Chronological timeline of all system events
- Pump start/stop events
- SMS request notifications
- Water distribution records
- Limited to 50 most recent events

---

## 🎬 Demo Scenario

Try this sequence to demonstrate the platform:

1. **Add Water Requests**
   - Click "Village A Request" 3 times
   - Click "Village B Request" 2 times
   - Watch the demand chart update

2. **Start Pumps**
   - Click "Start Pump" for Village A
   - Watch the pump indicator turn green on the map
   - See the runtime counter start

3. **Monitor Impact**
   - Scroll to Impact Metrics section
   - Watch water distributed increase
   - See people served calculation update

4. **Check Activity Log**
   - Scroll to Activity Log section
   - See all events logged with timestamps
   - Notice color-coded event types

5. **Stop Pumps**
   - Click "Stop Pump" for Village A
   - Watch the pump indicator turn red
   - See final runtime recorded

---

## 📊 Technical Details

### Technology Stack
- **Backend**: Python 3.8+ with Flask
- **Database**: SQLite (local file-based)
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js
- **Real-time**: WebSocket via Flask-SocketIO

### Database Schema
- **villages** - Community information and demand tracking
- **pumps** - Pump status, runtime, and control
- **water_distribution** - Distribution records and allocation
- **activity_log** - System event logging
- **sms_requests** - SMS request simulation tracking

### API Endpoints
The platform includes 25+ REST API endpoints:
- Dashboard metrics
- Pump control (start/stop/status/runtime)
- Demand monitoring
- Distribution calculation
- Water flow estimation
- SMS simulation
- Impact tracking
- System map data
- Activity logging

---

## 🔧 Troubleshooting

### Port Already in Use
If port 5000 is already in use:
```bash
# Find and kill the process using port 5000
lsof -ti:5000 | xargs kill -9
```

### Database Issues
If you encounter database errors:
```bash
# Reset the database
rm -rf backend/data/majisafe.db
python run.py  # Will recreate database automatically
```

### Dependencies Not Installing
Make sure you have Python 3.8 or higher:
```bash
python --version
```

If using Python 3.8+, try manual installation:
```bash
pip install flask flask-cors flask-socketio
```

---

## 📁 Project Structure

```
majisafe-platform/
├── backend/
│   ├── app.py              # Main Flask application (25+ API endpoints)
│   ├── database.py         # Database manager and schema
│   ├── models.py           # Data models (Village, Pump, etc.)
│   ├── init_db.py          # Database initialization script
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── templates/
│   │   └── index.html      # Main dashboard page
│   └── static/
│       ├── css/
│       │   └── style.css   # Platform styling
│       └── js/
│           └── app.js      # Frontend JavaScript
├── data/                   # Database storage (auto-created)
├── setup.py               # Dependency installer
├── run.py                 # Application launcher
├── README.md              # Full documentation
└── QUICKSTART.md          # This file
```

---

## 🎓 For Judges & Stakeholders

### Key Demonstration Points

1. **Real-time Monitoring**
   - All metrics update automatically
   - WebSocket-powered live updates
   - No page refresh needed

2. **Smart Distribution**
   - Water allocated based on demand ratios
   - Automatic calculation and logging
   - Fair distribution algorithm

3. **Community Engagement**
   - SMS-based request system (simulated)
   - Easy for villagers to request water
   - Transparent demand tracking

4. **Impact Measurement**
   - Clear metrics for NGO reporting
   - People served calculations
   - Historical activity tracking

5. **Scalability**
   - Easy to add more villages
   - Extensible database schema
   - Modular API design

### Business Value

- **For NGOs**: Track water distribution impact and report to donors
- **For Governments**: Monitor rural water infrastructure efficiently
- **For Communities**: Fair, demand-based water allocation
- **For Operators**: Remote pump control and system monitoring

---

## 📞 Support

For technical questions or issues during the demo:
1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure Python 3.8+ is being used
4. Check that port 5000 is available

---

## 🌟 Next Steps

This is a demonstration prototype. Production deployment would include:
- Real SMS gateway integration
- IoT sensor integration for actual pump control
- Multi-tenancy for multiple regions
- Advanced analytics and reporting
- Mobile app for field technicians
- Cloud deployment with scalability
- Security hardening and authentication

---

**Built with ❤️ for rural water infrastructure management**
