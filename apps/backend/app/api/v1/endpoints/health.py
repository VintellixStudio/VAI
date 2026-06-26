from fastapi import APIRouter
from sqlalchemy import text

from app.db.database import engine

router = APIRouter()


@router.get("/health")
def health():
    db_status = "connected"

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        db_status = "disconnected"

    return {
        "status": "ok",
        "service": "VAI Backend",
        "database": db_status,
    }