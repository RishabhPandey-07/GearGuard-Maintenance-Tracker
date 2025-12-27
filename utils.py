"""
GearGuard - Utility Functions
Helper functions for date handling, UI components, and formatting
"""

from datetime import datetime, date, timedelta
from typing import List, Dict
import streamlit as st

def is_overdue(scheduled_date: str) -> bool:
    """Check if a scheduled date is overdue"""
    if not scheduled_date:
        return False
    
    try:
        scheduled = datetime.strptime(scheduled_date, '%Y-%m-%d').date()
        return scheduled < date.today()
    except:
        return False

def format_date(date_str: str, format_out: str = "%b %d, %Y") -> str:
    """Format date string for display"""
    if not date_str:
        return "N/A"
    
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime(format_out)
    except:
        return date_str

def get_priority_color(priority: str) -> str:
    """Get color for priority badge"""
    colors = {
        'Critical': '#FF4444',
        'High': '#FF9800',
        'Medium': '#2196F3',
        'Low': '#4CAF50'
    }
    return colors.get(priority, '#9E9E9E')

def get_status_color(status: str) -> str:
    """Get color for status badge"""
    colors = {
        'Usable': '#4CAF50',
        'Scrapped': '#FF4444',
        'Under Maintenance': '#FF9800',
        'Reserved': '#2196F3'
    }
    return colors.get(status, '#9E9E9E')

def get_stage_color(stage: str) -> str:
    """Get color for request stage"""
    colors = {
        'New': '#2196F3',
        'In Progress': '#FF9800',
        'Repaired': '#4CAF50',
        'Scrap': '#FF4444'
    }
    return colors.get(stage, '#9E9E9E')

def create_badge(text: str, color: str) -> str:
    """Create HTML badge"""
    return f'<span style="background-color: {color}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600;">{text}</span>'

def create_smart_button(count: int, label: str) -> str:
    """Create smart button HTML"""
    return f'''
    <div style="
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 5px;
    ">
        <span style="font-size: 18px; margin-right: 8px;">{count}</span>
        <span style="font-size: 12px;">{label}</span>
    </div>
    '''

def get_technician_avatar(name: str) -> str:
    """Get initials for technician avatar"""
    if not name:
        return "NA"
    
    parts = name.split()
    if len(parts) >= 2:
        return f"{parts[0][0]}{parts[1][0]}".upper()
    return name[:2].upper()

def create_kanban_card(request: Dict, is_overdue: bool = False) -> str:
    """Create Kanban card HTML"""
    border_color = '#FF4444' if is_overdue else '#E0E0E0'
    priority_color = get_priority_color(request.get('priority', 'Medium'))
    avatar = get_technician_avatar(request.get('assigned_technician', ''))
    
    overdue_badge = '<span style="background: #FF4444; color: white; padding: 2px 8px; border-radius: 8px; font-size: 10px; font-weight: 600;">OVERDUE</span>' if is_overdue else ''
    
    return f'''
    <div style="
        background: white;
        border-left: 4px solid {border_color};
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    ">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
            <h4 style="margin: 0; font-size: 14px; color: #333; flex: 1;">{request.get('subject', 'N/A')}</h4>
            {overdue_badge}
        </div>
        <p style="margin: 4px 0; font-size: 12px; color: #666;">
            <strong>{request.get('equipment_name', 'N/A')}</strong>
        </p>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="
                    width: 32px;
                    height: 32px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 11px;
                    font-weight: 600;
                ">{avatar}</div>
                <span style="font-size: 11px; color: #666;">{request.get('assigned_technician', 'Unassigned')}</span>
            </div>
            <span style="background: {priority_color}; color: white; padding: 2px 8px; border-radius: 8px; font-size: 10px; font-weight: 600;">
                {request.get('priority', 'Medium')}
            </span>
        </div>
        <div style="margin-top: 8px; font-size: 11px; color: #999;">
            📅 {format_date(request.get('scheduled_date', ''))}
        </div>
    </div>
    '''

def get_calendar_events(requests: List[Dict]) -> List[Dict]:
    """Convert maintenance requests to calendar events"""
    events = []
    for req in requests:
        if req.get('request_type') == 'Preventive':
            events.append({
                'title': req.get('subject', 'N/A'),
                'start': req.get('scheduled_date'),
                'color': get_stage_color(req.get('stage', 'New')),
                'description': req.get('equipment_name', 'N/A')
            })
    return events

def calculate_metrics(stats: Dict) -> Dict:
    """Calculate additional metrics for dashboard"""
    metrics = {
        'completion_rate': 0,
        'equipment_health': 0,
        'response_time': 'Good'
    }
    
    if stats.get('total_equipment', 0) > 0:
        metrics['equipment_health'] = int((stats['total_equipment'] / (stats['total_equipment'] + 1)) * 100)
    
    return metrics
