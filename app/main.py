from fastapi import FastAPI
from app.api.v1 import auth
from app.db.base import Base
from app.db.session import engine
import app.models.user
import app.models.records

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Finance Dashboard API",
    description="Role-based finance data management system",
    version="1.0.0"
)

app.include_router(auth.router, prefix="/api/v1")