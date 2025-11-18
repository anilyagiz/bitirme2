from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.db.base import get_db
from app.db.models.user import User, UserRole
from app.db.models.assignment import Assignment, AssignmentStatus
from app.db.models.location import Location
from app.db.models.period import Period, PeriodStatus
from app.schemas.assignment import (
    AssignmentCreate, AssignmentUpdate, AssignmentResponse,
    AssignmentCleanRequest, AssignmentApproveRequest, AssignmentRejectRequest
)
from app.schemas.common import PaginationParams, PaginatedResponse
from app.api.deps import get_current_user, require_admin, require_staff, require_supervisor

router = APIRouter()

# Admin endpoints
@router.post("/", response_model=AssignmentResponse)
async def create_assignment(
    assignment_data: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    # Validate location is leaf
    location = db.query(Location).filter(Location.id == assignment_data.location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
    if not location.is_leaf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assignment can only be made to leaf locations"
        )
    
    # Validate period is active
    period = db.query(Period).filter(Period.id == assignment_data.period_id).first()
    if not period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Period not found"
        )
    if period.status != PeriodStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assignment can only be made to active periods"
        )
    
    # Check for existing assignment
    existing = db.query(Assignment).filter(
        Assignment.location_id == assignment_data.location_id,
        Assignment.period_id == assignment_data.period_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Assignment already exists for this location and period"
        )
    
    db_assignment = Assignment(**assignment_data.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    
    return AssignmentResponse.from_orm(db_assignment)

@router.get("/", response_model=PaginatedResponse)
async def get_assignments(
    pagination: PaginationParams = Depends(),
    period_id: Optional[str] = None,
    status: Optional[str] = None,
    building_id: Optional[str] = None,
    department_id: Optional[str] = None,
    staff_user_id: Optional[str] = None,
    supervisor_user_id: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    query = db.query(Assignment)
    
    if period_id:
        query = query.filter(Assignment.period_id == period_id)
    if status:
        query = query.filter(Assignment.status == status)
    if staff_user_id:
        query = query.filter(Assignment.staff_user_id == staff_user_id)
    if supervisor_user_id:
        query = query.filter(Assignment.supervisor_user_id == supervisor_user_id)
    
    total = query.count()
    assignments = query.offset((pagination.page - 1) * pagination.page_size).limit(pagination.page_size).all()
    
    return PaginatedResponse(
        items=[AssignmentResponse.from_orm(assignment) for assignment in assignments],
        page=pagination.page,
        page_size=pagination.page_size,
        total=total
    )

@router.get("/{assignment_id}", response_model=AssignmentResponse)
async def get_assignment(
    assignment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    # RBAC check
    if current_user.role == UserRole.ADMIN:
        pass  # Admin can see all
    elif current_user.role == UserRole.STAFF and assignment.staff_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    elif current_user.role == UserRole.SUPERVISOR and assignment.supervisor_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return AssignmentResponse.from_orm(assignment)

@router.put("/{assignment_id}", response_model=AssignmentResponse)
async def update_assignment(
    assignment_id: UUID,
    assignment_data: AssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    update_data = assignment_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(assignment, field, value)
    
    db.commit()
    db.refresh(assignment)
    
    return AssignmentResponse.from_orm(assignment)

@router.delete("/{assignment_id}")
async def delete_assignment(
    assignment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    db.delete(assignment)
    db.commit()
    
    return {"message": "Assignment deleted successfully"}

# Staff endpoints
@router.get("/my/assignments", response_model=PaginatedResponse)
async def get_my_assignments(
    pagination: PaginationParams = Depends(),
    status: Optional[str] = None,
    period_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    query = db.query(Assignment).filter(Assignment.staff_user_id == current_user.id)
    
    if status:
        query = query.filter(Assignment.status == status)
    if period_id:
        query = query.filter(Assignment.period_id == period_id)
    else:
        # Default to active period
        active_period = db.query(Period).filter(Period.status == PeriodStatus.ACTIVE).first()
        if active_period:
            query = query.filter(Assignment.period_id == active_period.id)
    
    total = query.count()
    assignments = query.offset((pagination.page - 1) * pagination.page_size).limit(pagination.page_size).all()
    
    return PaginatedResponse(
        items=[AssignmentResponse.from_orm(assignment) for assignment in assignments],
        page=pagination.page,
        page_size=pagination.page_size,
        total=total
    )

@router.post("/my/assignments/{assignment_id}/clean")
async def clean_assignment(
    assignment_id: UUID,
    request: AssignmentCleanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    if assignment.staff_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    if assignment.status not in [AssignmentStatus.PENDING, AssignmentStatus.REJECTED]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Assignment status is not suitable for cleaning"
        )
    
    assignment.status = AssignmentStatus.CLEANED
    assignment.staff_completed_at = datetime.utcnow()
    if request.staff_notes:
        assignment.staff_notes = request.staff_notes
    
    db.commit()
    
    return {"message": "Assignment marked as cleaned successfully"}

# Supervisor endpoints
@router.get("/my/reviews", response_model=PaginatedResponse)
async def get_my_reviews(
    pagination: PaginationParams = Depends(),
    status: str = AssignmentStatus.CLEANED,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_supervisor)
):
    query = db.query(Assignment).filter(
        Assignment.supervisor_user_id == current_user.id,
        Assignment.status == status
    )
    
    total = query.count()
    assignments = query.offset((pagination.page - 1) * pagination.page_size).limit(pagination.page_size).all()
    
    return PaginatedResponse(
        items=[AssignmentResponse.from_orm(assignment) for assignment in assignments],
        page=pagination.page,
        page_size=pagination.page_size,
        total=total
    )

@router.post("/my/reviews/{assignment_id}/approve")
async def approve_assignment(
    assignment_id: UUID,
    request: AssignmentApproveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_supervisor)
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    if assignment.supervisor_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    if assignment.status != AssignmentStatus.CLEANED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Assignment must be in cleaned status to approve"
        )
    
    assignment.status = AssignmentStatus.APPROVED
    assignment.supervisor_reviewed_at = datetime.utcnow()
    if request.rating:
        assignment.rating = request.rating
    if request.supervisor_notes:
        assignment.supervisor_notes = request.supervisor_notes
    
    db.commit()
    
    return {"message": "Assignment approved successfully"}

@router.post("/my/reviews/{assignment_id}/reject")
async def reject_assignment(
    assignment_id: UUID,
    request: AssignmentRejectRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_supervisor)
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    if assignment.supervisor_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    if assignment.status != AssignmentStatus.CLEANED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Assignment must be in cleaned status to reject"
        )
    
    assignment.status = AssignmentStatus.REJECTED
    assignment.supervisor_reviewed_at = datetime.utcnow()
    assignment.rejection_reason = request.rejection_reason
    
    db.commit()
    
    return {"message": "Assignment rejected successfully"}
