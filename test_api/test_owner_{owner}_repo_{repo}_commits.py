import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Case 1: Get Respository Commits
def test_valid_owner_and_repo():
    response = requests.get(f"{BASE_URL}/owner/octocat/repo/Hello-World/commits")
    assert response.status_code == 200
    assert response.json()

# Test Case 2: Valid Owner but Repository Does Not Exist
def test_repo_not_found():
    response = requests.get(f"{BASE_URL}/owner/octocat/repo/NonExistentRepo/commits")
    assert response.status_code == 404
    assert response.get_json()['message'] == "Error: Repository 'NonExistentRepo' not found!"

# Run tests
if __name__ == "__main__":
    pytest.main()