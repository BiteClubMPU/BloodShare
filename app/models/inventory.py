from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class InventoryItem(Base):
    """Stock level of a specific blood type in a blood bank."""
    __tablename__ = "inventory_items"
    __table_args__ = (
        UniqueConstraint("blood_bank_id", "blood_type", name="uq_blood_bank_blood_type"),
    )

    id = Column(Integer, primary_key=True, index=True)
    blood_bank_id = Column(Integer, ForeignKey("blood_banks.id"), nullable=False)
    blood_type = Column(String(5), nullable=False)
    units_available = Column(Integer, default=0, nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    blood_bank = relationship("BloodBank", back_populates="inventory_items")
