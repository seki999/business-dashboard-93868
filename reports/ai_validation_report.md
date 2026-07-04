# AI 技術検証レポート

作成日: 2026-07-04

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

- 正常データ件数: 1114
- 異常データ件数: 86
- センサー項目: temperature, vibration, pressure, current, rpm
- 異常条件: 高温、高振動、高圧、高電流、回転数低下を模擬

## 5. モデル選定理由

今回の PoC では教師あり分類ではなく、異常検知アルゴリズムである IsolationForest を採用した。  
機械設備の現場では異常データが十分に蓄積されていないケースが多く、少量の異常データまたは正常中心データから異常候補を抽出できる方式が初期検証に適しているためである。

採用モデル:

```json
{
  "algorithm": "IsolationForest",
  "contamination": 0.08,
  "n_estimators": 150
}
```

## 6. 評価結果

- Accuracy: 0.9916666666666667
- Confusion Matrix: `[[1104, 10], [0, 86]]`

分類レポート:

```json
{
  "normal": {
    "precision": 1.0,
    "recall": 0.9910233393177738,
    "f1-score": 0.9954914337240758,
    "support": 1114.0
  },
  "anomaly": {
    "precision": 0.8958333333333334,
    "recall": 1.0,
    "f1-score": 0.945054945054945,
    "support": 86.0
  },
  "accuracy": 0.9916666666666667,
  "macro avg": {
    "precision": 0.9479166666666667,
    "recall": 0.9955116696588868,
    "f1-score": 0.9702731893895105,
    "support": 1200.0
  },
  "weighted avg": {
    "precision": 0.9925347222222223,
    "recall": 0.9916666666666667,
    "f1-score": 0.9918768187027882,
    "support": 1200.0
  }
}
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
