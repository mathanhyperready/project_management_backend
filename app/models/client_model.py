from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ClientCreate(BaseModel):
    name: str
    email: Optional[str] = None
    address: Optional[str] = None
    contact: Optional[str] = None
    notes: Optional[str] = None
    is_enabled : bool = True
    


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    contact: Optional[str] = None
    notes: Optional[str] = None
    is_enabled : bool = True


class ClientResponse(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    address: Optional[str] = None
    contact: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
