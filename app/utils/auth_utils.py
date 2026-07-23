from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.models.user import User
from app.services import config_service

password_hash = PasswordHash.recommended()


def serialize_user(user: User) -> dict:
    return {"id": user.id, "full_name": user.full_name, "email": user.email}


def create_access_token(user: User) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=config_service.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"sub": str(user.id), "exp": expire}
    return jwt.encode(
        payload, config_service.SECRET_KEY, algorithm=config_service.ALGORITHM
    )


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)
