import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Team Performance API
def test_team_performance():
    response = requests.get(f"{BASE_URL}/teams/performance")
    assert response.status_code == 200
    assert "teams" in response.json()
    
if __name__ == "__main__":
    pytest.main()