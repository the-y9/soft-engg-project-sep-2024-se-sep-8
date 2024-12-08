import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Case 1: Get all the milestones for a project
def test_valid_project_with_milestones():
    response = requests.get(f"{BASE_URL}/project/1/milestones")
    assert response.status_code == 200
    assert response.json()

# Test Case 2: Project with No Milestones
def test_valid_project_no_milestones():
    response = requests.get(f"{BASE_URL}/project/2/milestones")
    assert response.status_code == 404
    assert response.json['message'] == 'Milestones not found for the project'

# Test Case 3: Invalid Project ID (String)
def test_invalid_project_id(client):
    response = client.get('/project//milestones')
    assert response.status_code == 404  # Flask returns 404 for invalid path parameters

# Run tests
if __name__ == "__main__":
    pytest.main()