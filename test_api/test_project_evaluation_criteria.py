import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Case 1: Add Criterias for evaluation
def test_add_criteria_list():
    data = {
        "criteriaList": [
            {"criterion": "Code Quality", "description": "Measures code efficiency"},
            {"criterion": "Collaboration", "description": "Teamwork assessment"}
        ]
    }
    response = requests.post(f"{BASE_URL}/project/1/evaluation-criteria", json=data)
    assert response.status_code == 201
    assert response.json['message'] == "Evaluation criteria added successfully"

# Test Case 2: Missing criteriaList
def test_missing_criteria_list():
    response = requests.post(f"{BASE_URL}/project/1/evaluation-criteria", json={})
    assert response.status_code == 400
    assert response.json['message'] == "Invalid data format. Please provide a valid criteria list."

# Test Case 3: Project Not Found
def test_project_not_found():
    data = {
        "criteriaList": [{"criterion": "Code Quality", "description": "Measures code efficiency"}]
    }
    response = requests.post(f"{BASE_URL}/project/1/evaluation-criteria", json=data)
    assert response.status_code == 404
    assert response.json['message'] == "Project with ID 999 not found."

# Test Case 4: Missing Criterion Name
def test_missing_criterion_name():
    data = {
        "criteriaList": [{"description": "Measures code efficiency"}]
    }
    response = requests.post(f"{BASE_URL}/project/1/evaluation-criteria", json=data)
    assert response.status_code == 400
    assert response.json['message'] == "Each criterion must have a name."

# Run tests
if __name__ == "__main__":
    pytest.main()