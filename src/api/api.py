from fastapi import APIRouter
from src.api.endpoints import project_board_controller, user_controller, team_controller

api_router = APIRouter()

api_router.include_router(project_board_controller.router, prefix="/project_board", tags=["Project-Boards"])
api_router.include_router(user_controller.router, prefix="/user", tags=["Users"])
api_router.include_router(team_controller.router, prefix="/team", tags=["Teams"])
