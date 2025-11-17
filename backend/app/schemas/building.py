from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class BuildingBase(BaseModel):
    name: str
    code: Optional[str] = None
    is_active: bool = True

class BuildingCreate(BuildingBase):
    pass

class BuildingUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    is_active: Optional[bool] = None

class BuildingResponse(BuildingBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
