from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()


class Base(DeclarativeBase):
    """SQLAlchemy ORM モデルの共通基底クラスです。"""


def _connect_args(database_url: str) -> dict[str, bool]:
    """SQLite のテスト実行時だけ thread 制限を緩和します。"""

    if database_url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


engine = create_engine(settings.database_url, connect_args=_connect_args(settings.database_url))
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency として DB セッションを払い出します。"""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """サンプル用途のため、起動時にテーブル作成と seed 投入を行います。"""

    from app.db import models  # noqa: F401
    from app.db.seed import seed_database

    Base.metadata.create_all(bind=engine)
    if settings.enable_seed_data:
        with SessionLocal() as db:
            seed_database(db)
