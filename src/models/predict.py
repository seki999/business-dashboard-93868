"""Prediction utilities for trained anomaly detection model."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from src.utils import load_config, project_path


def load_model(model_path: Path | None = None) -> Any:
    """Load a trained model artifact."""
    config = load_config()
    path = model_path or project_path(config["paths"]["model"])
    return joblib.load(path)


def load_preprocess_metadata(metadata_path: Path | None = None) -> dict[str, Any]:
    """Load preprocessing medians and scaler parameters."""
    config = load_config()
    path = metadata_path or project_path(config["paths"]["processed_metadata"])
    return json.loads(path.read_text(encoding="utf-8"))


def transform_input(
    records: list[dict[str, float]] | pd.DataFrame,
    feature_columns: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """Apply training-time preprocessing to inference input."""
    config = load_config()
    feature_columns = feature_columns or config["features"]
    metadata = metadata or load_preprocess_metadata()
    dataframe = pd.DataFrame(records).copy()

    for column in feature_columns:
        if column not in dataframe.columns:
            dataframe[column] = metadata["features"][column]["median"]
        dataframe[column] = pd.to_numeric(dataframe[column], errors="coerce")
        dataframe[column] = dataframe[column].fillna(metadata["features"][column]["median"])
        mean = metadata["scaler"][column]["mean"]
        scale = metadata["scaler"][column]["scale"] or 1.0
        dataframe[column] = (dataframe[column] - mean) / scale

    return dataframe[feature_columns]


def prediction_reason(record: dict[str, float], prediction: str) -> str:
    """Create a simple human-readable reason for an anomaly result."""
    if prediction == "normal":
        return "主要センサー値は学習済み正常パターンに近いです。"

    reasons: list[str] = []
    if record.get("temperature", 0) >= 80:
        reasons.append("温度が高い")
    if record.get("vibration", 0) >= 1.5:
        reasons.append("振動が大きい")
    if record.get("pressure", 0) >= 110:
        reasons.append("圧力が高い")
    if record.get("current", 0) >= 14:
        reasons.append("電流が高い")
    if record.get("rpm", 9999) <= 1300:
        reasons.append("回転数が低下")
    return "、".join(reasons) + "ため異常候補です。" if reasons else "複数センサーの組み合わせが正常パターンから外れています。"


def predict_batch(
    records: list[dict[str, float]] | pd.DataFrame,
    model: Any | None = None,
    metadata: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Predict anomaly labels and scores for multiple records."""
    input_dataframe = pd.DataFrame(records)
    model = model or load_model()
    metadata = metadata or load_preprocess_metadata()
    config = load_config()
    transformed = transform_input(input_dataframe, config["features"], metadata)

    raw_predictions = model.predict(transformed)
    scores = model.decision_function(transformed)

    results: list[dict[str, Any]] = []
    for index, raw_prediction in enumerate(raw_predictions):
        prediction = "anomaly" if int(raw_prediction) == -1 else "normal"
        record = input_dataframe.iloc[index].to_dict()
        results.append(
            {
                "prediction": prediction,
                "anomaly_score": float(-scores[index]),
                "reason": prediction_reason(record, prediction),
            }
        )
    return results


def predict_one(record: dict[str, float]) -> dict[str, Any]:
    """Predict anomaly label and score for one sensor record."""
    return predict_batch([record])[0]
