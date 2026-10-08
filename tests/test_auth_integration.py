"""HTTP-to-database integration coverage for authentication and task protection."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import models
from app.security import (
    TOKEN_ISSUER,
    get_auth_secret_key,
    validate_auth_config,
    verify_password,
)
from tests.conftest import TEST_PASSWORD

TEST_SECRET = "test-only-secret-key-with-at-least-32-bytes"


@pytest.mark.parametrize(
    "secret",
    ["", "short", "replace-with-a-random-secret-of-at-least-32-characters"],
)
def test_auth_configuration_rejects_missing_short_or_example_secret(
    monkeypatch: pytest.MonkeyPatch,
    secret: str,
) -> None:
    monkeypatch.setenv("AUTH_SECRET_KEY", secret)

    with pytest.raises(RuntimeError, match="AUTH_SECRET_KEY"):
        validate_auth_config()


def test_registration_persists_only_a_password_hash(
    unauthenticated_client: TestClient,
    db_session: Session,
) -> None:
    response = unauthenticated_client.post(
        "/auth/register",
        json={"email": "New.User@example.com", "password": TEST_PASSWORD},
    )

    assert response.status_code == 201
    assert response.json()["email"] == "new.user@example.com"
    assert "password" not in response.json()
    assert "password_hash" not in response.json()

    user = db_session.query(models.User).filter_by(email="new.user@example.com").one()
    assert user.password_hash != TEST_PASSWORD
    assert user.password_hash.startswith("$argon2id$")
    assert verify_password(TEST_PASSWORD, user.password_hash)


def test_duplicate_registration_is_rejected(
    unauthenticated_client: TestClient,
    registered_user: dict[str, object],
) -> None:
    response = unauthenticated_client.post(
        "/auth/register",
        json={"email": registered_user["email"], "password": TEST_PASSWORD},
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "An account with this email already exists"}


def test_valid_login_returns_signed_expiring_bearer_token(
    unauthenticated_client: TestClient,
    registered_user: dict[str, object],
) -> None:
    response = unauthenticated_client.post(
        "/auth/login",
        json={"email": registered_user["email"], "password": TEST_PASSWORD},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["expires_in"] == 1800
    assert set(body) == {"access_token", "token_type", "expires_in"}

    payload = jwt.decode(
        body["access_token"],
        TEST_SECRET,
        algorithms=["HS256"],
        issuer=TOKEN_ISSUER,
    )
    assert payload["sub"] == str(registered_user["id"])
    assert payload["token_type"] == "access"
    assert payload["exp"] > payload["iat"]


def test_invalid_password_and_unknown_user_share_the_same_error(
    unauthenticated_client: TestClient,
    registered_user: dict[str, object],
) -> None:
    invalid_password = unauthenticated_client.post(
        "/auth/login",
        json={"email": registered_user["email"], "password": "incorrect-password"},
    )
    unknown_user = unauthenticated_client.post(
        "/auth/login",
        json={"email": "unknown@example.com", "password": TEST_PASSWORD},
    )

    assert invalid_password.status_code == unknown_user.status_code == 401
    assert invalid_password.json() == unknown_user.json() == {"detail": "Invalid email or password"}


@pytest.mark.parametrize(
    "payload",
    [
        {"email": "not-an-email", "password": TEST_PASSWORD},
        {"email": "valid@example.com", "password": "short"},
        {"email": "valid@example.com"},
    ],
)
def test_registration_rejects_invalid_input(
    unauthenticated_client: TestClient,
    payload: dict[str, object],
) -> None:
    assert unauthenticated_client.post("/auth/register", json=payload).status_code == 422


def test_login_rejects_invalid_input(unauthenticated_client: TestClient) -> None:
    assert (
        unauthenticated_client.post(
            "/auth/login",
            json={"email": "invalid-email", "password": TEST_PASSWORD},
        ).status_code
        == 422
    )


def test_protected_routes_reject_a_missing_authorization_header(
    unauthenticated_client: TestClient,
) -> None:
    for path in ("/tasks", "/tasks/stats", "/tasks/1", "/tasks/1/comments"):
        response = unauthenticated_client.get(path)
        assert response.status_code == 401, f"{path}: {response.text}"
        assert response.headers["www-authenticate"] == "Bearer"


@pytest.mark.parametrize("authorization", ["Bearer not-a-jwt", "Basic dXNlcjpwYXNz"])
def test_protected_route_rejects_malformed_or_wrong_scheme_tokens(
    unauthenticated_client: TestClient,
    authorization: str,
) -> None:
    response = unauthenticated_client.get("/tasks", headers={"Authorization": authorization})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or missing authentication credentials"}


def test_protected_route_rejects_expired_token(
    unauthenticated_client: TestClient,
    registered_user: dict[str, object],
) -> None:
    now = datetime.now(UTC)
    token = jwt.encode(
        {
            "sub": str(registered_user["id"]),
            "iat": now - timedelta(minutes=2),
            "exp": now - timedelta(minutes=1),
            "iss": TOKEN_ISSUER,
            "token_type": "access",
        },
        TEST_SECRET,
        algorithm="HS256",
    )

    response = unauthenticated_client.get("/tasks", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401


def test_protected_route_rejects_invalid_signature_and_claims(
    unauthenticated_client: TestClient,
    registered_user: dict[str, object],
) -> None:
    now = datetime.now(UTC)
    claims: dict[str, Any] = {
        "sub": str(registered_user["id"]),
        "iat": now,
        "exp": now + timedelta(minutes=5),
        "iss": TOKEN_ISSUER,
        "token_type": "access",
    }
    bad_signature = jwt.encode(claims, "different-test-secret-with-at-least-32-bytes", algorithm="HS256")
    invalid_claim = jwt.encode(
        {key: value for key, value in claims.items() if key != "token_type"},
        TEST_SECRET,
        algorithm="HS256",
    )

    for token in (bad_signature, invalid_claim):
        response = unauthenticated_client.get("/tasks", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 401


def test_registered_login_token_allows_full_task_and_comment_lifecycle(
    registered_authenticated_client: TestClient,
) -> None:
    client = registered_authenticated_client
    created = client.post(
        "/tasks",
        json={
            "title": "Integration release task",
            "description": "searchable-marker",
            "priority": "high",
        },
    )
    assert created.status_code == 201
    task_id = created.json()["id"]

    fetched = client.get(f"/tasks/{task_id}")
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Integration release task"

    updated = client.patch(f"/tasks/{task_id}", json={"status": "in_progress"})
    assert updated.status_code == 200
    assert updated.json()["status"] == "in_progress"

    comment = client.post(f"/tasks/{task_id}/comments", json={"body": "integration comment"})
    assert comment.status_code == 201
    assert client.get(f"/tasks/{task_id}/comments").json()[0]["body"] == "integration comment"

    filtered = client.get("/tasks", params={"status": "in_progress", "q": "searchable-marker"})
    assert filtered.status_code == 200
    assert filtered.json()["total"] == 1
    assert filtered.json()["items"][0]["comment_count"] == 1

    statistics = client.get("/tasks/stats")
    assert statistics.status_code == 200
    assert statistics.json()["total"] == 1
    assert statistics.json()["total_comments"] == 1

    assert client.delete(f"/tasks/{task_id}").status_code == 204
    assert client.get(f"/tasks/{task_id}").status_code == 404


def test_openapi_declares_bearer_auth_for_protected_routes(
    unauthenticated_client: TestClient,
) -> None:
    response = unauthenticated_client.get("/openapi.json")

    assert response.status_code == 200
    schema = response.json()
    assert schema["components"]["securitySchemes"]["HTTPBearer"] == {
        "type": "http",
        "scheme": "bearer",
    }
    for path in ("/tasks", "/tasks/stats", "/tasks/{task_id}", "/tasks/{task_id}/comments"):
        for operation in schema["paths"][path].values():
            assert operation["security"] == [{"HTTPBearer": []}]
    for path, method in (("/auth/register", "post"), ("/auth/login", "post"), ("/health", "get")):
        assert schema["paths"][path][method].get("security", []) == []


def test_unique_user_completes_live_api_auth_and_task_workflow(
    unauthenticated_client: TestClient,
    db_session: Session,
) -> None:
    email = f"week5-e2e-{uuid4().hex}@example.com"
    password = f"Week5-E2E-{uuid4().hex}"
    registration = {"email": email, "password": password}

    invalid_payload = unauthenticated_client.post(
        "/auth/register",
        json={"email": "not-an-email", "password": password},
    )
    assert invalid_payload.status_code == 422

    invalid_credentials = unauthenticated_client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )
    assert invalid_credentials.status_code == 401

    unauthenticated = unauthenticated_client.post(
        "/tasks",
        json={"title": "Must be authenticated"},
    )
    assert unauthenticated.status_code == 401

    malformed = unauthenticated_client.get(
        "/tasks",
        headers={"Authorization": "Bearer not-a-jwt"},
    )
    assert malformed.status_code == 401

    created_user = unauthenticated_client.post("/auth/register", json=registration)
    assert created_user.status_code == 201
    user_data = created_user.json()
    assert user_data["email"] == email
    assert "password" not in user_data
    assert "password_hash" not in user_data

    user = db_session.query(models.User).filter_by(email=email).one()
    assert user.password_hash != password
    assert user.password_hash.startswith("$argon2id$")
    assert verify_password(password, user.password_hash)

    duplicate = unauthenticated_client.post("/auth/register", json=registration)
    assert duplicate.status_code == 409

    login = unauthenticated_client.post("/auth/login", json=registration)
    assert login.status_code == 200
    token_response = login.json()
    assert token_response["access_token"]
    assert token_response["token_type"] == "bearer"
    claims = jwt.decode(
        token_response["access_token"],
        get_auth_secret_key(),
        algorithms=["HS256"],
        issuer=TOKEN_ISSUER,
    )
    assert claims["sub"] == str(user_data["id"])
    assert claims["token_type"] == "access"

    unauthenticated_client.headers["Authorization"] = (
        f"Bearer {token_response['access_token']}"
    )
    task_response = unauthenticated_client.post(
        "/tasks",
        json={"title": "Unique authentication workflow", "description": email},
    )
    assert task_response.status_code == 201
    task_id = task_response.json()["id"]

    task_list = unauthenticated_client.get("/tasks")
    assert task_list.status_code == 200
    assert any(task["id"] == task_id for task in task_list.json()["items"])
    task_read = unauthenticated_client.get(f"/tasks/{task_id}")
    assert task_read.status_code == 200

    patched = unauthenticated_client.patch(
        f"/tasks/{task_id}",
        json={"status": "in_progress"},
    )
    assert patched.status_code == 200
    replaced = unauthenticated_client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Updated authentication workflow",
            "description": email,
            "status": "in_progress",
            "priority": "high",
        },
    )
    assert replaced.status_code == 200

    comment = unauthenticated_client.post(
        f"/tasks/{task_id}/comments",
        json={"body": "Authenticated end-to-end comment"},
    )
    assert comment.status_code == 201
    comments = unauthenticated_client.get(f"/tasks/{task_id}/comments")
    assert comments.status_code == 200
    assert comments.json()[0]["body"] == "Authenticated end-to-end comment"

    statistics = unauthenticated_client.get("/tasks/stats")
    assert statistics.status_code == 200
    assert statistics.json()["total"] == 1
    assert statistics.json()["total_comments"] == 1

    deleted = unauthenticated_client.delete(f"/tasks/{task_id}")
    assert deleted.status_code == 204
    assert unauthenticated_client.get(f"/tasks/{task_id}").status_code == 404
