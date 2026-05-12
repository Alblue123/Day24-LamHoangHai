import requests
import json
import sys

# Ensure UTF-8 output for Windows terminal
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:8000"

def test_endpoint(name, path, token, expected_status):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}{path}", headers=headers)
        print(f"--- Test: {name} ---")
        print(f"Path: {path} | Role: {token.split('-')[1]}")
        print(f"Status: {response.status_code} (Expected: {expected_status})")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                print(f"Data Sample (First 1 Record): {json.dumps(data[0], indent=2, ensure_ascii=False)}")
            else:
                print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"Error testing {name}: {e}")
    print("-" * 30)

# 1. Admin accessing raw data (Allowed)
test_endpoint("Admin access Raw PII", "/api/patients/raw", "token-alice", 200)

# 2. ML Engineer accessing raw data (Forbidden)
test_endpoint("ML Engineer access Raw PII", "/api/patients/raw", "token-bob", 403)

# 3. ML Engineer accessing anonymized data (Allowed)
test_endpoint("ML Engineer access Anonymized Data", "/api/patients/anonymized", "token-bob", 200)

# 4. Data Analyst accessing metrics (Allowed)
test_endpoint("Data Analyst access Aggregated Metrics", "/api/metrics/aggregated", "token-carol", 200)

# 5. Check Health and Prometheus Metrics
print("\nChecking Metrics Exposure...")
r = requests.get(f"{BASE_URL}/metrics")
print(f"Prometheus Metrics Status: {r.status_code}")
if "http_request_duration_seconds" in r.text:
    print("Prometheus Metrics found in output.")
