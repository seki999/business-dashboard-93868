# Project Structure

```text
sample-business-dashboard/
├── app/                  # FastAPI アプリ本体
├── tests/                # pytest と Playwright screenshot script
├── docs/                 # 設計・構築・構成説明
├── infra/                # DB 初期化と AWS sample config
├── screenshots/          # README 掲載用スクリーンショット
├── .github/workflows/    # GitHub Actions CI
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## app

- `main.py`: FastAPI アプリケーションの入口です。
- `core/`: 設定、ログ、エラー処理を管理します。
- `db/`: SQLAlchemy の DB 接続、モデル、schema、seed data を置きます。
- `routers/`: API と HTML 画面の routing を担当します。
- `services/`: 集計、バッチ、ログなどの業務処理を担当します。
- `templates/`: Jinja2 の画面テンプレートです。
- `static/`: CSS と JavaScript です。

## tests

API の基本テストと、スクリーンショット取得用 Playwright spec を配置しています。

## docs

architecture、technical design、project structure、setup を分け、上流工程・設計意図を説明します。

## infra

`infra/db/init.sql` は PostgreSQL 初期化サンプル、`infra/aws/` は AWS 配置を想定した sample config です。

## screenshots

GitHub README で参照する画像を配置します。実行環境で Playwright を使って差し替え可能です。
