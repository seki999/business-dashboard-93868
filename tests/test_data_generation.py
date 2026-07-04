"""Tests for simulated sensor data generation."""

from scripts.generate_sensor_data import generate_sensor_dataframe


def test_generate_sensor_dataframe_columns_and_status() -> None:
    """Generated data should contain required columns and statuses."""
    dataframe = generate_sensor_dataframe(n_samples=100, anomaly_rate=0.1, random_state=1)

    assert list(dataframe.columns) == [
        "timestamp",
        "machine_id",
        "temperature",
        "vibration",
        "pressure",
        "current",
        "rpm",
        "status",
    ]
    assert len(dataframe) == 100
    assert set(dataframe["status"].unique()).issubset({"normal", "anomaly"})
