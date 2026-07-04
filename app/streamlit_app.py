"""Streamlit dashboard for AI technology validation."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.models.predict import predict_batch
from src.utils import load_config, project_path


def load_sensor_data(path: Path) -> pd.DataFrame:
    """Load raw sensor data if available."""
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, parse_dates=["timestamp"])


def show_trend_chart(dataframe: pd.DataFrame) -> None:
    """Render sensor trend chart with matplotlib."""
    fig, ax = plt.subplots(figsize=(11, 5))
    for column in ["temperature", "vibration", "pressure", "current", "rpm"]:
        values = dataframe[column].interpolate(limit_direction="both")
        normalized = (values - values.min()) / (values.max() - values.min())
        ax.plot(dataframe["timestamp"], normalized, label=column)
    ax.set_title("Sensor Trends")
    ax.set_xlabel("timestamp")
    ax.set_ylabel("normalized value")
    ax.legend()
    st.pyplot(fig)


def show_anomaly_chart(dataframe: pd.DataFrame) -> None:
    """Render anomaly points on vibration timeline."""
    fig, ax = plt.subplots(figsize=(11, 4))
    normal = dataframe[dataframe["status"] == "normal"]
    anomaly = dataframe[dataframe["status"] == "anomaly"]
    ax.scatter(normal["timestamp"], normal["vibration"], s=12, label="normal", alpha=0.6)
    ax.scatter(anomaly["timestamp"], anomaly["vibration"], s=30, label="anomaly", alpha=0.9)
    ax.set_title("Anomaly Points")
    ax.set_xlabel("timestamp")
    ax.set_ylabel("vibration")
    ax.legend()
    st.pyplot(fig)


def main() -> None:
    """Run Streamlit dashboard."""
    st.set_page_config(page_title="AI Machine Research Workbench", layout="wide")
    st.title("AI Machine Research Workbench")
    st.caption("機械設備 AI システム開発前の技術検証 PoC")

    config = load_config()
    raw_data_path = project_path(config["paths"]["raw_data"])
    metrics_path = project_path(config["paths"]["metrics"])

    dataframe = load_sensor_data(raw_data_path)
    if dataframe.empty:
        st.warning("センサーデータがありません。先に `make generate-data` と `make train` を実行してください。")
    else:
        st.subheader("センサーデータ概要")
        col1, col2, col3 = st.columns(3)
        col1.metric("rows", f"{len(dataframe):,}")
        col2.metric("machines", dataframe["machine_id"].nunique())
        col3.metric("anomalies", int((dataframe["status"] == "anomaly").sum()))
        st.dataframe(dataframe.head(20), use_container_width=True)

        st.subheader("センサー推移")
        show_trend_chart(dataframe)

        st.subheader("異常点")
        show_anomaly_chart(dataframe)

    st.subheader("モデル評価結果")
    if metrics_path.exists():
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        st.json(
            {
                "accuracy": metrics.get("accuracy"),
                "confusion_matrix": metrics.get("confusion_matrix"),
                "normal_count": metrics.get("normal_count"),
                "anomaly_count": metrics.get("anomaly_count"),
                "model": metrics.get("model"),
            }
        )
    else:
        st.info("評価結果がありません。`make train` を実行してください。")

    st.subheader("CSV アップロード推論")
    uploaded = st.file_uploader("センサー CSV をアップロード", type=["csv"])
    if uploaded is not None:
        uploaded_df = pd.read_csv(uploaded)
        results = predict_batch(uploaded_df)
        result_df = pd.concat([uploaded_df.reset_index(drop=True), pd.DataFrame(results)], axis=1)
        st.dataframe(result_df, use_container_width=True)


if __name__ == "__main__":
    main()
