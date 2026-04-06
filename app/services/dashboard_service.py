from sqlalchemy.orm import Session
from sqlalchemy import func, extract, case
from app.models.records import FinancialRecord, RecordTypeEnum
from datetime import datetime
from typing import Optional


def get_summary(db: Session) -> dict:
    results = db.query(
        func.sum(
            case((FinancialRecord.record_type == RecordTypeEnum.income, FinancialRecord.amount), else_=0)
        ).label("total_income"),
        func.sum(
            case((FinancialRecord.record_type == RecordTypeEnum.expense, FinancialRecord.amount), else_=0)
        ).label("total_expenses"),
        func.count(FinancialRecord.id).label("total_records")
    ).filter(FinancialRecord.is_deleted == False).one()

    total_income = results.total_income or 0
    total_expenses = results.total_expenses or 0

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net_balance": round(total_income - total_expenses, 2),
        "total_records": results.total_records
    }


def get_category_breakdown(db: Session) -> list[dict]:
    results = db.query(
        FinancialRecord.category,
        FinancialRecord.record_type,
        func.sum(FinancialRecord.amount).label("total"),
        func.count(FinancialRecord.id).label("count")
    ).filter(
        FinancialRecord.is_deleted == False
    ).group_by(
        FinancialRecord.category,
        FinancialRecord.record_type
    ).order_by(
        func.sum(FinancialRecord.amount).desc()
    ).all()

    return [
        {
            "category": row.category,
            "record_type": row.record_type,
            "total": round(row.total, 2),
            "count": row.count
        }
        for row in results
    ]


def get_monthly_trends(db: Session, year: Optional[int] = None) -> list[dict]:
    if not year:
        year = datetime.utcnow().year

    results = db.query(
        extract("month", FinancialRecord.date).label("month"),
        func.sum(
            case((FinancialRecord.record_type == RecordTypeEnum.income, FinancialRecord.amount), else_=0)
        ).label("income"),
        func.sum(
            case((FinancialRecord.record_type == RecordTypeEnum.expense, FinancialRecord.amount), else_=0)
        ).label("expenses"),
        func.count(FinancialRecord.id).label("count")
    ).filter(
        FinancialRecord.is_deleted == False,
        extract("year", FinancialRecord.date) == year
    ).group_by(
        extract("month", FinancialRecord.date)
    ).order_by(
        extract("month", FinancialRecord.date)
    ).all()

    month_names = [
        "", "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    return [
        {
            "month": month_names[int(row.month)],
            "month_number": int(row.month),
            "income": round(row.income or 0, 2),
            "expenses": round(row.expenses or 0, 2),
            "net": round((row.income or 0) - (row.expenses or 0), 2),
            "count": row.count
        }
        for row in results
    ]


def get_weekly_trends(db: Session) -> list[dict]:
    results = db.query(
        extract("week", FinancialRecord.date).label("week"),
        extract("year", FinancialRecord.date).label("year"),
        func.sum(
            case((FinancialRecord.record_type == RecordTypeEnum.income, FinancialRecord.amount), else_=0)
        ).label("income"),
        func.sum(
            case((FinancialRecord.record_type == RecordTypeEnum.expense, FinancialRecord.amount), else_=0)
        ).label("expenses"),
    ).filter(
        FinancialRecord.is_deleted == False
    ).group_by(
        extract("year", FinancialRecord.date),
        extract("week", FinancialRecord.date)
    ).order_by(
        extract("year", FinancialRecord.date).desc(),
        extract("week", FinancialRecord.date).desc()
    ).limit(8).all()

    return [
        {
            "year": int(row.year),
            "week": int(row.week),
            "income": round(row.income or 0, 2),
            "expenses": round(row.expenses or 0, 2),
            "net": round((row.income or 0) - (row.expenses or 0), 2),
        }
        for row in results
    ]


def get_recent_activity(db: Session, limit: int = 10) -> list[dict]:
    records = db.query(FinancialRecord).filter(
        FinancialRecord.is_deleted == False
    ).order_by(
        FinancialRecord.created_at.desc()
    ).limit(limit).all()

    return [
        {
            "id": r.id,
            "amount": r.amount,
            "record_type": r.record_type,
            "category": r.category,
            "date": r.date,
            "notes": r.notes
        }
        for r in records
    ]


def get_top_categories(db: Session, record_type: Optional[RecordTypeEnum] = None, top_n: int = 5) -> list[dict]:
    query = db.query(
        FinancialRecord.category,
        func.sum(FinancialRecord.amount).label("total"),
        func.count(FinancialRecord.id).label("count")
    ).filter(FinancialRecord.is_deleted == False)

    if record_type:
        query = query.filter(FinancialRecord.record_type == record_type)

    results = query.group_by(
        FinancialRecord.category
    ).order_by(
        func.sum(FinancialRecord.amount).desc()
    ).limit(top_n).all()

    return [
        {
            "category": row.category,
            "total": round(row.total, 2),
            "count": row.count
        }
        for row in results
    ]