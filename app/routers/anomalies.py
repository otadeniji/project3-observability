from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Anomaly
from app.schemas import AnomalyResponse

router = APIRouter(prefix="/api/anomalies", tags=["anomalies"])


@router.get("", response_model=list[AnomalyResponse])
def list_anomalies(limit: int = Query(100, ge=1, le=500), database: Session = Depends(get_db)) -> list[Anomaly]:
    return list(database.scalars(select(Anomaly).order_by(Anomaly.detected_at.desc()).limit(limit)))