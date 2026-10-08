"""Account registration and login endpoints."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.security import authenticate_user, create_access_token, hash_password

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/register",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register an account",
)
def register(
    payload: schemas.UserCreate,
    db: Annotated[Session, Depends(get_db)],
) -> models.User:
    """Create an account while storing only its Argon2 password hash."""
    user = models.User(email=str(payload.email), password_hash=hash_password(payload.password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        ) from None
    db.refresh(user)
    return user


@router.post(
    "/login",
    response_model=schemas.TokenResponse,
    summary="Log in and receive an access token",
)
def login(
    payload: schemas.LoginRequest,
    db: Annotated[Session, Depends(get_db)],
) -> schemas.TokenResponse:
    """Verify credentials and issue a signed, expiring bearer token."""
    user = authenticate_user(db, str(payload.email), payload.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token, expires_in = create_access_token(user.id)
    return schemas.TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=expires_in,
    )


__all__ = ["router"]
