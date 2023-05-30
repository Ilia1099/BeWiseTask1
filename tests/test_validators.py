import pytest
from pydantic import ValidationError
from data_validation.validators import validate_response


@pytest.mark.asyncio
async def test_response_data_validator_ok():
    smp = [{"test": "test"}]
    try:
        res = validate_response(smp)
    except ValidationError as err:
        print(err)


@pytest.mark.asyncio
async def test_response_data_validator_flawed_resp():
    smp = "a"
    try:
        res = await validate_response(smp)
    except ValidationError as err:
        print(err)
