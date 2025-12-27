# 🛠️ GearGuard - Maintenance Management System

> A modern, full-stack maintenance management application built with **Flask + React**

[![Flask](https://img.shields.io/badge/Flask-3.0+-black?style=flat&logo=flask)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18.2-blue?style=flat&logo=react)](https://react.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-06B6D4?style=flat&logo=tailwindcss)](https://tailwindcss.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite)](https://www.sqlite.org/)

## 📋 Overview

GearGuard is a comprehensive maintenance management system designed to track equipment, manage maintenance requests, coordinate teams, and visualize maintenance operations through interactive dashboards.

**Built with Flask + React** for production-ready, scalable architecture.

## 🌟 Key Features

### 1. **Smart Auto-Fill & Automation**
- **Auto-Fill Intelligence**: When creating maintenance requests, team and department automatically populate from equipment
- **Scrap Automation**: Moving requests to "Scrap" stage automatically updates equipment status to "Scrapped"
- **Activity Logging**: All changes tracked automatically in activity log

### 2. **Interactive UI Components**
- **📊 Dashboard**: Real-time statistics with Recharts (Bar & Pie charts)
- **📦 Equipment Management**: Grid view with CRUD operations and filters
- **🔧 Maintenance Requests**: List view with stage/priority filters
- **📋 Kanban Board**: Drag-and-drop task management across 4 stages
- **📅 Calendar**: Monthly view for preventive maintenance scheduling
- **👥 Teams**: Complete team and member management

### 3. **Modern Architecture**
- **RESTful API**: Flask backend with 28 endpoints
- **React SPA**: Modern frontend with React Router
- **State Management**: Context API for global state
- **Responsive Design**: Tailwind CSS with custom purple gradient theme
- **Real-time Updates**: Optimistic UI with instant feedback

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 20+
- npm or yarn

### Installation

1. **Clone and navigate to project directory**
   ```bash
   git clone <repository-url>
   cd gearguard
   ```

2. **Install Backend Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Install Frontend Dependencies**
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

**Option 1: Windows (One-Click Start)**
```bash
start.bat
```

**Option 2: Manual Start**
```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

**Access the app:** http://localhost:3000

## 📁 Project Structure

```
gearguard/
├── backend/                    # Flask REST API
│   ├── app.py                 # Application entry
│   ├── database.py            # SQLAlchemy instance
│   ├── models.py              # Database models
│   ├── requirements.txt       # Python dependencies
│   └── api/                   # API endpoints
│       ├── equipment.py
│       ├── requests.py
│       ├── teams.py
│       └── dashboard.py
│
├── frontend/                   # React SPA
│   ├── src/
│   │   ├── pages/            # Page components
│   │   ├── components/       # Reusable components
│   │   ├── api/             # API services
│   │   └── context/         # State management
│   ├── package.json
│   └── vite.config.js       # Vite + proxy config
│
├── start.bat                  # Windows startup
├── start.sh                   # Linux/Mac startup
└── README.md                  # This file
```

## 🎯 Core Workflows

### Corrective Maintenance (Breakdown)
1. Equipment breaks down
2. User creates a "Corrective" maintenance request
3. System auto-fills Department and Team based on equipment
4. Technician assigned and request moves through stages
5. If unrepairable, move to "Scrap" → Equipment auto-flagged

### Preventive Maintenance (Scheduled)
1. Create "Preventive" maintenance request
2. Set scheduled date (appears in Calendar View)
3. Technician performs routine maintenance
4. Mark as "Repaired" when complete

## 💡 Smart Features

### 1. **Auto-Fill Logic** ✨
- When you select equipment in the maintenance request form
- The system automatically fetches and displays the linked Department and Team
- **Demo this**: Create a new request → Watch auto-fill in action

### 2. **Smart Buttons** 🔘
- Equipment cards show real-time count of open requests
- Click to filter maintenance history for that specific asset
- **Demo this**: Go to Equipment → View Details → See smart button

### 3. **Equipment Scrap Integration** 🔗
- Move a maintenance request to "Scrap" stage
- Equipment status automatically changes to "Scrapped"
- Activity log records the reason and timestamp
- **Demo this**: Kanban Board → Move request to Scrap → Check Equipment status

### 4. **Visual Kanban with Overdue Detection** ⚠️
- Cards display with red borders if overdue
- Technician avatars with initials
- Priority color coding (Critical = Red, High = Orange, etc.)
- **Demo this**: Kanban Board → See visual indicators

### 5. **Calendar Timeline for Preventive Maintenance** 📅
- Interactive calendar showing scheduled maintenance
- Filter upcoming tasks for next 30 days
- **Demo this**: Calendar View → See preventive schedule

## 📊 Database Schema

### Equipment Table
- ID, Name, Serial Number, Category, Department
- Assigned Employee, Purchase Date, Warranty Info
- Location, Status (Usable/Scrapped)
- Team ID (Foreign Key → Teams)

### Teams Table
- ID, Team Name, Description

### Maintenance Requests Table
- ID, Subject, Equipment ID (FK), Type (Corrective/Preventive)
- Scheduled Date, Duration, Stage, Assigned Technician
- Team ID (FK), Department (auto-filled), Priority

### Activity Log Table
- ID, Equipment ID (FK), Request ID (FK)
- Action, Details, Timestamp

## 🎨 UI Highlights
- **Purple Gradient Theme**: Professional navigation and buttons
- **Glass Card Layout**: Modern, clean containers with backdrop blur
- **Custom Badges**: Color-coded status/priority indicators
- **Hover Effects**: Smooth transitions on cards
- **Interactive Charts**: Recharts visualizations
- **Responsive Design**: Works on different screen sizes

## 📈 Sample Data

The application comes pre-loaded with:
- 5 Maintenance Teams (Mechanics, Electricians, IT, HVAC, Facilities)
- 7 Equipment items across different categories
- 7 Sample maintenance requests in various stages
- Activity logs showing system interactions

## 🏆 Demo Guide

1. **Start with Dashboard**: Show the analytics and real-time metrics
2. **Demo Auto-Fill**: Create a new maintenance request
3. **Show Smart Button**: View equipment details and click open requests badge
4. **Demonstrate Scrap Logic**: Move a request to Scrap → Show equipment status change
5. **Walk Through Kanban**: Highlight overdue indicators and visual design
6. **Show Calendar**: Display preventive maintenance timeline

## 🔧 Technologies Used

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Embedded database
- **Flask-CORS**: Cross-origin resource sharing

### Frontend
- **React**: UI library with hooks
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **Recharts**: Chart library for data visualization
- **Axios**: HTTP client for API calls
- **Lucide React**: Icon library
- **Vite**: Build tool and dev server

## 📝 API Endpoints

### Equipment
- `GET /api/equipment` - Get all equipment
- `POST /api/equipment` - Create equipment
- `PUT /api/equipment/:id` - Update equipment
- `DELETE /api/equipment/:id` - Delete equipment

### Maintenance Requests
- `GET /api/requests` - Get all requests
- `POST /api/requests` - Create request
- `PUT /api/requests/:id` - Update request
- `DELETE /api/requests/:id` - Delete request

### Teams
- `GET /api/teams` - Get all teams
- `POST /api/teams` - Create team
- `GET /api/teams/members` - Get all members
- `POST /api/teams/members` - Create member

### Dashboard
- `GET /api/dashboard/stats` - Get statistics
- `GET /api/dashboard/requests-by-team` - Chart data
- `GET /api/dashboard/equipment-by-category` - Chart data

## 🤝 Contributing

This is a demonstration project built to showcase:
- Clean architecture with separation of concerns
- Relational database best practices
- Professional UI/UX design
- Smart business logic implementation

## 📄 License

Built for educational and demonstration purposes.

---

**Built with ❤️ for Modern Maintenance Management**

_Key differentiators: Smart Auto-fill, Equipment Scrap Integration, Visual Kanban, and Professional Glass-morphism UI_