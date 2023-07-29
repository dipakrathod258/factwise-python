from fastapi import APIRouter

from src.schemas.project_board import ProjectBoardRequestData, TaskCreateRequestData, TaskUpdateRequestData, TaskListRequestData, ExportProjectBoardRequestData
from src.services.project_board import ProjectBoardBase

router = APIRouter()


@router.post("/create_board")
async def create_board(request_payload: ProjectBoardRequestData):
    response = ProjectBoardBase.create_board(request_payload)
    return response


@router.post("/close_board")
async def close_board(request_payload: ProjectBoardRequestData):
    response = ProjectBoardBase.close_board(request_payload)
    return response


@router.post("/add_task")
async def add_task(request_payload: TaskCreateRequestData):
    response = ProjectBoardBase.add_task(request_payload)
    return response


@router.post("/update_task_status")
async def update_task_status(request_payload: TaskUpdateRequestData):
    response = ProjectBoardBase.update_task_status(request_payload)
    return response


@router.post("/list_boards")
async def list_boards(request_payload: TaskListRequestData):
    response = ProjectBoardBase.list_boards(request_payload)
    return response


@router.post("/export_board")
async def export_board(request_payload: ExportProjectBoardRequestData):
    response = ProjectBoardBase.export_board(request_payload)
    return response
