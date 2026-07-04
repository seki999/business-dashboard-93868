from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.dashboard_service import get_dashboard_summary

router = APIRouter(tags=["dashboard"])


@router.get("/api/dashboard")
def dashboard_api(db: Session = Depends(get_db)) -> dict[str, object]:
    """ダッシュボード集計値を JSON API として返します。"""

    return get_dashboard_summary(db)


@router.get("/", response_class=HTMLResponse)
def dashboard_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """Jinja2 テンプレートでトップ画面を表示します。"""

    return request.app.state.templates.TemplateResponse(
        request,
        "dashboard.html",
        {"summary": get_dashboard_summary(db), "active": "dashboard"},
    )
