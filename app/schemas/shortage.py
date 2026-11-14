from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.schemas.common import VALID_BLOOD_TYPES, VALID_URGENCIES


class ShortageCreate(BaseModel):
    hospital_id: int
    blood_type: str
    units_needed: int = Field(..., gt=0)
    urgency: str

    @field_validator("blood_type")
    @classmethod
    def validate_blood_type(cls, v: str) -> str:
        clean = v.strip().upper()
        if clean not in VALID_BLOOD_TYPES:
            raise ValueError("Field 'blood_type' must be one of: A+, A-, B+, B-, AB+, AB-, O+, O-.")
        return clean

    @field_validator("urgency")
    @classmethod
    def validate_urgency(cls, v: str) -> str:
        clean = v.strip().upper()
        if clean not in VALID_URGENCIES:
            raise ValueError(f"Field 'urgency' must be one of: {', '.join(VALID_URGENCIES)}.")
        return clean


class ShortageResponse(BaseModel):
    id: int
    hospital_id: int
    blood_type: str
    units_needed: int
    urgency: str
    status: str
    created_at: datetime
    hospital_name: Optional[str] = None
    zone_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
