from fastapi import APIRouter, HTTPException, status
from app.models.user_model import UserCreate, UserLogin, UserResponse, Token
from app.services.utils.auth import hash_password, verify_password, create_access_token
from app.database import db

router = APIRouter()
@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate):
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



@router.post("/signin", response_model=Token)
async def signin(user: UserLogin):
    try:
        db_user = await db.user.find_first(where={"email": user.email},include={"role": { "include": { "permissions": True } }})
        if not db_user or not verify_password(user.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        token = create_access_token({"sub": str(db_user.id)})
        return {
            "access_token": token,
            "user": db_user
        }

    except HTTPException:
        raise
    except Exception as e:
        print("Sign-in failed:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error during sign-in"
        )



