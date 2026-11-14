from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.donor import Donor
from app.models.zone import Zone
from app.schemas.donor import DonorCreate, DonorUpdate, DonorResponse
from app.schemas.common import VALID_BLOOD_TYPES

router = APIRouter(prefix="/donors", tags=["Donors"])


@router.post("", response_model=DonorResponse, status_code=status.HTTP_201_CREATED)
def register_donor(payload: DonorCreate, db: Session = Depends(get_db)):
    """Registers a new voluntary donor in a specific city zone."""
    # Check if zone exists
    zone = db.query(Zone).filter(Zone.id == payload.city_zone_id).first()
    if not zone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Zone with id {payload.city_zone_id} does not exist.",
        )

    # Check email uniqueness
    existing_donor = db.query(Donor).filter(Donor.email == payload.email).first()
    if existing_donor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Donor with email '{payload.email}' already exists.",
        )

    donor = Donor(
        full_name=payload.full_name,
        email=payload.email,
        blood_type=payload.blood_type,
        city_zone_id=payload.city_zone_id,
        is_available=True,
    )
    db.add(donor)
    db.commit()
    db.refresh(donor)
    return donor


@router.get("", response_model=List[DonorResponse])
def get_donors(
    blood_type: Optional[str] = Query(None, description="Filter by blood type (e.g. O+, A-)"),
    zone_id: Optional[int] = Query(None, description="Filter by city zone ID"),
    available: Optional[bool] = Query(None, description="Filter by availability status"),
    db: Session = Depends(get_db),
):
    """Searches registered donors by blood type, city zone, and availability."""
    query = db.query(Donor)

    if blood_type is not None:
        clean_bt = blood_type.strip().upper()
        if clean_bt not in VALID_BLOOD_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Field 'blood_type' must be one of: {', '.join(VALID_BLOOD_TYPES)}.",
            )
        query = query.filter(Donor.blood_type == clean_bt)

    if zone_id is not None:
        query = query.filter(Donor.city_zone_id == zone_id)

    if available is not None:
        query = query.filter(Donor.is_available == available)

    return query.order_by(Donor.id).all()


@router.get("/{id}", response_model=DonorResponse)
def get_donor(id: int, db: Session = Depends(get_db)):
    """Retrieves a single donor by their unique ID."""
    donor = db.query(Donor).filter(Donor.id == id).first()
    if not donor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Donor with id {id} not found.",
        )
    return donor


@router.patch("/{id}", response_model=DonorResponse)
def update_donor(id: int, payload: DonorUpdate, db: Session = Depends(get_db)):
    """Updates donor data or availability status."""
    donor = db.query(Donor).filter(Donor.id == id).first()
    if not donor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Donor with id {id} not found.",
        )

    if payload.city_zone_id is not None:
        zone = db.query(Zone).filter(Zone.id == payload.city_zone_id).first()
        if not zone:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Zone with id {payload.city_zone_id} does not exist.",
            )
        donor.city_zone_id = payload.city_zone_id

    if payload.email is not None and payload.email != donor.email:
        conflict = db.query(Donor).filter(Donor.email == payload.email).first()
        if conflict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Donor with email '{payload.email}' already exists.",
            )
        donor.email = payload.email

    if payload.full_name is not None:
        donor.full_name = payload.full_name

    if payload.blood_type is not None:
        donor.blood_type = payload.blood_type

    if payload.is_available is not None:
        donor.is_available = payload.is_available

    db.commit()
    db.refresh(donor)
    return donor


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_donor(id: int, db: Session = Depends(get_db)):
    """Removes a donor record (completing the full CRUD lifecycle)."""
    donor = db.query(Donor).filter(Donor.id == id).first()
    if not donor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Donor with id {id} not found.",
        )
    db.delete(donor)
    db.commit()
    return {"message": f"Donor with id {id} successfully deleted."}
