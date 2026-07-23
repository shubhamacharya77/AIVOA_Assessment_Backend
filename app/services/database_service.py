from sqlmodel import Session, SQLModel, create_engine

from app.services import config_service

engine = create_engine(config_service.DATABASE_URL, echo=False)


def init_db() -> None:
    """Initializes the database schema by creating all tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """Creates and yields a new database session."""
    return Session(engine)
