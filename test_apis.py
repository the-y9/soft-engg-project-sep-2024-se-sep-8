import pytest
import requests
from datetime import datetime

# Base URL for the API
BASE_URL = "http://127.0.0.1:5000"  # Replace with your server's actual base URL


# Helper function for creating test data
def create_project(title, description="Test Project Description"):
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


# Test the Project Manager APIs
def test_create_project():
    response = create_project("Another Test Project")
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["title"] == "Another Test Project"


def test_get_project_milestones(setup_project, setup_milestone):
    project_id = setup_project["id"]
    response = requests.get(f"{BASE_URL}/project/{project_id}/milestones")
    assert response.status_code == 200
    milestones = response.json()["milestones"]
    assert len(milestones) > 0
    assert milestones[0]["task"] == "Test Task"


def test_delete_milestone(setup_milestone):
    milestone_id = setup_milestone["id"]
    response = requests.delete(f"{BASE_URL}/milestone/{milestone_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Milestone deleted successfully"


# Test Notification Manager APIs
def test_create_notification():
    response = requests.post(
        f"{BASE_URL}/notifications",
        json={"title": "Test Notification", 
              "message": "This is a test.", 
              "created_for": 1, 
              "created_by": 1}
    )
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_notification_by_id():
    notification = requests.post(
        f"{BASE_URL}/notifications",
        json={"title": "Notification by ID", "message": "Check by ID.", "created_for": 1, "created_by": 1}
    ).json()
    response = requests.get(f"{BASE_URL}/notifications/{notification['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Notification by ID"


def test_delete_notification():
    notification = requests.post(
        f"{BASE_URL}/notifications",
        json={"title": "Notification to Delete", "message": "To be deleted.", "created_for": 1, "created_by": 1}
    ).json()
    response = requests.delete(f"{BASE_URL}/notifications/{notification['id']}")
    assert response.status_code == 200
    assert response.json()["message"] == "Notification deleted successfully"


# Test GitHub Repo API
def test_get_repo_commits():
    response = requests.get(f"{BASE_URL}/owner/octocat/repo/Hello-World/commits")
    assert response.status_code == 200
    assert "total_commits" in response.json()


# Test the AI Integration APIs
def test_assessment_feedback_api():
    response = requests.post(
        f"{BASE_URL}/genai/feedback",
        json={"submission": "Test data for GenAI feedback"}
    )
    assert response.status_code == 200
    assert "feedback" in response.json()


def test_performance_prediction_api():
    response = requests.post(
        f"{BASE_URL}/genai/performance",
        json={"students_data": [{"id": 1, "name": "Test Student", "scores": [80, 90, 70]}]}
    )
    assert response.status_code == 200
    assert "students_needing_support" in response.json()


if __name__ == "__main__":
    pytest.main()
