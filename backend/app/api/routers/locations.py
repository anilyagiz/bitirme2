from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.db.base import get_db
from app.db.models.user import User
from app.db.models.location import Location
from app.schemas.location import LocationCreate, LocationUpdate, LocationResponse
from app.schemas.common import PaginationParams, PaginatedResponse
from app.api.deps import require_admin

router = APIRouter()

@router.get("/", response_model=PaginatedResponse)
async def get_locations(
    pagination: PaginationParams = Depends(),
    building_id: Optional[str] = None,
    department_id: Optional[str] = None,
    is_leaf: Optional[bool] = None,
    location_type: Optional[str] = None,
    active: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    query = db.query(Location)
    
    if building_id:
        query = query.filter(Location.building_id == building_id)
    if department_id:
        query = query.filter(Location.department_id == department_id)
    if is_leaf is not None:
        query = query.filter(Location.is_leaf == is_leaf)
    if location_type:
        query = query.filter(Location.location_type == location_type)
    if active is not None:
        query = query.filter(Location.is_active == active)
    if search:
        query = query.filter(Location.name.ilike(f"%{search}%"))
    
    total = query.count()
    locations = query.offset((pagination.page - 1) * pagination.page_size).limit(pagination.page_size).all()
    
    return PaginatedResponse(
        items=[LocationResponse.from_orm(location) for location in locations],
        page=pagination.page,
        page_size=pagination.page_size,
        total=total
    )

@router.post("/", response_model=LocationResponse)
async def create_location(
    location_data: LocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    # Validate parent_location_id if provided
    if location_data.parent_location_id:
        parent = db.query(Location).filter(Location.id == location_data.parent_location_id).first()
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent location not found"
            )
        if parent.is_leaf:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent location must not be a leaf"
            )
    
    db_location = Location(**location_data.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    
    return LocationResponse.from_orm(db_location)

@router.get("/{location_id}", response_model=LocationResponse)
async def get_location(
    location_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
    return LocationResponse.from_orm(location)

@router.put("/{location_id}", response_model=LocationResponse)
async def update_location(
    location_id: UUID,
    location_data: LocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
    
    update_data = location_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(location, field, value)
    
    db.commit()
    db.refresh(location)
    
    return LocationResponse.from_orm(location)

@router.delete("/{location_id}")
async def delete_location(
    location_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
    
    db.delete(location)
    db.commit()
    
    return {"message": "Location deleted successfully"}
