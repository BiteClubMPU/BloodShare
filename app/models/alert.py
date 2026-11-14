from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Alert(Base):
    """Notification sent to a matching donor for a blood shortage."""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    shortage_request_id = Column(Integer, ForeignKey("shortage_requests.id"), nullable=False)
    donor_id = Column(Integer, ForeignKey("donors.id"), nullable=True)
    channel = Column(String(20), nullable=False)  # SMS, EMAIL, PUSH
    status = Column(String(20), default="SENT", nullable=False)  # SENT, ACCEPTED, DECLINED
    message = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    shortage_request = relationship("ShortageRequest", back_populates="alerts")
    donor = relationship("Donor", back_populates="alerts")
