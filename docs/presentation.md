# Intelligent Observability & Event Watchdog

## Presentation Draft

**Interactive deck:** Open [presentation.html](presentation.html) in a browser. It embeds the live Swagger, anomaly, alert, and Streamlit views from the localhost app.

**Format:** 8 slides, approximately 7 minutes

**Demo URLs:**

- Swagger API: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/api/health
- Anomalies: http://127.0.0.1:8000/api/anomalies
- Alerts: http://127.0.0.1:8000/api/alerts
- Dashboard: http://localhost:8501

---

## Slide 1: From Raw Logs to Actionable Signals

**On-slide copy**

### Intelligent Observability & Event Watchdog

An API-first monitoring service that turns application logs into:

- Stored operational history
- Statistical anomaly detection
- Threshold-based alerts
- A live health dashboard

**Visual:** Use the Streamlit dashboard screenshot from `http://localhost:8501` as the full-slide background or right-side visual.

**Speaker notes:**

This project addresses a common observability problem: logs contain useful signals, but teams need a fast way to ingest, interpret, and act on them. The Watchdog provides that workflow through an API and a lightweight dashboard.

---

## Slide 2: The Problem We Solve

**On-slide copy**

Operational logs are valuable, but manual review is:

- Slow during incidents
- Difficult to scale
- Inconsistent across services
- Disconnected from alert history

**Key idea:** Make the first level of incident detection automatic and inspectable.

**Speaker notes:**

The goal is not to replace an enterprise observability platform. It is to create a focused, understandable MVP that demonstrates the full path from log upload to a visible alert.

---

## Slide 3: Architecture

**On-slide copy**

```text
Log file
   |
   v
FastAPI upload endpoint
   |
   +--> Parser --> SQLite LogEntry records
   |
   +--> HealthMetric history
              |
              v
       Moving average + standard deviation
              |
              v
       Anomaly --> Alert --> Simulated webhook
                              |
                              v
                       Streamlit dashboard
```

**Technology stack:** Python, FastAPI, SQLAlchemy, SQLite, NumPy, Streamlit.

**Speaker notes:**

SQLite keeps the MVP free and easy to run locally. FastAPI provides an API-first contract and automatic Swagger documentation. The dashboard reads the same database, so the API and UI show one operational state.

---

## Slide 4: API-First Workflow

**On-slide copy**

### One upload, one observable workflow

1. Upload a log file through Swagger or an HTTP client.
2. Parse timestamp, severity, message, and numeric values.
3. Store log entries and metric history.
4. Compare the new error count with prior observations.
5. Persist anomalies and alerts for review.

**Visual:** Screenshot of `http://127.0.0.1:8000/docs`, showing:

- `POST /api/logs/upload`
- `GET /api/health`
- `GET /api/anomalies`
- `GET /api/alerts`

**Speaker notes:**

Swagger makes the system immediately usable. A user can upload a sample file without writing a client, then inspect each API response from the same interface.

---

## Slide 5: Statistical Detection

**On-slide copy**

For each new error-count observation:

$$
\text{limit} = \text{moving average} + 2 \times \text{standard deviation}
$$

If the current count exceeds that limit, the system creates an anomaly.

### Demonstrated result

- Baseline average: `3` errors
- Current observation: `10` errors
- Standard deviation: `0`
- Classification: `critical`

**Speaker notes:**

The current upload is evaluated against previous metric history, not against itself. That distinction prevents the new value from hiding its own spike and gives the detector a clear baseline.

---

## Slide 6: Alerting and Traceability

**On-slide copy**

### Every anomaly becomes an actionable record

- Severity: `critical`
- Title: `Critical anomaly: error_count`
- Status: `open`
- Webhook status: `simulated`
- Acknowledgement endpoint available

**Visual:** Screenshot of `http://127.0.0.1:8000/api/alerts` showing the JSON alert response.

**Speaker notes:**

The webhook is intentionally simulated for this local MVP. The alert payload and delivery status are still persisted, so a real Slack, email, or incident-management integration can be added behind the same service boundary later.

---

## Slide 7: Dashboard View

**On-slide copy**

### One screen for operational context

The dashboard currently shows:

- `36` log entries
- `16` errors
- `1` open alert
- `1` anomaly
- Log-level distribution
- Error-count history
- Recent alerts and recent logs

**Visual:** Screenshot of `http://localhost:8501` showing the metric row and charts.

**Speaker notes:**

The dashboard is deliberately compact. It answers three immediate questions: how much data arrived, is the system seeing errors, and does anything require attention?

---

## Slide 8: MVP Value and Next Steps

**On-slide copy**

### What the MVP proves

- Logs can be ingested through a documented API.
- Data persists in a free local database.
- Statistical anomalies are detected from history.
- Alerts are created and traceable.
- Operators can inspect the state visually.

### Next steps

- Add authentication and role-based access
- Add configurable rules per service
- Add real webhook integrations
- Add time-window aggregation and deduplication
- Containerize API, dashboard, and database

**Speaker notes:**

The important achievement is the complete feedback loop. The next stage is production hardening: security, configuration, richer aggregation, delivery guarantees, and deployment automation.

---

## Live Demo Script

1. Open `http://127.0.0.1:8000/docs`.
2. Expand `POST /api/logs/upload` and upload `sample_logs/example_app.log`.
3. Open `GET /api/health` and point out database connectivity and log count.
4. Upload `sample_logs/example_app.log` again to establish metric history.
5. Upload `sample_logs/error_spike.log` to create a visible spike.
6. Open `GET /api/anomalies` and show the `critical` result.
7. Open `GET /api/alerts` and show `webhook_status: simulated`.
8. Refresh `http://localhost:8501` and show the dashboard metrics and charts.

## Screenshot Checklist

- [ ] Swagger endpoint overview
- [ ] Swagger upload form or successful upload response
- [ ] Health JSON response
- [ ] Anomaly JSON response
- [ ] Alert JSON response
- [ ] Streamlit dashboard top section
- [ ] Streamlit dashboard alert/log tables
