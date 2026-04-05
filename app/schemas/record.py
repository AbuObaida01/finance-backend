from pydantic import BaseModel, field_validator
from app.models.records import RecordTypeEnum
from datetime import datetime
from typing import Optional

class RecordCreate(BaseModel):
    amount: float
    record_type: RecordTypeEnum
    category: str
    date: datetime
    description: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than zero")
        return v

    @field_validator("category")
    @classmethod
    def category_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Category cannot be empty")
        return v.strip()

class RecordUpdate(BaseModel):
    amount: Optional[float] = None
    record_type: Optional[RecordTypeEnum] = None
    category: Optional[str] = None
    date: Optional[datetime] = None
    description: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Amount must be greater than zero")
        return v

class RecordResponse(BaseModel):
    id: int
    amount: float
    record_type: RecordTypeEnum
    category: str
    date: datetime
    description: Optional[str]
    is_deleted: bool
    created_at: datetime
    created_by: int

    class Config:
        from_attributes = True