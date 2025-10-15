from fastapi import APIRouter, HTTPException
from app.models.user_model import UserCreate, UserLogin, UserResponse, Token
from app.services.utils.auth import hash_password, verify_password, create_access_token
from app.database import db  # ✅ import the shared instance

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate):
    print("DEBUG: Received signup request")  # Log entry
    print(f"DEBUG: user_name={user.user_name}, email={user.email}")  # Safe info

    hashed_pw = hash_password(user.password)
    print(f"DEBUG: Hashed password: {hashed_pw}")  # Only hashed, safe to print

    db_user = await db.user.create(
        data={"user_name": user.user_name, "email": user.email, "password": hashed_pw}
    )
    print(f"DEBUG: User created in DB: {db_user}")  # DB return object

    return db_user


@router.post("/signin", response_model=Token)
async def signin(user: UserLogin):
    db_user = await db.user.find_first(where={"email": user.email})
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})
    print(db_user, "databaseUser")
    return {"access_token": token, "user":db_user}



