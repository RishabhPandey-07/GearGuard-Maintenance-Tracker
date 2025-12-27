import sys
sys.path.insert(0, 'd:\\gearguard\\backend')

try:
    from app import create_app
    app = create_app()
    print("SUCCESS: App created successfully")
    print(f"Registered blueprints: {[bp.name for bp in app.blueprints.values()]}")
    
    with app.app_context():
        from models import Team, Equipment, MaintenanceRequest
        print(f"Teams count: {Team.query.count()}")
        print(f"Equipment count: {Equipment.query.count()}")
        print(f"Requests count: {MaintenanceRequest.query.count()}")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
