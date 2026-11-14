import re
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator
from app.schemas.common import VALID_BLOOD_TYPES

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class DonorBase(BaseModel):
    full_name: str
    email: str
    blood_type: str
    city_zone_id: int

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        clean = v.strip()
        if not EMAIL_REGEX.match(clean):
            raise ValueError("Field 'email' must be a valid email address.")
        return clean

    @field_validator("blood_type")
    @classmethod
    def validate_blood_type(cls, v: str) -> str:
        clean = v.strip().upper()
        if clean not in VALID_BLOOD_TYPES:
            raise ValueError("Field 'blood_type' must be one of: A+, A-, B+, B-, AB+, AB-, O+, O-.")
        return clean


class DonorCreate(DonorBase):
    pass


class DonorUpdate(BaseModel):
    is_available: Optional[bool] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    blood_type: Optional[str] = None
    city_zone_id: Optional[int] = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        clean = v.strip()
        if not EMAIL_REGEX.match(clean):
            raise ValueError("Field 'email' must be a valid email address.")
        return clean

    @field_validator("blood_type")
    @classmethod
    def validate_blood_type(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        clean = v.strip().upper()
        if clean not in VALID_BLOOD_TYPES:
            raise ValueError("Field 'blood_type' must be one of: A+, A-, B+, B-, AB+, AB-, O+, O-.")
        return clean


class DonorResponse(BaseModel):
    id: int
    full_name: str
    email: str
    blood_type: str
    city_zone_id: int
    is_available: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
