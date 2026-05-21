from fastapi import APIRouter, HTTPException

from app.models.generate import TaskResponse
from app.services.task_store import task_store


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str) -> TaskResponse:
    task = task_store.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse.from_task(task)
