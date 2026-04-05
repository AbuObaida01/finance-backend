from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.db.session import get_db
from app.schemas.record import RecordCreate, RecordUpdate, RecordResponse
from app.models.records import RecordTypeEnum
from app.models.user import RoleEnum, User
from app.core.dependencies import get_current_user, require_role
from app.services import record_service

router = APIRouter(prefix="/records", tags=["Financial Records"])

# Anyone logged in can view records
@router.get("/", response_model=list[RecordResponse])
def list_records(
    record_type: Optional[RecordTypeEnum] = Query(None),
    category: Optional[str] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return record_service.get_records(db, record_type, category, date_from, date_to, skip, limit)


@router.get("/{record_id}", response_model=RecordResponse)
def get_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return record_service.get_record_by_id(db, record_id)


# Only admin can create, update, delete
@router.post("/", response_model=RecordResponse, status_code=201)
def create_record(
    payload: RecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.admin]))
):
    return record_service.create_record(db, payload, current_user.id)


@router.put("/{record_id}", response_model=RecordResponse)
def update_record(
    record_id: int,
    payload: RecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.admin]))
):
    return record_service.update_record(db, record_id, payload)


@router.delete("/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.admin]))
):
    return record_service.delete_record(db, record_id)