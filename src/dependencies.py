from sqlmodel import create_engine, Session, SQLModel, select  # noqa: F401
from fastapi import Depends
from typing import Generator
from .config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def get_db():
    db = get_session()
    try:
        yield next(db)
    finally:
        db.close()


SessionDep = Depends(get_db)
