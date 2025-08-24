import pytest
from sqlalchemy import inspect, text

from f3_nation_test_utils.fixtures import create_test_db_from_defaults


# Direct test of the utility function
def test_create_test_db_from_defaults_creates_tables():
    engine = create_test_db_from_defaults()
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert set(tables) >= {'aos', 'users', 'beatdowns'}
    engine.dispose()


# Test the pytest plugin fixtures
@pytest.mark.usefixtures('f3_test_database')
def test_f3_test_database_fixture(f3_test_database):
    inspector = inspect(f3_test_database)
    tables = inspector.get_table_names()
    assert set(tables) >= {'aos', 'users', 'beatdowns'}


@pytest.mark.usefixtures('f3_test_session')
def test_f3_test_session_fixture(f3_test_session):
    # Should be able to query tables
    result = f3_test_session.execute(text('SELECT COUNT(*) FROM aos')).scalar()
    assert isinstance(result, int)
