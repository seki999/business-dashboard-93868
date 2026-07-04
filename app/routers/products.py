from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import BusinessRuleError
from app.db.database import get_db
from app.db.models import Product
from app.db.schemas import ProductCreate, ProductRead
from app.services.log_service import write_log

router = APIRouter(tags=["products"])


@router.get("/api/products", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)) -> list[Product]:
    """商品データを一覧取得します。"""

    return list(db.scalars(select(Product).order_by(Product.id)))


@router.post("/api/products", response_model=ProductRead, status_code=201)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)) -> Product:
    """商品データを登録し、在庫や公開状態の入力検証を Pydantic に委ねます。"""

    product = Product(**payload.model_dump())
    db.add(product)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise BusinessRuleError("product_code already exists", 409) from exc
    db.refresh(product)
    write_log(db, "application", "INFO", f"商品データを登録しました: {product.product_code}")
    return product


@router.get("/products", response_class=HTMLResponse)
def products_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """商品一覧画面を表示します。"""

    return request.app.state.templates.TemplateResponse(
        "products.html",
        {"request": request, "products": list_products(db), "active": "products"},
    )
