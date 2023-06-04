from typing import Annotated

from aiohttp import ClientSession
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.services.services import get_questions, get_prev_added_question
from src.web_connetion import session_maker as sm

from src.database_connection import connector
from src.repositoreis.questions import get_last_added
from src.serializers.serializers import QuestionOut, ReqParams

router = APIRouter()


class ServiceError(BaseException):
    pass


@router.get("/")
async def root(db_ses: Annotated[AsyncSession,Depends(connector.get_session)]):
    qa = await get_prev_added_question(db_ses)
    print(type(qa))
    return qa


@router.post("/questions", status_code=status.HTTP_201_CREATED)
async def request_for_questions(
        params: ReqParams,
        db_ses: Annotated[AsyncSession, Depends(connector.get_session)],
        w_ses: Annotated[ClientSession, Depends(sm.get_aiohttp_session)]):
    # prev_question = None
    try:
        prev_question = await get_prev_added_question(db_ses)
        await get_questions(web_ses=w_ses, db_ses=db_ses,
                            url="https://jservice.io/api/random",
                            query_param=params.dict())
        await db_ses.commit()
    except IntegrityError as e:
        raise ServiceError("already exists")
    return prev_question
