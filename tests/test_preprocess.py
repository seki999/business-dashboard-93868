"""Tests for preprocessing."""

import pandas as pd

from src.data.preprocess import preprocess_dataframe


def test_preprocess_dataframe_fills_missing_and_scales() -> None:
    """Preprocessing should remove missing values and keep labels."""
    dataframe = pd.DataFrame(
        {
            "temperature": [60.0, None, 85.0],
            "vibration": [0.8, 0.9, None],
            "pressure": [100.0, 101.0, 115.0],
            "current": [10.0, None, 15.0],
            "rpm": [1500.0, 1490.0, 1200.0],
            "status": ["normal", "normal", "anomaly"],
        }
    )
    features, labels, metadata = preprocess_dataframe(
        dataframe,
        ["temperature", "vibration", "pressure", "current", "rpm"],
    )

    assert not features.isna().any().any()
    assert labels.tolist() == [0, 0, 1]
    assert "scaler" in metadata
