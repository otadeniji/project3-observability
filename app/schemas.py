from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LogUploadResponse(BaseModel):
    imported: int
    anomalies_detected: int
    alerts_created: int


class HealthResponse(BaseModel):
    status: str
    database: str
    log_count: int
    anomaly_count: int
    open_alert_count: int
    last_log_at: datetime | None = None


class AnomalyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    metric: str
    detected_at: datetime
    current_value: float
    moving_average: float
    standard_deviation: float
    severity: str
    description: str


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    anomaly_id: int | None
    severity: str
    title: str
    message: str
    status: str
    webhook_status: str
    created_at: datetime
    acknowledged_at: datetime | None