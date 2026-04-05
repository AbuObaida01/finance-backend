from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import func
import enum
from app.db.base import Base

class RecordTypeEnum(str, enum.Enum):
    income = "income"
    expense = "expense"

class FinancialRecord(Base):
    __tablename__ = 'financial_records'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    record_type: Mapped[RecordTypeEnum] = mapped_column(Enum(RecordTypeEnum), nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_at:Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at:Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by: Mapped[int]=mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    is_deleted:Mapped[bool]=mapped_column(Boolean, default=False)
    user = relationship("User", back_populates="financial_records")