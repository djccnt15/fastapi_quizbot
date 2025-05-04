import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.orm.session import Session

from src import main
from src.configuration.config import settings
from src.configuration.database import engine, get_db
from src.db import entity


@pytest.fixture(scope="session")
def app() -> FastAPI:
    if not settings.TESTING:
        raise SystemError("TESTING environment must be set true")
    return main.app


@pytest.fixture
async def session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
async def default_client(app: FastAPI):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.fixture
async def client(app: FastAPI):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test/api/v1",
    ) as ac:
        entity.Base.metadata.drop_all(bind=engine)
        entity.Base.metadata.create_all(bind=engine)
        yield ac


@pytest.fixture
def user(session: Session) -> entity.UserEntity:
    row = entity.UserEntity(id=123, username="test", first_name="te", last_name="st")
    session.add(row)
    session.commit()

    return row


@pytest.fixture
def add_quiz(session: Session):
    def func(
        question: str | None = None,
        content: str | None = None,
        answer: int | None = None,
    ) -> entity.QuizEntity:
        r = entity.QuizEntity(
            question=question or "qqq",
            content=content or "text",
            answer=answer or 1,
        )
        session.add(r)
        session.commit()
        return r

    return func
