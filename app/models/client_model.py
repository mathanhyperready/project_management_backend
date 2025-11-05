from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ClientCreate(BaseModel):
    name: str
    email: Optional[str] = None
    address: Optional[str] = None
    contact: Optional[str] = None
    notes: Optional[str] = None
    is_enabled: bool = True
    created_by: Optional[int] = None


class UserCreator(BaseModel):
    id: int
    user_name: str
    email: Optional[str] = None

    class Config:
        from_attributes = True


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    contact: Optional[str] = None
    notes: Optional[str] = None
    is_enabled: Optional[bool] = True


class ClientResponse(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    address: Optional[str] = None
    contact: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    is_enabled: bool
    creator: Optional[UserCreator] = None 

    class Config:
        from_attributes = True
