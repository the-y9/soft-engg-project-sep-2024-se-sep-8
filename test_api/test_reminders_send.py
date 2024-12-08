import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Case 1: Successful Trigger of Reminder Notifications
def test_send_reminders_success():
    response = requests.post(f"{BASE_URL}/reminders/send")
    assert response.status_code == 200
    assert response.json['message'] == "Reminder notifications sent successfully."

# Run tests
if __name__ == "__main__":
    pytest.main()