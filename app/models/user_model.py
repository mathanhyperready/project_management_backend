from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from .role_model import RoleResponse  # ✅ Import RoleResponse


class UserBase(BaseModel):
    user_name: str
    email: EmailStr
    role_id: Optional[int] = None
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    role_id: Optional[int] = None
    is_active: Optional[bool] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserData(BaseModel):
    id: int
    user_name: str
    email: EmailStr
    role_id: Optional[int] = None
    is_active: bool
    role: Optional[RoleResponse] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserData
