# Linux 環境構築手順

## 前提

- Ubuntu 22.04 以降を想定
- Python 3.11 以上
- Docker / Docker Compose は任意

## Python 環境

```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip make
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 動作確認

```bash
make generate-data
make train
make test
```

## API 起動

```bash
make api
```

ブラウザで `http://localhost:8000/docs` を開く。

## Dashboard 起動

```bash
make dashboard
```

ブラウザで `http://localhost:8501` を開く。

## Docker Compose

```bash
make docker-up
make docker-down
```

Docker 環境では API と Dashboard を同時に起動できる。
