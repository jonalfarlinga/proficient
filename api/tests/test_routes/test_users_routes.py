import json
from unittest.mock import MagicMock, patch
from authenticator import get_authenticator
from models import UserOut
from main import app
from fastapi.testclient import TestClient
from queries.users import UsersRepo

client = TestClient(app)


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

        def get_hashed_password(self, password):
            return password
    return FakeAuth()


class FakeUsers:
    def get_user(self, email=None):
        if email == 'test@basic.com':
            return UserOut(
                name="John Doe",
                email="test@basic.com",
                id=1,
                username="basicuser"
            )
        elif email == 'jane@basic.com':
            return UserOut(
                name="Jane Doe",
                email="jane@basic.com",
                id=2,
                username="superuser"
            )
        elif email is None:
            return [
                UserOut(
                    name="John Doe",
                    email="test@basic.com",
                    id=1,
                    username="basicuser"
                ),
                UserOut(
                    name="Jane Doe",
                    email="jane@basic.com",
                    id=2,
                    username="superuser"
                )
            ]
        else:
            return None

    def create_user(self, user):
        return UserOut(
            id=1,
            **user.model_dump()
        )


def test_get_user():
    # Arrange
    app.dependency_overrides[UsersRepo] = FakeUsers

    # Act
    response = client.get(
        "/api/users",
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0].get('name') == "John Doe"
    assert data[1].get('name') == "Jane Doe"

    # Clean Up
    app.dependency_overrides = {}


def test_get_user_by_email():
    # Arrange
    app.dependency_overrides[UsersRepo] = FakeUsers

    # Act
    response = client.get(
        "/api/users",
        params={"email": "test@basic.com"}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data.get('name') == "John Doe"

    # Clean Up
    app.dependency_overrides = {}


def test_get_user_no_match():
    # Arrange
    app.dependency_overrides[UsersRepo] = FakeUsers

    # Act
    response = client.get(
        "/api/users",
        params={"email": "@basic.com"}
    )

    # Assert
    assert response.status_code == 404

    # Clean Up
    app.dependency_overrides = {}


def test_create_user():
    # Arrange
    app.dependency_overrides[UsersRepo] = FakeUsers
    app.dependency_overrides[get_authenticator] = fake_get_auth
    data = json.dumps({
        "username": "newuser",
        "name": "Bob Doe",
        "password": "pass",
        "email": "doe@email.com",
    })
    mock_create_token = MagicMock()
    mock_create_token.return_value = "access_token"

    # Act
    with patch("routers.users.create_access_token", new=mock_create_token):
        response = client.post(
            "/api/users",
            data=data,
            headers={"Content-Type": "application/json"}
        )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data.get('access_token')
    assert data.get('token_type')
    assert data.get('user') and data['user'].get('name') == "Bob Doe"
