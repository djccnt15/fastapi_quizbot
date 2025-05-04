import pytest
from httpx import AsyncClient

from src.db.entity import UserEntity


@pytest.mark.asyncio
async def test_get_empty_user(client: AsyncClient):
    r = await client.get("/user")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, user: UserEntity):
    r = await client.get("/user")
    data = r.json()
    assert r.status_code == 200
    assert isinstance(data, list)
    assert data[0].get("username") == user.username
