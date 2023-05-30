import asyncio

import decouple
import models
from database_connection.connector import get_settings, engine_factory


async def create():
    settings = get_settings(decouple.config("mode"))
    engine = engine_factory(settings)
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)

    await engine.dispose()


if __name__ == '__main__':
    asyncio.run(create())
