from typing import List
from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositoreis.questions import add_question
from src.repositoreis.questions import get_non_unique
from src.serializers.serializers import QuestionIn, QuestionOut
from src.web_connetion.request_sender import make_request
from src.repositoreis.questions import get_last_added
from src.repositoreis.echo import HelloWorldResponse


async def plug_holder():
    return HelloWorldResponse()


async def get_questions(web_ses: ClientSession, db_ses: AsyncSession,
                        url: str, query_param: dict):
    """
    function which combines outer api call, runs check if received questions
    are unique, makes additional calls if some are not; saves questions
    :param web_ses: aiohttp session instance
    :param db_ses: ClientSession instance
    :param url: provided url for requesting
    :param query_param: query params for endpoint
    """
    data, response = await make_request(
        ses=web_ses, url=url, payload=query_param)
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


async def filter_unique(db_ses: AsyncSession, questions: List[dict]) -> List[dict]:
    """
    function which creates list of ids from received questions;
    calls get_non_unique() function
    :param db_ses: db session object
    :param questions: received json
    :return: filtered list of received data
    """
    ids_to_check = [qs["id"] for qs in questions]
    result = await get_non_unique(db_ses, ids_to_check)
    questions = [qs for qs in questions if qs.get("id") not in result]
    return questions


async def get_prev_added_question(db_ses: AsyncSession) -> QuestionOut:
    """
    function which calls get_last_added, checks response type;
    if return result is Row object, extracts model object from it,
    uses it to create corresponding Pydantinc class and returns it;
    otherwise returns None
    :param db_ses: dd session object
    """
    row = await get_last_added(db_ses=db_ses)
    if row:
        return QuestionOut.from_orm(row.qs)
    return row
