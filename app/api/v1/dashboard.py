from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.models.records import RecordTypeEnum
from app.models.user import RoleEnum, User
from app.core.dependencies import get_current_user, require_role
from app.services import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# Viewers and above can see summary
@router.get("/summary")
def summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return dashboard_service.get_summary(db)


# Viewers and above can see category breakdown
@router.get("/category-breakdown")
def category_breakdown(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return dashboard_service.get_category_breakdown(db)


# Viewers and above can see recent activity
@router.get("/recent-activity")
def recent_activity(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return dashboard_service.get_recent_activity(db, limit)


# Analyst and admin only — deeper insights
@router.get("/monthly-trends")
def monthly_trends(
    year: Optional[int] = Query(None, description="Year to filter by, defaults to current year"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.analyst, RoleEnum.admin]))
):
    return dashboard_service.get_monthly_trends(db, year)


@router.get("/weekly-trends")
def weekly_trends(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.analyst, RoleEnum.admin]))
):
    return dashboard_service.get_weekly_trends(db)


@router.get("/top-categories")
def top_categories(
    record_type: Optional[RecordTypeEnum] = Query(None),
    top_n: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.analyst, RoleEnum.admin]))
):
    return dashboard_service.get_top_categories(db, record_type, top_n)