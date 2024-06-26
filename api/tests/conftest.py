import pytest
import testing.postgresql
from psycopg_pool import ConnectionPool
from authenticator import authenticator

factory = testing.postgresql.PostgresqlFactory(
    cache_initialized_db=True
)


@pytest.fixture(scope="session")
def database_connection():
    # Use factory to create db
    postgresql = factory()

    # parse connection string
    dsn = postgresql.dsn()
    conn_string = (
        f"postgresql://{dsn['user']}@{dsn['host']}:{dsn['port']}/{dsn['database']}"  # noqa
    )

    # connect to db and create users table
    pool = ConnectionPool(open=True, conninfo=conn_string)
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            # Create the users table
            cursor.execute("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY NOT NULL,
                    email VARCHAR(254) NOT NULL UNIQUE,
                    username VARCHAR(100) NOT NULL UNIQUE,
                    name VARCHAR(100) NOT NULL,
                    password VARCHAR(255) NOT NULL UNIQUE
                )
            """)

    with pool.connection() as conn:
        with conn.cursor() as cursor:
            # default user
            cursor.execute(
                """
                INSERT INTO users
                    (
                    email,
                    username,
                    name,
                    password
                    )
                VALUES
                    (
                    'test@basic.com',
                    'basicuser',
                    'John Doe',
                    %s
                    )
                """,
                (authenticator.get_hashed_password("pass"),)
            )

    yield pool

    postgresql.stop()
