import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health(default_client: AsyncClient):
    r = await default_client.get("/health")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_index(default_client: AsyncClient):
    r = await default_client.get("/")
    assert r.status_code == 307
