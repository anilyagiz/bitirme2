from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Text, Enum, SmallInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.db.base import Base

class AssignmentStatus(str, enum.Enum):
    PENDING = "pending"
    CLEANED = "cleaned"
    APPROVED = "approved"
    REJECTED = "rejected"

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=False)
    period_id = Column(UUID(as_uuid=True), ForeignKey("periods.id"), nullable=False)
    staff_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    supervisor_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(Enum(AssignmentStatus), default=AssignmentStatus.PENDING, nullable=False)
    staff_notes = Column(Text, nullable=True)
    supervisor_notes = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    rating = Column(SmallInteger, nullable=True)  # 1-5
    staff_completed_at = Column(DateTime(timezone=True), nullable=True)
    supervisor_reviewed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    location = relationship("Location", back_populates="assignments")
    period = relationship("Period", back_populates="assignments")
    staff_user = relationship("User", foreign_keys=[staff_user_id])
    supervisor_user = relationship("User", foreign_keys=[supervisor_user_id])
