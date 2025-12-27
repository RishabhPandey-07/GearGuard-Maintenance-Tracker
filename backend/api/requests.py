"""
Maintenance Requests API Blueprint
Endpoints for maintenance request management
"""

from flask import Blueprint, request, jsonify
from database import db
from models import MaintenanceRequest, Equipment, ActivityLog
from datetime import datetime

requests_bp = Blueprint('requests', __name__)

@requests_bp.route('/', methods=['GET'])
def get_all_requests():
    """Get all maintenance requests"""
    try:
        # Optional filters
        stage = request.args.get('stage')
        request_type = request.args.get('type')
        team_id = request.args.get('team_id')
        
        query = MaintenanceRequest.query
        
        if stage:
            query = query.filter_by(stage=stage)
        if request_type:
            query = query.filter_by(request_type=request_type)
        if team_id:
            query = query.filter_by(team_id=int(team_id))
        
        requests = query.all()
        return jsonify([req.to_dict() for req in requests]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@requests_bp.route('/<int:request_id>', methods=['GET'])
def get_request(request_id):
    """Get single request by ID"""
    try:
        req = MaintenanceRequest.query.get_or_404(request_id)
        return jsonify(req.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@requests_bp.route('/', methods=['POST'])
def create_request():
    """Create new maintenance request"""
    try:
        data = request.get_json()
        
        # Get equipment to auto-fill team and department
        equipment = Equipment.query.get(data['equipment_id'])
        if not equipment:
            return jsonify({'error': 'Equipment not found'}), 404
        
        # Convert date string to date object
        scheduled_date = datetime.strptime(data['scheduled_date'], '%Y-%m-%d').date()
        
        req = MaintenanceRequest(
            subject=data['subject'],
            equipment_id=data['equipment_id'],
            request_type=data['request_type'],
            scheduled_date=scheduled_date,
            duration_hours=data.get('duration_hours', 1.0),
            stage=data.get('stage', 'New'),
            assigned_technician=data.get('assigned_technician'),
            team_id=equipment.team_id,  # Auto-fill from equipment
            department=equipment.department,  # Auto-fill from equipment
            priority=data.get('priority', 'Medium'),
            description=data.get('description')
        )
        
        db.session.add(req)
        db.session.commit()
        
        # Log activity
        log = ActivityLog(
            request_id=req.id,
            equipment_id=equipment.id,
            action='Request Created',
            details=f"Request '{req.subject}' created for {equipment.name}"
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify(req.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@requests_bp.route('/<int:request_id>', methods=['PUT'])
def update_request(request_id):
    """Update maintenance request"""
    try:
        req = MaintenanceRequest.query.get_or_404(request_id)
        data = request.get_json()
        
        old_stage = req.stage
        
        # Update fields
        if 'subject' in data:
            req.subject = data['subject']
        if 'stage' in data:
            req.stage = data['stage']
        if 'assigned_technician' in data:
            req.assigned_technician = data['assigned_technician']
        if 'priority' in data:
            req.priority = data['priority']
        if 'description' in data:
            req.description = data['description']
        if 'duration_hours' in data:
            req.duration_hours = data['duration_hours']
        
        # If stage changed to Repaired, set completed_at
        if req.stage == 'Repaired' and old_stage != 'Repaired':
            req.completed_at = datetime.utcnow()
        
        # If stage changed to Scrap, mark equipment as Scrapped
        if req.stage == 'Scrap' and old_stage != 'Scrap':
            equipment = Equipment.query.get(req.equipment_id)
            if equipment:
                equipment.status = 'Scrapped'
                log = ActivityLog(
                    equipment_id=equipment.id,
                    request_id=req.id,
                    action='Equipment Scrapped',
                    details=f"Equipment '{equipment.name}' marked as scrapped due to request #{req.id}"
                )
                db.session.add(log)
        
        db.session.commit()
        
        return jsonify(req.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@requests_bp.route('/<int:request_id>', methods=['DELETE'])
def delete_request(request_id):
    """Delete maintenance request"""
    try:
        req = MaintenanceRequest.query.get_or_404(request_id)
        db.session.delete(req)
        db.session.commit()
        
        return jsonify({'message': 'Request deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@requests_bp.route('/by-equipment/<int:equipment_id>', methods=['GET'])
def get_requests_by_equipment(equipment_id):
    """Get requests for specific equipment"""
    try:
        requests = MaintenanceRequest.query.filter_by(equipment_id=equipment_id).all()
        return jsonify([req.to_dict() for req in requests]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@requests_bp.route('/by-stage/<string:stage>', methods=['GET'])
def get_requests_by_stage(stage):
    """Get requests by stage"""
    try:
        requests = MaintenanceRequest.query.filter_by(stage=stage).all()
        return jsonify([req.to_dict() for req in requests]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@requests_bp.route('/preventive', methods=['GET'])
def get_preventive_requests():
    """Get all preventive maintenance requests"""
    try:
        requests = MaintenanceRequest.query.filter_by(request_type='Preventive').all()
        return jsonify([req.to_dict() for req in requests]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
