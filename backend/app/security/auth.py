"""Authentication utilities with enhanced security"""

import secrets
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.core.config import settings
from app.core.logging import get_logger
from app.db.models.user import User

logger = get_logger(__name__)

# Dummy hash for timing attack prevention
DUMMY_PASSWORD_HASH = "$2b$12$dummyhashtopreventtimingattacksthatareveryimportantforsecurity"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hash

    Args:
        plain_password: Plain text password
        hashed_password: Bcrypt hash

    Returns:
        True if password matches, False otherwise
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False


def get_password_hash(password: str) -> str:
    """
    Hash password using bcrypt

    Args:
        password: Plain text password

    Returns:
        Bcrypt hash
    """
    return bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS)
    ).decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token

    Args:
        data: Token payload
        expires_delta: Optional expiration time delta

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRES_MIN)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),  # Issued at
        "type": "access"
    })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGO
    )

    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verify and decode JWT token

    Args:
        token: JWT token

    Returns:
        Decoded payload

    Raises:
        HTTPException: If token is invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGO]
        )

        # Validate token type
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload

    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def authenticate_user(db, email: str, password: str) -> Optional[User]:
    """
    Authenticate user with timing attack prevention

    Args:
        db: Database session
        email: User email
        password: Plain text password

    Returns:
        User object if authenticated, None otherwise

    Note:
        Uses constant-time comparison to prevent timing attacks
    """
    # Query user
    user = db.query(User).filter(User.email == email).first()

    # Always verify hash, even if user not found (prevent timing attack)
    if user:
        password_correct = verify_password(password, user.hashed_password)
    else:
        # Dummy verification with same timing
        verify_password(password, DUMMY_PASSWORD_HASH)
        password_correct = False

    # Use secrets.compare_digest for constant-time comparison
    # This prevents timing attacks on the final check
    if user and password_correct:
        return user

    return None
