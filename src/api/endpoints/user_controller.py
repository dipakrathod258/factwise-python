from fastapi import APIRouter

from src.schemas.project_board import ProjectBoardRequestData
from src.schemas.user_schema import UserRequestData, UserDetailsRequestData, UserUpdateRequestData
from src.services.project_board import ProjectBoardBase
from src.services.user_base import UserBase

router = APIRouter()


@router.post("/create_user")
async def create_user(request_payload: UserRequestData):
    response = UserBase.create_user(request_payload)
    return response


@router.post("/list_users")
async def list_users():
    response = UserBase.list_users()
    return response


@router.post("/describe_user")
async def describe_user(request_payload: UserDetailsRequestData):
    response = UserBase.describe_user(request_payload)
    return response


@router.post("/update_user")
async def update_user(request_payload: UserUpdateRequestData):
    response = UserBase.update_user(request_payload)
    return response


@router.post("/get_user_teams")
async def get_user_teams(request_payload: ProjectBoardRequestData):
    response = UserBase.get_user_teams(request_payload)
    return response
