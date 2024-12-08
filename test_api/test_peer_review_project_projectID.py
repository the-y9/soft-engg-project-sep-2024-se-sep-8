import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Case 1: Successful Retrieval of Peer Reviews
def test_successful_peer_review_retrieval():
    response = requests.get(f"{BASE_URL}/peer-review/project/1")
    assert response.status_code == 200
    assert response.json()

# Test Case 2: No Peer Reviews Found
def test_no_peer_reviews_found():
    response = requests.get(f"{BASE_URL}/peer-review/project/9999")
    assert response.status_code == 404
    assert response.get_json()['message'] == "No peer reviews found for project ID 9999."

# Run tests
if __name__ == "__main__":
    pytest.main()