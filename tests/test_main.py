from src.main import app
from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest

client = TestClient(app)


# @pytest.mark.anyio
# def test_request_for_questions():
#     response = client.post("/questions", json={"questions_num": 2},
#                            headers={"content-type": "application/json"})
#     assert response.status_code == 201
#

@pytest.mark.asyncio
async def test_request_for_questions1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/questions", json={"questions_num": 2})
        assert resp.status_code == 201

@pytest.mark.asyncio
async def test_request_for_questions_fail():
    ...