import importlib.resources as pkg_resources
import json

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

_resource_pkg = 'f3_nation_test_utils.resources'
default_json_files = {
    'aos': 'aos.json',
    'users': 'users.json',
    'beatdowns': 'beatdowns.json',
}
default_table_schemas = {
    'aos': """
        CREATE TABLE aos (
            channel_id VARCHAR(45) PRIMARY KEY,
            ao VARCHAR(45) NOT NULL,
            channel_created INTEGER NOT NULL,
            archived BOOLEAN NOT NULL,
            backblast BOOLEAN,
            site_q_user_id VARCHAR(45)
        )
    """,
    'users': """
        CREATE TABLE users (
            user_id VARCHAR(45) PRIMARY KEY,
            user_name VARCHAR(45) NOT NULL,
            real_name VARCHAR(45) NOT NULL,
            phone VARCHAR(45),
            email VARCHAR(45),
            start_date DATE,
            app BOOLEAN NOT NULL DEFAULT 0,
            json JSON
        )
    """,
    'beatdowns': """
        CREATE TABLE beatdowns (
            timestamp VARCHAR(45),
            ts_edited VARCHAR(45),
            ao_id VARCHAR(45) NOT NULL,
            bd_date DATE NOT NULL,
            q_user_id VARCHAR(45) NOT NULL,
            coq_user_id VARCHAR(45),
            pax_count INTEGER,
            backblast TEXT,
            backblast_parsed TEXT,
            fngs VARCHAR(45),
            fng_count INTEGER,
            json JSON,
            PRIMARY KEY (ao_id, bd_date, q_user_id)
        )
    """,
}


def create_test_db_from_defaults() -> Engine:
    """Create an in-memory SQLite database and populate it with default F3 Nation test data from package resources."""
    engine = create_engine('sqlite:///:memory:')
    with engine.connect() as conn:
        # Create tables
        for schema in default_table_schemas.values():
            conn.execute(text(schema))
        # Load data from package resources
        for table, filename in default_json_files.items():
            try:
                with (
                    pkg_resources.files(_resource_pkg).joinpath(filename).open('r') as f,
                ):
                    data = json.load(f)
            except (FileNotFoundError, ModuleNotFoundError):  # pragma: no cover
                # Defensive: This should never happen in normal use, since resources are bundled with the library.
                continue
            for row in data:
                # Table and column names are controlled by the library, not user input
                columns = ', '.join(row)
                placeholders = ', '.join(f':{k}' for k in row)
                conn.execute(
                    text(
                        f'INSERT INTO {table} ({columns}) VALUES ({placeholders})',  # noqa: S608 - SQL injection not possible here
                    ),
                    row,
                )
        conn.commit()
    return engine
