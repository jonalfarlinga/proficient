import os
import pytest
from psycopg_pool import ConnectionPool


@pytest.fixture(autouse=True)
def database_connection():
    # Check if running tests

    # Connect to the in-memory database
    pool = ConnectionPool(
        open=True,
        conninfo="postgresql://test:test@localhost:5432/test")

    yield pool
