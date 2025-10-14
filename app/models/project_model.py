from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str]
    start_date: datetime
    end_date: datetime

class ProjectResponse(ProjectCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True