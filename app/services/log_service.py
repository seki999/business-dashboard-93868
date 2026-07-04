from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.db.models import OperationLog


def write_log(db: Session, log_type: str, level: str, message: str) -> OperationLog:
    """API・バッチ・エラーのイベントを DB に保存し、運用画面で参照可能にします。"""

    log = OperationLog(log_type=log_type, level=level, message=message)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def list_logs(db: Session, limit: int = 50) -> list[OperationLog]:
    """新しい順で運用ログを取得します。"""

    return list(
        db.scalars(
            select(OperationLog)
            .order_by(desc(OperationLog.created_at))
            .limit(limit)
        )
    )
