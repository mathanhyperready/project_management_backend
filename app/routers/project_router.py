from fastapi import APIRouter, HTTPException, Depends
from app.database import db
from app.models.project_model import ProjectCreate, ProjectUpdate
from datetime import datetime, date
from prisma import Json
from app.services.utils.permissions import require_permission

router = APIRouter()

def date_to_datetime(d: date | datetime | None) -> datetime | None:
    if d is None:
        return None
    if isinstance(d, datetime):
        return d
    return datetime(d.year, d.month, d.day)

@router.post("/")
# @router.post("/", dependencies=[Depends(require_permission("project_create"))])
async def create_project(project: ProjectCreate):
    try:
        created_project = await db.project.create(
            data={
                "project_name": project.project_name,
                "description": project.description,
                "start_date": date_to_datetime(project.start_date),
                "end_date": date_to_datetime(project.end_date),
                "created_by": project.created_by, 
            }
        )
        print("create_project********",created_project)
        return created_project
    
    except Exception as e:
        print("Create Project Error:", e)
        raise HTTPException(status_code=500, detail="Failed to create project")


@router.get("/")
async def list_projects():
    try:
        projects = await db.project.find_many(include={"timesheets": True, "user": True, "client" : True,"creator": True})
        return projects
    except Exception as e:
        print("List Projects Error:", e)
        raise HTTPException(status_code=500, detail="Failed to list projects")

@router.get("/{project_id}")
async def get_single_project(project_id: int):
    try:
        project = await db.project.find_first(
            where={"id": project_id},
            include={"timesheets": True,"creator": True}
        )
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except HTTPException:
        raise
    except Exception as e:
        print("Get Single Project Error:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch project")

@router.put("/{project_id}")
async def update_project(project_id: int, project: ProjectUpdate):
    try:
        data = project.dict(exclude_unset=True)
        if "teamMembers" in data and data["teamMembers"] is not None:
            data["teamMembers"] = Json(data["teamMembers"])
        updated_project = await db.project.update(
            where={"id": project_id},
            data=data
        )
        return updated_project
    except Exception as e:
        print("Update Project Error:", e)
        raise HTTPException(status_code=500, detail="Failed to update project")

@router.delete("/{project_id}")
async def delete_project(project_id: int):
    try:
        deleted_project = await db.project.delete(where={"id": project_id})
        return {"message": f"Project {project_id} deleted successfully"}
    except Exception as e:
        print("Delete Project Error:", e)
        raise HTTPException(status_code=500, detail="Failed to delete project")
