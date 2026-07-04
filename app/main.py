from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.errors import (
    BusinessRuleError,
    business_rule_exception_handler,
    unhandled_exception_handler,
)
from app.core.logging import configure_logging, logger
from app.db.database import init_db
from app.routers import batch, dashboard, deliveries, feedbacks, improvement_tasks, logs, products


@asynccontextmanager
async def lifespan(app: FastAPI):
    """起動時にログ設定と DB 初期化を行い、サンプルをすぐ試せる状態にします。"""

    configure_logging()
    init_db()
    logger.info("application started")
    yield
    logger.info("application stopped")


app = FastAPI(title="Sample Business Dashboard", version="0.1.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.state.templates = Jinja2Templates(directory="app/templates")

app.add_exception_handler(BusinessRuleError, business_rule_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(dashboard.router)
app.include_router(deliveries.router)
app.include_router(products.router)
app.include_router(feedbacks.router)
app.include_router(improvement_tasks.router)
app.include_router(batch.router)
app.include_router(logs.router)


@app.get("/api/health")
def health() -> dict[str, str]:
    """ヘルスチェック用エンドポイントです。CI や監視から利用できます。"""

    return {"status": "ok", "service": "sample-business-dashboard"}
