from fastapi import APIRouter, HTTPException, status
from typing import List
from app.database import db
from app.models.permissionModel import PermissionCreate, PermissionUpdate, PermissionResponse

router = APIRouter(prefix="/permission", tags=["Permissions"])

# -----------------------
# Create Permission
# -----------------------
@router.post("/", response_model=PermissionResponse)
async def create_permission(payload: PermissionCreate):
    try:
        existing = await db.permission.find_first(
            where={"OR": [{"name": payload.name}, {"code": payload.code}]}
        )
        if existing:
            raise HTTPException(status_code=400, detail="Permission already exists")

        new_permission = await db.permission.create(data=payload.dict())
        return new_permission
    except Exception as e:
        print("[ERROR] Create Permission:", e)
        raise HTTPException(status_code=500, detail="Failed to create permission")


# -----------------------
# Get All Permissions
# -----------------------
@router.get("/", response_model=List[PermissionResponse])
async def get_all_permissions():
    try:
        permissions = await db.permission.find_many(order={"id": "asc"})
        return permissions
    except Exception as e:
        print("[ERROR] Get All Permissions:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch permissions")


# -----------------------
# Get Single Permission
# -----------------------
@router.get("/{id}", response_model=PermissionResponse)
async def get_permission(id: int):
    permission = await db.permission.find_unique(where={"id": id})
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission


# -----------------------
# Update Permission
# -----------------------
@router.put("/{id}", response_model=PermissionResponse)
async def update_permission(id: int, payload: PermissionUpdate):
    try:
        existing = await db.permission.find_unique(where={"id": id})
        if not existing:
            raise HTTPException(status_code=404, detail="Permission not found")

        updated = await db.permission.update(
            where={"id": id},
            data={k: v for k, v in payload.dict().items() if v is not None}
        )
        return updated
    except Exception as e:
        print("[ERROR] Update Permission:", e)
        raise HTTPException(status_code=500, detail="Failed to update permission")


# -----------------------
# Delete Permission
# -----------------------
@router.delete("/{id}")
async def delete_permission(id: int):
    try:
        existing = await db.permission.find_unique(where={"id": id})
        if not existing:
            raise HTTPException(status_code=404, detail="Permission not found")

        await db.permission.delete(where={"id": id})
        return {"message": "Permission deleted successfully"}
    except Exception as e:
        print("[ERROR] Delete Permission:", e)
        raise HTTPException(status_code=500, detail="Failed to delete permission")
