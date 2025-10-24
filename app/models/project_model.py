from pydantic import BaseModel
from datetime import datetime,date
from typing import Optional, List ,Dict, Any

class ProjectCreate(BaseModel):
    project_name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    client_id : Optional[int] = None
    status : Optional[str] = None

class ProjectUpdate(BaseModel):
    project_name: str = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    user_id: Optional[int] = None
    client_id : Optional[int] = None
    status : Optional[str] = None
    teamMembers : Optional[List[Dict[str, Any]]] = None


class ProjectResponse(ProjectCreate):
    id: int
    created_at: datetime
    client_id : int

    class Config:
        orm_mode = True