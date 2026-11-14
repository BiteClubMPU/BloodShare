from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.zone import Zone
from app.schemas.zone import ZoneResponse

router = APIRouter(prefix="/zones", tags=["Zones"])


@router.get("", response_model=List[ZoneResponse])
def get_zones(db: Session = Depends(get_db)):
    """List all city zones available for blood logistics."""
    zones = db.query(Zone).order_by(Zone.id).all()
    return zones
