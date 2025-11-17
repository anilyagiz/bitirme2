from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from app.db.models.assignment import AssignmentStatus
from app.schemas.user import UserResponse
from app.schemas.location import LocationResponse
from app.schemas.period import PeriodResponse

class AssignmentBase(BaseModel):
    location_id: str
    period_id: str
    staff_user_id: str
    supervisor_user_id: str
    status: AssignmentStatus = AssignmentStatus.PENDING
    staff_notes: Optional[str] = None
    supervisor_notes: Optional[str] = None
    rejection_reason: Optional[str] = None
    rating: Optional[int] = None

class AssignmentCreate(BaseModel):
    location_id: str
    period_id: str
    staff_user_id: str
    supervisor_user_id: str

class AssignmentUpdate(BaseModel):
    location_id: Optional[str] = None
    period_id: Optional[str] = None
    staff_user_id: Optional[str] = None
    supervisor_user_id: Optional[str] = None
    staff_notes: Optional[str] = None
    supervisor_notes: Optional[str] = None
    rejection_reason: Optional[str] = None
    rating: Optional[int] = None

class AssignmentCleanRequest(BaseModel):
    staff_notes: Optional[str] = None

class AssignmentApproveRequest(BaseModel):
    rating: Optional[int] = None
    supervisor_notes: Optional[str] = None
    
    @validator('rating')
    def validate_rating(cls, v):
        if v is not None and (v < 1 or v > 5):
            raise ValueError('Rating must be between 1 and 5')
        return v

class AssignmentRejectRequest(BaseModel):
    rejection_reason: str

class AssignmentResponse(AssignmentBase):
    id: str
    staff_completed_at: Optional[datetime] = None
    supervisor_reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
