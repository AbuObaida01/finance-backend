from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.records import FinancialRecord, RecordTypeEnum
from app.schemas.record import RecordCreate, RecordUpdate
from fastapi import HTTPException
from datetime import datetime
from typing import Optional

def create_record(db: Session, payload: RecordCreate, user_id: int) -> FinancialRecord:
    record = FinancialRecord(
        amount=payload.amount,
        record_type=payload.record_type,
        category=payload.category,
        date=payload.date,
        description=payload.description,
        created_by=user_id
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_records(
    db: Session,
    record_type: Optional[RecordTypeEnum] = None,
    category: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 20
) -> list[FinancialRecord]:
    query = db.query(FinancialRecord).filter(FinancialRecord.is_deleted == False)

    if record_type:
        query = query.filter(FinancialRecord.record_type == record_type)
    if category:
        query = query.filter(FinancialRecord.category.ilike(f"%{category}%"))
    if date_from:
        query = query.filter(FinancialRecord.date >= date_from)
    if date_to:
        query = query.filter(FinancialRecord.date <= date_to)

    return query.order_by(FinancialRecord.date.desc()).offset(skip).limit(limit).all()


def get_record_by_id(db: Session, record_id: int) -> FinancialRecord:
    record = db.query(FinancialRecord).filter(
        FinancialRecord.id == record_id,
        FinancialRecord.is_deleted == False
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


def update_record(db: Session, record_id: int, payload: RecordUpdate) -> FinancialRecord:
    record = get_record_by_id(db, record_id)

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)

    record.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(record)
    return record


def delete_record(db: Session, record_id: int) -> dict:
    record = get_record_by_id(db, record_id)
    record.is_deleted = True
    db.commit()
    return {"detail": "Record deleted successfully"}