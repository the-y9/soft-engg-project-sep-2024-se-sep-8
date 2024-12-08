import pytest
from unittest.mock import patch
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Case 1: Valid Input Data
@patch('requests.post')
def test_valid_input(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "students_needing_support": [{"student_id": 101, "risk_level": "low", "recommendations": "Keep up the good work!"}]
    }
    input={
        "students_data": [{"student_id": 101, "coding_activity": 78.5, "task_completion_rate": 85.0, "engagement_score": 90.5}]
    }
    response = requests.post(f"{BASE_URL}/students/performance-prediction", json=input)
    assert response.status_code == 200
    assert response.json == {
        "students_needing_support": [{"student_id": 101, "risk_level": "low", "recommendations": "Keep up the good work!"}]
    }

# Test Case 2: Missing 'students_data' Field
def test_missing_students_data():
    input={}
    response = requests.post(f"{BASE_URL}/students/performance-prediction", json=input)
    assert response.status_code == 400
    assert response.json['message'] == "Missing students data"

# Test Case 3: External API Error Handling
@patch('requests.post')
def test_external_api_error(mock_post):
    mock_post.return_value.status_code = 500
    input={
        "students_data": [{"student_id": 101, "coding_activity": 78.5, "task_completion_rate": 85.0, "engagement_score": 90.5}]
    }
    response = requests.post(f"{BASE_URL}/students/performance-prediction", json=input)
    assert response.status_code == 500
    assert response.json['message'] == "Error from GenAI model"

# Run tests
if __name__ == "__main__":
    pytest.main()