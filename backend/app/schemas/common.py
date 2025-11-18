"""Common schemas with enhanced validation"""

from typing import Any, Dict, List

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.config import settings


class LoginRequest(BaseModel):
    """Login request with email validation"""

    email: EmailStr  # Email validation
    password: str = Field(..., min_length=1, max_length=100)


class LoginResponse(BaseModel):
    """Login response"""

    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]


class PaginationParams(BaseModel):
    """Pagination parameters with constraints"""

    page: int = Field(default=1, ge=1, description="Page number (starts from 1)")
    page_size: int = Field(
        default=settings.DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.MAX_PAGE_SIZE,
        description=f"Items per page (max {settings.MAX_PAGE_SIZE})"
    )


class PaginatedResponse(BaseModel):
    """Paginated response"""

    items: List[Dict[str, Any]]
    page: int = Field(..., ge=1)
    page_size: int = Field(..., ge=1)
    total: int = Field(..., ge=0)


class DashboardStats(BaseModel):
    """Dashboard statistics"""

    period_id: str
    pending: int = Field(..., ge=0)
    cleaned: int = Field(..., ge=0)
    rejected: int = Field(..., ge=0)
    approved: int = Field(..., ge=0)


class PasswordChangeRequest(BaseModel):
    """Password change request with strong validation"""

    current_password: str = Field(..., min_length=1, max_length=100)
    new_password: str = Field(..., min_length=settings.PASSWORD_MIN_LENGTH)

    @field_validator('new_password')
    @classmethod
    def validate_password_strength(cls, v: str, info) -> str:
        """Validate password strength"""
        import re

        if len(v) < settings.PASSWORD_MIN_LENGTH:
            raise ValueError(
                f"Password must be at least {settings.PASSWORD_MIN_LENGTH} characters long"
            )

        # Check for uppercase
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')

        # Check for lowercase
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')

        # Check for digit
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')

        # Check for special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=]', v):
            raise ValueError('Password must contain at least one special character')

        # Check if different from current password (if available)
        current = info.data.get('current_password')
        if current and v == current:
            raise ValueError('New password must be different from current password')

        return v


class MessageResponse(BaseModel):
    """Generic message response"""

    message: str
