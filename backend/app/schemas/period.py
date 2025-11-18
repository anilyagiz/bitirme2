from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID
from app.db.models.period import PeriodStatus

class PeriodBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    status: PeriodStatus = PeriodStatus.PLANNED

class PeriodCreate(PeriodBase):
    pass

class PeriodUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class PeriodResponse(PeriodBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
