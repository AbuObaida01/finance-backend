from fastapi import FastAPI
from app.api.v1 import auth, records, users, dashboard
from app.db.base import Base
from app.db.session import engine
import app.models.user
import app.models.records

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Finance Dashboard API",
    description="Role-based finance data management system for Zorvyn FinTech",
    version="1.0.0"
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(records.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Finance Dashboard API is running"}