import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Case 1: Successful Retrieval of Feedback Notifications
def test_get_feedback_notifications_success():
    response = requests.get(f"{BASE_URL}'/feedback/2")
    assert response.status_code == 200
    assert response.json()

# Run tests
if __name__ == "__main__":
    pytest.main()