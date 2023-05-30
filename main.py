import logging
from contextlib import asynccontextmanager
from typing import Annotated, Type
import decouple
from aiohttp import ClientSession
from fastapi import FastAPI, status, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from repositoreis.questions import add_question, get_non_unique
from database_connection import connector
from serializers.serializers import QuestionIn, ReqParams
from services.services import get_questions

settings = connector.get_settings(decouple.config("mode"))
engine = connector.engine_factory(settings)
connector.Session.configure(bind=engine)

logger = logging.getLogger(__name__)

app = FastAPI()


class ServiceError(BaseException):
    pass


@app.get('/db')
async def run_select(
        db_ses: Annotated[AsyncSession, Depends(connector.get_session)],
        # web_ses:
):
    # qs = QuestionIn(
    #     QuestionId = 12,
    #     Question = "str",
    #     Answer = "str",
    #     DateCreated = "2022-12-30T19:14:12.401Z"
    # )
    async with ClientSession() as ses:
        q = await get_questions(
            web_ses=ses,
            db_ses=db_ses,
            url="https://jservice.io/api/random",
            query_param={"count": 3})
        try:
            await db_ses.commit()
        except IntegrityError as e:
            print(e)
            raise ServiceError("already exists")
        # res = await get_non_unique(session, [12, 123])
        # print(res)
        return {"status": "201"}


@app.get("/")
async def root():
    # await asyncio.sleep(5)
    return


@app.post("/questions", status_code=status.HTTP_201_CREATED)
async def request_for_questions(params: ReqParams):
    print(params.count)
    return {"message": "Created"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# @asynccontextmanager
# async def web_session() -> Type[ClientSession]:
#     async with ClientSession() as ses:
#         logger.info("ClientSession opened")
#         yield ses
#     logger.info("ClientSession closed")


@asynccontextmanager
async def db_connection(app: FastAPI):
    await engine.connect()
    logger.info("Db connection established")
    yield
    await engine.dispose()
    logger.info("Db connection closed")
