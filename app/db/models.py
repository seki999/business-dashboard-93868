from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class TimestampMixin:
    """作成・更新日時を各テーブルで共通管理するための mixin です。"""

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )


class Delivery(Base, TimestampMixin):
    """宅配データを表すモデルです。"""

    __tablename__ = "deliveries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    delivery_code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    area: Mapped[str] = mapped_column(String(80), index=True)
    scheduled_date: Mapped[date] = mapped_column(Date, index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    assignee: Mapped[str] = mapped_column(String(80))
    note: Mapped[str | None] = mapped_column(Text, nullable=True)


class Product(Base, TimestampMixin):
    """商品データと在庫数を表すモデルです。"""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    category: Mapped[str] = mapped_column(String(80), index=True)
    stock_quantity: Mapped[int] = mapped_column(Integer)
    publish_status: Mapped[str] = mapped_column(String(32), index=True)


class Feedback(Base, TimestampMixin):
    """顧客フィードバックを匿名化された業務データとして扱うモデルです。"""

    __tablename__ = "feedbacks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    feedback_code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    feedback_type: Mapped[str] = mapped_column(String(60), index=True)
    content: Mapped[str] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(String(32), index=True)
    response_status: Mapped[str] = mapped_column(String(32), index=True)


class ImprovementTask(Base, TimestampMixin):
    """社内業務改善タスクを管理するモデルです。"""

    __tablename__ = "improvement_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task_code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(160))
    department: Mapped[str] = mapped_column(String(80), index=True)
    priority: Mapped[str] = mapped_column(String(32), index=True)
    progress_status: Mapped[str] = mapped_column(String(32), index=True)
    due_date: Mapped[date] = mapped_column(Date, index=True)


class OperationLog(Base):
    """アプリケーションログ、エラー、バッチ実行結果を画面表示するためのモデルです。"""

    __tablename__ = "operation_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    log_type: Mapped[str] = mapped_column(String(32), index=True)
    level: Mapped[str] = mapped_column(String(16), index=True)
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
