import os
from fastapi import FastAPI
from src.log_conf import Logger

LOGGER = Logger.get_logger(__name__)

environment = os.environ.get('ENVIRONMENT')


def create_app() -> FastAPI:
    try:
        LOGGER.info("Initialize analytics app")
        app = FastAPI()

        LOGGER.info("Initialize application configurations ...")
        return app
    except Exception as e:
        LOGGER.error(f"Error in analytics app initialisation => {e}")
