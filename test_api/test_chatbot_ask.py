import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Case 1: Successful Response
def test_successful_response():
    data={
        "question": "What is the deadline for milestone 2?",
        "api_key": "valid_api_key"
    }
    response = requests.post(f"{BASE_URL}/chatbot/ask", json=data)
    assert response.status_code == 200
    assert response.json()

# Test Case 2: Missing `question` Field
def test_missing_question_field():
    data={
        "api_key": "valid_api_key"
    }
    response = requests.post(f"{BASE_URL}/chatbot/ask", json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == "Missing question or api_key field"

# Test Case 3: Missing `api_key` Field
def test_missing_api_key_field():
    data={
        "question": "What is the deadline for milestone 2?"
    }
    response = requests.post(f"{BASE_URL}/chatbot/ask", json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == "Missing question or api_key field"

# Test Case 4: Invalid API Key
def test_invalid_api_key():
    data = {
        "question": "What is the deadline for milestone 2?",
        "api_key": "invalid_api_key"
    }
    response = requests.post(f"{BASE_URL}/chatbot/ask", json=data)
    assert response.status_code == 401
    assert response.get_json()['error'] == "Invalid API Key"

# Run tests
if __name__ == "__main__":
    pytest.main()