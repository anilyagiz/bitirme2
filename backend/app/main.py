"""Main application with enhanced security and monitoring"""

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy.exc import SQLAlchemyError

from app.api.routers import (
    assignments,
    auth,
    buildings,
    dashboard,
    departments,
    locations,
    periods,
    users,
)
from app.core.config import settings
from app.core.exceptions import AppException
from app.core.limiter import limiter
from app.core.logging import get_logger, setup_logging

# Setup logging
setup_logging(settings.LOG_LEVEL)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info(
        "Application starting",
        extra={
            "environment": settings.ENVIRONMENT,
            "version": app.version
        }
    )
    yield
    # Shutdown
    logger.info("Application shutting down")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Production-Ready Temizlik Takip Sistemi API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,  # Disable docs in production
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Add rate limiter state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Exception Handlers
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Handle application-specific exceptions"""
    logger.warning(
        f"Application exception: {exc.message}",
        extra={
            "status_code": exc.status_code,
            "path": request.url.path,
            "method": request.method
        }
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "type": exc.__class__.__name__,
            **exc.details
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database exceptions"""
    logger.error(
        f"Database error: {exc}",
        extra={
            "path": request.url.path,
            "method": request.method
        },
        exc_info=True
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Database error occurred"}
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(
        f"Unhandled exception: {exc}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "client_host": request.client.host if request.client else None
        },
        exc_info=True
    )

    # Don't expose internal errors in production
    if settings.ENVIRONMENT == "production":
        detail = "Internal server error"
    else:
        detail = str(exc)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": detail}
    )


# Middleware: Request Logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with timing"""
    start_time = time.time()

    # Log request
    logger.info(
        "Request received",
        extra={
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent")
        }
    )

    # Process request
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"Request processing error: {e}", exc_info=True)
        raise

    # Calculate duration
    duration_ms = int((time.time() - start_time) * 1000)

    # Log response
    logger.info(
        "Request completed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms
        }
    )

    # Add custom headers
    response.headers["X-Process-Time"] = str(duration_ms)

    return response


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.cors_methods_list,
    allow_headers=settings.cors_headers_list,
    expose_headers=["X-Process-Time"],
)


# Health Check Endpoints
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": settings.APP_NAME,
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Lightweight health check for load balancers"""
    return {"status": "ok"}


@app.get("/health/ready", tags=["Health"])
async def readiness_check():
    """Deep health check - database connectivity"""
    from sqlalchemy import text
    from app.db.base import SessionLocal

    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()

        return {
            "status": "ready",
            "database": "connected",
            "environment": settings.ENVIRONMENT
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {e}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "not_ready",
                "database": "disconnected",
                "error": str(e) if settings.DEBUG else "Database connection failed"
            }
        )


# Include API routers
api_prefix = f"/api/{settings.API_VERSION}"

app.include_router(auth.router, prefix=f"{api_prefix}/auth", tags=["Authentication"])
app.include_router(users.router, prefix=f"{api_prefix}/users", tags=["Users"])
app.include_router(buildings.router, prefix=f"{api_prefix}/buildings", tags=["Buildings"])
app.include_router(departments.router, prefix=f"{api_prefix}/departments", tags=["Departments"])
app.include_router(locations.router, prefix=f"{api_prefix}/locations", tags=["Locations"])
app.include_router(periods.router, prefix=f"{api_prefix}/periods", tags=["Periods"])
app.include_router(assignments.router, prefix=f"{api_prefix}/assignments", tags=["Assignments"])
app.include_router(assignments.router, prefix=f"{api_prefix}/my", tags=["My Tasks"])
app.include_router(dashboard.router, prefix=f"{api_prefix}/dashboard", tags=["Dashboard"])
