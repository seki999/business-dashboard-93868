"""Generate a Japanese AI validation report from metrics and figures."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.utils import ensure_parent, get_logger, load_config, project_path  # noqa: E402

logger = get_logger(__name__)


def build_report(metrics: dict[str, object]) -> str:
    """Build Japanese Markdown validation report."""
    accuracy = metrics.get("accuracy", "N/A")
    normal_count = metrics.get("normal_count", "N/A")
    anomaly_count = metrics.get("anomaly_count", "N/A")
    model = metrics.get("model", {})

    return f"""# AI 技術検証レポート

作成日: {date.today().isoformat()}

## 1. 検証目的

本検証は、機械設備 AI システム開発前の技術検証 PoC として、センサーデータを用いた異常検知の実現可能性を確認することを目的とする。  
温度、振動、圧力、電流、回転数の模擬データを対象に、機械学習モデルが通常状態と異常状態をどの程度分離できるかを評価した。

## 2. 使用技術

- Python 3.11
- pandas / numpy
- scikit-learn IsolationForest
- matplotlib
- FastAPI
- Streamlit
- Docker / Docker Compose
- pytest

## 3. 環境構築手順

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make generate-data
make train
```

Docker を利用する場合:

```bash
make docker-up
```

## 4. データ概要

- 正常データ件数: {normal_count}
- 異常データ件数: {anomaly_count}
- センサー項目: temperature, vibration, pressure, current, rpm
- 異常条件: 高温、高振動、高圧、高電流、回転数低下を模擬

## 5. モデル選定理由

今回の PoC では教師あり分類ではなく、異常検知アルゴリズムである IsolationForest を採用した。  
機械設備の現場では異常データが十分に蓄積されていないケースが多く、少量の異常データまたは正常中心データから異常候補を抽出できる方式が初期検証に適しているためである。

採用モデル:

```json
{json.dumps(model, ensure_ascii=False, indent=2)}
```

## 6. 評価結果

- Accuracy: {accuracy}
- Confusion Matrix: `{metrics.get("confusion_matrix", "N/A")}`

分類レポート:

```json
{json.dumps(metrics.get("classification_report", {}), ensure_ascii=False, indent=2)}
```

## 7. 図表

![Sensor Trends](figures/sensor_trends.png)

![Anomaly Scatter](figures/anomaly_scatter.png)

## 8. 今後の改善案

- 実機センサー値を用いたデータ分布確認
- 設備種別ごとの正常範囲と異常理由の整理
- 時系列特徴量や移動平均特徴量の追加
- LSTM、AutoEncoder、One-Class SVM との比較検証
- モデルバージョン管理と再学習パイプラインの検討
- API 認証、監視、ログ集約など運用設計の追加
"""


def main() -> None:
    """Generate report file."""
    config = load_config()
    metrics_path = project_path(config["paths"]["metrics"])
    report_path = project_path(config["paths"]["report"])

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    report = build_report(metrics)
    ensure_parent(report_path)
    report_path.write_text(report, encoding="utf-8")
    logger.info("Generated validation report -> %s", report_path)


if __name__ == "__main__":
    main()
