from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import BusinessRuleError
from app.db.database import get_db
from app.db.models import Feedback
from app.db.schemas import FeedbackCreate, FeedbackRead
from app.services.log_service import write_log

router = APIRouter(tags=["feedbacks"])


@router.get("/api/feedbacks", response_model=list[FeedbackRead])
def list_feedbacks(db: Session = Depends(get_db)) -> list[Feedback]:
    """顧客フィードバックを一覧取得します。"""

    return list(db.scalars(select(Feedback).order_by(Feedback.id)))


@router.post("/api/feedbacks", response_model=FeedbackRead, status_code=201)
def create_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)) -> Feedback:
    """匿名化されたフィードバックを登録します。"""

    feedback = Feedback(**payload.model_dump())
    db.add(feedback)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise BusinessRuleError("feedback_code already exists", 409) from exc
    db.refresh(feedback)
    write_log(db, "application", "INFO", f"フィードバックを登録しました: {feedback.feedback_code}")
    return feedback


@router.get("/feedbacks", response_class=HTMLResponse)
def feedbacks_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """フィードバック一覧画面を表示します。"""

    return request.app.state.templates.TemplateResponse(
        request,
        "feedbacks.html",
        {"feedbacks": list_feedbacks(db), "active": "feedbacks"},
    )
