import datetime
from sqlalchemy import String, MetaData, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


class Base(AsyncAttrs, DeclarativeBase):
    """
    base class for model mapping
    """
    metadata = metadata


class CollectedQuestions(Base):
    """
    model representing 'collected_questions' table in database
    """
    __tablename__ = "collected_questions"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True
    )
    question_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    question_text: Mapped[str] = mapped_column(String(900), nullable=False)
    answer_text: Mapped[str] = mapped_column(String(300), nullable=False)
    original_creation_time: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    time_added_to_db: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.datetime.now()
    )
