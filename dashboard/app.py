import os
import sqlite3

import pandas as pd
import streamlit as st

DATABASE_PATH = os.getenv("OBSERVABILITY_DB", "data/observability.db")

st.set_page_config(page_title="Observability Watchdog", page_icon="◉", layout="wide")
st.title("Observability Watchdog")
st.caption("SQLite-backed event health, anomaly detection, and alert history")


@st.cache_data(ttl=5)
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    connection = sqlite3.connect(DATABASE_PATH)
    try:
        logs = pd.read_sql_query("SELECT * FROM log_entries ORDER BY timestamp", connection)
        metrics = pd.read_sql_query("SELECT * FROM health_metrics ORDER BY timestamp", connection)
        alerts = pd.read_sql_query("SELECT * FROM alerts ORDER BY created_at DESC", connection)
        return logs, metrics, alerts
    except sqlite3.OperationalError:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    finally:
        connection.close()


logs, metrics, alerts = load_data()
total_logs = len(logs)
error_count = int(logs["level"].isin(["ERROR", "CRITICAL"]).sum()) if not logs.empty else 0
open_alerts = int((alerts["status"] == "open").sum()) if not alerts.empty else 0

summary = st.columns(4)
summary[0].metric("Log entries", total_logs)
summary[1].metric("Errors", error_count)
summary[2].metric("Open alerts", open_alerts)
summary[3].metric("Anomalies", len(alerts))

left, right = st.columns(2)
with left:
    st.subheader("Log levels")
    if logs.empty:
        st.info("Upload a log file through POST /api/logs/upload to populate the dashboard.")
    else:
        st.bar_chart(logs["level"].value_counts())
with right:
    st.subheader("Error-count history")
    if metrics.empty:
        st.info("No health metrics recorded yet.")
    else:
        chart = metrics.assign(timestamp=pd.to_datetime(metrics["timestamp"])).set_index("timestamp")
        st.line_chart(chart["value"])

st.subheader("Recent alerts")
if alerts.empty:
    st.success("No alerts recorded.")
else:
    st.dataframe(alerts[["created_at", "severity", "title", "status", "webhook_status"]], use_container_width=True, hide_index=True)

st.subheader("Recent logs")
if not logs.empty:
    st.dataframe(logs.tail(25)[["timestamp", "level", "message", "source"]], use_container_width=True, hide_index=True)