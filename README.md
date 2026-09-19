# Intelligent Observability & Event Watchdog

## Overview

An API-first observability service built with **FastAPI** and **SQLite** that monitors application logs, detects anomalies using AI-powered statistical analysis, and triggers configurable alerts when thresholds are breached.

---

## 🎯 What This Service Does

- **Real-time Log Monitoring**: Ingest and parse application/platform logs via REST API
- **Anomaly Detection**: Statistical analysis to detect spikes in errors (moving average, standard deviation)
- **Alerting System**: Threshold-based alerts with webhook simulation for email/Slack templates
- **Health Visualization**: Interactive Streamlit dashboard showing system health trends over time

---

## 🛠️ Tech Stack

| Component          | Technology                                         |
| ------------------ | -------------------------------------------------- |
| **Backend**  | Python 3.x + FastAPI                               |
| **Database** | SQLite (free-tier, no external dependencies)       |
| **Frontend** | Streamlit (interactive dashboard)                  |
| **AI/ML**    | NumPy, Scikit-learn (anomaly detection algorithms) |
| **API Docs** | Swagger UI (auto-generated at`/docs`)            |

---

## 📦 Installation

### Prerequisites

- Python 3.8+
- pip or poetry

### Setup Steps

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database automatically on API startup

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# In a second terminal, run the dashboard
streamlit run dashboard/app.py
```

### Access Points

- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Dashboard**: `http://localhost:8501` (Streamlit)
- **Health Endpoint**: `http://localhost:8000/api/health`

---

## 📊 API Endpoints

| Method | Endpoint             | Description            |
| ------ | -------------------- | ---------------------- |
| POST   | `/api/logs/upload` | Upload log files       |
| GET    | `/api/health`      | System health check    |
| GET    | `/api/anomalies`   | Get detected anomalies |
| GET    | `/api/alerts`      | Get recent alerts      |

---

## 🚀 Usage Examples

### Upload Logs via API

```
project3-observability/
├── app/                       # FastAPI app, models, routers, and services
├── dashboard/app.py           # Streamlit dashboard
├── tests/                     # API and service tests
├── data/                      # SQLite database location
├── sample_logs/               # Example log files
├── prompts.md                # Prompts audit trail
└── requirements.txt
```
```bash
curl http://localhost:8000/api/anomalies
```

---

## 📈 Dashboard Features

The Streamlit dashboard provides:

- **Real-time error rate visualization**
- **Anomaly detection results** (highlighted with severity colors)
- **Health trend charts** over time
- **Alert summary** with configurable thresholds
- **System metrics** display

---

## 🧠 Anomaly Detection Logic

The system uses statistical methods to identify anomalies:

1. **Moving Average**: Calculates rolling average of error counts
2. **Standard Deviation**: Detects spikes beyond ±2σ from normal baseline
3. **Threshold Breaching**: Triggers alerts when error count exceeds threshold × duration
4. **Pattern Recognition**: Identifies recurring anomalies (same error message patterns)

---

## 🔔 Alerting System

### Webhook Simulation

The system simulates webhook delivery for:

- Critical errors (>10 in 5 minutes)
- Database connection failures
- Memory/CPU spikes
- Authentication failures

### Alert Format

```json
{
  "event_type": "anomaly_detected",
  "severity": "critical",
  "message": "Error spike detected: 15 errors in last 5 minutes",
  "timestamp": "2026-09-18T17:30:00Z",
  "details": {
    "metric": "error_count",
    "current_value": 15,
    "threshold": 10,
    "baseline_average": 2.5
  }
}
```

---

## 📁 Project Structure

```
project3-observability/
├── src/
│   ├── app.py                 # Main FastAPI application
│   ├── models.py              # Database models (LogEntry, Anomaly, Alert)
│   ├── anomaly_detector.py    # AI-based anomaly detection logic
│   ├── alerting.py            # Webhook/alert configuration
│   └── dashboard/             # Streamlit dashboard files
├── tests/                     # Unit tests
├── docs/                      # Documentation
├── sample_logs/              # Example log files for testing
├── prompts.md                # Prompts audit trail (if using AI development)
└── requirements.txt          # Python dependencies
```

---

## 🔧 Configuration

Edit `src/config.py` to customize:

- Error thresholds for alerting
- Dashboard refresh rates
- Webhook delivery preferences
- Database connection settings

---

## 🧪 Testing

Run the test suite:

```bash
pytest -q
```

---

## 📝 Development Notes

This project was built using **Vibe Coding** methodology - directing AI agents to build the system while maintaining architectural oversight. All prompts and iterations are logged in `prompts.md` (if applicable).

### Architecture Decisions

- **SQLite**: Chosen for simplicity and zero external dependencies
- **FastAPI**: Auto-generated docs, async support, Pydantic validation
- **Streamlit**: Rapid dashboard prototyping with rich interactivity
- **Statistical Methods**: NumPy/Scikit-learn for anomaly detection without heavy ML dependencies

---

## 🤝 Contributing

This is a demonstration project. Feel free to fork and extend with:

- Additional anomaly detection algorithms
- Integration with Prometheus/Grafana
- Real webhook delivery (Email, Slack, PagerDuty)
- Historical trend analysis over weeks/months

---

## 📄 License

This project is provided as-is for educational and demonstration purposes.

---

## 🚀 Running in Production

For production deployment:

```bash
# Use Docker for containerization
docker-compose up -d

# Or deploy to cloud platforms:
# - AWS SageMaker, Google Vertex AI
# - Azure Machine Learning Studio
# - Streamlit Cloud (free tier)
```

---

**Built with ❤️ using Python, FastAPI, and intelligent agent collaboration.**
