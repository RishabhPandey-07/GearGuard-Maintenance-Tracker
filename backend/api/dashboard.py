"""
Dashboard API Blueprint
Endpoints for dashboard statistics and analytics
"""

from flask import Blueprint, jsonify, request
from database import db
from models import Equipment, MaintenanceRequest, Team
from sqlalchemy import func
from datetime import date


dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        # Total equipment (usable)
        total_equipment = Equipment.query.filter_by(status='Usable').count()

        # Active requests (not Repaired or Scrap)
        active_requests = MaintenanceRequest.query.filter(
            ~MaintenanceRequest.stage.in_(['Repaired', 'Scrap'])
        ).count()

        # Overdue requests
        overdue_requests = MaintenanceRequest.query.filter(
            ~MaintenanceRequest.stage.in_(['Repaired', 'Scrap']),
            MaintenanceRequest.scheduled_date < date.today()
        ).count()

        # Total teams
        total_teams = Team.query.count()

        # Critical requests
        critical_requests = MaintenanceRequest.query.filter(
            MaintenanceRequest.priority == 'Critical',
            ~MaintenanceRequest.stage.in_(['Repaired', 'Scrap'])
        ).count()

        return jsonify({
            'total_equipment': total_equipment,
            'active_requests': active_requests,
            'overdue_requests': overdue_requests,
            'total_teams': total_teams,
            'critical_requests': critical_requests
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/requests-by-team', methods=['GET'])
def get_requests_by_team():
    """Get request count grouped by team"""
    try:
        results = db.session.query(
            Team.name,
            func.count(MaintenanceRequest.id).label('count')
        ).outerjoin(MaintenanceRequest).group_by(Team.id).all()

        return jsonify([{'team': r[0], 'count': r[1]} for r in results]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/equipment-by-category', methods=['GET'])
def get_equipment_by_category():
    """Get equipment count grouped by category"""
    try:
        results = db.session.query(
            Equipment.category,
            func.count(Equipment.id).label('count')
        ).group_by(Equipment.category).all()

        return jsonify([{'category': r[0], 'count': r[1]} for r in results]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/recent-activity', methods=['GET'])
def get_recent_activity():
    """Get recent activity log"""
    try:
        from models import ActivityLog

        # Parse limit safely
        try:
            limit = int(request.args.get('limit', 10))
        except (TypeError, ValueError):
            limit = 10

        activities = ActivityLog.query.order_by(
            ActivityLog.created_at.desc()
        ).limit(limit).all()

        # Map to keys expected by frontend (description, timestamp)
        payload = [{
            'id': a.id,
            'action': a.action,
            'description': a.details,
            'timestamp': a.created_at.isoformat() if a.created_at else None,
            'equipment_id': a.equipment_id,
            'request_id': a.request_id
        } for a in activities]

        return jsonify(payload), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
