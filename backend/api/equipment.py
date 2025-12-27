"""
Equipment API Blueprint
Endpoints for equipment management
"""

from flask import Blueprint, request, jsonify
from database import db
from models import Equipment, Team, ActivityLog
from datetime import datetime

equipment_bp = Blueprint('equipment', __name__)

@equipment_bp.route('/', methods=['GET'])
def get_all_equipment():
    """Get all equipment"""
    try:
        equipment = Equipment.query.all()
        return jsonify([eq.to_dict() for eq in equipment]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@equipment_bp.route('/<int:equipment_id>', methods=['GET'])
def get_equipment(equipment_id):
    """Get single equipment by ID"""
    try:
        equipment = Equipment.query.get_or_404(equipment_id)
        return jsonify(equipment.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@equipment_bp.route('/', methods=['POST'])
def create_equipment():
    """Create new equipment"""
    try:
        data = request.get_json()
        
        # Convert date strings to date objects
        purchase_date = datetime.strptime(data.get('purchase_date'), '%Y-%m-%d').date() if data.get('purchase_date') else None
        warranty_expiry = datetime.strptime(data.get('warranty_expiry'), '%Y-%m-%d').date() if data.get('warranty_expiry') else None
        
        equipment = Equipment(
            name=data['name'],
            serial_number=data['serial_number'],
            category=data['category'],
            department=data['department'],
            assigned_employee=data.get('assigned_employee'),
            purchase_date=purchase_date,
            warranty_expiry=warranty_expiry,
            location=data.get('location'),
            status=data.get('status', 'Usable'),
            team_id=data.get('team_id'),
            notes=data.get('notes')
        )
        
        db.session.add(equipment)
        db.session.commit()
        
        # Log activity
        log = ActivityLog(
            equipment_id=equipment.id,
            action='Equipment Created',
            details=f"Equipment '{equipment.name}' added to system"
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify(equipment.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@equipment_bp.route('/<int:equipment_id>', methods=['PUT'])
def update_equipment(equipment_id):
    """Update equipment"""
    try:
        equipment = Equipment.query.get_or_404(equipment_id)
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            equipment.name = data['name']
        if 'category' in data:
            equipment.category = data['category']
        if 'department' in data:
            equipment.department = data['department']
        if 'assigned_employee' in data:
            equipment.assigned_employee = data['assigned_employee']
        if 'location' in data:
            equipment.location = data['location']
        if 'status' in data:
            equipment.status = data['status']
        if 'team_id' in data:
            equipment.team_id = data['team_id']
        if 'notes' in data:
            equipment.notes = data['notes']
        
        db.session.commit()
        
        return jsonify(equipment.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@equipment_bp.route('/<int:equipment_id>', methods=['DELETE'])
def delete_equipment(equipment_id):
    """Delete equipment"""
    try:
        equipment = Equipment.query.get_or_404(equipment_id)
        db.session.delete(equipment)
        db.session.commit()
        
        return jsonify({'message': 'Equipment deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@equipment_bp.route('/by-team/<int:team_id>', methods=['GET'])
def get_equipment_by_team(team_id):
    """Get equipment by team"""
    try:
        equipment = Equipment.query.filter_by(team_id=team_id).all()
        return jsonify([eq.to_dict() for eq in equipment]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@equipment_bp.route('/by-status/<string:status>', methods=['GET'])
def get_equipment_by_status(status):
    """Get equipment by status"""
    try:
        equipment = Equipment.query.filter_by(status=status).all()
        return jsonify([eq.to_dict() for eq in equipment]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
