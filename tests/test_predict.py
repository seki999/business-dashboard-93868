"""Tests for prediction output format."""

import pandas as pd
from sklearn.ensemble import IsolationForest

from src.data.preprocess import preprocess_dataframe
from src.models.predict import predict_batch


def test_predict_batch_output_format() -> None:
    """Prediction result should include prediction, score, and reason."""
    dataframe = pd.DataFrame(
        {
            "temperature": [65.0, 66.0, 67.0, 95.0],
            "vibration": [0.8, 0.9, 0.85, 2.1],
            "pressure": [100.0, 101.0, 99.0, 120.0],
            "current": [10.0, 11.0, 10.5, 16.0],
            "rpm": [1500.0, 1510.0, 1495.0, 1100.0],
            "status": ["normal", "normal", "normal", "anomaly"],
        }
    )
    feature_columns = ["temperature", "vibration", "pressure", "current", "rpm"]
    features, _, metadata = preprocess_dataframe(dataframe, feature_columns)
    model = IsolationForest(contamination=0.25, random_state=1).fit(features)

    result = predict_batch(
        [
            {
                "temperature": 90.0,
                "vibration": 2.0,
                "pressure": 118.0,
                "current": 15.0,
                "rpm": 1150.0,
            }
        ],
        model=model,
        metadata=metadata,
    )

    assert set(result[0]) == {"prediction", "anomaly_score", "reason"}
    assert result[0]["prediction"] in {"normal", "anomaly"}
    assert isinstance(result[0]["anomaly_score"], float)
