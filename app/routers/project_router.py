from fastapi import APIRouter, HTTPException
from app.database import db
from app.models.project_model import ProjectCreate

router = APIRouter()

@router.post("/")
async def create_project(project: ProjectCreate):
    return await db.project.create(data=project.dict())

@router.get("/")
async def list_projects():
    return await db.project.find_many(include={"tasks": True})
