import re
from datetime import datetime
from pydantic.dataclasses import dataclass
from pydantic import BaseModel, Field


class Serializer(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


@dataclass
class QuestionIn:
    QuestionId: int
    Question: str
    Answer: str
    DateCreated: str = Field(allow_mutation=True)

    @classmethod
    def from_dict(cls, question: dict):
        return cls(
            QuestionId = question.get('id'),
            Question=question.get('question'),
            Answer=question.get('answer'),
            DateCreated=question.get("created_at"),
        )

    def __post_init__(self):
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
    count: int
