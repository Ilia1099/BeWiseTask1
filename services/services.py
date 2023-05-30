import asyncio
from types import coroutine
from typing import List, Type
from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession
from repositoreis.questions import add_question
from data_validation.validators import validate_response
from repositoreis.questions import get_non_unique
from serializers.serializers import QuestionIn
from web_connetion.request_sender import make_request


async def get_questions(
        web_ses: ClientSession,
        db_ses: AsyncSession,
        url: str,
        query_param: dict):
    """

    :param web_ses:
    :param db_ses:
    :param url:
    :param query_param:
    :return:
    """
    data, response = await make_request(
        ses=web_ses, url=url, payload=query_param
    )
    data = await filter_unique(db_ses, data)
    while True:
        if len(data) == query_param.get("count"):
            break
        query_param["count"] = query_param.get("count") - len(data)
        body, resp = await make_request(
            ses=web_ses, url=url, payload=query_param)
        data.extend(await filter_unique(db_ses, body))
    for qs in data:
        await add_question(db_ses, QuestionIn.from_dict(qs))


async def filter_unique(db_ses: AsyncSession, questions: List[dict]):
    """
    function which creates list of ids from received questions;
    call get_non_unique() function
    :param db_ses: db session object
    :param questions: received json
    :return: filtered list of received data
    """
    ids_to_check = [qs["id"] for qs in questions]
    result = await get_non_unique(db_ses, ids_to_check)
    questions = [qs for qs in questions if qs.get("id") not in result]
    return questions


