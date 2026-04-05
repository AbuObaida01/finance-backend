from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
import enum
from app.db.base import Base

class RoleEnum(str, enum.Enum):
    viewer="viewer"
    analyst="analyst"
    admin="admin"


class User(Base):
    __tablename__='users'
    id:Mapped[int]=mapped_column(Integer, primary_key=True, nullable=False)
    first_name:Mapped[str]=mapped_column(String, nullable=False)
    last_name:Mapped[str]=mapped_column(String, nullable=False)
    email:Mapped[str]=mapped_column(String, unique=True, nullable=False, index=True)
    hashed_password:Mapped[str]=mapped_column(String, nullable=False)
    role:Mapped[RoleEnum]=mapped_column(Enum(RoleEnum),default=RoleEnum.viewer, nullable=False)
    is_active:Mapped[bool]=mapped_column(Boolean, default=True)
    created_at:Mapped[DateTime]=mapped_column(TIMESTAMP(timezone=True),server_default=func.now(), nullable=False)

    financial_records = relationship("FinancialRecord", back_populates="user")