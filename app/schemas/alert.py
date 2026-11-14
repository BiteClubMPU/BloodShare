from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from app.schemas.common import VALID_CHANNELS, VALID_ALERT_STATUSES


class AlertSendRequest(BaseModel):
    shortage_request_id: int
    channel: str

    @field_validator("channel")
    @classmethod
    def validate_channel(cls, v: str) -> str:
        clean = v.strip().upper()
        if clean not in VALID_CHANNELS:
            raise ValueError(f"Field 'channel' must be one of: {', '.join(VALID_CHANNELS)}.")
        return clean


class AlertStatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        clean = v.strip().upper()
        if clean not in VALID_ALERT_STATUSES:
            raise ValueError(f"Field 'status' must be one of: {', '.join(VALID_ALERT_STATUSES)}.")
        return clean


class AlertResponse(BaseModel):
    id: int
    shortage_request_id: int
    donor_id: Optional[int]
    channel: str
    status: str
    message: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AlertDispatchResponse(BaseModel):
    shortage_request_id: int
    channel: str
    notifications_dispatched: int
    matched_zone_id: int
    blood_type: str
    alerts: List[AlertResponse]
    message: str
