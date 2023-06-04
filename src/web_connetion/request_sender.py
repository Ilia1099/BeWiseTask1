from fastapi import HTTPException
from aiohttp import ClientSession


async def make_request(ses: ClientSession, url: str, payload: dict):
    """
    Function to make get request, if specified resource doesn't exist, raises
    HTTPException
    :param ses: Session instance
    :param url: full url, containing endpoint
    :param payload: query params
    :return: List[dict], ClientSession response instance
    """
    async with ses.get(url=url, data=payload) as resp:
        if resp.status != 200:
            raise HTTPException(
                status_code=resp.status,
                detail=resp.reason)
        data = await resp.json()
        return data, resp

