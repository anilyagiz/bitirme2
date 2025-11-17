from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routers import auth, users, buildings, departments, locations, periods, assignments, dashboard

app = FastAPI(
    title="Temizlik Takip Sistemi",
    description="Hafif Temizlik Takip Sistemi API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(buildings.router, prefix="/api/v1/buildings", tags=["buildings"])
app.include_router(departments.router, prefix="/api/v1/departments", tags=["departments"])
app.include_router(locations.router, prefix="/api/v1/locations", tags=["locations"])
app.include_router(periods.router, prefix="/api/v1/periods", tags=["periods"])
app.include_router(assignments.router, prefix="/api/v1/assignments", tags=["assignments"])
app.include_router(assignments.router, prefix="/api/v1/my", tags=["my"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["dashboard"])

@app.get("/")
async def root():
    return {"message": "Temizlik Takip Sistemi API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
