import asyncio
import traceback
import os
import sys
from dotenv import load_dotenv

# -------------------------------------------------------
# Ensure project root is in path
# -------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# -------------------------------------------------------
# Load environment variables from backend .env file
# -------------------------------------------------------
ENV_PATH = "/home/admin/internal_projects/task_management/back-end/.env"
print("[DEBUG] Loading .env from:", ENV_PATH)
load_dotenv(dotenv_path=ENV_PATH)

# Check if DATABASE_URL is loaded
db_url = os.getenv("DATABASE_URL")
if not db_url:
    print("[ERROR] DATABASE_URL not found. Please verify .env path or variable name.")
    sys.exit(1)
print(f"[INFO] DATABASE_URL loaded successfully: {db_url}")

# -------------------------------------------------------
# Import your Prisma DB instance
# -------------------------------------------------------
try:
    from app.database import db
except ModuleNotFoundError:
    try:
        from database import db  # fallback if script run from inside app/
    except ModuleNotFoundError:
        print("[FATAL] Could not import 'db' from app.database or database")
        sys.exit(1)

# -------------------------------------------------------
# Define permissions
# -------------------------------------------------------
PERMISSIONS = [
    # Dashboard
    {"name": "View Dashboard", "code": "dashboard_view"},

    # Projects
    {"name": "Create Project", "code": "project_create"},
    {"name": "View Project", "code": "project_read"},
    {"name": "Edit Project", "code": "project_update"},
    {"name": "Delete Project", "code": "project_delete"},

    # Timesheet
    {"name": "View Timesheet", "code": "timesheet_view"},
    {"name": "Create Timesheet Entry", "code": "timesheet_create"},
    {"name": "Edit Timesheet Entry", "code": "timesheet_update"},
    {"name": "Delete Timesheet Entry", "code": "timesheet_delete"},

    # Calendar
    {"name": "View Calendar", "code": "calendar_view"},

    # User Management
    {"name": "View User", "code": "user_read"},
    {"name": "Create User", "code": "user_create"},
    {"name": "Edit User", "code": "user_update"},
    {"name": "Delete User", "code": "user_delete"},

    # Role Management
    {"name": "View Role", "code": "role_read"},
    {"name": "Create Role", "code": "role_create"},
    {"name": "Edit Role", "code": "role_update"},
    {"name": "Delete Role", "code": "role_delete"},

    # Client Management
    {"name": "View Client", "code": "client_read"},
    {"name": "Create Client", "code": "client_create"},
    {"name": "Edit Client", "code": "client_update"},
    {"name": "Delete Client", "code": "client_delete"},

    # Reports
    {"name": "View Reports", "code": "report_view"},

    # Role Permission Management
    {"name": "Manage Role Permissions", "code": "role_permission_manage"},
]

# -------------------------------------------------------
# Seeder function
# -------------------------------------------------------
async def seed_permissions():
    print("[INFO] Connecting to DB...")
    try:
        await db.connect()
        print("[INFO] Connected to DB")

        for p in PERMISSIONS:
            print(f"[DEBUG] Upserting permission: {p['code']}")
            try:
                res = await db.permission.upsert(
                    where={"code": p["code"]},
                    data={
                        "create": p,
                        "update": {"name": p["name"]}  # only update name if it exists
                    }
                )
                print(f"[SUCCESS] Permission ensured: {p['code']}")
            except Exception as e:
                print(f"[ERROR] Failed upsert for {p['code']}: {e}")
                traceback.print_exc()

        # Verify inserted permissions
        codes = [p["code"] for p in PERMISSIONS]
        found = await db.permission.find_many(where={"code": {"in": codes}})
        print(f"[INFO] {len(found)} permissions found in DB after seeding")
        for f in found:
            print(f"[PERM] {f.code} - {f.name}")

    except Exception as e:
        print("[FATAL] Unexpected error during seeding:")
        traceback.print_exc()
    finally:
        print("[INFO] Disconnecting DB...")
        await db.disconnect()
        print("[INFO] Disconnected successfully")

# -------------------------------------------------------
# Main Entry Point
# -------------------------------------------------------
def main():
    print("[INFO] Starting Permission Seeder")
    try:
        asyncio.run(seed_permissions())
        print("[INFO] Seeder finished successfully ✅")
    except Exception as e:
        print("[ERROR] Seeder failed:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
