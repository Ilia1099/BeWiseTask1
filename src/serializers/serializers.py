import re
from datetime import datetime
from pydantic.dataclasses import dataclass
from pydantic import BaseModel, Field


@dataclass
class QuestionIn:
    """
    Pydantic dataclass for data serialization of a single question
    """
    QuestionId: int
    Question: str
    Answer: str
    DateCreated: str = Field(allow_mutation=True)

    @classmethod
    def from_dict(cls, question: dict):
        """
        class method for initialization instance of QuestionId
        :param question: a single dictionary of question data received from endpoint
        :return: instance of class
        """
        return cls(
            QuestionId=question.get('id'),
            Question=question.get('question'),
            Answer=question.get('answer'),
            DateCreated=question.get("created_at"),
        )

    def __post_init__(self):
        """
        magic method for validating data string and reformatting it
        """
        if not re.match(
                r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$",
                self.DateCreated):
            raise ValueError
        iso = datetime.fromisoformat(self.DateCreated.replace("Z", "+00:00"))
        self.DateCreated = iso.strftime("%Y-%m-%dT%H:%M:%S")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ReqParams(BaseModel):
    """
    simple pydantic class for received params for api call
    """
    count: int


class QuestionOut(BaseModel):
    """
    Pydantic dataclass for data serialization of a single question
    """
    question_id: int
    question_text: str
    answer_text: str
    original_creation_time: str = Field(allow_mutation=True)

    class Config:
        orm_mode = True
