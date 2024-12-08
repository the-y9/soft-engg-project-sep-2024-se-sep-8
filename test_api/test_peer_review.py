import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Case 1: Successful Peer Review Submission
def test_successful_peer_review_submission():
    data = {
        "reviewerId": 2,
        "projectId": 1,
        "criteria": [
            {"criterion": "Code Quality", "score": 4.5, "comment": "Well-written code."},
            {"criterion": "Collaboration", "score": 5, "comment": "Excellent teamwork."}
        ]
    }
    response = requests.post(f"{BASE_URL}/peer-review", json=data)
    assert response.status_code == 201
    assert response.json['message'] == "Peer review submitted successfully."

# Test Case 2: Missing reviewerId
def test_missing_reviewer_id():
    data = {
        "projectId": 1001,
        "criteria": [{"criterion": "Code Quality", "score": 4.5, "comment": "Well-written code."}]
    }
    response = requests.post(f"{BASE_URL}/peer-review", json=data)
    assert response.status_code == 400
    assert response.json['message'] == "Invalid request data."

# Test Case 3: Criteria missing
def test_criteria_missing():
    data = {"reviewerId": 201, "projectId": 1001}
    response = requests.post(f"{BASE_URL}/peer-review", json=data)
    assert response.status_code == 400
    assert response.json['message'] == "Invalid request data."

# Test Case 4: Missing projectId
def test_missing_project_id():
    data = {
        "reviewerId": 201,
        "criteria": [{"criterion": "Code Quality", "score": 4.5, "comment": "Well-written code."}]
    }
    response = requests.post(f"{BASE_URL}/peer-review", json=data)
    assert response.status_code == 400
    assert response.json['message'] == "Invalid request data."

# Run tests
if __name__ == "__main__":
    pytest.main()