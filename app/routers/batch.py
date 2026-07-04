from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.batch_service import run_daily_batch
from app.services.log_service import list_logs

router = APIRouter(tags=["batch"])


@router.post("/api/batch/run")
def run_batch(db: Session = Depends(get_db)) -> dict[str, object]:
    """日次バッチを手動起動する API です。"""

    return run_daily_batch(db)


@router.get("/batch", response_class=HTMLResponse)
def batch_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """バッチ実行結果を確認する画面を表示します。"""

    return request.app.state.templates.TemplateResponse(
        request,
        "batch.html",
        {"logs": list_logs(db, 10), "active": "batch"},
    )
