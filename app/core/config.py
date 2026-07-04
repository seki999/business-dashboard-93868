from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """アプリ全体で利用する設定値を環境変数から読み込みます。"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Sample Business Dashboard"
    app_env: str = "local"
    log_level: str = "INFO"
    database_url: str = "sqlite:///./sample_dashboard.db"
    low_stock_threshold: int = Field(default=20, ge=0)
    enable_seed_data: bool = True


@lru_cache
def get_settings() -> Settings:
    """設定インスタンスをキャッシュし、各モジュールで同じ値を参照します。"""

    return Settings()
