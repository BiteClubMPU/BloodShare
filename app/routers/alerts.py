from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.alert import Alert
from app.models.donor import Donor
from app.models.shortage import ShortageRequest
from app.schemas.alert import (
    AlertSendRequest,
    AlertStatusUpdate,
    AlertResponse,
    AlertDispatchResponse,
)

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.post("/send", response_model=AlertDispatchResponse, status_code=status.HTTP_202_ACCEPTED)
def send_alerts(payload: AlertSendRequest, db: Session = Depends(get_db)):
    """Triggers instant urgent notifications to matching donors in the hospital's city zone."""
    shortage = (
        db.query(ShortageRequest)
        .filter(ShortageRequest.id == payload.shortage_request_id)
        .first()
    )
    if not shortage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shortage request with id {payload.shortage_request_id} not found.",
        )

    hospital = shortage.hospital
    target_zone_id = hospital.zone_id

    # Find available donors in the same city zone with matching blood type
    matching_donors = (
        db.query(Donor)
        .filter(
            Donor.city_zone_id == target_zone_id,
            Donor.blood_type == shortage.blood_type,
            Donor.is_available.is_(True),
        )
        .all()
    )

    created_alerts: List[Alert] = []

    if matching_donors:
        for donor in matching_donors:
            alert = Alert(
                shortage_request_id=shortage.id,
                donor_id=donor.id,
                channel=payload.channel,
                status="SENT",
                message=(
                    f"URGENT: {hospital.name} needs {shortage.units_needed} units of "
                    f"{shortage.blood_type} blood. Urgency: {shortage.urgency}."
                ),
            )
            db.add(alert)
            created_alerts.append(alert)
    else:
        # Create a broadcast alert if no specific registered donor is available yet
        alert = Alert(
            shortage_request_id=shortage.id,
            donor_id=None,
            channel=payload.channel,
            status="SENT",
            message=(
                f"BROADCAST: Urgent need for {shortage.blood_type} at {hospital.name}. "
                f"Zone: {target_zone_id}."
            ),
        )
        db.add(alert)
        created_alerts.append(alert)

    # Transition shortage request status
    shortage.status = "IN_PROGRESS"

    db.commit()
    for alert in created_alerts:
        db.refresh(alert)

    return AlertDispatchResponse(
        shortage_request_id=shortage.id,
        channel=payload.channel,
        notifications_dispatched=len(created_alerts),
        matched_zone_id=target_zone_id,
        blood_type=shortage.blood_type,
        alerts=[AlertResponse.model_validate(a) for a in created_alerts],
        message=f"Successfully dispatched {len(created_alerts)} alert(s) via {payload.channel}.",
    )


@router.get("", response_model=List[AlertResponse])
def get_alerts(
    shortage_id: Optional[int] = Query(None, description="Filter alerts by shortage request ID"),
    donor_id: Optional[int] = Query(None, description="Filter alerts by donor ID"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by alert status"),
    db: Session = Depends(get_db),
):
    """Retrieves all dispatched alerts with optional filtering."""
    query = db.query(Alert)
    if shortage_id is not None:
        query = query.filter(Alert.shortage_request_id == shortage_id)
    if donor_id is not None:
        query = query.filter(Alert.donor_id == donor_id)
    if status_filter is not None:
        query = query.filter(Alert.status == status_filter.upper())
    return query.order_by(Alert.created_at.desc()).all()


@router.get("/{id}", response_model=AlertResponse)
def get_alert(id: int, db: Session = Depends(get_db)):
    """Retrieves the status and details of a single alert."""
    alert = db.query(Alert).filter(Alert.id == id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert with id {id} not found.",
        )
    return alert


@router.patch("/{id}", response_model=AlertResponse)
def update_alert_status(
    id: int,
    payload: AlertStatusUpdate,
    db: Session = Depends(get_db),
):
    """Lets a donor accept or decline an urgent blood alert."""
    alert = db.query(Alert).filter(Alert.id == id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert with id {id} not found.",
        )

    alert.status = payload.status
    db.commit()
    db.refresh(alert)
    return alert
