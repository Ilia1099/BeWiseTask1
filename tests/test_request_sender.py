import aiohttp
import pytest
from fastapi import HTTPException

from src.web_connetion.request_sender import make_request


class MockResponse:
    def __init__(self, status, json):
        self.status = status
        self._json = json

    async def json(self):
        return self._json

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


url = "https://jservice.io/api/random"
payload = {"count": "3"}


@pytest.fixture
def mock_resp_not_ok(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse(status=404, json={"ses": "ssss"})

    monkeypatch.setattr(aiohttp.ClientSession, "get", mock_get)


@pytest.fixture
def mock_resp_ok(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse(status=200, json={"ses": "ssss"})

    monkeypatch.setattr(aiohttp.ClientSession, "get", mock_get)


@pytest.mark.asyncio
async def test_make_request_raises404(mock_resp_not_ok):
    with pytest.raises(HTTPException) as e:
        async with aiohttp.ClientSession() as session:
            res, f = await make_request(session, url, payload)
    assert e.value.status_code == 400
    assert e.value.detail == "Not Found"


@pytest.mark.asyncio
async def test_make_request_raises404(mock_resp_ok):
    async with aiohttp.ClientSession() as session:
        data, response = await make_request(session, url, payload)
    assert data == {"ses": "ssss"}
    assert response.status == 200

