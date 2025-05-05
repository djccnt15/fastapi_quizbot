import pytest
from httpx import AsyncClient
from sqlalchemy.orm.session import Session

from src.db.entity import QuizEntity


@pytest.mark.asyncio
async def test_get_quiz_list(client: AsyncClient):
    r = await client.get("/quiz")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


@pytest.mark.parametrize(
    "q, expected",
    [
        (None, 422),
        ("🇰🇷 대한민국의 수도는?", 201),
        ("🐬 MySQL 로고의 동물은 무엇인가요?", 201),
    ],
)
@pytest.mark.asyncio
async def test_create_quiz(client: AsyncClient, session: Session, q, expected):
    data = {
        "question": q,
        "content": "1️⃣ 서울\n2️⃣ 인천\n3️⃣ 부산\n4️⃣ 대구",
        "answer": 1,
    }

    r = await client.post("/quiz", json=data)
    row = session.query(QuizEntity).first()
    assert r.status_code == expected
    assert q == (row and row.question)


@pytest.mark.asyncio
async def test_get_random_quiz(client: AsyncClient, add_quiz):
    for _ in range(10):
        add_quiz()
    r = await client.get("/quiz/random")
    assert r.status_code == 200
    assert not isinstance(r.json(), list)
