from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Delivery, Feedback, ImprovementTask, OperationLog, Product


def seed_database(db: Session) -> None:
    """初回起動時に匿名・架空のサンプルデータを投入します。"""

    if db.scalar(select(Delivery).limit(1)):
        return

    today = date.today()
    db.add_all(
        [
            Delivery(
                delivery_code="D-1001",
                area="North Area",
                scheduled_date=today,
                status="scheduled",
                assignee="Team A",
                note="午前便として確認中",
            ),
            Delivery(
                delivery_code="D-1002",
                area="Central Area",
                scheduled_date=today,
                status="delayed",
                assignee="Team B",
                note="交通状況により遅延",
            ),
            Delivery(
                delivery_code="D-1003",
                area="South Area",
                scheduled_date=today + timedelta(days=1),
                status="in_progress",
                assignee="Team C",
                note=None,
            ),
            Product(
                product_code="P-2001",
                name="Sample Fresh Box",
                category="Food Distribution",
                stock_quantity=14,
                publish_status="published",
            ),
            Product(
                product_code="P-2002",
                name="Sample Daily Set",
                category="Daily Goods",
                stock_quantity=56,
                publish_status="published",
            ),
            Feedback(
                feedback_code="F-3001",
                feedback_type="delivery",
                content="配送予定時間の通知をもう少し早く確認したい。",
                priority="medium",
                response_status="triage",
            ),
            Feedback(
                feedback_code="F-3002",
                feedback_type="product",
                content="在庫切れ表示が分かりにくい。",
                priority="high",
                response_status="new",
            ),
            ImprovementTask(
                task_code="T-4001",
                title="配送遅延アラートの自動通知化",
                department="Operations",
                priority="high",
                progress_status="doing",
                due_date=today + timedelta(days=7),
            ),
            ImprovementTask(
                task_code="T-4002",
                title="在庫しきい値レポートの改善",
                department="Back Office",
                priority="medium",
                progress_status="todo",
                due_date=today + timedelta(days=14),
            ),
            OperationLog(
                log_type="application",
                level="INFO",
                message="サンプルデータを初期投入しました。",
            ),
        ]
    )
    db.commit()
