import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Case 1: Fetch Notification for a team by Valid ID
def test_fetch_team_notification_valid_id():
    response = requests.get(f"{BASE_URL}/notifications/team/2")
    assert response.status_code == 200
    assert response.json()

# Test Case 2: Fetch Notification for a team by Invalid ID
def test_fetch_team_notification_invalid_id():
    response = requests.get(f"{BASE_URL}/notifications/999")
    assert response.status_code == 404
    assert response.json['message'] == "No notifications found for this team"

# Run tests
if __name__ == "__main__":
    pytest.main()