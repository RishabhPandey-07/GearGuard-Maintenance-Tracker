"""
GearGuard - Database Module
Handles SQLite database operations, schema creation, and data management
"""

import sqlite3
from datetime import datetime, date
from typing import List, Dict, Optional
import json

class Database:
    def __init__(self, db_name: str = "gearguard.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Create a database connection"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database with all required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Teams Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Team Members Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS team_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                role TEXT,
                email TEXT,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
            )
        ''')
        
        # Equipment Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS equipment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                serial_number TEXT UNIQUE NOT NULL,
                category TEXT NOT NULL,
                department TEXT NOT NULL,
                assigned_employee TEXT,
                purchase_date DATE,
                warranty_expiry DATE,
                location TEXT,
                status TEXT DEFAULT 'Usable',
                team_id INTEGER,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (team_id) REFERENCES teams(id)
            )
        ''')
        
        # Maintenance Requests Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS maintenance_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                equipment_id INTEGER NOT NULL,
                request_type TEXT NOT NULL,
                scheduled_date DATE NOT NULL,
                duration_hours REAL DEFAULT 1.0,
                stage TEXT DEFAULT 'New',
                assigned_technician TEXT,
                team_id INTEGER,
                department TEXT,
                priority TEXT DEFAULT 'Medium',
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (equipment_id) REFERENCES equipment(id),
                FOREIGN KEY (team_id) REFERENCES teams(id)
            )
        ''')
        
        # Activity Log Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                equipment_id INTEGER,
                request_id INTEGER,
                action TEXT NOT NULL,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (equipment_id) REFERENCES equipment(id),
                FOREIGN KEY (request_id) REFERENCES maintenance_requests(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Initialize with sample data if tables are empty
        self.seed_data()
    
    def seed_data(self):
        """Seed database with initial data if empty"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if teams exist
        cursor.execute("SELECT COUNT(*) FROM teams")
        if cursor.fetchone()[0] == 0:
            teams = [
                ('Mechanics', 'Mechanical equipment maintenance'),
                ('Electricians', 'Electrical systems and wiring'),
                ('IT Support', 'Computer and network equipment'),
                ('HVAC', 'Heating, ventilation, and air conditioning'),
                ('Facilities', 'Building and general maintenance')
            ]
            cursor.executemany('INSERT INTO teams (name, description) VALUES (?, ?)', teams)
        
        # Check if equipment exists
        cursor.execute("SELECT COUNT(*) FROM equipment")
        if cursor.fetchone()[0] == 0:
            equipment = [
                ('CNC Machine A1', 'CNC-2024-001', 'Machinery', 'Production', 'John Smith', 
                 '2024-01-15', '2026-01-15', 'Factory Floor A', 'Usable', 1),
                ('Hydraulic Press B2', 'HYD-2024-002', 'Machinery', 'Production', 'Jane Doe', 
                 '2024-02-20', '2026-02-20', 'Factory Floor B', 'Usable', 1),
                ('Industrial Generator', 'GEN-2024-003', 'Electrical', 'Maintenance', 'Mike Johnson', 
                 '2024-03-10', '2027-03-10', 'Power Room', 'Usable', 2),
                ('Server Rack Main', 'SRV-2024-004', 'IT Equipment', 'IT Department', 'Sarah Williams', 
                 '2024-04-05', '2027-04-05', 'Data Center', 'Usable', 3),
                ('HVAC Unit North', 'HVAC-2024-005', 'Climate Control', 'Facilities', 'Robert Brown', 
                 '2024-05-12', '2026-05-12', 'Roof North', 'Usable', 4),
                ('Conveyor Belt C3', 'CNV-2024-006', 'Machinery', 'Production', 'Emily Davis', 
                 '2024-06-18', '2026-06-18', 'Factory Floor C', 'Usable', 1),
                ('Backup Generator', 'GEN-2024-007', 'Electrical', 'Maintenance', 'David Wilson', 
                 '2024-07-22', '2027-07-22', 'Power Room', 'Usable', 2),
                ('Forklift FL-12', 'FRK-2024-008', 'Vehicles', 'Logistics', 'Lisa Anderson', 
                 '2024-08-30', '2025-08-30', 'Warehouse A', 'Usable', 5),
            ]
            cursor.executemany('''
                INSERT INTO equipment (name, serial_number, category, department, assigned_employee,
                                     purchase_date, warranty_expiry, location, status, team_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', equipment)
        
        # Check if maintenance requests exist
        cursor.execute("SELECT COUNT(*) FROM maintenance_requests")
        if cursor.fetchone()[0] == 0:
            requests = [
                ('Monthly Oil Change', 1, 'Preventive', '2024-12-28', 2.0, 'In Progress', 
                 'John Smith', 1, 'Production', 'Medium', 'Regular monthly maintenance'),
                ('Hydraulic Leak Repair', 2, 'Corrective', '2024-12-27', 4.0, 'New', 
                 'Jane Doe', 1, 'Production', 'High', 'Oil leak detected on hydraulic press'),
                ('Generator Load Test', 3, 'Preventive', '2024-12-29', 3.0, 'New', 
                 'Mike Johnson', 2, 'Maintenance', 'Medium', 'Quarterly load test'),
                ('Server Cooling Issue', 4, 'Corrective', '2024-12-26', 2.0, 'Repaired', 
                 'Sarah Williams', 3, 'IT Department', 'Critical', 'Server overheating detected'),
                ('HVAC Filter Replacement', 5, 'Preventive', '2024-12-30', 1.5, 'New', 
                 'Robert Brown', 4, 'Facilities', 'Low', 'Scheduled filter replacement'),
                ('Conveyor Belt Alignment', 6, 'Corrective', '2024-12-27', 3.0, 'In Progress', 
                 'Emily Davis', 1, 'Production', 'High', 'Belt misalignment causing jams'),
                ('Forklift Battery Check', 8, 'Preventive', '2024-12-31', 1.0, 'New', 
                 'Lisa Anderson', 5, 'Logistics', 'Low', 'Weekly battery inspection'),
            ]
            cursor.executemany('''
                INSERT INTO maintenance_requests (subject, equipment_id, request_type, scheduled_date,
                                                 duration_hours, stage, assigned_technician, team_id,
                                                 department, priority, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', requests)
        
        # Check if team members exist
        cursor.execute("SELECT COUNT(*) FROM team_members")
        if cursor.fetchone()[0] == 0:
            team_members = [
                # Mechanics Team (team_id=1)
                (1, 'John Smith', 'Senior Technician', 'john.smith@company.com', '555-0101'),
                (1, 'Jane Doe', 'Mechanic Lead', 'jane.doe@company.com', '555-0102'),
                (1, 'Emily Davis', 'Technician', 'emily.davis@company.com', '555-0103'),
                (1, 'Tom Baker', 'Apprentice', 'tom.baker@company.com', '555-0104'),
                # Electricians Team (team_id=2)
                (2, 'Mike Johnson', 'Master Electrician', 'mike.johnson@company.com', '555-0201'),
                (2, 'David Wilson', 'Electrician', 'david.wilson@company.com', '555-0202'),
                (2, 'Chris Martin', 'Electrical Technician', 'chris.martin@company.com', '555-0203'),
                # IT Support Team (team_id=3)
                (3, 'Sarah Williams', 'IT Manager', 'sarah.williams@company.com', '555-0301'),
                (3, 'Alex Turner', 'System Administrator', 'alex.turner@company.com', '555-0302'),
                (3, 'Nina Patel', 'IT Support Specialist', 'nina.patel@company.com', '555-0303'),
                # HVAC Team (team_id=4)
                (4, 'Robert Brown', 'HVAC Technician', 'robert.brown@company.com', '555-0401'),
                (4, 'James Lee', 'HVAC Specialist', 'james.lee@company.com', '555-0402'),
                # Facilities Team (team_id=5)
                (5, 'Lisa Anderson', 'Facilities Manager', 'lisa.anderson@company.com', '555-0501'),
                (5, 'Mark Thompson', 'Maintenance Worker', 'mark.thompson@company.com', '555-0502'),
            ]
            cursor.executemany('''
                INSERT INTO team_members (team_id, name, role, email, phone)
                VALUES (?, ?, ?, ?, ?)
            ''', team_members)
        
        conn.commit()
        conn.close()
    
    # ============ EQUIPMENT OPERATIONS ============
    
    def add_equipment(self, data: Dict) -> int:
        """Add new equipment"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO equipment (name, serial_number, category, department, assigned_employee,
                                 purchase_date, warranty_expiry, location, status, team_id, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'], data['serial_number'], data['category'], data['department'],
            data.get('assigned_employee'), data.get('purchase_date'), data.get('warranty_expiry'),
            data.get('location'), data.get('status', 'Usable'), data.get('team_id'), data.get('notes')
        ))
        
        equipment_id = cursor.lastrowid
        
        # Log activity
        self.log_activity(equipment_id=equipment_id, action='Equipment Created', 
                         details=f"Equipment '{data['name']}' added to system")
        
        conn.commit()
        conn.close()
        return equipment_id
    
    def get_all_equipment(self) -> List[Dict]:
        """Get all equipment with team information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT e.*, t.name as team_name
            FROM equipment e
            LEFT JOIN teams t ON e.team_id = t.id
            ORDER BY e.created_at DESC
        ''')
        
        equipment = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return equipment
    
    def get_equipment_by_id(self, equipment_id: int) -> Optional[Dict]:
        """Get equipment by ID with team information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT e.*, t.name as team_name
            FROM equipment e
            LEFT JOIN teams t ON e.team_id = t.id
            WHERE e.id = ?
        ''', (equipment_id,))
        
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def update_equipment(self, equipment_id: int, data: Dict):
        """Update equipment information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE equipment
            SET name=?, serial_number=?, category=?, department=?, assigned_employee=?,
                purchase_date=?, warranty_expiry=?, location=?, status=?, team_id=?, notes=?
            WHERE id=?
        ''', (
            data['name'], data['serial_number'], data['category'], data['department'],
            data.get('assigned_employee'), data.get('purchase_date'), data.get('warranty_expiry'),
            data.get('location'), data.get('status', 'Usable'), data.get('team_id'), 
            data.get('notes'), equipment_id
        ))
        
        self.log_activity(equipment_id=equipment_id, action='Equipment Updated', 
                         details=f"Equipment information modified")
        
        conn.commit()
        conn.close()
    
    def scrap_equipment(self, equipment_id: int, reason: str):
        """Mark equipment as scrapped"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE equipment SET status=? WHERE id=?', ('Scrapped', equipment_id))
        
        self.log_activity(equipment_id=equipment_id, action='Equipment Scrapped', 
                         details=f"Equipment marked as scrapped. Reason: {reason}")
        
        conn.commit()
        conn.close()
    
    def get_equipment_request_count(self, equipment_id: int) -> int:
        """Get count of open maintenance requests for equipment"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM maintenance_requests
            WHERE equipment_id = ? AND stage NOT IN ('Repaired', 'Scrap')
        ''', (equipment_id,))
        
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    # ============ TEAM OPERATIONS ============
    
    def add_team(self, name: str, description: str = '') -> int:
        """Add new team"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('INSERT INTO teams (name, description) VALUES (?, ?)', (name, description))
        team_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        return team_id
    
    def get_all_teams(self) -> List[Dict]:
        """Get all teams"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM teams ORDER BY name')
        teams = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return teams
    
    def get_team_by_id(self, team_id: int) -> Optional[Dict]:
        """Get team by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM teams WHERE id = ?', (team_id,))
        row = cursor.fetchone()
        
        conn.close()
        return dict(row) if row else None
    
    # ============ MAINTENANCE REQUEST OPERATIONS ============
    
    def add_maintenance_request(self, data: Dict) -> int:
        """Add new maintenance request with auto-fill logic"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Auto-fill department and team from equipment
        equipment = self.get_equipment_by_id(data['equipment_id'])
        if equipment:
            data['department'] = equipment['department']
            data['team_id'] = equipment['team_id']
        
        cursor.execute('''
            INSERT INTO maintenance_requests (subject, equipment_id, request_type, scheduled_date,
                                             duration_hours, stage, assigned_technician, team_id,
                                             department, priority, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['subject'], data['equipment_id'], data['request_type'], data['scheduled_date'],
            data.get('duration_hours', 1.0), data.get('stage', 'New'), 
            data.get('assigned_technician'), data.get('team_id'), data.get('department'),
            data.get('priority', 'Medium'), data.get('description')
        ))
        
        request_id = cursor.lastrowid
        
        self.log_activity(equipment_id=data['equipment_id'], request_id=request_id,
                         action='Maintenance Request Created', 
                         details=f"Request '{data['subject']}' created")
        
        conn.commit()
        conn.close()
        return request_id
    
    def get_all_requests(self) -> List[Dict]:
        """Get all maintenance requests with equipment and team info"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT mr.*, e.name as equipment_name, e.serial_number, t.name as team_name
            FROM maintenance_requests mr
            LEFT JOIN equipment e ON mr.equipment_id = e.id
            LEFT JOIN teams t ON mr.team_id = t.id
            ORDER BY mr.created_at DESC
        ''')
        
        requests = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return requests
    
    def get_request_by_id(self, request_id: int) -> Optional[Dict]:
        """Get request by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT mr.*, e.name as equipment_name, e.serial_number, t.name as team_name
            FROM maintenance_requests mr
            LEFT JOIN equipment e ON mr.equipment_id = e.id
            LEFT JOIN teams t ON mr.team_id = t.id
            WHERE mr.id = ?
        ''', (request_id,))
        
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def update_request_stage(self, request_id: int, new_stage: str):
        """Update request stage with scrap logic"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get request details
        request = self.get_request_by_id(request_id)
        
        # Update stage
        cursor.execute('UPDATE maintenance_requests SET stage=? WHERE id=?', (new_stage, request_id))
        
        # If moved to Scrap, update equipment status
        if new_stage == 'Scrap' and request:
            self.scrap_equipment(request['equipment_id'], f"Maintenance request #{request_id} marked as scrap")
        
        # If completed, set completed timestamp
        if new_stage == 'Repaired':
            cursor.execute('UPDATE maintenance_requests SET completed_at=? WHERE id=?', 
                         (datetime.now(), request_id))
        
        self.log_activity(request_id=request_id, action='Stage Changed', 
                         details=f"Stage updated to {new_stage}")
        
        conn.commit()
        conn.close()
    
    def get_requests_by_equipment(self, equipment_id: int) -> List[Dict]:
        """Get all requests for specific equipment"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT mr.*, t.name as team_name
            FROM maintenance_requests mr
            LEFT JOIN teams t ON mr.team_id = t.id
            WHERE mr.equipment_id = ?
            ORDER BY mr.created_at DESC
        ''', (equipment_id,))
        
        requests = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return requests
    
    def get_requests_by_stage(self, stage: str) -> List[Dict]:
        """Get requests filtered by stage"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT mr.*, e.name as equipment_name, t.name as team_name
            FROM maintenance_requests mr
            LEFT JOIN equipment e ON mr.equipment_id = e.id
            LEFT JOIN teams t ON mr.team_id = t.id
            WHERE mr.stage = ?
            ORDER BY mr.scheduled_date
        ''', (stage,))
        
        requests = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return requests
    
    # ============ ANALYTICS ============
    
    def get_requests_by_team(self) -> List[Dict]:
        """Get request count grouped by team"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.name, COUNT(mr.id) as count
            FROM teams t
            LEFT JOIN maintenance_requests mr ON t.id = mr.team_id
            GROUP BY t.id, t.name
            ORDER BY count DESC
        ''')
        
        data = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return data
    
    def get_equipment_by_category(self) -> List[Dict]:
        """Get equipment count grouped by category"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT category, COUNT(*) as count
            FROM equipment
            GROUP BY category
            ORDER BY count DESC
        ''')
        
        data = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return data
    
    def get_dashboard_stats(self) -> Dict:
        """Get dashboard statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total equipment
        cursor.execute('SELECT COUNT(*) FROM equipment WHERE status = "Usable"')
        stats['total_equipment'] = cursor.fetchone()[0]
        
        # Active requests
        cursor.execute('SELECT COUNT(*) FROM maintenance_requests WHERE stage NOT IN ("Repaired", "Scrap")')
        stats['active_requests'] = cursor.fetchone()[0]
        
        # Overdue requests
        cursor.execute('''
            SELECT COUNT(*) FROM maintenance_requests 
            WHERE stage NOT IN ("Repaired", "Scrap") AND scheduled_date < date('now')
        ''')
        stats['overdue_requests'] = cursor.fetchone()[0]
        
        # Total teams
        cursor.execute('SELECT COUNT(*) FROM teams')
        stats['total_teams'] = cursor.fetchone()[0]
        
        # Critical requests
        cursor.execute('SELECT COUNT(*) FROM maintenance_requests WHERE priority = "Critical" AND stage NOT IN ("Repaired", "Scrap")')
        stats['critical_requests'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
    
    # ============ TEAM MEMBERS OPERATIONS ============
    
    def add_team_member(self, team_id: int, name: str, role: str = '', email: str = '', phone: str = '') -> int:
        """Add a new team member"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO team_members (team_id, name, role, email, phone)
            VALUES (?, ?, ?, ?, ?)
        ''', (team_id, name, role, email, phone))
        
        member_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return member_id
    
    def get_team_members(self, team_id: int) -> List[Dict]:
        """Get all members of a specific team"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, team_id, name, role, email, phone, created_at
            FROM team_members
            WHERE team_id = ?
            ORDER BY name
        ''', (team_id,))
        
        members = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return members
    
    def get_all_team_members(self) -> List[Dict]:
        """Get all team members with their team info"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT tm.id, tm.team_id, tm.name, tm.role, tm.email, tm.phone, 
                   t.name as team_name, tm.created_at
            FROM team_members tm
            JOIN teams t ON tm.team_id = t.id
            ORDER BY t.name, tm.name
        ''')
        
        members = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return members
    
    def remove_team_member(self, member_id: int):
        """Remove a team member"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM team_members WHERE id = ?', (member_id,))
        
        conn.commit()
        conn.close()
    
    def update_team_member(self, member_id: int, data: Dict):
        """Update team member information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE team_members
            SET name = ?, role = ?, email = ?, phone = ?
            WHERE id = ?
        ''', (data.get('name'), data.get('role'), data.get('email'), data.get('phone'), member_id))
        
        conn.commit()
        conn.close()
    
    # ============ ACTIVITY LOG ============
    
    def log_activity(self, equipment_id: Optional[int] = None, request_id: Optional[int] = None,
                     action: str = '', details: str = ''):
        """Log activity"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO activity_log (equipment_id, request_id, action, details)
            VALUES (?, ?, ?, ?)
        ''', (equipment_id, request_id, action, details))
        
        conn.commit()
        conn.close()
    
    def get_recent_activity(self, limit: int = 10) -> List[Dict]:
        """Get recent activity log"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT al.*, e.name as equipment_name, mr.subject as request_subject
            FROM activity_log al
            LEFT JOIN equipment e ON al.equipment_id = e.id
            LEFT JOIN maintenance_requests mr ON al.request_id = mr.id
            ORDER BY al.created_at DESC
            LIMIT ?
        ''', (limit,))
        
        activities = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return activities
