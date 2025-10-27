from fastapi import APIRouter, HTTPException, status
from typing import List
from app.database import db
from app.models.role_model import RoleCreate, RoleResponse, RoleUpdate

router = APIRouter()

@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(data: RoleCreate):
    try:
        existing = await db.role.find_first(where={"name": data.name})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role name already exists"
            )

        # Base create data
        create_data = {
            "name": data.name,
            "is_enabled": data.is_enabled,
            "created_by": data.created_by,
        }

        # Attach permissions (if provided)
        if data.permissions:
            create_data["permissions"] = {
                "connect": [{"code": code} for code in data.permissions]
            }

        role = await db.role.create(
            data=create_data,
            include={"permissions": True}
        )

        return role

    except HTTPException:
        raise
    except Exception as e:
        print("Create Role Error:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create role: {e}"
        )



@router.get("/", response_model=List[RoleResponse])
async def get_all_roles():
    try:
        roles = await db.role.find_many(include={"permissions": True},order={"id": "asc"})
        return roles
    except Exception as e:
        print("Get All Roles Error:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch roles"
        )


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(role_id: int):
    try:
        role = await db.role.find_unique(where={"id": role_id},include={"permissions": True})
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        return role
    except HTTPException:
        raise
    except Exception as e:
        print("Get Role Error:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch role"
        )


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(role_id: int, data: RoleUpdate):
    try:
        existing = await db.role.find_unique(where={"id": role_id})
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )

        updated = await db.role.update(
            where={"id": role_id},
            data=data.model_dump(exclude_unset=True)
        )
        return updated
    except HTTPException:
        raise
    except Exception as e:
        print("Update Role Error:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update role"
        )


@router.delete("/{role_id}")
async def delete_role(role_id: int):
    try:
        users_with_role = await db.user.find_many(where={"role_id": role_id})
        if users_with_role:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete role because users are assigned to it"
            )

        await db.role.delete(where={"id": role_id})
        return {"message": f"Role {role_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print("Delete Role Error:", e)
        raise HTTPException(status_code=500, detail="Failed to delete role")
