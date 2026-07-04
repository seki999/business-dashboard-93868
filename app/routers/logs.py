from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.schemas import OperationLogRead
from app.services.log_service import list_logs

router = APIRouter(tags=["logs"])


@router.get("/api/logs", response_model=list[OperationLogRead])
def logs_api(db: Session = Depends(get_db)) -> list:
    """監視・運用画面で使うログを JSON API として返します。"""

    return list_logs(db)


@router.get("/logs", response_class=HTMLResponse)
def logs_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """ログ一覧画面を表示します。"""

    return request.app.state.templates.TemplateResponse(
        "logs.html",
        {"request": request, "logs": list_logs(db), "active": "logs"},
    )
