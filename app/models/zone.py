from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Zone(Base):
    """City zone representation for geographic proximity matching."""
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    code = Column(String(20), nullable=False, unique=True)

    donors = relationship("Donor", back_populates="zone", cascade="all, delete-orphan")
    hospitals = relationship("Hospital", back_populates="zone", cascade="all, delete-orphan")
    blood_banks = relationship("BloodBank", back_populates="zone", cascade="all, delete-orphan")
