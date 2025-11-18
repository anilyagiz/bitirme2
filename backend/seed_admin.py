#!/usr/bin/env python3
"""
Admin user creation script for Temizlik Takip Sistemi
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models.user import User, UserRole
from app.security.auth import get_password_hash
from app.config import settings

def create_admin_user():
    """Create an admin user in the database"""
    
    # Database URL
    database_url = settings.DATABASE_URL
    
    # Create engine
    engine = create_engine(database_url, echo=True)
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Check if admin user already exists
        from sqlalchemy import select
        result = session.execute(
            select(User).where(User.email == "admin@kku.com")
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            print("Admin user already exists!")
            print(f"Email: {existing_user.email}")
            print(f"Role: {existing_user.role}")
            return
        
        # Create admin user
        admin_user = User(
            email="admin@kku.com",
            full_name="Sistem Admin",
            role=UserRole.ADMIN,
            hashed_password=get_password_hash("admin123")
        )
        
        session.add(admin_user)
        session.commit()
        
        print("Admin user created successfully!")
        print("Login credentials:")
        print("Email: admin@kku.com")
        print("Password: admin123")
        print("\nPlease change the password after first login!")
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        session.rollback()
    finally:
        session.close()
        engine.dispose()

if __name__ == "__main__":
    create_admin_user()
