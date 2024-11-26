import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test 1: Valid Login
def test_valid_login():
    input = {
    "email": "johndoe@example.com",
    "password": "P@ssw0rd123"
    }
    response = requests.post(f"{BASE_URL}/user-login", json=input)
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["email"] == input["email"]
    assert data["role"] == "Student"

# Test 2: Login with username
def test_login_with_username():
    input = {
        "email": "john_doe", 
        "password": "P@ssw0rd123"
    }
    response = requests.post(f"{BASE_URL}/user-login", json=input)
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["email"] == input["email"]

# Test 3: Missing Email or Username
def test_missing_email_or_username():
    input = {
        "password": "P@ssw0rd123"
    }
    response = requests.post(f"{BASE_URL}/user-login", json=input)
    assert response.status_code == 400
    assert response.json()["message"] == "Email or Username not provided"

# Test 4: Missing Password
def test_missing_password():
    input = {
        "email":"johndoe@example.com"
    }
    response = requests.post(f"{BASE_URL}/user-login", json=input)
    assert response.status_code == 400
    assert response.json()["message"] == "Password not provided"

# Test 5: Incorrect Password
def test_incorrect_password():
    input = {
    "email": "johndoe@example.com",
    "password": "WrongPassword"
    }
    response = requests.post(f"{BASE_URL}/user-login", json=input)
    assert response.status_code == 400
    assert response.json()["message"] == "Wrong password"

# Test 6: User Not Found
def test_user_not_found():
    input = {
    "email": "nonexistent@example.com",
    "password": "P@ssw0rd123"
    }
    response = requests.post(f"{BASE_URL}/user-login", json=input)
    assert response.status_code == 404
    assert response.json()["message"] == "Email or Username not found."

# Test 7: Inactive User
def test_inactive_user():
    input = {
    "email": "inactive@example.com",
    "password": "P@ssw0rd123"
    }
    response = requests.post(f"{BASE_URL}/user-login", json=input)
    assert response.status_code == 403
    assert response.json()["message"] == "User not activated"

# Run tests
if __name__ == "__main__":
    pytest.main()