"""Authentication setup shared by local in-process API benchmark scripts."""

from __future__ import annotations

import os
import secrets
from typing import Any

from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app import models
from app.security import create_access_token, hash_password


def authenticate_test_client(
    client: TestClient,
    session_factory: sessionmaker[Any],
) -> None:
    """Seed a throw-away user and attach a signed token to the test client."""
    os.environ.setdefault("AUTH_SECRET_KEY", secrets.token_urlsafe(48))
    with session_factory() as db:
        user = models.User(
            email=f"benchmark-{secrets.token_hex(8)}@example.com",
            password_hash=hash_password(secrets.token_urlsafe(32)),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        token, _ = create_access_token(user.id)

    client.headers["Authorization"] = f"Bearer {token}"


__all__ = ["authenticate_test_client"]
