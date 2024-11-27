import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Case 1: Successful Deletion of Peer Review
def test_successful_peer_review_deletion():
    response = requests.delete(f"{BASE_URL}/peer-review/2")
    assert response.status_code == 200
    assert response.get_json()['message'] == "Peer review deleted successfully."

# Test Case 2: Peer Review Not Found
def test_peer_review_not_found():
    response = requests.delete(f"{BASE_URL}/peer-review/9999")
    assert response.status_code == 404
    assert response.get_json()['message'] == "Peer review not found."

# Run tests
if __name__ == "__main__":
    pytest.main()