from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.models import Delivery, Feedback, ImprovementTask, Product
from app.services.log_service import write_log


def run_daily_batch(db: Session) -> dict[str, object]:
    """日次運用を想定した集計・アラート生成をまとめて実行します。"""

    settings = get_settings()
    today = date.today()

    delayed_deliveries = list(db.scalars(select(Delivery).where(Delivery.status == "delayed")))
    low_stock_products = list(
        db.scalars(select(Product).where(Product.stock_quantity < settings.low_stock_threshold))
    )
    urgent_feedbacks = list(
        db.scalars(select(Feedback).where(Feedback.priority.in_(["high", "urgent"])))
    )
    overdue_tasks = list(
        db.scalars(
            select(ImprovementTask).where(
                ImprovementTask.due_date < today,
                ImprovementTask.progress_status != "done",
            )
        )
    )

    # バッチ結果をログ化することで、運用画面・API・監視設計の接点を示します。
    write_log(
        db,
        "batch",
        "INFO",
        (
            "daily batch completed: "
            f"delayed={len(delayed_deliveries)}, "
            f"low_stock={len(low_stock_products)}, "
            f"urgent_feedbacks={len(urgent_feedbacks)}, "
            f"overdue_tasks={len(overdue_tasks)}"
        ),
    )

    if low_stock_products:
        write_log(db, "batch", "WARN", "低在庫の商品があります。補充計画を確認してください。")
    if delayed_deliveries:
        write_log(db, "batch", "WARN", "遅延中の配送があります。担当チームに確認してください。")

    return {
        "status": "completed",
        "executed_at": today.isoformat(),
        "delayed_deliveries": len(delayed_deliveries),
        "low_stock_products": len(low_stock_products),
        "urgent_feedbacks": len(urgent_feedbacks),
        "overdue_tasks": len(overdue_tasks),
    }
