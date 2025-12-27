"""
Backend Status Checker
Verifies that the backend is properly configured and working
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def check_backend():
    print("\n" + "="*60)
    print("  GEARGUARD BACKEND STATUS CHECK")
    print("="*60 + "\n")
    
    # Check 1: Import modules
    print("1. Checking imports...")
    try:
        from app import create_app
        from models import Team, Equipment, MaintenanceRequest
        print("   [OK] All modules imported successfully")
    except Exception as e:
        print(f"   [FAIL] Import failed: {e}")
        return False
    
    # Check 2: Create app
    print("\n2. Creating Flask app...")
    try:
        app = create_app()
        print("   [OK] Flask app created successfully")
    except Exception as e:
        print(f"   [FAIL] App creation failed: {e}")
        return False
    
    # Check 3: Database
    print("\n3. Checking database...")
    try:
        with app.app_context():
            team_count = Team.query.count()
            equipment_count = Equipment.query.count()
            request_count = MaintenanceRequest.query.count()
            
            print(f"   [OK] Database connected")
            print(f"     - Teams: {team_count}")
            print(f"     - Equipment: {equipment_count}")
            print(f"     - Requests: {request_count}")
            
            if team_count == 0 or equipment_count == 0:
                print("   [WARN] Warning: Database appears empty")
    except Exception as e:
        print(f"   [FAIL] Database check failed: {e}")
        return False
    
    # Check 4: API endpoints
    print("\n4. Testing API endpoints...")
    try:
        client = app.test_client()
        
        endpoints = [
            ('/api/health', 'Health Check'),
            ('/api/equipment/', 'Equipment List'),
            ('/api/requests/', 'Requests List'),
            ('/api/teams/', 'Teams List'),
            ('/api/dashboard/stats', 'Dashboard Stats')
        ]
        
        all_ok = True
        for endpoint, name in endpoints:
            response = client.get(endpoint)
            if response.status_code == 200:
                print(f"   [OK] {name}: OK")
            else:
                print(f"   [FAIL] {name}: Failed (Status {response.status_code})")
                all_ok = False
        
        if not all_ok:
            return False
            
    except Exception as e:
        print(f"   [FAIL] API test failed: {e}")
        return False
    
    print("\n" + "="*60)
    print("  [SUCCESS] ALL CHECKS PASSED - BACKEND IS READY!")
    print("="*60 + "\n")
    print("To start the backend server, run:")
    print("  cd backend")
    print("  python run.py")
    print("\nOr use the start.bat script to start both backend and frontend.")
    print()
    
    return True

if __name__ == '__main__':
    success = check_backend()
    sys.exit(0 if success else 1)
