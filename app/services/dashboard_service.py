from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import Delivery, Feedback, ImprovementTask, OperationLog, Product


def get_dashboard_summary(db: Session) -> dict[str, object]:
    """ダッシュボードに必要な集計値をまとめて作成します。"""

    today = date.today()
    today_orders = db.scalar(
        select(func.count()).select_from(Delivery).where(Delivery.scheduled_date == today)
    )
    scheduled_deliveries = db.scalar(
        select(func.count())
        .select_from(Delivery)
        .where(Delivery.status.in_(["scheduled", "in_progress"]))
    )
    feedback_count = db.scalar(select(func.count()).select_from(Feedback))
    open_tasks = db.scalar(
        select(func.count())
        .select_from(ImprovementTask)
        .where(ImprovementTask.progress_status != "done")
    )
    low_stock = db.scalar(
        select(func.count()).select_from(Product).where(Product.stock_quantity < 20)
    )
    recent_logs = list(
        db.scalars(select(OperationLog).order_by(OperationLog.created_at.desc()).limit(6))
    )

    # API と画面の両方で使えるよう、ログは JSON serializable な辞書へ変換します。
    recent_log_items = [
        {
            "id": log.id,
            "log_type": log.log_type,
            "level": log.level,
            "message": log.message,
            "created_at": log.created_at.isoformat() if log.created_at else None,
        }
        for log in recent_logs
    ]

    return {
        "today_orders": today_orders or 0,
        "scheduled_deliveries": scheduled_deliveries or 0,
        "feedback_count": feedback_count or 0,
        "open_tasks": open_tasks or 0,
        "batch_status": "attention" if low_stock else "normal",
        "low_stock_count": low_stock or 0,
        "recent_logs": recent_log_items,
    }
