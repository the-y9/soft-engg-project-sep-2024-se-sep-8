import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Case 1: Successfully delete an existing project
def test_delete_existing_project():
    response = requests.delete(f"{BASE_URL}/project/1/milestones")
    assert response.status_code == 200
    assert response.json['message'] == "Project deleted successfully"

# Test Case 2: Attempt to delete a non-existing project
def test_delete_non_existing_project():
    response = requests.delete(f"{BASE_URL}/project/9999/milestones")
    assert response.status_code == 404
    assert response.json['message'] == "Project not found"

# Test Case 3: Delete without a project ID (invalid route)
def test_delete_without_project_id():
    response = requests.delete(f"{BASE_URL}/project//milestones")
    assert response.status_code == 404  # Flask will return 404 for unmatched routes

# Run tests
if __name__ == "__main__":
    pytest.main()