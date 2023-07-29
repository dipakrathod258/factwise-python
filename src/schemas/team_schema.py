from fastapi import HTTPException

from datetime import date
from pydantic import BaseModel, validator, Field
from datetime import datetime


class TeamRequestData(BaseModel):
    name: str = Field(
        title="Name of the user", max_length=64, unique=True
    )
    description: str | None = Field(
        default=None, title="The description of the user", max_length=128
    )
    admin: int
    class Config:
        validate_assignment = True

    @validator('name')
    def set_name(cls, name):
        return name.strip()


class TeamDetailsRequestData(BaseModel):
    id: int


class TeamUpdateRequestData(BaseModel):
    id: int
    team: TeamRequestData


class UsersTeamsRequestData(BaseModel):
    team_id: int
    users: list[int]
