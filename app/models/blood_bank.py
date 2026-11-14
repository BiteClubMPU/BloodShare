from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class BloodBank(Base):
    """Blood bank facility managing local blood inventory."""
    __tablename__ = "blood_banks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=False)

    zone = relationship("Zone", back_populates="blood_banks")
    inventory_items = relationship("InventoryItem", back_populates="blood_bank", cascade="all, delete-orphan")
