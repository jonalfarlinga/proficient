import json
from unittest.mock import MagicMock, patch
from authenticator import get_authenticator, get_current_user
from models import UserOut
from main import app
from fastapi.testclient import TestClient
from queries.users import UsersRepo

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


def fake_get_auth():
    class FakeAuth:
        def verify_password(self, email, password, repo):
            if email == "wrong_email":
                return None
            if password == "wrong_pass":
                return None
            return UserOut(
                name="John Doe",
                email="test@basic.com",
                id=1,
                username="basicuser"
            )
    return FakeAuth()


class FakeUsers:
    pass


def test_login():
    # Arrange
    data = {
        "username": "test@basic.com",
        "password": "pass"
    }
    app.dependency_overrides[get_authenticator] = fake_get_auth
    app.dependency_overrides[UsersRepo] = FakeUsers
    mock_create_token = MagicMock()
    mock_create_token.return_value = "access_token"

    # Act
    with patch("routers.auth.create_access_token", new=mock_create_token):
        response = client.post(
            "/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
    # Assert
    assert response.status_code == 200
    assert response.headers['content-type'] == "application/json"
    assert response.json().get('access_token') == "access_token"


def test_login_wrong_pass():
    # Arrange
    data = {
        "username": "test@basic.com",
        "password": "wrong_pass"
    }
    app.dependency_overrides[get_authenticator] = fake_get_auth
    app.dependency_overrides[UsersRepo] = FakeUsers
    mock_create_token = MagicMock()
    mock_create_token.return_value = "access_token"

    # Act
    with patch("routers.auth.create_access_token", new=mock_create_token):
        response = client.post(
            "/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

    # Assert
    assert response.status_code == 401
    assert response.headers['content-type'] == "application/json"
    assert response.json().get('detail') == "Incorrect email or password"


def test_login_wrong_email():
    # Arrange
    data = {
        "username": "wrong_email",
        "password": "pass"
    }
    app.dependency_overrides[get_authenticator] = fake_get_auth
    app.dependency_overrides[UsersRepo] = FakeUsers
    mock_create_token = MagicMock()
    mock_create_token.return_value = "access_token"

    # Act
    with patch("routers.auth.create_access_token", new=mock_create_token):
        response = client.post(
            "/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

    # Assert
    assert response.status_code == 401
    assert response.headers['content-type'] == "application/json"
    assert response.json().get('detail') == "Incorrect email or password"

    # Clean Up
    app.dependency_overrides = {}

