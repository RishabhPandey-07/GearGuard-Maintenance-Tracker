"""
GearGuard Flask Backend
Main application entry point
"""

from flask import Flask
from flask_cors import CORS
from database import db
from datetime import datetime, date
import os

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gearguard.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    app.config['JSON_SORT_KEYS'] = False
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Import models and routes (after app creation)
    with app.app_context():
        from models import Team, TeamMember, Equipment, MaintenanceRequest, ActivityLog
        from api import equipment_bp, requests_bp, teams_bp, dashboard_bp

        # Register blueprints
        app.register_blueprint(equipment_bp, url_prefix='/api/equipment')
        app.register_blueprint(requests_bp, url_prefix='/api/requests')
        app.register_blueprint(teams_bp, url_prefix='/api/teams')
        app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
        
        @app.route('/api/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
        
        @app.route('/')
        def index():
            """Root endpoint"""
            return {
                'message': 'GearGuard API',
                'version': '2.0',
                'endpoints': {
                    'equipment': '/api/equipment',
                    'requests': '/api/requests',
                    'teams': '/api/teams',
                    'dashboard': '/api/dashboard'
                }
            }
        
        # Initialize database
        db.create_all()
        
        # Check if data already exists
        if Team.query.count() == 0 and Equipment.query.count() == 0:
            # Seed teams
            teams_data = [
                Team(name='Mechanics', description='Mechanical equipment maintenance'),
                Team(name='Electricians', description='Electrical systems and wiring'),
                Team(name='IT Support', description='Computer and network equipment'),
                Team(name='HVAC', description='Heating, ventilation, and air conditioning'),
                Team(name='Facilities', description='Building and general maintenance')
            ]
            db.session.add_all(teams_data)
            db.session.commit()
            
            # Seed team members
            members_data = [
                # Mechanics Team (team_id=1)
                TeamMember(team_id=1, name='John Smith', role='Senior Technician', 
                          email='john.smith@company.com', phone='555-0101'),
                TeamMember(team_id=1, name='Jane Doe', role='Mechanic Lead',
                          email='jane.doe@company.com', phone='555-0102'),
                TeamMember(team_id=1, name='Emily Davis', role='Technician',
                          email='emily.davis@company.com', phone='555-0103'),
                TeamMember(team_id=1, name='Tom Baker', role='Apprentice',
                          email='tom.baker@company.com', phone='555-0104'),
                # Electricians Team (team_id=2)
                TeamMember(team_id=2, name='Mike Johnson', role='Master Electrician',
                          email='mike.johnson@company.com', phone='555-0201'),
                TeamMember(team_id=2, name='David Wilson', role='Electrician',
                          email='david.wilson@company.com', phone='555-0202'),
                TeamMember(team_id=2, name='Chris Martin', role='Electrical Technician',
                          email='chris.martin@company.com', phone='555-0203'),
                # IT Support Team (team_id=3)
                TeamMember(team_id=3, name='Sarah Williams', role='IT Manager',
                          email='sarah.williams@company.com', phone='555-0301'),
                TeamMember(team_id=3, name='Alex Turner', role='System Administrator',
                          email='alex.turner@company.com', phone='555-0302'),
                TeamMember(team_id=3, name='Nina Patel', role='IT Support Specialist',
                          email='nina.patel@company.com', phone='555-0303'),
                # HVAC Team (team_id=4)
                TeamMember(team_id=4, name='Robert Brown', role='HVAC Technician',
                          email='robert.brown@company.com', phone='555-0401'),
                TeamMember(team_id=4, name='James Lee', role='HVAC Specialist',
                          email='james.lee@company.com', phone='555-0402'),
                # Facilities Team (team_id=5)
                TeamMember(team_id=5, name='Lisa Anderson', role='Facilities Manager',
                          email='lisa.anderson@company.com', phone='555-0501'),
                TeamMember(team_id=5, name='Mark Thompson', role='Maintenance Worker',
                          email='mark.thompson@company.com', phone='555-0502'),
            ]
            db.session.add_all(members_data)
            db.session.commit()
            
            # Seed equipment
            equipment_data = [
                Equipment(name='Industrial Conveyor Belt A1', serial_number='CVB-001', 
                         category='Conveyor Systems', department='Production', 
                         assigned_employee='John Smith', purchase_date=date(2022, 1, 15),
                         warranty_expiry=date(2025, 1, 15), location='Factory Floor A',
                         status='Usable', team_id=1, notes='Main production line conveyor'),
                Equipment(name='Hydraulic Press HP-200', serial_number='HP-200-001',
                         category='Hydraulic Equipment', department='Manufacturing',
                         assigned_employee='Jane Doe', purchase_date=date(2021, 6, 10),
                         warranty_expiry=date(2024, 6, 10), location='Workshop B',
                         status='Usable', team_id=1, notes='Heavy duty hydraulic press'),
                Equipment(name='Main Electrical Panel', serial_number='EP-MAIN-001',
                         category='Electrical Systems', department='Facilities',
                         assigned_employee='Mike Johnson', purchase_date=date(2020, 3, 20),
                         warranty_expiry=date(2030, 3, 20), location='Electrical Room',
                         status='Usable', team_id=2, notes='Main building electrical distribution'),
                Equipment(name='Server Rack SR-01', serial_number='SR-01-2023',
                         category='IT Equipment', department='IT',
                         assigned_employee='Sarah Williams', purchase_date=date(2023, 2, 1),
                         warranty_expiry=date(2026, 2, 1), location='Server Room',
                         status='Usable', team_id=3, notes='Primary server infrastructure'),
                Equipment(name='HVAC Unit North Wing', serial_number='HVAC-N-001',
                         category='HVAC Systems', department='Facilities',
                         assigned_employee='Robert Brown', purchase_date=date(2019, 8, 15),
                         warranty_expiry=date(2024, 8, 15), location='North Wing Roof',
                         status='Usable', team_id=4, notes='Climate control for north wing'),
                Equipment(name='Emergency Generator', serial_number='GEN-EM-001',
                         category='Power Systems', department='Facilities',
                         assigned_employee='Lisa Anderson', purchase_date=date(2018, 11, 30),
                         warranty_expiry=date(2023, 11, 30), location='Generator Room',
                         status='Usable', team_id=5, notes='Backup power for critical systems'),
                Equipment(name='Forklift FL-03', serial_number='FL-03-2022',
                         category='Material Handling', department='Warehouse',
                         assigned_employee='Mark Thompson', purchase_date=date(2022, 4, 12),
                         warranty_expiry=date(2025, 4, 12), location='Warehouse',
                         status='Usable', team_id=1, notes='Warehouse material handling')
            ]
            db.session.add_all(equipment_data)
            db.session.commit()
            
            # Seed maintenance requests
            requests_data = [
                MaintenanceRequest(subject='Conveyor Belt Alignment Issue', equipment_id=1,
                                 request_type='Corrective', scheduled_date=date(2024, 1, 15),
                                 duration_hours=2.0, stage='New', assigned_technician='John Smith',
                                 team_id=1, department='Production', priority='High',
                                 description='Belt is misaligned causing product jams'),
                MaintenanceRequest(subject='Hydraulic Press Preventive Maintenance', equipment_id=2,
                                 request_type='Preventive', scheduled_date=date(2024, 1, 20),
                                 duration_hours=4.0, stage='In Progress', assigned_technician='Jane Doe',
                                 team_id=1, department='Manufacturing', priority='Medium',
                                 description='Quarterly preventive maintenance check'),
                MaintenanceRequest(subject='Electrical Panel Inspection', equipment_id=3,
                                 request_type='Preventive', scheduled_date=date(2024, 1, 25),
                                 duration_hours=1.5, stage='New', assigned_technician='Mike Johnson',
                                 team_id=2, department='Facilities', priority='Medium',
                                 description='Annual electrical safety inspection'),
                MaintenanceRequest(subject='Server Cooling System Check', equipment_id=4,
                                 request_type='Preventive', scheduled_date=date(2024, 1, 30),
                                 duration_hours=1.0, stage='Repaired', assigned_technician='Sarah Williams',
                                 team_id=3, department='IT', priority='Low',
                                 description='Monthly cooling system maintenance'),
                MaintenanceRequest(subject='HVAC Filter Replacement', equipment_id=5,
                                 request_type='Preventive', scheduled_date=date(2024, 2, 1),
                                 duration_hours=0.5, stage='New', assigned_technician='Robert Brown',
                                 team_id=4, department='Facilities', priority='Medium',
                                 description='Replace air filters in HVAC system'),
                MaintenanceRequest(subject='Generator Load Test', equipment_id=6,
                                 request_type='Preventive', scheduled_date=date(2024, 2, 5),
                                 duration_hours=3.0, stage='In Progress', assigned_technician='Lisa Anderson',
                                 team_id=5, department='Facilities', priority='Critical',
                                 description='Monthly generator load testing'),
                MaintenanceRequest(subject='Forklift Battery Replacement', equipment_id=7,
                                 request_type='Corrective', scheduled_date=date(2024, 1, 10),
                                 duration_hours=1.0, stage='Repaired', assigned_technician='Mark Thompson',
                                 team_id=1, department='Warehouse', priority='High',
                                 description='Battery not holding charge, needs replacement')
            ]
            db.session.add_all(requests_data)
            db.session.commit()
            
            print("Database initialized with seed data")
        else:
            print("Database already initialized")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000, host='0.0.0.0')