from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from app.db.models.location import LocationType

class LocationBase(BaseModel):
    name: str
    location_type: LocationType
    location_subtype: Optional[str] = None
    building_id: str
    department_id: Optional[str] = None
    parent_location_id: Optional[str] = None
    is_leaf: bool = True
    floor_label: Optional[str] = None
    area_sqm: Optional[int] = None
    special_instructions: Optional[str] = None
    is_active: bool = True

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseModel):
    name: Optional[str] = None
    location_type: Optional[LocationType] = None
    location_subtype: Optional[str] = None
    building_id: Optional[str] = None
    department_id: Optional[str] = None
    parent_location_id: Optional[str] = None
    is_leaf: Optional[bool] = None
    floor_label: Optional[str] = None
    area_sqm: Optional[int] = None
    special_instructions: Optional[str] = None
    is_active: Optional[bool] = None

class LocationResponse(LocationBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
