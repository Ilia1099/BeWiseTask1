from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from src.serializers.serializers import QuestionIn
from src.models import CollectedQuestions
from sqlalchemy import select, desc, Row
from sqlalchemy.orm import aliased


async def add_question(db_ses: AsyncSession, question: QuestionIn):
    """
    function which initializes new instance of CollectedQuestions model
    :param db_ses: database session instance
    :param question: a serializer dataclass
    """
    new_question = CollectedQuestions(
        question_id=question.QuestionId,
        question_text=question.Question,
        answer_text=question.Answer,
        original_creation_time=question.DateCreated,
    )
    db_ses.add(new_question)


async def get_non_unique(
        db_ses: AsyncSession,
        ids_to_check: List[int]) -> set[int]:
    """
    function which makes a query call to database to check for existence of
    specified questions by their ids
    :param db_ses: da session object
    :param ids_to_check: list of ids
    :return: set[int]
    """
    query = select(CollectedQuestions.question_id).where(
        CollectedQuestions.question_id.in_(ids_to_check))
    result = await db_ses.execute(query)
    return set(result.scalars().fetchall())


async def get_last_added(db_ses: AsyncSession) -> Row:
    """
    function which makes a query to a database to get last added question
    :param db_ses: db session object
    :return: Row object
    """
    qs = aliased(CollectedQuestions, name="qs")
    query = select(qs).order_by(desc(qs.id)).limit(1)
    result = await db_ses.execute(query)
    return result.one_or_none()
