import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.deps import get_db
from app.main import create_app

# Create in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///:memory:"

engine_test = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


# Override the get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def test_app():
    app = create_app()

    # Create tables in the test DB
    Base.metadata.create_all(bind=engine_test)

    # Apply override
    app.dependency_overrides[get_db] = override_get_db

    return app


@pytest.fixture()
def client(test_app):
    return TestClient(test_app)
