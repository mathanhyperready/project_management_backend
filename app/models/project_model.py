from pydantic import BaseModel
from datetime import datetime,date
from typing import Optional, List

class ProjectCreate(BaseModel):
    project_name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ProjectUpdate(BaseModel):
    project_name: str = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    user_id: Optional[int] = None


class ProjectResponse(ProjectCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True