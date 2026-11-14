from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.schemas.common import VALID_BLOOD_TYPES


class InventoryUpdate(BaseModel):
    blood_type: str
    units_available: int = Field(..., ge=0)

    @field_validator("blood_type")
    @classmethod
    def validate_blood_type(cls, v: str) -> str:
        clean = v.strip().upper()
        if clean not in VALID_BLOOD_TYPES:
            raise ValueError("Field 'blood_type' must be one of: A+, A-, B+, B-, AB+, AB-, O+, O-.")
        return clean


class InventoryResponse(BaseModel):
    id: int
    blood_bank_id: int
    blood_type: str
    units_available: int
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
