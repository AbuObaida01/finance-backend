from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserResponse
from app.models.user import RoleEnum, User
from app.core.dependencies import require_role
from app.services import user_service
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["User Management"])

class RoleUpdatePayload(BaseModel):
    role: RoleEnum

# All endpoints here are admin only
@router.get("/", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.admin]))
):
    return user_service.get_all_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.admin]))
):
    return user_service.get_user_by_id(db, user_id)


@router.patch("/{user_id}/role", response_model=UserResponse)
def update_role(
    user_id: int,
    payload: RoleUpdatePayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.admin]))
):
    return user_service.update_user_role(db, user_id, payload.role)


@router.patch("/{user_id}/toggle-status", response_model=UserResponse)
def toggle_status(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.admin]))
):
    return user_service.toggle_user_status(db, user_id)