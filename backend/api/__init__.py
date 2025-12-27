"""
API Package Initialization
Exports all blueprints
"""

from api.equipment import equipment_bp
from api.requests import requests_bp
from api.teams import teams_bp
from api.dashboard import dashboard_bp

__all__ = ['equipment_bp', 'requests_bp', 'teams_bp', 'dashboard_bp']
