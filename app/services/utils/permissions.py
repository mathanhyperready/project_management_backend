from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.services.utils.auth import decode_access_token
from app.database import db

# Define OAuth2 token scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

    user = await db.user.find_unique(
        where={"id": int(user_id)},
        include={"role": {"include": {"permissions": True}}}
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def require_permission(permission_code: str):
    async def wrapper(user = Depends(get_current_user)):
        role = user.role
        print("role****",role)
        if not role:
            raise HTTPException(status_code=403, detail="User has no role assigned")

        has_perm = any(p.code == permission_code for p in role.permissions)
        print("Has Permissiomn")
        if not has_perm:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission_code}' required"
            )
        return user

    return wrapper
