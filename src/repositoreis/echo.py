from pydantic import BaseModel


class HelloWorldResponse(BaseModel):
    echo: str = "Hello!\n" \
                "To get new questions you have to make a post request by " \
                "following path:\n" \
                "\\questions" \
                "The Body must contain following key: value pair:\n" \
                "count: {int}\""
