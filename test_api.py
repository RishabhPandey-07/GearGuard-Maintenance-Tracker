import sys
sys.path.insert(0, 'd:\\gearguard\\backend')

from app import create_app
import json

app = create_app()
client = app.test_client()

print("=" * 50)
print("TESTING GEARGUARD API ENDPOINTS")
print("=" * 50)

# Test 1: Health Check
print("\n1. Testing /api/health")
response = client.get('/api/health')
print(f"   Status: {response.status_code}")
print(f"   Data: {response.json}")

# Test 2: Dashboard Stats
print("\n2. Testing /api/dashboard/stats")
response = client.get('/api/dashboard/stats')
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json
    print(f"   Equipment: {data.get('total_equipment')}")
    print(f"   Active Requests: {data.get('active_requests')}")
    print(f"   Teams: {data.get('total_teams')}")

# Test 3: Get All Equipment
print("\n3. Testing /api/equipment/")
response = client.get('/api/equipment/')
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    equipment = response.json
    print(f"   Count: {len(equipment)}")
    if equipment:
        print(f"   First: {equipment[0].get('name')}")

# Test 4: Get All Requests
print("\n4. Testing /api/requests/")
response = client.get('/api/requests/')
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    requests = response.json
    print(f"   Count: {len(requests)}")
    if requests:
        print(f"   First: {requests[0].get('subject')}")

# Test 5: Get All Teams
print("\n5. Testing /api/teams/")
response = client.get('/api/teams/')
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    teams = response.json
    print(f"   Count: {len(teams)}")
    for team in teams:
        print(f"   - {team.get('name')}")

# Test 6: Requests by Team Chart
print("\n6. Testing /api/dashboard/requests-by-team")
response = client.get('/api/dashboard/requests-by-team')
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json
    print(f"   Data points: {len(data)}")

# Test 7: Equipment by Category Chart
print("\n7. Testing /api/dashboard/equipment-by-category")
response = client.get('/api/dashboard/equipment-by-category')
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json
    print(f"   Categories: {len(data)}")

print("\n" + "=" * 50)
print("ALL TESTS COMPLETED")
print("=" * 50)
