import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./test_dashboard.db"
os.environ["ENABLE_SEED_DATA"] = "true"

test_db = Path("test_dashboard.db")
if test_db.exists():
    test_db.unlink()

from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def client() -> TestClient:
    """テスト全体で共有する TestClient です。起動時に seed データも投入されます。"""

    with TestClient(app) as test_client:
        yield test_client
