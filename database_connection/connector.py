import uuid
import logging
from typing import Type

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from asyncpg import Connection
from database_connection.test_settings import ConfigTest
from database_connection.dep_settings import ConfigDep


logger = logging.getLogger(__name__)


# fix asyncpg.exceptions.InvalidSQLStatementNameError: prepared statement "__asyncpg_stmt_4c" does not exist
# discussion https://github.com/sqlalchemy/sqlalchemy/issues/6467#issuecomment-1187494311
class SQLAlchemyConnection(Connection):
    def _get_unique_id(self, prefix: str) -> str:
        return f'__asyncpg_{prefix}_{uuid.uuid4()}__'


def engine_factory(settings: Type[ConfigTest] | Type[ConfigDep]):
    return create_async_engine(
        url=settings().db_dsn(),
        echo=True,
        connect_args={
            'statement_cache_size': 0,  # required by asyncpg
            'prepared_statement_cache_size': 0,  # required by asyncpg
            'connection_class': SQLAlchemyConnection,
        },
        pool_pre_ping=True,
    )


Session = async_sessionmaker(expire_on_commit=False)


async def get_session():
    async with Session() as session:
        logger.info('Session started')
        yield session
    logger.info('Session closed')


def get_settings(mode: str):
    match mode:
        case "test":
            return ConfigTest
        case "dep":
            return ConfigDep
