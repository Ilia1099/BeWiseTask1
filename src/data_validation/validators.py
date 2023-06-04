from asyncio import Future
from typing import List
from pydantic import validate_arguments


@validate_arguments
async def validate_response(response_data) -> List[dict]:
    return response_data
