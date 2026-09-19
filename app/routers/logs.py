from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Anomaly, HealthMetric, LogEntry
from app.schemas import LogUploadResponse
from app.services.alert_manager import create_alert
from app.services.anomaly_detector import detect_error_spike
from app.services.parser import parse_content

router = APIRouter(prefix="/api/logs", tags=["logs"])


@router.post("/upload", response_model=LogUploadResponse)
async def upload_logs(file: UploadFile = File(...), database: Session = Depends(get_db)) -> LogUploadResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="A log file is required")
    content = (await file.read()).decode("utf-8", errors="replace")
    parsed_entries = parse_content(content)
    if not parsed_entries:
        raise HTTPException(status_code=400, detail="No parseable log entries found")
    entries = [LogEntry(**entry, source=file.filename) for entry in parsed_entries]
    database.add_all(entries)
    database.flush()
    error_count = sum(entry.level in {"ERROR", "CRITICAL"} for entry in entries)
    previous_counts = list(database.scalars(select(HealthMetric.value).where(HealthMetric.metric_name == "error_count").order_by(HealthMetric.timestamp.desc()).limit(20)))
    detection = detect_error_spike(error_count, [int(value) for value in previous_counts])
    database.add(HealthMetric(metric_name="error_count", value=error_count, unit="entries"))
    anomalies_detected = alerts_created = 0
    if detection:
        anomaly = Anomaly(**detection.__dict__)
        database.add(anomaly)
        database.flush()
        create_alert(database, detection, anomaly)
        anomalies_detected = alerts_created = 1
    database.commit()
    return LogUploadResponse(imported=len(entries), anomalies_detected=anomalies_detected, alerts_created=alerts_created)