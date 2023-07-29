import click
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.api import api_router
from src.core import server
from src.core.server import create_app
from src.log_conf import Logger

LOGGER = Logger.get_logger(__name__)

@click.group("Fast-api App manager")
def manage() -> None:
    # the main group of commands
    pass


@manage.command(help="Run the web server")
def run_server() -> None:
    click.echo("-> Runnning the server")
    run()


@manage.group(help="Manage the database")
def database() -> None:
    # group to manage data base
    pass


app: FastAPI = create_app()
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def _startup() -> None:
    LOGGER.info("Initialize CORS configurations ...")

    app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def run() -> None:
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=8082,
        log_level="debug"
    )


if __name__ == "__main__":
    manage()
