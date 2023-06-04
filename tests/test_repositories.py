import decouple
from sqlalchemy.ext.asyncio import AsyncSession
from src.database_connection import connector
from src.repositoreis.questions import get_non_unique

a = decouple.config("mode")
settings = connector.get_settings(a)
n = settings
# settings = connector.get_settings(a)
engine = connector.engine_factory(settings)
connector.Session.configure(bind=engine)


# @pytest.mark.asyncio
async def test_run_test():
    ses: AsyncSession = await connector.get_session()
    res = await get_non_unique(ses, [12])
    assert res is not None

