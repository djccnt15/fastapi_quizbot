import pytest
from httpx import AsyncClient

from src.configuration.config import settings

data = {
    "update_id": 1234,
    "message": {
        "message_id": 123,
        "from": {
            "id": 12345,
            "is_bot": False,
            "first_name": "QWER",
            "last_name": "ASDF",
            "username": "1q2w3e4r",
            "language_code": "ko",
        },
        "chat": {
            "id": 123,
            "first_name": "QWER",
            "last_name": "ASDF",
            "username": "1q2w3e4r",
            "type": "private",
        },
        "date": 1622902229,
        "text": None,
    },
}
text_from_user = [("문제 내줘"), ("퀴즈퀴즈"), ("1"), ("123")]


@pytest.mark.asyncio
async def test_get_webhook(client: AsyncClient):
    r = await client.get("/bot/wb")
    data = r.json()
    assert r.status_code == 200
    assert data.get("ok")


@pytest.mark.asyncio
async def test_set_webhook(client):
    r = await client.post("/bot/wb", json={"url": "https://example.com"})
    data = r.json()
    assert r.status_code == 200
    assert data.get("ok")


@pytest.mark.parametrize("text", text_from_user)
@pytest.mark.asyncio
async def test_webhook(client: AsyncClient, add_quiz, text):
    for _ in range(10):
        add_quiz()
    data["message"]["text"] = text
    r = await client.post(
        f"/bot/{settings.TELEGRAM_BOT_TOKEN.get_secret_value()}",
        json=data,
    )
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_webhook_with_right_answer(client: AsyncClient, add_quiz):
    quiz = add_quiz()
    data["message"]["text"] = "문제내줘"
    r = await client.post(
        f"/bot/{settings.TELEGRAM_BOT_TOKEN.get_secret_value()}",
        json=data,
    )
    data["message"]["text"] = str(quiz.id)
    r2 = await client.post(
        f"/bot/{settings.TELEGRAM_BOT_TOKEN.get_secret_value()}",
        json=data,
    )
    assert r.status_code == 200
    assert r2.status_code == 200


@pytest.mark.asyncio
async def test_webhook_with_wrong_answer(client: AsyncClient, add_quiz):
    quiz = add_quiz()
    data["message"]["text"] = "퀴즈!"
    r = await client.post(
        f"/bot/{settings.TELEGRAM_BOT_TOKEN.get_secret_value()}",
        json=data,
    )
    data["message"]["text"] = str(quiz.id + 1)
    r2 = await client.post(
        f"/bot/{settings.TELEGRAM_BOT_TOKEN.get_secret_value()}",
        json=data,
    )
    assert r.status_code == 200
    assert r2.status_code == 200


@pytest.mark.parametrize("text", text_from_user)
@pytest.mark.asyncio
async def test_webhook_with_empty_quiz(client: AsyncClient, text):
    data["message"]["text"] = text
    r = await client.post(
        f"/bot/{settings.TELEGRAM_BOT_TOKEN.get_secret_value()}",
        json=data,
    )
    assert r.status_code == 200
