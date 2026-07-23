from typing import Optional

from sqlmodel import select

from app.models.user import User
from app.services import database_service


def create_user(*, full_name: str, email: str, hashed_password: str) -> User:
    """Creates a new user in the database."""
    with database_service.get_session() as session:
        user = User(full_name=full_name, email=email, hashed_password=hashed_password)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def get_user_by_email(*, email: str) -> Optional[User]:
    """Retrieves a user by their email address."""
    with database_service.get_session() as session:
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()


def get_user_by_id(*, user_id: int) -> Optional[User]:
    """Retrieves a user by their unique ID."""
    with database_service.get_session() as session:
        return session.get(User, user_id)
