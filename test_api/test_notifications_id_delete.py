import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Case 1: Delete Notification by Valid ID
def test_delete_notification_valid_id():
    response = requests.delete(f"{BASE_URL}/notifications/10")
    assert response.status_code == 200
    assert response.json['message'] == "Notification deleted successfully"

# Test Case 2: Delete Notification by Invalid ID
def test_delete_notification_invalid_id():
    response = requests.get(f"{BASE_URL}/notifications/999")
    assert response.status_code == 404
    assert response.json['message'] == "Notification not found"

# Run tests
if __name__ == "__main__":
    pytest.main()