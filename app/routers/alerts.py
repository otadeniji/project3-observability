from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Alert
from app.schemas import AlertResponse

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertResponse])
def list_alerts(limit: int = Query(100, ge=1, le=500), database: Session = Depends(get_db)) -> list[Alert]:
    return list(database.scalars(select(Alert).order_by(Alert.created_at.desc()).limit(limit)))


@router.post("/{alert_id}/acknowledge", response_model=AlertResponse)
def acknowledge_alert(alert_id: int, database: Session = Depends(get_db)) -> Alert:
    alert = database.get(Alert, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.status = "acknowledged"
    alert.acknowledged_at = datetime.now(timezone.utc)
    database.commit()
    database.refresh(alert)
    return alert