import requests
import pytest

BASE_URL = "http://localhost:5000/init_gitlab"

def test_user_creation_failure():
    payload = {
        "users": [
            ("Existing", "existinguser", "password", "exist@example.com")
        ]
    }
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 200
    json_body = response.json()
    assert any(user["status"] == "failed" for user in json_body)


