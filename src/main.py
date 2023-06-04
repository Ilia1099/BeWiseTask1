import logging
from src.routes import common
import decouple
from fastapi import FastAPI
from src.database_connection import connector

settings = connector.get_settings(decouple.config("mode"))
engine = connector.engine_factory(settings)
connector.Session.configure(bind=engine)

logger = logging.getLogger(__name__)


app = FastAPI()


app.include_router(common.router)

