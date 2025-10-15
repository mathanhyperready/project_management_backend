from fastapi import APIRouter, HTTPException
from app.database import db
from app.models.timesheet_model import TimesheetCreate, TimesheetUpdate
import json

router = APIRouter()

@router.post("/")
async def create_timesheet(timesheet: TimesheetCreate):
    try:
        duration = None
        if timesheet.start_date and timesheet.end_date:
            diff = timesheet.end_date - timesheet.start_date
            duration = round(diff.total_seconds() / 3600, 2)

        data = {
            "description": timesheet.description,
            "status": timesheet.status,
            "start_date": timesheet.start_date,
            "end_date": timesheet.end_date,
            "projectId" : timesheet.projectId,
            "userId" : timesheet.userId,
            "duration": duration,
        }
        new_timesheet = await db.timesheet.create(data=data)
        return new_timesheet

    except Exception as e:
        print("Error creating timesheet:", e)
        raise HTTPException(status_code=500, detail="Failed to create timesheet")
    
    
@router.get("/{project_id}")
async def get_timesheet_list(project_id: int):
    return await db.timesheet.find_many(where={"project": {"id": project_id}})


@router.get("/{timesheet_id}")
async def get_single_timesheet(timesheet_id : int):
    return await db.timesheet.find_many(where={"timesheet": {"id": timesheet_id}})

# DELETE
@router.delete("/{timesheet_id}")
async def delete_timesheet(timesheet_id: int):
    try:
        return await db.timesheet.delete(where={"id": timesheet_id})
    except Exception:
        raise HTTPException(status_code=404, detail="Task not found")

@router.put("/{timesheet_id}")
async def update_timesheet(timesheet_id: int, timesheet: TimesheetUpdate):
    data = timesheet.dict(exclude_unset=True)
    print("Incoming data:", data)

    try:
        updated = await db.timesheet.update(
            where={"id": timesheet_id},
            data=data
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Timesheet id not found")
        return updated
    except Exception as e:
        print("Error updating timesheet:", e)
        raise HTTPException(status_code=404, detail="Timesheet id not found")

@router.put("/bulk-update/")
async def bulk_update_timesheet(timesheet_id: list[int], task: TimesheetUpdate):
    data = task.dict(exclude_unset=True)

    updated_timesheet = []
    for tid in timesheet_id:
        try:
            updated_task = await db.task.update(
                where={"id": tid},
                data=data
            )
            updated_timesheet.append(updated_task)
        except Exception:
            continue

    return {"updated_count": len(updated_timesheet), "tasks": updated_timesheet}