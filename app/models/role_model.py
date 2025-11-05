from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Permission Schema (nested)
class PermissionBase(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


# 👇 Add this new schema for creator details
class UserCreator(BaseModel):
    id: int
    user_name: str
    email: Optional[str] = None

    class Config:
        from_attributes = True


class RoleBase(BaseModel):
    name: str
    is_enabled: bool = True


class RoleCreate(RoleBase):
    created_by: Optional[int] = None
    permissions: Optional[List[str]] = []  # list of permission codes


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    is_enabled: Optional[bool] = None
    permissions: Optional[List[str]] = None


class RoleResponse(RoleBase):
    id: int
    created_at: datetime
    permissions: Optional[List[PermissionBase]] = []
    creator: Optional[UserCreator] = None   # 👈 include the creator relationship

    class Config:
        from_attributes = True
