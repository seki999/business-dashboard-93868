from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import BusinessRuleError
from app.db.database import get_db
from app.db.models import ImprovementTask
from app.db.schemas import ImprovementTaskCreate, ImprovementTaskRead
from app.services.log_service import write_log

router = APIRouter(tags=["improvement-tasks"])


@router.get("/api/improvement-tasks", response_model=list[ImprovementTaskRead])
def list_tasks(db: Session = Depends(get_db)) -> list[ImprovementTask]:
    """業務改善タスクを期限順に取得します。"""

    return list(db.scalars(select(ImprovementTask).order_by(ImprovementTask.due_date)))


@router.post("/api/improvement-tasks", response_model=ImprovementTaskRead, status_code=201)
def create_task(payload: ImprovementTaskCreate, db: Session = Depends(get_db)) -> ImprovementTask:
    """改善タスクを登録し、プロジェクト管理のサンプルとして利用します。"""

    task = ImprovementTask(**payload.model_dump())
    db.add(task)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise BusinessRuleError("task_code already exists", 409) from exc
    db.refresh(task)
    write_log(db, "application", "INFO", f"改善タスクを登録しました: {task.task_code}")
    return task


@router.get("/tasks", response_class=HTMLResponse)
def tasks_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """業務改善タスク一覧画面を表示します。"""

    return request.app.state.templates.TemplateResponse(
        request,
        "tasks.html",
        {"tasks": list_tasks(db), "active": "tasks"},
    )
