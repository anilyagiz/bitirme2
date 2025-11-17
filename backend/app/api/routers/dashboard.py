from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.base import get_db
from app.db.models.user import User
from app.db.models.assignment import Assignment, AssignmentStatus
from app.db.models.period import Period, PeriodStatus
from app.schemas.common import DashboardStats
from app.api.deps import require_admin

router = APIRouter()

@router.get("/active-period-stats", response_model=DashboardStats)
async def get_active_period_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    # Get active period
    active_period = db.query(Period).filter(Period.status == PeriodStatus.ACTIVE).first()
    if not active_period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active period found"
        )
    
    # Get assignment counts for active period
    stats = db.query(
        Assignment.status,
        func.count(Assignment.id).label('count')
    ).filter(
        Assignment.period_id == active_period.id
    ).group_by(Assignment.status).all()
    
    # Initialize counts
    counts = {
        AssignmentStatus.PENDING: 0,
        AssignmentStatus.CLEANED: 0,
        AssignmentStatus.REJECTED: 0,
        AssignmentStatus.APPROVED: 0
    }
    
    # Update counts from query results
    for status, count in stats:
        counts[status] = count
    
    return DashboardStats(
        period_id=active_period.id,
        pending=counts[AssignmentStatus.PENDING],
        cleaned=counts[AssignmentStatus.CLEANED],
        rejected=counts[AssignmentStatus.REJECTED],
        approved=counts[AssignmentStatus.APPROVED]
    )
