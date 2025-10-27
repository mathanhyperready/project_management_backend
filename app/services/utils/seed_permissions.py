import asyncio
import traceback
from app.database import db
import os
import sys
import time

PERMISSIONS = [
    {"name": "Create Project", "code": "project_create"},
    {"name": "View Project", "code": "project_read"},
    {"name": "Edit Project", "code": "project_update"},
    {"name": "Delete Project", "code": "project_delete"},
]

async def seed_permissions():
    print("[DEBUG] seed_permissions start")
    try:
        print("[DEBUG] connecting to db...")
        await db.connect()
        print("[DEBUG] connected")

        for p in PERMISSIONS:
            print(f"[DEBUG] upserting permission: code={p['code']} name={p['name']}")
            try:
                res = await db.permission.upsert(
                    where={"code": p["code"]},
                    update={}, 
                    create=p
                )
                print(f"[DEBUG] upsert result id={getattr(res, 'id', 'N/A')} code={getattr(res, 'code', None)}")
            except Exception as e:
                print(f"[ERROR] failed upsert for {p['code']}: {e}")
                traceback.print_exc()

        # Validate: fetch all permissions we just ensured
        codes = [p["code"] for p in PERMISSIONS]
        print(f"[DEBUG] fetching inserted/updated permissions for codes: {codes}")
        found = await db.permission.find_many(where={"code": {"in": codes}})
        print(f"[DEBUG] found {len(found)} permissions in DB")
        for f in found:
            # If using Prisma client objects, convert to dict-ish logging
            print(f"[PERM] id={f.id} code={f.code} name={f.name} created_at={getattr(f, 'created_at', None)}")

    except Exception as e:
        print("[FATAL] unexpected error during seeding:")
        traceback.print_exc()
        raise
    finally:
        try:
            print("[DEBUG] disconnecting from db...")
            await db.disconnect()
            print("[DEBUG] disconnected")
        except Exception as e:
            print("[WARNING] error during db.disconnect():", e)
            traceback.print_exc()


def main():
    print("[INFO] Starting seed script")
    try:
        asyncio.run(seed_permissions())
        print("[INFO] Seed script finished successfully")
    except Exception as e:
        print("[ERROR] seed script failed:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
