from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.hospital import Hospital
from app.models.blood_bank import BloodBank
from app.models.inventory import InventoryItem
from app.models.shortage import ShortageRequest
from app.schemas.shortage import ShortageCreate, ShortageResponse
from app.schemas.inventory import InventoryUpdate, InventoryResponse
from app.schemas.common import VALID_BLOOD_TYPES, VALID_URGENCIES

router = APIRouter(prefix="/inventory", tags=["Inventory & Shortages"])


@router.get("/shortages", response_model=List[ShortageResponse])
def get_shortages(
    blood_type: Optional[str] = Query(None, description="Filter by blood type (e.g. A+, O-)"),
    zone_id: Optional[int] = Query(None, description="Filter by hospital city zone ID"),
    urgency: Optional[str] = Query(None, description="Filter by urgency (LOW, MEDIUM, HIGH, CRITICAL)"),
    db: Session = Depends(get_db),
):
    """Retrieves a filtered list of current blood shortages across hospitals."""
    query = db.query(ShortageRequest).join(Hospital)

    if blood_type is not None:
        clean_bt = blood_type.strip().upper()
        if clean_bt not in VALID_BLOOD_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Field 'blood_type' must be one of: {', '.join(VALID_BLOOD_TYPES)}.",
            )
        query = query.filter(ShortageRequest.blood_type == clean_bt)

    if urgency is not None:
        clean_urg = urgency.strip().upper()
        if clean_urg not in VALID_URGENCIES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Field 'urgency' must be one of: {', '.join(VALID_URGENCIES)}.",
            )
        query = query.filter(ShortageRequest.urgency == clean_urg)

    if zone_id is not None:
        query = query.filter(Hospital.zone_id == zone_id)

    shortages = query.order_by(ShortageRequest.created_at.desc()).all()

    # Enrich response with hospital name and zone ID
    response = []
    for item in shortages:
        response.append(
            ShortageResponse(
                id=item.id,
                hospital_id=item.hospital_id,
                blood_type=item.blood_type,
                units_needed=item.units_needed,
                urgency=item.urgency,
                status=item.status,
                created_at=item.created_at,
                hospital_name=item.hospital.name if item.hospital else None,
                zone_id=item.hospital.zone_id if item.hospital else None,
            )
        )
    return response


@router.post("/shortages", response_model=ShortageResponse, status_code=status.HTTP_201_CREATED)
def create_shortage(payload: ShortageCreate, db: Session = Depends(get_db)):
    """Creates a new blood shortage request from a hospital."""
    hospital = db.query(Hospital).filter(Hospital.id == payload.hospital_id).first()
    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hospital with id {payload.hospital_id} not found.",
        )

    shortage = ShortageRequest(
        hospital_id=payload.hospital_id,
        blood_type=payload.blood_type,
        units_needed=payload.units_needed,
        urgency=payload.urgency,
        status="OPEN",
    )
    db.add(shortage)
    db.commit()
    db.refresh(shortage)

    return ShortageResponse(
        id=shortage.id,
        hospital_id=shortage.hospital_id,
        blood_type=shortage.blood_type,
        units_needed=shortage.units_needed,
        urgency=shortage.urgency,
        status=shortage.status,
        created_at=shortage.created_at,
        hospital_name=hospital.name,
        zone_id=hospital.zone_id,
    )


@router.put("/{blood_bank_id}", response_model=InventoryResponse)
def update_inventory(
    blood_bank_id: int,
    payload: InventoryUpdate,
    db: Session = Depends(get_db),
):
    """Updates the stock level of a blood type in a specific blood bank."""
    blood_bank = db.query(BloodBank).filter(BloodBank.id == blood_bank_id).first()
    if not blood_bank:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blood bank with id {blood_bank_id} not found.",
        )

    item = (
        db.query(InventoryItem)
        .filter(
            InventoryItem.blood_bank_id == blood_bank_id,
            InventoryItem.blood_type == payload.blood_type,
        )
        .first()
    )

    if item:
        item.units_available = payload.units_available
    else:
        item = InventoryItem(
            blood_bank_id=blood_bank_id,
            blood_type=payload.blood_type,
            units_available=payload.units_available,
        )
        db.add(item)

    db.commit()
    db.refresh(item)
    return item


@router.get("/{blood_bank_id}", response_model=List[InventoryResponse])
def get_inventory_by_bank(blood_bank_id: int, db: Session = Depends(get_db)):
    """Retrieves current blood inventory for a specific blood bank."""
    blood_bank = db.query(BloodBank).filter(BloodBank.id == blood_bank_id).first()
    if not blood_bank:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blood bank with id {blood_bank_id} not found.",
        )
    return (
        db.query(InventoryItem)
        .filter(InventoryItem.blood_bank_id == blood_bank_id)
        .order_by(InventoryItem.blood_type)
        .all()
    )
