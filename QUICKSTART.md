# 🚀 GearGuard Quick Start Guide

## Running the Application

### Option 1: Windows (Easy - One-Click Start)
Double-click the `start.bat` file in the root directory.

This will:
1. Start Flask backend on http://localhost:5000
2. Start React frontend on http://localhost:3000
3. Automatically open your browser

### Option 2: Manual Start

#### Terminal 1 - Backend (Flask)
```bash
cd backend
python app.py
```
✅ Backend running on http://localhost:5000

#### Terminal 2 - Frontend (React)
```bash
cd frontend
npm run dev
```
✅ Frontend running on http://localhost:3000

### Option 3: Linux/Mac
```bash
chmod +x start.sh
./start.sh
```

---

## Access the Application

Open your browser and navigate to:
**http://localhost:3000**

The frontend automatically proxies API calls to the backend.

---

## Verify Connection

### Test Backend API
- http://localhost:5000/api/teams
- http://localhost:5000/api/dashboard/stats
- http://localhost:5000/api/equipment

### Test Frontend
- http://localhost:3000 (Dashboard)
- http://localhost:3000/equipment
- http://localhost:3000/requests
- http://localhost:3000/kanban
- http://localhost:3000/calendar
- http://localhost:3000/teams

---

## Architecture

```
┌─────────────────────┐
│   Browser           │
│  localhost:3000     │
└──────────┬──────────┘
           │
           │ HTTP Requests
           ▼
┌─────────────────────┐
│   Vite Dev Server   │  ◄── Proxy /api → :5000
│   React Frontend    │
│   Port 3000         │
└──────────┬──────────┘
           │
           │ Proxied API Calls
           │ /api/* → localhost:5000/api/*
           ▼
┌─────────────────────┐
│   Flask Backend     │
│   REST API          │
│   Port 5000         │
└──────────┬──────────┘
           │
           │ SQLAlchemy ORM
           ▼
┌─────────────────────┐
│   SQLite Database   │
│   gearguard.db      │
└─────────────────────┘
```

---

## API Integration

### How It Works

1. **Frontend makes request:**
   ```javascript
   // In React component
   await api.get('/teams')
   ```

2. **Axios uses relative URL:**
   ```javascript
   // axios.js
   baseURL: "/api"  // Relative to frontend
   ```

3. **Vite proxy forwards to backend:**
   ```javascript
   // vite.config.js
   proxy: {
     '/api': {
       target: 'http://localhost:5000',
       changeOrigin: true
     }
   }
   ```

4. **Flask handles the request:**
   ```python
   # Flask backend
   @teams_bp.route('/', methods=['GET'])
   def get_teams():
       # Returns JSON
   ```

5. **Response flows back to React**

---

## Troubleshooting

### Backend not starting?
- Check if port 5000 is already in use
- Verify Python dependencies: `pip install -r requirements.txt`
- Check for errors in backend terminal

### Frontend not starting?
- Check if port 3000 is in use
- Install dependencies: `npm install`
- Check for errors in frontend terminal

### API calls failing?
- Ensure both servers are running
- Check browser console (F12) for errors
- Verify backend is accessible: http://localhost:5000/api/teams
- Check CORS configuration in Flask backend

### CORS errors?
- Already configured! Flask has CORS enabled for all origins
- If issues persist, check Flask terminal for CORS warnings

### Data not loading?
1. Open browser DevTools (F12)
2. Go to Network tab
3. Check if API calls are being made
4. Look for any 404, 500, or CORS errors
5. Verify backend terminal shows incoming requests

---

## Development Workflow

### Making Changes

#### Backend Changes
- Edit files in `backend/` directory
- Flask will auto-reload (debug mode enabled)
- Check terminal for any errors

#### Frontend Changes
- Edit files in `frontend/src/` directory
- Vite will hot-reload instantly (HMR)
- Changes appear in browser immediately

### Adding New Features

1. **Create Backend Endpoint:**
   - Add route in `backend/api/*.py`
   - Update model in `backend/models.py` if needed

2. **Create Frontend Service:**
   - Add API call in `frontend/src/api/services.js`

3. **Update Component:**
   - Use the service in your React component
   - Update state with Context API if needed

---

## Production Deployment

### Backend
```bash
# Install production WSGI server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

### Frontend
```bash
# Build for production
npm run build

# Output in frontend/dist/
# Deploy to: Vercel, Netlify, or any static host
```

### Environment Variables
Create `.env` files:

**Backend (.env):**
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///gearguard.db
```

**Frontend (.env):**
```
VITE_API_URL=https://your-backend-domain.com/api
```

---

## Quick Reference

### Ports
- **Frontend:** 3000
- **Backend:** 5000

### URLs
- **App:** http://localhost:3000
- **API:** http://localhost:5000/api
- **API Docs:** http://localhost:5000

### Commands
```bash
# Backend
cd backend
python app.py

# Frontend
cd frontend
npm run dev

# Build Frontend
npm run build

# Install Backend Deps
pip install -r requirements.txt

# Install Frontend Deps
npm install
```

---

## Need Help?

1. Check browser console (F12)
2. Check backend terminal for errors
3. Check frontend terminal for errors
4. Verify both servers are running
5. Test API directly: http://localhost:5000/api/teams

---

**Happy coding! 🚀**
