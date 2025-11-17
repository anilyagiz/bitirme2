from pydantic import BaseModel, validator
from typing import List

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 20
    
    @validator('page')
    def validate_page(cls, v):
        if v < 1:
            raise ValueError('Page must be >= 1')
        return v
    
    @validator('page_size')
    def validate_page_size(cls, v):
        if v < 1 or v > 100:
            raise ValueError('Page size must be between 1 and 100')
        return v

class PaginatedResponse(BaseModel):
    items: List[dict]
    page: int
    page_size: int
    total: int

class DashboardStats(BaseModel):
    period_id: str
    pending: int
    cleaned: int
    rejected: int
    approved: int
