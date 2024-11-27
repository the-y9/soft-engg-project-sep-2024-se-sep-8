import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Case 1: Search with a Valid Keyword
def test_search_logs_with_valid_keyword():
    data={"keyword": "error"}
    response = requests.post(f"{BASE_URL}/logs/search",json=data)
    assert response.status_code == 200
    assert response.json()

# Test Case 2: Missing Keyword in Request Body
def test_search_logs_missing_keyword():
    data={}
    response = requests.post(f"{BASE_URL}/logs/search",json=data)
    assert response.status_code == 400
    assert response.json['message'] == "Keyword is required for searching logs."

# Run tests
if __name__ == "__main__":
    pytest.main()