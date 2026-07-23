import jwt
from fastapi import HTTPException, status
from jwt import InvalidTokenError

from app.services import config_service, user_service
from app.utils.auth_utils import (
    create_access_token,
    hash_password,
    serialize_user,
    verify_password,
)


def register_user(*, full_name: str, email: str, password: str) -> dict:
    """Registers a new user and returns their auth token."""
    if user_service.get_user_by_email(email=email):
        raise ValueError("User already exists")

    user = user_service.create_user(
        full_name=full_name,
        email=email,
        hashed_password=hash_password(password),
    )
    token = create_access_token(user)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": serialize_user(user),
    }


def login_user(*, email: str, password: str) -> dict:
    """Authenticates a user and returns their auth token."""
    user = user_service.get_user_by_email(email=email)
    if not user or not verify_password(password, user.hashed_password):
        raise ValueError("Invalid email or password")

    token = create_access_token(user)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": serialize_user(user),
    }


def get_current_user(token: str) -> dict:
    """Decodes the JWT token and returns the current serialized user."""
    try:
        payload = jwt.decode(
            token, config_service.SECRET_KEY, algorithms=[config_service.ALGORITHM]
        )
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from exc

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    user = user_service.get_user_by_id(user_id=int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return serialize_user(user)
