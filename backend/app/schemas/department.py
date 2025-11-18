from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class DepartmentBase(BaseModel):
    name: str
    code: Optional[str] = None
    is_active: bool = True

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    is_active: Optional[bool] = None

class DepartmentResponse(DepartmentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
