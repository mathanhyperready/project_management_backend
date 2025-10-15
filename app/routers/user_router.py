from fastapi import APIRouter
from app.database import db
from app.models.user_model import UserCreate,UserUpdate,UserResponse
from fastapi import APIRouter, HTTPException
from app.services.utils.auth import hash_password 

app = APIRouter()


@app.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    existing_user = await db.user.find_first(where={"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = hash_password(user.password)
    new_user = await db.user.create(
        data={
            "user_name": user.user_name,
            "email": user.email,
            "password": hashed_pw
        }
    )
    return new_user

@app.get("/")
async def get_users():
    return await db.user.find_many(include={
        "projects": True,
        "timesheets": True
    })

@app.get("/{user_name}")
async def get_single_user(user_name : str):
    return await db.user.find_many(
        include={
        "projects": True,
        "timesheets": True
    },
        where = {"user_name" : user_name}
    )



@app.put("/{user_name}")
async def update_user(user_name : str, user : UserUpdate):
    data = user.dict(exclude_unset=True)
    try:
        updated_user = await db.user.update(
            where={"user_name": user_name},
            data=data
        )
        return updated_user
    except Exception:
        raise HTTPException(status_code=404, detail=f"User '{user_name}' not found")

@app.delete("/{user_name}")
async def delete_user(user_name: str):
    return await db.user.delete(
            where={"user_name": user_name}
        )
    