import pytest
from pydantic import ValidationError
from src.serializers.serializers import QuestionIn


def test_qsin_ok():
    test = QuestionIn(
        QuestionId=234,
        Question="aaa",
        Answer="aaaaa",
        DateCreated="2022-12-30T19:14:12.401Z"
    )
    assert test.Answer == "aaaaa"
    assert test.Question == "aaa"
    assert test.QuestionId == 234


def test_qsin_fails():
    with pytest.raises(ValidationError) as err:
        test = QuestionIn(
            QuestionId="gggg",
            Question="aaa",
            Answer="aaaaa",
            DateCreated="2022-12-30T19:14:12.401Z"
        )


def test_qsin_fails_datecreated():
    with pytest.raises(ValueError) as err:
        test = QuestionIn(
            QuestionId=234,
            Question="aaa",
            Answer="aaaaa",
            DateCreated="EEEEZ"
        )


def test_gsin_from_dict_method_ok():
    sample = {
        "id": 222,
        "question": "blabla",
        "answer": "bla",
        "created_at": "2022-12-30T19:14:12.401Z"
    }
    test = QuestionIn.from_dict(sample)
    assert test.Answer == "bla"
    assert test.Question == "blabla"
    assert test.QuestionId == 222


def test_gsin_from_dict_method_fail_types():
    sample = {
        "id": "two",
        "question": "blabla",
        "answer": "bla",
        "created_at": "2022-12-30T19:14:12.401Z"
    }
    with pytest.raises(ValueError) as err:
        test = QuestionIn.from_dict(sample)


def test_gsin_from_dict_method_fail_date():
    sample = {
        "id": 222,
        "question": "blabla",
        "answer": "bla",
        "created_at": "14:12.401Z"
    }
    with pytest.raises(ValueError) as err:
        test = QuestionIn.from_dict(sample)