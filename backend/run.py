"""
GearGuard Backend Server
Run this file to start the Flask API server
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    try:
        from app import create_app
        
        app = create_app()
        
        print("\n" + "="*50)
        print("  GEARGUARD BACKEND SERVER")
        print("="*50)
        print(f"  Server running on: http://localhost:5000")
        print(f"  API endpoints: http://localhost:5000/api/")
        print("="*50 + "\n")
        
        app.run(debug=True, port=5000, host='0.0.0.0')
        
    except Exception as e:
        print(f"\nERROR: Failed to start backend server")
        print(f"Reason: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check if port 5000 is already in use")
        print("3. Verify database file permissions")
        sys.exit(1)
