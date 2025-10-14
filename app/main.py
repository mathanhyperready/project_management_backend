from fastapi import FastAPI
from app.routers import project_router, task_router
from app.database import db

app = FastAPI(title="Time Tracker API")

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

# Routers
app.include_router(project_router.router, prefix="/projects", tags=["Projects"])
app.include_router(task_router.router, prefix="/tasks", tags=["Tasks"])
