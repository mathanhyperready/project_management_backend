from fastapi import APIRouter
from app.database import db
from app.models.task_model import TaskCreate

router = APIRouter()

@router.post("/")
async def create_task(task: TaskCreate):
    return await db.task.create(data=task.dict())

@router.get("/{project_id}")
async def list_tasks(project_id: int):
    return await db.task.find_many(where={"project_id": project_id})
