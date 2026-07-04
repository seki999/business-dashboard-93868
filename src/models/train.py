"""Train IsolationForest anomaly detection model."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from src.data.preprocess import preprocess_csv
from src.utils import ensure_parent, get_logger, load_config, project_path

logger = get_logger(__name__)


def evaluate_predictions(labels: pd.Series, raw_predictions: list[int]) -> dict[str, object]:
    """Convert IsolationForest output and calculate metrics."""
    predicted_labels = pd.Series(raw_predictions).map({1: 0, -1: 1}).astype(int)
    report = classification_report(
        labels,
        predicted_labels,
        target_names=["normal", "anomaly"],
        output_dict=True,
        zero_division=0,
    )
    matrix = confusion_matrix(labels, predicted_labels).tolist()
    return {
        "accuracy": float(accuracy_score(labels, predicted_labels)),
        "confusion_matrix": matrix,
        "classification_report": report,
        "normal_count": int((labels == 0).sum()),
        "anomaly_count": int((labels == 1).sum()),
    }


def create_figures(raw_data_path: Path, figures_dir: Path) -> dict[str, str]:
    """Create validation charts from raw data."""
    figures_dir.mkdir(parents=True, exist_ok=True)
    dataframe = pd.read_csv(raw_data_path, parse_dates=["timestamp"])

    trend_path = figures_dir / "sensor_trends.png"
    anomaly_path = figures_dir / "anomaly_scatter.png"

    plt.figure(figsize=(12, 7))
    for column in ["temperature", "vibration", "pressure", "current", "rpm"]:
        values = dataframe[column].interpolate(limit_direction="both")
        normalized = (values - values.min()) / (values.max() - values.min())
        plt.plot(dataframe["timestamp"], normalized, label=column)
    plt.title("Normalized Sensor Trends")
    plt.xlabel("timestamp")
    plt.ylabel("normalized value")
    plt.legend()
    plt.tight_layout()
    plt.savefig(trend_path)
    plt.close()

    plt.figure(figsize=(12, 6))
    normal = dataframe[dataframe["status"] == "normal"]
    anomaly = dataframe[dataframe["status"] == "anomaly"]
    plt.scatter(normal["timestamp"], normal["vibration"], s=12, label="normal", alpha=0.6)
    plt.scatter(anomaly["timestamp"], anomaly["vibration"], s=30, label="anomaly", alpha=0.9)
    plt.title("Vibration Anomaly Points")
    plt.xlabel("timestamp")
    plt.ylabel("vibration")
    plt.legend()
    plt.tight_layout()
    plt.savefig(anomaly_path)
    plt.close()

    return {"sensor_trends": str(trend_path), "anomaly_scatter": str(anomaly_path)}


def train_model(config_path: Path | None = None) -> dict[str, object]:
    """Train and persist an IsolationForest model."""
    config = load_config(config_path)
    raw_data_path = project_path(config["paths"]["raw_data"])
    model_path = project_path(config["paths"]["model"])
    metrics_path = project_path(config["paths"]["metrics"])
    figures_dir = project_path(config["paths"]["figures_dir"])

    features, labels, _ = preprocess_csv(
        input_path=raw_data_path,
        features_output_path=project_path(config["paths"]["processed_features"]),
        labels_output_path=project_path(config["paths"]["processed_labels"]),
        metadata_output_path=project_path(config["paths"]["processed_metadata"]),
        feature_columns=config["features"],
    )

    model = IsolationForest(
        contamination=config["model"]["contamination"],
        random_state=config["model"]["random_state"],
        n_estimators=config["model"]["n_estimators"],
    )
    model.fit(features)
    raw_predictions = model.predict(features)
    metrics = evaluate_predictions(labels, raw_predictions)
    metrics["figures"] = create_figures(raw_data_path, figures_dir)
    metrics["model"] = {
        "algorithm": "IsolationForest",
        "contamination": config["model"]["contamination"],
        "n_estimators": config["model"]["n_estimators"],
    }

    ensure_parent(model_path)
    ensure_parent(metrics_path)
    joblib.dump(model, model_path)
    metrics_path.write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    logger.info("Saved model -> %s", model_path)
    logger.info("Saved metrics -> %s", metrics_path)
    return metrics


def main() -> None:
    """Run model training."""
    train_model()


if __name__ == "__main__":
    main()
