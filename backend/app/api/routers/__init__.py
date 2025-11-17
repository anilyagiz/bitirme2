# Import all routers
from .auth import router as auth_router
from .users import router as users_router
from .buildings import router as buildings_router
from .departments import router as departments_router
from .locations import router as locations_router
from .periods import router as periods_router
from .assignments import router as assignments_router
from .dashboard import router as dashboard_router

__all__ = [
    "auth_router",
    "users_router", 
    "buildings_router",
    "departments_router",
    "locations_router",
    "periods_router",
    "assignments_router",
    "dashboard_router"
]
