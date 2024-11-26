import pytest
import requests
from datetime import datetime


BASE_URL = "http://127.0.0.1:5000"


# Helper function for creating test data
def create_project(title, description="Test Project Description"):
    print("Running tests...")

    return requests.post(f"{BASE_URL}/project", json={"title": title, "description": description})


def create_milestone(project_id, task_no, task, description="Test Milestone", deadline=None):

    if not deadline:
        deadline = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return requests.post(
        f"{BASE_URL}/milestone",
        json={"project_id": project_id, "task_no": task_no, "task": task, "description": description, "deadline": deadline}
    )


@pytest.fixture(scope="module")
def setup_project():
    """Fixture to set up a project for testing."""
    response = create_project("Test Project")
    assert response.status_code == 200
    return response.json()


@pytest.fixture(scope="module")
def setup_milestone(setup_project):
    """Fixture to set up a milestone for the created project."""
    project_id = setup_project["id"]
    response = create_milestone(project_id, 1, "Test Task")
    assert response.status_code == 201
    return response.json()


# Test the Reminder Manager API
def test_send_reminder_notifications(setup_milestone):
    response = requests.post(f"{BASE_URL}/reminders/send")
    assert response.status_code == 200
    assert response.json()["message"] == "Reminder notifications sent successfully"


# Test Submission Validation API
def test_submission_validation(setup_milestone):
    data = {
        "submission": "Test data for GenAI validation",
        "project_id": setup_milestone["project_id"],
        "milestone_id": setup_milestone["id"]
    }
    response = requests.post(f"{BASE_URL}/submission/validate", json=data)
    assert response.status_code == 200
    assert "validation_result" in response.json()


# Test Performance Prediction API
def test_performance_prediction():
    data = {
        "students_data": [{"id": 1, "name": "Test Student", "scores": [80, 90, 70]}]
    }
    response = requests.post(f"{BASE_URL}/students/performance-prediction", json=data)
    assert response.status_code == 200
    assert "students_needing_support" in response.json()


# Test Documentation Chatbot API
def test_documentation_chatbot():
    data = {"question": "How do I create a project?"}
    response = requests.post(f"{BASE_URL}/chatbot/ask", json=data)
    assert response.status_code == 200
    assert "response" in response.json()


# Test Team Performance API
def test_team_performance():
    response = requests.get(f"{BASE_URL}/teams/performance")
    assert response.status_code == 200
    assert "teams" in response.json()


# Test Instructor Feedback Notifications API
def test_instructor_feedback_notifications(setup_project):
    project_id = setup_project["id"]
    response = requests.get(f"{BASE_URL}/feedback/{project_id}")
    assert response.status_code == 200
    assert "feedback_notifications" in response.json()

    
if __name__ == "__main__":
    pytest.main()