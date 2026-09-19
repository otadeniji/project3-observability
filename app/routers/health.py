from fastapi import APIRouter, Depends
from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Alert, Anomaly, LogEntry
from app.schemas import HealthResponse

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health(database: Session = Depends(get_db)) -> HealthResponse:
    database.execute(text("SELECT 1"))
    return HealthResponse(status="healthy", database="connected", log_count=database.scalar(select(func.count()).select_from(LogEntry)) or 0, anomaly_count=database.scalar(select(func.count()).select_from(Anomaly)) or 0, open_alert_count=database.scalar(select(func.count()).select_from(Alert).where(Alert.status == "open")) or 0, last_log_at=database.scalar(select(func.max(LogEntry.timestamp))))