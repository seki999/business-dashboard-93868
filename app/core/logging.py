import logging
from logging.config import dictConfig

from app.core.config import get_settings


def configure_logging() -> None:
    """JSON ではなく読みやすい標準ログを採用し、ローカル検証しやすくします。"""

    settings = get_settings()
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s %(levelname)s [%(name)s] %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                }
            },
            "root": {
                "handlers": ["console"],
                "level": settings.log_level,
            },
        }
    )


logger = logging.getLogger("sample_dashboard")
