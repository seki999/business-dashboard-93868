"""Preprocess sensor CSV data for anomaly detection training."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.preprocessing import StandardScaler

from src.utils import ensure_parent, get_logger, load_config, project_path

logger = get_logger(__name__)


def preprocess_dataframe(
    dataframe: pd.DataFrame,
    feature_columns: list[str],
) -> tuple[pd.DataFrame, pd.Series, dict[str, dict[str, float]]]:
    """Fill missing values, standardize features, and return labels."""
    working = dataframe.copy()

    # 数値センサー欠損は中央値で補完する。
    medians = working[feature_columns].median(numeric_only=True)
    working[feature_columns] = working[feature_columns].fillna(medians)

    scaler = StandardScaler()
    scaled_values = scaler.fit_transform(working[feature_columns])
    features = pd.DataFrame(
        scaled_values,
        columns=feature_columns,
        index=working.index,
    )
    labels = working["status"].map({"normal": 0, "anomaly": 1}).fillna(0).astype(int)

    metadata = {
        "features": {column: {"median": float(medians[column])} for column in feature_columns},
        "scaler": {
            column: {
                "mean": float(scaler.mean_[index]),
                "scale": float(scaler.scale_[index]),
            }
            for index, column in enumerate(feature_columns)
        },
    }
    return features, labels, metadata


def preprocess_csv(
    input_path: Path,
    features_output_path: Path,
    labels_output_path: Path,
    metadata_output_path: Path,
    feature_columns: list[str],
) -> tuple[pd.DataFrame, pd.Series, dict[str, dict[str, float]]]:
    """Preprocess raw CSV and save processed artifacts."""
    dataframe = pd.read_csv(input_path)
    features, labels, metadata = preprocess_dataframe(dataframe, feature_columns)

    ensure_parent(features_output_path)
    ensure_parent(labels_output_path)
    ensure_parent(metadata_output_path)
    features.to_csv(features_output_path, index=False)
    labels.to_frame(name="label").to_csv(labels_output_path, index=False)
    metadata_output_path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    logger.info("Saved processed features -> %s", features_output_path)
    return features, labels, metadata


def main() -> None:
    """Run preprocessing from configured paths."""
    config = load_config()
    preprocess_csv(
        input_path=project_path(config["paths"]["raw_data"]),
        features_output_path=project_path(config["paths"]["processed_features"]),
        labels_output_path=project_path(config["paths"]["processed_labels"]),
        metadata_output_path=project_path(config["paths"]["processed_metadata"]),
        feature_columns=config["features"],
    )


if __name__ == "__main__":
    main()
