"""Password hashing, access tokens, and authenticated-user resolution."""

from __future__ import annotations

import os
from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from functools import lru_cache
from typing import Annotated

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app import models
from app.database import get_db

TOKEN_ISSUER = "yuva-intern-week5"
EXAMPLE_SECRET_KEY = "replace-with-a-random-secret-of-at-least-32-characters"
_password_hasher = PasswordHasher()
_bearer = HTTPBearer(auto_error=False)


def get_auth_secret_key() -> str:
    """Return the configured signing key or fail clearly when it is unsafe."""
    secret = os.getenv("AUTH_SECRET_KEY", "")
    if secret == EXAMPLE_SECRET_KEY or len(secret.encode("utf-8")) < 32:
        raise RuntimeError("AUTH_SECRET_KEY must contain at least 32 bytes")
    return secret


def get_access_token_expire_minutes() -> int:
    """Read and validate the configured access-token lifetime."""
    value = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    try:
        minutes = int(value)
    except ValueError as exc:
        raise RuntimeError("ACCESS_TOKEN_EXPIRE_MINUTES must be an integer") from exc
    if not 1 <= minutes <= 1440:
        raise RuntimeError("ACCESS_TOKEN_EXPIRE_MINUTES must be between 1 and 1440")
    return minutes


def validate_auth_config() -> None:
    """Fail application startup when authentication is not safely configured."""
    get_auth_secret_key()
    get_access_token_expire_minutes()


def hash_password(password: str) -> str:
    """Hash a password with Argon2id using the library's secure defaults."""
    return _password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password without exposing password-hasher exceptions."""
    try:
        return _password_hasher.verify(password_hash, password)
    except (VerifyMismatchError, VerificationError):
        return False


@lru_cache(maxsize=1)
def _dummy_password_hash() -> str:
    return hash_password("invalid-user-password-check")


def create_access_token(
    user_id: int,
    expires_delta: timedelta | None = None,
) -> tuple[str, int]:
    """Create a signed JWT and return it with its lifetime in seconds."""
    lifetime = expires_delta or timedelta(minutes=get_access_token_expire_minutes())
    if lifetime.total_seconds() <= 0:
        raise ValueError("Access-token lifetime must be positive")

    now = datetime.now(UTC)
    expires_at = now + lifetime
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": expires_at,
        "iss": TOKEN_ISSUER,
        "token_type": "access",
    }
    return jwt.encode(payload, get_auth_secret_key(), algorithm="HS256"), int(lifetime.total_seconds())


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    db: Annotated[Session, Depends(get_db)],
) -> models.User:
    """Validate the bearer token and resolve its subject to an existing user."""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise _unauthorized()

    try:
        payload: Mapping[str, object] = jwt.decode(
            credentials.credentials,
            get_auth_secret_key(),
            algorithms=["HS256"],
            issuer=TOKEN_ISSUER,
            options={"require": ["sub", "iat", "exp", "iss", "token_type"]},
        )
    except (jwt.InvalidTokenError, RuntimeError):
        raise _unauthorized() from None

    subject = payload.get("sub")
    if (
        not isinstance(subject, str)
        or not subject.isdecimal()
        or payload.get("token_type") != "access"
    ):
        raise _unauthorized()

    try:
        user_id = int(subject)
    except ValueError:
        raise _unauthorized() from None
    user = db.get(models.User, user_id)
    if user is None:
        raise _unauthorized()
    return user


def authenticate_user(db: Session, email: str, password: str) -> models.User | None:
    """Authenticate a user, using the same error outcome for unknown emails."""
    user = db.query(models.User).filter(models.User.email == email).one_or_none()
    if user is None:
        verify_password(password, _dummy_password_hash())
        return None
    return user if verify_password(password, user.password_hash) else None


__all__ = [
    "authenticate_user",
    "create_access_token",
    "get_access_token_expire_minutes",
    "get_auth_secret_key",
    "get_current_user",
    "hash_password",
    "validate_auth_config",
    "verify_password",
]
