from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    project_id: int
    title: str
    description: Optional[str]
    start_date: datetime
    end_date: datetime
    status: Optional[str] = "todo"

class TaskResponse(TaskCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
