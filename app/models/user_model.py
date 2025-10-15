from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    user_name : str
    password : str
    email : str
    

class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None

    
    
    
class UserResponse(UserCreate):
     id: int
     created_at: datetime
     
     class Config:
         orm_mode = True
    
    