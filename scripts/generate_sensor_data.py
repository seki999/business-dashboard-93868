"""Generate simulated mechanical sensor data for AI validation."""

from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.utils import ensure_parent, get_logger, load_config, project_path  # noqa: E402

logger = get_logger(__name__)


def generate_sensor_dataframe(
    n_samples: int = 1200,
    anomaly_rate: float = 0.08,
    random_state: int = 42,
    machine_ids: list[str] | None = None,
) -> pd.DataFrame:
    """Create a dataframe with normal and anomalous sensor rows."""
    rng = np.random.default_rng(random_state)
    machine_ids = machine_ids or ["machine-a", "machine-b", "machine-c"]

    timestamps = [
        datetime(2026, 1, 1, 0, 0, 0) + timedelta(minutes=5 * i)
        for i in range(n_samples)
    ]
    machines = rng.choice(machine_ids, size=n_samples)
    status = np.where(rng.random(n_samples) < anomaly_rate, "anomaly", "normal")

    # 正常状態のベースラインを生成する。
    temperature = rng.normal(68, 5, n_samples)
    vibration = rng.normal(0.9, 0.18, n_samples)
    pressure = rng.normal(101, 3, n_samples)
    current = rng.normal(11, 1.1, n_samples)
    rpm = rng.normal(1500, 90, n_samples)

    anomaly_mask = status == "anomaly"
    anomaly_count = int(anomaly_mask.sum())

    # 異常状態では複数センサーに同時に変化を加える。
    temperature[anomaly_mask] += rng.normal(18, 5, anomaly_count)
    vibration[anomaly_mask] += rng.normal(1.2, 0.35, anomaly_count)
    pressure[anomaly_mask] += rng.normal(12, 4, anomaly_count)
    current[anomaly_mask] += rng.normal(4, 1.2, anomaly_count)
    rpm[anomaly_mask] -= rng.normal(260, 80, anomaly_count)

    dataframe = pd.DataFrame(
        {
            "timestamp": timestamps,
            "machine_id": machines,
            "temperature": np.round(temperature, 3),
            "vibration": np.round(vibration, 3),
            "pressure": np.round(pressure, 3),
            "current": np.round(current, 3),
            "rpm": np.round(rpm, 3),
            "status": status,
        }
    )

    # PoC らしく欠損値処理も検証できるよう、少量の欠損を混入する。
    for column in ["temperature", "vibration", "pressure", "current", "rpm"]:
        missing_index = rng.choice(n_samples, size=max(1, n_samples // 100), replace=False)
        dataframe.loc[missing_index, column] = np.nan

    return dataframe


def main() -> None:
    """Generate sensor data and save it as CSV."""
    config = load_config()
    output_path = project_path(config["paths"]["raw_data"])
    data_config = config["data"]

    dataframe = generate_sensor_dataframe(
        n_samples=data_config["n_samples"],
        anomaly_rate=data_config["anomaly_rate"],
        random_state=data_config["random_state"],
        machine_ids=data_config["machine_ids"],
    )
    ensure_parent(output_path)
    dataframe.to_csv(output_path, index=False)
    logger.info("Generated sensor data: %s rows -> %s", len(dataframe), output_path)


if __name__ == "__main__":
    main()
