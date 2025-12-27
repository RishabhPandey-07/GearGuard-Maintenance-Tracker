"""
GearGuard Database Models
SQLAlchemy ORM models for all database tables
"""

from database import db
from datetime import datetime
from sqlalchemy import func

class Team(db.Model):
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    members = db.relationship('TeamMember', backref='team', lazy=True, cascade='all, delete-orphan')
    equipment = db.relationship('Equipment', backref='team', lazy=True)
    requests = db.relationship('MaintenanceRequest', backref='team', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'member_count': len(self.members),
            'equipment_count': len(self.equipment)
        }

class TeamMember(db.Model):
    __tablename__ = 'team_members'
    
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'team_id': self.team_id,
            'team_name': self.team.name if self.team else None,
            'name': self.name,
            'role': self.role,
            'email': self.email,
            'phone': self.phone,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Equipment(db.Model):
    __tablename__ = 'equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    serial_number = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    assigned_employee = db.Column(db.String(100))
    purchase_date = db.Column(db.Date)
    warranty_expiry = db.Column(db.Date)
    location = db.Column(db.String(200))
    status = db.Column(db.String(50), default='Usable')
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    requests = db.relationship('MaintenanceRequest', backref='equipment', lazy=True)
    activity_logs = db.relationship('ActivityLog', backref='equipment', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'serial_number': self.serial_number,
            'category': self.category,
            'department': self.department,
            'assigned_employee': self.assigned_employee,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'warranty_expiry': self.warranty_expiry.isoformat() if self.warranty_expiry else None,
            'location': self.location,
            'status': self.status,
            'team_id': self.team_id,
            'team_name': self.team.name if self.team else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'request_count': len([r for r in self.requests if r.stage not in ['Repaired', 'Scrap']])
        }

class MaintenanceRequest(db.Model):
    __tablename__ = 'maintenance_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    request_type = db.Column(db.String(50), nullable=False)  # Corrective or Preventive
    scheduled_date = db.Column(db.Date, nullable=False)
    duration_hours = db.Column(db.Float, default=1.0)
    stage = db.Column(db.String(50), default='New')  # New, In Progress, Repaired, Scrap
    assigned_technician = db.Column(db.String(100))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    department = db.Column(db.String(100))
    priority = db.Column(db.String(50), default='Medium')  # Critical, High, Medium, Low
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    activity_logs = db.relationship('ActivityLog', backref='request', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'equipment_id': self.equipment_id,
            'equipment_name': self.equipment.name if self.equipment else None,
            'equipment_serial': self.equipment.serial_number if self.equipment else None,
            'request_type': self.request_type,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'duration_hours': self.duration_hours,
            'stage': self.stage,
            'assigned_technician': self.assigned_technician,
            'team_id': self.team_id,
            'team_name': self.team.name if self.team else None,
            'department': self.department,
            'priority': self.priority,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'is_overdue': self.scheduled_date < datetime.now().date() if self.scheduled_date and self.stage not in ['Repaired', 'Scrap'] else False
        }

class ActivityLog(db.Model):
    __tablename__ = 'activity_log'
    
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))
    request_id = db.Column(db.Integer, db.ForeignKey('maintenance_requests.id'))
    action = db.Column(db.String(200), nullable=False)
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'equipment_id': self.equipment_id,
            'request_id': self.request_id,
            'action': self.action,
            'details': self.details,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
