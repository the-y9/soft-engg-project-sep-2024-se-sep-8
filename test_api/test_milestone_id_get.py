import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Case 1: Get Milestone Data
def test_valid_milestone():
    response = requests.get(f"{BASE_URL}/milestone/1")
    assert response.status_code == 200
    assert response.json()

# Test Case 2: Non-Existent Milestone ID
def test_non_existent_milestone():
    response = requests.get(f"{BASE_URL}/milestone/999")
    assert response.status_code == 404
    assert response.json['message'] == 'Milestone not found'

# Run tests
if __name__ == "__main__":
    pytest.main()