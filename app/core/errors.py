from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.logging import logger


class BusinessRuleError(Exception):
    """入力値は正しいが、業務ルールとして受け付けられない場合の例外です。"""

    def __init__(self, message: str, status_code: int = 400) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


async def business_rule_exception_handler(
    request: Request, exc: BusinessRuleError
) -> JSONResponse:
    """内部詳細を隠しつつ、利用者に必要なエラー情報だけ返します。"""

    logger.warning("business_rule_error path=%s message=%s", request.url.path, exc.message)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """想定外エラーをログに残し、API レスポンスには汎用メッセージだけ返します。"""

    logger.exception("unhandled_error path=%s", request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
