from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ShortageRequest(Base):
    """Urgent shortage request triggered by a hospital."""
    __tablename__ = "shortage_requests"

    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False)
    blood_type = Column(String(5), nullable=False, index=True)
    units_needed = Column(Integer, nullable=False)
    urgency = Column(String(20), nullable=False, index=True)  # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String(20), default="OPEN", nullable=False)  # OPEN, IN_PROGRESS, RESOLVED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    hospital = relationship("Hospital", back_populates="shortages")
    alerts = relationship("Alert", back_populates="shortage_request", cascade="all, delete-orphan")
