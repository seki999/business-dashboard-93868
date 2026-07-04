from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class DeliveryCreate(BaseModel):
    """配送データ作成 API の入力スキーマです。"""

    delivery_code: str = Field(min_length=3, max_length=32)
    area: str = Field(min_length=1, max_length=80)
    scheduled_date: date
    status: str = Field(pattern="^(scheduled|in_progress|delivered|delayed|cancelled)$")
    assignee: str = Field(min_length=1, max_length=80)
    note: str | None = Field(default=None, max_length=1000)


class DeliveryRead(DeliveryCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


class ProductCreate(BaseModel):
    """商品データ作成 API の入力スキーマです。"""

    product_code: str = Field(min_length=3, max_length=32)
    name: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=1, max_length=80)
    stock_quantity: int = Field(ge=0)
    publish_status: str = Field(pattern="^(draft|published|archived)$")


class ProductRead(ProductCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


class FeedbackCreate(BaseModel):
    """顧客フィードバック作成 API の入力スキーマです。"""

    feedback_code: str = Field(min_length=3, max_length=32)
    feedback_type: str = Field(min_length=1, max_length=60)
    content: str = Field(min_length=1, max_length=2000)
    priority: str = Field(pattern="^(low|medium|high|urgent)$")
    response_status: str = Field(pattern="^(new|triage|in_progress|resolved)$")


class FeedbackRead(FeedbackCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


class ImprovementTaskCreate(BaseModel):
    """業務改善タスク作成 API の入力スキーマです。"""

    task_code: str = Field(min_length=3, max_length=32)
    title: str = Field(min_length=1, max_length=160)
    department: str = Field(min_length=1, max_length=80)
    priority: str = Field(pattern="^(low|medium|high|urgent)$")
    progress_status: str = Field(pattern="^(todo|doing|blocked|done)$")
    due_date: date


class ImprovementTaskRead(ImprovementTaskCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


class OperationLogRead(BaseModel):
    """運用ログ API の出力スキーマです。"""

    model_config = ConfigDict(from_attributes=True)
    id: int
    log_type: str
    level: str
    message: str
    created_at: datetime
