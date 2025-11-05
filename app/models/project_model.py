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
    created_by: Optional[int] = None

class ProjectUpdate(BaseModel):
    project_name: str = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    user_id: Optional[int] = None
    client_id : Optional[int] = None
    status : Optional[str] = None
    teamMembers : Optional[List[Dict[str, Any]]] = None
    created_by: Optional[int] = None
    
class UserCreator(BaseModel):
    id: int
    user_name: str
    email: Optional[str] = None

    class Config:
        from_attributes = True


class ProjectResponse(ProjectCreate):
    id: int
    created_at: datetime
    client_id : int
    creator: Optional[UserCreator] = None

    class Config:
        orm_mode = True