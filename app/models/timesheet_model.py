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
    status : Optional[str] = None
    created_by: Optional[int] = None


class TimesheetUpdate(BaseModel):
    description: Optional[str] = None
    status: Optional[str] = None
    userId: Optional[int] = None
    projectId: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status : Optional[str] = None
    created_by: Optional[int] = None

class UserCreator(BaseModel):
    id: int
    user_name: str
    email: Optional[str] = None


class TimesheetResponse(TimesheetCreate):
    id: int
    created_at: datetime
    creator: Optional[UserCreator] = None

    class Config:
        from_attributes = True
