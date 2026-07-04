"""FastAPI inference API for mechanical sensor anomaly detection."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.models.predict import predict_batch, predict_one

app = FastAPI(
    title="AI Machine Research Workbench API",
    description="Mechanical sensor anomaly detection PoC API.",
    version="0.1.0",
)


class SensorRecord(BaseModel):
    """Input schema for one sensor record."""

    temperature: float = Field(..., description="Temperature sensor value")
    vibration: float = Field(..., description="Vibration sensor value")
    pressure: float = Field(..., description="Pressure sensor value")
    current: float = Field(..., description="Current sensor value")
    rpm: float = Field(..., description="Rotations per minute")


class PredictionResponse(BaseModel):
    """Prediction response schema."""

    prediction: str
    anomaly_score: float
    reason: str


@app.get("/health")
def health() -> dict[str, str]:
    """Return API health status."""
    return {"status": "ok", "service": "ai-machine-research-workbench"}


@app.post("/predict", response_model=PredictionResponse)
def predict(record: SensorRecord) -> dict[str, Any]:
    """Predict anomaly for one record."""
    return predict_one(record.model_dump())


@app.post("/batch-predict", response_model=list[PredictionResponse])
def batch_predict(records: list[SensorRecord]) -> list[dict[str, Any]]:
    """Predict anomalies for multiple records."""
    return predict_batch([record.model_dump() for record in records])
