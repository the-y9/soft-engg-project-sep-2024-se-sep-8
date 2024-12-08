import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Case 1: Successful Update of Peer Review
def test_successful_peer_review_update():
    data={
        'criteria': [{'criterion': "Collaboration", 'score': 4.7, 'comment': "Improved collaboration in recent weeks."}]
    }
    response = requests.put(f"{BASE_URL}/peer-review/2", json=data)
    assert response.status_code == 200
    assert response.get_json()['message'] == "Peer review updated successfully."

# Test Case 2: Peer Review Not Found
def test_peer_review_not_found():
    data={
        'criteria': [{'criterion': "Teamwork", 'score': 3.5, 'comment': "Needs improvement."}]
    }
    response = requests.put(f"{BASE_URL}/peer-review/9999", json=data)
    assert response.status_code == 404
    assert response.get_json()['message'] == "Peer review not found."

# Test Case 3: Invalid Request Data (Missing Criteria Field)
def test_invalid_request_data():
    data = {}
    response = requests.put(f"{BASE_URL}/peer-review/2", json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == "Invalid request data."

# Run tests
if __name__ == "__main__":
    pytest.main()