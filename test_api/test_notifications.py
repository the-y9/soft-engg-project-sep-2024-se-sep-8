import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Case 1: Create Notification
def test_create_notification_valid():
    data={
        "title": "Reminder",
        "message": "Submit by tomorrow",
        "created_for": 5,
        "created_by": 1
    }
    response = requests.post(f"{BASE_URL}/notifications",json=data)
    assert response.status_code == 200
    assert response.json['message'] == "Notification created successfully."

# Test Case 2: Create Notification with Missing Fields
def test_create_notification_missing_fields():
    data={
        "title": "Reminder",
        "created_for": 5
    }
    response = requests.post(f"{BASE_URL}/notifications",json=data)
    assert response.status_code == 400
    assert response.json['message'] == "Missing required fields"

# Run tests
if __name__ == "__main__":
    pytest.main()