# Setup

## 前提

- Python 3.11+
- Docker Desktop
- Git

## ローカル実行

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install ".[dev]"
uvicorn app.main:app --reload
```

Windows PowerShell の場合:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install ".[dev]"
uvicorn app.main:app --reload
```

ブラウザで `http://localhost:8000` を開きます。

## Docker 実行

```bash
docker compose up --build
```

- App: `http://localhost:8000`
- Adminer: `http://localhost:8080`
- PostgreSQL: `localhost:5432`

## DB 初期化

アプリ起動時に SQLAlchemy がテーブルを作成し、`ENABLE_SEED_DATA=true` の場合は seed data を投入します。PostgreSQL コンテナでは `infra/db/init.sql` も初期化時に実行されます。

## MySQL への切り替え

`pyproject.toml` に MySQL driver を追加し、`DATABASE_URL` を `mysql+pymysql://user:password@db:3306/database` の形式に変更します。SQLAlchemy model は標準的な型で構成しているため、基本的な移行は接続 URL と driver 変更で検証できます。

## テスト

```bash
pytest
ruff check .
```

## スクリーンショット生成

```bash
npm init -y
npm i -D @playwright/test
npx playwright install chromium
npx playwright test tests/e2e/screenshot.spec.ts --config=playwright.config.ts
```

この sample では Playwright config は必要に応じて追加してください。`baseURL` に `http://localhost:8000` を指定すると `screenshots/*.png` を更新できます。

## FAQ

- DB に接続できない: `docker compose ps` で db の healthcheck を確認してください。
- seed data が入らない: `.env` または compose の `ENABLE_SEED_DATA` を確認してください。
- ポートが競合する: `docker-compose.yml` の `8000:8000` または `5432:5432` を変更してください。

## Troubleshooting

ログ画面 `/logs` と `docker compose logs app` を確認します。想定外エラーは API response に詳細を出さず、アプリログに記録します。
