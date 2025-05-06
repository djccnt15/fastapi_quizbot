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


@pytest.fixture(autouse=True)
async def mock_telegram(monkeypatch: pytest.MonkeyPatch):
    from src.core.telegram import Telegram

    async def mock_get_bot_info(*args, **kwargs): ...

    async def mock_get_webhook(*args, **kwargs):
        return {
            "ok": True,
            "result": {
                "has_custom_certificate": False,
                "ip_address": "127.0.0.1",
                "last_error_date": 1622887352,
                "last_error_message": "Wrong response from the webhook: 500 Internal Server Error",
                "max_connections": 40,
                "pending_update_count": 0,
                "url": "https://localhost/v1/webhook/sometoken",
            },
        }

    async def mock_set_webhook(*args, **kwargs):
        return {"ok": True, "result": True, "description": "Webhook is already set"}

    async def mock_send_message(*args, **kwargs):
        return {
            "message_id": 1234,
            "from": {
                "id": 123,
                "is_bot": False,
                "first_name": "first",
                "last_name": "last",
                "username": "username",
                "language_code": "ko",
            },
            "chat": {
                "id": 123,
                "type": "private",
                "first_name": "first",
                "last_name": "last",
                "username": "username",
            },
            "datetime": 1622902229,
            "text": "some text",
        }

    monkeypatch.setattr(Telegram, "get_bot_info", mock_get_bot_info)
    monkeypatch.setattr(Telegram, "get_webhook", mock_get_webhook)
    monkeypatch.setattr(Telegram, "set_webhook", mock_set_webhook)
    monkeypatch.setattr(Telegram, "send_message", mock_send_message)
