from sqlalchemy.orm import Session

from app.models import Alert, Anomaly
from app.services.anomaly_detector import Detection
from app.services.webhook import simulate_webhook


def create_alert(database: Session, detection: Detection, anomaly: Anomaly) -> Alert:
    alert = Alert(anomaly_id=anomaly.id, severity=detection.severity, title=f"{detection.severity.title()} anomaly: {detection.metric}", message=detection.description)
    database.add(alert)
    database.flush()
    alert.webhook_status = simulate_webhook({"alert_id": alert.id, "severity": alert.severity, "message": alert.message})
    return alert