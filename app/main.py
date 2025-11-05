from fastapi import FastAPI
from app.routers import project_router, timesheet_router,user_router,auth,role_router, client_router, seed_routes, permissionRoutes
from app.database import db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Time Tracker API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True, 
    allow_methods=["*"],    
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(role_router.router, prefix="/role", tags=["Role"])
app.include_router(user_router.app,prefix="/user", tags= ["User"])
app.include_router(client_router.router, prefix="/clients", tags=["Client"])
app.include_router(project_router.router, prefix="/projects", tags=["Projects"])
app.include_router(timesheet_router.router, prefix="/timesheet", tags=["Timesheet"])
app.include_router(seed_routes.router, prefix='/seed', tags=["seed"])
app.include_router(permissionRoutes.router)