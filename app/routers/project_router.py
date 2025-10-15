from fastapi import APIRouter, HTTPException
from app.database import db
from app.models.project_model import ProjectCreate, ProjectUpdate
from datetime import datetime,date

router = APIRouter()


# helper to convert date to datetime
def date_to_datetime(d: date | datetime | None) -> datetime | None:
    if d is None:
        return None
    if isinstance(d, datetime):
        return d
    return datetime(d.year, d.month, d.day)

@router.post("/")
async def create_project(project: ProjectCreate):
    return await db.project.create(
        data={
            "project_name": project.project_name,
            "description": project.description,
            "start_date": date_to_datetime(project.start_date),
            "end_date": date_to_datetime(project.end_date),
        }
    )

@router.get("/")
async def list_projects():
    return await db.project.find_many(include={"timesheets": True,"user" : True})

@router.get("/{project_id}")
async def get_single_project(project_id : int):
    return await db.project.find_many(
        where = {"id" : project_id}
    )

@router.put("/{project_id}")
async def update_project(project_id: int, project: ProjectUpdate):
    data = project.dict(exclude_unset=True)

    try:
        updated_project = await db.project.update(
            where={"id": project_id},
            data=data
        )
        return updated_project
    except Exception as e:
        print("Update error:", e)
        raise HTTPException(status_code=404, detail="Project not found")

 

@router.delete("/{project_id}")
async def delete_project(project_id: int):
    try:
        deleted_project = await db.project.delete(where={"id": project_id})
        return {"message": f"Project {project_id} deleted successfully"}
    except Exception:
        raise HTTPException(status_code=404, detail="Project not found")