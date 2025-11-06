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
            
        create_data = {
            "name": data.name,
            "is_enabled": data.is_enabled,
            # "created_by": data.created_by,
        }

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
        roles = await db.role.find_many(
            include={
                "permissions": True,
                "creator": True
            },
            order={"id": "asc"}
        )
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
        role = await db.role.find_unique(
            where={"id": role_id},
            include={"permissions": True}
        )
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
        existing_role = await db.role.find_unique(
            where={"id": role_id},
            include={"permissions": True}
        )
        if not existing_role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        current_codes = [p.code for p in existing_role.permissions]
        
        if data.permissions is not None:
            removed = set(current_codes) - set(data.permissions)
            added = set(data.permissions) - set(current_codes)
    
        update_data = data.model_dump(exclude_unset=True)
        

        if data.permissions is not None:
            if data.permissions:

                existing_perms = await db.permission.find_many(
                    where={"code": {"in": data.permissions}}
                )
                existing_codes = {perm.code for perm in existing_perms}
                
                missing_codes = set(data.permissions) - existing_codes
                
                if missing_codes:
                    await db.permission.create_many(
                        data=[
                            {"code": code, "name": code.replace("_", " ").title()}
                            for code in missing_codes
                        ],
                        skip_duplicates=True
                    )
            
            update_data["permissions"] = {
                "set": [{"code": code} for code in data.permissions]
            }

        updated_role = await db.role.update(
            where={"id": role_id},
            data=update_data,
            include={"permissions": True}
        )
        
        updated_codes = [p.code for p in updated_role.permissions]
        
        return updated_role

    except HTTPException:
        raise
    except Exception as e:
        print("Update Role Error:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update role"
        )


@router.patch("/{role_id}/permissions/remove")
async def remove_specific_permission(role_id: int, permission_code: str):
    try:
        role = await db.role.find_unique(
            where={"id": role_id},
            include={"permissions": True}
        )
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        current_permission_codes = [p.code for p in role.permissions]
        
        if permission_code not in current_permission_codes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Permission '{permission_code}' not found in this role"
            )
    
        updated_role = await db.role.update(
            where={"id": role_id},
            data={
                "permissions": {
                    "disconnect": [{"code": permission_code}]
                }
            },
            include={"permissions": True}
        )
        
        updated_codes = [p.code for p in updated_role.permissions]
        
        return {
            "message": f"Permission '{permission_code}' removed successfully",
            "role": updated_role
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print("Remove Permission Error:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove permission from role"
        )


@router.patch("/{role_id}/permissions/add")
async def add_specific_permission(role_id: int, permission_code: str):
    try:
        role = await db.role.find_unique(
            where={"id": role_id},
            include={"permissions": True}
        )
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        current_permission_codes = [p.code for p in role.permissions]
        
        if permission_code in current_permission_codes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Permission '{permission_code}' already exists in this role"
            )
        
        
        permission = await db.permission.find_unique(where={"code": permission_code})
        if not permission:
            
            permission = await db.permission.create(
                data={
                    "code": permission_code,
                    "name": permission_code.replace("_", " ").title()
                }
            )
            print(f"📝 Created new permission: {permission_code}")
        
        
        updated_role = await db.role.update(
            where={"id": role_id},
            data={
                "permissions": {
                    "connect": [{"code": permission_code}]
                }
            },
            include={"permissions": True}
        )
        
        updated_codes = [p.code for p in updated_role.permissions]
        
        print(f"Updated permissions: {updated_codes}")
        print("=" * 40)
        
        return {
            "message": f"Permission '{permission_code}' added successfully",
            "role": updated_role
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print("Add Permission Error:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add permission to role"
        )


@router.delete("/{role_id}/permissions/{permission_code}")
async def remove_permission_from_role(role_id: int, permission_code: str):
    try:
        role = await db.role.find_unique(
            where={"id": role_id},
            include={"permissions": True}
        )
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        current_permission_codes = [p.code for p in role.permissions]
        if permission_code not in current_permission_codes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Permission '{permission_code}' not found in this role"
            )
        updated_role = await db.role.update(
            where={"id": role_id},
            data={
                "permissions": {
                    "disconnect": [{"code": permission_code}]
                }
            },
            include={"permissions": True}
        )
        
        return {
            "message": f"Permission '{permission_code}' removed from role",
            "role": updated_role
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print("Remove Permission Error:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove permission from role"
        )


@router.post("/{role_id}/permissions/{permission_code}")
async def add_permission_to_role(role_id: int, permission_code: str):
    try:
        role = await db.role.find_unique(
            where={"id": role_id},
            include={"permissions": True}
        )
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        

        current_permission_codes = [p.code for p in role.permissions]
        if permission_code in current_permission_codes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Permission '{permission_code}' already exists in this role"
            )
    
        permission = await db.permission.find_unique(where={"code": permission_code})
        if not permission:
            permission = await db.permission.create(
                data={
                    "code": permission_code,
                    "name": permission_code.replace("_", " ").title()
                }
            )
    
        updated_role = await db.role.update(
            where={"id": role_id},
            data={
                "permissions": {
                    "connect": [{"code": permission_code}]
                }
            },
            include={"permissions": True}
        )
        
        return {
            "message": f"Permission '{permission_code}' added to role",
            "role": updated_role
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print("Add Permission Error:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add permission to role"
        )


@router.delete("/{role_id}")
async def delete_role(role_id: int):
    try:
        users_with_role = await db.user.find_many(where={"role_id": role_id})
        if users_with_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete role because users are assigned to it"
            )

        role = await db.role.find_unique(where={"id": role_id})
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )

        await db.role.delete(where={"id": role_id})
        return {"message": f"Role {role_id} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        print("Delete Role Error:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete role"
        )