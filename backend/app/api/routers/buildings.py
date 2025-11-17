from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.base import get_db
from app.db.models.user import User
from app.db.models.building import Building
from app.schemas.building import BuildingCreate, BuildingUpdate, BuildingResponse
from app.schemas.common import PaginationParams, PaginatedResponse
from app.api.deps import require_admin

router = APIRouter()

@router.get("/", response_model=PaginatedResponse)
async def get_buildings(
    pagination: PaginationParams = Depends(),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    query = db.query(Building)
    
    if search:
        query = query.filter(Building.name.ilike(f"%{search}%"))
    
    total = query.count()
    buildings = query.offset((pagination.page - 1) * pagination.page_size).limit(pagination.page_size).all()
    
    return PaginatedResponse(
        items=[BuildingResponse.from_orm(building) for building in buildings],
        page=pagination.page,
        page_size=pagination.page_size,
        total=total
    )

@router.post("/", response_model=BuildingResponse)
async def create_building(
    building_data: BuildingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    # Check if name already exists
    existing_building = db.query(Building).filter(Building.name == building_data.name).first()
    if existing_building:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Building name already exists"
        )
    
    db_building = Building(**building_data.dict())
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    
    return BuildingResponse.from_orm(db_building)

@router.get("/{building_id}", response_model=BuildingResponse)
async def get_building(
    building_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    building = db.query(Building).filter(Building.id == building_id).first()
    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )
    return BuildingResponse.from_orm(building)

@router.put("/{building_id}", response_model=BuildingResponse)
async def update_building(
    building_id: str,
    building_data: BuildingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    building = db.query(Building).filter(Building.id == building_id).first()
    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )
    
    update_data = building_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(building, field, value)
    
    db.commit()
    db.refresh(building)
    
    return BuildingResponse.from_orm(building)

@router.delete("/{building_id}")
async def delete_building(
    building_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    building = db.query(Building).filter(Building.id == building_id).first()
    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )
    
    db.delete(building)
    db.commit()
    
    return {"message": "Building deleted successfully"}
