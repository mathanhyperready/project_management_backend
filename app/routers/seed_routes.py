from fastapi import APIRouter, HTTPException
from app.database import db

router = APIRouter()

# Permissions to seed
PERMISSIONS = [
    {"name": "Create Project", "code": "project_create"},
    {"name": "View Project", "code": "project_read"},
    {"name": "Edit Project", "code": "project_update"},
    {"name": "Delete Project", "code": "project_delete"},
]


@router.get("/seed/permissions")
async def seed_permissions():
    try:
        print("⏳ Seeding permissions...")
        for p in PERMISSIONS:
            await db.permission.upsert(
                where={"code": p["code"]},
                data={
                    "create": p,
                    "update": {}
                }
            )

        await db.disconnect()
        print("✅ Permissions seeded successfully!")
        return {"message": "Permissions seeded successfully"}

    except Exception as e:
        print(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))
