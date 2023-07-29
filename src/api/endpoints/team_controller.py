from fastapi import APIRouter

from src.services.team_base import TeamBase
from src.schemas.team_schema import TeamRequestData, TeamDetailsRequestData, TeamUpdateRequestData, UsersTeamsRequestData, TeamDetailsRequestData

router = APIRouter()


@router.post("/create_team")
async def create_team(request_payload: TeamRequestData):
    response = TeamBase.create_team(request_payload)
    return response


@router.post("/list_teams")
async def list_teams():
    response = TeamBase.list_teams()
    return response


@router.post("/describe_team")
async def describe_team(request_payload: TeamDetailsRequestData):
    response = TeamBase.describe_team(request_payload)
    return response


@router.post("/update_team")
async def update_team(request_payload: TeamUpdateRequestData):
    response = TeamBase.update_team(request_payload)
    return response


@router.post("/add_users_to_team")
async def add_users_to_team(request_payload: UsersTeamsRequestData):
    response = TeamBase.add_users_to_team(request_payload)
    return response


@router.post("/remove_users_from_team")
async def remove_users_from_team(request_payload: UsersTeamsRequestData):
    response = TeamBase.remove_users_from_team(request_payload)
    return response


@router.post("/list_team_users")
async def list_team_users(request_payload: TeamDetailsRequestData):
    response = TeamBase.list_team_users(request_payload)
    return response

