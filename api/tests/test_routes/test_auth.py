from unittest.mock import MagicMock, patch
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_login():
    with patch("routers.auth.authenticator", new=MagicMock()):
        client.post(
            "/token",
            json={
                "email": "email.com",
                "username": "testuser",
                "name": "Test User",
                "password": "password"
            }
        )
