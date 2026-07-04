from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import BusinessRuleError
from app.db.database import get_db
from app.db.models import Delivery
from app.db.schemas import DeliveryCreate, DeliveryRead
from app.services.log_service import write_log

router = APIRouter(tags=["deliveries"])


@router.get("/api/deliveries", response_model=list[DeliveryRead])
def list_deliveries(db: Session = Depends(get_db)) -> list[Delivery]:
    """配送データを予定日が近い順に返します。"""

    return list(db.scalars(select(Delivery).order_by(Delivery.scheduled_date, Delivery.id)))


@router.post("/api/deliveries", response_model=DeliveryRead, status_code=201)
def create_delivery(payload: DeliveryCreate, db: Session = Depends(get_db)) -> Delivery:
    """配送データを登録し、重複コードは業務エラーとして扱います。"""

    delivery = Delivery(**payload.model_dump())
    db.add(delivery)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise BusinessRuleError("delivery_code already exists", 409) from exc
    db.refresh(delivery)
    write_log(db, "application", "INFO", f"配送データを登録しました: {delivery.delivery_code}")
    return delivery


@router.get("/deliveries", response_class=HTMLResponse)
def deliveries_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """配送一覧画面を表示します。"""

    return request.app.state.templates.TemplateResponse(
        request,
        "deliveries.html",
        {"deliveries": list_deliveries(db), "active": "deliveries"},
    )
