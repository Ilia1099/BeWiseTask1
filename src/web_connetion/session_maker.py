import aiohttp


async def get_aiohttp_session():
    async with aiohttp.ClientSession() as ses:
        yield ses
