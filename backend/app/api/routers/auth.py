"""Authentication routes with rate limiting"""

from datetime import timedelta

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.exceptions import InactiveUserError, InvalidCredentialsError
from app.core.limiter import limiter
from app.core.logging import get_logger
from app.db.base import get_db
from app.db.models.user import User
from app.schemas.common import LoginRequest, LoginResponse, MessageResponse, PasswordChangeRequest
from app.schemas.user import UserResponse
from app.security.auth import authenticate_user, create_access_token, get_password_hash, verify_password

router = APIRouter()
logger = get_logger(__name__)


@router.post("/login", response_model=LoginResponse)
@limiter.limit(f"{settings.RATE_LIMIT_LOGIN_PER_MINUTE}/minute")
async def login(
    request: Request,
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login endpoint with rate limiting

    Rate limit: 5 requests per minute per IP
    """
    # Authenticate user
    user = authenticate_user(db, login_data.email, login_data.password)

    if not user:
        logger.warning(
            f"Failed login attempt for email: {login_data.email}",
            extra={"email": login_data.email, "ip": request.client.host}
        )
        raise InvalidCredentialsError()

    if not user.is_active:
        logger.warning(
            f"Login attempt for inactive user: {login_data.email}",
            extra={"user_id": str(user.id)}
        )
        raise InactiveUserError()

    # Create access token
    access_token_expires = timedelta(minutes=settings.JWT_EXPIRES_MIN)
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role.value},
        expires_delta=access_token_expires
    )

    logger.info(
        f"Successful login for user: {user.email}",
        extra={"user_id": str(user.id), "role": user.role.value}
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role.value,
            "is_active": user.is_active
        }
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user


@router.post("/change-password", response_model=MessageResponse)
@limiter.limit("10/hour")  # Prevent brute force
async def change_password(
    request: Request,
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change password for current user

    Rate limit: 10 requests per hour per user
    """
    # Verify current password
    if not verify_password(password_data.current_password, current_user.hashed_password):
        logger.warning(
            f"Failed password change attempt - wrong current password",
            extra={"user_id": str(current_user.id)}
        )
        raise InvalidCredentialsError()

    # Hash and update new password
    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()

    logger.info(
        f"Password changed successfully",
        extra={"user_id": str(current_user.id)}
    )

    return MessageResponse(message="Password changed successfully")
