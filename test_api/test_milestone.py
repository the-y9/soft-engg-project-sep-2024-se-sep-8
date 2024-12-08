import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Case 1: Create milestone successfully
def test_create_milestone_success():
    data = {
        "project_id": 1,
        "task_no": 1,
        "task": "Design schema",
        "description": "Design the database schema",
        "deadline": "2024-11-20 23:59:59"
    }
    response = requests.post(f"{BASE_URL}/milestone", json=data)
    assert response.status_code == 201
    assert response.json['task'] == "Design schema"

# Test Case 2: Project not found
def test_create_milestone_project_not_found():
    data = {
        "project_id": 9999,
        "task_no": 1,
        "task": "Invalid project"
    }
    response = requests.post(f"{BASE_URL}/milestone", json=data)
    assert response.status_code == 404
    assert response.json['message'] == "Project not found"

# Test Case 3: Missing project_id
def test_create_milestone_missing_project_id():
    data = {
        "task_no": 1,
        "task": "Missing project_id"
    }
    response = requests.post(f"{BASE_URL}/milestone", json=data)
    assert response.status_code == 400
    assert "Invalid data for creating project or milestone" in response.json['message']

# Test Case 4: Missing task
def test_create_milestone_missing_task():
    data = {
        "project_id": 1,
        "task_no": 1
    }
    response = requests.post(f"{BASE_URL}/milestone", json=data)
    assert response.status_code == 400
    assert "Invalid data for creating project or milestone" in response.json['message']

# Test Case 5: Missing task_no
def test_create_milestone_invalid_task_no():
    data = {
        "project_id": 1,
        "task": "Missing task_no"
    }
    response = requests.post(f"{BASE_URL}/milestone", json=data)
    assert response.status_code == 400
    assert "Invalid data for creating project or milestone" in response.json['message']

# Run tests
if __name__ == "__main__":
    pytest.main()