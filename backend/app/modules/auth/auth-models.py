"""
Authentication models using flexible role system.
1 user can have multiple roles (customer, staff, admin).
"""

from datetime import datetime, date
from uuid import UUID
from sqlmodel import SQLModel, Field

class Profile(SQLModel, table=True):
    """User profile - base info for all authenticated users"""
    
    id: UUID | None = Field(default=None, primary_key=True)
    user_id: str  # Foreign key to auth.users(id)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserRole(SQLModel, table=True):
    """User roles - supports multiple roles per user (Many-to-Many)"""
    
    id: UUID | None = Field(default=None, primary_key=True)
    user_id: str  # Foreign key to auth.users(id)
    role: str  # 'customer', 'staff', 'admin'
    assigned_at: datetime = Field(default_factory=datetime.utcnow)


class Customer(SQLModel, table=True):
    """Customer profile - extended information for customers"""
    
    id: UUID | None = Field(default=None, primary_key=True)
    user_id: str  # Foreign key to auth.users(id), unique
    full_name: str
    phone: str | None = None
    avatar_url: str | None = None
    date_of_birth: date | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Staff(SQLModel, table=True):
    """Staff profile - extended information for staff members"""
    
    id: UUID | None = Field(default=None, primary_key=True)
    user_id: str  # Foreign key to auth.users(id), unique
    full_name: str
    phone: str | None = None
    avatar_url: str | None = None
    specialization: str | None = None  # e.g., 'massage', 'skincare', 'nail'
    bio: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
