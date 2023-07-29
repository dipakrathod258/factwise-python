from fastapi import HTTPException

from datetime import date
from pydantic import BaseModel, validator, Field
from datetime import datetime


class ProjectBoardRequestData(BaseModel):
    name: str = Field(
        title="The name of the project board", max_length=128
    )
    description: str | None = Field(
        default=None, title="The description of the project board", max_length=128
    )
    team_id: int

    class Config:
        validate_assignment = True

    @validator('name')
    def set_name(cls, name):
        return name.strip()


class TaskCreateRequestData(BaseModel):
    title: str = Field(
        title="The title of the taks", max_length=128
    )
    description: str | None = Field(
        default=None, title="The description of the task", max_length=128
    )
    user_id: int
    project_board_id: int

    class Config:
        validate_assignment = True

    @validator('title')
    def set_name(cls, title):
        return title.strip()



class TaskUpdateRequestData(BaseModel):
    task_id: int
    status: str

    class Config:
        validate_assignment = True

    @validator('status', pre=True, always=True)
    def validate_to_email_count(cls, status):
        print(f"status: {status}")
        if status not in ["Open", "Closed", "In Progress"]:
            raise HTTPException(status_code=400, detail="Payload contains invalid status")
        return status


class TaskListRequestData(BaseModel):
    task_id: int


class ExportProjectBoardRequestData(BaseModel):
    project_board_id: int
