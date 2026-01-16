import os
from pathlib import Path
from typing import Generator

import pytest
from alembic.config import Config
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer

from alembic import command  # type: ignore[attr-defined]

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_alembic_migrations(database_url: str) -> None:
    alembic_config_path = PROJECT_ROOT / "alembic.ini"
    alembic_cfg = Config(str(alembic_config_path))
    alembic_cfg.set_main_option("sqlalchemy.url", database_url)
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope="session", autouse=True)
def database_url() -> Generator[str, None, None]:
    """
    Start a disposable Postgres container for the whole test session.
    Set DATABASE_URL env var and run Alembic migrations once.
    """
    with PostgresContainer("postgres:15") as postgres:
        raw_url = postgres.get_connection_url()

        sqlalchemy_url = raw_url.replace("postgresql://", "postgresql+psycopg2://")

        os.environ["DATABASE_URL"] = sqlalchemy_url

        run_alembic_migrations(sqlalchemy_url)

        yield sqlalchemy_url


@pytest.fixture()
def api_client(database_url: str) -> TestClient:
    """
    FastAPI TestClient using the application wired to the test database.
    Import app.main only after DATABASE_URL is set and migrations are run.
    """
    from app.main import app

    return TestClient(app)
