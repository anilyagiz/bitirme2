from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.db.base import get_db
from app.db.models.user import User
from app.db.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.schemas.common import PaginationParams, PaginatedResponse
from app.api.deps import require_admin

router = APIRouter()

@router.get("/", response_model=PaginatedResponse)
async def get_departments(
    pagination: PaginationParams = Depends(),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    query = db.query(Department)
    
    if search:
        query = query.filter(Department.name.ilike(f"%{search}%"))
    
    total = query.count()
    departments = query.offset((pagination.page - 1) * pagination.page_size).limit(pagination.page_size).all()
    
    return PaginatedResponse(
        items=[DepartmentResponse.from_orm(department) for department in departments],
        page=pagination.page,
        page_size=pagination.page_size,
        total=total
    )

@router.post("/", response_model=DepartmentResponse)
async def create_department(
    department_data: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    existing_department = db.query(Department).filter(Department.name == department_data.name).first()
    if existing_department:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Department name already exists"
        )
    
    db_department = Department(**department_data.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    
    return DepartmentResponse.from_orm(db_department)

@router.get("/{department_id}", response_model=DepartmentResponse)
async def get_department(
    department_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    return DepartmentResponse.from_orm(department)

@router.put("/{department_id}", response_model=DepartmentResponse)
async def update_department(
    department_id: UUID,
    department_data: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    update_data = department_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(department, field, value)
    
    db.commit()
    db.refresh(department)
    
    return DepartmentResponse.from_orm(department)

@router.delete("/{department_id}")
async def delete_department(
    department_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    db.delete(department)
    db.commit()
    
    return {"message": "Department deleted successfully"}
