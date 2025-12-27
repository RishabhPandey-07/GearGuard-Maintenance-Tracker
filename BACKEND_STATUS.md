# GearGuard Backend - Status & Troubleshooting

## ✅ Backend Status: WORKING

The backend has been tested and verified to be working correctly.

### Test Results:
- ✅ All modules import successfully
- ✅ Flask app creates without errors
- ✅ Database connected with sample data
  - 5 Teams
  - 7 Equipment items
  - 7 Maintenance Requests
- ✅ All API endpoints responding correctly

---

## 🚀 How to Start the Backend

### Option 1: Use the startup script (Recommended)
```bash
# Windows
start.bat

# This will start both backend and frontend automatically
```

### Option 2: Start backend manually
```bash
cd backend
python run.py
```

The backend will start on **http://localhost:5000**

---

## 🔍 Verify Backend is Working

Run the status check script:
```bash
python check_backend.py
```

This will test:
- Module imports
- Flask app creation
- Database connectivity
- All API endpoints

---

## 📡 API Endpoints

All endpoints are working and tested:

### Core Endpoints
- `GET /api/health` - Health check
- `GET /` - API information

### Equipment
- `GET /api/equipment/` - Get all equipment
- `POST /api/equipment/` - Create equipment
- `PUT /api/equipment/<id>` - Update equipment
- `DELETE /api/equipment/<id>` - Delete equipment

### Maintenance Requests
- `GET /api/requests/` - Get all requests
- `POST /api/requests/` - Create request
- `PUT /api/requests/<id>` - Update request
- `DELETE /api/requests/<id>` - Delete request

### Teams
- `GET /api/teams/` - Get all teams
- `POST /api/teams/` - Create team
- `GET /api/teams/members` - Get all members
- `POST /api/teams/members` - Create member

### Dashboard
- `GET /api/dashboard/stats` - Get statistics
- `GET /api/dashboard/requests-by-team` - Chart data
- `GET /api/dashboard/equipment-by-category` - Chart data

---

## 🐛 Troubleshooting

### Issue: Backend won't start

**Solution 1: Check dependencies**
```bash
cd backend
pip install -r requirements.txt
```

**Solution 2: Check if port 5000 is in use**
```bash
# Windows
netstat -ano | findstr :5000

# If port is in use, kill the process or change port in app.py
```

**Solution 3: Reset database**
```bash
# Delete the database file
del backend\instance\gearguard.db

# Restart backend (will recreate with sample data)
cd backend
python run.py
```

### Issue: Database is empty

The database auto-seeds on first run. If it's empty:
1. Delete `backend/instance/gearguard.db`
2. Restart the backend
3. Sample data will be automatically created

### Issue: Import errors

Make sure you're in the correct directory:
```bash
cd backend
python run.py
```

### Issue: Unicode encoding errors

This has been fixed. If you still see them:
- Make sure you're using the latest version of the files
- Check that print statements don't contain emoji or special Unicode characters

---

## 📊 Sample Data Included

The backend comes with pre-loaded sample data:

### Teams (5)
- Mechanics
- Electricians
- IT Support
- HVAC
- Facilities

### Equipment (7)
- Industrial Conveyor Belt A1
- Hydraulic Press HP-200
- Main Electrical Panel
- Server Rack SR-01
- HVAC Unit North Wing
- Emergency Generator
- Forklift FL-03

### Maintenance Requests (7)
- Mix of Corrective and Preventive maintenance
- Various stages: New, In Progress, Repaired
- Different priorities: Low, Medium, High, Critical

---

## 🔧 Configuration

### Database
- Type: SQLite
- Location: `backend/instance/gearguard.db`
- Auto-creates on first run

### Server
- Host: 0.0.0.0 (accessible from network)
- Port: 5000
- Debug: True (disable in production)

### CORS
- Enabled for all origins (configure for production)

---

## ✨ Smart Features Working

1. **Auto-fill Logic**: When creating a request, selecting equipment auto-fills team and department
2. **Scrap Integration**: Moving request to "Scrap" stage automatically updates equipment status
3. **Activity Logging**: All changes are logged automatically
4. **Relational Data**: Proper foreign keys and relationships between tables

---

## 📝 Next Steps

1. Start the backend: `cd backend && python run.py`
2. Start the frontend: `cd frontend && npm run dev`
3. Open browser: http://localhost:3000
4. Test the application features

---

**Backend is ready and fully functional! 🎉**