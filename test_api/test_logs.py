import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Case 1: Retrieve All Logs (No Filters)
def test_get_all_logs():
    response = requests.get(f"{BASE_URL}/logs")
    assert response.status_code == 200
    assert response.json()

# Test Case 2: Retrieve Logs Within a Date Range
def test_get_logs_date_range():
    response = requests.get(f"{BASE_URL}/logs?start_date=2024-11-18&end_date=2024-11-19")
    assert response.status_code == 200
    assert response.json()

# Test Case 3: Filter Logs by Severity Level
def test_get_logs_severity_filter():
    response = requests.get(f"{BASE_URL}/logs?severity=ERROR")
    assert response.status_code == 200
    assert response.json()

# Run tests
if __name__ == "__main__":
    pytest.main()