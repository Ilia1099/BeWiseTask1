from typing import Annotated
from aiohttp import ClientSession
from asyncpg import InvalidCatalogNameError
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
import logging
from src.services.services import get_questions, get_prev_added_question, \
    plug_holder
from src.web_connetion import session_maker as sm
from src.database_connection import connector
from src.serializers.serializers import ReqParams


logger = logging.getLogger(__name__)
router = APIRouter()


class ServiceError(BaseException):
    pass


@router.get("/")
async def root():
    return await plug_holder()


@router.post("/questions", status_code=status.HTTP_201_CREATED)
async def request_for_questions(
        params: ReqParams,
        db_ses: Annotated[AsyncSession, Depends(connector.get_session)],
        w_ses: Annotated[ClientSession, Depends(sm.get_aiohttp_session)]):
    try:
        prev_question = await get_prev_added_question(db_ses)
        await get_questions(web_ses=w_ses, db_ses=db_ses,
                            url="https://jservice.io/api/random",
                            query_param=params.dict())
        await db_ses.commit()
    except InvalidCatalogNameError as e:
        logger.error(e)
        raise ServiceError("Check database")
    return prev_question
