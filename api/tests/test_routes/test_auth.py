import json
from unittest.mock import MagicMock, patch
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def print_response_details(response):
    print("Status Code:", response.status_code)
    print("Headers:", response.headers)
    try:
        # Attempt to parse JSON content
        content = response.json()
        print("JSON Content:", json.dumps(content, indent=4))
    except ValueError:
        # Handle responses that do not contain JSON
        print("Content:", response.content)


def test_login():
    data = {
        "email": "test@basic.com",
        "password": "pass"
    }
    with patch("routers.auth.authenticator", new=MagicMock()):
        response = client.post(
            "/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
    print_response_details(response)
    assert response.status_code == 200
