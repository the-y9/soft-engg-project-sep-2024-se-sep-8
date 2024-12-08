import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test 1: Valid User Signup
def test_valid_user_signup():
    data = {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "password": "P@ssw0rd123"
    }
    response = requests.post(f"{BASE_URL}/user-signup", json=data)
    assert response.status_code == 201
    assert response.json()['message'] == "Successfully registered as student."

# Test 2: Missing Password Field
def test_missing_password():
    data = {
        "username": "johndoe",
        "email": "johndoe@example.com"
    }
    response = requests.post(f"{BASE_URL}/user-signup", json=data)
    assert response.status_code == 400
    assert response.json()['message'] == "Password not provided"

# Test 3: Email Already Registered
def test_email_already_registered():
    data = {
        "username": "existingUser",
        "email": "existing@example.com",
        "password": "P@ssw0rd123"
    }
    response = requests.post(f"{BASE_URL}/user-signup", json=data)
    assert response.status_code == 400
    assert response.json()['message'] == "Email already registered"

# Run tests
if __name__ == "__main__":
    pytest.main()