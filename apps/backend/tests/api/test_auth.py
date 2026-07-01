from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_endpoint_exists():
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "invalid@example.com",
            "password": "invalid",
        },
    )

    assert response.status_code in [200, 400, 401, 422]


def test_me_requires_authentication():
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_openapi_contains_bearer_auth():
    response = client.get("/openapi.json")

    schema = response.json()

    assert "securitySchemes" in schema["components"]
    assert "OAuth2PasswordBearer" in schema["components"]["securitySchemes"]
