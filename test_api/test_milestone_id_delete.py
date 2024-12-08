import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Case 1: Successfully delete an existing milestone
def test_delete_existing_milestone():
    response = requests.delete(f"{BASE_URL}/milestone/1")
    assert response.status_code == 200
    assert response.json['message'] == "Milestone deleted successfully"

# Test Case 2: Attempt to delete a non-existing milestone
def test_delete_non_existing_milestone():
    response = requests.delete(f"{BASE_URL}/milestone/9999")
    assert response.status_code == 404
    assert response.json['message'] == "Milestone not found"

# Test Case 3: Delete without an ID (invalid route)
def test_delete_without_id():
    response = requests.delete(f"{BASE_URL}/milestone/")
    assert response.status_code == 404  # Flask will return 404 for unmatched routes

# Run tests
if __name__ == "__main__":
    pytest.main()