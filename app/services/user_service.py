from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User, RoleEnum
from app.schemas.user import UserRegister
from app.core.security import hash_password

def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_user_role(db: Session, user_id: int, role: RoleEnum) -> User:
    user = get_user_by_id(db, user_id)
    user.role = role
    db.commit()
    db.refresh(user)
    return user

def toggle_user_status(db: Session, user_id: int) -> User:
    user = get_user_by_id(db, user_id)
    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)
    return user