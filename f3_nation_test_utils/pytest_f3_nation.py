import pytest
from collections.abc import Generator
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from f3_nation_test_utils.fixtures import create_test_db_from_defaults

@pytest.fixture
def f3_test_database() -> Generator[Engine, None, None]:
    """Create an in-memory SQLite database with F3 test data loaded from package resources."""
    engine = create_test_db_from_defaults()
    yield engine
    engine.dispose()

@pytest.fixture
def f3_test_session(f3_test_database: Engine) -> Generator[Session, None, None]:
    """Create a SQLAlchemy session connected to the F3 test database."""
    session_factory = sessionmaker(bind=f3_test_database)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
