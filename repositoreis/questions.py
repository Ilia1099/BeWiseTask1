from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from serializers.serializers import QuestionIn
from models import CollectedQuestions
from sqlalchemy import select


async def add_question(db_ses: AsyncSession, question: QuestionIn):
    new_question = CollectedQuestions(
        question_id=question.QuestionId,
        question_text=question.Question,
        answer_text=question.Answer,
        original_creation_time=question.DateCreated,
    )
    db_ses.add(new_question)
    return new_question


async def get_non_unique(
        db_ses: AsyncSession,
        ids_to_check: List[int]):
    """
    function which makes a query call to database to check for existence of
    specified questions by their ids
    :param db_ses: da session object
    :param ids_to_check: list of ids
    :return:
    """
    query = select(CollectedQuestions.question_id).where(
        CollectedQuestions.question_id.in_(ids_to_check))
    result = await db_ses.execute(query)
    return set(result.scalars().fetchall())
