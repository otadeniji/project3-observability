from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routers import alerts, anomalies, health, logs


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="Intelligent Observability & Event Watchdog", version="1.0.0", lifespan=lifespan)
app.include_router(logs.router)
app.include_router(health.router)
app.include_router(anomalies.router)
app.include_router(alerts.router)


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {"service": "observability-watchdog", "docs": "/docs", "status": "running"}