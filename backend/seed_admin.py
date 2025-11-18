#!/usr/bin/env python3
"""
Admin user creation script for Temizlik Takip Sistemi

Usage:
    # With environment variables (recommended)
    export ADMIN_EMAIL="admin@example.com"
    export ADMIN_PASSWORD="SecurePassword123!"
    python seed_admin.py

    # Interactive mode
    python seed_admin.py --interactive
"""

import getpass
import os
import sys
from argparse import ArgumentParser

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.logging import get_logger
from app.db.models.user import User, UserRole
from app.security.auth import get_password_hash

logger = get_logger(__name__)


def validate_password(password: str) -> bool:
    """Validate password strength"""
    if len(password) < settings.PASSWORD_MIN_LENGTH:
        logger.error(f"Password must be at least {settings.PASSWORD_MIN_LENGTH} characters long")
        return False

    import re
    if not re.search(r'[A-Z]', password):
        logger.error("Password must contain at least one uppercase letter")
        return False
    if not re.search(r'[a-z]', password):
        logger.error("Password must contain at least one lowercase letter")
        return False
    if not re.search(r'[0-9]', password):
        logger.error("Password must contain at least one digit")
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=]', password):
        logger.error("Password must contain at least one special character")
        return False

    return True


def create_admin_user(email: str = None, password: str = None, interactive: bool = False):
    """
    Create an admin user in the database

    Args:
        email: Admin email
        password: Admin password
        interactive: If True, prompt for credentials
    """
    # Get credentials from environment or arguments
    if interactive:
        email = input("Admin email: ").strip()
        password = getpass.getpass("Admin password: ")
        password_confirm = getpass.getpass("Confirm password: ")

        if password != password_confirm:
            logger.error("Passwords do not match!")
            sys.exit(1)
    else:
        email = email or os.getenv("ADMIN_EMAIL", "admin@example.com")
        password = password or os.getenv("ADMIN_PASSWORD")

        if not password:
            logger.error(
                "Password not provided! Use ADMIN_PASSWORD environment variable or --interactive flag"
            )
            sys.exit(1)

    # Validate password
    if not validate_password(password):
        logger.error("Password does not meet security requirements")
        sys.exit(1)

    # Create engine (without echo in production)
    engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)

    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Check if admin user already exists
        result = session.execute(select(User).where(User.email == email))
        existing_user = result.scalar_one_or_none()

        if existing_user:
            logger.info(f"User with email '{email}' already exists!")
            logger.info(f"  Role: {existing_user.role}")
            logger.info(f"  Active: {existing_user.is_active}")
            return

        # Create admin user
        admin_user = User(
            email=email,
            full_name=input("Admin full name: ") if interactive else "System Administrator",
            role=UserRole.ADMIN,
            hashed_password=get_password_hash(password),
            is_active=True
        )

        session.add(admin_user)
        session.commit()

        logger.info("=" * 60)
        logger.info("Admin user created successfully!")
        logger.info("=" * 60)
        logger.info(f"Email: {email}")
        logger.info(f"Role: {admin_user.role.value}")
        logger.info("")
        logger.info("IMPORTANT: Change your password after first login!")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Error creating admin user: {e}", exc_info=True)
        session.rollback()
        sys.exit(1)
    finally:
        session.close()
        engine.dispose()


if __name__ == "__main__":
    parser = ArgumentParser(description="Create admin user for Temizlik Takip Sistemi")
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Interactive mode (prompt for credentials)"
    )
    parser.add_argument("--email", help="Admin email")
    parser.add_argument("--password", help="Admin password (not recommended, use env var)")

    args = parser.parse_args()

    create_admin_user(
        email=args.email,
        password=args.password,
        interactive=args.interactive
    )
