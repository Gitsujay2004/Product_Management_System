from fastapi import APIRouter
from sqlalchemy import text

from app.database.session import engine
from app.core.metrics import metrics


router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("")
async def health_check():
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "healthy"
        }

    except Exception:
        return {
            "status": "unhealthy",
            "database": "unhealthy"
        }


@router.get("/liveness")
async def liveness_check():
    return {
        "status": "alive"
    }


@router.get("/readiness")
async def readiness_check():
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))

        return {
            "status": "ready",
            "database": "ready"
        }

    except Exception:
        return {
            "status": "not_ready",
            "database": "unavailable"
        }


@router.get("/metrics")
async def get_metrics():
    return metrics.get_metrics()