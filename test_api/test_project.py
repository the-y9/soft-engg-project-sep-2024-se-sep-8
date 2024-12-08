import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test 1: Tests successful project creation with a description.
def test_create_project_success():
    data = {
        "title": "Web App Development", 
        "description": "A project to develop a web app."
    }
    response = requests.post(f"{BASE_URL}/project", json=data)
    assert response.status_code == 201
    assert response.json['title'] == "Web App Development"

# Test 2: Tests successful project creation without a description.
def test_create_project_without_description():
    data = {"title": "Web App Development"}
    response = requests.post(f"{BASE_URL}/project", json=data)
    assert response.status_code == 201
    assert response.json['description'] == ""

# Test 3: Project title missing
def test_create_project_missing_title():
    data = {"description": "No title provided"}
    response = requests.post(f"{BASE_URL}/project", json=data)
    assert response.status_code == 400
    assert response.json['message'] == "Project title is required"

# Test 4: Duplicate project
def test_create_project_duplicate_title():
    data = {"title": "Existing Project"}
    project_first_copy = requests.post(f"{BASE_URL}/project", json=data)
    response = requests.post(f"{BASE_URL}/project", json=data) #Creating duplicate copy of the project
    assert response.status_code == 400
    assert response.json['message'] == "Project with this title already exists"

# Run tests
if __name__ == "__main__":
    pytest.main()