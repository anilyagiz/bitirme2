from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.db.base import get_db
from app.db.models.user import User
from app.db.models.period import Period, PeriodStatus
from app.schemas.period import PeriodCreate, PeriodUpdate, PeriodResponse
from app.schemas.common import PaginationParams, PaginatedResponse
from app.api.deps import require_admin

router = APIRouter()

@router.get("/", response_model=PaginatedResponse)
async def get_periods(
    pagination: PaginationParams = Depends(),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    query = db.query(Period)
    
    if status:
        query = query.filter(Period.status == status)
    
    total = query.count()
    periods = query.offset((pagination.page - 1) * pagination.page_size).limit(pagination.page_size).all()
    
    return PaginatedResponse(
        items=[PeriodResponse.from_orm(period) for period in periods],
        page=pagination.page,
        page_size=pagination.page_size,
        total=total
    )

@router.post("/", response_model=PeriodResponse)
async def create_period(
    period_data: PeriodCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    if period_data.start_date > period_data.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before end date"
        )
    
    db_period = Period(**period_data.dict())
    db.add(db_period)
    db.commit()
    db.refresh(db_period)
    
    return PeriodResponse.from_orm(db_period)

@router.get("/{period_id}", response_model=PeriodResponse)
async def get_period(
    period_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    period = db.query(Period).filter(Period.id == period_id).first()
    if not period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Period not found"
        )
    return PeriodResponse.from_orm(period)

@router.put("/{period_id}", response_model=PeriodResponse)
async def update_period(
    period_id: UUID,
    period_data: PeriodUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    period = db.query(Period).filter(Period.id == period_id).first()
    if not period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Period not found"
        )
    
    update_data = period_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(period, field, value)
    
    db.commit()
    db.refresh(period)
    
    return PeriodResponse.from_orm(period)

@router.put("/{period_id}/activate")
async def activate_period(
    period_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    period = db.query(Period).filter(Period.id == period_id).first()
    if not period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Period not found"
        )
    
    period.status = PeriodStatus.ACTIVE
    db.commit()
    
    return {"message": "Period activated successfully"}

@router.put("/{period_id}/complete")
async def complete_period(
    period_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    period = db.query(Period).filter(Period.id == period_id).first()
    if not period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Period not found"
        )
    
    period.status = PeriodStatus.COMPLETED
    db.commit()
    
    return {"message": "Period completed successfully"}

@router.delete("/{period_id}")
async def delete_period(
    period_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    period = db.query(Period).filter(Period.id == period_id).first()
    if not period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Period not found"
        )
    
    db.delete(period)
    db.commit()
    
    return {"message": "Period deleted successfully"}
