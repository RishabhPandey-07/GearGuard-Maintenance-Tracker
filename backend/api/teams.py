"""
Teams API Blueprint
Endpoints for team and team member management
"""

from flask import Blueprint, request, jsonify
from database import db
from models import Team, TeamMember

teams_bp = Blueprint('teams', __name__)

# ============ TEAMS ============

@teams_bp.route('/', methods=['GET'])
def get_all_teams():
    """Get all teams"""
    try:
        teams = Team.query.all()
        return jsonify([team.to_dict() for team in teams]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@teams_bp.route('/<int:team_id>', methods=['GET'])
def get_team(team_id):
    """Get single team by ID"""
    try:
        team = Team.query.get_or_404(team_id)
        return jsonify(team.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@teams_bp.route('/', methods=['POST'])
def create_team():
    """Create new team"""
    try:
        data = request.get_json()
        
        team = Team(
            name=data['name'],
            description=data.get('description')
        )
        
        db.session.add(team)
        db.session.commit()
        
        return jsonify(team.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@teams_bp.route('/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    """Delete team"""
    try:
        team = Team.query.get_or_404(team_id)
        db.session.delete(team)
        db.session.commit()
        
        return jsonify({'message': 'Team deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# ============ TEAM MEMBERS ============

@teams_bp.route('/members', methods=['GET'])
def get_all_members():
    """Get all team members"""
    try:
        members = TeamMember.query.all()
        return jsonify([member.to_dict() for member in members]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@teams_bp.route('/<int:team_id>/members', methods=['GET'])
def get_team_members(team_id):
    """Get members of a specific team"""
    try:
        members = TeamMember.query.filter_by(team_id=team_id).all()
        return jsonify([member.to_dict() for member in members]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@teams_bp.route('/members', methods=['POST'])
def create_member():
    """Create new team member"""
    try:
        data = request.get_json()
        
        member = TeamMember(
            team_id=data['team_id'],
            name=data['name'],
            role=data.get('role'),
            email=data.get('email'),
            phone=data.get('phone')
        )
        
        db.session.add(member)
        db.session.commit()
        
        return jsonify(member.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@teams_bp.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    """Update team member"""
    try:
        member = TeamMember.query.get_or_404(member_id)
        data = request.get_json()
        
        if 'name' in data:
            member.name = data['name']
        if 'role' in data:
            member.role = data['role']
        if 'email' in data:
            member.email = data['email']
        if 'phone' in data:
            member.phone = data['phone']
        
        db.session.commit()
        
        return jsonify(member.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@teams_bp.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    """Delete team member"""
    try:
        member = TeamMember.query.get_or_404(member_id)
        db.session.delete(member)
        db.session.commit()
        
        return jsonify({'message': 'Member deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
