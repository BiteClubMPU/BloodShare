from typing import Literal
from pydantic import BaseModel, Field

VALID_BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
BloodType = Literal["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

VALID_URGENCIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
UrgencyLevel = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]

VALID_CHANNELS = ["SMS", "EMAIL", "PUSH"]
AlertChannel = Literal["SMS", "EMAIL", "PUSH"]

VALID_ALERT_STATUSES = ["SENT", "ACCEPTED", "DECLINED"]
AlertStatus = Literal["SENT", "ACCEPTED", "DECLINED"]


class ErrorResponse(BaseModel):
    status: int = Field(..., json_schema_extra={"example": 400})
    error: str = Field(..., json_schema_extra={"example": "Bad Request"})
    message: str = Field(
        ...,
        json_schema_extra={"example": "Field 'blood_type' must be one of: A+, A-, B+, B-, AB+, AB-, O+, O-."},
    )
    timestamp: str = Field(..., json_schema_extra={"example": "2026-10-29T14:02:00Z"})
