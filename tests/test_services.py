import aiohttp
import pytest
from aiohttp import ClientSession

from src.web_connetion.request_sender import make_request
# from services.services import get_payload
from .test_request_sender import MockResponse


url = "https://jservice.io/api/random"
payload = {"count": "3"}


@pytest.fixture
def mock_resp(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse(status=200, json=[{"ses": "ssss"}, ])

    monkeypatch.setattr(aiohttp.ClientSession, "get", mock_get)


@pytest.mark.asyncio
async def test_get_payload(mock_resp):
    async with ClientSession() as session:
        data, response = await make_request(session, url, payload)
        # data = await get_payload(data)
        print()
        for dt in data:
            print(dt)

