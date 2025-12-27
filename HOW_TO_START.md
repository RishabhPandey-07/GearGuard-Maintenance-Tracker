# 🚀 GearGuard Quick Launch Guide

## ✅ Backend is Working!

Your Flask backend is **running perfectly** on port 5000!

---

## 🎯 HOW TO START THE APPLICATION

### **Option 1: EASY - Double-Click to Start Everything** ⭐ RECOMMENDED

Just double-click: **`START_ALL.bat`**

This will:
- ✅ Start Backend Server (Port 5000)
- ✅ Start Frontend Server (Port 3000)
- ✅ Open your browser automatically

---

### **Option 2: Start Servers Separately**

1. Double-click **`START_BACKEND.bat`** (starts Flask)
2. Double-click **`START_FRONTEND.bat`** (starts React)
3. Open browser to: http://localhost:3000

---

### **Option 3: Manual Terminal Commands**

**Backend Terminal:**
```bash
cd backend
python run.py
```

**Frontend Terminal (in a NEW terminal):**
```bash
cd frontend
npm run dev
```

---

## 🛑 HOW TO STOP THE SERVERS

Double-click: **`STOP_ALL.bat`**

OR just close the server windows manually.

---

## 🌐 Application URLs

| Service | URL |
|---------|-----|
| **Frontend (Main App)** | http://localhost:3000 |
| **Backend API** | http://localhost:5000 |
| **API Health Check** | http://localhost:5000/api/health |

---

## ✨ What's Working

- ✅ Flask Backend running on port 5000
- ✅ Database initialized with sample data
- ✅ All 28 API endpoints ready
- ✅ CORS enabled for frontend connection
- ✅ 5 Teams with 14 members seeded
- ✅ 7 Equipment items with maintenance history

---

## 🎨 Frontend Features

- 📊 Dashboard with charts
- 🔧 Equipment management
- 📝 Maintenance requests
- 📋 Kanban board
- 📅 Calendar view
- 👥 Teams management

---

## 📁 File Structure

```
gearguard/
├── START_ALL.bat          👈 Click this to start everything!
├── START_BACKEND.bat      Backend only
├── START_FRONTEND.bat     Frontend only
├── STOP_ALL.bat          Stop all servers
├── backend/
│   ├── run.py            Flask server entry
│   ├── app.py            Application factory
│   ├── database.py       SQLAlchemy instance
│   ├── models.py         Database models
│   └── api/              API blueprints
└── frontend/
    ├── src/
    │   ├── pages/        All 6 pages
    │   ├── context/      State management
    │   └── api/          API services
    └── package.json
```

---

## 🔥 Ready to Use!

**Just double-click `START_ALL.bat` and you're good to go!**

The backend is already tested and working perfectly. All database tables are ready with sample data.

---

## 💡 Tips

1. Keep both server windows open while using the app
2. Backend shows real-time API logs
3. Frontend has hot-reload for code changes
4. Use STOP_ALL.bat to cleanly shutdown everything

---

## 🆘 Troubleshooting

**Port 5000 already in use?**
- Run STOP_ALL.bat first
- Or manually kill Python/Node processes

**Frontend won't connect?**
- Make sure backend is running first
- Check backend window for errors

**Need fresh start?**
- Run STOP_ALL.bat
- Delete backend/instance/gearguard.db
- Run START_ALL.bat again

---

**Happy Maintenance Management! 🔧**
