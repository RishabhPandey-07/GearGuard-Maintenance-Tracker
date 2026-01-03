"""
GearGuard - Maintenance Management System
Professional Odoo-Inspired Dashboard for Hackathon
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import pandas as pd
from database import Database
from utils import *


st.set_page_config(
    page_title="GearGuard - Maintenance Management",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
def load_css():
    with open('styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    load_css()
except:
    pass

# Initialize Database
@st.cache_resource
def init_db():
    return Database()

db = init_db()

# ============ SIDEBAR NAVIGATION ============

def sidebar_navigation():
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 30px 0 20px 0;'>
        <div style='
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            width: 70px;
            height: 70px;
            border-radius: 20px;
            margin: 0 auto 15px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        '>
            <span style='font-size: 36px;'>🛠️</span>
        </div>
        <h1 style='color: white; font-size: 28px; margin: 0; font-weight: 800; letter-spacing: 1px;'>GearGuard</h1>
        <p style='color: #cbd5e0; font-size: 13px; margin-top: 8px; font-weight: 500; letter-spacing: 0.5px;'>
            MAINTENANCE MANAGEMENT
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("<div style='margin: 20px 0 10px 0;'><p style='color: #94a3b8; font-size: 11px; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 700;'>📍 NAVIGATION</p></div>", unsafe_allow_html=True)
    
    menu_items = {
        "📊 Dashboard": "dashboard",
        "🏗️ Equipment": "equipment",
        "🛠️ Maintenance Requests": "requests",
        "📋 Kanban Board": "kanban",
        "📅 Calendar View": "calendar",
        "👥 Teams": "teams",
    }
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "dashboard"
    
    for label, page_id in menu_items.items():
        if st.sidebar.button(label, key=f"nav_{page_id}", width='stretch'):
            st.session_state.current_page = page_id
            st.rerun()
    
    st.sidebar.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
    st.sidebar.markdown("""
    <div style='
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    '>
        <p style='color: #cbd5e0; font-size: 12px; margin: 0; font-weight: 600;'>🏆 Hackathon 2024</p>
        <p style='color: #94a3b8; font-size: 11px; margin-top: 8px;'>Version 1.0</p>
    </div>
    """, unsafe_allow_html=True)

# ============ DASHBOARD PAGE ============

def render_dashboard():
    st.markdown("""
    <div style='margin-bottom: 30px;'>
        <h1 style='margin-bottom: 10px;'>📊 Dashboard</h1>
        <p style='color: #64748b; font-size: 16px; font-weight: 500;'>Real-time overview of your maintenance operations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get Statistics
    stats = db.get_dashboard_stats()
    
    # Top Metrics Row with enhanced styling
    st.markdown("<div style='margin-bottom: 30px;'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4, gap="large")
    
    with col1:
        st.markdown("""
        <div class='metric-card' style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.05) 100%);'>
            <div style='font-size: 13px; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;'>Total Equipment</div>
            <div style='font-size: 42px; font-weight: 800; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top: 12px;'>{}</div>
            <div style='font-size: 13px; color: #10b981; margin-top: 8px; font-weight: 600;'>✓ Active & Usable</div>
        </div>
        """.format(stats['total_equipment']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card' style='background: linear-gradient(135deg, rgba(251, 146, 60, 0.08) 0%, rgba(249, 115, 22, 0.05) 100%);'>
            <div style='font-size: 13px; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;'>Active Requests</div>
            <div style='font-size: 42px; font-weight: 800; background: linear-gradient(135deg, #fb923c 0%, #f97316 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top: 12px;'>{}</div>
            <div style='font-size: 13px; color: #64748b; margin-top: 8px; font-weight: 600;'>⏳ In Progress</div>
        </div>
        """.format(stats['active_requests']), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card' style='background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(220, 38, 38, 0.05) 100%);'>
            <div style='font-size: 13px; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;'>Overdue Tasks</div>
            <div style='font-size: 42px; font-weight: 800; background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top: 12px;'>{}</div>
            <div style='font-size: 13px; color: #ef4444; margin-top: 8px; font-weight: 600;'>⚠️ Needs Attention</div>
        </div>
        """.format(stats['overdue_requests']), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='metric-card' style='background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(37, 99, 235, 0.05) 100%);'>
            <div style='font-size: 13px; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;'>Maintenance Teams</div>
            <div style='font-size: 42px; font-weight: 800; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top: 12px;'>{}</div>
            <div style='font-size: 13px; color: #64748b; margin-top: 8px; font-weight: 600;'>👥 Active Teams</div>
        </div>
        """.format(stats['total_teams']), unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-bottom: 20px;'>📊 Requests by Team</h3>", unsafe_allow_html=True)
        
        team_data = db.get_requests_by_team()
        if team_data:
            df_teams = pd.DataFrame(team_data)
            fig = px.bar(df_teams, x='name', y='count', 
                        labels={'name': 'Team', 'count': 'Number of Requests'},
                        color='count',
                        color_continuous_scale='Blues')
            fig.update_layout(showlegend=False, height=350)
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("No data available")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-bottom: 20px;'>🏗️ Equipment by Category</h3>", unsafe_allow_html=True)
        
        category_data = db.get_equipment_by_category()
        if category_data:
            df_categories = pd.DataFrame(category_data)
            fig = px.pie(df_categories, values='count', names='category', 
                        hole=0.4,
                        color_discrete_sequence=px.colors.sequential.RdBu)
            fig.update_layout(showlegend=True, height=350)
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("No data available")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3>📝 Recent Activity</h3>", unsafe_allow_html=True)
    
    activities = db.get_recent_activity(limit=8)
    if activities:
        for activity in activities:
            timestamp = format_date(activity['created_at'].split()[0]) if activity.get('created_at') else 'N/A'
            st.markdown(f"""
            <div class='activity-item'>
                <strong>{activity['action']}</strong>
                <p style='margin: 4px 0; font-size: 12px; color: #666;'>{activity['details']}</p>
                <span style='font-size: 11px; color: #999;'>{timestamp}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent activity")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============ EQUIPMENT PAGE ============

def render_equipment():
    st.markdown("""
    <div style='margin-bottom: 30px;'>
        <h1 style='margin-bottom: 10px;'>🏗️ Equipment Management</h1>
        <p style='color: #64748b; font-size: 16px; font-weight: 500;'>Manage your assets, track maintenance, and monitor equipment health</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 All Equipment", "➕ Add Equipment", "🔍 Equipment Details"])
    
    with tab1:
        equipment_list = db.get_all_equipment()
        
        if equipment_list:
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_status = st.selectbox("Filter by Status", ["All", "Usable", "Scrapped"])
            with col2:
                categories = list(set([e['category'] for e in equipment_list]))
                filter_category = st.selectbox("Filter by Category", ["All"] + categories)
            with col3:
                departments = list(set([e['department'] for e in equipment_list]))
                filter_dept = st.selectbox("Filter by Department", ["All"] + departments)
            
            # Apply filters
            filtered = equipment_list
            if filter_status != "All":
                filtered = [e for e in filtered if e['status'] == filter_status]
            if filter_category != "All":
                filtered = [e for e in filtered if e['category'] == filter_category]
            if filter_dept != "All":
                filtered = [e for e in filtered if e['department'] == filter_dept]
            
            # Display equipment cards
            for i in range(0, len(filtered), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    if i + j < len(filtered):
                        eq = filtered[i + j]
                        with col:
                            # Smart button - count of open requests
                            open_requests = db.get_equipment_request_count(eq['id'])
                            
                            status_color = get_status_color(eq['status'])
                            
                            st.markdown(f"""
                            <div class='equipment-card'>
                                <h4 style='margin: 0 0 10px 0; color: #1e3a8a;'>{eq['name']}</h4>
                                <p style='font-size: 12px; color: #666; margin: 4px 0;'>
                                    <strong>SN:</strong> {eq['serial_number']}
                                </p>
                                <p style='font-size: 12px; color: #666; margin: 4px 0;'>
                                    <strong>Category:</strong> {eq['category']}
                                </p>
                                <p style='font-size: 12px; color: #666; margin: 4px 0;'>
                                    <strong>Department:</strong> {eq['department']}
                                </p>
                                <p style='font-size: 12px; color: #666; margin: 4px 0;'>
                                    <strong>Location:</strong> {eq['location'] or 'N/A'}
                                </p>
                                <div style='margin-top: 12px;'>
                                    {create_badge(eq['status'], status_color)}
                                </div>
                                <div style='margin-top: 12px;'>
                                    {create_smart_button(open_requests, 'Open Requests')}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button(f"View Details", key=f"view_eq_{eq['id']}", use_container_width=True):
                                st.session_state.selected_equipment = eq['id']
                                st.session_state.current_page = "equipment"
                                st.rerun()
        else:
            st.info("No equipment found. Add your first equipment to get started!")
    
    with tab2:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        
        with st.form("add_equipment_form"):
            st.markdown("<h3>Add New Equipment</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Equipment Name*", placeholder="e.g., CNC Machine A1")
                serial_number = st.text_input("Serial Number*", placeholder="e.g., CNC-2024-001")
                category = st.selectbox("Category*", 
                    ["Machinery", "Electrical", "IT Equipment", "Climate Control", "Vehicles", "Tools", "Other"])
                department = st.text_input("Department*", placeholder="e.g., Production")
                assigned_employee = st.text_input("Assigned Employee", placeholder="e.g., John Smith")
            
            with col2:
                teams = db.get_all_teams()
                team_options = {t['name']: t['id'] for t in teams}
                team_name = st.selectbox("Maintenance Team", list(team_options.keys()))
                
                purchase_date = st.date_input("Purchase Date")
                warranty_expiry = st.date_input("Warranty Expiry Date")
                location = st.text_input("Location", placeholder="e.g., Factory Floor A")
                status = st.selectbox("Status", ["Usable", "Under Maintenance", "Reserved"])
            
            notes = st.text_area("Additional Notes", placeholder="Any additional information...")
            
            submitted = st.form_submit_button("➕ Add Equipment", width='stretch')
            
            if submitted:
                if name and serial_number and category and department:
                    try:
                        equipment_data = {
                            'name': name,
                            'serial_number': serial_number,
                            'category': category,
                            'department': department,
                            'assigned_employee': assigned_employee if assigned_employee else None,
                            'team_id': team_options[team_name] if team_name else None,
                            'purchase_date': purchase_date.strftime('%Y-%m-%d'),
                            'warranty_expiry': warranty_expiry.strftime('%Y-%m-%d'),
                            'location': location if location else None,
                            'status': status,
                            'notes': notes if notes else None
                        }
                        
                        eq_id = db.add_equipment(equipment_data)
                        st.success(f"✅ Equipment '{name}' added successfully! (ID: {eq_id})")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Error adding equipment: {str(e)}")
                else:
                    st.warning("⚠️ Please fill in all required fields marked with *")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        if 'selected_equipment' in st.session_state:
            eq = db.get_equipment_by_id(st.session_state.selected_equipment)
            
            if eq:
                st.markdown(f"<h2>{eq['name']}</h2>", unsafe_allow_html=True)
                
                # Equipment Details Card
                st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                st.markdown("<h3>Equipment Information</h3>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Serial Number:** {eq['serial_number']}")
                    st.markdown(f"**Category:** {eq['category']}")
                    st.markdown(f"**Department:** {eq['department']}")
                
                with col2:
                    st.markdown(f"**Status:** {create_badge(eq['status'], get_status_color(eq['status']))}", unsafe_allow_html=True)
                    st.markdown(f"**Location:** {eq['location'] or 'N/A'}")
                    st.markdown(f"**Team:** {eq['team_name'] or 'N/A'}")
                
                with col3:
                    st.markdown(f"**Assigned To:** {eq['assigned_employee'] or 'Unassigned'}")
                    st.markdown(f"**Purchase Date:** {format_date(eq['purchase_date'])}")
                    st.markdown(f"**Warranty Expiry:** {format_date(eq['warranty_expiry'])}")
                
                if eq['notes']:
                    st.markdown(f"**Notes:** {eq['notes']}")
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Smart Button - Maintenance History
                requests = db.get_requests_by_equipment(eq['id'])
                open_count = len([r for r in requests if r['stage'] not in ['Repaired', 'Scrap']])
                
                st.markdown(f"<h3>Maintenance History {create_smart_button(open_count, 'Open Requests')}</h3>", unsafe_allow_html=True)
                
                if requests:
                    df_requests = pd.DataFrame(requests)
                    df_requests = df_requests[['subject', 'request_type', 'scheduled_date', 'stage', 'priority', 'assigned_technician']]
                    df_requests.columns = ['Subject', 'Type', 'Scheduled', 'Stage', 'Priority', 'Technician']
                    st.dataframe(df_requests, width='stretch', hide_index=True)
                else:
                    st.info("No maintenance history for this equipment")
        else:
            st.info("Select an equipment from the 'All Equipment' tab to view details")

# ============ MAINTENANCE REQUESTS PAGE ============

def render_requests():
    st.markdown("""
    <div style='margin-bottom: 30px;'>
        <h1 style='margin-bottom: 10px;'>🛠️ Maintenance Requests</h1>
        <p style='color: #64748b; font-size: 16px; font-weight: 500;'>Create and track maintenance work orders for your equipment</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📋 All Requests", "➕ Create Request"])
    
    with tab1:
        requests = db.get_all_requests()
        
        if requests:
            # Filters
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                filter_stage = st.selectbox("Filter by Stage", ["All", "New", "In Progress", "Repaired", "Scrap"])
            with col2:
                filter_type = st.selectbox("Filter by Type", ["All", "Corrective", "Preventive"])
            with col3:
                filter_priority = st.selectbox("Filter by Priority", ["All", "Critical", "High", "Medium", "Low"])
            with col4:
                show_overdue = st.checkbox("Show Only Overdue", value=False)
            
            # Apply filters
            filtered = requests
            if filter_stage != "All":
                filtered = [r for r in filtered if r['stage'] == filter_stage]
            if filter_type != "All":
                filtered = [r for r in filtered if r['request_type'] == filter_type]
            if filter_priority != "All":
                filtered = [r for r in filtered if r['priority'] == filter_priority]
            if show_overdue:
                filtered = [r for r in filtered if is_overdue(r['scheduled_date']) and r['stage'] not in ['Repaired', 'Scrap']]
            
            # Display as table
            if filtered:
                df_requests = pd.DataFrame(filtered)
                display_cols = ['id', 'subject', 'equipment_name', 'request_type', 'scheduled_date', 
                              'stage', 'priority', 'assigned_technician', 'team_name']
                df_display = df_requests[display_cols]
                df_display.columns = ['ID', 'Subject', 'Equipment', 'Type', 'Scheduled', 'Stage', 'Priority', 'Technician', 'Team']
                
                st.dataframe(df_display, width='stretch', hide_index=True)
                
                # Quick stage update
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("🔄 Quick Stage Update"):
                    col1, col2 = st.columns(2)
                    with col1:
                        request_id = st.number_input("Request ID", min_value=1, step=1)
                    with col2:
                        new_stage = st.selectbox("New Stage", ["New", "In Progress", "Repaired", "Scrap"])
                    
                    if st.button("Update Stage", width='stretch'):
                        try:
                            db.update_request_stage(request_id, new_stage)
                            st.success(f"✅ Request #{request_id} moved to '{new_stage}' stage!")
                            
                            if new_stage == "Scrap":
                                st.warning("⚠️ Equipment has been automatically marked as 'Scrapped'")
                            
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
            else:
                st.info("No requests match the selected filters")
        else:
            st.info("No maintenance requests found")
    
    with tab2:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        
        with st.form("create_request_form"):
            st.markdown("<h3>Create Maintenance Request</h3>", unsafe_allow_html=True)
            
            # Equipment selection with auto-fill
            equipment_list = db.get_all_equipment()
            equipment_options = {f"{e['name']} ({e['serial_number']})": e['id'] for e in equipment_list if e['status'] == 'Usable'}
            
            selected_eq_str = st.selectbox("Select Equipment*", list(equipment_options.keys()))
            selected_eq_id = equipment_options[selected_eq_str] if selected_eq_str else None
            
            # Auto-fill preview
            if selected_eq_id:
                eq_data = db.get_equipment_by_id(selected_eq_id)
                st.info(f"🔍 Auto-filled: Department: **{eq_data['department']}** | Team: **{eq_data['team_name'] or 'Not Assigned'}**")
                
                # Get team members for technician assignment
                team_members = []
                if eq_data.get('team_id'):
                    team_members = db.get_team_members(eq_data['team_id'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                subject = st.text_input("Subject*", placeholder="e.g., Monthly Oil Change")
                request_type = st.selectbox("Request Type*", ["Corrective", "Preventive"])
                scheduled_date = st.date_input("Scheduled Date*", value=date.today())
                duration = st.number_input("Duration (Hours)", min_value=0.5, max_value=24.0, value=2.0, step=0.5)
            
            with col2:
                priority = st.selectbox("Priority", ["Critical", "High", "Medium", "Low"])
                stage = st.selectbox("Initial Stage", ["New", "In Progress"])
                
                # Technician dropdown showing only team members
                if selected_eq_id and team_members:
                    technician_options = ["Unassigned"] + [f"{m['name']} - {m['role']}" for m in team_members]
                    selected_tech = st.selectbox("Assigned Technician*", technician_options)
                    assigned_technician = None if selected_tech == "Unassigned" else selected_tech.split(" - ")[0]
                else:
                    st.selectbox("Assigned Technician", ["Unassigned"], disabled=True, help="Select equipment first to see team members")
                    assigned_technician = None
            
            description = st.text_area("Description", placeholder="Detailed description of the maintenance work required...")
            
            submitted = st.form_submit_button("🛠️ Create Request", width='stretch')
            
            if submitted:
                if selected_eq_id and subject and request_type and scheduled_date:
                    try:
                        request_data = {
                            'subject': subject,
                            'equipment_id': selected_eq_id,
                            'request_type': request_type,
                            'scheduled_date': scheduled_date.strftime('%Y-%m-%d'),
                            'duration_hours': duration,
                            'stage': stage,
                            'assigned_technician': assigned_technician if assigned_technician else None,
                            'priority': priority,
                            'description': description if description else None
                        }
                        
                        req_id = db.add_maintenance_request(request_data)
                        st.success(f"✅ Maintenance Request created successfully! (ID: {req_id})")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Error creating request: {str(e)}")
                else:
                    st.warning("⚠️ Please fill in all required fields marked with *")
        
        st.markdown("</div>", unsafe_allow_html=True)

# ============ KANBAN BOARD PAGE ============

def render_kanban():
    st.markdown("""
    <div style='margin-bottom: 30px;'>
        <h1 style='margin-bottom: 10px;'>📋 Kanban Board</h1>
        <p style='color: #64748b; font-size: 16px; font-weight: 500;'>Visual workflow management with interactive organization</p>
    </div>
    """, unsafe_allow_html=True)
    
    stages = ["New", "In Progress", "Repaired", "Scrap"]
    
    cols = st.columns(4)
    
    for idx, stage in enumerate(stages):
        with cols[idx]:
            stage_color = get_stage_color(stage)
            requests = db.get_requests_by_stage(stage)
            
            st.markdown(f"""
            <div class='kanban-column'>
                <div class='kanban-header' style='border-bottom: 3px solid {stage_color};'>
                    {stage} ({len(requests)})
                </div>
            """, unsafe_allow_html=True)
            
            for req in requests:
                overdue = is_overdue(req['scheduled_date']) and stage not in ['Repaired', 'Scrap']
                card_html = create_kanban_card(req, overdue)
                st.markdown(card_html, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Quick move functionality
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3>🔄 Move Request Between Stages</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b;'>Select a request and move it to a different stage:</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        move_req_id = st.number_input("Request ID", min_value=1, step=1, key="kanban_move")
    with col2:
        move_to_stage = st.selectbox("Move to Stage", stages, key="kanban_stage")
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Move Request", width='stretch', key="kanban_btn"):
            try:
                db.update_request_stage(move_req_id, move_to_stage)
                st.success(f"✅ Request #{move_req_id} moved to '{move_to_stage}'!")
                if move_to_stage == "Scrap":
                    st.warning("⚠️ Equipment has been automatically marked as 'Scrapped'")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============ CALENDAR VIEW PAGE ============

def render_calendar():
    st.markdown("""
    <div style='margin-bottom: 30px;'>
        <h1 style='margin-bottom: 10px;'>📅 Calendar View</h1>
        <p style='color: #64748b; font-size: 16px; font-weight: 500;'>Schedule and track preventive maintenance activities</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get preventive maintenance requests
    all_requests = db.get_all_requests()
    preventive_requests = [r for r in all_requests if r['request_type'] == 'Preventive']
    
    if preventive_requests:
        # Calendar view using timeline
        st.markdown("<div class='calendar-container'>", unsafe_allow_html=True)
        
        # Create DataFrame for calendar
        calendar_data = []
        for req in preventive_requests:
            calendar_data.append({
                'Task': req['subject'],
                'Start': req['scheduled_date'],
                'End': req['scheduled_date'],
                'Equipment': req['equipment_name'],
                'Team': req['team_name'],
                'Stage': req['stage'],
                'Technician': req['assigned_technician'] or 'Unassigned'
            })
        
        df_calendar = pd.DataFrame(calendar_data)
        
        # Timeline chart
        fig = px.timeline(df_calendar, x_start='Start', x_end='End', y='Task', 
                         color='Stage',
                         hover_data=['Equipment', 'Team', 'Technician'],
                         title="Preventive Maintenance Timeline",
                         color_discrete_map={
                             'New': '#2196F3',
                             'In Progress': '#FF9800',
                             'Repaired': '#4CAF50',
                             'Scrap': '#FF4444'
                         })
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, width='stretch')
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Upcoming preventive maintenance
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("<h3>📆 Upcoming Preventive Maintenance (Next 30 Days)</h3>", unsafe_allow_html=True)
        
        today = date.today()
        next_30_days = today + timedelta(days=30)
        
        upcoming = [r for r in preventive_requests 
                   if today <= datetime.strptime(r['scheduled_date'], '%Y-%m-%d').date() <= next_30_days
                   and r['stage'] not in ['Repaired', 'Scrap']]
        
        if upcoming:
            for req in upcoming:
                scheduled_dt = datetime.strptime(req['scheduled_date'], '%Y-%m-%d').date()
                days_until = (scheduled_dt - today).days
                
                priority_color = get_priority_color(req['priority'])
                
                st.markdown(f"""
                <div style='background: white; border-left: 4px solid {priority_color}; border-radius: 8px; padding: 12px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    <div style='display: flex; justify-content: space-between; align-items: start;'>
                        <div>
                            <h4 style='margin: 0; color: #1e3a8a;'>{req['subject']}</h4>
                            <p style='margin: 4px 0; font-size: 13px; color: #666;'>
                                <strong>Equipment:</strong> {req['equipment_name']} | 
                                <strong>Team:</strong> {req['team_name']} |
                                <strong>Technician:</strong> {req['assigned_technician'] or 'Not Assigned'}
                            </p>
                        </div>
                        <div style='text-align: right;'>
                            <div style='background: {priority_color}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600; margin-bottom: 4px;'>
                                {req['priority']}
                            </div>
                            <div style='font-size: 12px; color: #666;'>
                                📅 {format_date(req['scheduled_date'])}
                            </div>
                            <div style='font-size: 11px; color: #999;'>
                                {'Today!' if days_until == 0 else f'In {days_until} days'}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No upcoming preventive maintenance scheduled in the next 30 days")
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No preventive maintenance requests found")

# ============ TEAMS PAGE ============

def render_teams():
    st.markdown("""
    <div style='margin-bottom: 30px;'>
        <h1 style='margin-bottom: 10px;'>👥 Maintenance Teams</h1>
        <p style='color: #64748b; font-size: 16px; font-weight: 500;'>Manage your maintenance teams and their workload distribution</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 All Teams", "👨‍🔧 Team Members", "➕ Add Team/Member"])
    
    with tab1:
        teams = db.get_all_teams()
        
        if teams:
            for team in teams:
                # Get team statistics
                team_requests = db.get_all_requests()
                team_requests = [r for r in team_requests if r.get('team_id') == team['id']]
                active_requests = [r for r in team_requests if r['stage'] not in ['Repaired', 'Scrap']]
                
                team_equipment = db.get_all_equipment()
                team_equipment = [e for e in team_equipment if e.get('team_id') == team['id']]
                
                # Get team members
                team_members = db.get_team_members(team['id'])
                
                st.markdown(f"""
                <div class='custom-card' style='border-left: 4px solid #667eea;'>
                    <h3 style='margin: 0 0 10px 0; color: #1e3a8a;'>{team['name']}</h3>
                    <p style='color: #666; margin: 0 0 15px 0;'>{team['description'] or 'No description'}</p>
                    
                    <div style='display: flex; gap: 20px; margin-bottom: 15px;'>
                        <div>
                            {create_smart_button(len(team_equipment), 'Equipment')}
                        </div>
                        <div>
                            {create_smart_button(len(active_requests), 'Active Requests')}
                        </div>
                        <div>
                            {create_smart_button(len(team_members), 'Team Members')}
                        </div>
                    </div>
                    
                    <div style='background: #f8fafc; padding: 10px; border-radius: 8px;'>
                        <strong style='color: #475569;'>Team Members:</strong><br>
                        {'<span style="color: #94a3b8;">No members assigned</span>' if not team_members else 
                         ', '.join([f"{m['name']} ({m['role']})" if m['role'] else m['name'] for m in team_members])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No teams found")
    
    with tab2:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("<h3>All Team Members</h3>", unsafe_allow_html=True)
        
        all_members = db.get_all_team_members()
        
        if all_members:
            df_members = pd.DataFrame(all_members)
            display_df = df_members[['name', 'team_name', 'role', 'email', 'phone']]
            display_df.columns = ['Name', 'Team', 'Role', 'Email', 'Phone']
            
            st.dataframe(display_df, width='stretch', hide_index=True)
            
            # Remove member
            st.markdown("<br><h4>Remove Team Member</h4>", unsafe_allow_html=True)
            col1, col2 = st.columns([3, 1])
            with col1:
                member_options = {f"{m['name']} - {m['team_name']}": m['id'] for m in all_members}
                selected_member = st.selectbox("Select Member to Remove", list(member_options.keys()))
            with col2:
                if st.button("🗑️ Remove", type="secondary"):
                    if selected_member:
                        try:
                            db.remove_team_member(member_options[selected_member])
                            st.success(f"✅ {selected_member} removed successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
        else:
            st.info("No team members found. Add team members in the 'Add Team/Member' tab.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
            
            with st.form("add_team_form"):
                st.markdown("<h3>Add New Team</h3>", unsafe_allow_html=True)
                
                team_name = st.text_input("Team Name*", placeholder="e.g., Mechanics")
                team_description = st.text_area("Description", placeholder="Brief description of the team's responsibilities...")
                
                submitted = st.form_submit_button("➕ Add Team", width='stretch')
                
                if submitted:
                    if team_name:
                        try:
                            team_id = db.add_team(team_name, team_description)
                            st.success(f"✅ Team '{team_name}' added successfully! (ID: {team_id})")
                            st.balloons()
                        except Exception as e:
                            st.error(f"❌ Error adding team: {str(e)}")
                    else:
                        st.warning("⚠️ Please enter a team name")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
            
            with st.form("add_member_form"):
                st.markdown("<h3>Add Team Member</h3>", unsafe_allow_html=True)
                
                teams = db.get_all_teams()
                team_options = {t['name']: t['id'] for t in teams}
                
                if teams:
                    selected_team_name = st.selectbox("Team*", list(team_options.keys()))
                    selected_team_id = team_options[selected_team_name]
                    
                    member_name = st.text_input("Member Name*", placeholder="e.g., John Smith")
                    member_role = st.text_input("Role", placeholder="e.g., Senior Technician")
                    member_email = st.text_input("Email", placeholder="e.g., john@company.com")
                    member_phone = st.text_input("Phone", placeholder="e.g., 555-0123")
                    
                    submitted_member = st.form_submit_button("➕ Add Member", width='stretch')
                    
                    if submitted_member:
                        if member_name:
                            try:
                                member_id = db.add_team_member(
                                    selected_team_id, 
                                    member_name, 
                                    member_role, 
                                    member_email, 
                                    member_phone
                                )
                                st.success(f"✅ {member_name} added to {selected_team_name}!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                        else:
                            st.warning("⚠️ Please enter member name")
                else:
                    st.info("Create a team first before adding members")
            
            st.markdown("</div>", unsafe_allow_html=True)

# ============ MAIN APP ============

def main():
    sidebar_navigation()
    
    # Route to appropriate page
    page = st.session_state.current_page
    
    if page == "dashboard":
        render_dashboard()
    elif page == "equipment":
        render_equipment()
    elif page == "requests":
        render_requests()
    elif page == "kanban":
        render_kanban()
    elif page == "calendar":
        render_calendar()
    elif page == "teams":
        render_teams()

if __name__ == "__main__":
    main()
