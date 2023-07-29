from fastapi import HTTPException

from datetime import date
from pydantic import BaseModel, validator, Field
from datetime import datetime


class UserRequestData(BaseModel):
    name: str = Field(
        title="Name of the user", max_length=64, unique=True
    )
    display_name: str = Field(title="Display of the user", max_length=64)
    description: str | None = Field(
        default=None, title="The description of the user", max_length=128
    )

    class Config:
        validate_assignment = True

    @validator('name')
    def set_name(cls, name):
        return name.strip()


class UserDetailsRequestData(BaseModel):
    id: int


class UserUpdateRequestData(BaseModel):
    id: int
    user: UserRequestData
