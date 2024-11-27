import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Case 1: Owner Exists
def test_owner_exists():
    response = requests.get(f"{BASE_URL}/owner/octocat")
    assert response.status_code == 200
    assert response.get_json()['message'] == "'octocat' is a valid owner name."

# Test Case 2: Owner Does Not Exist
def test_owner_not_exists():
    response = requests.get(f"{BASE_URL}/owner/nonexistentuser12345")
    assert response.status_code == 404
    assert response.get_json()['message'] == "Owner 'nonexistentuser12345' not found on GitHub."

# Run tests
if __name__ == "__main__":
    pytest.main()