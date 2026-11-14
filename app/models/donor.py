from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Donor(Base):
    """Registered voluntary blood donor."""
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    blood_type = Column(String(5), nullable=False, index=True)
    city_zone_id = Column(Integer, ForeignKey("zones.id"), nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    zone = relationship("Zone", back_populates="donors")
    alerts = relationship("Alert", back_populates="donor", cascade="all, delete-orphan")
