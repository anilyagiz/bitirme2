from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base

class LocationType(str, enum.Enum):
    DERSLIK = "derslik"
    OFIS = "ofis"
    TUVALET = "tuvalet"
    KORIDOR = "koridor"
    DIGER = "diger"

class Location(Base):
    __tablename__ = "locations"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location_type = Column(Enum(LocationType), nullable=False)
    location_subtype = Column(String, nullable=True)
    building_id = Column(String, ForeignKey("buildings.id"), nullable=False)
    department_id = Column(String, ForeignKey("departments.id"), nullable=True)
    parent_location_id = Column(String, ForeignKey("locations.id"), nullable=True)
    is_leaf = Column(Boolean, default=True, nullable=False)
    floor_label = Column(String, nullable=True)
    area_sqm = Column(Integer, nullable=True)
    special_instructions = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    building = relationship("Building", back_populates="locations")
    department = relationship("Department", back_populates="locations")
    parent_location = relationship("Location", remote_side=[id])
    child_locations = relationship("Location", back_populates="parent_location")
    assignments = relationship("Assignment", back_populates="location")
