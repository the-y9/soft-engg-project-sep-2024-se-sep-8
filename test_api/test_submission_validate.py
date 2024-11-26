import pytest
from unittest.mock import patch
import requests

BASE_URL = "http://127.0.0.1:5000"


# Test Case 1: Valid Submission Data
@patch('requests.post')
def test_submission_validation_success(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "is_valid": True,
        "feedback": "The submission meets all milestone requirements. Excellent work!"
    }

    input={
        "submission": "Implemented a REST API for project management system.",
        "project_id": 101,
        "milestone_id": 10
    }
    response = requests.post(f"{BASE_URL}/submission/validate", json=input)
    assert response.status_code == 200
    data = response.get_json()
    assert data['validation_result']['is_valid'] == True
    assert data['feedback'] == "The submission meets all milestone requirements. Excellent work!"

# Test Case 2: Missing Required Fields
def test_submission_validation_missing_fields():
    input={
        "project_id": 101,
        "milestone_id": 10
    }
    response = requests.post(f"{BASE_URL}/submission/validate", json=input)
    assert response.status_code == 400
    data = response.get_json()
    assert data['message'] == "Missing required fields"

# Test Case 3: Non-existent Milestone ID
def test_submission_validation_milestone_not_found():
    input={
        "submission": "Sample submission",
        "project_id": 101,
        "milestone_id": 999  # Invalid milestone ID
    }
    response = requests.post(f"{BASE_URL}/submission/validate", json=input)
    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == "Milestone not found"

# Test Case 4: GenAI Model Returns an Error
@patch('requests.post')
def test_submission_validation_genai_error(mock_post):
    mock_post.return_value.status_code = 500

    input={
        "submission": "Sample submission",
        "project_id": 101,
        "milestone_id": 10
    }
    response = requests.post(f"{BASE_URL}/submission/validate", json=input)
    assert response.status_code == 500
    data = response.get_json()
    assert data['message'] == "Error from GenAI model"

# Test Case 5: Connection Failure to GenAI Service
@patch('requests.post')
def test_submission_validation_genai_connection_failure(mock_post):
    mock_post.side_effect = Exception("Connection to GenAI model failed")

    input={
        "submission": "Sample submission",
        "project_id": 101,
        "milestone_id": 10
    }
    response = requests.post(f"{BASE_URL}/submission/validate", json=input)
    assert response.status_code == 500
    data = response.get_json()
    assert data['ERROR'] == "Connection to GenAI model failed"

# Run tests
if __name__ == "__main__":
    pytest.main()