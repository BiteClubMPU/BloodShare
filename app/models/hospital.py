from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Hospital(Base):
    """Hospital entity that generates blood shortage requests."""
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=False)

    zone = relationship("Zone", back_populates="hospitals")
    shortages = relationship("ShortageRequest", back_populates="hospital", cascade="all, delete-orphan")
