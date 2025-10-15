from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TimesheetCreate(BaseModel):
    projectId: Optional[int] = None
    userId: Optional[int] = None
    description: Optional[str] = None
    status: Optional[str] = "todo"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class TimesheetUpdate(BaseModel):
    description: Optional[str] = None
    status: Optional[str] = None
    userId: Optional[int] = None
    projectId: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class TimesheetResponse(TimesheetCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
