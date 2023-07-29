from src.core import manage
import click
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.api import api_router
from src.core import server
from src.core.server import create_app
from src.log_conf import Logger

app: FastAPI = create_app()
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    manage.run_server()
