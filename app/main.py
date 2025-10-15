from fastapi import FastAPI
from app.routers import project_router, timesheet_router,user_router
from app.database import db

app = FastAPI(title="Time Tracker API")

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

# Routers
app.include_router(user_router.app,prefix="/user", tags= ["User"])
app.include_router(project_router.router, prefix="/projects", tags=["Projects"])
app.include_router(timesheet_router.router, prefix="/timesheet", tags=["Timesheet"])
