from fastapi import APIRouter, HTTPException, status
from app.database import db
from app.models.user_model import UserCreate, UserUpdate, UserResponse
from app.services.utils.auth import hash_password

app = APIRouter()

@app.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    try:
        existing_user = await db.user.find_first(where={"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        role = await db.role.find_unique(where={"id": user.role_id})
        if not role:
            raise HTTPException(status_code=400, detail="Invalid role_id")
        
        hashed_pw = hash_password(user.password)
        
        new_user = await db.user.create(
            data={
                "user_name": user.user_name,
                "email": user.email,
                "password": hashed_pw,
                "role_id": user.role_id
            }
        )
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        print("Create User Error:", e)
        raise HTTPException(status_code=500, detail="Failed to create user")


@app.get("/")
async def get_users():
    try:
        users = await db.user.find_many(include={
            "projects": True,
            "timesheets": True,
            "role": {
                    "include": {
                        "permissions": True
                    }
                }
        })
        return users
    except Exception as e:
        print("Get Users Error:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch users")


@app.get("/{user_name}")
async def get_single_user(user_name: str):
    try:
        user = await db.user.find_first(
            include={
                "projects": True,
                "timesheets": True,
                "role": True
            },
            where={"user_name": user_name}
        )
        if not user:
            raise HTTPException(status_code=404, detail=f"User '{user_name}' not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        print("Get Single User Error:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch user")


@app.put("/{user_name}")
async def update_user(user_name: str, user: UserUpdate):
    try:
        data = user.dict(exclude_unset=True)
        updated_user = await db.user.update(
            where={"user_name": user_name},
            data=data
        )
        return updated_user
    except Exception as e:
        print("Update User Error:", e)
        raise HTTPException(status_code=404, detail=f"User '{user_name}' not found")


@app.delete("/{user_name}")
async def delete_user(user_name: str):
    try:
        deleted_user = await db.user.delete(
            where={"user_name": user_name}
        )
        return {"message": f"User '{user_name}' deleted successfully"}
    except Exception as e:
        print("Delete User Error:", e)
        raise HTTPException(status_code=404, detail=f"User '{user_name}' not found")
